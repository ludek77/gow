from ui.models import Turn, Field, Unit, City, Country, CityCommand, Command, CommandType
from django.utils import timezone

class Engine:
      
    def closeTurn(self, turn):
        turn.open = False
        turn.save()
        
    def log(self, text, game, turn):
        now = '{:%x %X}'.format(timezone.now())
        print('['+now+'] game=['+str(game.pk)+'.'+game.name+'], turn=['+str(turn.pk)+'.'+turn.name+'] '+text);
        
    def recalculate(self, game, turn):
        self.log('Recalculating game', game, turn)
        #close original turn
        self.closeTurn(turn)
        #check validity of moves
        self.cancelInvalid(game, turn)
        #create new turn
        newTurn = self.nextTurn(game, turn)
        #cancel attacked commands
        self.cancelAttacked(game, turn, newTurn)
        #count defence powers
        self.countDefencePowers(game, turn)
        #cound attack powers
        self.countAttackPowers(game, turn)
        #copy units
        self.copyUnits(game, turn, newTurn)
        #add units
        if turn.newUnits:
            self.syncUnits(game, turn, newTurn)
        #setup new cities
        self.syncCities(game, turn, newTurn)
            
        self.log('Recalculation done', game, newTurn)
        return newTurn
    
    def cancelInvalid(self, game, turn):
        self.log('Canceling invalid moves', game, turn)
        # TODO: check validity of arguments, add this verification to command saving
        
    def nextTurn(self, game, turn):
        newTurn = Turn()
        newTurn.name = str(int(turn.name)+1)
        newTurn.game = game
        newTurn.newUnits = not turn.newUnits
        newTurn.open = True
        newTurn.deadline = timezone.now() + timezone.timedelta(minutes = 5)
        newTurn.save()
        return newTurn
    
    def createNewUnit(self, game, newTurn, country, unitType, field):
        newUnit = Unit()
        newUnit.turn = newTurn
        newUnit.country = country
        newUnit.unitType = unitType
        newUnit.field = field
        newUnit.save()
        newCommand = Command()
        newCommand.turn = newTurn
        newCommand.unit = newUnit
        newCommand.commandType = game.defaultCommandType
        newCommand.save()
    
    def copyUnits(self, game, turn, newTurn):
        self.log('Copying units', game, turn)
        cmds = Command.objects.filter(turn=turn)
        for cmd in cmds:
            self.createNewUnit(game, newTurn, cmd.unit.country, cmd.unit.unitType, cmd.unit.field)
        
    def countDefencePowers(self, game, turn):
        self.log('Counting defence powers', game, turn)
        cmds = Command.objects.filter(turn=turn)
        for cmd in cmds:
            #count my own power
            cmd.defencePower += cmd.commandType.defencePower
            cmd.save()
            #if support, add power to supported unit (if attackpower not 0, it's supporting attack, otherwise defence)
            if cmd.commandType.support and cmd.commandType.attackPower == 0 and cmd.result is None:
                targetField = self.getTargetField(game, cmd)
                if targetField is not None:
                    targetCmd = Command.objects.filter(turn=turn, unit__field=targetField)
                    if len(targetCmd) == 1:
                        targetCmd = targetCmd.first()
                        targetCmd.defencePower += cmd.commandType.defencePower
                        targetCmd.save()
                        
    def countAttackPowers(self, game, turn):
        self.log('Counting attack powers', game, turn)
        cmds = Command.objects.filter(turn=turn)
        for cmd in cmds:
            #count my own power
            if not cmd.commandType.support:
                cmd.attackPower += cmd.commandType.attackPower
                cmd.save()
            #if support, add power to supported unit (if attackpower > 0, it's supporting attack, otherwise defence)
            if cmd.commandType.support and cmd.commandType.attackPower > 0 and cmd.result is None:
                targetField = self.getTargetField(game, cmd)
                if targetField is not None:
                    targetCmd = Command.objects.filter(turn=turn, unit__field=targetField)
                    if len(targetCmd) == 1:
                        targetCmd = targetCmd.first()
                        targetCmd.attackPower += cmd.commandType.attackPower
                        targetCmd.save()
        
    def addUnits(self, game, turn, newTurn, country, unitPoints):
        #self.log('Adding units for ['+str(country.pk)+'.'+country.name+']:'+str(unitPoints)+'pts', game, turn)
        cmds = CityCommand.objects.filter(city__turn=turn, city__country=country).order_by('priority')
        for cmd in cmds:
            if unitPoints >= cmd.newUnitType.unitPoints:
                self.createNewUnit(game, newTurn, country, cmd.newUnitType, cmd.city.field)
                cmd.result = 'ok'
                cmd.save()
                unitPoints -= cmd.newUnitType.unitPoints
                #self.log('Add ['+cmd.newUnitType.name+'] to '+cmd.city.field.name, game, turn)   
    
    def removeUnits(self, game, turn, newTurn, country, unitPoints):
        self.log('Removing units for ['+str(country.pk)+'.'+country.name+']:'+str(unitPoints)+'pts', game, turn)
    
    def cancelAttacked(self, game, turn, newTurn):
        self.log('Canceling attacked', game, turn)
        cmds = Command.objects.filter(turn=turn)
        for cmd in cmds:
            if cmd.commandType.attackPower > 0 and not cmd.commandType.support and cmd.result is None:
                targetField = self.getTargetField(game, cmd)
                if targetField is not None:
                    targetCmd = Command.objects.filter(turn=turn, unit__field=targetField)
                    if len(targetCmd) == 1:
                        targetCmd = targetCmd.first()
                        if targetCmd.commandType.cancelByAttack:
                            targetCmd.result = 'canceled-by-attack'
                            targetCmd.save()
                        
    def getTargetField(self, game, cmd):
        args = cmd.args.split(',')
        target = args[len(args)-1]
        targetField = Field.objects.filter(game=game, pk=target)
        if len(targetField) == 1:
            return targetField.first()
        else:
            return None
    
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
                unitUnitPoints += unit.unitType.unitPoints
            if cityUnitPoints > unitUnitPoints:
                self.addUnits(game, turn, newTurn, country, cityUnitPoints-unitUnitPoints)
            elif unitUnitPoints > cityUnitPoints:
                self.removeUnits(game, turn, newTurn, country, unitUnitPoints-cityUnitPoints)
        return None
    
    def syncCities(self, game, turn, newTurn):
        self.log('Synchronizing cities', game, turn)
        cities = City.objects.filter(turn=turn)
        for city in cities:
            newCity = City()
            newCity.turn = newTurn
            newCity.field = city.field
            newCity.country = city.country
            newCity.save()