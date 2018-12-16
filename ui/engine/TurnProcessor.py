from ui.models import Game, Turn, Field, Country, City, CityCommand, Unit, Command
from ui.engine.CommandValidator import CommandValidator
from ui.engine.MapProcessor import MapProcessor
from django.utils import timezone

class TurnProcessor:
    
    def startGame(self, game, newGameName, firstTurnName):
        #create game
        newGame = Game()
        newGame.name = newGameName
        newGame.tileServer = game.tileServer
        newGame.winPoints = game.winPoints
        newGame.defaultCommandType = game.defaultCommandType
        newGame.status = 1
        newGame.save()
        for u in game.user.all():
            newGame.user.add(u)
        newGame.save()
        #initialize countries
        countries = Country.objects.filter(game=game)
        for c in countries:
            c.pk = None
            c.game = newGame
            c.save()
        #create initial turn
        newTurn = Turn()
        newTurn.name = firstTurnName
        newTurn.game = newGame
        newTurn.open = True
        newTurn.newUnits = True
        newTurn.save()
        #initialize fields
        fields = Field.objects.filter(game=game)
        for f in fields:
            newField = Field()
            newField.name = f.name
            newField.type = f.type
            newField.game = newGame
            newField.lat = f.lat
            newField.lng = f.lng
            newField.defaultPriority = f.defaultPriority
            newField.defaultUnitType = f.defaultUnitType
            newField.winPoints = f.winPoints
            newField.unitPoints = f.unitPoints
            if f.home is not None:
                newField.home = Country.objects.get(game=newGame, name=f.home.name)
            newField.isCity = f.isCity
            newField.save()
            if newField.isCity and newField.home is not None:
                newCity = City()
                newCity.turn = newTurn
                newCity.field = newField
                newCity.country = newField.home
                newCity.save()
                #initial command
                newCityCommand = CityCommand()
                newCityCommand.city = newCity
                newCityCommand.priority = newField.defaultPriority
                newCityCommand.newUnitType = newField.defaultUnitType
                newCityCommand.save()
            for f_next in f.next.all():
                newList = Field.objects.filter(game=newGame, name=f_next.name)
                if len(newList) > 0:
                    newField.next.add(newList.first())
            newField.save()
        return newGame
    
    def createNextTurn(self, lastTurn):
        newTurn = Turn()
        newTurn.name = str(int(lastTurn.name)+1)
        newTurn.game = lastTurn.game
        newTurn.newUnits = not lastTurn.newUnits
        newTurn.open = True
        if lastTurn.deadline is not None:
            newTurn.deadline = lastTurn.deadline + timezone.timedelta(minutes=lastTurn.game.turnMinutes)
        newTurn.previous = lastTurn
        newTurn.save()
        return newTurn
        
    def createCities(self, lastTurn, newTurn, nextMap):
        # setup new cities
        cities = City.objects.filter(turn=lastTurn)
        for city in cities:
            newCity = City()
            newCity.turn = newTurn
            newCity.field = city.field
            # if some unit is on field, copy its owner
            if lastTurn.newUnits and nextMap.get(city.field) is not None:
                newCity.country = nextMap[city.field].unit.country
            else:
                newCity.country = city.country
            newCity.save()
            if newTurn.newUnits:
                if newCity.country == newCity.field.home:
                    newCC = CityCommand()
                    newCC.city = newCity
                    newCC.priority = newCity.field.defaultPriority
                    newCC.newUnitType = newCity.field.defaultUnitType
                    newCC.save()
                    
    def createUnits(self, newTurn, nextMap):
        mapProcessor = MapProcessor(newTurn)
        game = Game.objects.get(pk=newTurn.game.pk)
        # setup new units
        for field in nextMap:
            cmd = nextMap[field]
            if cmd is not None:
                # add unit
                newUnit = Unit()
                newUnit.country = cmd.unit.country
                newUnit.turn = newTurn
                newUnit.unitType = cmd.unit.unitType
                newUnit.field = field
                newUnit.save()
                # add default command
                newCommand = Command()
                newCommand.unit = newUnit
                newCommand.commandType = newTurn.game.defaultCommandType
                newCommand.escape = mapProcessor.getEscapeFieldPks(newUnit)
                newCommand.removePriority = mapProcessor.getRemoveIndex(newUnit)
                #print(str(newCommand)+': '+str(newCommand.removePriority))
                newCommand.save()
