from ui.models import Field, City, Command, CityCommand
from ui.engine.CommandValidator import CommandValidator
import cmd

class MapProcessor:
    
    turn = None
    
    def __init__(self, turn):
        self.turn = turn
    
    getNeighboursBuffer = {}
    def getNeighbours(self, field):
        # get data from buffer
        if field in self.getNeighboursBuffer:
            return self.getNeighboursBuffer[field]
        # calculate result
        result = []
        for nf in field.next.all().order_by('pk'):
            result.append(nf)
        # store and return result
        self.getNeighboursBuffer[field] = result
        return result
    
    def filterReachable(self, unitType, fields):
        result = []
        validator = CommandValidator()
        for field in fields:
            if validator.isReachable(unitType, field):
                result.append(field)
        return result
    
    getHomeFieldsBuffer = {}
    def getHomeFields(self, country):
        # get result from buffer
        if country in self.getHomeFieldsBuffer:
            return self.getHomeFieldsBuffer[country]
        # calculate result
        result = []
        cities = City.objects.filter(turn=self.turn, country=country, field__home=country).order_by('pk')
        for city in cities:
            result.append(city.field)
        # store and return result
        self.getHomeFieldsBuffer[country] = result
        return result
    
    getFieldsByHomeDistanceBuffer = {}
    def getFieldsByHomeDistance(self, country, unitType):
        key = str(country.pk)+'.'
        if unitType is not None:
            key += str(unitType.pk)
        if key in self.getFieldsByHomeDistanceBuffer:
            return self.getFieldsByHomeDistanceBuffer[key]
        # get home fields
        result = self.getHomeFields(country)
        #build result
        if unitType is not None:
            result = self.filterReachable(unitType, result)
        index = 0
        while index < len(result):
            field = result[index]
            # get neighbours of processed field
            newFields = self.getNeighbours(field)
            if unitType is not None:
                newFields = self.filterReachable(unitType, newFields)
            # add those not in list yet
            for rr in newFields:
                if rr not in result:
                    result.append(rr)
            index+=1
        # store and return result
        self.getFieldsByHomeDistanceBuffer[key] = result
        return result

    def setPriorityEscape(self, command, escapeField):
        result = ''
        separator = ''
        message = None
        # get neighbours
        neighbours = self.getNeighbours(command.unit.field)
        reachable = self.filterReachable(command.unit.unitType, neighbours)
        # if defined priority in reachable neighbours
        if escapeField in reachable:
            result += str(escapeField.pk)
            separator = ','
        else:
            message = 'fail.not-reachable-for-escape'
        # get default list of escapes and add them
        escapes = self.getEscapeFieldPks(command.unit)
        eList = escapes.split(',')
        for e in eList:
            if e != str(escapeField.pk):
                result += separator + e
                separator = ','
        # set result
        command.escape = result
        command.save()
        return message
    
    def orderCommand(self, command, priority, commands):
        # iterate commands
        index = 4
        for cmd in commands:
            # command to be changed
            newPriority = index
            if cmd.pk == command.pk:
                if priority == -9:
                    newPriority = 1
                if priority == -1:
                    newPriority = index - 3
                if priority == 1:
                    newPriority = index + 3
                if priority == 9:
                    newPriority = 2*len(commands) + 3
            # other commands
            if type(cmd) is Command:
                cmd.removePriority = newPriority
            else:
                cmd.priority = newPriority
            cmd.save()
            index += 2
            lastCmd = cmd
        
    def fieldsToPks(self, fields):
        result = ''
        separator = ''
        for field in fields:
            result += separator+str(field.pk)
            separator = ','
        return result
    
    def getEscapeFieldPks(self, unit):
        # ordetr them by home distance
        fields = self.getFieldsByHomeDistance(unit.country, unit.unitType)
        # get neighbours
        neighbours = self.getNeighbours(unit.field)
        reachable = self.filterReachable(unit.unitType, neighbours)
        # build list of neighbours ordered by home distance
        result = []
        for field in fields:
            if field in neighbours:
                result.append(field)
        pks = self.fieldsToPks(result)
        return pks
    
    def getRemoveIndex(self, unit):
        fields = self.getFieldsByHomeDistance(unit.country, None)
        index = 1
        for fld in fields:
            if fld == unit.field:
                return len(fields) - index
            index += 1
        # if no home field exists, index not found
        return 0
