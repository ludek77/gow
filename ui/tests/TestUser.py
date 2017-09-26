from django.test import TestCase
from django.core.management import call_command
from django.urls import reverse

class TestUser(TestCase):
    
    def setUp(self):
        call_command('loaddata', 'user', verbosity=0)
    
    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/ui/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post('/ui/login/', {'username': 'unknown', 'password': 'unknown'})
        self.assertEqual(response.status_code, 401)
        
        response = self.client.post('/ui/login/', {'username': 'admin', 'password': 'administrator'})
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get('/ui/logout/')
        self.assertEqual(response.status_code, 302)
        
        response = self.client.post('/ui/login/', {'username': 'admin', 'password': 'administrator'})
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/ui/logout/')
        self.assertEqual(response.status_code, 200)
        