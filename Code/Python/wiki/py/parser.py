import re

class Node(object):
    def __init__(self, parent, action, tag=None, content=None):
        self.parent = parent
        self.action = action
        self.tag = tag
        self.content = content
        self.children = []

        if parent:
            parent.children.append(self)

    def __str__(self):
        out = []
        if self.tag:
            out.append(self.action[0])
        elif self.content:
            out.append(self.content)
        
        for child in self.children:
            out.append(str(child))

        if self.tag:
            out.append(self.action[1])
        

        return "\n".join(out)

class Parser(object):
    def __init__(self, command_map):
        self.command_map = command_map
        self.splitter = re.compile(r"(\[\w+\[|\]\])")

    def parse(self, text):
        parts = re.split(self.splitter, text)
        self.build_tree(parts)

    def build_tree(self, parts):
        root = Node(None, ("<html><body>", "</body></html>"), tag="ROOT")
        node_stack = [root]

        for i, part in enumerate(parts):
            if not part:
                continue

            if i % 2:
                tag = part.strip("[]")
                if tag:
                    node = Node(node_stack[-1], self.command_map[tag], tag=tag)
                    node_stack.append(node)
                else:
                    node_stack.pop()
            else:
                node = Node(node_stack[-1], None, content=part)
            
        self.tree = root

    def print_tree(self):
        print str(self.tree)

def parse(text):
    commands = dict(i=("<i>", "</i>"), b=("<b>", "</b>"), br=("<br />", ""))
    parser = Parser(commands)
    parser.parse(text)
    parser.print_tree()


if __name__ == "__main__":
    text = """
    [br[]]This is some text, this is [b[Bold and [i[BOLD ITALIC]] text]] this is the end[br[]]
    and this is [i[Italic text]]
    """

    parse(text)
