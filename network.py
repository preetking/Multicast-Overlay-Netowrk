class Network:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        self.nodes[node.id] = node

    def add_link(self, link):
        link.node1.add_neighbor(link.node2, link.cost)
        link.node2.add_neighbor(link.node1, link.cost)
