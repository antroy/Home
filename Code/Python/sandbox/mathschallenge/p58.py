import  math, sieve

PRIMES = sieve.sieve(10000000)

def add_layer(spiral):
    """Add a layer to the spiral, and return a pair: (prime_count, total, side_len) of the stats for the diagonals. """
    if not len(spiral):
        spiral.append(1)
        return (0, 1, 1)

    layer_size = int(math.sqrt(len(spiral)))
    side_len = layer_size + 1
    extra = range(len(spiral) + 1, len(spiral) + 1 + side_len * 4)
    diagonals = extra[side_len - 1::side_len]
    prime_diagonals = [x for x in diagonals if x in PRIMES]
    print prime_diagonals

    spiral.extend(extra)

    return (len(prime_diagonals), len(diagonals), side_len)

if __name__ == "__main__":
    spiral = [1]
    primes, total = 0, 0
    while True:
        prime_extra, total_extra, side_len = add_layer(spiral)
        primes += prime_extra
        total += total_extra
        ratio = float(primes) / float(total)
        print "Ratio: %s:%s = %s" % (primes, total, ratio)
        if ratio < 0.1:
            print "** Side Length: ", side_len, "**"
            break
