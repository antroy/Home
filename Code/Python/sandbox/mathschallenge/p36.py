def palindromic(num):
    a = list(str(num))
    b = list(a)
    b.reverse()
    return a == b

def decimal_palindromes(max_num):
    for i in xrange(max_num):
        if palindromic(i):
            yield i

def dec_to_bin(num):
    digits = []
    while num > 0:
        digits.append(str(num % 2))
        num = num / 2

    digits.reverse()
    return "".join(digits)

def double_palindromes(max_num):
    for p in decimal_palindromes(max_num):
        if palindromic(dec_to_bin(p)):
            yield p

print sum(double_palindromes(1000000))
