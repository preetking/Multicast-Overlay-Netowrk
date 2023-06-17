from link import Link

class Node:
    def __init__(self, node_id, ip, port):
        self.id = node_id
        self.ip = ip
        self.port = port
        self.links = []
        self.is_source = False
        self.is_receiver = False
        self.is_forwarder = False
        self.neighbors = {}

    def __repr__(self):
        return f"Node {self.id} ({self.ip}:{self.port})"

    def __lt__(self, other):
        return self.id < other.id

    def add_neighbor(self, neighbor, cost):
        self.neighbors[neighbor] = cost

    def get_link_to(self, other_node):
        for neighbor, cost in self.neighbors.items():
            if neighbor == other_node:
                return Link(self, neighbor, cost)
        return None
