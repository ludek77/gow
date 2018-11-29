from ui.tests.TestBase import TestBase
from ui.models import Turn

class TestAttacks(TestBase):
    
    def testSingleAttack(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertNoUnit(turn, 'Poland')
        # set commands
        self.setAssertCommand(turn, 'Germany', 'attack', 'Poland')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Attacks: Single attack')
        # verify units
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertNoUnit(turn, 'Germany')
        self.assertUnit(turn, 'Poland', 'Army', 'Spain')

    def testFailedAttack(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
        # set commands
        self.setAssertCommand(turn, 'Germany', 'attack', 'France')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Attacks: Failed attack')
        # verify units
        self.assertResult(turn.previous, 'Germany', 'fail.defence-stronger')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')

    def testTwoAttacks(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Latvia', 'Army', 'Russia')
        self.assertNoUnit(turn, 'Poland')
        # set commands
        self.setAssertCommand(turn, 'Germany', 'attack', 'Poland')
        self.setAssertCommand(turn, 'Latvia', 'attack', 'Poland')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Attacks: Two Attacks')
        # verify units
        self.assertResult(turn.previous, 'Germany', 'fail.not-strongest')
        self.assertResult(turn.previous, 'Latvia', 'fail.not-strongest')
        self.assertNoUnit(turn, 'Poland')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Latvia', 'Army', 'Russia')

    def testTwoWayAttack(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
        # set commands
        self.setAssertCommand(turn, 'Germany', 'attack', 'France')
        self.setAssertCommand(turn, 'France', 'attack', 'Germany')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Attacks: Two Way Attack')
        # verify units
        self.assertResult(turn.previous, 'Germany', 'fail.not-stronger-than-opposite')
        self.assertResult(turn.previous, 'France', 'fail.not-stronger-than-opposite')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
        
    def testFailedTrain(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
        self.assertUnit(turn, 'Denmark', 'Ship', 'Spain')
        # set commands
        self.setAssertCommand(turn, 'France', 'attack', 'Austria')
        self.setAssertCommand(turn, 'Austria', 'attack', 'Germany')
        self.setAssertCommand(turn, 'Germany', 'attack', 'Denmark')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Attacks: Failed Train')
        # verify units
        self.assertResult(turn.previous, 'France', 'fail.defence-stronger')
        self.assertResult(turn.previous, 'Austria', 'fail.defence-stronger')
        self.assertResult(turn.previous, 'Germany', 'fail.defence-stronger')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')

    def testSuccessfulTrain(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
        self.assertNoUnit(turn, 'Poland')
        # set commands
        self.setAssertCommand(turn, 'France', 'attack', 'Austria')
        self.setAssertCommand(turn, 'Austria', 'attack', 'Germany')
        self.setAssertCommand(turn, 'Germany', 'attack', 'Poland')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Attacks: Successful Train')
        # verify units
        self.assertResult(turn.previous, 'France', 'ok')
        self.assertResult(turn.previous, 'Austria', 'ok')
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertNoUnit(turn, 'France')
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Poland', 'Army', 'Spain')

    def testBlockedTrain(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
        self.assertUnit(turn, 'Ukraine', 'Army', 'Russia')
        self.assertNoUnit(turn, 'Poland')
        # set commands
        self.setAssertCommand(turn, 'France', 'attack', 'Austria')
        self.setAssertCommand(turn, 'Austria', 'attack', 'Germany')
        self.setAssertCommand(turn, 'Germany', 'attack', 'Poland')
        self.setAssertCommand(turn, 'Ukraine', 'attack', 'Poland')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Attacks: Blocked Train')
        # verify units
        self.assertResult(turn.previous, 'France', 'fail.defence-stronger')
        self.assertResult(turn.previous, 'Austria', 'fail.defence-stronger')
        self.assertResult(turn.previous, 'Germany', 'fail.not-strongest')
        self.assertResult(turn.previous, 'Ukraine', 'fail.not-strongest')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Ukraine', 'Army', 'Russia')
