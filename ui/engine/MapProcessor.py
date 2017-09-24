from ui.models import Field, City

class MapProcessor:
    
    MAX_DIST = 999999
    
    def getNeighbours(self, field):
        result = []
        for nf in field.next.all().order_by('pk'):
            result.append(nf)
        return result
    
    def getHomeFields(self, country, turn):
        result = []
        cities = City.objects.filter(turn=turn, country=country, field__home=country)
        for city in cities:
            result.append(city.field)
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
    
    def orderByFieldDistance(self, sourceField, turn):
        distMap = {}
        # setup distances
        map = Field.objects.filter(game=turn.game)
        for field in map:
            if field == sourceField:
                distMap[field] = 1
            else:
                distMap[field] = self.MAX_DIST
        # calculate all distances
        changed = True
        while changed:
            changed = self.findNextDistances(distMap)
        return distMap
    
    def orderByHomeDistance(self, country, turn):
        distMap = {}
        game = turn.game
        # find home fields
        homeFields = self.getHomeFields(country, turn)
        # calculate distances for all fields
        for homeField in homeFields:
            fieldMap = self.orderByFieldDistance(homeField, turn)
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
        return result
    
    def getFleeFields(self, field, country, turn):
        neighbours = self.getNeighbours(field)
        homeDists = self.orderByHomeDistance(country, turn)
        fields = []
        for field in homeDists:
            if field in neighbours:
                fields.append(field)
        return fields
    
    def getFleeIndex(self, field, country, turn):
        homeDists = self.orderByHomeDistance(country, turn)
        index = 0
        for fld in homeDists:
            if fld == field:
                return len(homeDists) - index
            index += 1
        return None
    
    def fieldsToPks(self, fields):
        result = ''
        separator = ''
        for field in fields:
            result += separator+str(field.pk)
            separator = ','
        return result
    