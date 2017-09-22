from django.test import TestCase
from django.core.management import call_command

class UiTests(TestCase):
    
    def setUp(self):
        call_command('loaddata', 'user', verbosity=0)
        call_command('loaddata', 'init', verbosity=0)
        call_command('loaddata', 'test/testworld', verbosity=0)
        
    def test_ui(self):
        response = self.client.post('/ui/login/', {'username': 'admin', 'password': 'administrator'})
        self.assertEqual(response.status_code, 200)
        