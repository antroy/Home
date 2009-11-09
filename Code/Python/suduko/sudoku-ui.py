from  Tkinter import *
import suduko

win = Tk()

fields = []
solution = []

def handleKeys(evt, entry):
    key = evt.char
    if not key in ["1","2","3","4","5","6","7","8","9"]:
        entry.delete(0,END)

for i in range(0,9):
    for j in range(0,9):
        var = StringVar()
        f = Entry(win, width=1, textvariable=var)
        f.grid(row=i, column=j)
        fields.append((f,var))
        #evt = "<KeyRelease>"
        #f.bind(sequence = evt, func = lambda x: handleKeys(x, f))
   
startGrid2 =   [2,0,0, 0,7,1, 0,0,0]
startGrid2 +=  [0,4,0, 0,0,8, 0,6,0]
startGrid2 +=  [7,0,0, 0,0,6, 1,0,9]
startGrid2 +=  [0,0,0, 0,5,0, 0,0,0]
startGrid2 +=  [0,0,4, 0,1,3, 7,0,6]
startGrid2 +=  [0,0,0, 0,0,9, 3,0,0]
startGrid2 +=  [0,9,0, 0,0,7, 6,0,0]
startGrid2 +=  [5,8,0, 0,6,0, 0,0,1]
startGrid2 +=  [4,0,0, 9,8,0, 0,0,0]

count = 0

for i in startGrid2:
    fields[count][1].set(i)
    count += 1

def convert(x):
    if (x == "" or x == None):
        #print "0"
        return 0
    else:
        #print x
        return int(x)
        
def validate():
    out = []
    try:
        out = [convert(x[1].get()) for x in fields]
    except:
        out = None
    return out

def solve():
    array = validate()
    if array == None:
        print "invalid grid"
        return
    game = suduko.game(array)
    game.solve()
    solution = game.getAsArray()
    count = 0
    for f in [y for (x,y) in fields]:
        f.set(solution[count])
        count += 1

solve = Button(win, text = "Solve", command = solve)
solve.grid(row=10, column=0, columnspan=9)
        
win.mainloop()
