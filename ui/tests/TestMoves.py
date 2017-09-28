from ui.tests.TestBase import TestBase
from ui.models import Turn

class TestAttacks(TestBase):
    
    def setUp(self):
        TestBase.setUp(self)
        self.importJson('test/test_units_1')

    def test(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Atlantic Ocean', 'Ship', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Ukraine')
        self.assertUnit(turn, 'London', 'Soldier', 'Russia')
        self.assertUnit(turn, 'Denmark', 'Soldier', 'Russia')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Ukraine')
        
        # set commands
        self.setAssertCommand(turn, 'Atlantic Ocean', 'move', 'Azores')
        self.setAssertCommand(turn, 'North Sea', 'move', 'London')
        self.setAssertCommand(turn, 'Norwegian Sea', 'move', 'North Sea')
        self.setAssertCommand(turn, 'London', 'move', 'France')
        self.setAssertCommand(turn, 'Denmark', 'move', 'Germany')
        self.setAssertCommand(turn, 'Austria', 'move', 'France')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Moves: Single move, Two moves to one field, Failed train')
        # verify units
        self.assertResult(turn.previous, 'Atlantic Ocean', 'ok')
        self.assertUnit(turn, 'Azores', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'fail.target-not-empty:par_0')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Norwegian Sea', 'fail.target-not-empty:par_0')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'London', 'fail.more-moves-to-target:par_0')
        self.assertUnit(turn, 'London', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Denmark', 'ok')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'fail.more-moves-to-target:par_0')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Ukraine')
        
        # set commands
        self.setAssertCommand(turn, 'Azores', 'move', 'Atlantic Ocean')
        self.setAssertCommand(turn, 'North Sea', 'move', 'Norwegian Sea')
        self.setAssertCommand(turn, 'Norwegian Sea', 'move', 'North Sea')
        self.setAssertCommand(turn, 'London', 'move', 'France')
        self.setAssertCommand(turn, 'Germany', 'move', ['Austria','Germany'])
        self.setAssertCommand(turn, 'Austria', 'move', ['Germany','Austria'])
        # calculate turn
        turn = self.assertNextTurn(turn, '2001', 'Moves: Single and double Switches')
        # verify units
        self.assertResult(turn.previous, 'Azores', 'ok')
        self.assertUnit(turn, 'Atlantic Ocean', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Norwegian Sea', 'ok')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'London', 'ok')
        self.assertUnit(turn, 'France', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'ok')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Ukraine')
        
        # set commands
        self.setAssertCommand(turn, 'Atlantic Ocean', 'move', 'North Sea')
        self.setAssertCommand(turn, 'North Sea', 'move', 'Norwegian Sea')
        self.setAssertCommand(turn, 'Norwegian Sea', 'move', 'Atlantic Ocean')
        self.setAssertCommand(turn, 'France', 'move', ['Germany','France'])
        self.setAssertCommand(turn, 'Germany', 'move', ['Austria','Germany'])
        self.setAssertCommand(turn, 'Austria', 'move', ['France','Austria'])
        # calculate turn
        turn = self.assertNextTurn(turn, '2002', 'Moves: Single and double Trains')
        # verify units
        self.assertResult(turn.previous, 'Atlantic Ocean', 'ok')
        self.assertUnit(turn, 'Atlantic Ocean', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'Norwegian Sea', 'ok')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'France', 'ok')
        self.assertUnit(turn, 'France', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'ok')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Ukraine')
        
        # set commands
        self.setAssertCommand(turn, 'Atlantic Ocean', 'move', 'North Sea')
        self.setAssertCommand(turn, 'North Sea', 'move', 'Germany')
        self.setAssertCommand(turn, 'Norwegian Sea', 'move', 'Atlantic Ocean')
        self.setAssertCommand(turn, 'France', 'move', ['Germany','France'])
        self.setAssertCommand(turn, 'Germany', 'move', ['Austria','Germany'])
        self.setAssertCommand(turn, 'Austria', 'move', ['France','Austria'])
        # calculate turn
        turn = self.assertNextTurn(turn, '2003', 'Moves: Blocked switches and trains')
        # verify units
        self.assertResult(turn.previous, 'Atlantic Ocean', 'fail.target-not-empty:par_0')
        self.assertUnit(turn, 'Atlantic Ocean', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'fail.more-moves-to-target:par_0')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'Norwegian Sea', 'fail.target-not-empty:par_0')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'France', 'fail.more-moves-to-target:par_0')
        self.assertUnit(turn, 'France', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Germany', 'fail.target-not-empty:par_0')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'fail.target-not-empty:par_0')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Ukraine')
        
        # set commands
        self.setAssertCommand(turn, 'Atlantic Ocean', 'move', ['North Sea', 'Germany'])
        self.setAssertCommand(turn, 'North Sea', 'move', ['Norwegian Sea', 'Atlantic Ocean'])
        self.setAssertCommand(turn, 'Norwegian Sea', 'move', ['Atlantic Ocean', 'North Sea'])
        self.setAssertCommand(turn, 'France', 'move', ['Germany','France'])
        self.setAssertCommand(turn, 'Germany', 'move', ['Austria','Germany'])
        self.setAssertCommand(turn, 'Austria', 'move', ['France','Austria'])
        # calculate turn
        turn = self.assertNextTurn(turn, '2004', 'Moves: Blocked second switches and trains')
        # verify units
        self.assertResult(turn.previous, 'Atlantic Ocean', 'fail.more-moves-to-target:par_1')
        self.assertUnit(turn, 'Atlantic Ocean', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'North Sea', 'fail.target-not-empty:par_1')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Norwegian Sea', 'fail.target-not-empty:par_1')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'France', 'fail.target-not-empty:par_1')
        self.assertUnit(turn, 'France', 'Soldier', 'Ukraine')
        self.assertResult(turn.previous, 'Germany', 'fail.more-moves-to-target:par_1')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'fail.target-not-empty:par_1')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Russia')
        
        # set commands
        self.setAssertCommand(turn, 'Atlantic Ocean', 'move', ['North Sea', 'Atlantic Ocean'])
        self.setAssertCommand(turn, 'North Sea', 'move', ['Atlantic Ocean', 'North Sea'])
        self.setAssertCommand(turn, 'Norwegian Sea', 'attack', 'Atlantic Ocean')
        self.setAssertCommand(turn, 'France', 'defend')
        self.setAssertCommand(turn, 'Germany', 'move', ['Germany','Poland'])
        self.setAssertCommand(turn, 'Austria', 'move', ['Poland', 'Austria'])
        # calculate turn
        turn = self.assertNextTurn(turn, '2005', 'Moves: Canceled by attack, Move in second phase')
        # verify units
        self.assertResult(turn.previous, 'Atlantic Ocean', 'fail.canceled-by-attack')
        self.assertUnit(turn, 'Atlantic Ocean', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'North Sea', 'fail.target-attacked:par_0')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Norwegian Sea', 'fail.defence-stronger')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'France', 'ok')
        self.assertUnit(turn, 'France', 'Soldier', 'Ukraine')
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertUnit(turn, 'Poland', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'ok')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Russia')
        
        # set commands
        self.setAssertCommand(turn, 'Atlantic Ocean', 'defend')
        self.setAssertCommand(turn, 'North Sea', 'attack', 'Germany')
        self.setAssertCommand(turn, 'Norwegian Sea', 'defend')
        self.setAssertCommand(turn, 'France', 'move', 'Germany')
        self.setAssertCommand(turn, 'Poland', 'move', ['Poland','Germany'])
        self.setAssertCommand(turn, 'Austria', 'attack', 'Germany')
        # calculate turn
        turn = self.assertNextTurn(turn, '2006', 'Moves: Target attacked')
        # verify units
        self.assertResult(turn.previous, 'Atlantic Ocean', 'ok')
        self.assertUnit(turn, 'Atlantic Ocean', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'North Sea', 'fail.not-strongest')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Norwegian Sea', 'ok')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'France', 'fail.target-attacked:par_0')
        self.assertUnit(turn, 'France', 'Soldier', 'Ukraine')
        self.assertResult(turn.previous, 'Poland', 'fail.target-attacked:par_1')
        self.assertUnit(turn, 'Poland', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'fail.not-strongest')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Russia')
        