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

def generate_graph_from_edges(edges):
    G = nx.Graph()
    G.add_edges_from(edges)
    return G

from connectivity import is_k_plus_1_edge_connected

def verify_augmentation(original_edges, new_edges, k):
    G = nx.Graph()
    G.add_edges_from(original_edges)
    G.add_edges_from(new_edges)
    return is_k_plus_1_edge_connected(G, k)
