import webbrowser, os, sys, inspect
from threading import Thread
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

__all__ = ("help",)

class HelpHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        print "PATH: ", self.path
        if self.path.endswith("quit.html"):
            print "Exiting..."
            self.server.exit = True
        else:
            return SimpleHTTPRequestHandler.do_GET(self)

class HelpServer(HTTPServer):
    def server_activate(self):
        print "Activating Server"
        self.exit = False
        HTTPServer.server_activate(self)

    def serve_forever(self):
        while not self.exit:
            self.handle_request()

def help(base_dir, server_class=HelpServer, handler_class=HelpHTTPRequestHandler, port=8000):
    """
    The help function creates an http server, and serves the pages in the 
    directory given by the base_dir parameter. Optional parameters include 
    server_class and handler_class with which you can set custom servers and 
    handlers, and the port parameter if you need to change from the default
    port (8000). 
    
    After starting the server, the page called index.html from your base_dir is opened in
    your web browser.

    """
    os.chdir(base_dir)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    server_thread = Thread(target=httpd.serve_forever)
    server_thread.start()

    webbrowser.open("http://localhost:%d/index.html" % port)

    print """Hit CTRL-Break or CTRL-C to exit server. 
Alternatively go to http://localhost:%d/quit.html to shut down the server""" % port

def main():
    current_dir = os.path.split(sys.argv[0])[0]
    help(current_dir)

if __name__ == "__main__":
    main()
