from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from ui.models import Game, Turn, Country, Unit

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
        output += separator+'['+str(row.pk)+','+str(row.unitType.pk)+']'
        separator = ','
    output += ']'
    
    output += '}'
    return HttpResponse(output)

def index(request):
    context = {}
    if request.user.is_authenticated:
        if request.session.get('selected_game',None) != None:
            games = Game.objects.filter(user__id=request.user.id,pk=request.session['selected_game'])
            if len(games) == 1:
                context['game'] = games[0]
                countries = Country.objects.filter(owner__id=request.user.id,game=games[0])
                if len(countries)>0:
                    context['country'] = countries[0]
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))
