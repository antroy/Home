LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3

def direction(size):
    DIRS = [RIGHT, DOWN, LEFT, UP]
    corners_turned = 0
    steps_to_take = 1
    i = 1
    steps_taken = 0

    middle = (size - 1)/2
    coords = [middle, middle]


    while i < size ** 2:
        yield (coords, i)
        i += 1

        if steps_taken == steps_to_take:
            steps_taken = 0
            if corners_turned % 2:
                steps_to_take += 1
            corners_turned +=1
        
        steps_taken += 1
        
        direction = DIRS[corners_turned % 4]
        adjust_coords(coords, direction)
    yield (coords, i)

        
def adjust_coords(coords, direction):
    if direction == LEFT:
        coords[0] -= 1
    if direction == RIGHT:
        coords[0] += 1
    if direction == UP:
        coords[1] -= 1
    if direction == DOWN:
        coords[1] += 1


def get_spiral(size):
    out = [[None for x in range(size)] for y in range(size)]
    
    for coords, value in direction(size):
        x, y = coords
        out[x][y] = value

    return out

def print_spiral(input):
    for row in input:
        print row

def sum_diags(input):
    rd = []
    lu = []

    for i in range(len(input)):
        rd.append(input[i][i])
        lu.append(input[i][-i-1])

    rd.extend(lu)
    return sum(rd) - 1


if __name__ == "__main__":
    print "Answer:", sum_diags(get_spiral(1001))
    #for c in direction(5):
    #    print c

    #print len(list(direction(5)))


