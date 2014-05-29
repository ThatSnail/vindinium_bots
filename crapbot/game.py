import re
from pos import in_radius, valid_pos
from math import sqrt

TAVERN = 0
AIR = -1
WALL = -2

PLAYER1 = 1
PLAYER2 = 2
PLAYER3 = 3
PLAYER4 = 4

AIM = {'North': (-1, 0),
       'East': (0, 1),
       'South': (1, 0),
       'West': (0, -1)}

class HeroTile:
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return self.id

class MineTile:
    def __init__(self, heroId = None):
        self.heroId = heroId

    def __repr__(self):
        return self.heroId

class Game:
    def __init__(self, state):
        self.state = state
        self.board = Board(state['game']['board'])
        self.heroes = [Hero(state['game']['heroes'][i]) for i in range(len(state['game']['heroes']))]
        self.mines_locs = {}
        self.heroes_locs = {}
        self.taverns_locs = set([])
        for row in range(len(self.board.tiles)):
            for col in range(len(self.board.tiles[row])):
                obj = self.board.tiles[row][col]
                if isinstance(obj, MineTile):
                    self.mines_locs[(row, col)] = obj.heroId
                elif isinstance(obj, HeroTile):
                    self.heroes_locs[(row, col)] = obj.id
                elif (obj == TAVERN):
                    self.taverns_locs.add((row, col))

    def own_hero(self, name):
        return filter(lambda h: h.name == name, self.heroes)[0]

    def other_heroes(self, name):
        return filter(lambda h: h.name != name, self.heroes)

class Board:
    def __parseTile(self, str):
        if (str == '  '):
            return AIR
        if (str == '##'):
            return WALL
        if (str == '[]'):
            return TAVERN
        match = re.match('\$([-0-9])', str)
        if (match):
            return MineTile(match.group(1))
        match = re.match('\@([0-9])', str)
        if (match):
            return HeroTile(match.group(1))

    def __parseTiles(self, tiles):
        vector = [tiles[i:i+2] for i in range(0, len(tiles), 2)]
        matrix = [vector[i:i+self.size] for i in range(0, len(vector), self.size)]

        return [[self.__parseTile(x) for x in xs] for xs in matrix]

    def __init__(self, board):
        self.size = board['size']
        self.tiles = self.__parseTiles(board['tiles'])

    def passable(self, loc):
        'true if can not walk through'
        x, y = loc
        pos = self.tiles[x][y]
        return (pos != WALL) and (pos != TAVERN) and not isinstance(pos, MineTile)

    def to(self, loc, direction):
        'calculate a new location given the direction'
        row, col = loc
        d_row, d_col = AIM[direction]
        n_row = row + d_row
        if (n_row < 0): n_row = 0
        if (n_row > self.size): n_row = self.size
        n_col = col + d_col
        if (n_col < 0): n_col = 0
        if (n_col > self.size): n_col = self.size

        return (n_row, n_col)


class HBoard:
    def __init__(self, game, board):
        self.game = game
        self.hboard = dict()
        self.size = board.size
        for x in range(board.size):
            for y in range(board.size):
                self.hboard[(x, y)] = (board.tiles[x][y], 0) # Initialize tiles with 0 weight
        
    def diffuse_board(self):
        #RW_HERO = (10, lambda hero: (((100 - hero.life) / 100) * 2 - 1) * 80 if hero.name != "crapbot" else -5000)
        RW_HERO = (10, lambda hero: 100000 if hero.name != "crapbot" else -5000)
        RW_MINE = (5, 10)
        RW_TAVERN = (0, 0)
        RW_AIR = (0, 0)
        RW_WALL = (0, -100)
        def diffuse_tile(pos, tile, weight):
            if isinstance(tile, HeroTile):
                # Fucking massive hack
                # Get hero at pos
                rw = (RW_HERO[0], lambda pos, _: RW_HERO[1](filter(lambda h: h.pos == pos, self.game.heroes)[0]))
            elif isinstance(tile, MineTile):
                rw = (RW_MINE[0], lambda x, y: RW_MINE[1])
            elif tile == TAVERN:
                rw = (RW_TAVERN[0], lambda x, y: RW_TAVERN[1])
            elif tile == AIR:
                rw = (RW_AIR[0], lambda x, y: RW_AIR[1])
            elif tile == WALL:
                rw = (RW_WALL[0], lambda x, y: RW_WALL[1])
            r, w = rw
            for p in in_radius(pos, r, self.size):
                dist = sqrt(pow(p[0] - pos[0], 2) + pow(p[1] - pos[1], 2))
                self.hboard[p] = (self.hboard[p][0], self.hboard[p][1] + w(pos, tile) * dist / (r + 1))
        map(lambda p: diffuse_tile(p, self.hboard[p][0], self.hboard[p][1]), self.hboard.keys())

    def best_move(self, pos):
        x, y = pos
        moves = []
        def add_move(dx, dy):
            if valid_pos(x + dx, y + dy, self.size):
                newpos = (x + dx, y + dy)
                moves.append((self.hboard[newpos][1], (dx, dy)))
        map(lambda p: add_move(p[0], p[1]), [(0, 0), (0, 1), (1, 0), (0, -1), (-1, 0)])
        return max(moves)[1]

    def __repr__(self):
        return str(self.hboard)


class Hero:
    def __init__(self, hero):
        self.name = hero['name']
        self.pos = (hero['pos']['x'], hero['pos']['y'])
        self.life = hero['life']
        self.gold = hero['gold']

    def __repr__(self):
        return str(self.pos)
