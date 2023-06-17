class Packet:
    def __init__(self, source, destination, links=None):
        self.source = source
        self.destination = destination
        self.links = links or []
        self.total_cost = sum(link.cost for link in self.links)

    def add_link(self, link):
        self.links.append(link)
        self.total_cost += link.cost

    def send(self):
        dest = self.destination
        path = " --> ".join([str(link.node1.id) for link in self.links])
        path += f" --> {dest.id}"

