import operator

def prod(seq):
    return reduce(operator.mul, seq)


def get_grid():
    out = []
    fh = open("p11.dat")
    for line in fh:
        row = map(int, line.split())
        out.append(row)
    fh.close()

    return out

def get_max(grid):
    max_val = 0
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if j <= len(row) - 4:
                max_val = max(max_val, prod(row[j:j+4]))
            if i <= len(grid) - 4:
                line = [grid[i][j], grid[i + 1][j], grid[i + 2][j], grid[i + 3][j]]
                max_val = max(max_val, prod(line))
            if j <= len(row) - 4 and i <= len(grid) - 4:
                line = [grid[i][j], grid[i + 1][j + 1], grid[i + 2][j + 2], grid[i + 3][j + 3]]
                max_val = max(max_val, prod(line))
            if j >= 3 and i <= len(grid) - 4:
                line = [grid[i][j], grid[i + 1][j - 1], grid[i + 2][j - 2], grid[i + 3][j - 3]]
                max_val = max(max_val, prod(line))
    return max_val

print get_max(get_grid())



