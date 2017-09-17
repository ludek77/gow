
class Engine:
    
    def __init__(self, game, turn):
        print("Initializing "+game.name+"."+turn.name)
        
    def recalculate(self):
        print("Recalculating")
        
    def newTurn(self):
        return None