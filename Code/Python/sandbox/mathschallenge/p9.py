import operator

def isPythagorean(a, b, c):
    if a > b or b > c:
        return False
    return (a ** 2 + b ** 2) == (c ** 2)

total = 1000

def max_a(total):
    return total / 3

def max_b(a, total):
    return (total - a) / 2

def get_c(a, b, total):
    return total - a - b

def pythagorean_triples(total):
    print "finding triples"
    for a in xrange(1, max_a(total) + 1):
        for b in xrange(1, max_b(a, total) + 1):
            c = get_c(a, b, total)
            out =  (a, b, c)
            if isPythagorean(*out):
                yield out

for triple in pythagorean_triples(1000):
    print reduce(operator.mul, triple)

#print isPythagorean(3,4, 5)
