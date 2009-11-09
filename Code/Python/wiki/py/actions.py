from os import sep
import os, os.path as path, logging, adapter
import wiki_parser as w_p
import wiki_interpreter as w_i

LOG = logging.getLogger('wiki-actions')

class abstract_action(object):
    def __init__(self, adapter, action=""):
        self.adapter = adapter
        self.action = action
        
    def run(self):
        pass

class shutdown_action(abstract_action):
    def run(self):
        print "Shutdown Action"
        self.adapter.shutdown()
        return 0
        
class show_all_pages_action(abstract_action):
    def run(self):
        print "Show All Pages Action"
        files = os.listdir(adapter.wiki_dir)
        wikifiles = [x.split('.')[0] for x in files if x.endswith(".txt")]
        wikifiles.sort()
        content = "\n".join(wikifiles)
        parser = w_p.parser(content)
        self.adapter.show_page("AllPages", parser.parsed_text(), "now")
        return 0
        
class root_page_action(abstract_action):
    def run(self):
        print "Root Page Action"
        self.adapter.redirect(path.join(self.adapter.get_context_path(), "IndexPage"))
        return 0
        
class show_wiki_page_action(abstract_action):
    def run(self):
        self.adapter.show_wiki_page()
        return 0
        
class show_raw_page_action(abstract_action):
    def run(self):
        self.adapter.show_raw_page()
        return 0
        
class show_edit_page_action(abstract_action):
    def run(self):
        self.adapter.show_edit_page()
        return 0
        
class show_history_action(abstract_action):
    def run(self):
        self.adapter.show_history_page()
        return 0

class view_history_action(abstract_action):
    def run(self):
        self.adapter.view_history_page()
        return 0

class rollback_history_action(abstract_action):
    def run(self):
        self.adapter.rollback_history()
        return 0

class default_action(abstract_action):
    acceptable_extensions = [".css",".js",".jpg",".png",".gif",".html",".htm"]
    def run(self):
        if self.acceptable_request(self.adapter.get_path()):
            self.reply_to_standard_request()
            return 0
        else:
            return self.adapter.send_error(404,'File Not Found: %s' % self.adapter.get_path())
            
    def acceptable_request(self, filepath):
        LOG.debug("Filepath: " + filepath)
        exts = self.acceptable_extensions
        p, ext = path.splitext(filepath)
        return ext in exts

    def reply_to_standard_request(self):
        p, ext = path.splitext(self.adapter.get_path())
        resource_path = path.join(adapter.static_dir, self.adapter.get_path()[1:])
        resource_path = path.abspath(resource_path)
        
        LOG.debug("Resource requested: %s" % resource_path)
        
        f = open(resource_path)
        data = f.read()
        f.close()
        self.adapter.send_response(data, self.adapter.type_map.get(ext))

class action_map(object):
    
    override_actions = {'shutdown': shutdown_action}
    special_pages = {'AllPages': show_all_pages_action, '': root_page_action}
    normal_actions = {'edit': show_edit_page_action, 'raw': show_raw_page_action, \
                      'history': show_history_action, 'viewhistory': view_history_action, \
                      'rollback': rollback_history_action}
    
    def __init__(self, adapter, name, query):
        self.adapter = adapter
        self.name = name
        self.action = query
        LOG.debug("Page Name: " + name)
        LOG.debug("Page Query: " + query)
        
    def get_action(self):
        action = None
        if self.override_actions.has_key(self.action):
            LOG.debug("Override Action called: " + self.action)
            action_class = self.override_actions[self.action]
            return action_class(self.adapter)
        
        if self.special_pages.has_key(self.name):
            LOG.debug("Special Page called: " + self.name)
            action_class = self.special_pages[self.name]
            return action_class(self.adapter, self.action)
            
        if w_i.isWikiWord(self.name):
            action_class = self.normal_actions.get(self.action, show_wiki_page_action)
            return action_class(self.adapter)
            
        return default_action(self.adapter)
    

