from django.test import TestCase
from django.core.management import call_command
from ui.models import Game, Turn, Unit, City
from ui.engine.Engine import Engine
from ui.engine.TurnProcessor import TurnProcessor

class EngineTests(TestCase):
    
    def setUp(self):
        call_command('loaddata', 'user', verbosity=0)
        call_command('loaddata', 'init', verbosity=0)
        call_command('loaddata', 'test/testworld', verbosity=0)
        
    def assertCity(self, turn, fieldName, countryName):
        city = City.objects.get(turn=turn, field__name=fieldName)
        self.assertEqual(city.country.name, countryName)
        
    def assertUnit(self, turn, fieldName, unitTypeName, unitCountryName):
        unit = Unit.objects.filter(turn=turn, field__name=fieldName)
        self.assertEqual(len(unit), 1)
        self.assertEqual(unit[0].unitType.name, unitTypeName)
        self.assertEqual(unit[0].country.name, unitCountryName)
        
    def test_Engine(self):
        gameTemplate = Game.objects.get(pk=1) 
        processor = TurnProcessor()
        engine = Engine()
        
        testGame = processor.startGame(gameTemplate, 'TestGame', '1999')
        firstTurn = Turn.objects.get(game=testGame)
        self.assertNotEqual(firstTurn, None)
        self.assertEqual(firstTurn.newUnits, True)
        self.assertEqual(firstTurn.game, testGame)
        self.assertCity(firstTurn, 'Spain', 'Spain')
        self.assertCity(firstTurn, 'France', 'Spain')
        self.assertCity(firstTurn, 'London', 'Spain')
        
        turn = engine.calculateNextTurn(firstTurn)
        self.assertEqual(turn.previous, firstTurn)
        self.assertEqual(turn.name, '2000')
        self.assertUnit(turn, 'Spain', 'Ship', 'Spain')