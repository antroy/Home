#!/usr/bin/python
import urllib, urllib2, sys

auth = None
userid = "17525563424027503091"
blog_id = "3869421696923778870"

class Info(object):
    def __init__(self, url, method=None, data=None):
        self.url = url
        self.method = method
        self.data = data
        self.auth = None

class Request(urllib2.Request):

    def __init__(self, url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None):
        urllib2.Request.__init__(self, url, data, headers, origin_req_host, unverifiable)
        self.method = method

    def get_method(self):
        if self.method is None:
            if self.data is not None:
                return "POST"
            else:
                return "GET"
        return self.method 

def call_url(inf):
    if inf.data:
        data = urllib.urlencode(inf.data)
    else:
        data = None

    req = Request(inf.url, method=inf.method, data=data)

    if inf.auth:
        req.add_header("Authorization", "GoogleLogin auth=%s" % auth)

    resp = urllib2.urlopen(req)
    resp_info = resp.info()
    out = []

    for line in resp:
        out.append(line)
    
    return out, resp_info

auth_data = {"Email": "antroy@gmail.com", "Passwd": "sloth5b", "source": "antroy-pyblogger-1", "service": "blogger"}
authenticate_info = Info("https://www.google.com/accounts/ClientLogin", "POST", auth_data)
list_posts_info  = Info("http://www.blogger.com/feeds/%s/posts/default" % blog_id, "GET")

def authenticate():
    global auth
    out, info = call_url(authenticate_info)

    for line in out:
        if line.startswith("Auth"):
            auth = line.split("=")[1].strip()

def list_entries():
    list_posts_info.auth = auth
    out, info = call_url(list_posts_info)
    print "\n".join(out)

if __name__ == "__main__":
    authenticate()
    if not auth:
        print "Could not authenticate!"
        sys.exit(1)

    list_entries()

