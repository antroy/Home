from zipfile import *
import re

zipfile = ZipFile("channel.zip")
entries = zipfile.infolist()

readme = zipfile.getinfo("readme.txt")

print "Entries: " + str(len(zipfile.namelist()))

#content = zipfile.read("readme.txt")

#print content

#content = zipfile.read("90052.txt")

#print content

#for entry in entries:
#    print entry.filename
    # 
code = "90052"

exp = re.compile(r"^Next nothing is (\d+)$")
set = zipfile.namelist()
comments = []

for i in range(1,1000):
    f = code + ".txt"
    content = zipfile.read(f)
    entry = zipfile.getinfo(f)
    comments.append(entry.comment)
    
    m = exp.match(content)
    
    if not m:
      print f
      print content
      break
    code = m.group(1)
    set.remove(f)
    print i, code, content
    
print "Comments:", ''.join(comments)
# Answer: Hockey
