import smtplib, os
from email import Encoders
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.MIMENonMultipart import MIMENonMultipart

default_server = "relay.plus.net"
default_port = 25
default_user = None
default_pass = None

mime_types = {
    '.pdf': 'pdf',
    '.doc': 'msword'
}

class Email (object):
    def __init__(self, subject, to, from_address="Anthony Roy<work@antroy.co.uk>"):
        """to is a list of strings."""
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = subject
        msgRoot['From'] = from_address
        msgRoot['To'] = ", ".join(to)
        msgRoot.preamble = 'This is a multi-part message in MIME format.'
                
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        self.root = msgRoot
        self.alternative = msgAlternative
        self.to = to
        self.ccs = []
        self.bccs = []
        self.from_address = from_address
        self.next = 1

    def addCC(self, *ccs):
        self.add_to_field("CC", *ccs)
        self.ccs.extend(ccs)

    def addBCC(self, *bccs):
        self.bccs.extend(bccs)

    def add_to_field(self, field, *items):
        existing_ccs = self.root.get(field, '')
        out = ''

        if existing_ccs:
            out = existing_ccs + ", "

        out += ", ".join(items)
        self.root[field] = out

    def addPlain(self, message):
        msgText = MIMEText(message)
        self.alternative.attach(msgText)

    def addHtml(self, message):
        msgText = MIMEText(message, "html")
        self.alternative.attach(msgText)

    def addImage(self, path, id=None):
        """Refer to the image in the HTML message like so:
        <img src="cid:id">"""
        filename = os.path.split(path)[-1]
        fp = open(path, 'rb')
        msgImage = MIMEImage(fp.read(), name=filename)
        fp.close()

        if id == None:
            id = "attach_%s" % self.next
            self.next += 1

        msgImage.add_header('Content-ID', id)
        self.root.attach(msgImage)

    def addAttachment(self, path):
        filename = os.path.split(path)[-1]
        ext = os.path.splitext(filename)[-1]

        subtype = mime_types.get(ext, "octet-stream")

        msgAttachment = MIMENonMultipart("application", subtype, name=filename)

        fp = open(path, 'rb')
        msgAttachment.set_payload(fp.read())
        fp.close()

        Encoders.encode_base64(msgAttachment)

        id = "attach_%s" % self.next
        self.next += 1

        msgAttachment.add_header('Content-ID', id)
        self.root.attach(msgAttachment)

    def __str__(self):
        return self.root.as_string()

class SMTP (object):
    def __init__(self, server=default_server, port=default_port, user=default_user, passwd=default_pass):
        self.server = server
        self.user = user
        self.port = port
        self.passwd = passwd
        self.tls = False

    def send(self, email):
        """The email parameter must be an Email object."""
        smtp = smtplib.SMTP(self.server, self.port)
        smtp.ehlo()
        
        if self.tls:
            smtp.starttls()
            smtp.ehlo()

        if self.user and self.passwd:
            smtp.login(self.user, self.passwd)

        smtp.sendmail(email.from_address, email.to + email.ccs, str(email))
        if email.bccs:
            email.root['X-antroy-sent'] = "True"
            smtp.sendmail(email.from_address, email.bccs, str(email))
            del email.root['X-antroy-sent']
        smtp.quit()

if __name__ == "__main__":
    email = Email("Test", ["home@antroy.co.uk"])
    email.addPlain("The message")
    email.addHtml('<html><b>BOLD</b> other stuff.<img src="cid:my_id">')
    email.addImage(r"C:\0\DSC01403.JPG", "my_id")
    email.addAttachment(r"C:\0\test.doc")

    server = SMTP()
    server.send(email)



