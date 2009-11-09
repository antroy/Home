import operator

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

def gcd(a, b):
    if b == 0: return a
    return gcd(b, a % b)

def lcm(a, b):
    return (a * b) / gcd(a,b)

def solve():
    primes = sieve_of_eratosthenes(20)
    others = [x for x in range(1,21) if x not in primes]
    others.sort()
    smallest_contender = reduce(operator.mul, primes)
    
    for x in others:
        if smallest_contender % x:
            smallest_contender = lcm(smallest_contender, x)
    
    return smallest_contender

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print sieve_of_eratosthenes(int(sys.argv[1]))
    else:
        print solve()

