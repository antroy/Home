def fib(first=0, second=1, step=1):
    last = first
    next = second
    while True:
        if next % step == 0:
            yield next
        last, next = next, last + next
def add(x, y):
    return x + y
    
def times(x, y):
    return x * y
