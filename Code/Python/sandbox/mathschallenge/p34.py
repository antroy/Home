import operator

def fact(num):
    if num in [0,1]:
        return 1 
    return reduce(operator.mul, range(1,num + 1))

def is_fact_sum(num):
    raw_digits = [int(x) for x in str(num)]
    digits = [fact(x) for x in raw_digits]

    return num == sum(digits)

print is_fact_sum(145)
print is_fact_sum(40585)

def fact_sum_digits(max_num):
    for i in xrange(10, max_num):
        if is_fact_sum(i):
            yield i

print sum(fact_sum_digits(1000000))

