############################################################
##                    Filters                           ##
############################################################

filters = {
        r"DIRECT LINE INS.*": "Direct Line Insurance",
        r"SAINSBURY'S S/MKT.*": "Sainsbury's",
        r"SAINSBURYS PFS.*": "Petrol (Sainsbury's)"
        }

categories = {
        r"SAINSBURYS PFS.*": "Transportation: Gas & Oil",
        #r"DIRECT LINE INS.*": "Direct Line Insurance",
        r"SAINSBURY'S S/MKT.*": "Food: Groceries",
        }

############################################################
##                    Converter                           ##
############################################################

import sys, re

filename = sys.argv[1]

class converter (object):
    def __init__(self, filename):
        self.old = open(filename)
        
        new_name = "-new.".join(filename.rsplit(".", 1))
        self.new = open(new_name, "w")
        print "Converted File:", new_name
        self.function_map = {
            "D": self.dateline,
            "P": self.descline
                }

        self.convert()
        self.close()

    def dateline(self, line):
        date = line.split('/')
        newline = "/".join([date[1], date[0], date[2]])
        return [newline]

    def descline(self, line):
        out = []

        for k in filters:
            m = re.match(k, line)
            if m:
                out.append(m.expand(filters[k]))
                break
        else:
            out.append(line)

        for c in categories:
            m = re.match(c, line)
            if m:
                out.append(("L", categories[c]))

        return out

    def defaultline(self, line):
        return [line]

    def convert(self):
        for line in self.old:
            key, value = line[0], line[1:].strip()
            funct = self.function_map.get(key, self.defaultline)

            for new_line in funct(value):
                is_str = isinstance(new_line, str)
                k = key if is_str else new_line[0]
                v = new_line if is_str else new_line[1]

                print >> self.new, "%s%s" % (k, v)
    def close(self):
        self.old.close()
        self.new.close()

converter(filename)

