from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ui.models import City

@login_required
def city_get_rest(request):
    uid = request.GET.get("c")
    selectedCity = City.objects.get(field__id=uid)
    output = '{'
    #output += '"pk":'+str(selectedCity.pk)+','
    output += '"field":"'+selectedCity.field.name+'",'
    output += '"country":"'+selectedCity.country.name+'"'
    output += '}'
    return HttpResponse(output)