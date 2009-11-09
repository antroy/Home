from archinterfaces import filetransit
from ftplib import FTP

class ftptransit(filetransit):
    def __init__(self, *args, **kw):
        self.host = kw.get('host')
        self.port = int(kw.get('port','21'))
        self.user = kw.get('user', 'anonymous')
        self.pwd = kw.get('pwd', '')
        self.remotedir = kw.get('remotedir', '')

    def upload(self, fromfilename, tofilename):
        
        filehandle = open(fromfilename, 'rb')
         
        try:
            ftp = FTP(self.host, self.user, self.pwd)
            ftp.cwd(self.remotedir)
            command = "STOR %s" % tofilename.strip()
            resp = ftp.storbinary(command, filehandle)
        except:
            print "Problem storing file..."
            return False
        print "Upload successful.", resp
        
        filehandle.close()
        ftp.quit()
        return True
        
if __name__ == '__main__':
    tr = ftptransit(host='mavin', remotedir='xxx', user='ant', pwd='useouszl')
    f = r'C:\0\pyarch\test.zip'
    tr.upload(f, 'uptest.zip ')
    
    
