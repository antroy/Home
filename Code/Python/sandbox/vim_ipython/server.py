
# Copyright (c) 2001-2004 Twisted Matrix Laboratories.
# See LICENSE for details.


from twisted.internet import reactor, protocol


class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""
    
    def __init__(self, pre):
        self.pre = pre

    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        print data, self.pre
        if data.strip() == ":q":
            #print dir(self.transport.reactor)
            self.transport.reactor.stop()
        self.transport.write("OK - " + self.pre)


class EchoFactory(protocol.ServerFactory):
    protocol = Echo
    
    def buildProtocol(self, addr):
        return Echo("BogusPrefix")

def main():
    """This runs the protocol on port 8000"""
    factory = EchoFactory()
    reactor.listenTCP(4321,factory)
    reactor.run()
    print "Ha"
    print "Ho"

if __name__ == '__main__':
    main()

