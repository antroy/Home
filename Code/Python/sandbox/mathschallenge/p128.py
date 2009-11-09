
class HexCell(object):
    __slots__ = 'n', 'ne', 'se', 's', 'sw', 'nw', 'value'
    def __init__(self, value):
        self.value = value
        self.n, self.ne, self.se, self.s, self.sw, self.nw = None, None, None, None, None, None

    def __str__(self):
        return "%s [%s,%s,%s,%s,%s,%s]" % (str(self.value), self.n, self.ne, self.se, self.s, self.sw, self.nw)


x = HexCell(1)
y = HexCell(2)
x.n = y

print x
