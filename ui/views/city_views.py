from django.http import HttpResponse
from ui.models import Game, Turn

def city_get_rest(request):
    selectedGame = Game.objects.get(pk=request.session['selected_game'], user__id=request.user.id)
    output = 'city'
    return HttpResponse(output)