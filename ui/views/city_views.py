from django.http import HttpResponse
from ui.models import City

def city_get_rest(request):
    uid = request.GET.get("c")
    selectedCity = City.objects.get(field__id=uid)
    output = '{'
    #output += '"pk":'+str(selectedCity.pk)+','
    output += '"field":"'+selectedCity.field.name+'",'
    output += '"country":"'+selectedCity.country.name+'"'
    output += '}'
    return HttpResponse(output)