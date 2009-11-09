import mc

sum = 0

for i in mc.fib(step=2):
    if i >= 1000000:
        break
    sum += i

print sum
