from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ui.models import Unit, CommandType, Game, Turn, Command, Country, Field, City, CityCommand, UnitType
from ui.engine.CommandValidator import CommandValidator

def unitResponse(request, fieldId):
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

    # public data
    output += '"field":"'+selectedField.name+'"'
    output += ',"type":"'+selectedField.type.name+'"'
    if selectedField.isCity:
        city = City.objects.get(turn=selectedTurn, field=selectedField)
        output += ',"country":"'+city.country.name+'"'
    if selectedTurn is not None and selectedTurn.open:
        output += ',"open":true'
    else:
        output += ',"open":false'
    if selectedUnit is not None:
        output += ',"unitCountry":"'+selectedUnit.country.name+'"'
        output += ',"unitType":"'+selectedUnit.unitType.name+'"'
    
    # owner restricted data if turn is open
    if selectedTurn is not None:
        selectedCountry = Country.objects.get(game=selectedGame, owner__id=request.user.id)
        if selectedTurn.open:
            selectedUnit = Unit.objects.filter(field__pk=fieldId, country=selectedCountry, turn=selectedTurn)
        else:
            selectedUnit = Unit.objects.filter(field__pk=fieldId, turn=selectedTurn)
        if len(selectedUnit) == 1:
            selectedUnit = selectedUnit.first(); 
        
            cmd = Command.objects.filter(turn=selectedTurn, unit=selectedUnit)
            if len(cmd) == 1:
                cmd = cmd.first()
                output += ',"cmd":['+str(cmd.commandType.pk)+',['+cmd.commandType.template+'],['
                if cmd.args != '':
                    flds = cmd.args.split(',')
                    separator = ''
                    for fld in flds:
                        if fld != '0' and fld != '':
                            f = Field.objects.get(pk=fld)
                            fpk = f.pk
                            fname = f.name
                        else:
                            fpk = 0
                            fname = ''
                        output += separator+'['+str(fpk)+',"'+fname+'"]'
                        separator = ','
                output += ']'
                result = ''
                if cmd.result is not None:
                    result = CommandValidator().getResult(cmd)
                output += ',"'+result+'"'
                output += ']'
            
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
                    output += ',"fcmd":"'+str(cityCommand.newUnitType.pk)+'"'
                    newTypes = UnitType.objects.filter(fieldTypes=selectedField.type)
                    output += ', "fcmds":['
                    separator = ''
                    for type in newTypes:
                        output += separator+'['+str(type.pk)+',"'+type.name+'"]'
                        separator = ','
                    output += ']'    
    output += '}'
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
    selectedGame = Game.objects.get(pk=request.session['selected_game'], user__id=request.user.id)
    selectedTurn = Turn.objects.get(pk=request.session['selected_turn'], game=selectedGame, open=True)
    selectedCountry = Country.objects.get(game=selectedGame, owner__id=request.user.id)
    selectedUnit = Unit.objects.get(field__pk=fieldId, country=selectedCountry, turn=selectedTurn)
    selectedCommand = Command.objects.get(unit=selectedUnit, turn=selectedTurn)
    commandType = CommandType.objects.get(pk=ctid)
    selectedCommand.commandType = commandType
    if(args is None):
        args = '';
    selectedCommand.args = args;
    # validate command
    validator = CommandValidator()
    validator.validateCommand(selectedCommand)
    #save command
    selectedCommand.save()
    
    return unitResponse(request, fieldId)

@login_required
def city_command_rest(request):
    fieldId = request.GET.get("f")
    ctid = request.GET.get("ct")
    selectedGame = Game.objects.get(pk=request.session['selected_game'], user__id=request.user.id)
    selectedTurn = Turn.objects.get(pk=request.session['selected_turn'], game=selectedGame, open=True)
    selectedCountry = Country.objects.get(game=selectedGame, owner__id=request.user.id)
    selectedCity = City.objects.get(field__pk=fieldId, country=selectedCountry, turn=selectedTurn)
    selectedCommand = CityCommand.objects.get(city=selectedCity)
    newUnitType = UnitType.objects.get(pk=ctid)
    selectedCommand.newUnitType = newUnitType
    selectedCommand.save()
    
    return unitResponse(request, fieldId)