def perms(numbs):
    numbs.sort()
    return _perms(numbs)

def _perms(ordered_numbs):
    if len(ordered_numbs) == 1:
        return [ordered_numbs]
    out = []
    for i in ordered_numbs:
        temp_list = []
        temp_list.append(i)
        popped = list(ordered_numbs)
        popped.remove(i)
        # print popped
        tails = _perms(popped)
        for tail in tails:
            # print tail
            out.append([i] + tail)
    return out

def main():
    print perms([1,2,3])

    from time import time
    bef = time()
    print perms(range(7))
    print "Time: %s secs" % (time() - bef)

if __name__ == "__main__":
    main()
