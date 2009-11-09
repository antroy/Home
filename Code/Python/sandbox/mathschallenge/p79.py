#!/usr/local/bin/python

from __future__ import with_statement

data = set()

with open("p79.dat") as f:
    for line in f:
        if line:
            data.add(line.strip())

print data, len(data)

