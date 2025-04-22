# from graph_utils import generate_random_graph, get_complement_graph, get_vertices_of_degree_k, get_subgraph_by_vertices
# from augmentation import augment_graph_via_matching
# from matching import compute_maximum_matching
# from visualize import draw_graph
# import networkx as nx

# def compute_edge_connectivity(G):
#     return nx.edge_connectivity(G)

# def is_k_plus_1_edge_connected(G, k):
#     return compute_edge_connectivity(G) >= k + 1

# NUM_NODES = 10
# EDGE_PROBABILITY = 0.4
# CONNECTIVITY_LEVEL = 2

# def main():
#     # Step 1: Generate original graph
#     G = generate_random_graph(NUM_NODES, EDGE_PROBABILITY)
#     print(f"Original edge connectivity: {compute_edge_connectivity(G)}")

#     # Save and display original graph
#     draw_graph(G, title="Original Graph", filename="original_graph.png")

#     # Step 2: Show complement graph
#     G_comp = get_complement_graph(G)
#     draw_graph(G_comp, title="Complement Graph", filename="complement_graph.png")

#     # Step 3: Determine which case (1 or 2)
#     vertices_k = get_vertices_of_degree_k(G, CONNECTIVITY_LEVEL)
#     G_k = get_subgraph_by_vertices(G, vertices_k)
#     complement_G_k = get_complement_graph(G_k)
#     matching = compute_maximum_matching(complement_G_k)

#     if len(matching) * 2 == len(vertices_k):
#         print("Case 1: Matching covers all degree-k vertices.")
#     else:
#         print("Case 2: Matching does NOT cover all degree-k vertices.")

#     # Step 4: Augment graph
#     G_aug, added_edges = augment_graph_via_matching(G, CONNECTIVITY_LEVEL)

#     # Save and display augmented graph
#     draw_graph(G_aug, title="Augmented Graph", highlight_edges=added_edges, filename="augmented_graph.png")

#     # Step 5: Print results
#     print(f"New edge connectivity: {compute_edge_connectivity(G_aug)}")
#     print(f"Edges added: {added_edges}")

# if __name__ == "__main__":
#     main()
from graph_utils import generate_random_graph, get_complement_graph, get_vertices_of_degree_k, get_subgraph_by_vertices
from augmentation import augment_connectivity, compute_edge_connectivity, is_k_plus_1_edge_connected
from matching import compute_maximum_matching
from visualize import draw_graph
import networkx as nx


# from augmentation import is_k_plus_1_edge_connected

NUM_NODES = 10
EDGE_PROBABILITY = 0.4
CONNECTIVITY_LEVEL = 2

def main():
    G = generate_random_graph(NUM_NODES, EDGE_PROBABILITY)
    draw_graph(G, title="Original Graph", filename="original_graph.png")
    print(f"Original edge connectivity: {compute_edge_connectivity(G)}")

    G_comp = get_complement_graph(G)
    draw_graph(G_comp, title="Complement Graph", filename="complement_graph.png")

    # Determine which case
    vertices_k = get_vertices_of_degree_k(G, CONNECTIVITY_LEVEL)
    G_k = get_subgraph_by_vertices(G, vertices_k)
    complement_G_k = get_complement_graph(G_k)
    matching = compute_maximum_matching(complement_G_k)

    if len(matching) * 2 == len(vertices_k):
        print("Case 1: Matching covers all degree-k vertices.")
    else:
        print("Case 2: Matching does NOT cover all degree-k vertices.")

    # Augment using full logic (case handled inside)
    edges = list(G.edges())
    # new_edges = augment_connectivity(edges, CONNECTIVITY_LEVEL)
    G_aug, new_edges = augment_connectivity(edges, CONNECTIVITY_LEVEL)


    G_aug = G.copy()
    G_aug.add_edges_from(new_edges)
    draw_graph(G_aug, title="Augmented Graph", highlight_edges=new_edges, filename="augmented_graph.png")

    print(f"New edge connectivity: {compute_edge_connectivity(G_aug)}")
    print(f"Edges added: {new_edges}")

if __name__ == "__main__":
    main()
