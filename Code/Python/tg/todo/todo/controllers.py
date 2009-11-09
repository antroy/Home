import logging, datetime as dt
import turbogears
from turbogears import controllers, expose, flash, config
from model import *

log = logging.getLogger(__name__)
log.addHandler(logging.FileHandler(config.get("log_file")))

class Root(controllers.RootController):
    @expose(template="cheetah:todo.templates.todo")
    def index(self):
        out = {}
        res = ToDoItem.select().orderBy("deadline")
        out['todoitems'] = res
        out['now'] = dt.datetime.now()

        return out

    @expose()
    def add(self, title, deadline):
        log.debug("Title: %s; Deadline: %s" % (title,deadline))
        kw = {"title": title}
        if deadline:
            kw['deadline'] = deadline

        ToDoItem(**kw)
        raise turbogears.redirect("/")
        
    @expose("json")
    def notes_for_id(self, id):
        res = Note.selectBy(toDoItemID=id).orderBy("id")
        out = {}
        out["notes"] = [x.info for x in res]

        return out

    @expose("json")
    def add_note_for_id(self, id, note):
        Note(toDoItemID=id, info=note)
        out = self.notes_for_id(id)
        log.debug("ADD NOTE: " + str(out))
        return out

    @expose("json")
    def done_for_id(self, id, done):
        log.debug("DONE_FOR_ID: ID: %s; DONE: %s" % (id, done))
        ToDoItem.get(id).done = done == "true"
        return {}

