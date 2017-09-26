from ui.tests.TestBase import TestBase
from ui.models import Turn

class TestInvasions(TestBase):
    
    def setUp(self):
        TestBase.setUp(self)
        self.importJson('test/test_invasions')

    def test_Engine(self):
        turn = Turn.objects.get(pk=1)
        
        # verify units
        self.assertUnit(turn, 'Atlantic Ocean', 'Ship', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Spain')
        self.assertUnit(turn, 'London', 'Soldier', 'Russia')
        self.assertUnit(turn, 'Denmark', 'Soldier', 'Russia')
        self.assertUnit(turn, 'Austria', 'Soldier', 'Ukraine')
        # set commands
        self.setAssertCommand(turn, 'Atlantic Ocean', 'transport', 'London') # ok - sea
        self.setAssertCommand(turn, 'North Sea', 'transport', 'London') # ok - beach
        self.setAssertCommand(turn, 'Norwegian Sea', 'defend')
        self.setAssertCommand(turn, 'London', 'invade', ['Atlantic Ocean', 'North Sea', 'Germany'])
        self.setAssertCommand(turn, 'Denmark', 'defend')
        self.setAssertCommand(turn, 'Austria', 'defend')
