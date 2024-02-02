import matplotlib.pyplot as plt
import networkx as nx

def draw_graph(G: nx.Graph, source_name: str, target_name: str):
    # search the nodes for the source and target
    source = None
    target = None
    for node in G.nodes:
        if node.name == source_name:
            source = node
        if node.name == target_name:
            target = node

    # if the source or target are not found, raise an error
    if source is None:
        raise ValueError(f"Source node '{source_name}' not found in the graph.")
    if target is None:
        raise ValueError(f"Target node '{target_name}' not found in the graph.")

    # compute the shortest path
    shortest_path = nx.shortest_path(G, source=source, target=target, weight='weight')

    # Position nodes using one of the layout options
    pos = nx.spring_layout(G)

    # Draw the graph
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray')

    # Highlight the shortest path
    path_edges = list(zip(shortest_path, shortest_path[1:]))
    nx.draw_networkx_nodes(G, pos, nodelist=shortest_path, node_color='blue')
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

    # Show the plot
    plt.show()
