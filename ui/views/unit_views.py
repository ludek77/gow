from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ui.models import Unit, CommandType, Game, Turn, Command, Country

def unitResponse(request, unitId):
    selectedGame = Game.objects.get(pk=request.session['selected_game'], user__id=request.user.id)
    selectedTurn = Turn.objects.get(pk=request.session['selected_turn'], game=selectedGame)
    selectedCountry = Country.objects.get(game=selectedGame, owner__id=request.user.id)
    selectedUnit = Unit.objects.get(pk=unitId)
    
    output = '{'

    # public data
    #output += '"pk":'+str(selectedUnit.pk)+','
    output += '"field":"'+selectedUnit.field.name+'"'
    output += ',"country":"'+selectedUnit.country.name+'"'
    output += ',"type":"'+selectedUnit.unitType.name+'"'
    
    # owner restricted data
    selectedUnit = Unit.objects.filter(pk=unitId, country=selectedCountry, turn=selectedTurn)
    if len(selectedUnit) == 1:
        selectedUnit = selectedUnit.first(); 
    
        cmd = Command.objects.filter(turn=selectedTurn, unit=selectedUnit)
        if len(cmd) == 1:
            output += ',"cmd":['+str(cmd[0].commandType.pk)+',['+cmd[0].commandType.template+'],['+cmd[0].args+']]'
        
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
    unitId = request.GET.get("u")
    return unitResponse(request, unitId)

@login_required
def unit_command_rest(request):
    unitId = request.GET.get("u")
    ctid = request.GET.get("ct")
    args = request.GET.get("args")
    selectedGame = Game.objects.get(pk=request.session['selected_game'], user__id=request.user.id)
    selectedTurn = Turn.objects.get(pk=request.session['selected_turn'], game=selectedGame)
    selectedCountry = Country.objects.get(game=selectedGame, owner__id=request.user.id)
    selectedUnit = Unit.objects.get(pk=unitId, country=selectedCountry, turn=selectedTurn)
    selectedCommand = Command.objects.get(unit=selectedUnit, turn=selectedTurn)
    commandType = CommandType.objects.get(pk=ctid)
    selectedCommand.commandType = commandType
    if(args is None):
        args = '';
    selectedCommand.args = args;
    selectedCommand.save()
    
    return unitResponse(request, unitId)