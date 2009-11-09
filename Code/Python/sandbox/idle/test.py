Python 2.4.1 (#65, Mar 30 2005, 09:13:57) [MSC v.1310 32 bit (Intel)] on win32
Type "copyright", "credits" or "license()" for more information.

    ****************************************************************
    Personal firewall software may warn about the connection IDLE
    makes to its subprocess using this computer's internal loopback
    interface.  This connection is not visible on any external
    interface and no data is sent to or received from the Internet.
    ****************************************************************
    
IDLE 1.1.1      
>>> print out

Traceback (most recent call last):
  File "<pyshell#0>", line 1, in -toplevel-
    print out
NameError: name 'out' is not defined
>>> print "out"
out
>>> import os.path as path
>>> path.abspath(".")
'C:\\Python24'
>>> import os
>>> os.listdir()

Traceback (most recent call last):
  File "<pyshell#5>", line 1, in -toplevel-
    os.listdir()
TypeError: listdir() takes exactly 1 argument (0 given)
>>> os.listdir(os.currdir)

Traceback (most recent call last):
  File "<pyshell#6>", line 1, in -toplevel-
    os.listdir(os.currdir)
AttributeError: 'module' object has no attribute 'currdir'
>>> os.listdir(os.curdir)
['DLLs', 'Doc', 'include', 'Lib', 'libs', 'LICENSE.txt', 'msvcp71.dll', 'msvcr71.dll', 'NEWS.txt', 'PIL-wininst.log', 'py.ico', 'pyc.ico', 'python.exe', 'python.exe.manifest', 'pythonw.exe', 'pythonw.exe.manifest', 'README.txt', 'RemovePIL.exe', 'Scripts', 'tcl', 'Tools', 'w9xpopen.exe']
>>> os.chdir("F:\Websites\lordine\html")
>>> l = os.listdir(os.curdir)
>>> html = [x for x in l if x.endswith(".htm")]
>>> print l
['scripts', 'contact.htm', 'index.htm', 'links.htm', 'lodges.htm', 'main.htm', 'map.htm', 'prices.htm', 'site.htm', 'images', 'Photographs']
>>> print html
['contact.htm', 'index.htm', 'links.htm', 'lodges.htm', 'main.htm', 'map.htm', 'prices.htm', 'site.htm']
>>> 
