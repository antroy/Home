import re, wiki_interpreter as w_i, props

class parser:
    NO_BR = "~~~"
    
    def __init__(self, content):
        self.__raw_text = content
        self.__wiki_text = self.__raw_text.split("\n")
        self.parse()
    
    def parse(self):
        self.process_lines()
        self.process_blocks()
        self.process_lists()
        self.process_tables()
        
        self.add_br()
        
        self.html_output = "\n".join(self.__wiki_text)
        return self.html_output

    def process_lines(self):
        """ 
        This method does the basic first pass over the text.
        The things in here can only appear on a single line.
        """
        new_lines = []
        
        in_table = False
        in_list = False
        in_pre  = False
        list_stack = []
        
        for line in self.__wiki_text:
            if line.startswith('|') and not in_table:
                new_lines.append('<table class="wiki_table">')
                in_table = True
            if in_table and not line.startswith('|'):
                new_lines.append('</table>')
                in_table = False
            if in_table:
                new_lines.append('<tr><td>')
                line = re.sub(r"\|(.*)\|", r"\1", line)
                line = re.sub(r"\|", r"</td><td>", line)
            
            if line.startswith('</pre>'):
                in_pre = False
            if in_pre:
                line = re.sub(r'\&(\s)',r'&amp;\1', line)
                line = line.replace('<','&lt;')
                line = self.NO_BR + line
                new_lines.append(line)
                continue
            if line.startswith('<pre>'):
                in_pre = True
            
            p = re.compile(r"^(\*+|\#+)(.*)")
            m = p.match(line)
            
            if m:
                list_type = 'ul'
                if m.group(1)[:1] == '#':
                    list_type = 'ol'
                if len(m.group(1)) > len(list_stack):
                    list_stack.append(list_type)
                    li = '' #'<li>'
                    if len(list_stack) <= 1:
                        li = ''
                    new_lines.append('%s<%s>' % (li, list_type))
                else:
                    while len(m.group(1)) < len(list_stack):
                        lst = list_stack.pop()
                        new_lines.append('</%s>' % lst)
                line = "<li>%s</li>" % m.group(2)
            else:
                while len(list_stack) > 0:
                    close_li = '' #'</li>'
                    if len(list_stack) == 1:
                        close_li = ''
                    new_lines.append("</%s>%s" % (list_stack.pop(), close_li))
                
            line = re.sub("----\s*","<hr />", line)
            line = self.process_links(line)
            def do_header(match):
                equals = match.group(1)
                text = match.group(2)
                number = str(len(equals) + 1)
                out = "<h%s>%s</h%s>" % (number, text, number)
                return out
            
            line = re.sub(r"^(=+) (.*?)\1", do_header, line)
            line = re.sub(r"'''''(.*?)'''''",r"<strong><i>\1</i></strong>", line)
            line = re.sub(r"--(.*?)--",r'<span class="strikeout">\1</span>', line)
            line = re.sub(r"'''(.*?)'''",r"<strong>\1</strong>", line)
            line = re.sub(r"''(.*?)''",r"<i>\1</i>", line)
            line = re.sub(r"\{\{\{(.*?)\}\}\}",r"<code>\1</code>", line)
            
            new_lines.append(line)
            
            if in_table:
                new_lines.append('</td></tr>')
            
        self.__wiki_text = new_lines
        
    def add_br(self):
        tags = ['hr','td','tr','table','li','ul','ol',r'h\d','p','div']
        end = r'^.*?<(/\s*)?(%s)[^>]*>\s*$' % "|".join(tags)
        start = r'^\s*<(/\s*)?(%s)[^>]*>.*?$' % "|".join(tags)
        endpattern = re.compile(end)
        startpattern = re.compile(start)
        
        out = []
        prev = None
        firstline = True
        
        for line in self.__wiki_text:
            explicit = line.startswith(self.NO_BR)
            match = endpattern.match(line)
            
            if not firstline and not (prev or match or explicit):
                out.append('<br />')
            
            if explicit:
                line = line[len(self.NO_BR):]
            
            if firstline: firstline = False
            
            prev = match
            out.append(line)
            
        self.__wiki_text = out
        
    def process_blocks(self):
        """
        Looks for block level syntax, and processes them accordlingly
        """
        
        
    def process_lists(self):
        """
        This method needs to look for list syntax and process accordingly
        """
        pass
    
    def process_tables(self):
        """
        This method looks for table syntax, and processes accordingly.
        """
        pass
        
    def process_links(self, line):
        out = line
        
        # >>> exp = r"(?:\[\[([^]]+)\]\[)?\b(https?://[^]]+)(?:]])?"
        # >>> p = re.compile(exp)
        # >>> print re.sub(exp, fn, s)
        # testing bob testing
        # >>> m = p.search(s)
        # >>> print m.groups()
        # ('Bob is a Girl', 'http://google.com?s=bob')
        # >>> m = p.search("Testing http://test.com testing")
        # >>> print m.groups()
        # (None, 'http://test.com testing')
        
        exp = r"\[\[([^]]+)\]\[([^]]+)\]\]"
        out = re.sub(exp, r"<a class='linkOut' href='\2'>\1</a>", out)
        if out != line:
            return out

        out = re.sub(r"\b((https?|file|ftp)://\S+)", r"<a class='linkOut' href='\1'>\1</a>", out)
        out = re.sub(r"\b(mailto:\S+)", r"<a class='mailLink' href='\1'>\1</a>", out)
        
        if out == line:
            out = re.sub(parser.wiki_word_pattern, parser.process_wiki_link, out)
        
        return out
        
    def parsed_text(self):
        return self.html_output

    wiki_word_pattern = re.compile(r"((?:[A-Z][a-z]+){2,})")
        
    def process_wiki_link(match):
        link = match.group(1)
        interp = w_i.wiki_interpreter(link)
        if interp.exists  or link in props.special:
            return parser.wiki_link(link)
        else:
            return link + parser.wiki_link(link, '?', 'action=edit')
    process_wiki_link = staticmethod(process_wiki_link)
                
    def wiki_link(title, link_text="", command=""):
        if not command == "":
            command = "?" + command
        if link_text == "":
            link_text = title
        return r"<a class='wikilink' href='%s%s'>%s</a>" % (title, command, link_text)
    wiki_link = staticmethod(wiki_link)
    
    
