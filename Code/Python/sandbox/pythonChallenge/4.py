import re
out = ""

p = re.compile(r"(?<![A-Z])[A-Z]{3}([a-z])[A-Z]{3}(?![A-Z])")

f = file("data.txt")

for line in f:
    m = p.search(line)
    if m:
        out += m.group(1)
print out
