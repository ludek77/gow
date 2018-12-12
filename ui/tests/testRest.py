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
        
    def testAuthorizedRest(self):
        response = self.client.post('/ui/login/', {'username': 'admin', 'password': 'administrator'})
        self.assertEqual(response.status_code, 200)
        self.doTestRest('ui/tests/rest/auth')
        
    def testUnauthorizedRest(self):
        self.doTestRest('ui/tests/rest/no-auth')
        
    def writeResult(self, filename, content):
        file = open(filename, 'w')
        file.write(content)
        file.close()
        
    def doTestRest(self, rootUrl):
        for filename in os.listdir(rootUrl):
            #print('Testing '+filename)
            # get expected result
            file = open(rootUrl+'/'+filename, 'r')
            expectedResult = file.read()
            # get real result
            url = '/ui/' + filename.replace(':','/?')
            result = self.client.get(url)
            resultContent = result.content.decode('utf-8')
            #self.writeResult(rootUrl+'/'+filename+'.result', resultContent)
            if result.status_code == 200:
                self.assertEqual(expectedResult, resultContent)
            else:
                self.assertEqual(expectedResult, str(result.status_code))
            print(url+' ok')
        
        