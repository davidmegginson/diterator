import xpath

class Base:

    def __init__ (self, node):
        self.node = node

    def get_text (self, xpath_expr):
        node = self.get_node(xpath_expr)
        if not node:
            return None
        elif node.nodeType == node.ELEMENT_NODE:
            s = ""
            for child in node.childNodes:
                if child.nodeType == child.TEXT_NODE:
                    s += child.data
            return s
        elif node.nodeType == node.ATTRIBUTE_NODE:
            return node.value
        else:
            raise Exception("Cannot get text for node of type {}".format(node.nodeType))

    def get_node (self, xpath_expr, base_node=None):
        nodes = self.get_nodes(xpath_expr, base_node)
        if len(nodes) == 0:
            return None
        else:
            return nodes[0]

    def get_nodes (self, xpath_expr, base_node=None):
        if base_node is None:
            base_node = self.node
        return xpath.find(xpath_expr, base_node)

class Activity(Base):

    def __init__ (self, node):
        super().__init__(node)

    @property
    def identifier (self):
        return self.get_text("iati-identifier")
