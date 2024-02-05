import matplotlib.pyplot as plt
import networkx as nx


def draw_graph(G: nx.Graph, shortest_path: list = []):

    # Position nodes using one of the layout options
    pos = nx.spring_layout(G)

    node_labels = {node: node.name for node in G.nodes}
    # display the weights on the edges, if they exist
    edge_labels = {(edge[0], edge[1]): edge[2].get("weight", "") for edge in G.edges(data=True)}

    # Draw the graph
    nx.draw(G, pos, with_labels=False, node_color="lightblue", edge_color="gray")

    # Highlight the shortest path
    if shortest_path:
        path_edges = list(zip(shortest_path, shortest_path[1:]))
        nx.draw_networkx_nodes(G, pos, nodelist=shortest_path, node_color="blue")
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=2)

    nx.draw_networkx_labels(G, pos, labels=node_labels)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Show the plot
    plt.show()
