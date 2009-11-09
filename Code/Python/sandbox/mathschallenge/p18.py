#!/usr/local/bin/python
from __future__ import with_statement

def parse(line):
    if not line or len(line.strip()) == 0:
        return None

    return map(int, line.split(" "))


def reduce(triangle):
    red_row = triangle[-2]
    bottom = triangle[-1]
    
    for i, e in enumerate(red_row):
        red_row[i] = e + max(bottom[i], bottom[i + 1])                

    triangle.pop()

def reduce_all_the_way(triangle):
    while len(triangle) > 1:
        reduce(triangle)
    return triangle[0][0]

def get_data(filename):
    data = []
    with open(filename) as f:
        for line in f:
            layer = parse(line)
            if layer:
                data.append(layer)
    return data

if __name__ == "__main__":

    data = get_data("p18.dat")
    print "Result:", reduce_all_the_way(data)
    print 
    small = [[3],[7,5],[2,4,6],[8,5,9,3]]
    print "Small:", reduce_all_the_way(small)
    
