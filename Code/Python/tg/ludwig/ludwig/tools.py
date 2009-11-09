import smtplib, os.path
import datetime
from model import *
from turbogears import identity, redirect, config
import logging

log = logging.getLogger(__name__)
log.addHandler(logging.FileHandler(config.get("log_file")))

def send_mail(idea_id, subject, action_id=None, note_id=None, attach_id=None):
    idea = Idea.get(idea_id)

    if action_id:
        text = Action.get(action_id).text
    elif note_id:
        text = Note.get(note_id).text
    elif attach_id:
        file = Attachment.get(attach_id).url
        text = os.path.split(file)[1]
    else:
        text = idea.text

    from_ = '"Ludwig" <work@antroy.co.uk>'
    name_info = [(u.display_name, u.email_address) for u in User.select()]
    to = [x[1] for x in name_info]
    to_header = ", ".join('"%s" <%s>' % x for x in name_info)

    date_ = datetime.now()
    datestr = date_.strftime("%a, %d %b %Y %H:%M:%S -0000")

    data = dict(id=idea_id, title=idea.title,
                base_url=config.get("ludwig.baseurl"),
                text=text, from_addr=from_, to_addrs=to_header,
                date=datestr)
    data['subject'] = subject % data

    message = u"""Idea URL:
%(base_url)s/idea?id=%(id)s

==================   Item Text   ===========================

%(text)s

============================================================

""" % data
    data['message'] = message

    msg = u"From: %(from_addr)s\r\nTo: %(to_addrs)s\r\nDate: %(date)s\r\nSubject: %(subject)s\r\n\r\n%(message)s" % data

    msg = msg.encode("utf-8")
    log.debug("SMTP: " + config.get("smtp.server"))
    log.debug("To: %s" % to)
    log.debug("From: " + from_)
    log.debug("Text: " + msg)

    server = smtplib.SMTP(config.get("smtp.server"))
    server.set_debuglevel(1)
    server.sendmail(from_, to, msg)
    server.quit()


