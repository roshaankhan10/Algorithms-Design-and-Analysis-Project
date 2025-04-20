from augmentation import augment_graph_via_matching
from connectivity import is_k_plus_1_edge_connected
from graph_utils import generate_graph_from_edges
from itertools import combinations
from augmentation import augment_connectivity
import unittest
from graph_utils import verify_augmentation
import networkx as nx


class TestEdgeConnectivityAugmentation(unittest.TestCase):
    def test_4_cycle(self):
        edges = [(0,1), (1,2), (2,3), (3,0)]
        k = 2
        new_edges = augment_connectivity(edges, k)
        self.assertEqual(len(new_edges), 2)
        self.assertTrue(verify_augmentation(edges, new_edges, k))
    
    def test_complete_graph(self):
        edges = list(combinations(range(4), 2))  # K4
        k = 3
        new_edges = augment_connectivity(edges, k)
        self.assertEqual(len(new_edges), 0)
    
    def test_path_augmentation_case(self):
        # Graph where complement has no perfect matching
        edges = [(0,1), (1,2), (2,3), (3,4), (4,5), (5,0), (0,2), (3,5)]
        k = 2
        new_edges = augment_connectivity(edges, k)
        self.assertTrue(verify_augmentation(edges, new_edges, k))
        self.assertTrue(2 <= len(new_edges) <= 3)

if __name__ == '__main__':
    unittest.main()