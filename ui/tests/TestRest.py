from django.test import TestCase
import os

class TestRest(TestCase):
    
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
    
    
