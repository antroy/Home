# :wrap=soft:maxLineLen=100:
import string, cgi,time, os, os.path as path, sys, urllib, wiki_parser as w_p, logging
from history import history
from os import sep
from wiki_interpreter import isWikiWord
from actions import *
import wiki_interpreter as wi
import templates

LOG = logging.getLogger('wiki-adapter')

wiki_dir = None
static_dir = None
template_dir = None

class RequestInterface(object):
    """
    This method should return the name of the Adapter.
    """
    def get_name(self):
        pass

    """
    This method should send an error back to the client.
    """
    def send_error(self, resp_code, message):
        pass        

    """
    This method should send a response back to the client - typically an HTML page.
    """
    def send_response(self,  content, content_type='text/html', resp_code='200', headers=[]):
        pass
    
    """
    This method retrieves the named header from the request.
    """
    def get_header(self, header):
        pass

    """
    This method should read post data as sent from the client.
    """
    def read_from_client(self, bytes):
        pass

    """
    This method should retrieve the current path from the request.
    """
    def get_path(self):
        pass
    
    """
    This method should set the current path ready for a redirect.
    """
    def set_path(self, pathstring):
        pass
    
    def get_context_path(self):
        pass

        
    """
    Shutdown the server (optional).
    """
    def shutdown(self):
        pass
        
    templateDict = None
    trail = wi.trail()
    type_map = {'.css': 'text/css', ".js": 'text/javascript' ,".jpg": 'image/jpeg',".png": 'image/png', ".gif": 'image/gif', ".html": 'text/html',".htm": 'text/html'}
    
    def do_get(self):
        try:
            pp = wi.path_parser(self.get_path())
            self.name = pp.name
            self.action = pp.action
            self.attributes = pp.attributes
            
            action = action_map(self, self.name, self.action).get_action()
            LOG.debug("Action name: " + str(type(action)))
            return action.run()
        except IOError:
            return self.send_error(404,'File Not Found: %s' % self.get_path())
    
    def do_post(self):
        pp = wi.path_parser(self.get_path())
        self.name = pp.name
        self.action = pp.action
                
        LOG.debug("Updating %s with new content..." % self.name)

        if self.get_path().endswith("UPLOAD"):
            return self.do_upload()
        elif isWikiWord(self.name):
            return self.do_update()
        else:
            return self.send_error(404,'File Not Found: %s' % self.get_path())
       
    def send_error_404(self):
        return self.send_error(404,'File Not Found: %s' % self.get_path())
            
#    def redirect(req, url, temporary=False, seeOther=False):
#        """
#        Immediately redirects the request to the given url. If the
#        seeOther parameter is set, 303 See Other response is sent, if the
#        temporary parameter is set, the server issues a 307 Temporary
#        Redirect. Otherwise a 301 Moved Permanently response is issued.
#        """
#        from mod_python import apache
#                                                                                    
#        if seeOther:
#            status = apache.HTTP_SEE_OTHER
#        elif temporary:
#            status = apache.HTTP_TEMPORARY_REDIRECT
#        else:
#            status = apache.HTTP_MOVED_PERMANENTLY
#                                                                                    
#        req.headers_out['Location'] = url
#        req.status = status
#        raise apache.SERVER_RETURN, status
        
    def do_update(self):
        content_length = int(self.get_header('content-length'))
        LOG.debug("About to read %s bytes from the client." % content_length)
        
        content = self.read_from_client(content_length)
        content_map = self.parse_content(content)
        
        _path = '/' + content_map['title']

        saved = self.save_wiki_page(_path, content_map['new_details'])

        LOG.debug("Wiki page %s" % ("removed", "saved")[saved])

        if saved:
            self.set_path(_path)
        else:
            self.set_path("/")
        
        self.do_get()
        
        return 0
    
    def parse_content(self, content):
        out = {}
        pairlist = content.split('&')
        
        for pair in pairlist:
            p = pair.split('=')
            out[p[0]] = urllib.unquote_plus(p[1])
        return out
        
    def do_upload(self):
        global rootnode
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            
            if ctype == 'multipart/form-data':
                query=cgi.parse_multipart(self.rfile, pdict)
                
            self.send_response(301)
            self.end_headers()
            
            upfilecontent = query.get('upfile')
            print "filecontent", upfilecontent[0]
            self.wfile.write(upfilecontent[0]);
            
        except :
            pass
            
    def show_raw_page(self):
        interp = wi.wiki_interpreter(self.name)
        cont = ""
        
        if not interp.exists:
            self.show_edit_page(interp)
            return
        else:
            interp.load()
            cont = interp.raw_content()
        content_type = "text/plain"
        if self.name == "StyleSheet":
            content_type = "text/css"
        self.send_response(cont, content_type)
        
    def show_wiki_page(self):
        interp = wi.wiki_interpreter(self.name)
        cont = ""
        
        if not interp.exists:
            self.show_edit_page(interp)
            return
        else:
            interp.load()
            cont = interp.parsed_content()
        
        self.show_page(interp.title, cont, interp.last_modified())
        
    def show_history_page(self):
        interp = wi.wiki_interpreter(self.name)
        cont = ""
        
        if not interp.exists:
            self.show_edit_page(interp)
            return
        
        pageHist = history(self.name)
        out = templates.history_template(self.name, pageHist.listVersions())
        self.send_response(out)
        
    def view_history_page(self):
        interp = wi.wiki_interpreter(self.name)
        cont = ""
        
        if not interp.exists:
            self.show_edit_page(interp)
            return
        
        version = 'v1'
        if self.attributes.has_key('version'):
            version = self.attributes['version'][0]
            
        pageHist = history(self.name)
        rawText = pageHist.getVersion(version)
        interp = wi.wiki_interpreter(self.name, rawText)
        content = interp.parsed_content()
        
        out = templates.view_history_template(self.name, content, "NOT IMPLEMENTED", version)
        self.send_response(out)
        
    def rollback_history(self):
        interp = wi.wiki_interpreter(self.name)
        cont = ""
        
        if not interp.exists:
            self.show_edit_page(interp)
            return
        
        versionlst = self.attributes.get('version')
        if versionlst == None:
            self.show_wiki_page()
            
        version = versionlst[0]
        
        pageHist = history(self.name)
        rawText = pageHist.getVersion(version)
        
        self.save_wiki_page(self.name, rawText)
        self.show_wiki_page()
        
    def show_page(self, title, content, modified):
        trail = self.trail
        trail.update(title)
        
        sidebar_interp = wi.wiki_interpreter("/SideBar").load()
        sidebar = sidebar_interp.parsed_content()
        
        out = templates.main_template(title, content, modified, trail.trail_html(), sidebar)
        LOG.debug("TRAIL: " + trail.trail_html())
        
        self.send_response(out)
        
    def show_edit_page(self, interp=None):
        if not interp:
            q_mark = self.get_path().index('?')
            interp = wi.wiki_interpreter(self.name[:q_mark])
        interp.load()

        out = templates.edit_template(interp.title, interp.raw_content())
        
        self.send_response(out)
        
    def save_wiki_page(self, page, content):
        LOG.debug("Saving WikiPage " + page)
        title = path.basename(page)
        wikipath = path.join(wiki_dir, title + ".txt")
        if content.strip() in ("remove", "delete"):
            os.remove(wikipath)
            return False
        else:
            f = open(wikipath, 'w')
            f.write(content)
            f.close()
            pageHist = history(title)
            pageHist.addPage(content)
            return True
        
    def showAllPages(self):
        files = os.listdir(wiki_dir)
        wikifiles = [x.split('.')[0] for x in files if x.endswith(".txt")]
        wikifiles.sort()
        content = "\n".join(wikifiles)
        parser = w_p.parser(content)
        self.show_page("AllPages", parser.parsed_text(), "now")
        
    def templates(self):
        if self.templateDict == None:
            print "Parsing Templates..."
            self.templateDict = {}
            templatePath = template_dir
            for f in os.listdir(templatePath):
                filepath = path.join(templatePath, f)
                if path.isfile(filepath) and filepath.endswith('.html'):
                    handle = open(filepath)
                    text = handle.read()
                    handle.close()
                    tmpl_name = path.splitext(f)[0]
                    self.templateDict[tmpl_name] = string.Template(text)
        return self.templateDict


