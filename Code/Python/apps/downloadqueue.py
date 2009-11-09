from kid import Template
import sys, os, marshal, urllib, urllib2
import os.path as path

__auth_realm__ = "Go away dude!"
__auth__ = {"ant": "sanmelas"}
__access__ = ["ant"]

_DATA_FILE = "/srv/www/app_data/download_urls.dat"

def index(req):
    try:
        url_list = _get_url_list()
        page = Template(name='downloadform')
        page.url_list = url_list
    except:
        return "Unexpected error: " + str(sys.exc_info()[1])
    return page.serialize(output='html')

def _get_url_list():
    url_list = []
    if path.isfile(_DATA_FILE):
        fh = open(_DATA_FILE, "rb")
        url_list.extend(marshal.load(fh))
        fh.close()
    
    return url_list

def _save_url_list(urls):
    fh = open(_DATA_FILE, "wb")
    marshal.dump(urls, fh)
    fh.close()

def add_url(req):
    urls = _get_url_list()
    new_url = req.form.getfirst('new_url')
    new_url = urllib.unquote(new_url)
    if new_url and _test_url(new_url):
        urls.append((new_url, "In Queue"))
        _save_url_list(urls)

    return index(req)

def _test_url(url):
    try:
        #urlh = urllib2.urlopen(url)
        #urlh.close()
        return True
    except:
        return False

def delete_url(req):
    out = ""
    to_delete = [url.value for url in req.form.list if url.name == 'url']
    original_list = _get_url_list()
    urls = [url for url in original_list if url[0] not in to_delete]
    _save_url_list(urls)

    return index(req)

