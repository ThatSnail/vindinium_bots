from random import choice
import time
from game import Game, HBoard

class Bot:
    pass

class RandomBot(Bot):

    def move(self, state):
        game = Game(state)
        dirs = ['Stay', 'North', 'South', 'East', 'West']
        return choice(dirs)


class FighterBot(Bot):
    def move(self, state):
        dirs = ['Stay', 'North', 'South', 'East', 'West']
        return choice(dirs)



class SlowBot(Bot):
    def move(self, state):
        dirs = ['Stay', 'North', 'South', 'East', 'West']
        time.sleep(2)
        return choice(dirs)

class CrapBot(Bot):
    name = "crapbot"
    dirs = {(0, 0): 'Stay',
            (0, -1): 'North',
            (0,  1): 'South',
            (-1, 0): 'East',
            (1,  0): 'West'}

    def move(self, state):
        game = Game(state)
        hboard = HBoard(game, game.board)
        hboard.diffuse_board()
        return CrapBot.dirs[hboard.best_move(game.own_hero(CrapBot.name).pos)]
