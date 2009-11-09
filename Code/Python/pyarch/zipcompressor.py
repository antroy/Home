from archinterfaces import compressor
import os, os.path as path
from zipfile import *

class zipcompressor(compressor):
    def compress(self):
        zf = ZipFile(self.tofile, 'w', ZIP_DEFLATED)
        
        for name in self.files:
            if path.isfile(name):
                zf.write(name, transform_filename(name))
            elif path.isdir(name):
                for root, dirs, files in os.walk(name):
                    for f in files:
                        fp = path.join(root, f)
                        zf.write(fp, transform_filename(fp))
                        print transform_filename(fp)
        zf.close()
        print self.files, self.tofile
        
def transform_filename(name):
    drive, p = path.splitdrive(name)
    out = drive[:-1] + 'drive' + p
    
    return out

if __name__ == '__main__':
    l = [r'F:\Perl']
    zipcompressor(l, r'C:\0\pyarch\test.zip')

