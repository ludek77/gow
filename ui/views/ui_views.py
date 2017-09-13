from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.template import loader
from ui.models import Game, Turn, Country, Unit

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

@login_required
def unit_dialog(request):
    return HttpResponse(loader.get_template('unit_dialog.html').render())

@login_required
def city_dialog(request):
    return HttpResponse(loader.get_template('city_dialog.html').render())

@login_required
@permission_required('change_game')
def new_field_dialog(request):
    return HttpResponse(loader.get_template('new_field_dialog.html').render())