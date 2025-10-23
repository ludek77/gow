from ui.tests.TestBase import TestBase
from ui.models import Turn, CityCommand
from ui.engine.MapProcessor import MapProcessor

class TestAddRemove(TestBase):

    def testAddPriorities(self):
        turn = Turn.objects.get(pk=1)
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'AddRemove: Add Priorities')
        turn = self.assertNextTurn(turn, '2001', 'AddRemove: Add Priorities')
        # assert adding/removing
        self.assertAddCommands(turn, 'Spain', ['Spain','London','France','Ireland'])
        self.assertAddCommands(turn, 'Russia', ['Ukraine','Latvia','Moscow','Latuvia'])
        # change priority
        self.assertOrderCommand(turn, 'Spain', 'London', -9)
        self.assertAddCommands(turn, 'Spain', ['London','Spain','France','Ireland'])
        # change priority
        self.assertOrderCommand(turn, 'Spain', 'Ireland', -9)
        self.assertAddCommands(turn, 'Spain', ['Ireland','London','Spain','France'])
        # change priority
        self.assertOrderCommand(turn, 'Spain', 'Ireland', -9)
        self.assertAddCommands(turn, 'Spain', ['Ireland','London','Spain','France'])
        # change priority
        self.assertOrderCommand(turn, 'Spain', 'London', 9)
        self.assertAddCommands(turn, 'Spain', ['Ireland','Spain','France', 'London'])
        # change priority
        self.assertOrderCommand(turn, 'Spain', 'London', 9)
        self.assertAddCommands(turn, 'Spain', ['Ireland','Spain','France', 'London'])
        # change priority
        self.assertOrderCommand(turn, 'Spain', 'France', 9)
        self.assertAddCommands(turn, 'Spain', ['Ireland','Spain','London','France'])
        # change priority
        self.assertOrderCommand(turn, 'Spain', 'Ireland', 9)
        self.assertAddCommands(turn, 'Spain', ['Spain','London','France','Ireland'])
        # change priority
        self.assertOrderCommand(turn, 'Spain', 'Ireland', -1)
        self.assertAddCommands(turn, 'Spain', ['Spain','London','Ireland','France'])
        # change priority
        self.assertOrderCommand(turn, 'Spain', 'Ireland', -1)
        self.assertAddCommands(turn, 'Spain', ['Spain','Ireland','London','France'])
        # change priority
        self.assertOrderCommand(turn, 'Spain', 'Ireland', -1)
        self.assertAddCommands(turn, 'Spain', ['Ireland','Spain','London','France'])
        # change priority
        self.assertOrderCommand(turn, 'Spain', 'Ireland', -1)
        self.assertAddCommands(turn, 'Spain', ['Ireland','Spain','London','France'])
        # change priority
        self.assertOrderCommand(turn, 'Spain', 'Ireland', 1)
        self.assertAddCommands(turn, 'Spain', ['Spain','Ireland','London','France'])
        # change priority
        self.assertOrderCommand(turn, 'Spain', 'Spain', 1)
        self.assertAddCommands(turn, 'Spain', ['Ireland','Spain','London','France'])
        # change priority
        self.assertOrderCommand(turn, 'Spain', 'Spain', 1)
        self.assertAddCommands(turn, 'Spain', ['Ireland','London','Spain','France'])
        # change priority
        self.assertOrderCommand(turn, 'Spain', 'Spain', 1)
        self.assertAddCommands(turn, 'Spain', ['Ireland','London','France','Spain'])
        # change priority
        self.assertOrderCommand(turn, 'Spain', 'Spain', 1)
        self.assertAddCommands(turn, 'Spain', ['Ireland','London','France','Spain'])
        # change priority
        self.assertOrderCommand(turn, 'Spain', 'Spain', 1)
        self.assertAddCommands(turn, 'Spain', ['Ireland','London','France','Spain'])

    def testRemovePriorities(self):
        turn = Turn.objects.get(pk=1)
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'AddRemove: Remove Priorities')
        self.assertRemoveCommands(turn, 'Spain', ['Austria','Germany','North Sea','France'])
        # change priority
        self.assertOrderUnitCommand(turn, 'Spain', 'Austria', 9)
        self.assertRemoveCommands(turn, 'Spain', ['Germany','North Sea','France','Austria'])
        # change priority
        self.assertOrderUnitCommand(turn, 'Spain', 'North Sea', 9)
        self.assertRemoveCommands(turn, 'Spain', ['Germany','France','Austria','North Sea'])
        # change priority
        self.assertOrderUnitCommand(turn, 'Spain', 'North Sea', 9)
        self.assertRemoveCommands(turn, 'Spain', ['Germany','France','Austria','North Sea'])
        # change priority
        self.assertOrderUnitCommand(turn, 'Spain', 'North Sea', -9)
        self.assertRemoveCommands(turn, 'Spain', ['North Sea','Germany','France','Austria'])
        # change priority
        self.assertOrderUnitCommand(turn, 'Spain', 'North Sea', -9)
        self.assertRemoveCommands(turn, 'Spain', ['North Sea','Germany','France','Austria'])
        # change priority
        self.assertOrderUnitCommand(turn, 'Spain', 'France', -9)
        self.assertRemoveCommands(turn, 'Spain', ['France','North Sea','Germany','Austria'])
        # change priority
        self.assertOrderUnitCommand(turn, 'Spain', 'France', 1)
        self.assertRemoveCommands(turn, 'Spain', ['North Sea','France','Germany','Austria'])
        # change priority
        self.assertOrderUnitCommand(turn, 'Spain', 'France', 1)
        self.assertRemoveCommands(turn, 'Spain', ['North Sea','Germany','France','Austria'])
        # change priority
        self.assertOrderUnitCommand(turn, 'Spain', 'France', 1)
        self.assertRemoveCommands(turn, 'Spain', ['North Sea','Germany','Austria','France'])
        # change priority
        self.assertOrderUnitCommand(turn, 'Spain', 'France', 1)
        self.assertRemoveCommands(turn, 'Spain', ['North Sea','Germany','Austria','France'])
        # change priority
        self.assertOrderUnitCommand(turn, 'Spain', 'France', -1)
        self.assertRemoveCommands(turn, 'Spain', ['North Sea','Germany','France','Austria'])
        # change priority
        self.assertOrderUnitCommand(turn, 'Spain', 'France', -1)
        self.assertRemoveCommands(turn, 'Spain', ['North Sea','France','Germany','Austria'])
        # change priority
        self.assertOrderUnitCommand(turn, 'Spain', 'France', -1)
        self.assertRemoveCommands(turn, 'Spain', ['France','North Sea','Germany','Austria'])
        # change priority
        self.assertOrderUnitCommand(turn, 'Spain', 'France', -1)
        self.assertRemoveCommands(turn, 'Spain', ['France','North Sea','Germany','Austria'])

    def testDoRemovePriorities(self):
        turn = Turn.objects.get(pk=1)
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'AddRemove: Remove Priorities')
        self.assertRemoveCommands(turn, 'Spain', ['Austria','Germany','North Sea','France'])
        self.setAssertCommand(turn, 'North Sea', 'move', 'Norway')
        self.assertRemoveCommands(turn, 'Russia', ['Norwegian Sea','Baltic Sea','Croatia','Sweden','Ukraine'])
        # calculate turn
        turn = self.assertNextTurn(turn, '2001', 'AddRemove: Remove Priorities')
        self.assertRemoveCommands(turn, 'Spain', ['Norway','Austria','Germany','France'])
        self.setAssertCommand(turn, 'France', 'move', 'Spain')
        self.setAssertCommand(turn, 'Germany', 'move', 'France')
        self.setAssertCommand(turn, 'Austria', 'move', 'Poland')
        self.setAssertCommand(turn, 'Norway', 'move', ['North Sea','London'])
        # calculate turn
        turn = self.assertNextTurn(turn, '2002', 'AddRemove: Remove Priorities')
        self.assertRemoveCommands(turn, 'Spain', ['Poland','France','London','Spain'])
    
    def testSingleAddRemove(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertNoUnit(turn, 'Norway')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertUnit(turn, 'Sweden', 'Army', 'Russia')
        self.assertCity(turn, 'Sweden', 'Russia')
        # do command
        self.setAssertCommand(turn, 'Sweden', 'move', 'Norway')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'AddRemove: Move units')
        self.assertEqual(False,turn.newUnits)
        # verify units
        self.assertNoUnit(turn, 'Sweden')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertUnit(turn, 'Norway', 'Army', 'Russia')
        self.assertCity(turn, 'Sweden', 'Russia')
        # move unit
        self.setAssertCommand(turn, 'North Sea', 'move', 'Sweden')
        # calculate turn
        turn = self.assertNextTurn(turn, '2001', 'AddRemove: Dont take city yet')
        self.assertEqual(True,turn.newUnits)
        self.assertAddCommands(turn, 'Spain', ['Spain','London','France','Ireland'])
        self.assertRemoveCommands(turn, 'Russia', ['Norwegian Sea','Norway','Baltic Sea','Croatia','Ukraine'])
        # verify units
        self.assertUnit(turn, 'Norway', 'Army', 'Russia')
        self.assertUnit(turn, 'Sweden', 'Ship', 'Spain')
        self.assertCity(turn, 'Sweden', 'Russia')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Russia')
        self.assertNoUnit(turn, 'Spain')
        self.setAssertCityCommand(turn, 'Spain', 'Ship')
        # calculate turn
        turn = self.assertNextTurn(turn, '2002', 'AddRemove: Take City')
        self.assertEqual(False,turn.newUnits)
        # verify units
        self.assertUnit(turn, 'Norway', 'Army', 'Russia')
        self.assertUnit(turn, 'Sweden', 'Ship', 'Spain')
        self.assertCity(turn, 'Sweden', 'Spain')
        self.assertUnit(turn, 'Spain', 'Ship', 'Spain')
        self.assertNoUnit(turn, 'Norwegian Sea')
        
