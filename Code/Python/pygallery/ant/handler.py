from mod_python import apache
from mod_python import util

import os.path as path, os, ant.images as antim, re, logging, ftplib
import upload_io as io

#from kid import Template
from Cheetah.Template import Template
import ant.templates as templates

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
LOG = logging.getLogger('gallery')

def handler(req):
    req.content_type = "text/html"
    
    if req.args:
        params = dict([x.split('=') for x in req.args.split('&')])
    else:
        params = dict()
    
    LOG.debug("Request: " + str(params))
    if "slideshow" in params:
        req.write(getSlideshowPage(req, int(params.get('slide_no', 0))))
    else:
        req.write(getIndexPage(req))
 
    return apache.OK

def fill_template(req, templ):
    scanner = Scanner(req)
    triples = scanner.image_triples
    
    index = Template(source=templ)
    index.info = io.get_title_and_description(scanner.root)
    index.image_triples = triples
    index.imagearray = scanner.preload_js_array
    index.initialimage = scanner.preload_first 
    index.folders = scanner.subdirs
    index.movies = scanner.movies
    index.context = scanner.baseUrl
    
    fields = util.FieldStorage(req)
    admin_url = fields.getfirst("admin_url")
    index.admin_url = admin_url
    
    uri = req.uri
    if uri.endswith('/'):
        uri = uri[:-1]
        
    LOG.debug("[getIndexPage] URI: %s" % uri)
    
    index.parent = path.split(uri)[0]
    index.parent_name = path.basename(index.parent)

    return index

def getIndexPage(req):
    return str(fill_template(req, templates.index))
        
def getSlideshowPage(req, slide_no):
    out =  fill_template(req, templates.slideshow)
    out.slide_no = slide_no
    return str(out)
        
class Scanner:
    def __init__(self, req):
        uri = req.uri
        root = req.get_options()['galleryRoot']
        self.baseUrl = req.get_options()['galleryBaseUrl']
        self.rel_path = uri[len(self.baseUrl):]
        self.root = root + self.rel_path
        self.files = os.listdir(self.root)
        
        self.get_images()
        self.get_image_triples()
        self.get_movies()
        self.get_subdirs()
        
    def get_images(self):
        self.pics = [self.lower_ext(x) for x in self.files if x.lower().endswith(".jpg")]
        self.shrinkPics()
        self.prepareThumbDir()

    def get_movies(self):
        self.movies = [{'url':self.lower_ext(x), 'description':self.getname(x[:-4])} for x in self.files if x.lower().endswith(".mov")]

    def get_subdirs(self):
        self.subdirs = [{'dir': x, 'name': self.getname(x)} for x in self.files if (path.isdir(path.join(self.root, x)) and not x.startswith('.') and not x.startswith('_'))]

    def get_image_triples(self):
        self.image_triples = []
        
        for pic in self.pics:
            name, ext = path.splitext(pic)
            thumbnail = ".thumbs/%s-thumb%s" % (name.replace("'", r"\'"), ext)
            pic_desc = self.getname(name)
            thumb = path.join(self.root, thumbnail)
            
            imageurl = '/'.join([config.static_image_root, self.rel_path, pic])
            bigimageurl = '/'.join([config.static_image_root, "%s_big%s" % path.splitext(pic)])
            
            self.image_triples.append({'imageurl': imageurl, 'bigimageurl': bigimageurl, 'thumburl': thumbnail, 'description': pic_desc})
        self.image_triples.sort()
        
        preload = [x['thumburl'] for x in self.image_triples]
        self.preload_js_array = "['%s']" % "', '".join(preload)
        
        if len(preload) > 0:
            self.preload_first = preload[0]
        else:
            self.preload_first = None

    def shrinkPics(self):
        pics = self.pics

        ftped = False

        for p in pics:
            pic = path.join(self.root, p)
            size = path.getsize(pic)
            if (path.exists(pic) and size > 200000):
                ftped = True
                client = self.getFtpClient(self.rel_path)
                
                big_image_name = "%s_big%s" % path.splitext(p)
                self.uploadFile(client, big_image_name, pic)

                opts = antim.get_default_options()
                opts.overwrite = True
                m = antim.manipulator(pic, opts)
                m.process()

                self.uploadFile(client, p, pic)

        if ftped:
            client.close()
                
    def prepareThumbDir(self):
        thumbroot = path.join(self.root, ".thumbs") 
        if not path.exists(thumbroot):
            os.makedirs(thumbroot)
        
        thumbs = [path.join(".thumbs", x) for x in os.listdir(thumbroot) if x.endswith(".jpg")]
        LOG.debug("[prepareThumbDir] Thumbnails: %s" % thumbs)
        
        requiredThumbs = {}
        
        for pic in self.pics:
            name, ext = path.splitext(pic)
            thumbnail = path.join(".thumbs",name + "-thumb" + ext)
            requiredThumbs[thumbnail] = pic
            
        LOG.debug("[prepareThumbDir] Required Thumbs: %s", requiredThumbs.keys())
        
        for thumb in thumbs:
            if not (thumb in requiredThumbs.keys()):
                os.remove(path.join(self.root, thumb))
                
        for thumb in requiredThumbs.keys():
            if not (thumb in thumbs):
                m = antim.manipulator(path.join(self.root, requiredThumbs[thumb]))
                LOG.debug("[prepareThumbDir] Creating thumbnail %s", thumb)
                m.createThumb(path.join(self.root,thumb))
            
    def getFtpClient(self, folder):
        folder = folder.strip().strip(r'\/')
        LOG.debug("Getting ftp client. Target folder: ", folder)
        try:
            return self.client
        except:
            LOG.debug("Initializing ftp client")
            self.client = ftplib.FTP(config.ftp_server, config.ftp_user, config.ftp_passwd)
            self.client.cwd('/htdocs/photos')
            LOG.debug("Base folder: " + folder)
            path_elements = [d for d in path.split(folder) if d]
            
            LOG.debug("Base folderi parts: " + str(path_elements))
            
            for d in list(path_elements):
                LOG.debug("Trying to cd to %s" % d)
                try:
                    self.client.cwd(d)
                    path_elements.remove(d)
                except:
                    LOG.debug("dir %s doesn't exist - need to make it." % d)
                    break

            for d in path_elements:
                LOG.debug("Trying to create folder " + d)
                self.client.mkd(d)
                self.client.cwd(d)

            return self.client

    def uploadFile(self, client, name, pic):
        LOG.debug("Uploading file: " + name)
        fh = open(pic, 'rb')
        server, user, passwd = config.ftp_server, config.ftp_user, config.ftp_passwd
        client.storbinary("STOR %s" % name, fh)
        fh.close()

    def getname(self, input):
        output = input.replace("-", " ").replace("_", " ")
        return output
 
    def lower_ext(self, x):
        if x == x.lower():
            return x
        else:
            pair = path.splitext(x)
            newx = pair[0] + pair[1].lower()
            LOG.debug("[lower_ext] root: %s\nold: %s\nnew: %s\n\n" % (self.root, x, newx))
            os.rename(path.join(self.root,x), path.join(self.root,newx))
            return newx

