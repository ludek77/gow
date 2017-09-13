from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ui.models import Unit, CommandType, Game, Turn, Command, Country, Field

def unitResponse(request, fieldId):
    selectedGame = Game.objects.get(pk=request.session['selected_game'], user__id=request.user.id)
    selectedTurn = Turn.objects.get(pk=request.session['selected_turn'], game=selectedGame)
    selectedField = Field.objects.get(pk=fieldId)
    selectedUnit = Unit.objects.filter(field__pk=fieldId, turn=selectedTurn)
    
    output = '{'

    # public data
    output += '"field":"'+selectedField.name+'"'
    if len(selectedUnit) == 1:
        output += ',"country":"'+selectedUnit[0].country.name+'"'
        output += ',"type":"'+selectedUnit[0].unitType.name+'"'
    
    # owner restricted data
    selectedCountry = Country.objects.get(game=selectedGame, owner__id=request.user.id)
    selectedUnit = Unit.objects.filter(field__pk=fieldId, country=selectedCountry, turn=selectedTurn)
    if len(selectedUnit) == 1:
        selectedUnit = selectedUnit.first(); 
    
        cmd = Command.objects.filter(turn=selectedTurn, unit=selectedUnit)
        if len(cmd) == 1:
            output += ',"cmd":['+str(cmd[0].commandType.pk)+',['+cmd[0].commandType.template+'],['
            if cmd[0].args != '':
                flds = cmd[0].args.split(',')
                separator = ''
                for fld in flds:
                    f = Field.objects.get(pk=fld)
                    output += separator+'['+str(f.pk)+',"'+f.name+'"]'
                    separator = ','
            output += ']]'
        
        cmds = CommandType.objects.filter(unitType=selectedUnit.unitType)
        output += ',"cmds":['
        separator = ''
        for row in cmds:
            output += separator+'['+str(row.id)+',"'+row.name+'"]'
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
    selectedTurn = Turn.objects.get(pk=request.session['selected_turn'], game=selectedGame)
    selectedCountry = Country.objects.get(game=selectedGame, owner__id=request.user.id)
    selectedUnit = Unit.objects.get(field__pk=fieldId, country=selectedCountry, turn=selectedTurn)
    selectedCommand = Command.objects.get(unit=selectedUnit, turn=selectedTurn)
    commandType = CommandType.objects.get(pk=ctid)
    selectedCommand.commandType = commandType
    if(args is None):
        args = '';
    selectedCommand.args = args;
    selectedCommand.save()
    
    return unitResponse(request, fieldId)