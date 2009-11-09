def is_fifth_power_sum(num):
    digits = [int(x)**5 for x in str(num)]
    return num == sum(digits)

def fifth_power_numbers(max_num):
    for i in xrange(10,max_num):
        if is_fifth_power_sum(i):
            yield i

print sum(fifth_power_numbers(1000000))

