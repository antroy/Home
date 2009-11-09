import re

class TagNode(object):
    def __init__(self, parent, closing_tag, action):
        self.parent = parent
        self.closing_tag = closing_tag
        self.action = action
        self.children = []

        if parent:
            parent.children.append(self)

    def __str__(self):
        out = []

        for child in self.children:
            out.append(str(child))

        return self.action("\n".join(out))

class TextNode(object):
    def __init__(self, parent, content):
        self.parent = parent
        self.content = content

        if parent:
            parent.children.append(self)

    def __str__(self):
        return self.content

class Parser(object):
    def __init__(self, command_map, custom_map=None):
        commands = [("[%s[" % k, ("]]", v)) for k, v in command_map.iteritems()]
        self.command_map = dict(commands)
       
        if custom_map:
            self.command_map.update(custom_map)

        delimiters = set()
        for k, v in self.command_map.iteritems():
            delimiters.add(k)
            delimiters.add(v[0])
        
        delimiters = list(delimiters)
        delimiters.sort()
        delimiters.reverse()

        split_string = "(" + "|".join(map(re.escape, delimiters)) + ")"
        self.splitter = re.compile(split_string)

    def parse(self, text):
        parts = re.split(self.splitter, text)
        self.build_tree(parts)

    def build_tree(self, parts):
        root = TagNode(None, "", surround("<html><body>", "</body></html>"))
        node_stack = [root]

        for i, part in enumerate(parts):
            if not part:
                continue

            if i % 2:
                if part == node_stack[-1].closing_tag:
                    node_stack.pop()
                elif part in self.command_map.keys():
                    closing_tag, command = self.command_map[part]
                    node = TagNode(node_stack[-1], closing_tag, command)
                    node_stack.append(node)
            else:
                node = TextNode(node_stack[-1], part)
            
        self.tree = root

    def print_tree(self):
        print str(self.tree)

def surround(start, finish):
    def _out(text):
        return "".join([start, text, finish])
    return _out

def replace(replacement):
    def _out(text):
        return replacement
    return _out


def parse(text):
    commands = dict(i=surround("<i>", "</i>"), b=surround("<b>", "</b>"), br=replace("<br />"))
    custom_commands = {"'''": ("'''", surround("<b>", "</b>")), 
            "''": ("''", surround("<i>", "</i>")),
            "== ": (" ==", surround("<h1>","</h1>")),
            r"\u{": ("}", surround('<span style="text-decoration: underline">',"</span>")),
            "=== ": (" ===", surround("<h2>","</h2>"))
            }
    parser = Parser(commands, custom_commands)
    parser.parse(text)
    parser.print_tree()


if __name__ == "__main__":
    text = """
== Heading One ==
    [br[]]This is some text, this is [b[Bold and [i[BOLD ITALIC]] text]] this is the end[br[]]
    and this is [i[Italic text]]

=== Heading 2 ===
    This is '''bob ''italic'' text''' ok?

    Some \u{underlined} text.

    """

    parse(text)

