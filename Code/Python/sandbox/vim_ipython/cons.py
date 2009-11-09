import sys, threading
from IPython.Shell import *#IPShellEmbed
    

from twisted.internet import reactor, protocol


class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""
    
    def __init__(self, shell):
        self.shell = shell

    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        try:
            if data.strip() == ":q":
                self.transport.reactor.stop()
            
            print data
            self.shell.IP.input_hist_raw.append('%s\n' % data)
            self.shell.IP.runsource(data)
            self.transport.write("OK")
        except:
            self.transport.write("Failed!")


class EchoFactory(protocol.ServerFactory):
    def __init__(self, shell):
        self.shell = shell

    def buildProtocol(self, addr):
        return Echo(self.shell)

def get_shell_runner(shell):
    def shell_runner():
        shell(header='Vim Interactor')
        print dir(shell)
    return shell_runner

ipshell = IPShellEmbed()
#ipshell(header='Vim Interactor')


#for i in range(10):
#    for j in range(5):
#        ipshell.IP.runsource("%s * %s\n" % (i, j))

t = threading.Thread(target=get_shell_runner(ipshell))
t.start()

data = """8 * 9 """

ipshell.IP.input_hist.append(data)
ipshell.IP.runsource(data)
#
#factory = EchoFactory(ipshell)
#reactor.listenTCP(4321, factory)
#reactor.run()
#ipshell.IP.runsource("print Hello Dudes!")



