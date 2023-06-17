import heapq
from node import Node
from link import Link
from network import Network
from multicast_socket import MulticastSocket

class MulticastOverlayNetwork:
    def __init__(self, network):
        self.network = network
        self.forwarder_credits = {}

    def initialize_credits(self, forwarder_credits):
        self.forwarder_credits = forwarder_credits

    def dijkstra(self, source):
        dist = {node: float('infinity') for node in self.network.nodes.values()}
        prev = {node: None for node in self.network.nodes.values()}
        dist[source] = 0
        pq = [(0, source)]

        while pq:
            current_dist, current_node = heapq.heappop(pq)

            if current_dist > dist[current_node]:
                continue

            for neighbor, cost in current_node.neighbors.items():
                alt = dist[current_node] + cost
                if alt < dist[neighbor]:
                    dist[neighbor] = alt
                    prev[neighbor] = current_node
                    heapq.heappush(pq, (alt, neighbor))

        return prev

    def build_multicast_tree(self):
        source = None
        receivers = []
        for node in self.network.nodes.values():
            if node.is_source:
                source = node
            elif node.is_receiver:
                receivers.append(node)

        prev = self.dijkstra(source)
        multicast_tree = {receiver: [] for receiver in receivers}

        for receiver in receivers:
            path = []
            node = receiver
            while prev[node]:
                path.append(prev[node])
                node = prev[node]
            multicast_tree[receiver] = path[::-1]

        return multicast_tree

    def assign_forwarders(self, multicast_tree):
        source = None
        for node in self.network.nodes.values():
            if node.is_source:
                source = node
                break

        for receiver, path in multicast_tree.items():
            if len(path) > 1:
                max_credits = -1
                selected_forwarder = None
                for forwarder in path:
                    if forwarder == source:
                        continue
                if self.forwarder_credits[forwarder.id] > max_credits:
                    max_credits = self.forwarder_credits[forwarder.id]
                    selected_forwarder = forwarder
                selected_forwarder.is_forwarder = True
                self.forwarder_credits[selected_forwarder.id] -= 1

    def run_multicast_routing(self):
        multicast_tree = self.build_multicast_tree()
        self.assign_forwarders(multicast_tree)

    def get_path_to_receiver(self, receiver):
        multicast_tree = self.build_multicast_tree()
        return multicast_tree.get(receiver, [])