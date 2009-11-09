
def odd(num):
    return (3 * num) + 1
    
def even(num):
    return num / 2

def next(num):
    if num % 2 == 0:
        return even(num)
    else:
        return odd(num)

def get_seq(num):
    out = [num]

    while out[-1] > 1:
        out.append(next(out[-1]))

    return out

def get_longest_seq(start_limit):
    current_seq = []

    for i in xrange(1, start_limit):
        seq = get_seq(i)
        if len(seq) > len(current_seq):
            current_seq = seq

    return current_seq



if __name__ == "__main__":
    seq = get_longest_seq(1000000)
    print "Start: %s; Length: %s" % (seq[0], len(seq))

