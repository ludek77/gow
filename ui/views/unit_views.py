from django.http import HttpResponse
from ui.models import Unit

def unit_get_rest(request):
    uid = request.GET.get("u")
    selectedUnit = Unit.objects.get(pk=uid)
    output = '{'
    #output += '"pk":'+str(selectedUnit.pk)+','
    output += '"field":"'+selectedUnit.field.name+'",'
    output += '"country":"'+selectedUnit.country.name+'",'
    output += '"type":"'+selectedUnit.unitType.name+'"'
    output += '}'
    return HttpResponse(output)