import sys, threading
from IPython.genutils import Term
from IPython.Shell import *#IPShellEmbed
    
def get_shell_runner(shell):
    def shell_runner():
        shell(header='Vim Interactor')
        print dir(shell)
    return shell_runner

ipshell = IPShellEmbed()
#ipshell = MTInteractiveShell("Bob")
t = threading.Thread(target=get_shell_runner(ipshell))
t.start()

#Term.cout.write("Fred\n")
line = """x = 2 * 3
print x
"""

ip = ipshell.IP

#print dir(ipshell.IP)
#ipshell.IP.input_hist_raw.append('%s\n' % line)
#ip.input_hist_raw[-1] += '%s\n' % line
#ip.runlines(line)
#ip.raw_input()
#ipshell.IP.push(line)
#sys.stdin.write("2 * 8\n")
ip.process_input("2*3")
