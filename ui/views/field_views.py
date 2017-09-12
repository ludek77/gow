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

@login_required
@permission_required('change_game')
def path_add_rest(request):
    pk1 = request.GET.get("f1")
    pk2 = request.GET.get("f2")
    selectedGame = Game.objects.get(pk=request.session['selected_game'], user__id=request.user.id)
    field1 = Field.objects.get(pk=pk1)
    field2 = Field.objects.get(pk=pk2)
    field1.next.add(field2)
    field1.save()
    output = '{'
    output += '"pk1":'+pk1+','
    output += '"pk2":'+pk2+','
    output += '"ll1":['+str(field1.lat)+','+str(field1.lng)+'],'
    output += '"ll2":['+str(field2.lat)+','+str(field2.lng)+']'
    output += '}'
    return HttpResponse(output)

@login_required
@permission_required('change_game')
def path_delete_rest(request):
    pk1 = request.GET.get("f1")
    pk2 = request.GET.get("f2")
    selectedGame = Game.objects.get(pk=request.session['selected_game'], user__id=request.user.id)
    field1 = Field.objects.get(pk=pk1)
    field2 = Field.objects.get(pk=pk2)
    field1.next.remove(field2)
    field1.save()
    output = '{'
    output += '"pk1":'+pk1+','
    output += '"pk2":'+pk2
    output += '}'
    return HttpResponse(output)