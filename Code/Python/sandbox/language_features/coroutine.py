def gen_test(): 
    out = 0
    for x in range(10):
        val = (yield out)
        out += (1 if not val else val)

print "Run through all:"

#for x in gen_test():
#    print x

print "Run through each in turn, doing a send sometimes:"

gen = gen_test()

print "N:", gen.next()
print "N:", gen.next()
print "S:", gen.send(10)
print "N:", gen.next()
print "S:", gen.send(3)
print "N:", gen.next()


