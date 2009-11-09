# -*- coding: UTF-8 -*-

from turbogears import controllers, expose, flash
from model import *
from turbogears import identity, redirect, config
from cherrypy import request, response
from sqlobject.dberrors import DuplicateEntryError
from sqlobject.main import SQLObjectNotFound
import datetime, os, os.path, re 
from docutils.core import publish_parts
import tools, images

# from ludwig import json
import logging

log = logging.getLogger(__name__)
log.addHandler(logging.FileHandler(config.get("log_file")))

def now():
    return datetime.datetime.now()

class DummyIdea(object):
    id = ""
    title = ""
    date = now()
    text = ""
    status = ""
    categories = []
    user = None
    notes = []
    attachments = []
    dummy = True

def user():
    return identity.current.user

def all_users():
    return User.select()

def get_header():
    out = """
    <div id="header">
        <div class="left">
            <a href="." class="header_link" alt="Index">Index</a> |
            <a href="new" class="header_link" alt="New Idea">New Idea</a>
        </div>
        <div class="right">
            <a href="logout" alt="Log out">Log out</a>
        </div>                                
    </div>
    """
    return out

entity_pattern = r"\&amp;(\w+|#\d+);"

def reSt(text):
    content = publish_parts(text, writer_name="html")['html_body']

    log.debug("Content before:" + content)
    content = re.sub(entity_pattern, r"&\1;", content) 
    
    return content

def get_categories():
    categories = Category.select()
    out = []
    
    for cat in categories:
        ideas = cat.ideas
        if not ideas:
            Category.delete(cat.id)
        else:
            out.append(cat.name)

    return out

def get_statuses():
    statuses = Status.select()
    out = []
    
    for stat in statuses:
        ideas = Idea.selectBy(status=stat)
        if ideas.count() == 0:
            Status.delete(stat.id)
        else:
            out.append(stat.name)

    return out

class Root(controllers.RootController):
    @expose(template="cheetah:ludwig.templates.index")
    @identity.require(identity.in_group("users"))
    def index(self, all=True):
        log.debug("In Index action")
        if all:
            ideas = Idea.select()
        #else:
        #    ideas = Idea.select(Idea.q.status != "Archive")

        return dict(now=now(), ideas=ideas, header=get_header(), categories=get_categories(), statuses=get_statuses(), category=None, status=None)

    @expose(template="cheetah:ludwig.templates.index")
    @identity.require(identity.in_group("users"))
    def category_search(self, category):
        cat = Category.byName(category)
        ideas = cat.ideas

        return dict(now=now(), ideas=ideas, header=get_header(), categories=get_categories(), statuses=get_statuses(), category=category)

    @expose(template="cheetah:ludwig.templates.index")
    @identity.require(identity.in_group("users"))
    def status_search(self, status):
        stat = Status.byName(status)
        ideas = Idea.selectBy(status=stat)

        return dict(now=now(), ideas=ideas, header=get_header(), categories=get_categories(), statuses=get_statuses(), category=None, status=status)

    @expose(template="cheetah:ludwig.templates.new")
    @identity.require(identity.in_group("users"))
    def new(self):
        idea = DummyIdea()

        return dict(idea=idea, header=get_header(), categories=get_categories(), statuses=get_statuses())

    @expose(template="cheetah:ludwig.templates.new")
    @identity.require(identity.in_group("users"))
    def edit(self, id):
        idea = Idea.get(id)

        return dict(idea=idea, header=get_header(), categories=get_categories(), statuses=get_statuses())

    @expose()
    @identity.require(identity.in_group("users"))
    def add(self, **kw):
        kw['date'] = now()
        kw['user'] = user()
        log.debug(str(kw))
        id = kw['id'].strip()
        log.debug("ID1: " + id)
        del kw['id']
        log.debug("ID2: " + id)

        categories = kw['categories']
        del kw['categories']

        status = kw['status'].strip()
        del kw['status']

        try:
            stat = Status(name=status)
        except DuplicateEntryError:
            stat = Status.byName(status)

        kw['status'] = stat

        log.debug("ID3: " + id)
        if not id:
            idea = Idea(**kw)
            
        else:
            idea = Idea.get(id)
            for k, v in kw.iteritems():
                if hasattr(idea, k):
                    setattr(idea, k, v)
            
        categories = re.split(r"[^a-z_-]+", categories.lower())
        
        for c in idea.categories:
            idea.removeCategory(c)

        for cat in categories:
            try:
                c = Category.byName(cat)
            except SQLObjectNotFound:
                c = Category(name=cat)

            idea.addCategory(c)

        if not id:
            tools.send_mail(idea.id, "New Idea added: '%(title)s'")

        redirect("/idea", redirect_params={'id':idea.id})

    @expose()
    @identity.require(identity.in_group("users"))
    def add_note(self, item_id, text, id=None):
        note = Note(text=text, date=now(), user=user())
        idea = Idea.get(item_id)
        idea.addNote(note)

        tools.send_mail(item_id, "New Note added for idea '%(title)s'", note_id=note.id)

        redirect("/idea", redirect_params={'id':item_id})

    @expose()
    @identity.require(identity.in_group("users"))
    def add_action(self, item_id, text, assign_to, id=None):
        log.debug("item_id: '%s'; assign_to: '%s'" % (item_id, assign_to))
        ass_to = User.get(assign_to)
        log.debug("User: " + ass_to.display_name)
        action = Action(text=text, date=now(), assigned_by=user(), assigned_to=ass_to)
        log.debug("Action created")
        idea = Idea.get(item_id)
        log.debug("Idea: " + idea.title)
        idea.addAction(action)
        log.debug("Action added")

        tools.send_mail(item_id, "New Action Added for idea '%(title)s'", action_id=action.id)

        redirect("/idea", redirect_params={'id':item_id})

    @expose()
    @identity.require(identity.in_group("users"))
    def attach(self, upload_file, item_id, **kw):
        log.debug("Request Params:" + str(request.params.keys()))
        log.debug("kw Params:" + str(kw.keys()))
        
        fn = re.split(r"[\\/]", upload_file.filename)[-1]
        
        target_file_name = os.path.join(os.getcwd(), config.get("upload.dir"), fn)
        url = "./static/uploads/%s" % fn

        #try:
        #    att = Attachment.select(Attachment.q.filename == upload_file.filename,
        #                            Attachment.q.ideaID == item_id)
        #    att.date = now()
        #except SQLObjectNotFound:
        att = Attachment(date=now(), filename=fn, url=url, ideaID=item_id, user=user()) 

        f = open(target_file_name, 'wb')
        bytes = upload_file.file.read(1024)
        
        while bytes:
            f.write(bytes)
            bytes = upload_file.file.read(1024)

        f.close()

        try:
           man = images.Manipulator(target_file_name)
           man.createThumb()
        except:
           log.debug("Could not create thumbnail for file: " + target_file_name)
           import traceback
           log.debug("Trace:" + traceback.format_exc())

        
        tools.send_mail(item_id, "Attachment Added for idea '%(title)s'", attach_id=att.id)
            
        redirect("/idea", redirect_params={'id': item_id})

    @expose()
    @identity.require(identity.in_group("users"))
    def edit_action(self, id, item_id, assign_to, text): 
        act = Action.get(id)
        user = User.get(assign_to)
        act.text = text
        act.assigned_to = user

        redirect("/idea", redirect_params={'id': item_id})

    @expose()
    @identity.require(identity.in_group("users"))
    def edit_note(self, id, item_id, text): 
        act = Note.get(id)
        act.text = text

        redirect("/idea", redirect_params={'id': item_id})

    @expose('json')
    def get_action_data(self, id):
        act = Action.get(id)
        return dict(text=act.text, assigned_to=act.assigned_to)

    @expose('json')
    def get_action_update_data(self, id):
        act = Note.get(id)
        return dict(text=act.text)
        
    @expose('json')
    def get_note_data(self, id):
        note = Note.get(id)
        return dict(text=note.text)
        
    @expose(template="cheetah:ludwig.templates.idea")
    @identity.require(identity.in_group("users"))
    def idea(self, id):
        idea = Idea.get(id)

        return dict(idea=idea, header=get_header(), all_users=all_users(), current_user=user(), reSt=reSt)

    @expose()
    @identity.require(identity.in_group("users"))
    def add_edit_update(self, idea_id, action_id, text, update_id=None):
        action = Action.get(action_id)
        
        update = update_id and not update_id.strip() == "null"
        
        if update:
            note = Note.get(update_id)
            note.text = text
        else:
            note = Note(text=text, date=now(), user=user())
            action.addNote(note)

        redirect("/idea", redirect_params={'id':idea_id})

    @expose(template="cheetah:ludwig.templates.login")
    def login(self, forward_url=None, previous_url=None, *args, **kw):
        log.debug("In Login action")
        log.debug("Forward URL: " + str(forward_url))
        
        if forward_url:
            forward_url = config.get("url.root") + forward_url
        
        if not identity.current.anonymous \
            and identity.was_login_attempted() \
            and not identity.get_identity_errors():
            raise redirect(forward_url)

        forward_url = None
        previous_url = config.get("url.root") + request.path
        log.debug("Previous URL: " + str(previous_url))

        log.debug("Login Errors" + str(identity.get_identity_errors()))

        if identity.was_login_attempted():
            msg=_("The credentials you supplied were not correct or "
                   "did not grant access to this resource.")
        elif identity.get_identity_errors():
            msg=_("You must provide your credentials before accessing "
                   "this resource.")
        else:
            msg=_("Please log in.")
            forward_url= request.headers.get("Referer", "/")
             
        if forward_url:
            forward_url = config.get("url.root") + forward_url

        log.debug("Forward URL (2): " + str(forward_url))
            
        response.status=403
        out = dict(message=msg, previous_url=previous_url, logging_in=True,
                    original_parameters=request.params,
                    forward_url=forward_url)

        log.debug("Login output: " + str(out))
        
        return out

    @expose()
    def logout(self):
        identity.current.logout()
        raise redirect("/")
