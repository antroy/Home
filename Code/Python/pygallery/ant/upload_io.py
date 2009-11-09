from kid import Template

import os.path as path, os, stat
import constants as const

import logging
LOG = logging.getLogger('gallery_admin.io')

FILE_PERMISSIONS = stat.S_IRUSR + stat.S_IWUSR + stat.S_IRGRP + stat.S_IWGRP + stat.S_IROTH

def tryDeleteFolder(root, pth):
    directory = path.join(root, pth)
    errors = None
    if not path.exists(directory):
        errors = 'The folder %s seems to have already been removed!' % pth
    try:
        info = path.join(directory, "info.txt")
        thumbs = path.join(directory, ".thumbs")
        
        if path.exists(thumbs):
            for base, dirs, files in os.walk(thumbs, topdown=False):
                for d in dirs: os.rmdir(path.join(base, d))
                for f in files: os.remove(path.join(base, f))
            os.rmdir(thumbs)
         
        if path.exists(info) and len(os.listdir(directory)) == 1:
            os.remove(info)
        
        os.rmdir(directory)
    except:
        if len(os.listdir(directory)) > 0:
            LOG.debug('[tryDeleteFolder] Could not remove the folder %s as it is not empty.' % directory)
            errors = 'Could not remove the folder %s as it is not empty.' % pth
        else:
            errors = 'Could not remove the folder %s - it is possible that someone else is looking at it...' % directory
    return errors
    
def tryDeleteFile(root, pth):
    filename = path.join(root, pth)
    errors = None
    if not path.exists(filename):
        errors = 'The folder %s seems to have already been removed!' % pth
    try:
        os.remove(filename)
    except OSError, ex:
        errors = 'Could not remove the file %s - it is possible that someone else is looking at it...\n%s' % (filename, ex)
    return errors
       
def getFolderTree(user, root):
    LOG.debug("[getFolderTree] User: %s; Root: %s" % (user, root))
    dirmap = {}
    top = Node(user)
    dirmap[root] = top
    
    for base, dirs, files in os.walk(root):
        if path.basename(base).startswith('.'): 
            continue
        parent = dirmap[base]
        for dir in dirs:
            if dir.startswith('.'): 
                continue
            node = Node(dir, parent)
            parent.addChild(node)
            dirmap[path.join(base, dir)] = node
    
    return top
    
def getFilelist(root, folder):
    localpath = path.join(root, folder)
    
    if not path.exists(localpath):
        return [], None
        
    out = os.listdir(localpath)
    
    empty_test_list = [f for f in out if not (f == '.thumbs' or f == 'info.txt')]
    is_empty = len(empty_test_list) == 0
    
    out = [x for x in out if (path.isfile(path.join(localpath, x)) and file_permitted(x))]
    out.sort()
    
    return out, is_empty
    
def saveFiles(fields, localroot, permitted_uploads=None):
    if not path.exists(localroot):
        os.makedirs(localroot)
    errors = None
    
    temp_fields = [f for f in fields if file_permitted(f.filename)]
    
    if len(temp_fields) != len(fields):
        fields = temp_fields
        errors = "Only image files can be uploaded! Some of your files could not be uploaded..."
    for field in fields:
        LOG.debug("Saving %s" % field.filename)
        filepath = path.join(localroot, field.filename)
        f = open(filepath, 'wb')
        f.write(field.file.read())
        f.close()
        os.chmod(filepath, FILE_PERMISSIONS)

def getUploadPage(user, tree, errors=None, messages=None, 
                              admin_context='', gallery_context=''):
    upload = Template(name="templates.upload")
    upload.user = user
    upload.root_node = tree
    upload.errors = errors
    upload.messages = messages
    upload.admin_context = admin_context
    upload.gallery_context = gallery_context
    
    return upload.serialize(output='html')
    
def getEditFolderPage(user, folder, parent, files, is_empty, errors=None, 
        title='', description='', messages=None, admin_context='', gallery_context=''):
    editfolder = Template(name="templates.editfolder")
    editfolder.user = user
    if folder:
        editfolder.folder = folder.replace('\\','/')
        editfolder.folder_name = path.basename(folder)
    else:
        editfolder.folder = ''
        editfolder.folder_name = ''
    editfolder.files = files
    editfolder.parent = parent
    editfolder.errors = errors
    editfolder.messages = messages
    editfolder.is_empty = is_empty
    editfolder.description = description
    editfolder.title = title
    editfolder.admin_context = admin_context
    editfolder.gallery_context = gallery_context
    
    return editfolder.serialize(output='html')

def get_title_and_description(root, pth=''):
    LOG.debug("[get_title_and_description] Getting title and description for root %s and path %s" % (root, pth))
    out = {}
    if not root or pth is None:
        out['title'] = ''
        out['description'] = []
        return out
        
    descriptor = path.join(root, pth, 'info.txt')
    
    LOG.debug("[get_title_and_description] Folder description: ", descriptor)
    
    if path.exists(descriptor) and path.isfile(descriptor):
        f = file(descriptor)
        temp = [line.strip() for line in f]
        f.close()
        
        out['title'] = temp[0] 
        out['description'] = paragraphs_to_array(temp[1:])
        
    else:
        out['title'] = ''
        out['description'] = []
    
    return out

def set_title_and_description(title, description, root, pth=''):
    descriptor = path.join(root, pth, 'info.txt')
    
    if not title:
        out = '\n'
    else:
        out = title + '\n'
    
    if not description:
            description = []
    
    if isinstance(description, str):
        descarr = [(x + '\n') for x in description.split('\n')]
        description = paragraphs_to_array(descarr)
    
    LOG.debug("[set_title_and_description] Description: %s" % description)
        
    for para in description:
        out = out + para + '\n\n'
    
    info = file(descriptor, 'w')
    info.write(out)
    info.close()
    os.chmod(descriptor, FILE_PERMISSIONS)

def rename_folder(fs_path, new_name):
    LOG.debug("[rename_folder] Path: %s; New Name: %s;" % (fs_path, new_name))
    if path.basename(fs_path) == new_name:
        return None
    new_folder = path.join(path.split(fs_path)[0], new_name)
    try:
        os.rename(fs_path, new_folder)
        return None
    except OSError, ex:
        LOG.error("{rename_folder] Could not rename folder %s to %s. %s" % (fs_path, new_folder, ex))
        return "Could not rename folder."
    
def paragraphs_to_array(text_array):
    buffer = ''
    paragraphs = []

    for line in text_array:
       if len(line) == 0 and len(buffer) > 0:
          paragraphs.append(buffer)
          buffer = ''
       else:
          buffer += line
          
    if len(buffer.strip()) > 0:
        paragraphs.append(buffer)
        
    LOG.debug("[paragraphs_to_array] Paragraphs: %s" % paragraphs)
    
    return paragraphs
    
def file_permitted(filename):
    filename = str(filename)
    LOG.debug("[file_permitted] Getting permission to upload %s" % filename)
    extension = path.splitext(filename)[1]
    
    return extension.lower() in const.permitted_uploads
    
class Node (object):
    
    def __init__(self, pth, parent=None):
        self.path = pth
        self.parent = parent
        self.fullpath = self.path
        self.parentpath = ''
        
        if self.parent:
            self.parentpath = self.parent.fullpath
            self.fullpath = path.join(self.parentpath, self.path)
        
        self.fullpath = self.fullpath.replace('\\', '/')
        LOG.debug("[Node.__init__] full path: %s" % self.fullpath)
        
        parts = self.fullpath.split('/', 1)
        if len(parts) > 1:
            self.contextpath = parts[1]
        else:
            self.contextpath = ''
            
        LOG.debug("[Node.__init__] context path: %s" % self.contextpath)
            
        self.children = []
           
    def addChild(self, child):
        self.children.append(child)
        
    def __str__(self):
        return self.get_decorated_node(PlainDecorator())
    
    def get_decorated_node(self, decorator):
        out = decorator.valuePre(self)
        
        if len(self.children) > 0:
            out = out + decorator.childrenPre(self)
            for child in self.children:
                out = out + child.get_decorated_node(decorator)
            out = out + decorator.childrenPost(self)
            
        out = out + decorator.valuePost(self)
            
        return out
        
class ListDecorator (object):
    def valuePre(self, node):
        fields = {'fullpath': node.fullpath, 'shortpath': node.path}
        if node.parent:
            fields['parentpath'] = node.parent.fullpath
        else:
            fields['parentpath'] = ''
        
        return """<li><input type="radio" name="folder" value="%(fullpath)s" />%(shortpath)s """ % fields
    def valuePost(self, node):
        return '</li>'
    def childrenPre(self, node):
        return '<ul>'
    def childrenPost(self, node):
        return '</ul>'

class PlainDecorator (object):
    def valuePre(self, node):
        return "Node:(%s) [" % node.path
    def valuePost(self, node):
        return ']'
    def childrenPre(self, node):
        return ''
    def childrenPost(self, node):
        return ''

