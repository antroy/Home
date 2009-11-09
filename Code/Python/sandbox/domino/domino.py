dominos = [(1,2), (1,3), (1,4), (1,5), (1,6), (2,3), (2,4), (2,5), (2,6),
		(3,4), (3,5), (3,6), (4,5), (4,6), (5,6)]


#slots = [Slot() for i in range(15)]


class Slot(object):
    def __init_(self, domino=None, orientable=None):
        self.orientable = orientable
        self.fill(domino)
        
    def fill(self, domino):
        self.domino = domino

def permutations(items):
    n = len(items)
    
    if n==0:
        yield []
    else:
        for i in xrange(len(items)):
            for cc in permutations(items[:i]+items[i+1:]):
                yield [items[i]]+cc


if __name__ == "__main__":

    count = 0
    
    for perm in permutations(dominos):
        print perm
        count += 1
        #if count >= 10:
        #    break
    print "finished."
    
