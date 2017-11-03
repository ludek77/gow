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
        self.assertNoUnit(turn, 'SpainBuff')
        self.assertNoUnit(turn, 'UkraineBuff')
        
        # set commands
        self.setAssertCommand(turn, 'Atlantic Ocean', 'attack', 'Azores')
        self.setAssertCommand(turn, 'North Sea', 'attack', 'London')
        self.setAssertCommand(turn, 'Norwegian Sea', 'attack', 'North Sea')
        self.setAssertCommand(turn, 'London', 'attack', 'France')
        self.setAssertCommand(turn, 'Denmark', 'attack', 'Germany')
        self.setAssertCommand(turn, 'Austria', 'attack', 'France')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Attacks: Single attack, Two attacks to one field, Failed train')
        # verify units
        self.assertResult(turn.previous, 'Atlantic Ocean', 'ok')
        self.assertUnit(turn, 'Azores', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'fail.defence-stronger')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Norwegian Sea', 'fail.defence-stronger')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'London', 'fail.not-strongest')
        self.assertUnit(turn, 'London', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Denmark', 'ok')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'fail.not-strongest')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Ukraine')
        
        # set commands
        self.setAssertCommand(turn, 'Azores', 'attack', 'Atlantic Ocean')
        self.setAssertCommand(turn, 'North Sea', 'attack', 'Norwegian Sea')
        self.setAssertCommand(turn, 'Norwegian Sea', 'attack', 'North Sea')
        self.setAssertCommand(turn, 'London', 'attack', 'France')
        self.setAssertCommand(turn, 'Germany', 'attack', 'Poland')
        self.setAssertCommand(turn, 'Austria', 'attack', 'Poland')
        # calculate turn
        turn = self.assertNextTurn(turn, '2001', 'Attacks: Two-way-attacks, Two attacks to one field')
        # verify units
        self.assertResult(turn.previous, 'Azores', 'ok')
        self.assertUnit(turn, 'Atlantic Ocean', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'fail.not-stronger-than-opposite')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Norwegian Sea', 'fail.not-stronger-than-opposite')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'London', 'ok')
        self.assertUnit(turn, 'France', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Germany', 'fail.not-strongest')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'fail.not-strongest')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Ukraine')
        
        # set commands
        self.setAssertCommand(turn, 'Atlantic Ocean', 'attack', 'North Sea')
        self.setAssertCommand(turn, 'North Sea', 'attack', 'Norwegian Sea')
        self.setAssertCommand(turn, 'Norwegian Sea', 'attack', 'Atlantic Ocean')
        self.setAssertCommand(turn, 'France', 'attack', 'Germany')
        self.setAssertCommand(turn, 'Germany', 'attack', 'Austria')
        self.setAssertCommand(turn, 'Austria', 'attack', 'France')
        # calculate turn
        turn = self.assertNextTurn(turn, '2002', 'Attacks: Successful trains of three')
        # verify units
        self.assertResult(turn.previous, 'Atlantic Ocean', 'ok')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Norwegian Sea', 'ok')
        self.assertUnit(turn, 'Atlantic Ocean', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'France', 'ok')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'ok')
        self.assertUnit(turn, 'France', 'Soldier', 'Ukraine')
        
        # set commands
        self.setAssertCommand(turn, 'Atlantic Ocean', 'attack', 'North Sea')
        self.setAssertCommand(turn, 'North Sea', 'attack', 'Germany')
        self.setAssertCommand(turn, 'Norwegian Sea', 'attack', 'North Sea')
        self.setAssertCommand(turn, 'France', 'attack', 'Germany')
        self.setAssertCommand(turn, 'Germany', 'attack', 'Austria')
        self.setAssertCommand(turn, 'Austria', 'attack', 'France')
        # calculate turn
        turn = self.assertNextTurn(turn, '2003', 'Attacks: Train of three blocked by attack')
        # verify units
        self.assertResult(turn.previous, 'Atlantic Ocean', 'fail.not-strongest')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'fail.not-strongest')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'Norwegian Sea', 'fail.not-strongest')
        self.assertUnit(turn, 'Atlantic Ocean', 'Ship', 'Ukraine')
        self.assertResult(turn.previous, 'France', 'fail.not-strongest')
        self.assertUnit(turn, 'Germany', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Germany', 'fail.defence-stronger')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'fail.defence-stronger')
        self.assertUnit(turn, 'France', 'Soldier', 'Ukraine')