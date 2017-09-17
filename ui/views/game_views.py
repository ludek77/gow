from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from ui.models import Game, Turn, Field, UnitType, City, Unit, Country, CityCommand

@login_required
def game_list_rest(request):
    list = Game.objects.filter(user__id=request.user.id)
    output = '[' + ','.join(['{"name":"'+row.name+'","id":"'+str(row.id)+'"}' for row in list]) + ']'
    return HttpResponse(output)

@login_required
def game_select_rest(request):
    game = request.GET.get("g")
    g = Game.objects.filter(pk=game, user__id=request.user.id)
    if len(g) == 1: 
        request.session['selected_game'] = str(g[0].id)
        
        turns = Turn.objects.filter(game=g[0], open=True)
        if len(turns) == 1:
            request.session['selected_turn'] = str(turns[0].id)
        else:
            request.session['selected_turn'] = 0
    return HttpResponse('OK')

@login_required
def game_setup_rest(request):
    selectedGame = Game.objects.get(pk=request.session['selected_game'], user__id=request.user.id)
    if 'selected_turn' in request.session:
        selectedTurn = Turn.objects.filter(pk=request.session['selected_turn'], game=selectedGame)
        if len(selectedTurn) == 1:
            selectedTurn = selectedTurn.first()
        else:
            selectedTurn = None
    else:
        selectedTurn = None
    output = '{'
    
    unitTypes = UnitType.objects.all()
    output += '"unitTypes":['
    separator = ''
    for row in unitTypes:
        output += separator+'['+str(row.pk)+',"'+row.icon+'",'+str(row.width)+','+str(row.height)+',"'+row.name+'"]'
        separator = ','
    output += ']'
    
    fields = Field.objects.filter(game=selectedGame)
    if selectedTurn is not None:
        cities = City.objects.filter(turn=selectedTurn)
    else:
        cities = None
    output += ',"fields":['
    separator = ''
    for row in fields:
        color = '';
        if(row.isCity):
            color='-'
        if cities is not None:
            city = cities.filter(field=row)
            if len(city)==1:
                color = city[0].country.color
        output += separator+'['+str(row.pk)+',['+str(row.lat)+','+str(row.lng)+'],"'+color+'"]'
        separator = ','
    output += ']'
    
    output += ',"paths":['
    separator = ''
    for f in fields:
        for n in f.next.all():
            if(n.pk < f.pk):
                output += separator+'[['+str(f.lat)+','+str(f.lng)+'],['+str(n.lat)+','+str(n.lng)+'],'+str(f.pk)+','+str(n.pk)+']'
                separator = ','
    output += ']'
    
    if selectedTurn is not None:
        units = Unit.objects.filter(turn=selectedTurn)
        output += ',"units":['
        separator = ''
        for row in units:
            output += separator+'['+str(row.pk)+','+str(row.field.pk)+',['+str(row.field.lat)+','+str(row.field.lng)+'],"'+row.country.color+'",'+str(row.unitType.pk)+']'
            separator = ','
        output += ']'
    
    output += '}'
    return HttpResponse(output)

@login_required
@permission_required('game_start')
def game_start_rest(request):
    gname = request.GET.get("g")
    tname = request.GET.get("t")
    selectedGame = Game.objects.get(pk=request.session['selected_game'], user__id=request.user.id)
    #create game
    newGame = Game()
    newGame.name = gname
    newGame.tileServer = selectedGame.tileServer
    newGame.save()
    for u in selectedGame.user.all():
        newGame.user.add(u)
    newGame.save()
    #initialize countries
    countries = Country.objects.filter(game=selectedGame)
    for c in countries:
        c.pk = None
        c.game = newGame
        c.save()
    #create initial turn
    newTurn = Turn()
    newTurn.name = tname
    newTurn.game = newGame
    newTurn.open = True
    newTurn.newUnits = True
    newTurn.save()
    #initialize fields
    fields = Field.objects.filter(game=selectedGame)
    for f in fields:
        newField = Field()
        newField.name = f.name
        newField.type = f.type
        newField.game = newGame
        newField.lat = f.lat
        newField.lng = f.lng
        newField.defaultPriority = f.defaultPriority
        newField.defaultUnitType = f.defaultUnitType
        if f.home is not None:
            newField.home = Country.objects.get(game=newGame, name=f.home.name)
        newField.isCity = f.isCity
        newField.save()
        if newField.isCity and newField.home is not None:
            newCity = City()
            newCity.turn = newTurn
            newCity.field = newField
            newCity.country = newField.home
            newCity.save()
            #initial command
            newCityCommand = CityCommand()
            newCityCommand.city = newCity
            newCityCommand.priority = newField.defaultPriority
            newCityCommand.newUnitType = newField.defaultUnitType
            newCityCommand.save()
        for f_next in f.next.all():
            newList = Field.objects.filter(game=newGame, name=f_next.name)
            if len(newList) > 0:
                newField.next.add(newList.first())
        newField.save()
    request.session['selected_game'] = str(newGame.id)
    request.session['selected_turn'] = str(newTurn.id)
    return HttpResponse()
