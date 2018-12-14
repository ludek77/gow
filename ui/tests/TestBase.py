from django.test import TestCase
from django.core.management import call_command
from ui.models import Game, Turn, Unit, City, Command, CommandType, Field, CityCommand, UnitType
from ui.engine.Engine import Engine
from ui.engine.TurnProcessor import TurnProcessor
from ui.engine.MapProcessor import MapProcessor
from ui.engine.CommandValidator import CommandValidator
from encodings import unicode_escape

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
        
    def setAssertCityCommand(self, turn, fieldName, unitTypeName, expectedResult=None):
        command = CityCommand.objects.get(city__turn=turn, city__field__name=fieldName)
        ut = UnitType.objects.get(name=unitTypeName)
        command.newUnitType = ut
        command.save()
        result = self.validator.validateCityCommand(command)
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
        
    def setAssertEscape(self, turn, fieldName, escapeName, escapes, message=None):
        mapProcessor = MapProcessor(turn)
        command = Command.objects.get(unit__turn=turn, unit__field__name=fieldName)
        field = Field.objects.get(game=turn.game, name=escapeName)
        self.assertEqual(mapProcessor.setPriorityEscape(command, field), message)
        result = []
        keys = command.escape.split(',')
        for key in keys:
            field = Field.objects.get(game=turn.game, pk=key)
            result.append(field.name)
        self.assertEqual(escapes, result)
        
    def assertOrderCommand(self, turn, countryName, fieldName, priority): #priority: -9,-1,1,9
        commands = CityCommand.objects.filter(city__turn=turn,city__country__name=countryName).order_by('priority')
        processor = MapProcessor(turn)
        cmd = CityCommand.objects.get(city__turn=turn,city__country__name=countryName,city__field__name=fieldName)
        processor.orderCommand(cmd, priority, commands)

    def assertOrderUnitCommand(self, turn, countryName, fieldName, priority): #priority: -9,-1,1,9
        commands = Command.objects.filter(unit__turn=turn,unit__country__name=countryName).order_by('removePriority')
        processor = MapProcessor(turn)
        cmd = Command.objects.get(unit__turn=turn,unit__country__name=countryName,unit__field__name=fieldName)
        processor.orderCommand(cmd, priority, commands)
        
    def assertAddCommands(self, turn, countryName, expectedResult):
        cmds = CityCommand.objects.filter(city__turn=turn, city__country__name=countryName, city__field__home__name=countryName).order_by('priority')
        i = 0
        for er in expectedResult:
            cmd = cmds[i]
            self.assertEquals(er, cmd.city.field.name)
            i += 1
        
    def assertRemoveCommands(self, turn, countryName, expectedResult):
        cmds = Command.objects.filter(unit__turn=turn, unit__country__name=countryName).order_by('removePriority')
        i = 0
        for er in expectedResult:
            cmd = cmds[i]
            self.assertEquals(er, cmd.unit.field.name)
            i += 1
