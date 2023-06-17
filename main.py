from MulticastOverlayNetwork import MulticastOverlayNetwork
from link import Link
from network import Network
from node import Node
from packet import Packet

def main():
    # Initialize network
    network = Network()

    # Add nodes
    for node_data in [(1, '127.0.0.1', 65001), (2, '127.0.0.1', 65002), (3, '127.0.0.1', 65003), 
                      (4, '127.0.0.1', 65004), (5, '127.0.0.1', 65005), (6, '127.0.0.1', 65006), 
                      (7, '127.0.0.1', 65007)]:
        node = Node(*node_data)
        network.add_node(node)

    # Add links
    network.add_link(Link(network.nodes[1], network.nodes[2], 2))
    network.add_link(Link(network.nodes[1], network.nodes[3], 5))
    network.add_link(Link(network.nodes[2], network.nodes[1], 2))
    network.add_link(Link(network.nodes[2], network.nodes[3], 6))
    network.add_link(Link(network.nodes[2], network.nodes[4], 4))
    network.add_link(Link(network.nodes[2], network.nodes[5], 5))
    network.add_link(Link(network.nodes[3], network.nodes[2], 6))
    network.add_link(Link(network.nodes[3], network.nodes[5], 2))
    network.add_link(Link(network.nodes[3], network.nodes[6], 2))
    network.add_link(Link(network.nodes[3], network.nodes[7], 5))
    network.add_link(Link(network.nodes[4], network.nodes[2], 4))
    network.add_link(Link(network.nodes[4], network.nodes[5], 5))
    network.add_link(Link(network.nodes[4], network.nodes[7], 4))
    network.add_link(Link(network.nodes[5], network.nodes[2], 5))
    network.add_link(Link(network.nodes[5], network.nodes[3], 2))
    network.add_link(Link(network.nodes[5], network.nodes[4], 5))
    network.add_link(Link(network.nodes[5], network.nodes[7], 2))
    network.add_link(Link(network.nodes[6], network.nodes[3], 2))
    network.add_link(Link(network.nodes[6], network.nodes[7], 5))
    network.add_link(Link(network.nodes[7], network.nodes[3], 5))
    network.add_link(Link(network.nodes[7], network.nodes[4], 4))
    network.add_link(Link(network.nodes[7], network.nodes[5], 2))
    network.add_link(Link(network.nodes[7], network.nodes[6], 5))
    # Set multicast source and receivers
    multicast_source = network.nodes[1]
    multicast_source.is_source = True
    receivers = [network.nodes[4], network.nodes[6], network.nodes[7]]
    for receiver in receivers:
        receiver.is_receiver = True

    # Create multicast overlay network
    multicast_network = MulticastOverlayNetwork(network)

    # Initialize forwarder credits
    forwarder_credits = {2: 10, 3: 12, 5: 8}
    multicast_network.initialize_credits(forwarder_credits)

    # Run multicast routing
    multicast_network.run_multicast_routing()

    # Print results
    print("Multicast Tree:")
    for node in network.nodes.values():
        print(f"{node}:")
        print(f"  Forwarder: {node.is_forwarder}")
        print(f"  Receiver: {node.is_receiver}")
        print(f"  Source: {node.is_source}")
    
    for receiver in receivers:
        path = multicast_network.get_path_to_receiver(receiver)
        if path:
            links = [src_node.get_link_to(dst_node) for src_node, dst_node in zip(path, path[1:])]
            packet = Packet(source=multicast_source, destination=receiver, links=links)
            packet.send()
            print(f"Sending Node: {multicast_source.id} --> Destination Node: {receiver.id}")
            print("Packet Path: ", end="")
            for node in path:
                print(f"{node.id}-->", end=" ")
            print(f"{receiver.id}")
            print(f"Total Cost: {packet.total_cost}\n")
            packet.send()

if __name__ == "__main__":
    main()
