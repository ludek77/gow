from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from ui.models import Game, Field, FieldType

@login_required
@permission_required('change_game')
def field_add_rest(request):
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")
    selectedGame = Game.objects.get(pk=request.session['selected_game'], user__id=request.user.id)
    field = Field()
    field.name = ''
    field.type = FieldType.objects.first()
    field.game = selectedGame
    field.lat = lat
    field.lng = lng
    field.isCity = False
    field.save()
    output = '{'
    output += '"pk":'+str(field.pk)+','
    output += '"lat":'+str(field.lat)+','
    output += '"lng":'+str(field.lng)    
    output += '}'
    return HttpResponse(output)

@login_required
@permission_required('change_game')
def field_delete_rest(request):
    pk = request.GET.get("pk")
    selectedGame = Game.objects.get(pk=request.session['selected_game'], user__id=request.user.id)
    field = Field.objects.get(pk=pk)
    field.delete()
    return HttpResponse('OK')