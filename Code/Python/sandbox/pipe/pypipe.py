#!/usr/bin/python
import sys


def suck_input():
    lines = []
    source = sys.stdin

    while True:
        data = source.read(1024)
        lines.append(data)
        if not data:
            break

    return ''.join(lines)

def main(out_f):
    text = suck_input()
    out_handle = open(out_f, 'w')
    out_handle.write(text)

    out_handle.close()

if __name__ == "__main__":
    out_f = sys.argv[1]
    main(out_f)


