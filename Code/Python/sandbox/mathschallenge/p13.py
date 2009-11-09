from __future__ import with_statement

numbers = []

with open("p13.dat") as f:
    for line in f:
        num_str = line.strip()
        num = long(num_str)
        numbers.append(num)

print  str(sum(numbers))[0:10]


