from kid import Template

class Node (object):
    def __init__(self, name, children=[]):
        self.children = children
        self.name = name
    
    def children(self):
        return self.children


top = Node("top")
a = Node("A", [Node("a")])
b = Node("B", [Node("x"),Node("y")])
top.children = [a, b]
        

template = Template(name="xx")
template.tree = top
print template.serialize(output='html')
