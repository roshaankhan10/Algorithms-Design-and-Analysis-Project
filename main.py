# Project: Edge Connectivity Augmentation on Simple Graphs Title.md

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