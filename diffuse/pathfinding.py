from pos import neighborPos, distTo, validPos
from collections import deque

fwList = {}

def insertPath(x, y, destx, desty, p):
    fwList[(x, y, destx, desty)] = p

def getPath(x, y, destx, desty):
    # TODO Exploit map x-symmetry
    if (x, y, destx, desty) in fwList:
        return fwList[(x, y, destx, desty)]
    elif (destx, desty, x, y) in fwList:
        return fwList[(destx, desty, x, y)]
    else:
        return None

def pathDistTo(game, x, y, destx, desty):
    if (x, y) == (destx, desty):
        return 0
    if not validPos(x, y, game.board.size) or not validPos(destx, desty, game.board.size):
        return -1
    path = getPath(x, y, destx, desty)
    if path != None:
        return path
    else:
        if game.board.passable((x, y)) and game.board.passable((destx, desty)):
            """
            # Check for neighbors in fwList
            neighborKeys = [(x + 1, y, destx, desty), (x - 1, y, destx, desty), (x, y - 1, destx, desty), (x, y + 1, destx, desty), (x, y, destx - 1, desty), (x, y, destx + 1, desty), (x, y, destx, desty - 1), (x, y, destx, desty + 1)]
            for n in neighborKeys:
                if n in fwList:
                    fwList[(x, y, destx, desty)] = fwList[n] + 1
                    return fwList[n] + 1
            """
            # Calculate with a-star instead
            p = astar(game, x, y, destx, desty)
            insertPath(x, y, destx, desty, p)
            return p
        else:
            return -1

def astar(game, x, y, destx, desty):
    if not game.board.passable((destx, desty)) or not game.board.passable((x, y)):
        return -1
    if (x, y) == (destx, desty):
        return 0
    closed = set([])
    frontier = deque([(0, distTo(x, y, destx, desty), x, y)])
    while len(frontier) > 0:
        p, d, x, y = frontier.popleft()
        closed.add((x, y))
        neighbors = neighborPos(x, y, game.board.size)
        minifrontier = []
        for nx, ny in neighbors:
            if (nx, ny) == (destx, desty):
                return p + 1
            if game.board.passable((nx, ny)) and (nx, ny) not in closed:
                minifrontier.append((p + 1, distTo(nx, ny, destx, desty), nx, ny))
                insertPath(x, y, nx, ny, p + 1)
        minifrontier.sort()
        frontier += minifrontier
    return -1
