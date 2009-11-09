import re

def __get_patterns(text, regex):
    out = text

    if isinstance(text, str):
        out = [text]
        
    if regex:
        out = [re.compile(p, re.MULTILINE | re.DOTALL) for p in out]
  
    return out

def __find(pattern, page, regex):
    if regex:
        return bool(pattern.search(page))
    else:
        return page.find(pattern) > -1
    
def get_text_present_asn(patt, regex=False):
    """Returns an assertion function which returns True if the specified text or
    pattern is found in the page. The parameter patt can be either a string or
    a list of strings. If the latter, all strings in the list must be found
    for the function to return True. If regex is True patt is compiled as a 
    regex before the search is made.
    """
    patterns = __get_patterns(patt, regex)

    def text_present_asn(page):
        for pattern in patterns:
            found = __find(pattern, page, regex)
            if not found:
                return False
        return True
            
    text_present_asn.assertion = True 
       
    return text_present_asn
    
def get_text_not_present_asn(patt, regex=False):
    """Returns an assertion function which returns True if the specified text or
    pattern is not found in the page. The parameter patt can be either a string or
    a list of strings. If the latter, none of the strings can be found
    for the function to return True. If regex is True patt is compiled as a 
    regex before the search is made.
    """
    patterns = __get_patterns(patt, regex)

    def text_not_present_asn(page):
        for pattern in patterns:
            if __find(pattern, page, regex):
                return False
        return True
            
    text_not_present_asn.assertion = True
       
    return text_not_present_asn
    
    
def get_is_xhtml_asn():
    def is_xhtml_asn(page):
        from elementtree.ElementTree import parse
        import xml.parsers.expat as expat
        from StringIO import StringIO
        try:
            parse(StringIO(page))
            return True
        except expat.ExpatError, ex:
            print "XHTML problem:\n", ex
            return False
    
    is_xhtml_asn.assertion = True
    
    return is_xhtml_asn
    
    
__all__ = ('get_text_present_asn', 'get_text_not_present_asn')
    
# ================================================================
# ==                     T E S T S                              ==
# ================================================================

def __assert(test, success):
    print "Test %s - %s" % (test, ("FAILED", "OK")[success])

if __name__ == "__main__":
    page = """Test stuff here.
    <span>tagged up text</span>
    and <div id="bob">Id tagged stuff</div>
    <p>multi
    line
    paragraph</p>"""

    a1 = "<span>"
    a2 = "bernard"
    b1 = ["Test stuff", "paragraph"]
    b2 = ["Test stooff", "paragroof"]
    c1 = r'<div id=".*?">.*</div>'
    c2 = r'<rubbish>.*</rubbish>'
    d1 = [r"<span>.*?</span>", r"<p>.*</p>", r"^\s*line\s*$"]
    d2 = [r"<span>.*?</splan>", r"<lp>.*</p>", r"^lion$"]

    __assert("Single text Search positive", get_text_present_asn(a1)(page))
    __assert("Single text Search negative", get_text_not_present_asn(a2)(page))
    __assert("Multiple text Search positive", get_text_present_asn(b1)(page))
    __assert("Multiple text Search negative", get_text_not_present_asn(b2)(page))
    __assert("Single regex Search positive", get_text_present_asn(c1, True)(page))
    __assert("Single regex Search negative", get_text_not_present_asn(c2, True)(page))
    __assert("Multiple regex Search positive", get_text_present_asn(d1, True)(page))
    __assert("Multiple regex Search negative", get_text_not_present_asn(d2, True)(page))


