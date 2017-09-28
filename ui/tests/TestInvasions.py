from ui.tests.TestBase import TestBase
from ui.models import Turn

class TestInvasions(TestBase):
    
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
        self.setAssertCommand(turn, 'Atlantic Ocean', 'transport', 'London')
        self.setAssertCommand(turn, 'North Sea', 'transport', 'London')
        self.setAssertCommand(turn, 'Norwegian Sea', 'defend')
        self.setAssertCommand(turn, 'London', 'invade', ['Atlantic Ocean', 'North Sea', 'Germany'])
        self.setAssertCommand(turn, 'Denmark', 'defend')
        self.setAssertCommand(turn, 'Austria', 'defend')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Invasion Success: Invasion')
        # verify units
        self.assertResult(turn.previous, 'Atlantic Ocean', 'ok')
        self.assertUnit(turn, 'Atlantic Ocean', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Norwegian Sea', 'ok')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'London', 'ok')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Denmark', 'ok')
        self.assertUnit(turn, 'Denmark', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'ok')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Ukraine')
        
        # set commands
        self.setAssertCommand(turn, 'Atlantic Ocean', 'transport', 'Germany')
        self.setAssertCommand(turn, 'North Sea', 'transport', 'Germany')
        self.setAssertCommand(turn, 'Norwegian Sea', 'defend')
        self.setAssertCommand(turn, 'Germany', 'invade', ['North Sea', 'Atlantic Ocean', 'London'])
        self.setAssertCommand(turn, 'Denmark', 'attack', 'Germany')
        self.setAssertCommand(turn, 'Austria', 'attack', 'Germany')
        # calculate turn
        turn = self.assertNextTurn(turn, '2001', 'Invasion Success: Invasion from attack')
        # verify units
        self.assertResult(turn.previous, 'Atlantic Ocean', 'ok')
        self.assertUnit(turn, 'Atlantic Ocean', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Norwegian Sea', 'ok')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertUnit(turn, 'London', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Denmark', 'fail.not-strongest')
        self.assertUnit(turn, 'Denmark', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'fail.not-strongest')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Ukraine')
        
        # set commands
        self.setAssertCommand(turn, 'Atlantic Ocean', 'transport', 'London')
        self.setAssertCommand(turn, 'North Sea', 'transport', 'London')
        self.setAssertCommand(turn, 'Norwegian Sea', 'attack', 'North Sea')
        self.setAssertCommand(turn, 'London', 'invade', ['Atlantic Ocean', 'North Sea', 'Germany'])
        self.setAssertCommand(turn, 'Denmark', 'defend')
        self.setAssertCommand(turn, 'Austria', 'defend')
        # calculate turn
        turn = self.assertNextTurn(turn, '2002', 'Invasion Fail: Transport under attack')
        # verify units
        self.assertResult(turn.previous, 'Atlantic Ocean', 'ok')
        self.assertUnit(turn, 'Atlantic Ocean', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'fail.canceled-by-attack')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Norwegian Sea', 'fail.defence-stronger')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'London', 'fail.transport-canceled')
        self.assertUnit(turn, 'London', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Denmark', 'ok')
        self.assertUnit(turn, 'Denmark', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'ok')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Ukraine')
        
        # set commands
        self.setAssertCommand(turn, 'Atlantic Ocean', 'transport', 'London')
        self.setAssertCommand(turn, 'North Sea', 'transport', 'London')
        self.setAssertCommand(turn, 'Norwegian Sea', 'defend')
        self.setAssertCommand(turn, 'London', 'invade', ['Atlantic Ocean', 'North Sea', 'Germany'])
        self.setAssertCommand(turn, 'Denmark', 'support_attack', ['Germany', 'Austria'])
        self.setAssertCommand(turn, 'Austria', 'attack', 'Germany')
        # calculate turn
        turn = self.assertNextTurn(turn, '2003', 'Invasion Fail: Invasion not strongest')
        # verify units
        self.assertResult(turn.previous, 'Atlantic Ocean', 'ok')
        self.assertUnit(turn, 'Atlantic Ocean', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Norwegian Sea', 'ok')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'London', 'fail.not-strongest')
        self.assertUnit(turn, 'London', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Denmark', 'ok')
        self.assertUnit(turn, 'Denmark', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'ok')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Ukraine')
        
        # set commands
        self.setAssertCommand(turn, 'Atlantic Ocean', 'transport', 'London')
        self.setAssertCommand(turn, 'North Sea', 'transport', 'London')
        self.setAssertCommand(turn, 'Norwegian Sea', 'defend')
        self.setAssertCommand(turn, 'London', 'invade', ['Atlantic Ocean', 'North Sea', 'Germany'])
        self.setAssertCommand(turn, 'Denmark', 'defend')
        self.setAssertCommand(turn, 'Germany', 'defend')
        # calculate turn
        turn = self.assertNextTurn(turn, '2004', 'Invasion Fail: Target not empty')
        # verify units
        self.assertResult(turn.previous, 'Atlantic Ocean', 'ok')
        self.assertUnit(turn, 'Atlantic Ocean', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Norwegian Sea', 'ok')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'London', 'fail.defence-stronger')
        self.assertUnit(turn, 'London', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Ukraine')
        self.assertResult(turn.previous, 'Denmark', 'ok')
        self.assertUnit(turn, 'Denmark', 'Soldier', 'Russia')
        
        # set commands
        self.setAssertCommand(turn, 'Atlantic Ocean', 'transport', 'London')
        self.setAssertCommand(turn, 'North Sea', 'defend')
        self.setAssertCommand(turn, 'Norwegian Sea', 'defend')
        self.setAssertCommand(turn, 'London', 'invade', ['Atlantic Ocean', 'North Sea', 'Germany'])
        self.setAssertCommand(turn, 'Denmark', 'defend')
        self.setAssertCommand(turn, 'Germany', 'defend')
        # calculate turn
        turn = self.assertNextTurn(turn, '2005', 'Invasion Fail: Transporter not transporting')
        # verify units
        self.assertResult(turn.previous, 'Atlantic Ocean', 'ok')
        self.assertUnit(turn, 'Atlantic Ocean', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Norwegian Sea', 'ok')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'London', 'fail.transport-missing')
        self.assertUnit(turn, 'London', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Ukraine')
        self.assertResult(turn.previous, 'Denmark', 'ok')
        self.assertUnit(turn, 'Denmark', 'Soldier', 'Russia')
        
        # set commands
        self.setAssertCommand(turn, 'Atlantic Ocean', 'transport', 'London')
        self.setAssertCommand(turn, 'North Sea', 'defend')
        self.setAssertCommand(turn, 'Norwegian Sea', 'defend')
        self.setAssertCommand(turn, 'London', 'invade', ['North Sea', 'Atlantic Ocean', 'Germany'], 'invalid.not_next:par_2')
        self.setAssertCommand(turn, 'Denmark', 'defend')
        self.setAssertCommand(turn, 'Germany', 'defend')
        # calculate turn
        turn = self.assertNextTurn(turn, '2006', 'Invasion Fail: Misconfigured invasion: wrong transport sequence')
        # verify units
        self.assertResult(turn.previous, 'Atlantic Ocean', 'ok')
        self.assertUnit(turn, 'Atlantic Ocean', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Norwegian Sea', 'ok')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'London', 'invalid.not_next:par_2')
        self.assertUnit(turn, 'London', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Ukraine')
        self.assertResult(turn.previous, 'Denmark', 'ok')
        self.assertUnit(turn, 'Denmark', 'Soldier', 'Russia')
        
        # set commands
        self.setAssertCommand(turn, 'Atlantic Ocean', 'transport', 'London')
        self.setAssertCommand(turn, 'North Sea', 'defend')
        self.setAssertCommand(turn, 'Norwegian Sea', 'defend')
        self.setAssertCommand(turn, 'London', 'invade', ['Atlantic Ocean', 'Azores', 'Spain'], 'invalid.not_unit:Ship.par_1')
        self.setAssertCommand(turn, 'Denmark', 'defend')
        self.setAssertCommand(turn, 'Germany', 'defend')
        # calculate turn
        turn = self.assertNextTurn(turn, '2007', 'Invasion Fail: Misconfigured invasion: missing transporter')
        # verify units
        self.assertResult(turn.previous, 'Atlantic Ocean', 'ok')
        self.assertUnit(turn, 'Atlantic Ocean', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Norwegian Sea', 'ok')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'London', 'invalid.not_unit:Ship.par_1')
        self.assertUnit(turn, 'London', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Ukraine')
        self.assertResult(turn.previous, 'Denmark', 'ok')
        self.assertUnit(turn, 'Denmark', 'Soldier', 'Russia')
        
        # set commands
        self.setAssertCommand(turn, 'Atlantic Ocean', 'transport', 'London')
        self.setAssertCommand(turn, 'North Sea', 'transport', 'London')
        self.setAssertCommand(turn, 'Norwegian Sea', 'defend')
        self.setAssertCommand(turn, 'London', 'invade', ['Atlantic Ocean', 'North Sea', 'Germany'])
        self.setAssertCommand(turn, 'Denmark', 'support_attack', ['Germany', 'London'])
        self.setAssertCommand(turn, 'Germany', 'defend')
        # calculate turn
        turn = self.assertNextTurn(turn, '2008', 'Invasion Success: Supported invasion - escaping defender')
        # verify units
        self.assertResult(turn.previous, 'Atlantic Ocean', 'ok')
        self.assertUnit(turn, 'Atlantic Ocean', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Norwegian Sea', 'ok')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'London', 'ok')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Denmark', 'ok')
        self.assertUnit(turn, 'Denmark', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Germany', 'escaped')
        self.assertUnit(turn, 'France', 'Soldier', 'Ukraine')
        