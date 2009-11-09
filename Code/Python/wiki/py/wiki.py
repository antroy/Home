import os, os.path as path, sys, adapter, logging
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

logfile = "wiki.log"
loglevel = logging.DEBUG

try:
    import config
    logfile = config.logfile
    loglevel = config.loglevel
except:
    pass
    
logging.basicConfig(level=loglevel,
        format='%(name)-12s: %(asctime)s %(levelname)s %(message)s',
        filename=logfile,
        filemode='w')
    
logging.debug('Initializing logging...')
LOG = logging.getLogger('wiki-handler')


class WikiServer(HTTPServer):
    def serve_forever(self):
        """Handle one request at a time until server_on is set to False."""
        self.server_on = True
        
        while self.server_on:
            self.handle_request()
    def server_shutdown(self):
        self.server_on = False

class Handler(BaseHTTPRequestHandler):
    adapter = None
    
    def do_GET(self):
        self.get_adapter().do_get()
    
    def do_POST(self):
        self.get_adapter().do_post()
            
    def get_adapter(self):
        if self.adapter == None:
            self.adapter = BaseHTTPRequestAdapter(self)
            
        return self.adapter
            
class BaseHTTPRequestAdapter(adapter.RequestInterface):
    def __init__(self, handler):
        self.handler = handler
        adapter.wiki_dir = path.join(curdir, "data", "wiki")
        adapter.static_dir = path.join(curdir, "data", "static")
        adapter.template_dir = path.join(curdir, "templates")
        LOG.debug("Wiki-Dir: " + adapter.wiki_dir)
        LOG.debug("Static-Dir: " + adapter.static_dir)
        LOG.debug("Template-Dir: " + adapter.template_dir)

    def get_name(self):
        return "sa_wiki"

    def send_error(self, resp_code, message):
        self.handler.send_error(resp_code, message)
        
    def send_response(self,  content, content_type='text/html', resp_code=200, headers=[]):
        self.handler.send_response(resp_code)
        self.handler.send_header('Content-type', content_type)
        for name, value in headers:
            self.handler.send_header(name, value)
        self.handler.end_headers()
        self.handler.wfile.write(content)
    
    def get_header(self, header):
        return self.handler.headers.getheader(header)
    
    def get_path(self):
        return self.handler.path
        
    def get_context_path(self):
        return '/'
        
    def redirect(self, pth):
        self.handler.path = pth
        self.do_get()
        
    def read_from_client(self, bytes):
        content = self.handler.rfile.read(bytes)
        return content
        
    def shutdown(self):
        print "Closing Server"
        self.send_response("<html><body><h1>Shutting down server!</h1></body></html>")
        self.handler.server.server_shutdown()
        
def main():
    port = 1234
    args = sys.argv[1:]
    print args
    if len(args) > 1:
        if args[0] == '-p':
            port = int(args[1])
    
    try:
        server = WikiServer(('', port), Handler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()
