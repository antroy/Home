import sys
from zipcompressor import *
from ftptransit import *
from datetime import date

def backup(*args):
    l = [r'D:\Helen']
    zipfile = path.join('Z:/Data', get_qualified_name('Helen.zip'))
    zipcompressor(l, zipfile)
    
    #tr = ftptransit(host='mavin', remotedir='', user='backup', pwd='backup')
    #tr.upload(zipfile, get_qualified_name('Helen.zip'))
        
def get_qualified_name(name):
    dayint = date.today().weekday()
    day = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][dayint]
    out = ("%s-" + day + "%s") % path.splitext(name)
    return out

if __name__ == "__main__":
    backup(sys.argv)

