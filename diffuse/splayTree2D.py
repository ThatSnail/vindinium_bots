class SplayTree2D:
    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, x, y, value):
        if self.root == None:
            self.root = Node2D(x, y, value)
            return
        node = self.root
        newNode = None
        while True:
            if x < node.x:
                if y < node.y:
                    nextNodeS = "llNode"
                else:
                    nextNodeS = "lgNode"
            else:
                if y < node.y:
                    nextNodeS = "glNode"
                else:
                    nextNodeS = "ggNode"
            nextNode = getattr(node, nextNodeS)
            if nextNode == None:
                newNode = Node2D(x, y, value, node)
                setattr(node, nextNodeS, newNode)
                break
            node = nextNode
        newNode.splay()

    def find(self, x, y):
        node = self.root
        while (x, y) != (node.x, node.y):
            if x < node.x:
                if y < node.y:
                    node = node.llNode
                else:
                    node = node.lgNode
            else:
                if y < node.y:
                    node = node.glNode
                else:
                    node = node.ggNode
            if node == None:
                return
        node.splay()
        return node.value

class Node2D:
    def __init__(self, x, y, value, parent=None):
        self.x = x
        self.y = y
        self.value = value
        self.parent = parent

        self.llNode = None
        self.lgNode = None
        self.glNode = None
        self.ggNode = None

    def splay(self):
        while self.parent != None:
            if self.parent.parent == None:
                # Zig
            else:
                if self == self.parent.
