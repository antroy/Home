import turbogears
from turbogears import controllers
from model import *

class Root(controllers.Root):
    @turbogears.expose(html="py_planner.templates.item")
    def index(self, title="Default"):
        item = TodoItem.byName(title)
        description = item.description;
        
        results = Notes.selectBy(item=title)
        
        notes = [note.content for note in results]
        
        return dict(title=title, description=description, notes=notes)
        