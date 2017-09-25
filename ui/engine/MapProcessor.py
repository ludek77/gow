from ui.models import Field, City
from ui.engine.CommandValidator import CommandValidator

class MapProcessor:
    
    MAX_DIST = 999999
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
        cities = City.objects.filter(turn=self.turn, country=country, field__home=country)
        for city in cities:
            result.append(city.field)
        # store and return result
        self.getHomeFieldsBuffer[country] = result
        return result
    
    def findNextDistances(self, map):
        changed = False
        for field in map:
            neighbours = self.getNeighbours(field)
            for neighbour in neighbours:
                if map[field] > map[neighbour]+1:
                    map[field] = map[neighbour]+1
                    changed = True
        return changed
    
    orderByFieldDistanceBuffer = {}
    def orderByFieldDistance(self, sourceField):
        # get result from buffer
        if sourceField in self.orderByFieldDistanceBuffer:
            return self.orderByFieldDistanceBuffer[sourceField]
        # calculate result
        distMap = {}
        # setup distances
        map = Field.objects.filter(game=self.turn.game)
        for field in map:
            if field == sourceField:
                distMap[field] = 1
            else:
                distMap[field] = self.MAX_DIST
        # calculate all distances
        changed = True
        while changed:
            changed = self.findNextDistances(distMap)
        # store and return result
        self.orderByFieldDistanceBuffer[sourceField] = distMap
        return distMap
    
    orderByHomeDistanceBuffer = {}
    def orderByHomeDistance(self, country):
        # get result from buffer
        if country in self.orderByHomeDistanceBuffer:
            return self.orderByHomeDistanceBuffer[country]
        # calculate result
        distMap = {}
        game = self.turn.game
        # find home fields
        homeFields = self.getHomeFields(country)
        # calculate distances for all fields
        for homeField in homeFields:
            fieldMap = self.orderByFieldDistance(homeField)
            for field in fieldMap:
                if field in distMap:
                    distMap[field] = distMap[field] * fieldMap[field]
                else:
                    distMap[field] = fieldMap[field]
        # build result
        result = []
        nextDist = 0
        while nextDist != self.MAX_DIST:
            dist = nextDist
            nextDist = self.MAX_DIST
            for field in distMap:
                if distMap[field] == dist:
                    result.append(field)
                    #print str(dist)+'='+field.name
                elif distMap[field] > dist and distMap[field] < nextDist:
                    nextDist = distMap[field]
        # store and return result
        self.orderByHomeDistanceBuffer = result
        return result
    
    def getEscapeFieldPks(self, unit):
        neighbours = self.getNeighbours(unit.field)
        reachable = self.filterReachable(unit.unitType, neighbours)
        homeDists = self.orderByHomeDistance(unit.country)
        fields = []
        for field in homeDists:
            if field in reachable:
                fields.append(field)
        pks = self.fieldsToPks(fields)
        return pks
    
    def getRemoveIndex(self, unit):
        homeDists = self.orderByHomeDistance(unit.country)
        index = 0
        for fld in homeDists:
            if fld == unit.field:
                return len(homeDists) - index
            index += 1
        # if no home field exists, index not found
        return 1
    
    def fieldsToPks(self, fields):
        result = ''
        separator = ''
        for field in fields:
            result += separator+str(field.pk)
            separator = ','
        return result
    