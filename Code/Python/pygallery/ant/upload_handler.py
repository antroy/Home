from mod_python import apache
from mod_python import util

import os.path as path
import upload_actions as actions
import upload_io as io
import logging
from kid import Template

try:
    import config
except (ImportError):
    class ConfigObject(object): pass
    config = ConfigObject()
    config.log_level = logging.WARNING
    config.log_file = 'pygallery.log'
    
logging.basicConfig(level=config.log_level,
    format='%(name)-12s: %(asctime)s %(levelname)s %(message)s',
    filename=config.log_file,
    filemode='w')
logging.debug('Initializing logging...')
print "Log file: ", config.log_file
LOG = logging.getLogger('gallery_admin')

def handler(req):
    handler = PathHandler(req)
    return handler.run()

class PathHandler (object):
    action_map = { 'update': actions.updateAction,
                'upload':  actions.uploadAction,
                'delete': actions.deleteFileAction,
                'folderadd':  actions.addFolderAction,
                'indexpage': actions.indexPageAction}
                
    def __init__(self, req):
        self.req = req

    def run(self):
        req_info = RequestInfo(self.req)
        
        LOG.debug('Action: %s' % req_info.action)
        
        action =  self.action_map.get(req_info.action, actions.defaultAction)
        req_info = action(req_info)
        
        LOG.debug('Forward: %s' % req_info.resp_forward)
        
        self.req.content_type = req_info.resp_content_type
        
        if req_info.resp_code == apache.OK:
            template = Template(name=req_info.resp_forward)
            template.__dict__.update(req_info.resp_data)
            data = template.serialize(output='html')
            
            self.req.write(data)
        
        return req_info.resp_code

class RequestInfo (object):
    resp_data = {'errors': [] ,'messages': []}
    resp_content_type = "text/html"
    resp_code = apache.OK
    resp_forward = ''

    def __init__(self, req):
        self.req = req
        uri = req.uri
        
        self.fields = util.FieldStorage(req)
        self.action = self.fields.getfirst("action")
        if path.basename(uri) == 'index.html':
            self.action = 'indexpage'
            uri = path.split(uri)[0]
        
        self.user = req.user
        self.root = path.join(req.get_options()['galleryRoot'], self.user)
        self.admin_context = req.get_options()['admin_context']
        self.gallery_context = req.get_options()['gallery_context']
        
        self.url_path = uri[len(self.admin_context) + 1:]
        self.fs_path = path.join(self.root, self.url_path)
        self.parent = path.split(self.url_path)[0]
        
        self.resp_data['admin_context'] = self.admin_context
        self.resp_data['gallery_context'] = self.gallery_context
        self.resp_data['folder'] = self.url_path
        self.resp_data['parent'] = self.parent
        self.resp_data['folder_name'] = path.basename(self.url_path)
        self.resp_data['user'] = req.user
        
        debug_message = """
        root: %s
        admin_context: %s
        gallery_context: %s
        uri: %s
        url_path: %s
        fs_path: %s
        parent: %s""" % (self.root, self.admin_context, self.gallery_context, uri, self.url_path, self.fs_path, self.parent)
        
        LOG.debug(debug_message)
     
    def add_error(self, mssg):
        self.resp_data['errors'].append(mssg)
        
        
    def add_message(self, mssg):
        self.resp_data['messages'].append(mssg)
        
if __name__ == '__main__':
    args = 'a=xxx&b=yyy&c&d=333'
    print parseargs(args)
    
    tree = getFolders('ant', 'c:/0/upload')
    print tree.get_decorated_node(ListDecorator())
    

