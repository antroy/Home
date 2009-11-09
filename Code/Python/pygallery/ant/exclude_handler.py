from mod_python import apache

def handler(req):
    return apache.DECLINED
