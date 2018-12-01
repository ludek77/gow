from ui.tests.TestBase import TestBase
from ui.models import Turn

class TestMoves(TestBase):
     
    def testSingleMove(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertNoUnit(turn, 'Poland')
        # set commands
        self.setAssertCommand(turn, 'Germany', 'move', 'Poland')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Moves: Single move')
        # verify units
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertNoUnit(turn, 'Germany')
        self.assertUnit(turn, 'Poland', 'Army', 'Spain')

    def testSingleSecondMove(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertNoUnit(turn, 'Poland')
        # set commands
        self.setAssertCommand(turn, 'Germany', 'move', ['Germany', 'Poland'])
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Moves: Single Second move')
        # verify units
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertNoUnit(turn, 'Germany')
        self.assertUnit(turn, 'Poland', 'Army', 'Spain')

    def testFailedSecondMove(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        self.assertNoUnit(turn, 'Poland')
        # set commands
        self.setAssertCommand(turn, 'Germany', 'move', 'Poland')
        self.setAssertCommand(turn, 'Croatia', 'move', ['Croatia', 'Poland'])
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Moves: Failed Second move')
        # verify units
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertResult(turn.previous, 'Croatia', 'fail.target-not-moving:par_1')
        self.assertNoUnit(turn, 'Germany')
        self.assertUnit(turn, 'Poland', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')

    def testFailedMove(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
        # set commands
        self.setAssertCommand(turn, 'Germany', 'move', 'France')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Moves: Failed move')
        # verify units
        self.assertResult(turn.previous, 'Germany', 'fail.target-not-moving:par_0')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
 
    def testTwoMoves(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Baltic Sea', 'Ship', 'Russia')
        self.assertNoUnit(turn, 'Poland')
        # set commands
        self.setAssertCommand(turn, 'Germany', 'move', 'Poland')
        self.setAssertCommand(turn, 'Baltic Sea', 'move', 'Poland')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Moves: Two Moves')
        # verify units
        self.assertResult(turn.previous, 'Germany', 'fail.more-moves-to-target:par_0')
        self.assertResult(turn.previous, 'Baltic Sea', 'fail.more-moves-to-target:par_0')
        self.assertNoUnit(turn, 'Poland')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Baltic Sea', 'Ship', 'Russia')
  
    def testSwitch(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'Austria', 'move', 'Croatia')
        self.setAssertCommand(turn, 'Croatia', 'move', 'Austria')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Moves: Switch')
        # verify units
        self.assertResult(turn.previous, 'Austria', 'ok')
        self.assertResult(turn.previous, 'Croatia', 'ok')
        self.assertUnit(turn, 'Austria', 'Army', 'Russia')
        self.assertUnit(turn, 'Croatia', 'Army', 'Spain')

    def testSecondSwitch(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'Austria', 'move', ['Austria', 'Croatia'])
        self.setAssertCommand(turn, 'Croatia', 'move', ['Croatia', 'Austria'])
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Moves: Second Switch')
        # verify units
        self.assertResult(turn.previous, 'Austria', 'ok')
        self.assertResult(turn.previous, 'Croatia', 'ok')
        self.assertUnit(turn, 'Austria', 'Army', 'Russia')
        self.assertUnit(turn, 'Croatia', 'Army', 'Spain')

    def testBlockedSwitch(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
        # set commands
        self.setAssertCommand(turn, 'Austria', 'move', 'Croatia')
        self.setAssertCommand(turn, 'Croatia', 'move', 'Austria')
        self.setAssertCommand(turn, 'France', 'move', 'Austria')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Moves: Blocked Switch')
        # verify units
        self.assertResult(turn.previous, 'Austria', 'fail.target-not-empty:par_0')
        self.assertResult(turn.previous, 'Croatia', 'fail.more-moves-to-target:par_0')
        self.assertResult(turn.previous, 'France', 'fail.more-moves-to-target:par_0')
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
          
    def testFailedTrain(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
        # set commands
        self.setAssertCommand(turn, 'France', 'move', 'Austria')
        self.setAssertCommand(turn, 'Austria', 'move', 'Germany')
        self.setAssertCommand(turn, 'Germany', 'move', 'Denmark')
        self.setAssertCommand(turn, 'North Sea', 'move', 'Denmark')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Moves: Failed Train')
        # verify units
        self.assertResult(turn.previous, 'France', 'fail.target-not-empty:par_0')
        self.assertResult(turn.previous, 'Austria', 'fail.target-not-empty:par_0')
        self.assertResult(turn.previous, 'Germany', 'fail.more-moves-to-target:par_0')
        self.assertResult(turn.previous, 'North Sea', 'fail.more-moves-to-target:par_0')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'North Sea', 'Ship', 'Spain')
  
    def testSuccessfulTrain(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
        self.assertNoUnit(turn, 'Poland')
        # set commands
        self.setAssertCommand(turn, 'France', 'move', 'Austria')
        self.setAssertCommand(turn, 'Austria', 'move', 'Germany')
        self.setAssertCommand(turn, 'Germany', 'move', 'Poland')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Moves: Successful Train')
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
        self.setAssertCommand(turn, 'France', 'move', 'Austria')
        self.setAssertCommand(turn, 'Austria', 'move', 'Germany')
        self.setAssertCommand(turn, 'Germany', 'move', 'Poland')
        self.setAssertCommand(turn, 'Ukraine', 'move', 'Poland')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Moves: Blocked Train')
        # verify units
        self.assertResult(turn.previous, 'France', 'fail.target-not-empty:par_0')
        self.assertResult(turn.previous, 'Austria', 'fail.target-not-empty:par_0')
        self.assertResult(turn.previous, 'Germany', 'fail.more-moves-to-target:par_0')
        self.assertResult(turn.previous, 'Ukraine', 'fail.more-moves-to-target:par_0')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Ukraine', 'Army', 'Russia')

    def testSuccessfulSecondTrain(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'France', 'Army', 'Spain')
        self.assertNoUnit(turn, 'Poland')
        # set commands
        self.setAssertCommand(turn, 'France', 'move', ['France', 'Austria'])
        self.setAssertCommand(turn, 'Austria', 'move', ['Austria', 'Germany'])
        self.setAssertCommand(turn, 'Germany', 'move', 'Poland')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Moves: Successful Second Train')
        # verify units
        self.assertResult(turn.previous, 'France', 'ok')
        self.assertResult(turn.previous, 'Austria', 'ok')
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertNoUnit(turn, 'France')
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Poland', 'Army', 'Spain')

    def testDoubleSwitch(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'Austria', 'move', ['Croatia', 'Austria'])
        self.setAssertCommand(turn, 'Croatia', 'move', ['Austria', 'Croatia'])
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Moves: Double Switch')
        # verify units
        self.assertResult(turn.previous, 'Austria', 'ok')
        self.assertResult(turn.previous, 'Croatia', 'ok')
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')

    def testSuccessfulTrainSwitch(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        self.assertNoUnit(turn, 'Poland')
        # set commands
        self.setAssertCommand(turn, 'Croatia', 'move', ['Austria', 'Germany'])
        self.setAssertCommand(turn, 'Austria', 'move', ['Croatia', 'Austria'])
        self.setAssertCommand(turn, 'Germany', 'move', ['Germany', 'Poland'])
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Moves: Successful Train Switch')
        # verify units
        self.assertResult(turn.previous, 'France', 'ok')
        self.assertResult(turn.previous, 'Austria', 'ok')
        self.assertResult(turn.previous, 'Germany', 'ok')
        self.assertNoUnit(turn, 'Croatia')
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Germany', 'Army', 'Russia')
        self.assertUnit(turn, 'Poland', 'Army', 'Spain')

    def testFailedSecondTrainSwitch(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        self.assertNoUnit(turn, 'Poland')
        # set commands
        self.setAssertCommand(turn, 'Croatia', 'move', ['Austria', 'Germany'])
        self.setAssertCommand(turn, 'Austria', 'move', ['Croatia', 'Austria'])
        self.setAssertCommand(turn, 'Germany', 'move', ['Germany', 'Austria'])
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Moves: Failed Second Train Switch')
        # verify units
        self.assertResult(turn.previous, 'Croatia', 'fail.target-not-empty:par_1')
        self.assertResult(turn.previous, 'Austria', 'fail.more-moves-to-target:par_1')
        self.assertResult(turn.previous, 'Germany', 'fail.more-moves-to-target:par_1')
        self.assertUnit(turn, 'Austria', 'Army', 'Russia')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Spain')

    def testFirstBlockedNoSecondMove(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'Austria', 'move', ['Austria', 'Croatia'])
        self.setAssertCommand(turn, 'Croatia', 'move', ['Austria', 'Poland'])
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Moves: First Blocked No Second Move')
        # verify units
        self.assertResult(turn.previous, 'Austria', 'fail.more-moves-to-target:par_0')
        self.assertResult(turn.previous, 'Croatia', 'fail.more-moves-to-target:par_0')
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')

    def testMoveAttacked(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'Austria', 'move', 'Poland')
        self.setAssertCommand(turn, 'Croatia', 'attack', 'Austria')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Moves: Move attacked')
        # verify units
        self.assertResult(turn.previous, 'Austria', 'fail.canceled-by-attack')
        self.assertResult(turn.previous, 'Croatia', 'fail.defence-stronger')
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')

    def testSecondMoveAttacked(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'Austria', 'move', ['Austria', 'Poland'])
        self.setAssertCommand(turn, 'Croatia', 'attack', 'Austria')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Moves: Second Move attacked')
        # verify units
        self.assertResult(turn.previous, 'Austria', 'fail.canceled-by-attack')
        self.assertResult(turn.previous, 'Croatia', 'fail.defence-stronger')
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')

    def testMoveWeaker(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'Austria', 'move', 'Poland')
        self.setAssertCommand(turn, 'Croatia', 'attack', 'Poland')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Moves: Move Weaker')
        # verify units
        self.assertResult(turn.previous, 'Austria', 'fail.target-attacked:par_0')
        self.assertResult(turn.previous, 'Croatia', 'ok')
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Poland', 'Army', 'Russia')
        self.assertNoUnit(turn, 'Croatia')

    def testSecondMoveWeaker(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        # set commands
        self.setAssertCommand(turn, 'Austria', 'move', ['Austria', 'Poland'])
        self.setAssertCommand(turn, 'Croatia', 'attack', 'Poland')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Moves: Second Move Weaker')
        # verify units
        self.assertResult(turn.previous, 'Austria', 'fail.target-attacked:par_1')
        self.assertResult(turn.previous, 'Croatia', 'ok')
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Poland', 'Army', 'Russia')
        self.assertNoUnit(turn, 'Croatia')

    def testMoveToAttacked(self):
        turn = Turn.objects.get(pk=1)
        # verify units
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        # set commands
        self.setAssertCommand(turn, 'Austria', 'move', 'Poland')
        self.setAssertCommand(turn, 'Croatia', 'attack', 'Poland')
        self.setAssertCommand(turn, 'Germany', 'attack', 'Poland')
        # calculate turn
        turn = self.assertNextTurn(turn, '2000', 'Moves: Move to attacked field')
        # verify units
        self.assertResult(turn.previous, 'Austria', 'fail.target-attacked:par_0')
        self.assertResult(turn.previous, 'Croatia', 'fail.not-strongest')
        self.assertResult(turn.previous, 'Germany', 'fail.not-strongest')
        self.assertUnit(turn, 'Austria', 'Army', 'Spain')
        self.assertUnit(turn, 'Croatia', 'Army', 'Russia')
        self.assertUnit(turn, 'Germany', 'Army', 'Spain')
        self.assertNoUnit(turn, 'Poland')
