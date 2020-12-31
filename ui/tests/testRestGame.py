from ui.tests.TestRest import TestRest
from django.core.management import call_command

class TestRestGame(TestRest):
    
    def setUp(self):
        call_command('loaddata', 'user', verbosity=0)
        call_command('loaddata', 'init', verbosity=0)
        call_command('loaddata', 'test/testWorld', verbosity=0)
        call_command('loaddata', 'test/testUnits', verbosity=0)
        
    def testGameRest(self):
        self.doMove1999()
        self.doMove2000()

    def doMove1999(self):
        print('---- test 1999 ----')
        # set russian commands
        self.loginRussia()
        self.doTestRest('ui/tests/rest/game/1/move0', 'index1')
        self.doTestRest('ui/tests/rest/game/1/move0', 'unit_get:f=7')
        self.doTestRest('ui/tests/rest/game/1/move0', 'unit_get:f=5')
        self.doTestRest('ui/tests/rest/game/1/move0', 'unit_command:f=7&ct=2&args=5')
        self.logout()
        # set spanish commands
        self.loginSpain()
        self.logout()
        # end move
        self.endMove('ui/tests/rest/game/1/move0', 'index2')
        # test units
        self.loginRussia()
        self.doTestRest('ui/tests/rest/game/1/move0/result', 'unit_get:f=7')
        self.doTestRest('ui/tests/rest/game/1/move0/result', 'unit_get:f=5')
        
    def doMove2000(self):
        print('---- test 2000 ----')
        # set russian commands
        self.loginRussia()
        self.logout()
        # set spanish commands
        self.loginSpain()
        self.logout()
        # end move
        #self.endMove('ui/tests/rest/game/1/move1', 'index1')
        
        

