import sys
from zipcompressor import *
from ftptransit import *
from datetime import date

def backup(*args):
    l = [r'c:\Documents and Settings\John\My Documents']
    zipfile = path.join('d:/My_Documents_Backup', get_qualified_name('John.zip'))
    zipcompressor(l, zipfile)
    
      
def get_qualified_name(name):
    day = date.today()
    timestamp = "%04d-%02d-%02d" % (day.year, day.month, day.day)
    out = ("%s_" + timestamp + "%s") % path.splitext(name)
    return out

if __name__ == "__main__":
    #print get_qualified_name("John.zip")
    backup(sys.argv)

