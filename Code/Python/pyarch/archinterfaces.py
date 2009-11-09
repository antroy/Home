class filetransit:
    def __init__(self, *args, **kw):
        pass
    def upload(self, remotedir, filename):
        pass

class compressor:
    def __init__(self, filelist, tofile):
        self.files = filelist
        self.tofile = tofile
        self.compress()
    def compress(self):
        pass

