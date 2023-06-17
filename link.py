class Link:
    def __init__(self, node1, node2, cost):
        self.node1 = node1
        self.node2 = node2
        self.cost = cost

    def __str__(self):
        return f"Link between {self.node1} and {self.node2} with cost {self.cost}"
