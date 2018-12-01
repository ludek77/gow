from django.test import TestCase
from django.core.management import call_command
from ui.models import Game, Turn, Unit, City, Command, CommandType, Field
from ui.engine.Engine import Engine
from ui.engine.TurnProcessor import TurnProcessor
from ui.engine.MapProcessor import MapProcessor
from ui.engine.CommandValidator import CommandValidator

class TestBase(TestCase):
    
    processor = TurnProcessor()
    engine = Engine()
    validator = CommandValidator()
    
    def setUp(self):
        self.importJson('user')
        self.importJson('init')
        self.importJson('test/testWorld')
        self.importJson('test/testUnits')
        
    def importJson(self, fileName):
        call_command('loaddata', fileName, verbosity=0)
        
    def setDefaultEscapes(self, turn):
        mapProcessor = MapProcessor(turn)
        cmds = Command.objects.filter(unit__turn=turn)
        for cmd in cmds:
            cmd.escape = mapProcessor.getEscapeFieldPks(cmd.unit)
            cmd.save()
            #print(str(cmd.unit)+':'+cmd.escape)
        
    def assertCity(self, turn, fieldName, countryName):
        city = City.objects.get(turn=turn, field__name=fieldName)
        self.assertEqual(city.country.name, countryName)
        return city
    
    def assertNoUnit(self, turn, fieldName):
        units = Unit.objects.filter(turn=turn, field__name=fieldName)
        self.assertEqual(len(units), 0)
        
    def assertUnit(self, turn, fieldName, unitTypeName, unitCountryName, commandTypeName='defend'):
        # assert unit
        unit = Unit.objects.get(turn=turn, field__name=fieldName)
        self.assertEqual(unit.unitType.name, unitTypeName)
        self.assertEqual(unit.country.name, unitCountryName)
        # assert command
        command = Command.objects.get(unit=unit)
        self.assertEqual(command.commandType.name, commandTypeName)
        return unit

    def assertResult(self, turn, fieldName, expectedResult):
        command = Command.objects.get(unit__turn=turn, unit__field__name=fieldName)
        self.assertEqual(command.result, expectedResult)
    
    def setAssertCommand(self, turn, fieldName, commandTypeName, targetName=None, expectedResult=None):
        command = Command.objects.get(unit__turn=turn, unit__field__name=fieldName)
        ct = CommandType.objects.get(name=commandTypeName)
        args = ''
        if isinstance(targetName, list):
            args = ''
            separator = ''
            for tName in targetName:
                if tName is not None:
                    field = Field.objects.get(game=turn.game, name=tName)
                    args += separator + str(field.pk)
                else:
                    args += separator+'0'
                separator = ','
            args 
        else:
            if targetName is not None:
                field = Field.objects.get(game=turn.game, name=targetName)
                args = str(field.pk)
        command.commandType = ct
        command.args = args
        command.save()
        result = self.validator.validateCommand(command)
        self.assertEqual(result, expectedResult)
        
    def assertNextTurn(self, turn, turnName, message=None):
        if message is not None:
            newUnits = '_'
            if turn.newUnits:
                newUnits = 'R'
            print(turnName + newUnits + ' : ' + message)
        nextTurn = self.engine.calculateNextTurn(turn)
        self.assertEqual(nextTurn.previous, turn)
        self.assertEqual(nextTurn.name, turnName)
        return nextTurn
    
    def assertEscapes(self, turn, fieldName, expectedEscapes):
        command = Command.objects.get(unit__turn=turn, unit__field__name=fieldName)
        keys = command.escape.split(',')
        result = []
        for key in keys:
            field = Field.objects.get(game=turn.game, pk=key)
            result.append(field.name)
        self.assertEqual(expectedEscapes,result)