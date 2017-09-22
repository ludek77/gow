from ui.models import Turn, Field, Unit, City, Country, CityCommand, Command, CommandType
from ui.engine.CommandValidator import CommandValidator
from ui.engine.TurnProcessor import TurnProcessor
from django.utils import timezone

class Engine:
    
    # remember turn
    turn = None
    # remember game
    game = None
    # current turn dict, key=field
    thisMap = None
    # next turn dict, key=field
    nextMap = None
    # properties
    defencePower = None # defence power of command
    attackPower = None # attack power of command
    maxAttackPower = None # max attack power to field
    maxAttackers = None # number of attackers with max power to field
    moves = None # number of moves to field
      
    def closeTurn(self):
        self.turn.open = False
        self.turn.save()
        
    def log(self, text):
        now = '{:%x %X}'.format(timezone.now())
        print('['+now+'] game=['+str(self.game.pk)+'.'+self.game.name+'], turn=['+str(self.turn.pk)+'.'+self.turn.name+'] '+text);
        
    def initialize(self, turn):
        self.turn = turn
        self.game = turn.game
        self.thisMap = {}
        self.nextMap = {}
        self.defencePower = {}
        self.attackPower = {}
        self.maxAttackPower = {}
        self.maxAttackers = {}
        self.moves = {}
        # copy commands
        cmds = Command.objects.filter(turn=turn)
        for cmd in cmds:
            self.thisMap[cmd.unit.field] = cmd
        
    def calculateNextTurn(self, turn):
        # initialize turn
        self.initialize(turn)
        # log start
        self.log('Recalculating game')
        # close original turn
        self.closeTurn()
        # cancel invalid commands
        self.cancelInvalid()
        # cancel attacked commands
        self.cancelAttacked()
        # cancel broken invasions
        self.cancelBrokenInvasions()
        # count defence powers
        self.countDefencePowers()
        # cound attack powers
        self.countAttackPowers()
        # cancel reverse attacks that are not stronger than opposite ones
        self.cancelWeakReverseAttacks()
        # cancel attacks that are not strongest to target field
        self.cancelWeakAttacks()
        # drop units that don't move or commands
        self.dropUnits()
        # proceed attacks while situation is changing
        self.proceedAttacks()
        # add units
        if turn.newUnits:
            # add or remove units
            self.addRemoveUnits()
        # save results
        self.saveResults()
        # create new turn
        self.log('Building next turn')
        newTurn = TurnProcessor().createNextTurn(turn, self.nextMap)
            
        self.log('Recalculation done')
        return newTurn
    
    def cancelInvalid(self):
        self.log('Validating moves')
        validator = CommandValidator()
        for field in self.thisMap:
            cmd = self.thisMap[field]
            validator.validateCommand(cmd)
            
    def dropUnit(self, cmd, newField):
        for field, command in self.nextMap.iteritems():
            if command == cmd:
                self.nextMap.pop(field, None)
                break
        self.nextMap[newField] = cmd
    
    def dropUnits(self):
        self.log('Dropping units to new map')
        for field in self.thisMap:
            cmd = self.thisMap[field]
            self.dropUnit(cmd, field)

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
                        targetCmd.result = 'fail.canceled-by-attack'
    
    def cancelBrokenInvasions(self):
        # TODO implement
        return None
        
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
        # count attack powers of commands
        for field in self.thisMap:
            cmd = self.thisMap[field]
            ct = cmd.commandType
            #count my own power
            if not ct.support:
                self.addAttackPower(cmd, ct.attackPower)
            #if support, add power to supported unit (if attackpower > 0, it's supporting attack, otherwise defence)
            if ct.support and ct.attackPower > 0 and cmd.result is None:
                targetField = self.getTargetField(cmd)
                targetCmd = self.thisMap[targetField]
                if targetCmd is not None:
                    self.addAttackPower(targetCmd, ct.attackPower)
        # store max attack powers and numbers
        for field in self.thisMap:
            cmd = self.thisMap[field]
            ct = cmd.commandType
            if not ct.support and ct.attackPower > 0 and cmd.result is None:
                power = self.attackPower.get(cmd)
                if power is not None:
                    targetField = self.getTargetField(cmd)
                    maxPower = self.maxAttackPower.get(targetField)
                    if maxPower is None:
                        maxPower = 0
                    if power > maxPower:
                        self.maxAttackPower[targetField] = power
                        self.maxAttackers[targetField] = 1
                    elif power == maxPower:
                        maxAttackers = self.maxAttackers[targetField]
                        self.maxAttackers[targetField] = maxAttackers + 1
        
    def cancelWeakReverseAttacks(self):
        self.log('Canceling weak reverse attacks')
        for field in self.thisMap:
            cmd = self.thisMap[field]
            ct = cmd.commandType
            if ct.move and ct.attackPower > 0 and cmd.result is None:
                targetField = self.getTargetField(cmd)
                targetCmd = self.thisMap.get(targetField)
                if targetCmd is not None:
                    rev_ct = targetCmd.commandType
                    if rev_ct.move and rev_ct.attackPower > 0:
                        revTargetField = self.getTargetField(targetCmd)
                        if revTargetField == field:
                            rev_power = self.attackPower.get(targetCmd)
                            power = self.attackPower.get(cmd)
                            if rev_power is not None and rev_power >= power:
                                cmd.result = 'fail.not-stronger-than-opposite'
    
    def cancelWeakAttacks(self):
        self.log('Canceling weak attacks')
        for field in self.thisMap:
            cmd = self.thisMap[field]
            ct = cmd.commandType
            if ct.move and ct.attackPower > 0 and cmd.result is None:
                targetField = self.getTargetField(cmd)
                if self.attackPower[cmd] < self.maxAttackPower[targetField] or self.maxAttackers[targetField] > 1:
                    cmd.result = 'fail.not-strongest'
        
    def tryAttacks(self):
        changed = False
        for field in self.thisMap:
            cmd = self.thisMap[field]
            ct = cmd.commandType
            # for each attack not processed yet
            if ct.attackPower > 0 and ct.move and not ct.support and cmd.result is None:
                targetField = self.getTargetField(cmd)
                targetCmd = self.nextMap.get(targetField)
                # if target field is empty, drop unit to that field
                if targetCmd is None:
                    self.dropUnit(cmd, targetField)
                    cmd.result = 'ok'
                    changed = True
                # if target field is not empty
                else:
                    # and target will not move (not move or cancelled)
                    if not targetCmd.commandType.move or targetCmd.result is not None:
                        attackPower = self.attackPower[cmd]
                        defencePower = self.defencePower[targetCmd]
                        # if attack is stronger than defence, attacker succeeds
                        if attackPower > defencePower:
                            self.dropUnit(cmd, targetField)
                            cmd.result = 'ok'
                            targetCmd.result = 'flee'
                            changed = True
                        else:
                            cmd.result = 'fail.defence-stronger'
                            changed = True
                        
        self.log('   next round changed:'+str(changed))
        return changed
    
    def proceedAttacks(self):
        self.log('Processing attacks')
        changed = True
        while changed:
            changed = self.tryAttacks()
    
    def proceedAllAttacks(self):
        self.log('Processing remaining attacks')
        return None
                        
    def getTargetField(self, cmd):
        args = cmd.args.split(',')
        target = args[len(args)-1]
        if target == '':
            target = 0
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
                newCommand = Command()
                newCommand.unit = newUnit
                self.dropUnit(newCommand, cmd.city.field)
                cmd.result = 'ok'
                unitPoints -= cmd.newUnitType.unitPoints
   
    def removeUnits(self, country, unitPoints):
        self.log('Removing units for ['+str(country.pk)+'.'+country.name+']:'+str(unitPoints)+'pts')
        # TODO finish
    
    def addRemoveUnits(self):
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
    
    def saveResults(self):
        self.log('Saving results')
        for field in self.thisMap:
            cmd = self.thisMap[field]
            if cmd.result is None:
                cmd.result = 'ok'
            cmd.save()
        