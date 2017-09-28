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
    escapes = None # number of escapes to field
      
    def closeTurn(self):
        self.turn.open = False
        self.turn.save()
        
    def log(self, text):
        #now = '{:%x %X}'.format(timezone.now())
        #print('['+now+'] game=['+str(self.game.pk)+'.'+self.game.name+'], turn=['+str(self.turn.pk)+'.'+self.turn.name+'] '+text);
        return None
        
    def isAttack(self, ct):
        return ct.attackPower > 0 and not ct.support and not ct.transport and ct.move
    
    def isMove(self, ct):
        return ct.attackPower == 0 and not ct.support and ct.move
    
    def isSupportAttack(self, ct):
        return ct.attackPower > 0 and ct.support
    
    def isSupportDefence(self, ct):
        return ct.attackPower == 0 and ct.support and ct.defencePower > 0
    
    def isTransport(self, ct):
        return ct.attackPower == 0 and ct.transport and not ct.move
    
    def isInvasion(self, ct):
        return ct.attackPower > 0 and ct.transport and ct.move
        
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
        # cancel commands on successfully invaded field
        self.cancelInvaded()
        # count defence powers
        self.countDefencePowers()
        # cound attack powers
        self.countAttackPowers()
        # cancel reverse attacks that are not stronger than opposite ones
        self.cancelWeakReverseAttacks()
        # cancel attacks that are not strongest to target field
        self.cancelWeakAttacksAndInvasions()
        # drop units that don't move or commands
        self.dropUnits()
        # proceed attacks while situation is changing
        self.proceedAttacksAndInvasions()
        # proceed all remaining attacks
        self.proceedRemainingAttacksAndInvasions()
        for index in [0, 1]:
            # cancel moves to attacked fields or there are more moves
            self.cancelWeakMoves(index)
            # proceed first step of moves
            self.proceedMoves(index)
            # do all remaining moves
            self.proceedRemainingMoves(index)
        # escape units
        self.doEscapes()
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
            
    def dropUnit(self, cmd, targetField):
        for field, command in self.nextMap.iteritems():
            if command == cmd:
                self.nextMap.pop(field, None)
                break
        self.nextMap[targetField] = cmd
    
    def dropUnits(self):
        self.log('Dropping units to new map')
        for field in self.thisMap:
            cmd = self.thisMap[field]
            self.dropUnit(cmd, field)

    def cancelAttacked(self):
        self.log('Canceling attacked')
        for field in self.thisMap:
            cmd = self.thisMap[field]
            if self.isAttack(cmd.commandType) and cmd.result is None:
                targetField = self.getTargetField(cmd)
                targetCmd = self.thisMap.get(targetField)
                # there is active target command
                if targetCmd is not None and targetCmd.result is None and targetCmd.commandType.cancelByAttack:
                    ttField = self.getTargetField(targetCmd, 0)
                    isSupportingAttackAtMe = self.isSupportAttack(targetCmd.commandType) and ttField == field
                    if not isSupportingAttackAtMe:
                        targetCmd.result = 'fail.canceled-by-attack'
    
    def cancelBrokenInvasions(self):
        self.log('Canceling broken invasions')
        for field in self.thisMap:
            cmd = self.thisMap[field]
            if self.isInvasion(cmd.commandType) and cmd.result is None:
                args = cmd.args.split(',')
                index = 0
                transportCanceled = False
                transportMissing = False
                while index < len(args)-1:
                    pathField = self.getTargetField(cmd, index)
                    if pathField is not None:
                        if pathField in self.thisMap:
                            pathCmd = self.thisMap[pathField]
                            if not self.isTransport(pathCmd.commandType):
                                transportMissing = True
                            elif pathCmd.result is not None:
                                transportCanceled = True
                        else:
                            transportMissing = True 
                    index += 1
                if transportMissing:
                    cmd.result = 'fail.transport-missing'
                elif transportCanceled:
                    cmd.result = 'fail.transport-canceled'
                    
    def cancelInvaded(self):
        self.log('Canceling successfully invaded')
        for field in self.thisMap:
            cmd = self.thisMap[field]
            if self.isInvasion(cmd.commandType) and cmd.result is None:
                targetField = self.getTargetField(cmd)
                targetCmd = self.thisMap.get(targetField)
                # there is active target command
                if targetCmd is not None and targetCmd.result is None and targetCmd.commandType.cancelByAttack:
                    targetCmd.result = 'fail.canceled-by-invasion'
        
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
            #count my own power
            self.addDefencePower(cmd, cmd.commandType.defencePower)
            #if support, add power to supported unit (if attackpower not 0, it's supporting attack, otherwise defence)
            if self.isSupportDefence(cmd.commandType) and cmd.result is None:
                targetField = self.getTargetField(cmd)
                targetCmd = self.thisMap[targetField]
                if targetCmd is not None:
                    self.addDefencePower(targetCmd, cmd.commandType.defencePower)
                        
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
            if self.isSupportAttack(ct) and cmd.result is None:
                supportedField = self.getTargetField(cmd, 1)
                supportedCmd = self.thisMap[supportedField]
                if supportedCmd is not None and (self.isAttack(supportedCmd.commandType) or self.isInvasion(supportedCmd.commandType)):
                    sField = self.getTargetField(supportedCmd)
                    if sField == self.getTargetField(cmd, 0):
                        self.addAttackPower(supportedCmd, ct.attackPower)
                    else:
                        cmd.result = 'fail.unit-attacking-elsewhere'
                else:
                    cmd.result = 'fail.unit-not-attacking'
        # store max attack powers and numbers
        for field in self.thisMap:
            cmd = self.thisMap[field]
            if (self.isAttack(cmd.commandType) or self.isInvasion(cmd.commandType)) and cmd.result is None:
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
            if self.isAttack(cmd.commandType) and cmd.result is None:
                targetField = self.getTargetField(cmd)
                targetCmd = self.thisMap.get(targetField)
                if targetCmd is not None:
                    if self.isAttack(targetCmd.commandType):
                        revTargetField = self.getTargetField(targetCmd)
                        if revTargetField == field:
                            rev_power = self.attackPower.get(targetCmd)
                            power = self.attackPower.get(cmd)
                            if rev_power is not None and rev_power >= power:
                                cmd.result = 'fail.not-stronger-than-opposite'
    
    def cancelWeakAttacksAndInvasions(self):
        self.log('Canceling weak attacks and invasions')
        for field in self.thisMap:
            cmd = self.thisMap[field]
            if (self.isAttack(cmd.commandType) or self.isInvasion(cmd.commandType)) and cmd.result is None:
                targetField = self.getTargetField(cmd)
                if self.attackPower[cmd] < self.maxAttackPower[targetField] or self.maxAttackers[targetField] > 1:
                    cmd.result = 'fail.not-strongest'
        
    def tryAttacks(self):
        changed = False
        for field in self.thisMap:
            cmd = self.thisMap[field]
            # for each attack not processed yet
            if (self.isAttack(cmd.commandType) or self.isInvasion(cmd.commandType)) and cmd.result is None:
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
                            targetCmd.result = 'to-escape'
                            changed = True
                        else:
                            cmd.result = 'fail.defence-stronger'
                            changed = True
                        
        self.log('   next round changed:'+str(changed))
        return changed
    
    def proceedAttacksAndInvasions(self):
        self.log('Processing attacks and invasions')
        changed = True
        while changed:
            changed = self.tryAttacks()
    
    def proceedRemainingAttacksAndInvasions(self):
        self.log('Processing all remaining attacks and invasions')
        for field in self.thisMap:
            cmd = self.thisMap[field]
            if (self.isAttack(cmd.commandType) or self.isInvasion(cmd.commandType)) and cmd.result is None:
                targetField = self.getTargetField(cmd)
                self.dropUnit(cmd, targetField)
                cmd.result = 'ok'
    
    def cancelWeakMoves(self, index):
        self.log('Canceling weak moves '+str(index))
        # count moves
        moveCounter = {}
        for field in self.thisMap:
            cmd = self.thisMap[field]
            if self.isMove(cmd.commandType) and cmd.result is None:
                targetField = self.getTargetField(cmd, index)
                if targetField is not None:
                    if moveCounter.get(targetField) is None:
                        moveCounter[targetField] = 1
                    else:
                        moveCounter[targetField] = moveCounter[targetField] + 1
        # cancel commands with more moves
        for field in self.thisMap:
            cmd = self.thisMap[field]
            if self.isMove(cmd.commandType) and cmd.result is None:
                targetField = self.getTargetField(cmd, index)
                if targetField is not None:
                    if self.maxAttackers.get(targetField) is not None:
                        cmd.result = 'fail.target-attacked:par_'+str(index)
                    elif moveCounter[targetField] > 1:
                        cmd.result = 'fail.more-moves-to-target:par_'+str(index)
    
    def tryMoves(self, index):
        changed = False
        for field in self.thisMap:
            cmd = self.thisMap[field]
            if self.isMove(cmd.commandType) and cmd.result is None:
                targetField = self.getTargetField(cmd, index)
                if targetField is not None:
                    targetCmd = self.nextMap.get(targetField)
                    # target not empty and will not move
                    if targetCmd is not None and targetCmd.result is not None:
                        cmd.result = 'fail.target-not-empty:par_'+str(index)
                        changed = True
                    elif targetCmd is None:
                        self.dropUnit(cmd, targetField)
                        changed = True
        self.log('   next round changed:'+str(changed))
        return changed
                    
    def proceedMoves(self, index):
        self.log('Processing moves '+str(index))
        changed = True
        while changed:
            changed = self.tryMoves(index)
            
    def proceedRemainingMoves(self, index):
        self.log('Processing all remaining moves '+str(index))
        for field in self.thisMap:
            cmd = self.thisMap[field]
            if self.isMove(cmd.commandType) and cmd.result is None:
                targetField = self.getTargetField(cmd, index)
                if targetField is not None:
                    self.dropUnit(cmd, targetField)
         
    def tryEscapes(self, index):
        changed = False
        # initialize array of escapess
        self.escapes = {}
        # count escapes
        for field in self.thisMap:
            cmd = self.thisMap[field]
            if cmd.result == 'to-escape':
                changed = True
                eList = cmd.escape.split(',')
                if index <= len(eList):
                    escape = eList[index]
                    if escape in self.escapes:
                        self.escapes[escape] = self.escapes[escape] + 1
                    else:
                        self.escapes[escape] = 1
                else:
                    cmd.result = 'destroyed'
        # try to escape
        for field in self.thisMap:
            cmd = self.thisMap[field]
            if cmd.result == 'to-escape':
                eList = cmd.escape.split(',')
                if index <= len(eList):
                    escape = eList[index]
                    if self.escapes[escape] == 1:
                        field = self.getField(escape)
                        targetCmd = self.nextMap.get(field)
                        attackers = self.maxAttackers.get(field)
                        attackCmd = self.nextMap.get(cmd.unit.field)
                        if targetCmd is None and attackers is None and field != attackCmd.unit.field:
                            self.dropUnit(cmd, field)
                            cmd.result = 'escaped'
        self.log('   next round changed:'+str(changed))
        return changed
                    
    def doEscapes(self):
        self.log('Escaping units')
        changed = True
        index = 0
        while changed:
            # try to escape
            changed = self.tryEscapes(index)
            index += 1
            
    def getField(self, pk):
        fields = Field.objects.filter(game=self.game, pk=pk)
        if len(fields) == 1:
            result = fields.first()
        return result
                        
    def getTargetField(self, cmd, index=99):
        args = cmd.args.split(',')
        if index == 99:
            index = len(args) - 1
        if index <= len(args) - 1:
            target = args[index]
            if target != '' and target != '0':
                targetField = self.getField(target)
                if targetField is not None:
                    return targetField    
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
        