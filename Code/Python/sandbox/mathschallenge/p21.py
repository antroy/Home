import math

DIV_SUMS = {}

def divisors(number):
    largest_candidate = number / 2
    out = []
    for i in xrange(1, largest_candidate + 1):
        if not number % i:
            out.append(i)
    return out

def init_divisor_sum_map(largest):
    for i in xrange(largest):
        DIV_SUMS[i] = sum_of_divisors(i)

def sum_of_divisors(number):
    if number in DIV_SUMS:
        return DIV_SUMS[number]

    tot = sum(divisors(number))
    DIV_SUMS[number] = tot

    return tot

def amicable(a, b):
    a, b = min(a,b), max(a, b)
    return sum_of_divisors(a) == b and sum_of_divisors(b) == a

def amicable_pairs(largest):
    out = set()
    for i in xrange(largest):
        for j in xrange(largest):
            if i == j:
                continue
            if (min(i,j), max(i,j)) in out:
                continue
            if amicable(i, j):
                out.add((min(i,j), max(i,j)))
    return out


# a = 220
# print "220 factors: ", divisors(a)
# 
# b = 284
# print "Amicable" if amicable(a, b) else "Hostile"

pairs =  amicable_pairs(10000)

flattened = []
map(flattened.extend, pairs)

print "Sum of Amicable Pairs", sum(flattened)



