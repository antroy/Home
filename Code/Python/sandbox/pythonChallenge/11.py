#  http://www.pythonchallenge.com/pc/return/bull.html
#
# a = [1, 11, 21, 1211, 111221, 
#
# len(a[30]) = ?

# http://www.ocf.berkeley.edu/~stoll/answer.html

#a = ['1', '11', '21', '1211', '111221']

# count and parse should be iterating over string not seq.

a = ['1']

def count(seq):
    initial = seq[0]
    count = 1
    out = ''
    for i in range(1,len(seq)):
        if seq[i] == initial:
            count += 1
        else:
            break
    out = str(count) + initial
    return (out, count)

def parse(seq):
    start = 0
    length = len(seq)
    newdigit = ''
    while True:
        x = count(seq[start:])
        newdigit += x[0]
        start += x[1]
        if start >= length:
            break
    return newdigit

current = "1"
for i in range(0,30):
    current = parse(current)

print len(current)

