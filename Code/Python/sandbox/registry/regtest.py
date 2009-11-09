from _winreg import *


def subkeys(key):
    info = QueryInfoKey(key)
    subs = [EnumKey(key, i) for i in range(info[0])] 
    out = [(name, OpenKey(key, name)) for name in subs]

    return dict(out)

def values(key):
    info = QueryInfoKey(key)
    out = [EnumValue(key, i) for i in range(info[1])]

    return out

def add_to_context(name, command):
    key_path = "*\shell\%s\command" % name
    cmd = CreateKey(HKEY_CLASSES_ROOT, key_path)
    SetValueEx(cmd, "", 0, REG_SZ, command)

def remove_from_context(name, root=None):
    if not root:
        root = OpenKey(HKEY_CLASSES_ROOT, "*\shell", 0, KEY_ALL_ACCESS)
    
    to_remove = OpenKey(root, name, 0, KEY_ALL_ACCESS)
    
    info = QueryInfoKey(to_remove)
    for i in range(info[0]):
        remove_from_context(EnumKey(to_remove, i), to_remove)
        
    DeleteKey(root, name)

def test():
    subs = subkeys(shell)

    print subs

    shrinkk = subkeys(subs["shrink"])

    print values(shrinkk['command'])

#add_to_context("bogus", "notepad")

remove_from_context('bogus')

#shell = OpenKey(HKEY_CLASSES_ROOT, "*\shell\UliPad\command")
#print values(shell)



