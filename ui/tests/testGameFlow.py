from ui.tests.TestBase import TestBase
from ui.models import Turn, Game

class TestGameFlow(TestBase):
        
    def testFlow(self):
        # start game from template
        gameTemplate = Game.objects.get(pk=1) 
        testGame = self.processor.startGame(gameTemplate, 'TestGame', '1999')
        self.assertEqual(1, testGame.status)
   
        # verify first turn     
        turn = Turn.objects.get(game=testGame)
        self.assertEqual(turn.newUnits, True)
        self.assertCity(turn, 'Spain', 'Spain')
        self.assertNoUnit(turn, 'Spain')
        self.assertCity(turn, 'France', 'Spain')
        self.assertNoUnit(turn, 'France')
        self.assertCity(turn, 'London', 'Spain')
        self.assertNoUnit(turn, 'London')
        self.assertCity(turn, 'Ireland', 'Spain')
        self.assertNoUnit(turn, 'Ireland')
        self.assertCity(turn, 'Latvia', 'Russia')
        self.assertNoUnit(turn, 'Latvia')
        self.assertCity(turn, 'Moscow', 'Russia')
        self.assertNoUnit(turn, 'Moscow')
        self.assertCity(turn, 'Latuvia', 'Russia')
        self.assertNoUnit(turn, 'Latuvia')
        self.assertCity(turn, 'Ukraine', 'Russia')
        self.assertNoUnit(turn, 'Ukraine')
        self.assertCity(turn, 'Sweden', 'Russia')
        self.assertNoUnit(turn, 'Sweden')
        # calculate first turn
        turn = self.assertNextTurn(turn, '2000', 'TestGameFlow: Start game')
        testGame = Game.objects.get(pk=testGame.pk) 
        self.assertEqual(1, testGame.status)
        self.assertEqual(turn.newUnits, False)
        # verify units
        self.assertUnit(turn, 'Spain', 'Army', 'Spain')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
        self.assertUnit(turn, 'London', 'Ship', 'Spain')
        self.assertUnit(turn, 'Ireland', 'Ship', 'Spain')
        self.assertUnit(turn, 'Latvia', 'Army', 'Russia')
        self.assertUnit(turn, 'Moscow', 'Army', 'Russia')
        self.assertUnit(turn, 'Ukraine', 'Army', 'Russia')
        self.assertUnit(turn, 'Latuvia', 'Army', 'Russia')
        self.assertUnit(turn, 'Sweden', 'Ship', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'London', 'move', ['North Sea','Sweden'], None)
        self.setAssertCommand(turn, 'Ireland', 'move', ['London','North Sea'], None)
        self.setAssertCommand(turn, 'Sweden', 'move', 'Norway', None)
        self.setAssertCommand(turn, 'Latvia', 'move', ['Poland','Germany'], None)
        self.setAssertCommand(turn, 'Ukraine', 'move', ['Croatia','Austria'], None)
        self.setAssertCommand(turn, 'Latuvia', 'move', ['Latvia','Poland'], None)
        # calculate turn
        turn = self.assertNextTurn(turn, '2001', 'TeStGameFlow: turn')
        testGame = Game.objects.get(pk=testGame.pk) 
        self.assertEqual(1, testGame.status)
        self.assertEqual(turn.newUnits, True)
        # verify units
        self.assertCity(turn, 'Sweden', 'Russia')
        self.assertUnit(turn, 'Sweden', 'Ship', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertUnit(turn, 'Spain', 'Army', 'Spain')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
        self.assertUnit(turn, 'Norway', 'Ship', 'Russia')
        self.assertUnit(turn, 'Germany', 'Army', 'Russia')
        self.assertUnit(turn, 'Austria', 'Army', 'Russia')
        self.assertUnit(turn, 'Poland', 'Army', 'Russia')
        self.assertUnit(turn, 'Moscow', 'Army', 'Russia')
        self.assertAddCommands(turn, 'Spain', ['Spain','London','France','Ireland'])
        self.assertRemoveCommands(turn, 'Spain', ['Sweden','North Sea','France','Spain'])
        self.assertRemoveCommands(turn, 'Russia', ['Austria','Germany','Norway','Poland','Moscow'])
        self.setAssertCityCommand(turn, 'London', 'Army')
        # calculate turn
        turn = self.assertNextTurn(turn, '2002', 'TeStGameFlow: turn')
        testGame = Game.objects.get(pk=testGame.pk) 
        self.assertEqual(1, testGame.status)
        self.assertEqual(turn.newUnits, False)
        # verify units
        self.assertCity(turn, 'Sweden', 'Spain')
        self.assertUnit(turn, 'Sweden', 'Ship', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertUnit(turn, 'Spain', 'Army', 'Spain')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
        self.assertUnit(turn, 'London', 'Army', 'Spain')
        self.assertUnit(turn, 'Norway', 'Ship', 'Russia')
        self.assertUnit(turn, 'Germany', 'Army', 'Russia')
        self.assertUnit(turn, 'Moscow', 'Army', 'Russia')
        self.assertUnit(turn, 'Poland', 'Army', 'Russia')
        self.assertNoUnit(turn, 'Austria')
        # set commands
        self.setAssertCommand(turn, 'France', 'move', ['Germany','Poland'], None)
        self.setAssertCommand(turn, 'Spain', 'move', ['France','Germany'], None)
        self.setAssertCommand(turn, 'Germany', 'move', ['Poland','Croatia'], None)
        self.setAssertCommand(turn, 'Poland', 'move', ['Austria','France'], None)
        # calculate turn
        turn = self.assertNextTurn(turn, '2003', 'TeStGameFlow: turn')
        testGame = Game.objects.get(pk=testGame.pk) 
        self.assertEqual(1, testGame.status)
        self.assertEqual(turn.newUnits, True)
        # verify units
        self.assertCity(turn, 'Spain', 'Spain')
        self.assertCity(turn, 'France', 'Spain')
        self.assertUnit(turn, 'Sweden', 'Ship', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Poland', 'Army', 'Spain')
        self.assertUnit(turn, 'London', 'Army', 'Spain')
        self.assertUnit(turn, 'Norway', 'Ship', 'Russia')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        self.assertUnit(turn, 'Moscow', 'Army', 'Russia')
        self.assertUnit(turn, 'France', 'Army', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'France', 'move', 'Spain', None)
        self.setAssertCommand(turn, 'Croatia', 'move', ['Austria','France'], None)
        self.assertRemoveCommands(turn, 'Spain', ['Poland','Sweden','Germany','North Sea','London'])
        # calculate turn
        turn = self.assertNextTurn(turn, '2004', 'TeStGameFlow: turn')
        testGame = Game.objects.get(pk=testGame.pk) 
        self.assertEqual(2, testGame.status)
        self.assertEqual('Russia', testGame.winner.name)
        self.assertEqual(turn.newUnits, False)
        # verify units
        self.assertCity(turn, 'Spain', 'Russia')
        self.assertCity(turn, 'France', 'Russia')        
        self.assertNoUnit(turn, 'Poland')
        self.assertNoUnit(turn, 'Sweden')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'London', 'Army', 'Spain')
        self.assertUnit(turn, 'Norway', 'Ship', 'Russia')
        self.assertUnit(turn, 'France', 'Army', 'Russia')
        self.assertUnit(turn, 'Moscow', 'Army', 'Russia')
        self.assertUnit(turn, 'Spain', 'Army', 'Russia')
        self.assertUnit(turn, 'Latvia', 'Army', 'Russia')
        self.assertUnit(turn, 'Ukraine', 'Army', 'Russia')
        # test calculation
        turn = self.assertNextTurn(turn, '2005', 'TeStGameFlow: turn')
        self.assertEquals(None, turn)
        