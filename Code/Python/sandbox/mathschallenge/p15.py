
class pathfinder(object):
    def __init__(self, dim):
        self.x, self.y = dim
        self.current_path =  [[(0,0), 0]]
        self.path_count = 0

    def extend(self):
        if not self.current_path:
            return -1
        node_action = self.current_path[-1]
        node, action = node_action
        next_nodes = self.to_nodes(node)
        status = len(next_nodes)

        if status == 0:
            self.path_count += 1
            return 0
        
        if action < status:
            node_action[1] += 1
        else:
            return 0

        next = [next_nodes[action], 0]
        self.current_path.append(next)

        return 1
    
    def backtrack(self):
        self.current_path.pop()

    def run(self):
        while True:
            code = self.extend()

            if code == 0:
                self.backtrack()
            elif code == -1:
                break

    def to_nodes(self, node):
        x, y = node
        out = []
        if x < self.x:
            out.append((x + 1, y))
        if y < self.y:
            out.append((x, y + 1))
        return out


def print_paths():
    p = get_paths()
    print "Count: ", len(p)

import sys
#dims = map(int, sys.argv[1:3])
for i in range(1,9):
    pf = pathfinder((i,i))
    pf.run()
    print "%dx%d: %d (2**(2*%d - 2): %d)" % (i,i,pf.path_count, i, 2**(2*i - 2))


