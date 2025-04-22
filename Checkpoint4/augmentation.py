# from graph_utils import get_vertices_of_degree_k, get_subgraph_by_vertices, get_complement_graph
# from matching import compute_maximum_matching, get_unmatched_vertices
# import networkx as nx

# def augment_graph_via_matching(G, k):
#     vertices_k = get_vertices_of_degree_k(G, k)
#     G_k = get_subgraph_by_vertices(G, vertices_k)
#     complement_G_k = get_complement_graph(G_k)
#     matching = compute_maximum_matching(complement_G_k)
#     new_edges = [(u, v) for u, v in matching if u in vertices_k and v in vertices_k]
#     G_aug = G.copy()
#     G_aug.add_edges_from(new_edges)
#     return G_aug, new_edges


# from graph_utils import generate_graph_from_edges, get_vertices_of_degree_k, get_subgraph_by_vertices, get_complement_graph
# from matching import compute_maximum_matching
# import networkx as nx

# def augment_connectivity(edges, k):
#     G = generate_graph_from_edges(edges)
#     vertices_k = get_vertices_of_degree_k(G, k)
#     G_k = get_subgraph_by_vertices(G, vertices_k)
#     complement_G_k = get_complement_graph(G_k)
#     matching = compute_maximum_matching(complement_G_k)
#     new_edges = [(u, v) for u, v in matching if u in vertices_k and v in vertices_k]
#     return new_edges


# def augment_graph_via_paths(G, unmatched_vertices, complement_G_k):
#     # Placeholder for path-based augmentation logic
#     # Example: Try greedy matching through common neighbors
#     return G.copy(), []
from graph_utils import get_vertices_of_degree_k, get_subgraph_by_vertices, get_complement_graph
from matching import compute_maximum_matching, get_unmatched_vertices
import networkx as nx



def compute_edge_connectivity(G):
    return nx.edge_connectivity(G)

def is_k_plus_1_edge_connected(G, k):
    return compute_edge_connectivity(G) >= k + 1


def force_augmentation(G, k, limit=5):
    """
    Add up to `limit` edges from the complement randomly or greedily to improve connectivity.
    """
    G_aug = G.copy()
    comp = get_complement_graph(G)
    attempts = 0
    added = []

    for u, v in comp.edges():
        if not G_aug.has_edge(u, v):
            G_aug.add_edge(u, v)
            added.append((u, v))
            attempts += 1
            if compute_edge_connectivity(G_aug) > k:
                print(f"[Forced Success] Increased connectivity to {compute_edge_connectivity(G_aug)} after {attempts} injections.")
                return G_aug, added
            if attempts >= limit:
                break

    print("[Forced Fallback] Tried multiple injections, connectivity still not increased.")
    return G_aug, added


def augment_graph_via_matching(G, k):
    # from connectivity import compute_edge_connectivity

    vertices_k = get_vertices_of_degree_k(G, k)
    G_k = get_subgraph_by_vertices(G, vertices_k)
    complement_G_k = get_complement_graph(G_k)
    matching = compute_maximum_matching(complement_G_k)
    new_edges = [(u, v) for u, v in matching if u in vertices_k and v in vertices_k]

    # Fallback if no effective edges found
    if not new_edges:
        print("[Fallback] No augmenting edges found from matching. Forcing edge additions.")
        for u in vertices_k:
            for v in vertices_k:
                if u != v and not G.has_edge(u, v):
                    new_edges.append((u, v))
                    if len(new_edges) >= len(vertices_k) // 2:
                        break

    G_aug = G.copy()
    G_aug.add_edges_from(new_edges)
    if compute_edge_connectivity(G_aug) <= k:
        print("[Backup] Trying smart forced edge addition...")
        G_aug, forced_edges = force_augmentation(G_aug, k)
        new_edges.extend(forced_edges)

    # Validation step
    new_connectivity = compute_edge_connectivity(G_aug)
    if new_connectivity <= k:
        print(f"[Warning] Edge-connectivity remains {new_connectivity} after matching. Consider alternative augmentations.")
    else:
        print(f"[Success] Edge-connectivity increased to {new_connectivity} after matching.")

    return G_aug, new_edges



def augment_connectivity(edges, k):
    G = nx.Graph()
    G.add_edges_from(edges)

    vertices_k = get_vertices_of_degree_k(G, k)
    G_k = get_subgraph_by_vertices(G, vertices_k)
    complement_G_k = get_complement_graph(G_k)
    matching = compute_maximum_matching(complement_G_k)

    if len(matching) * 2 == len(vertices_k):
        print("Case 1: Matching covers all degree-k vertices.")
        return augment_graph_via_matching(G, k)
    else:
        print("Case 2: Matching does NOT cover all degree-k vertices.")
        unmatched = set(vertices_k) - set([v for edge in matching for v in edge])
        return augment_graph_via_paths(G, unmatched, complement_G_k,k)



def augment_graph_via_paths(G, unmatched_vertices, complement_G_k,k):
    G_aug = G.copy()
    new_edges = []
    unmatched = list(unmatched_vertices)
    visited = set()

    # Attempt to connect unmatched vertices via common neighbors (length 2 paths)
    for i in range(len(unmatched)):
        u = unmatched[i]
        if u in visited:
            continue
        for j in range(i + 1, len(unmatched)):
            v = unmatched[j]
            if v in visited:
                continue
            # Check for a common neighbor in the complement graph
            neighbors_u = set(complement_G_k.neighbors(u))
            neighbors_v = set(complement_G_k.neighbors(v))
            common = neighbors_u & neighbors_v
            if common:
                intermediary = list(common)[0]
                G_aug.add_edge(u, intermediary)
                G_aug.add_edge(intermediary, v)
                new_edges.extend([(u, intermediary), (intermediary, v)])
                visited.update([u, v])
                break

    # If still unmatched, try to directly connect remaining pairs (length 1 paths)
    for i in range(len(unmatched)):
        u = unmatched[i]
        if u in visited:
            continue
        for j in range(i + 1, len(unmatched)):
            v = unmatched[j]
            if v in visited:
                continue
            if not G_aug.has_edge(u, v):
                G_aug.add_edge(u, v)
                new_edges.append((u, v))
                visited.update([u, v])
                break
    
    if not new_edges:
        print("[NOTE] No augmenting paths found. Forcing direct links between unmatched nodes.")
        for i in range(0, len(unmatched) - 1, 2):
            u, v = unmatched[i], unmatched[i + 1]
            if not G_aug.has_edge(u, v):
                G_aug.add_edge(u, v)
                new_edges.append((u, v))

    if compute_edge_connectivity(G_aug) <= k:
        print("[Backup] Trying smart forced edge addition...")
        G_aug, forced_edges = force_augmentation(G_aug, k)
        new_edges.extend(forced_edges)


    return G_aug, new_edges
