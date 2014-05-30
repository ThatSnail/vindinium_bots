def distTo(x, y, destx, desty):
    return abs(x - destx) + abs(y - desty)

def validPos(x, y, size):
    return not (x < 0 or x >= size or y < 0 or y >= size)
