from p5 import sieve_of_eratosthenes as sieve
import operator
import math

#primes = sieve(1000000)
#print reduce(operator.add, primes)

def numbers(limit, initial=1):
    for i in range(initial, limit):
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
    return results

if __name__ == "__main__":
    primes = sieve_of_atkin(1000000)
    print len(primes)
    print "10001: " + str(primes[1000])     # 7927
    print sum(primes)
