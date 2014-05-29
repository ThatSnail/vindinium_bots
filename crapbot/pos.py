def in_radius(pos, radius, size):
    if radius == 0:
        return [pos]
    x, y = pos[0], pos[1]
    out = []
    def check_append(x, y):
        if valid_pos(x, y, size):
            out.append((x, y))
    for r in range(radius):
        check_append(x + r, y + radius - r - 1)
        check_append(x + radius - r - 1, y + r)
        check_append(x - r, y - (radius - r - 1))
        check_append(x - (radius - r - 1), y - r)
    return out + in_radius(pos, radius - 1, size)

def valid_pos(x, y, size):
    return 0 <= x and x < size and 0 <= y and y < size
