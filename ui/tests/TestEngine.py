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
        self.assertCity(turn, 'France', 'Ukraine')
        self.assertCity(turn, 'London', 'Spain')
        self.assertCity(turn, 'Ukraine', 'Ukraine')
        self.assertNoUnit(turn, 'Spain')
        self.assertNoUnit(turn, 'France')
        self.assertNoUnit(turn, 'London')
        # calculate first turn
        turn = self.assertNextTurn(turn, '2000', 'Engine: Start game')
        # verify units
        self.assertUnit(turn, 'Spain', 'Ship', 'Spain')
        self.assertUnit(turn, 'France', 'Soldier', 'Ukraine')
        self.assertUnit(turn, 'London', 'Ship', 'Spain')
        self.assertUnit(turn, 'Latvia', 'Ship', 'Russia')
        self.assertUnit(turn, 'Moscow', 'Soldier', 'Russia')
        self.assertUnit(turn, 'Ukraine', 'Soldier', 'Ukraine')
        # verify flees
        self.assertEscapes(turn, 'Spain', ['France','Azores'])
        self.assertEscapes(turn, 'France', ['Germany', 'Austria','Spain','London'])
        self.assertEscapes(turn, 'London', ['France','Atlantic Ocean', 'North Sea'])
        self.assertEscapes(turn, 'Ukraine', ['Poland','Croatia','Latvia','Moscow'])
        self.assertEscapes(turn, 'Latvia', ['Poland','Baltic Sea'])
        self.assertEscapes(turn, 'Moscow', ['Latvia','Ukraine'])
        
        # verify wrong parameters
        self.setAssertCommand(turn, 'Spain', 'defend', None, None)
        self.setAssertCommand(turn, 'Spain', 'defend', 'France', 'invalid.too-many-parameters')
        self.setAssertCommand(turn, 'Spain', 'attack', None, 'invalid.empty:par_0')
        self.setAssertCommand(turn, 'Spain', 'attack', 'France', None)
        self.setAssertCommand(turn, 'Spain', 'attack', ['France','Azores'], 'invalid.too-many-parameters')
        self.setAssertCommand(turn, 'Spain', 'move', None, 'invalid.empty:par_0')
        self.setAssertCommand(turn, 'Spain', 'move', 'Azores', None)
        self.setAssertCommand(turn, 'Spain', 'move', ['Azores', 'France'], None)
        self.setAssertCommand(turn, 'Spain', 'move', ['Azores', 'France', 'Azores'], 'invalid.too-many-parameters')
        self.setAssertCommand(turn, 'Spain', 'support_defence', None, 'invalid.empty:par_0')
        self.setAssertCommand(turn, 'Spain', 'support_defence',  'France', None)
        self.setAssertCommand(turn, 'Spain', 'support_defence',  ['France', 'France'], 'invalid.too-many-parameters')
        self.setAssertCommand(turn, 'Spain', 'support_attack', None, 'invalid.empty:par_0')
        self.setAssertCommand(turn, 'Spain', 'support_attack',  'France', 'invalid.empty:par_1')
        self.setAssertCommand(turn, 'Spain', 'support_attack',  ['Austria', 'London'], 'invalid.not_next:par_0')
        self.setAssertCommand(turn, 'Spain', 'support_attack',  ['France', 'Austria'], 'invalid.missing_unit:par_1')
        self.setAssertCommand(turn, 'Spain', 'support_attack',  ['France', 'London'], None)
        self.setAssertCommand(turn, 'Spain', 'support_attack',  ['France', 'London', 'London'], 'invalid.too-many-parameters')
        self.setAssertCommand(turn, 'Spain', 'transport', None, 'invalid.empty:par_0')
        self.setAssertCommand(turn, 'France', 'transport', None, 'invalid.not-command-for-unit')
        self.setAssertCommand(turn, 'Spain', 'transport', 'France', None)
        self.setAssertCommand(turn, 'Spain', 'transport', ['France', 'France'], 'invalid.too-many-parameters')
        # verify commands
        self.setAssertCommand(turn, 'Spain', 'attack', 'Spain', 'invalid.not_next:par_0')
        self.setAssertCommand(turn, 'Spain', 'attack', 'Azores', None)
        self.setAssertCommand(turn, 'France', 'attack', 'Azores', 'invalid.not_reachable:par_0')
        self.setAssertCommand(turn, 'London', 'attack', 'Atlantic Ocean', None)
        self.setAssertCommand(turn, 'Latvia', 'move', 'Baltic Sea', None)
        self.setAssertCommand(turn, 'Moscow', 'move', 'Latvia', None)
        self.setAssertCommand(turn, 'Ukraine', 'move', 'Germany', 'invalid.not_next:par_0')
        # calculate turn
        turn = self.assertNextTurn(turn, '2001', 'Engine: Testing neighbours')
        # verify units
        self.assertResult(turn.previous, 'Spain', 'ok')
        self.assertUnit(turn, 'Azores', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'France', 'invalid.not_reachable:par_0')
        self.assertUnit(turn, 'France', 'Soldier', 'Ukraine')
        self.assertResult(turn.previous, 'London', 'ok')
        self.assertUnit(turn, 'Atlantic Ocean', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Latvia', 'ok')
        self.assertUnit(turn, 'Baltic Sea', 'Ship', 'Russia')
        self.assertResult(turn.previous, 'Moscow', 'ok')
        self.assertUnit(turn, 'Latvia', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Ukraine', 'invalid.not_next:par_0')
        self.assertUnit(turn, 'Ukraine', 'Soldier', 'Ukraine')
        
        # verify invasions
        self.setAssertCommand(turn, 'Azores', 'invade', None, 'invalid.not-command-for-unit')
        self.setAssertCommand(turn, 'France', 'invade', None, 'invalid.empty:par_0')
        self.setAssertCommand(turn, 'France', 'invade', 'Germany', 'invalid.not_field:Sea.par_0')
        self.setAssertCommand(turn, 'France', 'invade', 'Azores', 'invalid.empty:par_2')
        self.setAssertCommand(turn, 'France', 'invade', ['Azores','Spain'], 'invalid.not_field:Sea.par_1')
        self.setAssertCommand(turn, 'France', 'invade', ['Azores','Atlantic Ocean'], 'invalid.empty:par_2')
        self.setAssertCommand(turn, 'France', 'invade', ['Azores',None,'Spain'], None)
        self.setAssertCommand(turn, 'France', 'invade', ['Azores',None,None], 'invalid.empty:par_2')
        self.setAssertCommand(turn, 'France', 'invade', ['Azores','Atlantic Ocean','London'], None)
        self.setAssertCommand(turn, 'France', 'invade', ['Azores','Atlantic Ocean','Germany'], 'invalid.not_next:par_2')
        
        
