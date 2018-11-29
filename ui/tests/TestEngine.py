from ui.tests.TestBase import TestBase
from ui.models import Turn, Game

class TestEngine(TestBase):
        
    def testEngine(self):
        # start game from template
        gameTemplate = Game.objects.get(pk=1) 
        testGame = self.processor.startGame(gameTemplate, 'TestGame', '1999')
   
        # verify first turn     
        turn = Turn.objects.get(game=testGame)
        self.assertNotEqual(turn, None)
        self.assertEqual(turn.newUnits, True)
        self.assertEqual(turn.game, testGame)
        self.assertCity(turn, 'Spain', 'Spain')
        self.assertCity(turn, 'France', 'Spain')
        self.assertCity(turn, 'London', 'Spain')
        self.assertCity(turn, 'Ireland', 'Spain')
        self.assertCity(turn, 'Latvia', 'Russia')
        self.assertCity(turn, 'Moscow', 'Russia')
        self.assertCity(turn, 'Latuvia', 'Russia')
        self.assertCity(turn, 'Ukraine', 'Russia')
        self.assertNoUnit(turn, 'Spain')
        self.assertNoUnit(turn, 'France')
        self.assertNoUnit(turn, 'London')
        # calculate first turn
        turn = self.assertNextTurn(turn, '2000', 'Engine: Start game')
        # verify units
        self.assertUnit(turn, 'Spain', 'Army', 'Spain')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
        self.assertUnit(turn, 'London', 'Ship', 'Spain')
        self.assertUnit(turn, 'Ireland', 'Ship', 'Spain')
        self.assertUnit(turn, 'Latvia', 'Army', 'Russia')
        self.assertUnit(turn, 'Moscow', 'Army', 'Russia')
        self.assertUnit(turn, 'Ukraine', 'Army', 'Russia')
        self.assertUnit(turn, 'Latuvia', 'Army', 'Russia')
        
        # verify wrong parameters
        self.setAssertCommand(turn, 'Spain', 'defend', None, None)
        self.setAssertCommand(turn, 'Spain', 'defend', 'France', 'invalid.too-many-parameters')
        self.setAssertCommand(turn, 'Spain', 'defend', ['France','Austria'], 'invalid.too-many-parameters')
        self.setAssertCommand(turn, 'Spain', 'attack', 'France', None)
        self.setAssertCommand(turn, 'Spain', 'attack', None, 'invalid.empty:par_0')
        self.setAssertCommand(turn, 'Spain', 'attack', ['France','Austria'], 'invalid.too-many-parameters')
        self.setAssertCommand(turn, 'Spain', 'attack', 'Spain', 'invalid.not_next:par_0')
        self.setAssertCommand(turn, 'Spain', 'attack', 'Austria', 'invalid.not_next:par_0')
        self.setAssertCommand(turn, 'Spain', 'attack', 'Bay of Biscai', 'invalid.not_reachable:par_0')
        self.setAssertCommand(turn, 'London', 'attack', 'France', None)
        self.setAssertCommand(turn, 'London', 'attack', 'Spain', 'invalid.not_next:par_0')
        self.setAssertCommand(turn, 'Spain', 'move', 'France', None)
        self.setAssertCommand(turn, 'Spain', 'move', ['France', 'Germany'], None)
        self.setAssertCommand(turn, 'Spain', 'move', None, 'invalid.empty:par_0')
        self.setAssertCommand(turn, 'Spain', 'move', ['France', 'Croatia'], 'invalid.not_next:par_1')
        self.setAssertCommand(turn, 'Spain', 'move', ['France', 'Bay of Biscai'], 'invalid.not_reachable:par_1')
        self.setAssertCommand(turn, 'Spain', 'move', ['France', 'Austria', 'Croatia'], 'invalid.too-many-parameters')
        self.setAssertCommand(turn, 'Spain', 'move', ['France', 'Germany', 'Poland'], 'invalid.too-many-parameters')
        self.setAssertCommand(turn, 'Spain', 'support_defence',  'France', None)
        self.setAssertCommand(turn, 'Spain', 'support_defence', None, 'invalid.empty:par_0')
        self.setAssertCommand(turn, 'Spain', 'support_defence',  ['France', 'France'], 'invalid.too-many-parameters')
        self.setAssertCommand(turn, 'Spain', 'support_defence',  'Croatia', 'invalid.not_next:par_0')
        self.setAssertCommand(turn, 'Spain', 'support_defence',  'Bay of Biscai', 'invalid.not_reachable:par_0')
        self.setAssertCommand(turn, 'Spain', 'support_attack',  ['France', 'London'], None)
        self.setAssertCommand(turn, 'Spain', 'support_attack',  ['France', 'Spain'], None)
        self.setAssertCommand(turn, 'Spain', 'support_attack', None, 'invalid.empty:par_0')
        self.setAssertCommand(turn, 'Spain', 'support_attack',  'France', 'invalid.empty:par_1')
        self.setAssertCommand(turn, 'Spain', 'support_attack',  ['Austria', 'London'], 'invalid.not_next:par_0')
        self.setAssertCommand(turn, 'Spain', 'support_attack',  ['France', 'Austria'], 'invalid.missing_unit:par_1')
        self.setAssertCommand(turn, 'Spain', 'support_attack',  ['France', 'Spain', 'London'], 'invalid.too-many-parameters')
        # set commands
        self.setAssertCommand(turn, 'London', 'move', ['North Sea','Norwegian Sea'], None)
        self.setAssertCommand(turn, 'Ireland', 'move', ['London','North Sea'], None)
        self.setAssertCommand(turn, 'Spain', 'defend', None)
        self.setAssertCommand(turn, 'France', 'move', 'Germany', None)
        # calculate turn
        turn = self.assertNextTurn(turn, '2001', 'Engine: Testing neighbours')
        # verify units
        self.assertResult(turn.previous, 'Spain', 'ok')
        self.assertUnit(turn, 'Spain', 'Army', 'Spain')
        self.assertResult(turn.previous, 'France', 'ok')
        self.assertNoUnit(turn, 'France')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertResult(turn.previous, 'London', 'ok')
        self.assertNoUnit(turn, 'London')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Ireland', 'ok')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertNoUnit(turn, 'Ireland')
        
        # verify invasions
        self.setAssertCommand(turn, 'North Sea', 'invade', None, 'invalid.not-command-for-unit')
        self.setAssertCommand(turn, 'Germany', 'invade', None, 'invalid.empty:par_0')
        self.setAssertCommand(turn, 'Germany', 'invade', 'Austria', 'invalid.not_field:Sea.par_0')
        self.setAssertCommand(turn, 'Germany', 'invade', 'North Sea', 'invalid.empty:par_2')
        self.setAssertCommand(turn, 'Germany', 'invade', ['Austria','Poland'], 'invalid.not_field:Sea.par_0')
        self.setAssertCommand(turn, 'Germany', 'invade', ['North Sea','Poland'], 'invalid.not_next:par_1')
        self.setAssertCommand(turn, 'Germany', 'invade', ['North Sea',None,'Denmark'], None)
        self.setAssertCommand(turn, 'Germany', 'invade', ['North Sea',None,None], 'invalid.empty:par_2')
        self.setAssertCommand(turn, 'North Sea', 'transport', 'Germany', None)
        self.setAssertCommand(turn, 'North Sea', 'transport', None, 'invalid.empty:par_0')
        self.setAssertCommand(turn, 'North Sea', 'transport', ['Germany', 'Germany'], 'invalid.too-many-parameters')
        self.setAssertCommand(turn, 'Spain', 'transport', None, 'invalid.not-command-for-unit')
        
        
