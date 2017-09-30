from ui.tests.TestBase import TestBase
from ui.models import Turn

class TestEscapes(TestBase):
    
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
        self.setAssertCommand(turn, 'Atlantic Ocean', 'defend')
        self.setAssertCommand(turn, 'North Sea', 'attack', 'London')
        self.setAssertCommand(turn, 'Norwegian Sea', 'defend')
        self.setAssertCommand(turn, 'London', 'defend')
        self.setAssertCommand(turn, 'Denmark', 'move', 'Germany')
        self.setAssertCommand(turn, 'Austria', 'defend')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Escapes: No escape needed')
        # verify units
        self.assertResult(turn.previous, 'Atlantic Ocean', 'ok')
        self.assertUnit(turn, 'Atlantic Ocean', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'fail.defence-stronger')
        self.assertUnit(turn, 'London', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Norwegian Sea', 'ok')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'London', 'ok')
        self.assertUnit(turn, 'London', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Denmark', 'ok')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'ok')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Ukraine')
        
        # set commands
        self.setAssertCommand(turn, 'Atlantic Ocean', 'support_attack', ['London', 'North Sea'])
        self.setAssertCommand(turn, 'North Sea', 'attack', 'London')
        self.setAssertCommand(turn, 'Norwegian Sea', 'defend')
        self.setAssertCommand(turn, 'London', 'defend')
        self.setAssertCommand(turn, 'Germany', 'defend')
        self.setAssertCommand(turn, 'Austria', 'defend')
        # calculate turn
        turn = self.assertNextTurn(turn, '2001', 'Escapes: Simple escape')
        # verify units
        self.assertResult(turn.previous, 'Atlantic Ocean', 'ok')
        self.assertUnit(turn, 'Atlantic Ocean', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'London', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Norwegian Sea', 'ok')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'London', 'escaped')
        self.assertUnit(turn, 'France', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'ok')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Ukraine')