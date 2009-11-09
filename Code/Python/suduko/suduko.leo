<?xml version="1.0" encoding="UTF-8"?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="0" clone_windows="0"/>
<globals body_outline_ratio="0.5">
	<global_window_position top="20" left="20" height="600" width="800"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="antroy.20050703104813" a="E"><vh>NewHeadline</vh>
<v t="antroy.20050705212224" a="E"><vh>F:/Python/suduko/suduko.py</vh>
<v t="antroy.20050705212224.1"><vh>&lt;&lt; suduko declarations &gt;&gt;</vh></v>
<v t="antroy.20050705212224.2" a="E"><vh>class game</vh>
<v t="antroy.20050705212224.3"><vh>__init__</vh></v>
<v t="antroy.20050705212224.4"><vh>getSquare</vh></v>
<v t="antroy.20050705212224.5"><vh>solve</vh></v>
<v t="antroy.20050705212224.6"><vh>printGrid</vh></v>
</v>
<v t="antroy.20050705212224.7" a="E"><vh>class square</vh>
<v t="antroy.20050705212224.8"><vh>__init__</vh></v>
<v t="antroy.20050705212224.9"><vh>__str__</vh></v>
<v t="antroy.20050705212224.10"><vh>remove</vh></v>
<v t="antroy.20050705212224.11"><vh>coords</vh></v>
<v t="antroy.20050705212224.12"><vh>definite</vh></v>
<v t="antroy.20050705212224.13"><vh>getPossibles</vh></v>
<v t="antroy.20050705212224.14"><vh>setDefinite</vh></v>
</v>
<v t="antroy.20050705212224.15" a="E"><vh>class block</vh>
<v t="antroy.20050705212224.16"><vh>__init__</vh></v>
<v t="antroy.20050705212224.17"><vh>__str__</vh></v>
<v t="antroy.20050705212224.18"><vh>cleanup</vh></v>
<v t="antroy.20050705212224.19"><vh>cleanSeqs</vh></v>
<v t="antroy.20050705212224.20"><vh>resolveSingles</vh></v>
<v t="antroy.20050705212224.21" a="TV"><vh>solve</vh></v>
</v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="antroy.20050703104813"></t>
<t tx="antroy.20050705212224">@ignore
@root-code suduko.py
@language python
&lt;&lt; suduko declarations &gt;&gt;
&lt;&lt; suduko methods &gt;&gt;

        
# 
# startGrid =   [9,0,0, 0,3,0, 0,0,0]
# startGrid +=  [3,4,0, 0,0,0, 7,0,5]
# startGrid +=  [0,2,0, 0,1,0, 0,6,0]
# startGrid +=  [5,0,0, 8,0,0, 0,0,6]
# startGrid +=  [4,0,9, 0,0,0, 0,7,0]
# startGrid +=  [0,1,3, 5,7,0, 2,0,0]
# startGrid +=  [0,6,0, 0,0,3, 8,0,4]
# startGrid +=  [0,0,4, 1,6,2, 0,5,0]
# startGrid +=  [0,0,0, 0,0,0, 0,0,0]
#         
# game = game(startGrid)
# game.printGrid()
# game.eliminate()
# game.printGrid()
#         

startGrid =   [9,0,0, 0,3,0, 0,0,0]
startGrid +=  [3,4,0, 0,0,0, 7,0,5]
startGrid +=  [0,2,0, 0,1,0, 0,6,0]
startGrid +=  [5,0,0, 8,0,0, 0,0,6]
startGrid +=  [4,0,9, 0,0,0, 0,7,0]
startGrid +=  [0,1,3, 5,7,0, 2,0,0]
startGrid +=  [0,6,0, 0,0,3, 8,0,4]
startGrid +=  [0,0,4, 1,6,2, 0,5,0]
startGrid +=  [0,0,0, 0,0,0, 0,0,0]
        
# game = game(startGrid)
# game.printGrid()
# game.solve()
# game.printGrid()
        
arr = []

for col in range(0,9):
    row  = 0
    blck = col / 3
    sq  = square(row, col, blck)
    arr.append(sq)
    
arr[0].setDefinite(5)
arr[1].setDefinite(3)
arr[2].setDefinite(8)
arr[3].possible = [4,5]
arr[4].possible = [1,5]
arr[5].possible = [1,9]
arr[6].possible = [1,5,2]
arr[7].setDefinite(7)
arr[8].setDefinite(6)

block = block(arr)
print block

block.resolveSingles()
print block


</t>
<t tx="antroy.20050705212224.1">@code

#:folding=indent:collapseFolds=2:
import sys

f = file("c:\\0\\suduko.txt", 'w')

sys.stdout = f

</t>
<t tx="antroy.20050705212224.2">&lt;&lt; suduko methods &gt;&gt;=

class game:
	&lt;&lt; class game methods &gt;&gt;

</t>
<t tx="antroy.20050705212224.3">&lt;&lt; class game methods &gt;&gt;=

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
</t>
<t tx="antroy.20050705212224.4">&lt;&lt; class game methods &gt;&gt;=

def getSquare(self, i, j):
    return self.entries[str(i) + "," + str(j)]
</t>
<t tx="antroy.20050705212224.5">&lt;&lt; class game methods &gt;&gt;=

def solve(self):
    print "=========================================="
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
</t>
<t tx="antroy.20050705212224.6">&lt;&lt; class game methods &gt;&gt;=

def printGrid(self):
    print ""
    for i in range(0,9):
        row = ""
        for j in range(0,9):
            sqr = self.getSquare(i,j)
            n = sqr.definite()
            if n == 0:
                row += "_ "
            else:
                row += str(n) + " "
            
        print row
    print ""
</t>
<t tx="antroy.20050705212224.7">&lt;&lt; suduko methods &gt;&gt;=



class square:
	&lt;&lt; class square methods &gt;&gt;

</t>
<t tx="antroy.20050705212224.8">&lt;&lt; class square methods &gt;&gt;=

def __init__(self, row, col, block, definite=0):
    self.row = row
    self.col = col
    self.block = block
    
    if not definite == 0:
        self.possible = [definite]
    else:
        self.possible = [1,2,3,4,5,6,7,8,9]
</t>
<t tx="antroy.20050705212224.9">&lt;&lt; class square methods &gt;&gt;=

def __str__(self):
    out = "(%s, %s)[%s]: " % (self.row, self.col, self.block)
    return out + str(self.possible)
</t>
<t tx="antroy.20050705212224.10">&lt;&lt; class square methods &gt;&gt;=

def remove(self, number):
    changed = False
    if number in self.possible:
        self.possible.remove(number)
        changed = True
    return changed
</t>
<t tx="antroy.20050705212224.11">&lt;&lt; class square methods &gt;&gt;=

def coords(self):
    return "(%s, %s)" % (self.row, self.col)
</t>
<t tx="antroy.20050705212224.12">&lt;&lt; class square methods &gt;&gt;=

def definite(self):
    if len(self.possible) &gt; 1:
        return 0
    elif len(self.possible) == 0:
        return -1
    else:
        return self.possible[0]
</t>
<t tx="antroy.20050705212224.13">&lt;&lt; class square methods &gt;&gt;=

def getPossibles(self):
    return self.possibles
</t>
<t tx="antroy.20050705212224.14">&lt;&lt; class square methods &gt;&gt;=

def setDefinite(self, number):
    self.possible = [number]
</t>
<t tx="antroy.20050705212224.15">&lt;&lt; suduko methods &gt;&gt;=


class block:
	&lt;&lt; class block methods &gt;&gt;

</t>
<t tx="antroy.20050705212224.16">&lt;&lt; class block methods &gt;&gt;=

def __init__(self, entries = []):
    self.entries = []
    for sq in entries[:9]:
        self.entries.append(sq)
</t>
<t tx="antroy.20050705212224.17">&lt;&lt; class block methods &gt;&gt;=

def __str__(self):
    out = ""
    for sq in self.entries:
        out += str(sq.possible)
        out += "\n"
    return out
</t>
<t tx="antroy.20050705212224.18">&lt;&lt; class block methods &gt;&gt;=

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
</t>
<t tx="antroy.20050705212224.19">&lt;&lt; class block methods &gt;&gt;=

def cleanSeqs(self):
    countmap = {}
    for sq in self.entries:
        poss = sq.possibile.sort()
        if poss in countmap:
            countmap[poss] += 1
        else:
            countmap[poss] = poss
            
    for key in keys(countmap):
        if len(key) == countmap[key]:
            for sq in self.entries:
                if sq.possibile.sort() == key:
                    continue
                else:
                    for i in key:
                        sq.remove(i)
</t>
<t tx="antroy.20050705212224.20">&lt;&lt; class block methods &gt;&gt;=

    # map arrays to count
    # if  len(elmnts) == count:
    #     remove elements from all other squares.
    
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
</t>
<t tx="antroy.20050705212224.21">&lt;&lt; class block methods &gt;&gt;=

def solve(self):
    return self.cleanup()
</t>
</tnodes>
</leo_file>
