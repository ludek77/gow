from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ui.models import Game, Turn, Field, UnitType, City, Unit, Country, CityCommand, Command

@login_required
def country_setup_rest(request):
    selectedGame = Game.objects.get(pk=request.session['selected_game'], user__id=request.user.id)
    if 'selected_turn' in request.session:
        selectedTurn = Turn.objects.filter(pk=request.session['selected_turn'], game=selectedGame)
        if len(selectedTurn) == 1:
            selectedTurn = selectedTurn.first()
        else:
            selectedTurn = None
    else:
        selectedTurn = None
        
    if selectedTurn.open:
        countries = Country.objects.filter(game=selectedGame, owner__id=request.user.id)
    else:
        countries = Country.objects.filter(game=selectedGame)
    separator = ''
    output =  '{'
    if selectedTurn.open:
        output += '"open":true,'
    output += '"countries":['
    for country in countries:
        output += separator + renderCountry(country, selectedTurn)
        separator = ','
    output += ']'
    output += '}'
    return HttpResponse(output)
    
def renderCountry(country, turn):
    output = '{'
    output += '"name":"'+country.name+'"'
    output += ',"pk":'+str(country.pk)+''
    
    output += ',"units":['
    if turn is not None:
        commands = Command.objects.filter(unit__turn=turn,unit__country=country).order_by('removePriority')
        separator = ''
        for command in commands:
            unit = command.unit
            field = command.unit.field
            output += separator+'{'
            output += '"id":'+str(unit.pk)
            output += ',"type":'+str(unit.unitType.pk)
            output += ',"fieldId":'+str(field.pk)
            output += ',"field":"'+field.name+'"'
            output += ',"latlng":['+str(field.lat)+','+str(field.lng)+']'
            output += ',"command":"'+command.commandType.name+'"'
            if command.args != '':
                args = ''
                cargs = command.args.split(',')
                aseparator = ''
                for arg in cargs:
                    fld = Field.objects.get(pk=arg)
                    args += aseparator+'"'+fld.name+'"'
                    aseparator = ','
                output += ',"args":['+args+']'
            output += '}'
            separator = ','
    output += ']'
    
    output += ',"cities":['
    if turn is not None:
        cmds = CityCommand.objects.filter(city__country=country, city__turn=turn).order_by('priority')
        separator = ''
        for row in cmds:
            output += separator+'{'
            output += '"id":'+str(row.city.pk)
            output += ',"newUnit":"'+str(row.newUnitType.name)+'"'
            output += ',"fieldId":'+str(row.city.field.pk)
            output += ',"field":"'+row.city.field.name+'"'
            output += ',"latlng":['+str(row.city.field.lat)+','+str(row.city.field.lng)+']'
            output += '}'
            separator = ','
    output += ']'
    
    output += '}'
    return output
    
    