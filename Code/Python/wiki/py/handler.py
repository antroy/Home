# :wrap=soft:maxLineLen=100:
# This file should contain classes for use with mod_python.

from mod_python import apache
import adapter as adptr, logging, os.path as path

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

def handler(req):
    code = apache.DECLINED
    adptr.wiki_dir = req.get_options()['wikiDir']
    adptr.static_dir = req.get_options()['staticDir']
    adptr.template_dir = req.get_options()['templateDir']
    
    LOG.debug("Wiki-Dir: " + adptr.wiki_dir)
    LOG.debug("Static-Dir: " + adptr.static_dir)
    LOG.debug("Template-Dir: " + adptr.template_dir)
    
    LOG.debug("""path_info: %s
        args: %s
        parsed_uri: %s
        uri: %s
        filename: %s
        unparsed_uri: %s""" % (req.path_info, req.args, req.parsed_uri, req.uri, req.filename, req.unparsed_uri))

    adapter = ModPythonRequestAdapter(req)
    
    if req.method == "POST":
        LOG.debug("POST Request")
        code = adapter.do_post()
    elif req.method == "GET":
        LOG.debug("GET Request")
        code = adapter.do_get()
    
    LOG.debug("Return Code: %s" % code)
        
    if code == 0:
        return apache.OK
    elif code == 1:
        return apache.DECLINED
    else:
        return code

class ModPythonRequestAdapter(adptr.RequestInterface):
    def __init__(self, req):
        self.req = req
        
    def get_name(self):
        return "mod_python"    


    """
    This method should send an error back to the client.
    """
    def send_error(self, resp_code, message):
        return resp_code
        
    """
    This method should send a response back to the client - typically an HTML page.
    """
    def send_response(self,  content, content_type='text/html', resp_code='200', headers=[]):
        # Append Headers
        self.req.content_type = content_type
        for name, value in headers:
            self.req.headers_out[name] = value
            
        self.req.write(content)
        return 200
    
    """
    This method retrieves the named header from the request.
    """
    def get_header(self, header):
        return self.req.headers_in[header]

    """
    This method should read post data as sent from the client.
    """
    def read_from_client(self, bytes):
        content = self.req.read(bytes)
        return content

    """
    This method should retrieve the current path from the request.
    """
    def get_path(self):
        out = self.req.path_info
        args = self.req.args
        if args:
            out = out + "?" + args
        
        return out
    
    def get_context_path(self):
        return self.req.get_options()['contextPath']
        
    """
    This method should set the current path ready for a redirect.
    """
    def redirect(self, pathstring):
        self.req.internal_redirect(pathstring)
    
    def shutdown(self):
        print "Shutdown not supported under mod_python"
        pass
        
