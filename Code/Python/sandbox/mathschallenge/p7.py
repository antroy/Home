# Get the answer to p10 first - find out how many primes it generates.
from p10 import sieve_of_atkin

primes = sieve_of_atkin(1000000)

print primes[10000]

