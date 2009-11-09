import sieve

def get_rotations(number):
    digits = list(str(number))
    out = set()

    for i in range(len(digits)):
        perm = digits[i:]
        perm.extend(digits[:i])
        out.add(int("".join(perm)))

    return out

def prime_filter(primes):
    last = len(primes)
    i = 0
    while i < last:
        to_remove = yield primes[i]
        i += 1
        if to_remove:
            last -= (len(to_remove) )
            i -= 1
            for entry in to_remove:
                primes.remove(entry)

def get_circular_primes(primes):
    circular = set()
    prime_fil = prime_filter(primes)

    prime = prime_fil.next()

    try:
        while prime:
            rots = get_rotations(prime)
            cont = False
            for x in rots:
                if x not in primes: 
                    cont = True
                    break
            if cont: 
                prime = prime_fil.next()
                continue
    
            circular.update(rots)
            prime = prime_fil.send(rots)
    except StopIteration:
        pass
    return circular

def main():
    primes = sieve.sieve(1000000)
    circular = get_circular_primes(primes)
    print "Answer", (circular), len(circular)


if __name__ == "__main__":
    import datetime
    
    import psyco
    psyco.full()
    
    now = datetime.datetime.now()
    main()
    print "Time taken: ", (datetime.datetime.now() - now)

