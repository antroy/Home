from sqlobject import *
from turbogears.database import PackageHub
from datetime import datetime

hub = PackageHub("py_planner")
__connection__ = hub

class TodoItem (SQLObject):
    name = StringCol(alternateID=True, length=100)
    description = StringCol(length=1000)
    created = DateTimeCol(default=datetime.now)
    #date_due = DateTimeCol()
    done = BoolCol(default=False)

class Notes (SQLObject):
    created = DateTimeCol(default=datetime.now)
    content = StringCol(length=1000)
    item = ForeignKey('ToDoItem')