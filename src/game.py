from player import Player
from settings import *

class Game:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.player1 = Player(0, 4, BLUE)
        self.player2 = Player(8, 4, RED)

        self.players = [self.player1, self.player2]

        self.current_player_index = 0

        self.horizontal_walls = set()
        self.vertical_walls = set()

        self.game_over = False
        self.winner = None

    def current_player(self):
        return self.players[self.current_player_index]

    def switch_turn(self):
        self.current_player_index = 1 - self.current_player_index