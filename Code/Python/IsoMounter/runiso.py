from subprocess import *
from optparse import OptionParser
import sys, os, ConfigParser, win32com.client, shutil
import win32pipe

ISO = r'"C:\Program Files\MagicDisc\miso.exe"'

def run(command):
    print "&& ", command, " &&"

    p = Popen(command, stdout=PIPE)
    r = p.stdout
    
    #r = win32pipe.popen(command)
    
    output = []
    for line in r:
        output.append(line)

    r.close()

    return output

def shortcut(drive, iso_file, exe, icon):

    parts = os.path.split(iso_file)
    linkname = os.path.splitext(parts[1])[0] + ".lnk"
    link = os.path.join(parts[0], "..", linkname)
    link = os.path.abspath(link)

    if os.path.exists(link):
        print "Shortcut %s already exists!" % link
        return


    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(link)
    shortcut.IconLocation = "%s, 0" % icon
    shortcut.WorkingDirectory = drive 
    shortcut.Targetpath = sys.argv[0]
    shortcut.Arguments = iso_file
    shortcut.save()
    

def exe_and_icon(drive):
    autorun_ini = "%sautorun.inf" % drive
    print "Parsing config: ", autorun_ini
    config = ConfigParser.ConfigParser()
    config.read(autorun_ini)
    exe = "%s%s" % (drive, config.get("autorun", "open"))
    icon = "%s%s" % (drive, config.get("autorun", "icon"))

    return exe, icon
    
def parse_options():
    parser = OptionParser()
    parser.add_option("-i", "--initialise",
                  action="store_true", dest="init", default=False,
                  help="initialize shortcuts for future use.")

    (options, args) = parser.parse_args()
    
    if not args:
        parser.print_help()
        sys.exit(0)

    return options, args[0]


def main():
    options, isopath = parse_options()
    
    #print run(ISO + " NULL -sdrv 1")
    print "Unmounting virtual CD"
    run(ISO + " NULL -umnt 1")
    print "Mounting %s virtual CD" % isopath
    run(ISO + ' NULL -mnt 1 "' + isopath + '"')

    if options.init:
        print "Getting drive letter for vrtual CD"
        lines = run(ISO + " NULL -vlist")
        setup_shortcuts(isopath, lines)

def setup_shortcuts(isopath, lines):
    for line in lines:
        line = line.strip()
        if line.startswith("[1]"):
            drive = "%s:\\" % line[-3]
            print "Virtual drive is mounted at ", drive
            exe, icon = exe_and_icon(drive)
                
            new_icon = os.path.join(os.path.split(isopath)[0], os.path.split(icon)[1])
            if not os.path.exists(new_icon):
                shutil.copy(icon, new_icon)

            shortcut(drive, isopath, exe, new_icon)

if __name__ == "__main__":
    main()


