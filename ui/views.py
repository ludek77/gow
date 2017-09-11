from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.template import loader
from .models import Game, Turn, Field, Country, UnitType, City, Unit

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
        output += separator+'['+str(row.pk)+',"'+row.icon+'"]'
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
            color = city[0].color
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
    print(output)
    return HttpResponse(output)

def logout_rest(request):
    logout(request)
    return HttpResponse("Logged out")

def login_rest(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        #login
        login(request, user)
        #if one game available, select it
        games = Game.objects.filter(user__id=request.user.id)
        if len(games) >= 1:
            request.session['selected_game'] = str(games[0].id)
            
            turns = Turn.objects.filter(game=games[0], open=True)
            if len(turns) == 1:
                request.session['selected_turn'] = str(turns[0].id)
        return HttpResponse('OK')
    else:
        return HttpResponse('Invalid username or password', status=401)

def index(request):
    #return render(request, 'index.html')
    context = {}
    if request.session.get('selected_game',None) != None:
        games = Game.objects.filter(user__id=request.user.id,pk=request.session['selected_game'])
        if len(games) == 1:
            context['game'] = games[0]
            countries = Country.objects.filter(owner__id=request.user.id,game=games[0])
            if len(countries)>0:
                context['country'] = countries[0]
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))
