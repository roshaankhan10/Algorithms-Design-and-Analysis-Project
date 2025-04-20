import networkx as nx
import random

def generate_random_graph(n, p):
    G = nx.erdos_renyi_graph(n, p)
    while not nx.is_connected(G):
        G = nx.erdos_renyi_graph(n, p)
    return G

def get_complement_graph(G):
    return nx.complement(G)

def get_vertices_of_degree_k(G, k):
    return [v for v, d in G.degree() if d == k]

def get_subgraph_by_vertices(G, vertices):
    return G.subgraph(vertices).copy()
