from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ui.models import Unit, CommandType, Game, Turn, Command, Country, Field, City, CityCommand, UnitType
from ui.engine.CommandValidator import CommandValidator
from ui.engine.MapProcessor import MapProcessor
from django.utils import timezone

def unitResponse(request, fieldId,message=None):
    selectedGame = Game.objects.get(pk=request.session['selected_game'], user__id=request.user.id)
    selectedField = Field.objects.get(pk=fieldId)
    if 'selected_turn' in request.session:
        selectedTurn = Turn.objects.get(pk=request.session['selected_turn'], game=selectedGame)
        selectedUnit = Unit.objects.filter(field__pk=fieldId, turn=selectedTurn)
        if len(selectedUnit) == 1:
            selectedUnit = selectedUnit.first()
        else:
            selectedUnit = None
    else:
        selectedTurn = None
        selectedUnit = None
    
    output = '{'

    # field public data
    output += '"field":{'
    output += '"name":"'+selectedField.name+'"'
    output += ',"ll":['+str(selectedField.lat)+','+str(selectedField.lng)+']'
    output += ',"type":"'+selectedField.type.name+'"'
    if selectedField.isCity:
        city = City.objects.filter(turn=selectedTurn, field=selectedField)
        if len(city) == 1:
            output += ',"owner":{'
            output += '"country":"'+city[0].country.name+'"'
            output += ',"color":"'+city[0].country.color+'"'
            output += ',"textColor":"'+city[0].country.fgcolor+'"'
            output += '}'
        if selectedField.home is not None:
            output += ',"home":{'
            output += '"name":"'+selectedField.home.name+'"'
            output += ',"color":"'+selectedField.home.color+'"'
            output += ',"textColor":"'+selectedField.home.fgcolor+'"'
            output += '}'
    output += '}'
    
    if selectedTurn is not None and selectedTurn.open:
        output += ',"open":true'
    else:
        output += ',"open":false'
        
    if selectedUnit is not None:
        output += ',"unit":{'
        output += '"country":"'+selectedUnit.country.name+'"'
        output += ',"color":"'+selectedUnit.country.color+'"'
        output += ',"textColor":"'+selectedUnit.country.fgcolor+'"'
        output += ',"type":"'+selectedUnit.unitType.name+'"'
        output += '}'
        
    if message is not None:
        output += ',"message":"'+message+'"'
    
    # owner restricted data if turn is open
    if selectedTurn is not None:
        commandValidator = CommandValidator()
        selectedCountry = Country.objects.get(game=selectedGame, owner__id=request.user.id)
        if selectedTurn.open:
            selectedUnit = Unit.objects.filter(field__pk=fieldId, country=selectedCountry, turn=selectedTurn)
        else:
            selectedUnit = Unit.objects.filter(field__pk=fieldId, turn=selectedTurn)
        if len(selectedUnit) == 1:
            selectedUnit = selectedUnit.first(); 
        
            cmd = Command.objects.filter(unit__turn=selectedTurn, unit=selectedUnit)
            if len(cmd) == 1:
                cmd = cmd.first()
                # append command
                output += ',"command":{'
                output += '"pk":'+str(cmd.commandType.pk)
                output += ',"name":"'+cmd.commandType.name+'"'
                output += ',"template":['+cmd.commandType.template+']'
                if cmd.result is not None:
                    result = commandValidator.getResult(cmd)
                    output += ',"result":"'+result+'"'
                # append arguments
                if cmd.args != '':
                    output += ',"args":['
                    flds = cmd.args.split(',')
                    separator = ''
                    for fld in flds:
                        if fld != '0' and fld != '':
                            f = Field.objects.get(pk=fld)
                            output += separator+'{'
                            output += '"pk":'+str(f.pk)
                            output += ',"name":"'+f.name+'"'
                            output += ',"ll":['+str(f.lat)+','+str(f.lng)+']'
                            output += '}'
                        else:
                            output += separator+'{0,"",[0,0]}'
                        separator = ','
                    output += ']'
                #append escape
                if cmd.escape is not None:
                    escapes = cmd.escape.split(',')
                    if escapes[0] is not None and escapes[0] != '':
                        f = Field.objects.get(pk=escapes[0])
                        if f is not None:
                            output += ',"escape":{'
                            output += '"pk":'+str(f.pk)
                            output += ',"name":"'+f.name+'"'
                            output += '}'
                output += "}"
            
            cmds = CommandType.objects.filter(unitType=selectedUnit.unitType)
            output += ',"cmds":['
            separator = ''
            for row in cmds:
                output += separator+'['+str(row.id)+',"'+row.name+'"]'
                separator = ','
            output += ']'
        if selectedTurn.open:
            selectedCity = City.objects.filter(field__pk=fieldId, country=selectedCountry, turn=selectedTurn)
        else:
            selectedCity = City.objects.filter(field__pk=fieldId, turn=selectedTurn)
        if len(selectedCity) == 1:
            selectedCity = selectedCity.first()
            if selectedField.isCity and selectedCity.country == selectedField.home:
                cityCommand = CityCommand.objects.filter(city=selectedCity)
                if len(cityCommand) == 1:
                    cityCommand = cityCommand.first()
                    output += ',"citycommand":{'
                    output += '"pk":"'+str(cityCommand.newUnitType.pk)+'"'
                    if cityCommand.result is not None:
                        output += ',"result":"'+commandValidator.getResult(cityCommand)+'"'
                    newTypes = UnitType.objects.filter(fieldTypes=selectedField.type)
                    output += ',"fcmds":['
                    separator = ''
                    for type in newTypes:
                        output += separator+'['+str(type.pk)+',"'+type.name+'"]'
                        separator = ','
                    output += '}'    
    output += '}'
#     print(output)
    return HttpResponse(output)

@login_required
def unit_get_rest(request):
    fieldId = request.GET.get("f")
    return unitResponse(request, fieldId)

@login_required
def unit_command_rest(request):
    fieldId = request.GET.get("f")
    ctid = request.GET.get("ct")
    args = request.GET.get("args")
    validator = CommandValidator()
    messageKey = None
    selectedGame = Game.objects.get(pk=request.session['selected_game'], user__id=request.user.id)
    selectedTurn = Turn.objects.get(pk=request.session['selected_turn'], game=selectedGame, open=True)
    if selectedTurn.deadline is None or selectedTurn.deadline > timezone.now():
        selectedCountry = Country.objects.get(game=selectedGame, owner__id=request.user.id)
        selectedUnit = Unit.objects.get(field__pk=fieldId, country=selectedCountry, turn=selectedTurn)
        selectedCommand = Command.objects.get(unit=selectedUnit)
        # changing remove priority
        if ctid == 'prio':
            commands = Command.objects.filter(unit__turn=selectedTurn,unit__country=selectedCountry).order_by('removePriority')
            processor = MapProcessor(selectedTurn)
            processor.orderCommand(selectedCommand, int(args), commands)
        # chaing escape priority
        elif ctid == 'esc':
            escape = Field.objects.get(pk=int(args))
            processor = MapProcessor(selectedTurn)
            messageKey = processor.setPriorityEscape(selectedCommand, escape)
        # setting command and arguments
        else:
            commandType = CommandType.objects.get(pk=ctid)
            selectedCommand.commandType = commandType
            if(args is None):
                args = '';
            selectedCommand.args = args;
            # validate command
            validator.validateCommand(selectedCommand)
            #save command
            selectedCommand.save()
    else:
        messageKey = 'fail.turn-closed' 

    message = validator.getError(messageKey)
    return unitResponse(request, fieldId, message)

@login_required
def city_command_rest(request):
    fieldId = request.GET.get("f")
    ctid = request.GET.get("ct")
    args = request.GET.get("args")
    validator = CommandValidator()
    message = None
    selectedGame = Game.objects.get(pk=request.session['selected_game'], user__id=request.user.id)
    selectedTurn = Turn.objects.get(pk=request.session['selected_turn'], game=selectedGame, open=True)
    if selectedTurn.deadline is None or selectedTurn.deadline > timezone.now():
        selectedCountry = Country.objects.get(game=selectedGame, owner__id=request.user.id)
        selectedCity = City.objects.get(field__pk=fieldId, country=selectedCountry, turn=selectedTurn)
        selectedCommand = CityCommand.objects.get(city=selectedCity)
        if ctid == 'prio':
            commands = CityCommand.objects.filter(city__turn=selectedTurn,city__country=selectedCountry).order_by('priority')
            processor = MapProcessor(selectedTurn)
            processor.orderCommand(selectedCommand, int(args), commands)
        else:
            newUnitType = UnitType.objects.get(pk=ctid)
            selectedCommand.newUnitType = newUnitType
            #validate command
            validator.validateCityCommand(selectedCommand)
            #save command
            selectedCommand.save()
    else:
        message = 'fail.turn-closed'
        
    return unitResponse(request, fieldId, message)