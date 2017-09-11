from django.http import HttpResponse
from ui.models import Game, Turn

def unit_get_rest(request):
    selectedGame = Game.objects.get(pk=request.session['selected_game'], user__id=request.user.id)
    output = 'unit'
    return HttpResponse(output)