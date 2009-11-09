from twisted.internet import reactor, protocol
from twisted.internet.protocol import ClientCreator
import sys


class EchoClient(protocol.Protocol):
    """Once connected, send a message, then print the result."""
    
    def __init__(self, code):
        self.code = code

    def connectionMade(self):
        self.transport.write(self.code)
    
    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        print "Server said:", data
        self.transport.loseConnection()
    
    def connectionLost(self, reason):
        print "connection lost"

class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient
    
    def __init__(self, code=""):
        self.code = code

    def buildProtocol(self, addr):
        return EchoClient(self.code)

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed - goodbye!"
        reactor.stop()
    
    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
        reactor.stop()

def send_code(code):
    f = EchoFactory(code)
    conn = reactor.connectTCP("localhost", 4321, f)
    print dir(f)
    reactor.run()

# this connects the protocol to a server runing on port 8000
def main():
   send_code(sys.argv[1])

if __name__ == '__main__':
    main()

