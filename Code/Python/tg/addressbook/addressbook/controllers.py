from turbogears import controllers, expose, flash
from model import *
from turbogears import identity, redirect
from cherrypy import request, response
import re
# from addressbook import json
# import logging
# log = logging.getLogger("addressbook.controllers")

def get_header():
    out = """
    <div id="header">
        <div class="left">
            <a href="." class="header_link" alt="Index">All Contacts</a> |
            <a href="new" class="header_link" alt="Add Contact">Add Contact</a>
        </div>
        <div class="right">
            <a href="logout" alt="Log out">Log out</a>
        </div>                                
    </div>
    """
    return out

class Root(controllers.RootController):
    @expose(template="cheetah:addressbook.templates.index")
    # @identity.require(identity.in_group("admin"))
    def index(self):
        flash("Your application is now running")

        out = {}

        out['title'] = "Addressbook"
        out['tagname'] = None
        out['contacts'] = Contact.select()
        out['tags'] = Tag.select()
        out['header'] = get_header()

        return out

    @expose(template="cheetah:addressbook.templates.index")
    # @identity.require(identity.in_group("admin"))
    def quickadd(self, details):
        contact_re = re.compile(r"^(?:\((\w+)\)|(\w)):\s*(.*)$")
        contact_map = dict(t="Phone", m="Mobile", f="Fax", e="Email", w="Web")

        details = details.split("\n")
        if not details:
            return

        first, last = details[0].rsplit(None, 1)

        contacts = []
        addresses = []
        current_address = []

        for line in details[1:]:
            line = line.strip()
            m = contact_re.match(line)
            if m:
                if current_address:
                    addresses.append(current_address)
                    current_address = []
                key = contact_map.get(m.group(1), m.group(1))
                contacts.append( ContactItem( method=key, information=m.group(2) ) )
            else:
                current_address.append(line)

        if current_address:
            addresses.append(current_address)

        contact = Contact(first_name=first, last_name=last)
        #personal = ContactGroup()
        #for con in contacts:
        #    personal.addContactItem(con)

        #contact.addContactGroup(personal)

        return self.index()

    @expose(template="cheetah:addressbook.templates.new")
    # @identity.require(identity.in_group("admin"))
    def new(self):
        out = {}

        out['title'] = "Addressbook"
        out['tagname'] = None
        out['contacts'] = Contact.select()
        out['tags'] = Tag.select()
        out['header'] = get_header()

        return out

    @expose(template="addressbook.templates.login")
    def login(self, forward_url=None, previous_url=None, *args, **kw):

        if not identity.current.anonymous \
            and identity.was_login_attempted() \
            and not identity.get_identity_errors():
            raise redirect(forward_url)

        forward_url=None
        previous_url= request.path

        if identity.was_login_attempted():
            msg=_("The credentials you supplied were not correct or "
                   "did not grant access to this resource.")
        elif identity.get_identity_errors():
            msg=_("You must provide your credentials before accessing "
                   "this resource.")
        else:
            msg=_("Please log in.")
            forward_url= request.headers.get("Referer", "/")
            
        response.status=403
        return dict(message=msg, previous_url=previous_url, logging_in=True,
                    original_parameters=request.params,
                    forward_url=forward_url)

    @expose()
    def logout(self):
        identity.current.logout()
        raise redirect("/")
