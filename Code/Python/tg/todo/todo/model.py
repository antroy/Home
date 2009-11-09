from turbogears.database import PackageHub
from sqlobject import *
from datetime import datetime

hub = PackageHub('todo')
__connection__ = hub

class Note(SQLObject):
    info = StringCol()
    toDoItem = ForeignKey("ToDoItem")

class ToDoItem(SQLObject):
    done = BoolCol(default=False)
    title = StringCol()
    deadline = DateCol(default=datetime.now)
    notes = MultipleJoin("Note")
    

