from ui.tests.TestBase import TestBase
from ui.models import Turn

class TestInvasions(TestBase):
    
    def testInvasion(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertNoUnit(turn, 'Norway')
        # set commands
        self.setAssertCommand(turn, 'Germany', 'invade', ['North Sea',None,'Norway'])
        self.setAssertCommand(turn, 'North Sea', 'transport', 'Germany')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Invasions: Single invasion')
        # verify units
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertNoUnit(turn, 'Germany')
        self.assertUnit(turn, 'Norway', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')

    def testInvasion2(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Russia')
        self.assertNoUnit(turn, 'Norway')
        # set commands
        self.setAssertCommand(turn, 'Germany', 'invade', ['North Sea','Norwegian Sea','Norway'])
        self.setAssertCommand(turn, 'North Sea', 'transport', 'Germany')
        self.setAssertCommand(turn, 'Norwegian Sea', 'transport', 'Germany')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Invasions: Double invasion')
        # verify units
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertNoUnit(turn, 'Germany')
        self.assertUnit(turn, 'Norway', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Russia')
        self.assertResult(turn.previous, 'Norwegian Sea', 'ok')

    def testSelfInvasion(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        # set commands
        self.setAssertCommand(turn, 'Germany', 'invade', ['North Sea',None,'Germany'])
        self.setAssertCommand(turn, 'North Sea', 'transport', 'Germany')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Invasions: Self invasion')
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        
    def testNotStrongestSelfInvasion(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertUnit(turn, 'Baltic Sea', 'Ship', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'Germany', 'invade', ['North Sea',None,'Germany'])
        self.setAssertCommand(turn, 'North Sea', 'transport', 'Germany')
        self.setAssertCommand(turn, 'Baltic Sea', 'attack', 'Germany')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Invasions: Not Strongest Self invasion')
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertResult(turn.previous, 'Germany', 'fail.not-strongest')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'Baltic Sea', 'Ship', 'Russia')
        self.assertResult(turn.previous, 'Baltic Sea', 'fail.not-strongest')
    
    def testInvasionFromAttack(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertNoUnit(turn, 'Norway')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
        # set commands
        self.setAssertCommand(turn, 'Germany', 'invade', ['North Sea',None,'Norway'])
        self.setAssertCommand(turn, 'North Sea', 'transport', 'Germany')
        self.setAssertCommand(turn, 'France', 'attack', 'Germany')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Invasions: Invasion from attack')
        # verify units
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertResult(turn.previous, 'France', 'ok')
        self.assertNoUnit(turn, 'France')
        self.assertUnit(turn, 'Norway', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
    
    def testNoTransport(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Russia')
        self.assertNoUnit(turn, 'Norway')
        # set commands
        self.setAssertCommand(turn, 'Germany', 'invade', ['North Sea','Norwegian Sea','Norway'])
        self.setAssertCommand(turn, 'North Sea', 'defend')
        self.setAssertCommand(turn, 'Norwegian Sea', 'transport', 'Germany')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Invasions: No Transport')
        # verify units
        self.assertResult(turn.previous, 'Germany', 'fail.transport-missing')
        self.assertNoUnit(turn, 'Norway')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Russia')
        self.assertResult(turn.previous, 'Norwegian Sea', 'ok')
        
    def testNoTransport2(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Russia')
        self.assertNoUnit(turn, 'Norway')
        # set commands
        self.setAssertCommand(turn, 'Germany', 'invade', ['North Sea','Norwegian Sea','Norway'])
        self.setAssertCommand(turn, 'North Sea', 'transport', 'Germany')
        self.setAssertCommand(turn, 'Norwegian Sea', 'defend')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Invasions: No second Transport')
        # verify units
        self.assertResult(turn.previous, 'Germany', 'fail.transport-missing')
        self.assertNoUnit(turn, 'Norway')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Russia')
        self.assertResult(turn.previous, 'Norwegian Sea', 'ok')
        
    def testAttackedTransport(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Russia')
        self.assertNoUnit(turn, 'Norway')
        # set commands
        self.setAssertCommand(turn, 'Germany', 'invade', ['North Sea',None,'Norway'])
        self.setAssertCommand(turn, 'North Sea', 'transport', 'Germany')
        self.setAssertCommand(turn, 'Norwegian Sea', 'attack', 'North Sea')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Invasions: No second Transport')
        # verify units
        self.assertResult(turn.previous, 'Germany', 'fail.transport-canceled')
        self.assertNoUnit(turn, 'Norway')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'fail.canceled-by-attack')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Russia')
        self.assertResult(turn.previous, 'Norwegian Sea', 'fail.defence-stronger')

    def testAttackedTransport(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertUnit(turn, 'Sweden', 'Army', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'Germany', 'invade', ['North Sea',None,'Norway'])
        self.setAssertCommand(turn, 'Sweden', 'invade', ['North Sea',None,'Norway'])
        self.setAssertCommand(turn, 'North Sea', 'transport', 'Germany')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Invasions: No second Transport')
        # verify units
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertNoUnit(turn, 'Germany')
        self.assertUnit(turn, 'Norway', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'Sweden', 'Army', 'Russia')
        self.assertResult(turn.previous, 'Sweden', 'fail.transport-missing')
        
    def testMoveNotCancelingTransport(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Russia')
        self.assertNoUnit(turn, 'Norway')
        # set commands
        self.setAssertCommand(turn, 'Germany', 'invade', ['North Sea',None,'Norway'])
        self.setAssertCommand(turn, 'North Sea', 'transport', 'Germany')
        self.setAssertCommand(turn, 'Norwegian Sea', 'move', 'North Sea')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Invasions: Move not canceling Transport')
        # verify units
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertNoUnit(turn, 'Germany')
        self.assertUnit(turn, 'Norway', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Russia')
        self.assertResult(turn.previous, 'Norwegian Sea', 'fail.target-not-moving:par_0')
    
    def testNotStrongestInvasion(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Russia')
        self.assertNoUnit(turn, 'Norway')
        # set commands
        self.setAssertCommand(turn, 'Germany', 'invade', ['North Sea',None,'Norway'])
        self.setAssertCommand(turn, 'North Sea', 'transport', 'Germany')
        self.setAssertCommand(turn, 'Norwegian Sea', 'attack', 'Norway')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Invasions: Not strongest Invasion')
        # verify units
        self.assertResult(turn.previous, 'Germany', 'fail.not-strongest')
        self.assertNoUnit(turn, 'Norway')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Russia')
        self.assertResult(turn.previous, 'Norwegian Sea', 'fail.not-strongest')
        
    def testSupportedInvasion(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Russia')
        self.assertUnit(turn, 'Sweden', 'Army', 'Russia')
        self.assertNoUnit(turn, 'Norway')
        # set commands
        self.setAssertCommand(turn, 'Germany', 'invade', ['North Sea',None,'Norway'])
        self.setAssertCommand(turn, 'North Sea', 'transport', 'Germany')
        self.setAssertCommand(turn, 'Norwegian Sea', 'attack', 'Norway')
        self.setAssertCommand(turn, 'Sweden', 'support_attack', ['Norway','Germany'])
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Invasions: Supported invasion')
        # verify units
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertNoUnit(turn, 'Germany')
        self.assertUnit(turn, 'Norway', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'Norwegian Sea', 'Ship', 'Russia')
        self.assertResult(turn.previous, 'Norwegian Sea', 'fail.not-strongest')
        self.assertUnit(turn, 'Sweden', 'Army', 'Russia')
        self.assertResult(turn.previous, 'Sweden', 'ok')     

    def testDefenceStronger(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertUnit(turn, 'Sweden', 'Army', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'Germany', 'invade', ['North Sea',None,'Sweden'])
        self.setAssertCommand(turn, 'North Sea', 'transport', 'Germany')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Invasions: Defence Stronger')
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertResult(turn.previous, 'Germany', 'fail.defence-stronger')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertUnit(turn, 'Sweden', 'Army', 'Russia')
        self.assertResult(turn.previous, 'Sweden', 'ok')

    def testSupportedInvasionRetreat(self):
        turn = Turn.objects.get(pk=1)
        self.setDefaultEscapes(turn)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertUnit(turn, 'Sweden', 'Army', 'Russia')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
        # set commands
        self.setAssertCommand(turn, 'Germany', 'defend')
        self.setAssertCommand(turn, 'North Sea', 'transport', 'Sweden')
        self.setAssertCommand(turn, 'Sweden', 'invade', ['North Sea',None,'Germany'])
        self.setAssertCommand(turn, 'France', 'support_attack', ['Germany','Sweden'])
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Invasions: Supported invasion, retreating defender')
        # verify units
        self.assertResult(turn.previous, 'Germany', 'escaped')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertResult(turn.previous, 'Sweden', 'ok')
        self.assertResult(turn.previous, 'France', 'ok')
        self.assertNoUnit(turn, 'Sweden')
        self.assertUnit(turn, 'Germany', 'Army', 'Russia')
        self.assertUnit(turn, 'Denmark', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertUnit(turn, 'France', 'Army', 'Spain')

    def testInvasionSwitch(self):
        turn = Turn.objects.get(pk=1)
        self.setDefaultEscapes(turn)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertUnit(turn, 'Sweden', 'Army', 'Russia')
        self.assertUnit(turn, 'Baltic Sea', 'Ship', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'Germany', 'invade', ['Baltic Sea',None,'Sweden'])
        self.setAssertCommand(turn, 'Baltic Sea', 'transport', 'Germany')
        self.setAssertCommand(turn, 'Sweden', 'invade', ['North Sea',None,'Germany'])
        self.setAssertCommand(turn, 'North Sea', 'transport', 'Sweden')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Invasions: Invasion switch')
        # verify units
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertResult(turn.previous, 'Sweden', 'ok')
        self.assertResult(turn.previous, 'Baltic Sea', 'ok')
        self.assertUnit(turn, 'Germany', 'Army', 'Russia')
        self.assertUnit(turn, 'Sweden', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertUnit(turn, 'Baltic Sea', 'Ship', 'Russia')

    def testTwoInvasionsToOne(self):
        turn = Turn.objects.get(pk=1)
        self.setDefaultEscapes(turn)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertUnit(turn, 'Sweden', 'Army', 'Russia')
        self.assertUnit(turn, 'Baltic Sea', 'Ship', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'Germany', 'invade', ['Baltic Sea',None,'Denmark'])
        self.setAssertCommand(turn, 'Baltic Sea', 'transport', 'Germany')
        self.setAssertCommand(turn, 'Sweden', 'invade', ['North Sea',None,'Denmark'])
        self.setAssertCommand(turn, 'North Sea', 'transport', 'Sweden')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Invasions: Two Invasions to one')
        # verify units
        self.assertResult(turn.previous, 'Germany', 'fail.not-strongest')
        self.assertResult(turn.previous, 'North Sea', 'ok')
        self.assertResult(turn.previous, 'Sweden', 'fail.not-strongest')
        self.assertResult(turn.previous, 'Baltic Sea', 'ok')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Sweden', 'Army', 'Russia')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        self.assertUnit(turn, 'Baltic Sea', 'Ship', 'Russia')

