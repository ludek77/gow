from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.template import loader
from django.utils import timezone
from ui.models import Game, Turn, Country, Unit
from ui.engine.Engine import Engine
from datetime import datetime
import pytz

def index(request):
    context = {}
    if request.user.is_authenticated:
        if request.session.get('selected_game',None) != None:
            games = Game.objects.filter(user__id=request.user.id,pk=request.session['selected_game'])
            if len(games) == 1:
                context['game'] = games[0]
                countries = Country.objects.filter(owner__id=request.user.id,game=games[0])
                if request.session.get('selected_turn', None) != None:
                    turn = Turn.objects.filter(pk=request.session.get('selected_turn'))
                    if len(turn) == 1:
                        turn = turn.first()
                        now = datetime.now(tz=pytz.utc)
                        if turn.open and turn.deadline and turn.deadline <= now:
                            while turn.deadline <= now:
                                newTurn = Engine().calculateNextTurn(turn)
                                turn = newTurn
                            request.session['selected_turn'] = turn.pk
                        context['turn'] = turn
                        nextTurn=Turn.objects.filter(previous=turn)
                        if len(nextTurn) == 1:
                            context['nextTurn'] = nextTurn
                if len(countries)>0:
                    context['country'] = countries[0]
                if games[0].winner is not None:
                    context['winner'] = games[0].winner
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))

@login_required
def field_dialog(request):
    return HttpResponse(loader.get_template('field_dialog.html').render())

@login_required
@permission_required('change_game')
def new_field_dialog(request):
    return HttpResponse(loader.get_template('new_field_dialog.html').render())

@login_required
@permission_required('game_dialog')
def game_dialog(request):
    return HttpResponse(loader.get_template('game_dialog.html').render())
