#!/usr/bin/python
from path import path as Path
import sys
import config
import smtplib

class State (object):
    
    jpegs = set()
    details = None
        
    def __init__(self, str_or_folder=''):
        
        if isinstance(str_or_folder, set):
            self.jpegs = str_or_folder
            return
        
        if not isinstance(str_or_folder, Path):
            str_or_folder = Path(str_or_folder)
        
        if not str_or_folder.exists():
            pass
        
        if str_or_folder.isdir():
            self.store(str_or_folder)
        else:
            print "State initializer must be a directory, or a string representation of some data."

    def store(self, root):
        
        out = set()
          
        for f in root.walkfiles():
            if f.splitext()[1] == '.jpg' and not '.thumbs' in f.abspath():
                cann_f = f.abspath()[len(root.abspath()):]
                out.add(cann_f)
        
        self.jpegs = out

    def save(self, datafile):
        print "Saving State to %s" % datafile
        jpeg_strings = (str(x) + '\n' for x in self.jpegs)
        fh = file(datafile, 'w')
        fh.writelines(jpeg_strings)
        fh.close()

    def diff(self, other):
        added = other.jpegs - self.jpegs
        removed = self.jpegs - other.jpegs
        
        return (added, removed)
        
    @staticmethod
    def load(datafile):
        print "Loading from file %s" % datafile
        if not isinstance(datafile, Path):
            datafile = Path(datafile)
        
        out = set()
        
        if datafile.exists():
            fh = file(datafile)
            for line in fh:
                out.add(line.strip())
            fh.close()
                        
            return State(out)
        else:
            print "Path %s does not exist - creating empty state..."
            return State()

    def __str__(self):
        return '\n'.join(self.jpegs)

class MonitorDetails (object):
    def __init__(self, folder="", previous_state="", base_url="", email_list=[], template=""):
        self.folder = folder
        self.base_url = base_url
        self.email_list = email_list
        self.template = template
        self.previous_state = previous_state
        
def message(changes, monitorConf):
    
    changed_folders = {}
    
    for change in changes:
        change = Path(change)
        parent, name = change.splitpath()
        if not changed_folders.has_key(parent):
            changed_folders[parent] = 1
        else:
            changed_folders[parent] = changed_folders[parent] + 1

    gallery_template = "%s (%d photo%s added)"
    
    def plural(v):
        if v is 1: return ''
        else: return "'s"
    
    galleries = [gallery_template % (format_path(k, monitorConf.base_url), v, plural(v)) for k, v in changed_folders.iteritems()]
    
    return monitorConf.template % "\n".join(galleries)

def send_mail(to, message, subject="New Photographs in the Gallery!", from_add="home@antroy.co.uk"):
    to_str = ", ".join(to)
    date_ = datetime.datetime.now()
    datestr = date_.strftime("%a, %d %b %Y, %H:%M:S -0000")
    msg = ("From: %s\r\nTo: %s\r\nDate: %s\r\nSubject: %s\r\n\r\n%s" % (from_add, to_str, datestr, subject, message))

    server = smtplib.SMTP(config.smtp_server)
    server.set_debuglevel(1)
    server.sendmail(from_add, to, msg)
    server.quit()
    
def format_path(filepath, base_url):
    print "fp", filepath
    base = base_url
    folder = filepath.replace('\\', '/')
    if not folder[0] == '/':
        folder = "/" + folder
    
    out = base + folder
    out = out.replace(' ', '%20').replace("'", '%27')
    
    return out
    
def get_recipients(filename):
    fh = open(filename)
    out = [line.strip() for line in fh if line.strip() != '']
    return out

def main():
    for conf in config.monitors:
        print "Loading previous State: "
        last = State.load(conf.previous_state)
        
        print 'Creating current state'
        current = State(Path(conf.folder))
        print "Saving current state"
        current.save(conf.previous_state)
        
        added = last.diff(current)[0]
        
        if len(added) > 0:
            mssg = message(added, conf)
            print mssg
            if isinstance(conf.email_list, str):
                to_addresses = get_recipients(conf.email_list)
            else:
                to_addresses = conf.email_list
            send_mail(to_addresses, mssg)
        else:
            print "No changes this time!"
            
        print "Done"
    
if __name__ == '__main__':
    main()
