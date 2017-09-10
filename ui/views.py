from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import Game, Turn, Field

def game_list_rest(request):
    list = Game.objects.filter(user__id=request.user.id)
    output = '[' + ', '.join(['{"name":"'+row.name+'","id":"'+str(row.id)+'"}' for row in list]) + ']'
    return HttpResponse(output)

def game_select_rest(request):
    game = request.GET.get("g")
    g = Game.objects.filter(pk=game, user__id=request.user.id)
    if len(g) == 1: 
        request.session['selected_game'] = str(g[0].id)
    return HttpResponse('OK')

def game_setup_rest(request):
    g = Game.objects.get(pk=request.session['selected_game'], user__id=request.user.id)
    t = Turn.objects.get(game=g,open=True)
    output = '['
    
    fields = Field.objects.filter(game=g)
    output += ', '.join(['{"f":"'+row.name+'","l":['+str(row.lon)+","+str(row.lat)+']}' for row in fields])
    
    output += ']'
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
        list = Game.objects.filter(user__id=request.user.id)
        if len(list) >= 1:
            request.session['selected_game'] = str(list[0].id)
        return HttpResponse('OK')
    else:
        return HttpResponse('Invalid username or password', status=401)

def index(request):
    return render(request, 'index.html')
