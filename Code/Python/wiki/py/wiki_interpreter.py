import re, os.path as path, wiki_parser as w_p, props, logging, adapter, cgi
from datetime import datetime
from os import sep

LOG = logging.getLogger('wiki-interpreter')

class wiki_interpreter:
    def __init__(self, page, rawText=None):
        LOG.debug(adapter.wiki_dir)
        self.title = path.basename(page)
        self.wikipath = path.join(adapter.wiki_dir, self.title + ".txt")
        self.content = rawText
        
        LOG.debug("Wiki directory path: " + self.wikipath)
        LOG.debug("Wiki Page: " + page)
        
        if path.exists(self.wikipath):
            self.exists = True
            self._last_modified = path.getmtime(self.wikipath)
        else:
            self.exists = False
            self._last_modified = datetime.now()
        
    def load(self):
        if not self.content:
            if self.exists:
                f = open(self.wikipath)
                self.content = f.read()
                f.close()
            else:
                self.content = ""
        return self
        
    def raw_content(self):
        return self.content
    
    def last_modified(self):
        lastmod = datetime.fromtimestamp(self._last_modified)
        return lastmod.strftime("%d-%m-%Y %H:%M")
        
    def parsed_content(self):
        try:
            return self.processed_content
        except AttributeError:
            return self.process()
    
    def process(self):
        parser = w_p.parser(self.content)
        
        self.processed_content = parser.parsed_text()
        return self.processed_content


class path_parser:
    def __init__(self, pth):
        reqpath, name = path.split(pth)
        name_act = name.split('?')
        self.name = name_act[0]
        self.action = ''
        self.attributes = {}
        if len(name_act) > 1:
            query = name_act[1]
            
            pairs = cgi.parse_qs(query)
            
            self.action = pairs['action'][0]
            LOG.debug("Action %s requested." % self.action)
            self.attributes = pairs
        
            
def process_wiki_link(match):
    link = match.group(1)
    interp = wiki_interpreter(link)
    print "LINK:", link
    if interp.exists or link in props.special:
        return wiki_link(link)
    else:
        return link + wiki_link(link, '?', 'edit')
        
wiki_word_pattern = re.compile(r"((?:[A-Z][a-z]+){2,})")
            
def wiki_link(title, link_text="", command=""):
    if not command == "":
        command = "?" + command
    if link_text == "":
        link_text = title
    return r"<a class='wikilink' href='%s%s'>%s</a>" % (title, command, link_text)

def isWikiWord(name):
    """
     Tests whether a string is a valid wiki word or not.
     
     >>> isWikiWord("CamelCase")
     True
     
     >>> isWikiWord("bob")
     False
     
     >>> isWikiWord("TuTu")
     True
     
     >>> isWikiWord("javaWord")
     False
     
     >>> isWikiWord("TestHTMLCode")
     False
     """
    if wiki_word_pattern.match(name):
        return True
    else:
        return False
    
class trail:
    def __init__(self, maximum=10):
        self.__trail = []
        self.__max_size = 10
    
    def update(self, title):
        try:
            index = self.__trail.index(title)
            print "INDEX: ", index
            self.__trail = self.__trail[:index]
        except ValueError:
            print title, "Not Found!", self.__trail
        length = len(self.__trail)
        maxlen = self.__max_size
        if length > maxlen:
            self.trail = self.trail[length - maxlen:]
        self.__trail.append(title)
        
    def trail_html(self):
        traillinks = map(wiki_link, self.__trail[:len(self.__trail)-1])
        trailstring = " > ".join(traillinks) 
        return trailstring
    
if __name__ == "__main__":
    print "Running Tests..."
    
    import doctest, sys
    doctest.testmod(sys.modules[__name__])

