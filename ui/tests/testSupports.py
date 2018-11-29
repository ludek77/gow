from ui.tests.TestBase import TestBase
from ui.models import Turn

class TestSupports(TestBase):

    def testSupportAttack(self):
        turn = Turn.objects.get(pk=1)
        self.setDefaultEscapes(turn)
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'Croatia', 'attack', 'Austria')
        self.setAssertCommand(turn, 'Germany', 'support_attack', ['Austria','Croatia'])
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Supports: Successful attack, escaped')
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'escaped')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertNoUnit(turn, 'Croatia')
        self.assertUnit(turn, 'Poland', 'Army', 'Spain')
        self.assertResult(turn.previous, 'Croatia', 'ok')
 
    def testSupportNoAttack(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'Croatia', 'move', 'Austria')
        self.setAssertCommand(turn, 'Germany', 'support_attack', ['Austria','Croatia'])
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Supports: Not attacking unit')
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertResult(turn.previous, 'Austria', 'ok')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertResult(turn.previous, 'Germany', 'fail.unit-not-attacking')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        self.assertResult(turn.previous, 'Croatia', 'fail.target-not-moving:par_0')
         
    def testSupportSelfAttack(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'Croatia', 'attack', 'Austria')
        self.setAssertCommand(turn, 'Austria', 'support_attack', ['Croatia','Austria'])
        self.setAssertCommand(turn, 'Germany', 'attack', 'Austria')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Supports: Support attack to self')
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertResult(turn.previous, 'Austria', 'fail.canceled-by-attack')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertResult(turn.previous, 'Germany', 'fail.not-strongest')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        self.assertResult(turn.previous, 'Croatia', 'fail.not-strongest')
 
    def testSupportElsewhereAttack(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'Croatia', 'attack', 'Poland')
        self.setAssertCommand(turn, 'Germany', 'support_attack', ['Austria','Croatia'])
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Supports: Unit attacking something else')
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertResult(turn.previous, 'Austria', 'ok')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertResult(turn.previous, 'Germany', 'fail.unit-attacking-elsewhere')
        self.assertNoUnit(turn, 'Croatia')
        self.assertUnit(turn, 'Poland', 'Army', 'Russia')
        self.assertResult(turn.previous, 'Croatia', 'ok')
 
    def testSupportDefence(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'France', 'support_defence', 'Austria')
        self.setAssertCommand(turn, 'Croatia', 'attack', 'Austria')
        self.setAssertCommand(turn, 'Germany', 'support_attack', ['Austria','Croatia'])
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Supports: Successful defence')
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertResult(turn.previous, 'Austria', 'ok')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
        self.assertResult(turn.previous, 'France', 'ok')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        self.assertResult(turn.previous, 'Croatia', 'fail.defence-stronger')
 
    def testSupportDefenceCancelled(self):
        turn = Turn.objects.get(pk=1)
        self.setDefaultEscapes(turn)
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Denmark', 'Ship', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'Germany', 'support_defence', 'Austria')
        self.setAssertCommand(turn, 'Denmark', 'attack', 'Germany')
        self.setAssertCommand(turn, 'Croatia', 'attack', 'Austria')
        self.setAssertCommand(turn, 'France', 'support_attack', ['Austria','Croatia'])
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Supports: Canceled defence support')
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'escaped')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
        self.assertResult(turn.previous, 'France', 'ok')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertResult(turn.previous, 'Germany', 'fail.canceled-by-attack')
        self.assertNoUnit(turn, 'Croatia')
        self.assertUnit(turn, 'Poland', 'Army', 'Spain')
        self.assertResult(turn.previous, 'Croatia', 'ok')
 
    def testDontCancelAttackToSelf(self):
        turn = Turn.objects.get(pk=1)
        self.setDefaultEscapes(turn)
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'Austria', 'attack', 'Germany')
        self.setAssertCommand(turn, 'Croatia', 'attack', 'Austria')
        self.setAssertCommand(turn, 'Germany', 'support_attack', ['Austria','Croatia'])
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Supports: Dont cancel attack to self')
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertUnit(turn, 'Austria', 'Army', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'fail.defence-stronger,escaped')
        self.assertUnit(turn, 'Poland', 'Army', 'Spain')
        self.assertNoUnit(turn, 'Croatia')
        self.assertResult(turn.previous, 'Croatia', 'ok')

    def testStrongerAttack(self):
        turn = Turn.objects.get(pk=1)
        self.setDefaultEscapes(turn)
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Denmark', 'Ship', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        self.assertUnit(turn, 'Ukraine', 'Army', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'Austria', 'attack', 'Poland')
        self.setAssertCommand(turn, 'Denmark', 'support_attack', ['Poland','Austria'])
        self.setAssertCommand(turn, 'Germany', 'support_attack', ['Poland','Austria'])
        self.setAssertCommand(turn, 'Croatia', 'attack', 'Poland')
        self.setAssertCommand(turn, 'Ukraine', 'support_attack', ['Poland','Croatia'])
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Supports: Attack supported more')
        # verify units
        self.assertNoUnit(turn, 'Austria')
        self.assertUnit(turn, 'Poland', 'Army', 'Spain')
        self.assertResult(turn.previous, 'Austria', 'ok')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertUnit(turn, 'Poland', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        self.assertResult(turn.previous, 'Croatia', 'fail.not-strongest')


