from ui.tests.TestBase import TestBase
from ui.models import Turn, Game

class TestEngine(TestBase):
        
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
        self.assertCity(turn, 'Ukraine', 'Ukraine')
        self.assertNoUnit(turn, 'Spain')
        self.assertNoUnit(turn, 'France')
        self.assertNoUnit(turn, 'London')
        # calculate first turn
        turn = self.assertNextTurn(turn, '2000', 'Engine: Start game')
        # verify units
        self.assertUnit(turn, 'Spain', 'Ship', 'Spain')
        self.assertUnit(turn, 'France', 'Soldier', 'Spain')
        self.assertUnit(turn, 'London', 'Ship', 'Spain')
        self.assertUnit(turn, 'Latvia', 'Ship', 'Russia')
        self.assertUnit(turn, 'Moscow', 'Soldier', 'Russia')
        self.assertUnit(turn, 'Ukraine', 'Soldier', 'Ukraine')
        # verify flees
        self.assertEscapes(turn, 'Spain', ['France','Azores'])
        self.assertEscapes(turn, 'France', ['Spain','London', 'Germany', 'Austria'])
        self.assertEscapes(turn, 'London', ['France','Atlantic Ocean', 'North Sea'])
        self.assertEscapes(turn, 'Ukraine', ['Poland','Latvia','Moscow','Croatia'])
        self.assertEscapes(turn, 'Latvia', ['Poland','Baltic Sea'])
        self.assertEscapes(turn, 'Moscow', ['Latvia','Ukraine'])
        
        # verify commands
        self.setAssertCommand(turn, 'Spain', 'attack', 'Spain', 'invalid.not_next:par_0')
        self.setAssertCommand(turn, 'Spain', 'attack', 'Germany', 'invalid.not_next:par_0')
        self.setAssertCommand(turn, 'France', 'attack', 'Azores', 'invalid.not_reachable:par_0')
        self.setAssertCommand(turn, 'London', 'attack', 'France', None)
        self.setAssertCommand(turn, 'Latvia', 'move', 'Moscow', 'invalid.not_reachable:par_0')
        self.setAssertCommand(turn, 'Moscow', 'move', 'Latvia', None)
        self.setAssertCommand(turn, 'Ukraine', 'move', 'Germany', 'invalid.not_next:par_0')
        # calculate turn
        turn = self.assertNextTurn(turn, '2001', 'Engine: Testing neighbours')
        # verify units
        self.assertResult(turn.previous, 'Spain', 'invalid.not_next:par_0')
        self.assertUnit(turn, 'Spain', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'France', 'invalid.not_reachable:par_0')
        self.assertUnit(turn, 'France', 'Soldier', 'Spain')
        self.assertResult(turn.previous, 'London', 'fail.defence-stronger')
        self.assertUnit(turn, 'London', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Latvia', 'invalid.not_reachable:par_0')
        self.assertUnit(turn, 'Latvia', 'Ship', 'Russia')
        self.assertResult(turn.previous, 'Moscow', 'fail.target-not-empty:par_0')
        self.assertUnit(turn, 'Moscow', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Ukraine', 'invalid.not_next:par_0')
        self.assertUnit(turn, 'Ukraine', 'Soldier', 'Ukraine')
        
