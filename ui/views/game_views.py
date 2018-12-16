from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from ui.models import Game, Turn, Field, UnitType, City, Unit, Country, CityCommand, Command
from ui.engine.TurnProcessor import TurnProcessor
from ui.engine.Engine import Engine

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
        output += separator+'['
        output += str(row.pk)
        output += ',"'+row.icon+'"'
        output += ','+str(row.width)
        output += ','+str(row.height)+','
        output += '"'+row.name+'"'
        output += ']'
        separator = ','
    output += ']'
    
    fields = Field.objects.filter(game=selectedGame)
    if selectedTurn is not None:
        cities = City.objects.filter(turn=selectedTurn)
    else:
        cities = None
    output += ',"fields":['
    separator = ''
    for field in fields:
        color = ''
        currentCountry = None
        if(field.isCity):
            color='-'
        if cities is not None:
            city = cities.filter(field=field)
            if len(city)==1:
                color = city[0].country.color
                currentCountry = city[0].country
        output += separator+'{'
        output += '"id":'+str(field.pk)
        output += ',"latlng":['+str(field.lat)+','+str(field.lng)+']'
        output += ',"color":"'+color+'"'
        if field.home is not None and field.home == currentCountry:
            output += ',"home":true'
        output += '}'
        separator = ','
    output += ']'
    
    output += ',"paths":['
    separator = ''
    for f in fields:
        for n in f.next.all():
            if(n.pk < f.pk):
                output += separator+'['
                output += '['+str(f.lat)+','+str(f.lng)+']'
                output += ',['+str(n.lat)+','+str(n.lng)+']'
                output += ','+str(f.pk)
                output += ','+str(n.pk)
                output += ']'
                separator = ','
    output += ']'
    
    if selectedTurn is not None:
        engine = Engine()
        engine.initialize(selectedTurn)
        selectedCountry = Country.objects.get(game=selectedGame, owner__id=request.user.id)
        commands = Command.objects.filter(unit__turn=selectedTurn).order_by('removePriority')
        output += ',"units":['
        separator = ''
        for command in commands:
            unit = command.unit
            field = unit.field
            output += separator+'{'
            output += '"id":'+str(unit.pk)
            output += ',"fid":'+str(field.pk)
            output += ',"latlng":['+str(field.lat)+','+str(field.lng)+']'
            output += ',"clr":"'+unit.country.color+'"'
            output += ',"type":'+str(unit.unitType.pk)
            output += ',"cmd":"'+command.commandType.name+'"'
            if unit.country == selectedCountry or not selectedTurn.open:
                targets = engine.getTargetFields(command)
                if len(targets) > 0:
                    output += ',"tgt":['
                    ssep = ''
                    for target in targets:
                        output += ssep+'['+str(target.lat)+','+str(target.lng)+']'
                        ssep = ','
                    output += ']'
                if command.result is not None:
                    idx = command.result.find('.')
                    output += ',"res":"'+command.result[:idx]+'"'
            output +='}'
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
    # create new game
    newGame = TurnProcessor().startGame(selectedGame, gname, tname)
    newTurn = Turn.objects.get(game=newGame)
    # set is as active
    request.session['selected_game'] = str(newGame.id)
    request.session['selected_turn'] = str(newTurn.id)
    return HttpResponse()

@login_required
def turn_previous_rest(request):
    selectedGame = Game.objects.get(pk=request.session['selected_game'], user__id=request.user.id)
    if 'selected_turn' in request.session:
        selectedTurn = Turn.objects.filter(pk=request.session['selected_turn'], game=selectedGame)
        if len(selectedTurn) == 1:
            selectedTurn = selectedTurn.first()
            if selectedTurn.previous is not None:
                request.session['selected_turn'] = selectedTurn.previous.pk
    return HttpResponse()

@login_required
def turn_next_rest(request):
    selectedGame = Game.objects.get(pk=request.session['selected_game'], user__id=request.user.id)
    if 'selected_turn' in request.session:
        selectedTurn = Turn.objects.filter(previous__pk=request.session['selected_turn'], game=selectedGame)
        if len(selectedTurn) == 1:
            selectedTurn = selectedTurn.first()
            if selectedTurn is not None:
                request.session['selected_turn'] = selectedTurn.pk
    return HttpResponse()