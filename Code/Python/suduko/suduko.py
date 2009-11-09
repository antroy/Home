#:folding=indent:collapseFolds=2:
import sys, os.path as path

class game:
    def __init__(self, grid):
        
        self.blocks = []
        self.cols = []
        self.rows = []
        self.entries = {}
        
        rows   = [[],[],[], [],[],[], [],[],[]]
        cols   = [[],[],[], [],[],[], [],[],[]]
        blocks = [[],[],[], [],[],[], [],[],[]]
        
        for i in range(0,9):
            for j in range(0,9):
                index = (i * 9) + j
                blk = ((i/3) * 3) + (j/3)
                #print i,j,block
                sq = square(i, j, blk, grid[index])
                rows[i].append(sq)
                cols[j].append(sq)
                blocks[blk].append(sq)
                key = str(i) + "," + str(j)
                self.entries[key] = sq
        
        for arr in rows:
            self.rows.append(block(arr))
        
        for arr in cols:
            self.cols.append(block(arr))
        
        for arr in blocks:
            self.blocks.append(block(arr))
        
    def __str__(self):
        out = ""
        for i in range(0,9):
            row = ""
            for j in range(0,9):
                sqr = self.getSquare(i,j)
                n = sqr.definite()
                if n == 0:
                    row += "- "
                else:
                    row += str(n) + " "
                
            out += row
            out += "\n"
        return out
    def getSquare(self, i, j):
        return self.entries[str(i) + "," + str(j)]
    
    def solve(self):
        #print "=========================================="
        changed = 0
        
        for row in self.rows:
            if row.solve():
                changed = True
        for col in self.cols:
            if col.solve():
                changed = True
        for blk in self.blocks:
            if blk.solve():
                changed = True
        
        if changed:
            #pass
            self.solve()
                    
    def printGrid(self):
        print ""
        print str(self)
        
    def getAsArray(self):
        out = []
        for i in range(0,9):
            for j in range(0,9):
                sqr = self.getSquare(i,j)
                n = sqr.definite()
                out += str(n)
        return out
        

class square:
    def __init__(self, row, col, block, definite=0):
        self.row = row
        self.col = col
        self.block = block
        
        if not definite == 0:
            self.possible = [definite]
        else:
            self.possible = [1,2,3,4,5,6,7,8,9]
        
    def __str__(self):
        out = "(%s, %s)[%s]: " % (self.row, self.col, self.block)
        return out + str(self.possible)
            
    def remove(self, number):
        changed = False
        if number in self.possible:
            self.possible.remove(number)
            changed = True
        return changed
        
    def coords(self):
        return "(%s, %s)" % (self.row, self.col)
        
    def definite(self):
        if len(self.possible) > 1:
            return 0
        elif len(self.possible) == 0:
            return -1
        else:
            return self.possible[0]
        
    def getPossibles(self):
        return self.possibles
    def setDefinite(self, number):
        self.possible = [number]

class block:
    def __init__(self, entries = []):
        self.entries = []
        for sq in entries[:9]:
            self.entries.append(sq)
            
    def __str__(self):
        out = ""
        for sq in self.entries:
            out += str(sq.possible)
            out += "\n"
        return out
        
    def cleanup(self):
        changed = False
        for sq in self.entries:
            if not sq.definite() == 0:
                continue
            for other in self.entries:
                if not other == sq: 
                    if sq.remove(other.definite()):
                        changed = True
        if changed:
            self.cleanup()
        return changed
        
    def cleanSeqs(self):
        countmap = {}
        changed = False
        for sq in self.entries:
            poss = sq.possible
            poss.sort()
            key = reduce(lambda x,y: str(x) + "," + str(y), poss, "")[1:]
            if key in countmap.keys():
                countmap[key].append(sq)
            else:
                countmap[key] = [sq]
        
        relevantKeys = [k for k in countmap.keys() if len(k.split(",")) == len(countmap[k])]
        for key in relevantKeys:
            #print key
            for sq in self.entries:
                if not sq in countmap[key]:
                    toRemove = map(int, key.split(","))
                    for i in toRemove:
                        if sq.remove(i):
                            changed = True
        return changed
        
    def resolveSingles(self):
        countMap = {}
        changed = False
        for sq in self.entries:
            for i in sq.possible:
                if i in countMap.keys()   :
                    countMap[i] += 1
                else:
                    countMap[i] = 1
        singles = [x for x in countMap.keys() if (countMap[x] == 1)]
        for sq in self.entries:
            for x in singles:
                if x in sq.possible:
                    for p in [po for po in sq.possible if not po == x]:
                        sq.remove(p)
                        changed = True
        
        return changed
                    
        
       
    def solve(self):
        changed = False
        if self.cleanup():
            changed = True
            
        if self.cleanSeqs():
            changed = True

        if self.resolveSingles():
            changed = True
            
        if changed:
            self.solve()
            
        return changed
        
def solveFile(filename):
    if not path.exists(filename):
        return 1
        
    puzzFile = file(filename)
        
    return 0

def solve(grid):
    g = game(grid)
    g.solve()
    return str(g)
    
if __name__ == '__main__':
    
    if len(sys.argv) >= 2:
        code = solveFile(sys.argv[1])
        sys.exit(code)
    
    f = file("c:\\0\\suduko.txt", 'w')
    sys.stdout = f
    
    
    startGrid =   [9,0,0, 0,3,0, 0,0,0]
    startGrid +=  [3,4,0, 0,0,0, 7,0,5]
    startGrid +=  [0,2,0, 0,1,0, 0,6,0]
    startGrid +=  [5,0,0, 8,0,0, 0,0,6]
    startGrid +=  [4,0,9, 0,0,0, 0,7,0]
    startGrid +=  [0,1,3, 5,7,0, 2,0,0]
    startGrid +=  [0,6,0, 0,0,3, 8,0,4]
    startGrid +=  [0,0,4, 1,6,2, 0,5,0]
    startGrid +=  [0,0,0, 0,0,0, 0,0,0]
            
    #game1 = game(startGrid)
    #game1.printGrid()
    #game1.solve()
    #game1.printGrid()
            
    print "=================================================="
    
    startGrid2 =   [2,0,0, 0,7,1, 0,0,0]
    startGrid2 +=  [0,4,0, 0,0,8, 0,6,0]
    startGrid2 +=  [7,0,0, 0,0,6, 1,0,9]
    startGrid2 +=  [0,0,0, 0,5,0, 0,0,0]
    startGrid2 +=  [0,0,4, 0,1,3, 7,0,6]
    startGrid2 +=  [0,0,0, 0,0,9, 3,0,0]
    startGrid2 +=  [0,9,0, 0,0,7, 6,0,0]
    startGrid2 +=  [5,8,0, 0,6,0, 0,0,1]
    startGrid2 +=  [4,0,0, 9,8,0, 0,0,0]
            
    #game2 = game(startGrid2)
    #game2.printGrid()
    #game2.solve()
    #game2.printGrid()

    print "=================================================="
    
    startGrid3 =   [0,0,6, 0,0,3, 5,0,0]
    startGrid3 +=  [4,3,8, 0,0,0, 0,0,7]
    startGrid3 +=  [0,0,0, 0,7,0, 0,2,0]
    startGrid3 +=  [0,0,5, 0,9,0, 0,0,0]
    startGrid3 +=  [2,0,0, 6,0,1, 8,0,0]
    startGrid3 +=  [6,0,0, 0,0,0, 0,3,0]
    startGrid3 +=  [0,5,4, 0,0,0, 0,0,0]
    startGrid3 +=  [0,0,2, 9,0,0, 0,0,0]
    startGrid3 +=  [3,0,0, 7,5,0, 0,0,8]
            
    #game3 = game(startGrid3)
    #game3.printGrid()
    #game3.solve()
    #game3.printGrid()
    
    #for row in game3.rows:
    #    print row
     
    print "=================================================="
    
    startGrid4 =   [0,0,0, 1,0,0, 7,4,0]
    startGrid4 +=  [0,5,0, 0,9,0, 0,3,2]
    startGrid4 +=  [0,0,6, 7,0,0, 9,0,0]
    startGrid4 +=  [4,0,0, 8,0,0, 0,0,0]
    startGrid4 +=  [0,2,0, 0,0,0, 0,1,0]
    startGrid4 +=  [0,0,0, 0,0,9, 0,0,5]
    startGrid4 +=  [0,0,4, 0,0,7, 3,0,0]
    startGrid4 +=  [7,3,0, 0,2,0, 0,6,0]
    startGrid4 +=  [0,6,5, 0,0,4, 0,0,0] 
            
    #game4 = game(startGrid4)
    #game4.printGrid()
    #game4.solve()
    print solve(startGrid4)
    #game4.printGrid()
    
    
    # arr = []
    # 
    # for col in range(0,9):
        # row  = 0
        # blck = col / 3
        # sq  = square(row, col, blck)
        # arr.append(sq)
        # 
    # arr[0].possible = [1,5,2]
    # arr[1].setDefinite(3)
    # arr[2].setDefinite(8)
    # arr[3].possible = [4,5]
    # arr[4].possible = [1,5]
    # arr[5].possible = [1,9]
    # arr[6].possible = [1,5]
    # arr[7].setDefinite(7)
    # arr[8].setDefinite(6)
    # 
    # block = block(arr)
    # print block
    # 
    # block.cleanSeqs()
    # print block
    # 

