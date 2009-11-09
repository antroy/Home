import mc
first = 0
next = 1

posn = 1

while len(str(next)) < 1000:
    first, next = next, next + first
    posn += 1

print "F%s = %s" % (posn, next)
