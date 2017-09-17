from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ui.models import Game, Turn, Field, UnitType, City, Unit, Country, CityCommand

@login_required
def country_setup_rest(request):
    selectedGame = Game.objects.get(pk=request.session['selected_game'], user__id=request.user.id)
    selectedCountry = Country.objects.filter(game=selectedGame, owner__id=request.user.id)
    if len(selectedCountry) > 0:
        selectedCountry = selectedCountry.first()
    else:
        selectedCountry = None
    if 'selected_turn' in request.session:
        selectedTurn = Turn.objects.filter(pk=request.session['selected_turn'], game=selectedGame)
        if len(selectedTurn) == 1:
            selectedTurn = selectedTurn.first()
        else:
            selectedTurn = None
    else:
        selectedTurn = None
    output = '{'
    
    if selectedCountry is not None:
        output += '"name":"'+selectedCountry.name+'"'
        output += ',"pk":'+str(selectedCountry.pk)+''
    
    output += ',"units":['
    if selectedTurn is not None:
        units = Unit.objects.filter(country=selectedCountry, turn=selectedTurn)
        separator = ''
        for row in units:
            output += separator+'['+str(row.pk)+','+str(row.unitType.pk)+','+str(row.field.pk)+',"'+row.field.name+'",['+str(row.field.lat)+','+str(row.field.lng)+']]'
            separator = ','
    output += ']'
    
    output += ',"cities":['
    if selectedTurn is not None:
        cmds = CityCommand.objects.filter(city__country=selectedCountry, city__turn=selectedTurn).order_by('priority')
        separator = ''
        for row in cmds:
            output += separator+'['+str(row.city.pk)+',"'+str(row.newUnitType.name)+'",'+str(row.city.field.pk)+',"'+row.city.field.name+'",['+str(row.city.field.lat)+','+str(row.city.field.lng)+']]'
            separator = ','
    output += ']'
    
    output += '}'
    return HttpResponse(output)