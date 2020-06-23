from ui.tests.TestRest import TestRest
from django.core.management import call_command

class TestRestGame(TestRest):
    
    def setUp(self):
        call_command('loaddata', 'user', verbosity=0)
        call_command('loaddata', 'init', verbosity=0)
        call_command('loaddata', 'test/testWorld', verbosity=0)
        call_command('loaddata', 'test/testUnits', verbosity=0)
        
    def testGameRest(self):
        self.doFirstMove()

    def doFirstMove(self):
        print('---- test First Move ----')
        response = self.client.post('/ui/login/', {'username': 'russia', 'password': 'russia456'})
        self.assertEqual(response.status_code, 200)
        self.doTestRest('ui/tests/rest/game/1', 'unit_command:f=7&ct=2&args=5')

