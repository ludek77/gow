from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from ui.models import Game, Turn

@login_required
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
        #if games available, select first
        games = Game.objects.filter(user__id=request.user.id).order_by('pk')
        if len(games) > 0:
            request.session['selected_game'] = str(games[0].id)
            
            turns = Turn.objects.filter(game=games[0]).order_by('-deadline')
            if len(turns) > 0:
                request.session['selected_turn'] = str(turns[0].id)
        return HttpResponse('OK')
    else:
        return HttpResponse('Invalid username or password', status=401)
