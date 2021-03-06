from django.test import TestCase
from django.core.management import call_command

class TestUi(TestCase):
    
    def setUp(self):
        call_command('loaddata', 'user', verbosity=0)
        call_command('loaddata', 'init', verbosity=0)
        call_command('loaddata', 'test/testWorld', verbosity=0)
        
    def test_ui(self):
        response = self.client.post('/ui/login/', {'username': 'admin', 'password': 'admin1379'})
        self.assertEqual(response.status_code, 200)
        
    def test_wrong_pwd(self):
        response = self.client.post('/ui/login/', {'username': 'admin', 'password': 'admin137xxx'})
        self.assertEqual(response.status_code, 401)
        
    def test_bad_user(self):
        response = self.client.post('/ui/login/', {'username': 'adminxxx', 'password': 'admin1379'})
        self.assertEqual(response.status_code, 401)