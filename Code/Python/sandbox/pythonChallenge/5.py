from urllib import *
import re
import sys
import string

code = "46059"
if len(sys.argv) > 1:
    code = sys.argv[1]
exp = re.compile(r"(.*)and the next nothing is (\d+)(.*)")
set = [code]

for i in range(1,500):
    url = "http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=%s" % code
    u = urlopen(url)
    page = string.replace(u.read(), "\n", "")
    u.close()
    m = exp.search(page)
    
    if not m:
        print url
        print page
        break
    code = m.group(2)
    remainder = m.group(1).strip() + m.group(3).strip()

    print str(i),

    set.append(code)
    
    if not remainder == "":
        print "Odd Message: " , page
        result = string.lower(raw_input("Continue? [Y, N, number]"))
        if result == "y":
            pass
        elif result == "n":
            break
        else:
            print code
            code = result
            set.append(code)
    print code
    
out = reduce(lambda x,y: x+y, set)
print ""
print out
