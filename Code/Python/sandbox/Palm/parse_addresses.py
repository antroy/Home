from __future__ import with_statement
import sys, struct

def read_cstring(fh):
    length = read_format(fh, "b")[0]

    print "LENGTH:", length

    if not length:
        return ""

    if length == 255:
        length = read_format(fh, "h")[0]

    print "LENGTH:", length

    out = read_format(fh, "%ds" % length)

    return out

def read_format(fh, format):
    byte_length = struct.calcsize(format)
    bytes = fh.read(byte_length)

    return struct.unpack(format, bytes)

def eat_blanks(fh):
    while True:
        posn = fh.tell()
        b = read_format(fh, "b")[0]
        if b != 0:
            print "Val: ", b
            fh.seek(posn)
            break

def chomp(fh, num):
    read_format(fh, "%db" % num)

def main():
    filename = sys.argv[1]
    
    out = {}
    
    with open(filename, "rb") as fh:
        out['version_tag'] = read_format(fh, "4B")
        out['db_name'] = read_cstring(fh)
        read_format(fh, "8b")
        eat_blanks(fh)
        chomp(fh, 2)
        eat_blanks(fh)
        out['db_filename'] = read_cstring(fh)

    
    print out

if __name__ == "__main__":
    main()


