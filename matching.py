import networkx as nx

def compute_maximum_matching(G):
    matching = nx.max_weight_matching(G, maxcardinality=True)
    return list(matching)

def get_unmatched_vertices(G, matching):
    matched = set(u for edge in matching for u in edge)
    return [v for v in G.nodes if v not in matched]
