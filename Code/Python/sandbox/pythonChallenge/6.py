from pickle import *
f = file("banner.p")
v = load(f)

for x in v:
    s = []
    for tup in x:
        s.append(tup[1]*tup[0])
    print ''.join(s)
    
