from operator import mul

class irrational(object):
    def __init__(self, initial=20):
        self.current_digit = initial
        self.content = "".join(map(str, xrange(1, self.current_digit + 1)))

    def digit(self, index):

        if len(self.content) < index:
            self._extend(index)

        return int(self.content[index - 1])

    def _extend(self, min_len):
        while len(self.content) < min_len:
            self.current_digit += 1
            self.content += str(self.current_digit)
    def __str__(self):
        return self.content

x = irrational(initial=1000000)
#print x.content
#print x.digit(9)
#print x.digit(12)
numbers = map(x.digit, [1,10,100,1000,10000,100000,1000000])
print numbers
print reduce(mul, numbers)


