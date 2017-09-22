from django.test import TestCase
from django.core.management import call_command
from ui.models import Game, Turn
from ui.engine.Engine import Engine

class EngineTests(TestCase):
    
    def setUp(self):
        call_command('loaddata', 'user', verbosity=0)
        call_command('loaddata', 'init', verbosity=0)
        call_command('loaddata', 'test/testworld', verbosity=0)
        
    def test_Engine(self):
        game = Game.objects.get(pk=1)
        
        Engine().recalculate(game)
    #    game = Game()
    #    turn = Turn()
    #    newTurn = Engine().recalculate(game, turn)
        