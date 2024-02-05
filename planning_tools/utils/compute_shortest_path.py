import networkx as nx

def compute_shortest_path(G: nx.Graph, source_name: str = "", target_name: str = ""):
    source = None
    target = None
    for node in G.nodes:
        if node.name == source_name:
            source = node
        if node.name == target_name:
            target = node

    if source is None:
        raise ValueError(f"Source node '{source_name}' not found in the graph.")
    if target is None:
        raise ValueError(f"Target node '{target_name}' not found in the graph.")

    shortest_path = nx.shortest_path(G, source=source, target=target, weight="weight")
    return shortest_path
