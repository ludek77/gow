from django.test import TestCase
from ui.models import Turn, Game
from django.utils import timezone, dateformat
from datetime import datetime
import os, pytz, re

class TestRest(TestCase):
    
    def writeResult(self, filename, content):
        file = open(filename, 'w')
        file.write(content)
        file.close()

    # Normalize dynamic content (deadlines) for comparison
    def normalize_timestamps(self, content):
        # Replace deadline timestamps with a fixed placeholder
        # Pattern matches "Deadline: YYYY-MM-DD HH:MM"
        return re.sub(r'Deadline: \d{4}-\d{2}-\d{2} \d{2}:\d{2}', 'Deadline: ####-##-## ##:##', content)
        
    def doTestRest(self, rootUrl, filename, replaceText=None):
        print('Testing '+rootUrl+'/'+filename)
        # Convert filename format to match actual file names on disk
        # Replace : with .colon., = with .equals., and & with .and.
        disk_filename = filename.replace(':', '.colon.').replace('&', '.and.')
        
        # Handle cases where parameter ends with = (empty value)
        import re
        disk_filename = re.sub(r'=([&]|$)', r'.equals.end\1', disk_filename)
        # Replace remaining = with .equals.
        disk_filename = disk_filename.replace('=', '.equals.')
        
        if disk_filename.endswith('.'):
            disk_filename = disk_filename[:-1] + '.end'
                
        # get expected result
        file = open(rootUrl+'/'+disk_filename, 'r')
        expectedResult = file.read().rstrip()
        file.close()
        # replace placeholder if defined
        if(replaceText != None):
            #print("replacing #### with '"+replaceText+"'")
            expectedResult = expectedResult.replace('####', replaceText)
        # get real result
        url = '/ui/' + filename.replace(':','/?')
        if(url.startswith('/ui/index')):
            url = '/ui/'
        result = self.client.get(url)
        resultContent = result.content.decode('utf-8').rstrip()
        
        expectedResult = self.normalize_timestamps(expectedResult)
        resultContent = self.normalize_timestamps(resultContent)
#         expectedResult = 'load'
        if expectedResult == 'load':
            print('writing '+filename)
            self.writeResult(rootUrl+'/'+filename, resultContent)
        else:
            if result.status_code == 200:
                self.assertEqual(expectedResult, resultContent)
            else:
                self.assertEqual(expectedResult, 'response:'+str(result.status_code))

    def loginRussia(self):
        response = self.client.post('/ui/login/', {'username': 'russia', 'password': 'russia456'})
        self.assertEqual(response.status_code, 200)
        
    def loginSpain(self):
        response = self.client.post('/ui/login/', {'username': 'spain', 'password': 'spain258'})
        self.assertEqual(response.status_code, 200)
        
    def logout(self):
        response = self.client.post('/ui/logout')
        self.assertEqual(response.status_code, 301)
        
    def endMove(self, indexFolder, indexFile):
        game = Game.objects.get(pk=1)
        # get turn and set deadline to now
        turn = Turn.objects.get(game=game, open=True)
        turn.deadline = datetime.now(tz=pytz.utc)
        turn.save()
        # call index to recalculate move
        newDeadline = turn.deadline + timezone.timedelta(minutes=turn.game.turnMinutes)
        # move by one/two more hour for timezone diff
        newDeadline = newDeadline + timezone.timedelta(hours = 2)
        self.doTestRest(indexFolder, indexFile, dateformat.format(newDeadline, 'Y-m-d H:i'))
        # verify that move was done
        nextTurn = Turn.objects.get(game=game, open=True)
        self.assertEqual(nextTurn.previous, turn)
        print('Move '+turn.name+ ' ended')

