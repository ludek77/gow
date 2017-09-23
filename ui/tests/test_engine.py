from django.test import TestCase
from django.core.management import call_command
from ui.models import Game, Turn, Unit, City, Command, CommandType, Field
from ui.engine.Engine import Engine
from ui.engine.TurnProcessor import TurnProcessor
from ui.engine.CommandValidator import CommandValidator

class EngineTests(TestCase):
    
    processor = TurnProcessor()
    engine = Engine()
    validator = CommandValidator()
    
    def setUp(self):
        call_command('loaddata', 'user', verbosity=0)
        call_command('loaddata', 'init', verbosity=0)
        call_command('loaddata', 'test/testworld', verbosity=0)
        
    def assertCity(self, turn, fieldName, countryName):
        city = City.objects.get(turn=turn, field__name=fieldName)
        self.assertEqual(city.country.name, countryName)
        return city
        
    def assertUnit(self, turn, fieldName, unitTypeName, unitCountryName, commandTypeName):
        # assert unit
        unit = Unit.objects.get(turn=turn, field__name=fieldName)
        self.assertEqual(unit.unitType.name, unitTypeName)
        self.assertEqual(unit.country.name, unitCountryName)
        # assert command
        command = Command.objects.get(turn=turn, unit=unit)
        self.assertEqual(command.commandType.name, commandTypeName)
        return unit
    
    def setAssertCommand(self, turn, fieldName, commandTypeName, targetName, expectedResult):
        command = Command.objects.get(turn=turn, unit__field__name=fieldName)
        ct = CommandType.objects.get(name=commandTypeName)
        field = Field.objects.get(game=turn.game, name=targetName)
        command.commandType = ct
        command.args = str(field.pk)
        command.save()
        result = self.validator.validateCommand(command)
        self.assertEqual(result, expectedResult)
        
    def assertNextTurn(self, turn, turnName):
        nextTurn = self.engine.calculateNextTurn(turn)
        self.assertEqual(nextTurn.previous, turn)
        self.assertEqual(nextTurn.name, turnName)
        return nextTurn
        
    def test_Engine(self):
        gameTemplate = Game.objects.get(pk=1) 
        
        testGame = self.processor.startGame(gameTemplate, 'TestGame', '1999')
        turn = Turn.objects.get(game=testGame)
        self.assertNotEqual(turn, None)
        self.assertEqual(turn.newUnits, True)
        self.assertEqual(turn.game, testGame)
        self.assertCity(turn, 'Spain', 'Spain')
        self.assertCity(turn, 'France', 'Spain')
        self.assertCity(turn, 'London', 'Spain')
        
        turn = self.assertNextTurn(turn, '2000')
        # verify units
        self.assertUnit(turn, 'Spain', 'Ship', 'Spain', 'defend')
        self.assertUnit(turn, 'France', 'Soldier', 'Spain', 'defend')
        self.assertUnit(turn, 'London', 'Ship', 'Spain', 'defend')
        self.assertUnit(turn, 'Latvia', 'Ship', 'Russia', 'defend')
        self.assertUnit(turn, 'Moscow', 'Soldier', 'Russia', 'defend')
        self.assertUnit(turn, 'Ukraine', 'Soldier', 'Russia', 'defend')
        # set commands
        self.setAssertCommand(turn, 'France', 'attack', 'Atlantic Ocean', 'invalid.not_reachable:par_0') # OK'soldier -> sea
        self.setAssertCommand(turn, 'France', 'attack', 'Germany', None) # OK
        self.setAssertCommand(turn, 'Spain', 'attack', 'Germany', 'invalid.not_next:par_0') # not neighbour
        
        turn = self.assertNextTurn(turn, '2001')
        # verify units
        self.assertUnit(turn, 'Germany', 'Soldier', 'Spain', 'defend')
