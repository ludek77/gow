from django.http import HttpResponse
from ui.models import Unit, CommandType, Game, Turn, Command, Country

def unit_get_rest(request):
    uid = request.GET.get("u")
    selectedGame = Game.objects.get(pk=request.session['selected_game'], user__id=request.user.id)
    selectedTurn = Turn.objects.get(pk=request.session['selected_turn'], game=selectedGame)
    selectedCountry = Country.objects.get(game=selectedGame, owner__id=request.user.id)
    selectedUnit = Unit.objects.get(pk=uid)
    output = '{'

    # public data
    #output += '"pk":'+str(selectedUnit.pk)+','
    output += '"field":"'+selectedUnit.field.name+'"'
    output += ',"country":"'+selectedUnit.country.name+'"'
    output += ',"type":"'+selectedUnit.unitType.name+'"'
    
    # owner restricted data
    selectedUnit = Unit.objects.filter(pk=uid, country=selectedCountry, turn=selectedTurn)
    if len(selectedUnit) == 1:
        selectedUnit = selectedUnit.first(); 
    
        cmd = Command.objects.filter(turn=selectedTurn, unit=selectedUnit)
        if len(cmd) == 1:
            output += ',"cmd":'+str(cmd[0].pk)
        
        cmds = CommandType.objects.filter(unitType=selectedUnit.unitType)
        output += ',"cmds":['
        separator = ''
        for row in cmds:
            output += separator+'['+str(row.id)+',"'+row.name+'"]'
            separator = ','
        output += ']'

    output += '}'
    return HttpResponse(output)