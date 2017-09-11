from django.http import HttpResponse
from ui.models import Game, Turn, Field, UnitType, City, Unit

def game_list_rest(request):
    list = Game.objects.filter(user__id=request.user.id)
    output = '[' + ','.join(['{"name":"'+row.name+'","id":"'+str(row.id)+'"}' for row in list]) + ']'
    return HttpResponse(output)

def game_select_rest(request):
    game = request.GET.get("g")
    g = Game.objects.filter(pk=game, user__id=request.user.id)
    if len(g) == 1: 
        request.session['selected_game'] = str(g[0].id)
    return HttpResponse('OK')

def game_setup_rest(request):
    selectedGame = Game.objects.get(pk=request.session['selected_game'], user__id=request.user.id)
    selectedTurn = Turn.objects.get(pk=request.session['selected_turn'], game=selectedGame)
    output = '{'
    
    unitTypes = UnitType.objects.all()
    output += '"unitTypes":['
    separator = ''
    for row in unitTypes:
        output += separator+'['+str(row.pk)+',"'+row.icon+'",'+str(row.width)+','+str(row.height)+']'
        separator = ','
    output += '],'
    
    fields = Field.objects.filter(game=selectedGame)
    cities = City.objects.filter(turn=selectedTurn)
    output += '"fields":['
    separator = ''
    for row in fields:
        color = '';
        if(row.isCity):
            color='-'
        city = cities.filter(field=row)
        if len(city)==1:
            color = city[0].country.color
        output += separator+'['+str(row.pk)+',['+str(row.lat)+','+str(row.lng)+'],"'+color+'"]'
        separator = ','
    output += '],'
    
    output += '"paths":['
    separator = ''
    for f in fields:
        for n in f.next.all():
            if(n.pk < f.pk):
                output += separator+'[['+str(f.lat)+','+str(f.lng)+'],['+str(n.lat)+','+str(n.lng)+']]'
                separator = ','
    output += '],'
    
    units = Unit.objects.filter(turn=selectedTurn)
    output += '"units":['
    separator = ''
    for row in units:
        output += separator+'['+str(row.pk)+',['+str(row.field.lat)+','+str(row.field.lng)+'],"'+row.country.color+'",'+str(row.unitType.pk)+']'
        separator = ','
    output += ']'
    
    output += '}'
    return HttpResponse(output)
