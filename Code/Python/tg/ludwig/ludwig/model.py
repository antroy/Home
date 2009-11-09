from datetime import datetime
from turbogears.database import PackageHub
from sqlobject import *
from turbogears import identity

hub = PackageHub('ludwig')
__connection__ = hub

# class YourDataClass(SQLObject):
#     pass

# identity models.
class Visit(SQLObject):
    """
    A visit to your site
    """
    class sqlmeta:
        table = 'visit'

    visit_key = StringCol(length=40, alternateID=True,
                          alternateMethodName='by_visit_key')
    created = DateTimeCol(default=datetime.now)
    expiry = DateTimeCol()

    def lookup_visit(cls, visit_key):
        try:
            return cls.by_visit_key(visit_key)
        except SQLObjectNotFound:
            return None
    lookup_visit = classmethod(lookup_visit)


class VisitIdentity(SQLObject):
    """
    A Visit that is link to a User object
    """
    visit_key = StringCol(length=40, alternateID=True,
                          alternateMethodName='by_visit_key')
    user_id = IntCol()


class Group(SQLObject):
    """
    An ultra-simple group definition.
    """
    # names like "Group", "Order" and "User" are reserved words in SQL
    # so we set the name to something safe for SQL
    class sqlmeta:
        table = 'tg_group'

    group_name = UnicodeCol(length=16, alternateID=True,
                            alternateMethodName='by_group_name')
    display_name = UnicodeCol(length=255)
    created = DateTimeCol(default=datetime.now)

    # collection of all users belonging to this group
    users = RelatedJoin('User', intermediateTable='user_group',
                        joinColumn='group_id', otherColumn='user_id')

    # collection of all permissions for this group
    permissions = RelatedJoin('Permission', joinColumn='group_id',
                              intermediateTable='group_permission',
                              otherColumn='permission_id')


class User(SQLObject):
    """
    Reasonably basic User definition.
    Probably would want additional attributes.
    """
    # names like "Group", "Order" and "User" are reserved words in SQL
    # so we set the name to something safe for SQL
    class sqlmeta:
        table = 'tg_user'

    user_name = UnicodeCol(length=16, alternateID=True,
                           alternateMethodName='by_user_name')
    email_address = UnicodeCol(length=255, alternateID=True,
                               alternateMethodName='by_email_address')
    display_name = UnicodeCol(length=255)
    password = UnicodeCol(length=40)
    created = DateTimeCol(default=datetime.now)

    # groups this user belongs to
    groups = RelatedJoin('Group', intermediateTable='user_group',
                         joinColumn='user_id', otherColumn='group_id')

    def _get_permissions(self):
        perms = set()
        for g in self.groups:
            perms = perms | set(g.permissions)
        return perms

    def _set_password(self, cleartext_password):
        "Runs cleartext_password through the hash algorithm before saving."
        password_hash = identity.encrypt_password(cleartext_password)
        self._SO_set_password(password_hash)

    def set_password_raw(self, password):
        "Saves the password as-is to the database."
        self._SO_set_password(password)


class Permission(SQLObject):
    """
    A relationship that determines what each Group can do
    """
    permission_name = UnicodeCol(length=16, alternateID=True,
                                 alternateMethodName='by_permission_name')
    description = UnicodeCol(length=255)

    groups = RelatedJoin('Group',
                         intermediateTable='group_permission',
                         joinColumn='permission_id',
                         otherColumn='group_id')

class Idea(SQLObject):
    """
    The main concept - an Idea. This will hold the main text of the idea, along
    with attributes such as Status, Category etc.
    """
    title = StringCol()
    date = DateCol()
    text = UnicodeCol()
    status = ForeignKey("Status")
    categories = RelatedJoin("Category")
    user = ForeignKey("User")
    notes = RelatedJoin("Note")
    actions = RelatedJoin("Action")
    ideas = MultipleJoin("Idea")
    attachments = MultipleJoin("Attachment")

class Note(SQLObject):
    date = DateCol()
    text = UnicodeCol()
    user = ForeignKey("User")
    idea = RelatedJoin("Idea")
    action = RelatedJoin("Action")

class Action(SQLObject):
    date = DateCol()
    text = UnicodeCol()
    complete = BoolCol()
    assigned_by = ForeignKey("User")
    assigned_to = ForeignKey("User")
    idea = RelatedJoin("Idea")
    notes = RelatedJoin("Note")

class Attachment(SQLObject):
    date = DateCol()
    filename = StringCol()
    url = StringCol()
    user = ForeignKey("User")
    idea = ForeignKey("Idea")

    def thumb_url(self):
        url = self.url
        h, t = url.rsplit('.', 1)

        return "%s-thumb.%s" % (h, t)

class Category(SQLObject):
    name = StringCol(alternateID=True)
    ideas = RelatedJoin("Idea")

class Status(SQLObject):
    name = StringCol(alternateID=True)

