from ui.tests.TestBase import TestBase
from ui.models import Turn

class TestSupports(TestBase):
    
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
        self.setAssertCommand(turn, 'Atlantic Ocean', 'support_defence', 'Azores', 'invalid.missing_unit:par_0')
        self.setAssertCommand(turn, 'North Sea', 'support_defence', 'Atlantic Ocean')
        self.setAssertCommand(turn, 'Norwegian Sea', 'support_defence', 'Austria', 'invalid.not_next:par_0')
        self.setAssertCommand(turn, 'London', 'support_defence', 'North Sea', 'invalid.not_reachable:par_0')
        self.setAssertCommand(turn, 'Denmark', 'move', 'Germany')
        self.setAssertCommand(turn, 'Austria', 'move', 'France')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Supports: Various simple fails')
        # verify units
        self.assertResult(turn.previous, 'Atlantic Ocean', 'invalid.missing_unit:par_0')
        self.assertUnit(turn, 'Atlantic Ocean', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Norwegian Sea', 'invalid.not_next:par_0')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'London', 'invalid.not_reachable:par_0')
        self.assertUnit(turn, 'London', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Denmark', 'ok')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'ok')
        self.assertUnit(turn, 'France', 'Soldier', 'Ukraine')
        
        # set commands
        self.setAssertCommand(turn, 'Atlantic Ocean', 'attack', 'London')
        self.setAssertCommand(turn, 'North Sea', 'move', 'Denmark')
        self.setAssertCommand(turn, 'Norwegian Sea', 'move', 'North Sea')
        self.setAssertCommand(turn, 'London', 'attack', 'France')
        self.setAssertCommand(turn, 'Germany', 'support_attack', ['France', 'London'])
        self.setAssertCommand(turn, 'France', 'move', 'London')
        # calculate turn
        turn = self.assertNextTurn(turn, '2001', 'Supports: Supported Attack')
        # verify units
        self.assertResult(turn.previous, 'Atlantic Ocean', 'ok')
        self.assertUnit(turn, 'London', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'Denmark', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Norwegian Sea', 'ok')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'London', 'ok')
        self.assertUnit(turn, 'France', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'France', 'fail.canceled-by-attack,escaped')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Ukraine')
        
        # set commands
        self.setAssertCommand(turn, 'London', 'support_attack', ['France','Austria'])
        self.setAssertCommand(turn, 'Denmark', 'support_attack', ['Germany','France'])
        self.setAssertCommand(turn, 'North Sea', 'defend')
        self.setAssertCommand(turn, 'France', 'defend')
        self.setAssertCommand(turn, 'Germany', 'defend')
        self.setAssertCommand(turn, 'Austria', 'attack', 'Germany')
        # calculate turn
        turn = self.assertNextTurn(turn, '2002', 'Supports: Supporting not attacking units')
        # verify units
        self.assertResult(turn.previous, 'London', 'fail.unit-attacking-elsewhere')
        self.assertUnit(turn, 'London', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Denmark', 'fail.unit-not-attacking')
        self.assertUnit(turn, 'Denmark', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'France', 'ok')
        self.assertUnit(turn, 'France', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'fail.defence-stronger')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Ukraine')
        
        # set commands
        self.setAssertCommand(turn, 'London', 'move', 'France')
        self.setAssertCommand(turn, 'Denmark', 'defend')
        self.setAssertCommand(turn, 'North Sea', 'transport', 'Germany')
        self.setAssertCommand(turn, 'France', 'move', 'Spain')
        self.setAssertCommand(turn, 'Germany', 'invade', ['North Sea',None,'London'])
        self.setAssertCommand(turn, 'Austria', 'defend')
        # calculate turn
        turn = self.assertNextTurn(turn, '2003', 'Supports: Support invasion')
        # verify units
        self.assertResult(turn.previous, 'London', 'fail.canceled-by-invasion')
        self.assertUnit(turn, 'London', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Denmark', 'ok')
        self.assertUnit(turn, 'Denmark', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'France', 'ok')
        self.assertUnit(turn, 'Spain', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Germany', 'fail.defence-stronger')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'ok')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Ukraine')
        
        # set commands
        self.setAssertCommand(turn, 'London', 'defend')
        self.setAssertCommand(turn, 'Denmark', 'attack', 'Germany')
        self.setAssertCommand(turn, 'North Sea', 'support_attack', ['Germany','Denmark'])
        self.setAssertCommand(turn, 'Spain', 'move', 'France')
        self.setAssertCommand(turn, 'Germany', 'attack', 'Austria')
        self.setAssertCommand(turn, 'Austria', 'attack', 'Germany')
        # calculate turn
        turn = self.assertNextTurn(turn, '2004', 'Supports: Attack not canceling support on self')
        # verify units
        self.assertResult(turn.previous, 'London', 'ok')
        self.assertUnit(turn, 'London', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Denmark', 'ok')
        self.assertUnit(turn, 'Germany', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'Spain', 'ok')
        self.assertUnit(turn, 'France', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Germany', 'fail.not-stronger-than-opposite,escaped')
        self.assertUnit(turn, 'Poland', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'fail.not-stronger-than-opposite')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Ukraine')
        
        # set commands
        self.setAssertCommand(turn, 'London', 'attack', 'France')
        self.setAssertCommand(turn, 'Germany', 'attack', 'Poland')
        self.setAssertCommand(turn, 'North Sea', 'defend')
        self.setAssertCommand(turn, 'France', 'support_defence', 'Germany')
        self.setAssertCommand(turn, 'Poland', 'attack', 'Germany')
        self.setAssertCommand(turn, 'Austria', 'support_attack', ['Germany','Poland'])
        # calculate turn
        turn = self.assertNextTurn(turn, '2005', 'Supports: Support canceled by attack')
        # verify units
        self.assertResult(turn.previous, 'London', 'fail.defence-stronger')
        self.assertUnit(turn, 'London', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Germany', 'fail.not-stronger-than-opposite,escaped')
        self.assertUnit(turn, 'Denmark', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'France', 'fail.canceled-by-attack')
        self.assertUnit(turn, 'France', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Poland', 'ok')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'ok')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Ukraine')
        
        # set commands
        self.setAssertCommand(turn, 'London', 'defend')
        self.setAssertCommand(turn, 'Denmark', 'support_defence', 'Germany')
        self.setAssertCommand(turn, 'North Sea', 'defend')
        self.setAssertCommand(turn, 'France', 'support_attack', ['Germany','Austria'])
        self.setAssertCommand(turn, 'Germany', 'defend')
        self.setAssertCommand(turn, 'Austria', 'attack', 'Germany')
        # calculate turn
        turn = self.assertNextTurn(turn, '2006', 'Supports: Supported attack fails on supported defence')
        # verify units
        self.assertResult(turn.previous, 'London', 'ok')
        self.assertUnit(turn, 'London', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Denmark', 'ok')
        self.assertUnit(turn, 'Denmark', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'France', 'ok')
        self.assertUnit(turn, 'France', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'fail.defence-stronger')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Ukraine')
        
        # set commands
        self.setAssertCommand(turn, 'London', 'defend')
        self.setAssertCommand(turn, 'Denmark', 'support_defence', 'Germany')
        self.setAssertCommand(turn, 'North Sea', 'attack', 'Denmark')
        self.setAssertCommand(turn, 'France', 'support_attack', ['Germany','Austria'])
        self.setAssertCommand(turn, 'Germany', 'defend')
        self.setAssertCommand(turn, 'Austria', 'attack', 'Germany')
        # calculate turn
        turn = self.assertNextTurn(turn, '2007', 'Supports: Support defence canceled, attack successful')
        # verify units
        self.assertResult(turn.previous, 'London', 'ok')
        self.assertUnit(turn, 'London', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Denmark', 'fail.canceled-by-attack')
        self.assertUnit(turn, 'Denmark', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'fail.defence-stronger')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'France', 'ok')
        self.assertUnit(turn, 'France', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Germany', 'escaped')
        self.assertUnit(turn, 'Poland', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'ok')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Ukraine')
        
        # set commands
        self.setAssertCommand(turn, 'London', 'defend')
        self.setAssertCommand(turn, 'Denmark', 'support_attack', ['Germany','Poland'])
        self.setAssertCommand(turn, 'North Sea', 'support_defence', 'Germany')
        self.setAssertCommand(turn, 'France', 'support_attack', ['Germany','Poland'])
        self.setAssertCommand(turn, 'Poland', 'attack', 'Germany')
        self.setAssertCommand(turn, 'Germany', 'attack', 'Denmark')
        # calculate turn
        turn = self.assertNextTurn(turn, '2008', 'Supports: Attack supported more than defence')
        # verify units
        self.assertResult(turn.previous, 'London', 'ok')
        self.assertUnit(turn, 'London', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Denmark', 'ok')
        self.assertUnit(turn, 'Denmark', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'France', 'ok')
        self.assertUnit(turn, 'France', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Poland', 'ok')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Germany', 'fail.defence-stronger,escaped')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Ukraine')
        