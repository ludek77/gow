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
        
        turn = self.assertNextTurn(turn, '2000')
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
        # set commands
        self.setAssertCommand(turn, 'France', 'attack', 'Germany', None) # OK - beach
        self.setAssertCommand(turn, 'France', 'attack', 'Austria', None) # OK - ground
        self.setAssertCommand(turn, 'France', 'attack', 'Atlantic Ocean', 'invalid.not_reachable:par_0') #  fail sea
        self.setAssertCommand(turn, 'Spain', 'attack', 'Germany', 'invalid.not_next:par_0') # not neighbour
        self.setAssertCommand(turn, 'Spain', 'attack', 'Azores', None) # ok - sea
        self.setAssertCommand(turn, 'Spain', 'attack', 'London', 'invalid.not_next:par_0') # ok - sea
        self.setAssertCommand(turn, 'Spain', 'attack', 'France', None) # ok - beach
        self.setAssertCommand(turn, 'London', 'attack', 'North Sea', None)
        self.setAssertCommand(turn, 'Latvia', 'attack', 'Baltic Sea', None)
        self.setAssertCommand(turn, 'Moscow', 'attack', 'Latvia', None)
        self.setAssertCommand(turn, 'Ukraine', 'attack', 'Poland', None)
        # result: France fails attack Ocean, Spain cant move to France
        
        turn = self.assertNextTurn(turn, '2001')
        # verify units
        self.assertResult(turn.previous, 'France', 'invalid.not_reachable:par_0')
        self.assertUnit(turn, 'France', 'Soldier', 'Spain')
        self.assertResult(turn.previous, 'Spain', 'fail.defence-stronger')
        self.assertUnit(turn, 'Spain', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'London', 'ok')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Ukraine', 'ok')
        self.assertUnit(turn, 'Poland', 'Soldier', 'Ukraine')
        self.assertResult(turn.previous, 'Latvia', 'ok')
        self.assertUnit(turn, 'Baltic Sea', 'Ship', 'Russia')
        self.assertResult(turn.previous, 'Moscow', 'ok')
        self.assertUnit(turn, 'Latvia', 'Soldier', 'Russia')
        self.assertNoUnit(turn, 'Moscow')
        self.assertNoUnit(turn, 'Ukraine')
        self.assertNoUnit(turn, 'London')
        # set commands
        self.setAssertCommand(turn, 'North Sea', 'attack', 'Denmark', None)
        self.setAssertCommand(turn, 'Baltic Sea', 'attack', 'Denmark', None)
        self.setAssertCommand(turn, 'France', 'attack', 'Germany', None)
        self.setAssertCommand(turn, 'Spain', 'attack', 'France', None)
        self.setAssertCommand(turn, 'France', 'attack', 'Germany', None)
        self.setAssertCommand(turn, 'Poland', 'attack', 'Austria', None)
        self.setAssertCommand(turn, 'Latvia', 'attack', 'Poland', None)
        
        turn = self.assertNextTurn(turn, '2002')
        # verify units
        self.assertResult(turn.previous, 'North Sea', 'fail.not-strongest')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Baltic Sea', 'fail.not-strongest')
        self.assertUnit(turn, 'Baltic Sea', 'Ship', 'Russia')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Spain')
        self.assertUnit(turn, 'France', 'Ship', 'Spain')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Ukraine')
        self.assertUnit(turn, 'Poland', 'Soldier', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'France', 'attack', 'Austria', 'invalid.not_reachable:par_0') #  fail sea
        self.setAssertCommand(turn, 'France', 'support_defence', 'Germany', None)
        self.setAssertCommand(turn, 'Germany', 'support_defence', 'Poland', None)
        self.setAssertCommand(turn, 'North Sea', 'attack', 'Denmark', None)
        self.setAssertCommand(turn, 'Baltic Sea', 'move', 'Denmark', None)
        self.setAssertCommand(turn, 'Austria', 'attack', 'Germany', None)
        self.setAssertCommand(turn, 'Poland', 'support_attack', ['Germany', 'Austria'], None)
        
        turn = self.assertNextTurn(turn, '2003')
        # verify units
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'Denmark', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Baltic Sea', 'fail.target-attacked:par_0')
        self.assertUnit(turn, 'Baltic Sea', 'Ship', 'Russia')
        self.assertResult(turn.previous, 'Germany', 'fail.canceled-by-attack')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Spain')
        self.assertResult(turn.previous, 'France', 'ok')
        self.assertUnit(turn, 'France', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Austria', 'fail.defence-stronger')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Ukraine')
        self.assertResult(turn.previous, 'Poland', 'ok')
        self.assertUnit(turn, 'Poland', 'Soldier', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'Denmark', 'attack', 'Baltic Sea', None)
        self.setAssertCommand(turn, 'Baltic Sea', 'attack', 'Denmark', None)
        self.setAssertCommand(turn, 'Germany', 'move', 'Poland', None)
        self.setAssertCommand(turn, 'Poland', 'move', 'Ukraine', None)
        self.setAssertCommand(turn, 'France', 'move', 'Austria', 'invalid.not_reachable:par_0')
        self.setAssertCommand(turn, 'Austria', 'move', 'Croatia', None)
        
        turn = self.assertNextTurn(turn, '2004')
        # verify units
        self.assertResult(turn.previous, 'Denmark', 'fail.not-stronger-than-opposite')
        self.assertUnit(turn, 'Denmark', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Baltic Sea', 'fail.not-stronger-than-opposite')
        self.assertUnit(turn, 'Baltic Sea', 'Ship', 'Russia')
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertUnit(turn, 'Poland', 'Soldier', 'Spain')
        self.assertResult(turn.previous, 'Poland', 'ok')
        self.assertUnit(turn, 'Ukraine', 'Soldier', 'Russia')
        self.assertCity(turn, 'Ukraine', 'Russia')
        self.assertResult(turn.previous, 'France', 'invalid.not_reachable:par_0')
        self.assertUnit(turn, 'France', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Austria', 'ok')
        self.assertUnit(turn, 'Croatia', 'Soldier', 'Ukraine')
        # set commands
        self.setAssertCommand(turn, 'Poland', 'move', 'Ukraine', None)
        self.setAssertCommand(turn, 'Ukraine', 'move', 'Croatia', None)
        self.setAssertCommand(turn, 'Croatia', 'move', 'Poland', None)
        
        turn = self.assertNextTurn(turn, '2005')
        # verify units
        self.assertResult(turn.previous, 'Poland', 'ok')
        self.assertUnit(turn, 'Ukraine', 'Soldier', 'Spain')
        self.assertResult(turn.previous, 'Ukraine', 'ok')
        self.assertUnit(turn, 'Croatia', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Croatia', 'ok')
        self.assertUnit(turn, 'Poland', 'Soldier', 'Ukraine')
        # set commands
        self.setAssertCommand(turn, 'Poland', 'attack', 'Ukraine', None)
        self.setAssertCommand(turn, 'Ukraine', 'attack', 'Croatia', None)
        self.setAssertCommand(turn, 'Croatia', 'attack', 'Poland', None)
        
        turn = self.assertNextTurn(turn, '2006')
        # verify units
        self.assertResult(turn.previous, 'Poland', 'ok')
        self.assertUnit(turn, 'Ukraine', 'Soldier', 'Ukraine')
        self.assertResult(turn.previous, 'Ukraine', 'ok')
        self.assertUnit(turn, 'Croatia', 'Soldier', 'Spain')
        self.assertResult(turn.previous, 'Croatia', 'ok')
        self.assertUnit(turn, 'Poland', 'Soldier', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'Poland', 'attack', 'Ukraine', None)
        self.setAssertCommand(turn, 'Ukraine', 'move', 'Croatia', None)
        self.setAssertCommand(turn, 'Croatia', 'move', 'Poland', None)
        
        turn = self.assertNextTurn(turn, '2007')
        # verify units
        self.assertResult(turn.previous, 'Poland', 'fail.defence-stronger')
        self.assertUnit(turn, 'Poland', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Ukraine', 'fail.canceled-by-attack')
        self.assertUnit(turn, 'Ukraine', 'Soldier', 'Ukraine')
        self.assertResult(turn.previous, 'Croatia', 'fail.target-not-empty:par_0')
        self.assertUnit(turn, 'Croatia', 'Soldier', 'Spain')
        # set commands
        self.setAssertCommand(turn, 'Poland', 'attack', 'Ukraine', None)
        self.setAssertCommand(turn, 'Ukraine', 'move', 'Croatia', None)
        self.setAssertCommand(turn, 'Croatia', 'move', 'Austria', None)
        
        turn = self.assertNextTurn(turn, '2008')
        # verify units
        self.assertResult(turn.previous, 'Poland', 'fail.defence-stronger')
        self.assertUnit(turn, 'Poland', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Ukraine', 'fail.canceled-by-attack')
        self.assertUnit(turn, 'Ukraine', 'Soldier', 'Ukraine')
        self.assertResult(turn.previous, 'Croatia', 'ok')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Spain')
        # set commands
        self.setAssertCommand(turn, 'Poland', 'move', 'Croatia', None)
        self.setAssertCommand(turn, 'Ukraine', 'move', 'Croatia', None)
        self.setAssertCommand(turn, 'Austria', 'move', 'Croatia', None)
        
        turn = self.assertNextTurn(turn, '2009')
        # verify units
        self.assertResult(turn.previous, 'Poland', 'fail.more-moves-to-target:par_0')
        self.assertUnit(turn, 'Poland', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Ukraine', 'fail.more-moves-to-target:par_0')
        self.assertUnit(turn, 'Ukraine', 'Soldier', 'Ukraine')
        self.assertResult(turn.previous, 'Austria', 'fail.more-moves-to-target:par_0')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Spain')
        # set commands
        self.setAssertCommand(turn, 'Poland', 'attack', 'Croatia', None)
        self.setAssertCommand(turn, 'Ukraine', 'attack', 'Croatia', None)
        self.setAssertCommand(turn, 'Austria', 'move', 'Croatia', None)
        
        turn = self.assertNextTurn(turn, '2010')
        # verify units
        self.assertResult(turn.previous, 'Poland', 'fail.not-strongest')
        self.assertUnit(turn, 'Poland', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Ukraine', 'fail.not-strongest')
        self.assertUnit(turn, 'Ukraine', 'Soldier', 'Ukraine')
        self.assertResult(turn.previous, 'Austria', 'fail.target-attacked:par_0')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Spain')
        # set commands
        self.setAssertCommand(turn, 'Poland', 'move', ['Ukraine', 'Croatia'], None)
        self.setAssertCommand(turn, 'Ukraine', 'move', ['Poland', 'Ukraine'], None)
        self.setAssertCommand(turn, 'Austria', 'move', ['Croatia', 'Poland'], None)
        
        turn = self.assertNextTurn(turn, '2011')
        # verify units
        self.assertResult(turn.previous, 'Poland', 'ok')
        self.assertUnit(turn, 'Croatia', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Ukraine', 'ok')
        self.assertUnit(turn, 'Ukraine', 'Soldier', 'Ukraine')
        self.assertResult(turn.previous, 'Austria', 'ok')
        self.assertUnit(turn, 'Poland', 'Soldier', 'Spain')
        # set commands
        self.setAssertCommand(turn, 'Poland', 'move', ['Poland', 'Ukraine'], None)
        self.setAssertCommand(turn, 'Ukraine', 'move', ['Croatia', 'Croatia'], None)
        self.setAssertCommand(turn, 'Croatia', 'move', ['Ukraine', 'Poland'], None)
        
        turn = self.assertNextTurn(turn, '2012')
        # verify units
        self.assertResult(turn.previous, 'Poland', 'ok')
        self.assertUnit(turn, 'Ukraine', 'Soldier', 'Spain')
        self.assertResult(turn.previous, 'Ukraine', 'ok')
        self.assertUnit(turn, 'Croatia', 'Soldier', 'Ukraine')
        self.assertResult(turn.previous, 'Croatia', 'ok')
        self.assertUnit(turn, 'Poland', 'Soldier', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'Poland', 'move', ['Poland', 'Croatia'], None)
        self.setAssertCommand(turn, 'Ukraine', 'move', ['Croatia', 'Ukraine'], None)
        self.setAssertCommand(turn, 'Croatia', 'move', ['Austria', 'Croatia'], None)
        
        turn = self.assertNextTurn(turn, '2013')
        # verify units
        self.assertResult(turn.previous, 'Poland', 'fail.more-moves-to-target:par_1')
        self.assertUnit(turn, 'Poland', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Croatia', 'fail.more-moves-to-target:par_1')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Ukraine')
        self.assertResult(turn.previous, 'Ukraine', 'ok')
        self.assertUnit(turn, 'Ukraine', 'Soldier', 'Spain')
        # set commands
        self.setAssertCommand(turn, 'Poland', 'attack', 'Croatia', None)
        self.setAssertCommand(turn, 'Austria', 'attack', 'Croatia', None)
        self.setAssertCommand(turn, 'Ukraine', 'move', ['Ukraine', 'Croatia'], None)
        
        turn = self.assertNextTurn(turn, '2014')
        # verify units
        self.assertResult(turn.previous, 'Poland', 'fail.not-strongest')
        self.assertUnit(turn, 'Poland', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'fail.not-strongest')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Ukraine')
        self.assertResult(turn.previous, 'Ukraine', 'fail.target-attacked:par_1')
        self.assertUnit(turn, 'Ukraine', 'Soldier', 'Spain')
        # set commands
        self.setAssertCommand(turn, 'Poland', 'move', ['Croatia','Ukraine'], None)
        self.setAssertCommand(turn, 'Austria', 'attack', 'Croatia', None)
        self.setAssertCommand(turn, 'Ukraine', 'move', ['Ukraine', 'Poland'], None)
        
        turn = self.assertNextTurn(turn, '2015')
        # verify units
        self.assertResult(turn.previous, 'Poland', 'fail.target-attacked:par_0')
        self.assertUnit(turn, 'Poland', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'ok')
        self.assertUnit(turn, 'Croatia', 'Soldier', 'Ukraine')
        self.assertResult(turn.previous, 'Ukraine', 'fail.target-not-empty:par_1')
        self.assertUnit(turn, 'Ukraine', 'Soldier', 'Spain')
        # set commands
        self.setAssertCommand(turn, 'Poland', 'support_attack', ['Ukraine','Croatia'], None)
        self.setAssertCommand(turn, 'Croatia', 'attack', 'Ukraine', None)
        self.setAssertCommand(turn, 'Ukraine', 'attack', 'Poland', None)
        
        turn = self.assertNextTurn(turn, '2016')
        # verify units
        self.assertResult(turn.previous, 'Poland', 'ok')
        self.assertUnit(turn, 'Poland', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Croatia', 'ok')
        self.assertUnit(turn, 'Ukraine', 'Soldier', 'Ukraine')
        self.assertResult(turn.previous, 'Ukraine', 'escaped')
        self.assertUnit(turn, 'Latvia', 'Soldier', 'Spain')
        