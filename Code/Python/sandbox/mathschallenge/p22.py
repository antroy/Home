#!/usr/local/bin/python
letters = "abcdefghijklmnopqrstuvwxyz"
lettermap = dict([(lett, i + 1) for i, lett in enumerate(letters)])

print lettermap

def name_value(vals):
    print vals
    i, name = vals
    
    position = (i + 1)
    seq = map(lambda a: lettermap[a.lower()], name)
    value = sum(seq)
    
    print position, seq
    
    return position * value


names = None

data = open("p22.dat").read().strip()
data = "[%s]" % data
names = eval(data)
names.sort()
    
print name_value((937, "COLIN"))

print sum(map(name_value, enumerate(names)))

