from ui.models import Turn, Field, Unit, City, Country, CityCommand, Command, CommandType
from ui.engine.CommandValidator import CommandValidator
from django.utils import timezone

class Engine:
    
    # remember turn
    turn = None
    # remember game
    game = None
    # current turn dict, key=fieldPk
    thisMap = None
    # next turn dict, key=fieldPk
    nextMap = None
    # properties
    defencePower = None
    attackPower = None
      
    def closeTurn(self):
        self.turn.open = False
        self.turn.save()
        
    def log(self, text):
        now = '{:%x %X}'.format(timezone.now())
        print('['+now+'] game=['+str(self.game.pk)+'.'+self.game.name+'], turn=['+str(self.turn.pk)+'.'+self.turn.name+'] '+text);
        
    def initialize(self, game, turn):
        self.turn = turn
        self.game = game
        self.thisMap = {}
        self.nextMap = {}
        self.defencePower = {}
        self.attackPower = {}
        # copy commands
        cmds = Command.objects.filter(turn=turn)
        for cmd in cmds:
            self.thisMap[cmd.unit.field] = cmd
        
    def recalculate(self, game, turn):
        # initialize turn
        self.initialize(game, turn)
        # log start
        self.log('Recalculating game')
        # close original turn
        self.closeTurn()
        # cancel invalid commands
        self.cancelInvalid()
        # cancel attacked commands
        self.cancelAttacked()
        # count defence powers
        self.countDefencePowers()
        # cound attack powers
        self.countAttackPowers()
        # copy units
        self.dropStaticUnits()
        # proceed attacks
        self.doAttacks()
        # add units
        if turn.newUnits:
            self.syncUnits()
        # create new turn
        newTurn = self.createNextTurn()
            
        self.log('Recalculation done')
        return newTurn
    
    def cancelInvalid(self):
        self.log('Validating moves')
        validator = CommandValidator()
        for field in self.thisMap:
            cmd = self.thisMap[field]
            validator.validateCommand(cmd)
    
    def dropStaticUnits(self):
        self.log('Dropping static units')
        for field in self.thisMap:
            cmd = self.thisMap[field]
            if not cmd.commandType.move:
                self.nextMap[field] = cmd

    def cancelAttacked(self):
        self.log('Canceling attacked')
        for field in self.thisMap:
            cmd = self.thisMap[field]
            ct = cmd.commandType
            if ct.attackPower > 0 and not ct.support and cmd.result is None:
                targetField = self.getTargetField(cmd)
                targetCmd = self.thisMap.get(targetField)
                if targetCmd is not None:
                    if targetCmd.commandType.cancelByAttack:
                        targetCmd.result = 'canceled-by-attack'
        
    def addDefencePower(self, cmd, addedPower):
        power = 0
        if self.defencePower.get(cmd) is not None:
            power = self.defencePower[cmd]
        power += addedPower
        self.defencePower[cmd] = power
        
    def countDefencePowers(self):
        self.log('Counting defence powers')
        for field in self.thisMap:
            cmd = self.thisMap[field]
            ct = cmd.commandType
            #count my own power
            self.addDefencePower(cmd, ct.defencePower)
            #if support, add power to supported unit (if attackpower not 0, it's supporting attack, otherwise defence)
            if ct.support and ct.attackPower == 0 and cmd.result is None:
                targetField = self.getTargetField(cmd)
                targetCmd = self.thisMap[targetField]
                if targetCmd is not None:
                    self.addDefencePower(targetCmd, ct.defencePower)
                        
    def addAttackPower(self, cmd, addedPower):
        power = 0
        if self.attackPower.get(cmd) is not None:
            power = self.attackPower[cmd]
        power += addedPower
        self.attackPower[cmd] = power
                        
    def countAttackPowers(self):
        self.log('Counting attack powers')
        for field in self.thisMap:
            cmd = self.thisMap[field]
            ct = cmd.commandType
            #count my own power
            if not ct.support:
                self.addAttackPower(cmd, ct.attackPower)
            #if support, add power to supported unit (if attackpower > 0, it's supporting attack, otherwise defence)
            if ct.support and ct.attackPower > 0 and cmd.result is None:
                targetField = self.getTargetField(game, cmd)
                targetCmd = self.thisMap[targetField]
                if targetCmd is not None:
                    self.addAttackPower(targetCmd, ct.attackPower)
        
    def doAttacks(self):
        self.log('Processing attacks')
        for field in self.thisMap:
            cmd = self.thisMap[field]
            ct = cmd.commandType
            if ct.attackPower > 0 and ct.move and not ct.support and cmd.result is None:
                targetField = self.getTargetField(cmd)
                targetCmd = self.nextMap.get(targetField)
                if targetCmd is None:
                    self.nextMap[targetField] = cmd
                    cmd.result = 'ok'
                        
    def getTargetField(self, cmd):
        args = cmd.args.split(',')
        target = args[len(args)-1]
        targetField = Field.objects.filter(game=self.game, pk=target)
        if len(targetField) == 1:
            return targetField.first()
        else:
            return None
    
    def addUnits(self, country, unitPoints):
        self.log('Adding units for ['+str(country.pk)+'.'+country.name+']:'+str(unitPoints)+'pts')
        cmds = CityCommand.objects.filter(city__turn=self.turn, city__country=country).order_by('priority')
        for cmd in cmds:
            if unitPoints >= cmd.newUnitType.unitPoints:
                newUnit = Unit()
                newUnit.country = country
                newUnit.unitType = cmd.newUnitType
                self.nextMap[cmd.city.field] = newUnit
                cmd.result = 'ok'
                unitPoints -= cmd.newUnitType.unitPoints
   
    def removeUnits(self, country, unitPoints):
        self.log('Removing units for ['+str(country.pk)+'.'+country.name+']:'+str(unitPoints)+'pts')
        # TODO finish
    
    def syncUnits(self):
        if not self.turn.newUnits:
            return
        self.log('Synchronizing units')
        countries = Country.objects.filter(game=self.game)
        for country in countries:
            cityUnitPoints = 0
            cities = City.objects.filter(turn=self.turn, country=country)
            for city in cities:
                cityUnitPoints += city.field.unitPoints
            unitUnitPoints = 0
            units = Unit.objects.filter(turn=self.turn, country=country)
            for unit in units:
                unitUnitPoints += unit.unitType.unitPoints
            if cityUnitPoints > unitUnitPoints:
                self.addUnits(country, cityUnitPoints-unitUnitPoints)
            elif unitUnitPoints > cityUnitPoints:
                self.removeUnits(country, unitUnitPoints-cityUnitPoints)
        return None
    
    def createNextTurn(self):
        self.log('Building next turn')
        newTurn = Turn()
        newTurn.name = str(int(self.turn.name)+1)
        newTurn.game = self.game
        newTurn.newUnits = not self.turn.newUnits
        newTurn.open = True
        newTurn.deadline = timezone.now() + timezone.timedelta(minutes = 5)
        newTurn.save()
        # setup new cities
        cities = City.objects.filter(turn=self.turn)
        for city in cities:
            newCity = City()
            newCity.turn = newTurn
            newCity.field = city.field
            newCity.country = city.country
            newCity.save()
        # setup new units
        for field in self.nextMap:
            cmd = self.nextMap[field]
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
            newCommand.turn = newTurn
            newCommand.commandType = self.game.defaultCommandType
            newCommand.save()
        return newTurn
            
            