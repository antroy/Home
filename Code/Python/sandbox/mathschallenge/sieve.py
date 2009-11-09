import operator
import math

def sieve_of_eratosthenes(largest):
    current_list = range(2, largest + 1)
    primes = []
    return _sieve_of_eratosthenes(current_list, primes)

def _sieve_of_eratosthenes(current_list, primes):
    while current_list:
        first_prime = current_list[0]
        primes.append(first_prime)
        current_list = remove_multiples(current_list, first_prime)
            
    return primes
        
def remove_multiples(numbers, prime):
    return [n for n in numbers if n % prime != 0]


def numbers(limit, initial=1):
    for i in xrange(initial, limit):
        if i > math.sqrt(limit): break
        yield i

def sieve_of_atkin(limit):
    results = [2,3]
    sieve  =  [False for x in range(0, limit)]

    # put in candidate primes: 
    # integers which have an odd number of representations by certain quadratic forms
    for x in numbers(limit):
        for y in numbers(limit):
            n = (4 * (x**2)) + (y**2)
            if n <= limit and n % 12 in [1, 5]:
                sieve[n] = not sieve[n]

            n = (3 * (x**2)) + (y**2)
            if n <= limit and n % 12 == 7:
                sieve[n] = not sieve[n]

            n = (3 * (x**2)) - (y**2)
            if x > y and n <= limit and n % 12 == 11:
                sieve[n] = not sieve[n]

    # eliminate composites by sieving
    for n in numbers(limit, initial=5):
        if sieve[n]:
            for k in range(n**2, limit, n**2):
                sieve[k] = False
 
    for n in range(5, limit):
        if sieve[n]:
            results.append(n)

    # out = [n for n in range(5, limit) if sieve[n]]

    return results

sieve = sieve_of_atkin

# _______________________________________________________________
def numbers2(limit, initial=1):
    i = initial
    while i <= math.sqrt(limit):
        yield i
        i += 1

def sieve_of_atkin2(limit):
    sieve  =  [False for x in xrange(0, limit)]
    sieve[2] = True
    sieve[3] = True

    # put in candidate primes: 
    # integers which have an odd number of representations by certain quadratic forms
    for x in numbers2(limit):
        for y in numbers2(limit):
            n = (4 * (x**2)) + (y**2)
            if n <= limit and n % 12 in [1, 5]:
                sieve[n] = not sieve[n]

            n = (3 * (x**2)) + (y**2)
            if n <= limit and n % 12 == 7:
                sieve[n] = not sieve[n]

            n = (3 * (x**2)) - (y**2)
            if x > y and n <= limit and n % 12 == 11:
                sieve[n] = not sieve[n]

    # eliminate composites by sieving
    for n in numbers2(limit, initial=2):
        if sieve[n]:
            for k in xrange(n**2, limit, n**2):
                sieve[k] = False
 
    
    out = [n for n in xrange(2, limit) if sieve[n]]

    return out

if __name__ == "__main__":

    assert sieve_of_atkin(100) == sieve_of_atkin2(100)
    assert sieve_of_atkin(100) == sieve_of_eratosthenes(100)

    import timeit
    t = timeit.Timer("sieve_of_atkin2(100000)", "from __main__ import sieve_of_atkin2")
    print "A:", t.timeit(10)

    t = timeit.Timer("sieve_of_atkin(100000)", "from __main__ import sieve_of_atkin")
    print "B:", t.timeit(10)

    #t = timeit.Timer("sieve_of_eratosthenes(100000)", "from __main__ import sieve_of_eratosthenes")
    #print "C:", t.timeit(10)


