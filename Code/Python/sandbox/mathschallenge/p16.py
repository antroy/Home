from operator import add

big_number = 2**1000
digits = [int(x) for x in str(big_number)]

ans = reduce(add, digits)

print "Sum of digits in 2**1000 is: %s" % ans