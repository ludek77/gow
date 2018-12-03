from ui.tests.TestBase import TestBase
from ui.models import Turn

class TestEscapes(TestBase):

    def test(self):
        turn = Turn.objects.get(pk=1)
        self.setDefaultEscapes(turn)
        # verify escapes
        self.assertEscapes(turn, 'Germany', ['France','Austria','Poland','Denmark'])
        self.assertEscapes(turn, 'France', ['Spain','London','Germany', 'Austria'])
        self.assertEscapes(turn, 'Austria', ['France','Germany','Poland','Croatia'])
        self.assertEscapes(turn, 'North Sea', ['London','Germany','Denmark','Sweden','Norwegian Sea','Norway'])
        self.assertEscapes(turn, 'Croatia', ['Ukraine','Poland','Austria'])
        self.assertEscapes(turn, 'Ukraine', ['Latvia','Moscow','Poland','Croatia'])
        self.assertEscapes(turn, 'Baltic Sea', ['Latvia','Sweden','Poland','Denmark','Germany'])
        self.assertEscapes(turn, 'Sweden', ['Denmark','Norway'])
        self.assertEscapes(turn, 'Norwegian Sea', ['North Sea','Norway','Atlantic Ocean'])
        
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
        turn = self.assertNextTurn(turn, '2000', 'Escapes: Escaped successfully')
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'escaped')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertNoUnit(turn, 'Croatia')
        self.assertUnit(turn, 'Poland', 'Army', 'Spain')
        self.assertResult(turn.previous, 'Croatia', 'ok')

    def testDestroyed(self):
        turn = Turn.objects.get(pk=1)
        self.setDefaultEscapes(turn)
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        self.assertUnit(turn, 'Baltic Sea', 'Ship', 'Russia')
        self.assertUnit(turn, 'Ukraine', 'Army', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'Croatia', 'attack', 'Austria')
        self.setAssertCommand(turn, 'Germany', 'support_attack', ['Austria','Croatia'])
        self.setAssertCommand(turn, 'Baltic Sea', 'attack', 'Poland')
        self.setAssertCommand(turn, 'Ukraine', 'attack', 'Poland')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Escapes: Unit destroyed')
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'destroyed')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertNoUnit(turn, 'Croatia')
        self.assertResult(turn.previous, 'Croatia', 'ok')
        self.assertNoUnit(turn, 'Poland')
        self.assertUnit(turn, 'Baltic Sea', 'Ship', 'Russia')
        self.assertResult(turn.previous, 'Baltic Sea', 'fail.not-strongest')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Ukraine', 'Army', 'Russia')
        self.assertResult(turn.previous, 'Ukraine', 'fail.not-strongest')
        
    def testCollidingEscapes(self):
        turn = Turn.objects.get(pk=1)
        self.setDefaultEscapes(turn)
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        self.assertUnit(turn, 'Baltic Sea', 'Ship', 'Russia')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        # set commands
        self.setAssertCommand(turn, 'Croatia', 'attack', 'Austria')
        self.setAssertCommand(turn, 'France', 'support_attack', ['Austria','Croatia'])
        self.setAssertCommand(turn, 'Baltic Sea', 'attack', 'Germany')
        self.setAssertCommand(turn, 'North Sea', 'support_attack', ['Germany','Baltic Sea'])
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Escapes: Colliding Escapes')
        # verify units
        self.assertResult(turn.previous, 'Croatia', 'ok')
        self.assertUnit(turn, 'Austria', 'Army', 'Russia')
        self.assertResult(turn.previous, 'Austria', 'destroyed')
        self.assertResult(turn.previous, 'Baltic Sea', 'ok')
        self.assertUnit(turn, 'Germany', 'Ship', 'Russia')
        self.assertResult(turn.previous, 'Germany', 'escaped')
        self.assertUnit(turn, 'Denmark', 'Army', 'Spain')
        self.assertNoUnit(turn, 'Croatia')
        self.assertNoUnit(turn, 'Baltic Sea')
        self.assertNoUnit(turn, 'Poland')

    def testSettingEscapes(self):
        turn = Turn.objects.get(pk=1)
        self.setDefaultEscapes(turn)
        # verify default escapes
        self.assertEscapes(turn,'Austria',['France','Germany','Poland','Croatia'])
        # verify setting escapes
        self.setAssertEscape(turn, 'Austria', 'Germany', ['Germany','France','Poland','Croatia'])
        self.setAssertEscape(turn, 'Austria', 'France', ['France','Germany','Poland','Croatia'])
        self.setAssertEscape(turn, 'Austria', 'Poland', ['Poland','France','Germany','Croatia'])
        self.setAssertEscape(turn, 'Austria', 'Croatia', ['Croatia','France','Germany','Poland'])
        self.setAssertEscape(turn, 'Austria', 'Spain', ['France','Germany','Poland','Croatia'],'fail.not-reachable-for-escape')
        self.setAssertEscape(turn, 'Austria', 'Austria', ['France','Germany','Poland','Croatia'],'fail.not-reachable-for-escape')
