from django.test import TestCase
from django.core.management import call_command
import os
from reportlab.platypus import tableofcontents

class TestRest(TestCase):
    
    def setUp(self):
        call_command('loaddata', 'user', verbosity=0)
        call_command('loaddata', 'init', verbosity=0)
        call_command('loaddata', 'test/testWorld', verbosity=0)
        call_command('loaddata', 'test/testUnits', verbosity=0)
        
    def testAuthorizedRusRest(self):
        print('---- test Rus ----')
        response = self.client.post('/ui/login/', {'username': 'russia', 'password': 'russia456'})
        self.assertEqual(response.status_code, 200)
        self.doTestRest('ui/tests/rest/rus-auth', 'city_get:c=1')
        self.doTestRest('ui/tests/rest/rus-auth', 'city_get:c=2')
        self.doTestRest('ui/tests/rest/rus-auth', 'country_setup:')
        self.doTestRest('ui/tests/rest/rus-auth', 'game_list:')
        self.doTestRest('ui/tests/rest/rus-auth', 'game_select:g=2')
        self.doTestRest('ui/tests/rest/rus-auth', 'game_select:g=1')
        self.doTestRest('ui/tests/rest/rus-auth', 'game_setup:')
        self.doTestRest('ui/tests/rest/rus-auth', 'unit_get:f=1')
        self.doTestRest('ui/tests/rest/rus-auth', 'unit_get:f=29')
        self.doTestRest('ui/tests/rest/rus-auth', 'unit_command:f=29&ct=1&args=1')
        self.doTestRest('ui/tests/rest/rus-auth', 'city_command:f=29&ct=1&args=1')
        
    def testAuthorizedSpainRest(self):
        print('---- test Spain ----')
        response = self.client.post('/ui/login/', {'username': 'spain', 'password': 'spain258'})
        self.assertEqual(response.status_code, 200)
        self.doTestRest('ui/tests/rest/spain-auth', 'city_get:c=2')
        self.doTestRest('ui/tests/rest/spain-auth', 'country_setup:')
        self.doTestRest('ui/tests/rest/spain-auth', 'game_list:')
        self.doTestRest('ui/tests/rest/spain-auth', 'game_select:g=1')
        self.doTestRest('ui/tests/rest/spain-auth', 'game_setup:')
        self.doTestRest('ui/tests/rest/spain-auth', 'unit_get:f=1')
        self.doTestRest('ui/tests/rest/spain-auth', 'unit_get:f=29')
        self.doTestRest('ui/tests/rest/spain-auth', 'unit_command:f=29&ct=1&args=')
        self.doTestRest('ui/tests/rest/spain-auth', 'unit_command:f=29&ct=1&args=1')
        self.doTestRest('ui/tests/rest/spain-auth', 'unit_command:f=29&ct=2&args=2')
        self.doTestRest('ui/tests/rest/spain-auth', 'unit_command:f=29&ct=2&args=8')
        self.doTestRest('ui/tests/rest/spain-auth', 'unit_command:f=29&ct=3&args=1')
        self.doTestRest('ui/tests/rest/spain-auth', 'unit_command:f=29&ct=3&args=1,8')
        self.doTestRest('ui/tests/rest/spain-auth', 'unit_command:f=29&ct=3&args=1,1')
        self.doTestRest('ui/tests/rest/spain-auth', 'unit_command:f=29&ct=4&args=1')
        self.doTestRest('ui/tests/rest/spain-auth', 'unit_command:f=29&ct=5&args=1')
        self.doTestRest('ui/tests/rest/spain-auth', 'unit_command:f=29&ct=6&args=1')
        self.doTestRest('ui/tests/rest/spain-auth', 'unit_command:f=29&ct=7&args=1')
        self.doTestRest('ui/tests/rest/spain-auth', 'unit_command:f=29&ct=8&args=')
        self.doTestRest('ui/tests/rest/spain-auth', 'unit_command:f=29&ct=prio&args=')
        self.doTestRest('ui/tests/rest/spain-auth', 'unit_command:f=29&ct=prio&args=1')
        self.doTestRest('ui/tests/rest/spain-auth', 'unit_command:f=29&ct=prio&args=-1')
        self.doTestRest('ui/tests/rest/spain-auth', 'unit_command:f=29&ct=esc&args=')
        self.doTestRest('ui/tests/rest/spain-auth', 'unit_command:f=29&ct=esc&args=1')
        self.doTestRest('ui/tests/rest/spain-auth', 'unit_command:f=29&ct=esc&args=8')
        self.doTestRest('ui/tests/rest/spain-auth', 'city_command:f=29&ct=1&args=1')
        self.doTestRest('ui/tests/rest/spain-auth', 'city_command:f=29&ct=2&args=')
        self.doTestRest('ui/tests/rest/spain-auth', 'city_command:f=29&ct=3&args=')
        self.doTestRest('ui/tests/rest/spain-auth', 'city_command:f=29&ct=prio&args=')
        self.doTestRest('ui/tests/rest/spain-auth', 'city_command:f=29&ct=prio&args=1')
        self.doTestRest('ui/tests/rest/spain-auth', 'city_command:f=29&ct=prio&args=-1')

    def testUnauthorizedRest(self):
        print('---- test NoAuth ----')
        self.doTestRest('ui/tests/rest/no-auth', 'city_get:c=1')
        self.doTestRest('ui/tests/rest/no-auth', 'country_setup:')
        self.doTestRest('ui/tests/rest/no-auth', 'game_list:')
        self.doTestRest('ui/tests/rest/no-auth', 'game_select:g=1')
        self.doTestRest('ui/tests/rest/no-auth', 'game_setup:')
        self.doTestRest('ui/tests/rest/no-auth', 'unit_get:f=1')
        self.doTestRest('ui/tests/rest/no-auth', 'unit_command:f=29&ct=1&args=1')
        self.doTestRest('ui/tests/rest/no-auth', 'city_command:f=29&ct=1&args=1')
         
    def writeResult(self, filename, content):
        file = open(filename, 'w')
        file.write(content)
        file.close()
        
    def doTestRest(self, rootUrl, filename):
        print('Testing '+rootUrl+'/'+filename)
        # get expected result
        file = open(rootUrl+'/'+filename, 'r')
        expectedResult = file.read()
        file.close()
        # get real result
        url = '/ui/' + filename.replace(':','/?')
        result = self.client.get(url)
        resultContent = result.content.decode('utf-8')
#         expectedResult = 'load'
        if expectedResult == 'load':
            print('writing '+filename)
            self.writeResult(rootUrl+'/'+filename, resultContent)
        else:
            if result.status_code == 200:
                self.assertEqual(expectedResult, resultContent)
            else:
                self.assertEqual(expectedResult, 'response:'+str(result.status_code))
    
    