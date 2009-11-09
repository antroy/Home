import sieve, math

number = 317584931803

primes = sieve.sieve(int(math.sqrt(number)))

def get_largest_prime_divisor():
    for i in primes[::-1]:
        if not number % i:
            return i


if __name__ == "__main__":
    print "Largest = ", get_largest_prime_divisor()

