import os, sys, ftplib, re

class File(object):
    def __init__(self, filename, isdir=False):
        self.filename = filename
        self.isdir = isdir

    def __str__(self):
        return self.filename

    def __hash__(self):
        return hash(self.filename)

    def __eq__(self, other):
        return type(self) == type(other) and self.filename == other.filename

class FSFS(object):
    def __init__(self, basedir):
        self.basedir = basedir

    def file(self, path, mode):
        return open(path, mode)

    def cd(self, path):
        os.chdir(path)

    def list(self, dir):
        dir = os.path.join(self.basedir, dir)
        names =  os.listdir(dir)
        curdir = os.getcwd()
        os.chdir(dir)
        out = [File(f, os.path.isdir(f)) for f in names]
        os.chdir(curdir)
        return out

class FTP_FS(object): 
    def __init__(self, basedir, host, user, passwd, port=None):
        if port:
            self.client = ftplib.FTP()
            self.client.connect(host, port)
            self.client.login(user, passwd)
        else:
            self.client = ftplib.FTP(host, user, passwd)
        self.basedir = basedir

    def file(self, path, mode):
        pass

    def cd(self, path):
        self.client.cwd(path)

    def list(self, dir):
        dir = os.path.join(self.basedir, dir)
        lines = []
        def concat(x):
            lines.append(x)

        self.client.dir(dir, concat)
        
        parts = [re.split("\\s+", line, 9) for line in lines]
        out = [File(part[8], part[0].startswith("d")) for part in parts]
        return out

class SynchRight(object):
    """Synchronise from left to right. i.e. assume that left folder is correct, 
    and copy files right, and delete excess files from right."""
    def __init__(self, left_fs, right_fs):
        self.left = left_fs
        self.right = right_fs

    def sync(self, left_path=".", right_path="."):
        files_l = set(self.left.list(left_path))
        files_r = set(self.right.list(right_path))
        
        to_copy = files_l - files_r
        to_delete = files_r - files_l

        for f in to_copy:
            if f.isdir:
                self.right.mkdir(f)
                self.sync(os.path.join(left_path, f), os.path.join(left_path, f))
            else:
                print "Copy", f, "from", left_path, "to", right_path

        for f in to_delete:
            if f.isdir:
                self.right.rmdir(f)
            else:
                print "Delete", f, "from", right_path
                # self.right.delete(f)

        print "Copy ", map(str, to_copy), "to", right_path
        print "Delete ", map(str, to_delete), "from", right_path


if __name__ == "__main__":
    # fs = FTP_FS("/htdocs/photos", "ftp.plus.net", "antroy", "requiner")

    # for line in fs.list(""):
    #     print line, line.isdir
    # 
    # fsfs = FSFS()

    # for line in fsfs.list("/home/ant/0"):
    #     print line

    fs_l = FSFS("/home/ant/0/testsync/a")
    fs_r = FSFS("/home/ant/0/testsync/b")

    sync = SynchRight(fs_l, fs_r)
    sync.sync()


