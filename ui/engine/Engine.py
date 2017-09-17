from ui.models import Turn, Field, Unit, City, Country, CityCommand, Command, CommandType
from django.utils import timezone

class Engine:
      
    def closeTurn(self, turn):
        turn.open = False
        turn.save()
        
    def log(self, text, game, turn):
        print('['+str(timezone.now())+'] game=['+str(game.pk)+'.'+game.name+'], turn=['+str(turn.pk)+'.'+turn.name+'] '+text);
        
    def recalculate(self, game, turn):
        self.log('Recalculating game', game, turn)
        #close original turn
        #self.closeTurn(turn) DONT CLOSE FOR EASIER DEVELOPMENT
        #create new turn
        newTurn = self.nextTurn(game, turn)
        #add units
        if turn.newUnits:
            self.syncUnits(game, turn, newTurn)
            
        self.log('Recalculation done', game, turn)
        #return newTurn RETURN OLD TURN FOR EASIER DEVELOPMENT
        return turn
        
    def nextTurn(self, game, turn):
        newTurn = Turn()
        newTurn.name = str(int(turn.name)+1)
        newTurn.game = game
        newTurn.newUnits = not turn.newUnits
        newTurn.open = True
        newTurn.deadline = timezone.now() + timezone.timedelta(minutes = 5)
        newTurn.save()
        return newTurn
    
    def addUnits(self, game, turn, newTurn, country, unitPoints):
        self.log('Adding units for ['+str(country.pk)+'.'+country.name+']:'+str(unitPoints)+'pts', game, turn)
        cmds = CityCommand.objects.filter(city__turn=turn, city__country=country).order_by('priority')
        for cmd in cmds:
            if unitPoints >= cmd.newUnitType.unitPoints:
                newUnit = Unit()
                newUnit.turn = newTurn
                newUnit.country = country
                newUnit.unitType = cmd.newUnitType
                newUnit.field = cmd.city.field
                newUnit.save()
                newCommand = Command()
                newCommand.turn = newTurn
                newCommand.unit = newUnit
                newCommand.commandType = game.defaultCommandType
                newCommand.save()
                unitPoints -= cmd.newUnitType.unitPoints
                self.log('Add ['+cmd.newUnitType.name+'] to '+cmd.city.field.name, game, turn)   
    
    def removeUnits(self, game, turn, newTurn, country, unitPoints):
        self.log('Removing units for ['+str(country.pk)+'.'+country.name+']:'+str(unitPoints)+'pts', game, turn)
    
    def syncUnits(self, game, turn, newTurn):
        if not turn.newUnits:
            return
        self.log('Synchronizing units', game, turn)
        countries = Country.objects.filter(game=game)
        for country in countries:
            cityUnitPoints = 0
            cities = City.objects.filter(turn=turn, country=country)
            for city in cities:
                cityUnitPoints += city.field.unitPoints
            unitUnitPoints = 0
            units = Unit.objects.filter(turn=turn, country=country)
            for unit in units:
                unitUnitPoints += unit.type.unitPoints
            if cityUnitPoints > unitUnitPoints:
                self.addUnits(game, turn, newTurn, country, cityUnitPoints-unitUnitPoints)
            elif unitUnitPoints > cityUnitPoints:
                self.removeUnits(game, turn, newTurn, country, unitUnitPoints-cityUnitPoints)
        return None