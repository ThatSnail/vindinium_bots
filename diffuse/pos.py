def distTo(x, y, destx, desty):
    return abs(x - destx) + abs(y - desty)

def validPos(x, y, size):
    return not (x < 0 or x >= size or y < 0 or y >= size)

def neighborPos(x, y, size):
    ' Return valid orthogonal neighbors '
    deltaPos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for dx, dy in deltaPos:
        nx = x + dx
        ny = y + dy
        if validPos(nx, ny, size):
            neighbors.append((nx, ny))
    return neighbors
