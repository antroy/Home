import pdb

def gtl(x,y):
    """Grid to Linear coordinates"""
    return (y * 9) + x

class grid(object):
    def __init__(self, numbers):
        self.grid = []
        for n in numbers:
            if n in "123456789":
                self.grid.append([n])
            else:
                self.grid.append([1,2,3,4,5,6,7,8,9])
        
        grps = [[],[],[],[],[],[],[],[],[]]
        rows = []
        cols = []
        
        for i in range(9):
            row = []
            col = []
            for j in range(9):
                row.append(self.grid[gtl(j, i)])
                col.append(self.grid[gtl(i,j)])
                grps[((i/3) * 3) + (j/3)].append(self.grid[gtl(i,j)])
                
            rows.append(row)
            cols.append(col)
            
        self.groups = grps
        self.rows = rows
        self.columns = cols

    @classmethod
    def valid(clzz, grp):
        copy = list(grp)
        copy.sort()
        out = copy == [[1],[2],[3],[4],[5],[6],[7],[8],[9]]
        
        if not out:
            print "INVALID GROUP: ", copy
        
        return out
        
    def solved(self):
        for cell in self.grid:
            if len(cell) > 1:
                return False
            if len(cell) == 0:
                raise InvalidSolutionError, "This solultion is invalid!"
                
        for grp in self.groups:
            if not self.valid(grp):
                return False
            
        for grp in self.rows:
            if not self.valid(grp):
                return False
            
        for grp in self.columns:
            if not self.valid(grp):
                return False
                
        return True
        
    def apply_algorithm(self, algorithm):
        changed = False
        
        for group in self.groups:
            changed = algorithm(group) or changed
        for group in self.rows:
            changed = algorithm(group) or changed
        for group in self.columns:
            changed = algorithm(group) or changed
            
        if changed:
            self.apply_algorithm(algorithm)
            
        return changed
            
    def print_all_groups(self, verbose=False):
        out = "Rows:\n%s\nColumns:\n%s\nGroups:\n%s\n"
        
        def minimise(s):
            if verbose:
                return s
            arr = []
            for x in s:
                if len(x) < 1:
                    arr.append(-1)
                elif len(x) > 1:
                    arr.append(0)
                else:
                    arr.append(x[0])
            return arr
        
        c = [minimise(x) for x in self.columns]
        r = [minimise(x) for x in self.rows]
        g = [minimise(x) for x in self.groups]
        
        print out % (r, c, g)
    
    def print_grid(self, filename=None):
        br = (((('+' + '-' * 11) * 3) + '+') * 3) + '\n'
        out = br
        for i in range(9):
            for j in range(9):
                out += "| %9s " % "".join(str(q) for q in self.grid[gtl(i,j)])
                if (j + 1) % 3 == 0: out += '|'
                
            out += "\n"
            if (i + 1) % 3 == 0: 
                out += br
            
        if filename:
            fh = file(filename, 'w')
            fh.write(out)
            fh.close()
        else:
            print out
        
    def print_row(self, index):
        print self.rows[index]
        
    def print_column(self, index):
        print self.columns[index]
        
    def print_group(self, index):
        print self.groups[index]

class InvalidSolutionError (Exception):
    pass

def validate_group(group):
    for cell in group:
        if len(cell) < 1:
            raise InvalidSolutionError, "Group invalid! Cells cannot be empty!"
    
def remove_known_numbers(group):
    """For each solved cell, we can eliminate the number in that cell from each of 
    it's containing groups, rows and columns"""
    changed = False

    for single in group:
        if len(single) > 1:
            continue
        if len(single) == 0:
            raise InvalidSolutionError, "Cells cannot be empty!"
        
        eliminate = single[0]
        
        for cell in group:
            if cell is single:
                continue
            if eliminate in cell:
                cell.remove(eliminate)
                changed = True
                
    validate_group(group)
    if changed:
        remove_known_numbers(group)

    return changed

def get_eliminate_tups(size=2):
    def eliminate_tups(group):
        """For example if a group contains two cells with the same pair of numbers
        in, (e.g. [[1,2], [1,2,3], 6, [5,4], 8, 9, [2,4,5], [1,2], 7]) we can eliminate those
        two numbers from all other cells in the group (i.e. the group becomes: 
        [[1,2], 3, 6, [5,4], 8, 9, [4,5], [1,2], 7])
        """
        changed = False
        
        tups = [x for x in group if len(x) == size]
        
        def tups_identical(a, b):
            for x in a:
                if not x in b:
                    return False
            return True
        
        for tup in tups:
            temp = [x for x in tups if tups_identical(tup, x)]
            if len(temp) > size:
                raise Exception, "Suduko - error in calulations. More than one tup of numbers in a group." + tup
            elif len(temp) < size:
                continue
            
            for cell in group:
                if not cell == tup:
                    for i in tup:
                        if i in cell:
                            cell.remove(i)
                            changed = True
        
        if changed:
            eliminate_tups(group)
                            
        return changed
    return eliminate_tups
        
def confirm_solitary(group):
    """In a group, if there is a single cell which is the only cell containing a 
    particular number, then that cell can be confirmed to be definitely that number.
    e.g. [[1,2,7], 3, 6, 4, 8, 9, [1,2,5], [1,2,7], [1,2,7]] we can see that the 
    7th cell is the only possible candidate for the number 5, so we get:
    [[1,2,7], 3, 6, 4, 8, 9, 5, [1,2,7], [1,2,7]]"""
    
    changed = False
    
    for i in range(1, 10):
        count = 0
        cell = None
        for j in range(9):
            temp_cell = group[j]
            if i in temp_cell:
                count += 1
                if len(temp_cell) > 1:
                    cell = temp_cell
            if count > 1: 
                break
        if cell and count == 1:
            cell[:] = [i]
            changed = True
            
    return changed

def get_smallest_cell(g):
    out = None
    size = 10
    
    for cell in g.grid:
        #print cell,
        length = len(cell)
        if length < size and length >= 2:
            size = len(cell)
            out = cell
            if size == 2:
                break
            
    #print ""
    return out
    
def ariadnes_thread(grd, top=False, count=None):
    """Backtracking trial and error search for a solution"""
    
    if not count:
        count = [0]
    
    if top: print "Trying Ariadne's approach"
    count[0] += 1
    
    while True:
        try:
            if solve(grd):
                print "(recursed %d times)" % count[0]
                return True
        except Exception, ex:
            return False
        
        cell = get_smallest_cell(grd)
        
        if not cell:
            print "NOT_A_CELL!"
            break
        if len(cell) == 1:
            print "LEN ONE"
            
        test_val = cell[0]
        original_cell = cell[:]
        cell[:] = [test_val]
        
        if ariadnes_thread(grd, False, count):
            if top: print "Ariadne finished successfully!"
            return True
            
        cell[:] = original_cell
        cell.remove(test_val)
        
    return False
    
def solve(game):
    """Input array must be an array of 81 integers, 0-9 where 0
    denotes no value present in the grid"""
    
    while True:
        changed = False
        changed = game.apply_algorithm(remove_known_numbers) or changed
        print "Changed?%s" % changed
        changed = game.apply_algorithm(get_eliminate_tups()) or changed
        changed = game.apply_algorithm(get_eliminate_tups(3)) or changed
        changed = game.apply_algorithm(confirm_solitary) or changed
        
        if not changed or game.solved():
            break
    
    return game.solved()
    
    
def asst(b):
    print b and "OK" or "FAILED"
    
if __name__ == "__main__":
    arr = [[1,2,7], [3], [6], [4], [8], [9], [1,2,5], [1,2,7], [1,2,7]]
    exp = [[1,2,7], [3], [6], [4], [8], [9], [5], [1,2,7], [1,2,7]]
    confirm_solitary(arr)
    asst(arr == exp)
    
    group = [[1,2,3,4,5,6,7,8,9],
             [1,2,3,4,5,6,7,8,9],
             [1,2,3,4,5,6,7,8,9],
             [1,2,3,4,5,6,7,8,9],
             [1,2,3,4,5,6,7,8,9],
             [1,2,3,4,5,6,7,8,9],
             [1,2,3,4,5,6,7,8,9],
             [1,2,3,4,5,6,7,8,9],
             [1]]
             
    exp =   [[2,3,4,5,6,7,8,9],
             [2,3,4,5,6,7,8,9],
             [2,3,4,5,6,7,8,9],
             [2,3,4,5,6,7,8,9],
             [2,3,4,5,6,7,8,9],
             [2,3,4,5,6,7,8,9],
             [2,3,4,5,6,7,8,9],
             [2,3,4,5,6,7,8,9],
             [1]]
    
    remove_known_numbers(group)
    asst(group == exp)
    
    group2 = [[9],
             [1,2,3],
             [2],
             [6,7],
             [1,2,8,9],
             [1,4,5],
             [6,7,5,8,9],
             [7,8,9],
             [1]]
    
    remove_known_numbers(group2)
    asst(group2 == [[9], [3], [2], [6], [8], [4], [5], [7], [1]])
    
    try:
        group3 = [[1],[2],[1],[1],[1],[1],[1],[1],[1]]
        remove_known_numbers(group3)
    except InvalidSolutionError:
        print "OK"
    
    asst(grid.valid([1,2,3,7,6,5,4,8,9]))
    
    asst(not grid.valid([1,2,7,7,6,5,4,8,9]))
    
