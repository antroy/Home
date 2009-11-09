import sys
from zipcompressor import *
from ftptransit import *
from optparse import OptionParser
from optparse import Values
from datetime import date

class backup:
    
    def __init__(self):
        self.opts, self.args = self.getopts()
        if (not self.valid(self.opts)): return
        
        zipfile = os.tmpfile()
        zipcompressor(self.args, zipfile)
        
        tr = ftptransit(host=self.opts.host, remotedir=self.opts.remotedir,
                        user=self.opts.user, pwd=self.opts.pwd)
        tr.upload(zipfile, self.get_qualified_name(self.opts.zipname))
        
    def get_qualified_name(self, name):
        dayint = date.today().weekday()
        day = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][dayint]
        out = ("%s-" + day + "%s") % path.splitext(name)
        return out
        
    def getopts(self):
        parser = OptionParser()
        parser.set_defaults(zipname="archive", tempfile="pyarch-temp")
        parser.add_option("-s", "--host",  dest="host",
                          help="Upload Host")
        parser.add_option("-p", "--port", dest="port", type="int",
                          help="Upload Port")
        parser.add_option("-d", "--remotedir",  dest="remotedir",
                          help="Upload directory.")
        parser.add_option("-u", "--user", dest="user",
                          help="Upload user name.")
        parser.add_option("-q", "--pass",  dest="pwd",
                          help="Upload password")
        parser.add_option("-n", "--zipname", dest="zipname",
                          help="Remote filename (before qualification)")
        parser.add_option("-t", "--tempfile",  dest="tempfile",
                          help="Temporary file name")
        parser.add_option("-c", "--config",  dest="config",
                          help="configuration file")
                         
        return parser.parse_args()
        
    def valid(self, opts):
        print opts
        
        required_list = [opts[x] for x in opts.keys() if x != 'config']
        print required_list
        
        def and_f(a, b): return a and b
        
        out = reduce(and_f, required_list)
        
        return out

        
backup()

