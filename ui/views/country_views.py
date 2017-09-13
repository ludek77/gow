from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ui.models import Game, Turn, Field, UnitType, City, Unit, Country

@login_required
def country_setup_rest(request):
    selectedGame = Game.objects.get(pk=request.session['selected_game'], user__id=request.user.id)
    selectedCountry = Country.objects.get(game=selectedGame, owner__id=request.user.id)
    selectedTurn = Turn.objects.get(pk=request.session['selected_turn'], game=selectedGame)
    output = '{'
    
    output += '"name":"'+selectedCountry.name+'",'
    output += '"pk":'+str(selectedCountry.pk)+','
    
    output += '"units":['
    units = Unit.objects.filter(country=selectedCountry, turn=selectedTurn)
    separator = ''
    for row in units:
        output += separator+'['+str(row.pk)+','+str(row.unitType.pk)+','+str(row.field.pk)+',"'+row.field.name+'"]'
        separator = ','
    output += ']'
    
    output += '}'
    return HttpResponse(output)