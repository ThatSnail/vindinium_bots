from random import choice
import time
from game import Game, HeroTile, MineTile, Statics
from pos import distTo, validPos

class Bot:
    pass

class DiffuseBot(Bot):

    def calculate_cell(self, pos, game):
        if not validPos(pos[0], pos[1], game.board.size):
            return -10000
        score = 0

        def calc_score(amt, x, y, destx, desty):
            ' Increment score based on distance falloff '
            return amt / (distTo(x, y, destx, desty) + 1)

        for x in range(game.board.size):
            for y in range(game.board.size):
                tile = game.board.tiles[x][y]
                if tile == Statics.AIR:
                    score += calc_score(1, x, y, pos[0], pos[1])
                elif isinstance(tile, HeroTile):
                    if game.hero.pos == (x, y):
                        # Own hero
                        pass
                    else:
                        # Other hero
                        enemyHero = game.getHeroAtPos(x, y)
                        score += calc_score(10, x, y, pos[0], pos[1])
                elif isinstance(tile, MineTile):
                    if tile.heroId != game.heroId:
                        if game.hero.life > 40:
                            score += calc_score(100, x, y, pos[0], pos[1])
                        else:
                            score += calc_score(-2, x, y, pos[0], pos[1])
                elif tile == Statics.TAVERN:
                    if game.hero.life < 20:
                        score += calc_score(100, x, y, pos[0], pos[1])
                    else:
                        score += calc_score(4, x, y, pos[0], pos[1])
        return score

    def move(self, state):
        game = Game(state)
        cpos = game.hero.pos
        positions = {
            cpos                   : "Stay",
            (cpos[0], cpos[1] - 1) : "West",
            (cpos[0], cpos[1] + 1) : "East",
            (cpos[0] - 1, cpos[1]) : "North",
            (cpos[0] + 1, cpos[1]) : "South"
            }
        bestScore = -99999
        bestMove = None
        for p in positions.keys():
            score = self.calculate_cell(p, game)
            if score > bestScore:
                bestScore = score
                bestMove = positions[p]
        return bestMove
