class Base:
    def __init__(self):
        print "Initializing base"
    def shouldBeImplemented(self):
        raise NotImplementedError
    def hasDefaultImplementation(self):
        print "Wey Hey!"

class A(Base):
    def shouldBeImplemented(self):
        print "Has been implemented!"

class B(Base):
    def __init__(self):
        Base.__init__(self)
        print 'Initializing B'

class C(Base):
    def __init__(self):
        print "Initializing C"
    def hasDefaultImplementation(self):
        print "Boo Hoo!"

base = Base()
print "\n------- A --------"
a = A()
a.shouldBeImplemented()
print "\n------- B --------"
b = B()
b.hasDefaultImplementation()
print "\n------- C --------"
c = C()
c.hasDefaultImplementation()
c.shouldBeImplemented()


