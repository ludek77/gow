from django.test import TestCase
from django.core.management import call_command
from ui.engine.TurnProcessor import TurnProcessor
from ui.engine.MapProcessor import MapProcessor
from ui.models import Game, Field, Country, Turn, City

class MapProcessorTests(TestCase):
    
    mp = MapProcessor()
    
    def setUp(self):
        call_command('loaddata', 'user', verbosity=0)
        call_command('loaddata', 'init', verbosity=0)
        call_command('loaddata', 'test/testworld', verbosity=0)
        
    def assertHomeCities(self, turn, country, expectedResult):
        country = Country.objects.get(game=turn.game, name=country)
        cities = City.objects.filter(turn=turn, country=country, field__home=country)
        result = self.fieldsToNames(cities)
        self.assertEqual(result, expectedResult)
        
    def assertNeighbours(self, game, fieldName, expectedResult):
        field = Field.objects.get(game=game, name=fieldName)
        fields = self.mp.getNeighbours(field)
        result = self.fieldsToNames(fields)
        self.assertEqual(result, expectedResult)
        
    def assertGetFlees(self, turn, fieldName, countryName, expectedResult):
        field = Field.objects.get(game=turn.game, name=fieldName)
        country = Country.objects.get(game=turn.game, name=countryName)
        fields = self.mp.getFleeFields(field, country, turn)
        result = self.fieldsToNames(fields)
        self.assertEqual(result, expectedResult)
        
    def assertFleeIndex(self, turn, fieldName, countryName, expectedIndex):
        field = Field.objects.get(game=turn.game, name=fieldName)
        country = Country.objects.get(game=turn.game, name=countryName)
        index = self.mp.getFleeIndex(field, country, turn)
        self.assertEqual(index, expectedIndex)
        
    def fieldsToNames(self, list):
        result = ''
        separator = ''
        for e in list:
            if type(e) is City:
                result += separator + e.field.name
            elif type(e) is Field:
                result += separator + e.name
            separator = ','
        return result
        
    def test_Processor(self):
        gameTemplate = Game.objects.get(pk=1) 
        game = TurnProcessor().startGame(gameTemplate, 'TestGame', '1999')
        turn = Turn.objects.get(game=game)
        mp = MapProcessor()
        
        self.assertHomeCities(turn, 'Spain', 'Spain,London,France')
        self.assertHomeCities(turn, 'Russia', 'Latvia,Moscow')
        self.assertHomeCities(turn, 'Ukraine', 'Ukraine')
        
        self.assertNeighbours(game, 'Spain', 'France,Azores')
        self.assertNeighbours(game, 'France', 'Spain,London,Germany,Austria,Atlantic Ocean,Azores')
        
        self.assertGetFlees(turn, 'Spain', 'Spain', 'France,Azores')
        self.assertGetFlees(turn, 'France', 'Spain', 'Spain,London,Atlantic Ocean,Azores,Germany,Austria')
        self.assertGetFlees(turn, 'Germany', 'Spain', 'France,London,Austria,North Sea,Poland,Denmark')
        
        self.assertFleeIndex(turn, 'France', 'Spain', 17)
        self.assertFleeIndex(turn, 'Spain', 'Spain', 16)
        self.assertFleeIndex(turn, 'London', 'Spain', 15)
        self.assertFleeIndex(turn, 'Atlantic Ocean', 'Spain', 14)
        self.assertFleeIndex(turn, 'Azores', 'Spain', 13)
        self.assertFleeIndex(turn, 'Germany', 'Spain', 12)
        
        