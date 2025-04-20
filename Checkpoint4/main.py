# Project: Edge Connectivity Augmentation on Simple Graphs Title.md
from graph_utils import generate_random_graph, get_complement_graph
from augmentation import augment_graph_via_matching
# from connectivity import compute_edge_connectivity, is_k_plus_1_edge_connected
from visualize import draw_graph
# from constants import NUM_NODES, EDGE_PROBABILITY, CONNECTIVITY_LEVEL
import networkx as nx

def compute_edge_connectivity(G):
    return nx.edge_connectivity(G)

def is_k_plus_1_edge_connected(G, k):
    return compute_edge_connectivity(G) >= k + 1

NUM_NODES = 10
EDGE_PROBABILITY = 0.4
CONNECTIVITY_LEVEL = 2

def main():
    G = generate_random_graph(NUM_NODES, EDGE_PROBABILITY)
    draw_graph(G, "Original Graph")
    print(f"Original edge connectivity: {compute_edge_connectivity(G)}")

    G_aug, added_edges = augment_graph_via_matching(G, CONNECTIVITY_LEVEL)
    draw_graph(G_aug, "Augmented Graph", highlight_edges=added_edges)
    print(f"New edge connectivity: {compute_edge_connectivity(G_aug)}")
    print(f"Edges added: {added_edges}")

if __name__ == "__main__":
    main()
