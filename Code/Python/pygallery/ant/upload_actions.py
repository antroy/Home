from mod_python import apache
import os.path as path, os
import upload_handler
import upload_io as io
import logging
LOG = logging.getLogger('gallery_admin.io')

def uploadFilesAction(user, fields, root, admin_context, gallery_context):
    errors = []
    action = fields.getfirst("action")
    
    if action and action == 'delete_folder':
        field = fields.getfirst("folder")
        if field:
            err = io.tryDeleteFolder(root, field)
            if err:
                errors.append(err)
    elif fields.getfirst('upload'):
        localroot = path.join(root, fields.getfirst('folder', user))
        to_save = [f for f in fields.list if f.name == 'u' and len(f.filename.strip()) > 0]
        err = io.saveFiles(to_save, localroot)
        if err: 
            errors.append(err)
    
    content_type = "text/html"
    data = io.getUploadPage(user, io.getFolders(user, root), errors, None, admin_context, gallery_context)
    response = apache.OK
    
    return data, content_type, response
    
def addFolderAction(user, fields, root, admin_context, gallery_context):
    localroot = path.join(root, fields.getfirst('parent', user))
    if not path.exists(localroot):
        path.makedirs(localroot)
    
    return showEditFolderPageAction(user, fields, root)
    
def deleteFileAction(req_info):
    LOG.debug("[deleteFileAction] Delete action called.")
    for field in req_info.fields.getlist("file"):
        err = io.tryDeleteFile(req_info.fs_path, field)
        if err:
            req_info.add_error(err)

    return defaultAction(req_info)
    
def uploadAction(req_info):
    LOG.debug("[uploadAction] Upload action called.")
    to_save = [f for f in req_info.fields.list if f.name == 'u' and len(f.filename.strip()) > 0]
    LOG.debug("Uploading: %s" % to_save)
    err = io.saveFiles(to_save, req_info.fs_path)
    if err: 
        req_info.add_error(err)

    return defaultAction(req_info)
    
def updateAction(req_info):
    LOG.debug("[updateAction] Update action called.")
    title = req_info.fields.getfirst("title")
    description = req_info.fields.getfirst("description")
    
    folder_path = req_info.fs_path
        
    if not path.exists(folder_path):
        if not path.exists(path.split(folder_path)[0]):
            req_info.resp_code = apache.HTTP_FORBIDDEN
        try:
            os.mkdir(folder_path)
        except:
            err = "Could not create folder %s"
            errors.append(err % req_info.url_path)
            LOG.error(("[showEditFolderPageAction] " + err) % folder_path)

    LOG.debug("[showEditFolderPageAction] New Description: ", description)
    
    err = io.set_title_and_description(title, description, req_info.fs_path)
    if err:
        errors.append(err)
        err = ''
        
    new_name = req_info.fields.getfirst("folder_name")
    
    if new_name:
        err = io.rename_folder(req_info.fs_path, new_name)
        if not err:
            new_loc =  path.split(req_info.req.uri)[0] + '/' + new_name
            LOG.debug("New Location: %s" % new_loc)
            req_info.req.headers_out.add('Location',new_loc)
            req_info.resp_code = apache.HTTP_MOVED_PERMANENTLY
            
            return req_info
    if err:
        LOG.error("[showEditFolderPageAction] Appending Error: " + err)
        req_info.add_error(err)
   
    return defaultAction(req_info)
    
    
def defaultAction(req_info):
    folder = req_info.url_path
    
    LOG.debug("Root: %s; Folder: %s" % (req_info.root, folder))
        
    files, is_empty = io.getFilelist(req_info.root, folder)
    title_desc = io.get_title_and_description(req_info.root, folder)
    
    description = '\n\n'.join(title_desc['description'])
    
    title =  title_desc['title']
    if  title == '':
        title = path.basename(folder)
    LOG.debug("[showEditFolderPageAction] Title: %s; Description: %s" % (title, description))
    
    req_info.resp_data['files'] = files
    req_info.resp_data['is_empty'] = is_empty
    req_info.resp_data['description'] = description
    req_info.resp_data['title'] = title
    
    LOG.debug('[showEditFolderPageAction] url_path: %s' % req_info.url_path)
    
    req_info.resp_forward = 'templates.editfolder'
    
    return req_info
    

def indexPageAction(req_info):
    defaultAction(req_info)
    tree = io.getFolderTree(req_info.user, req_info.fs_path)
    req_info.resp_data['root_node'] = tree
    req_info.resp_forward = 'templates.upload_index'
    
    return req_info
    
