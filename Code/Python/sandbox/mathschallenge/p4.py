out = []

def palin(s):
    lst = list(s)
    lst.reverse()
    
    return s == ''.join(lst)
    
for x in range(100, 1000):
    for y in range(100, 1000):
        prod = x * y
        s = str(prod)
        if palin(s):
            out.append(prod)

out.sort()

print out[-1]
