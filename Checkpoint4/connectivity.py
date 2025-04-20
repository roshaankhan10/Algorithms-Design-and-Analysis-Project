from itertools import combinations
import networkx as nx
import random
import unittest
def is_k_plus_1_edge_connected(G, k):
    return nx.edge_connectivity(G) >= k + 1