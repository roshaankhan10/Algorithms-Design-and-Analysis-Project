from graph_utils import get_vertices_of_degree_k, get_subgraph_by_vertices, get_complement_graph
from matching import compute_maximum_matching, get_unmatched_vertices
import networkx as nx


def compute_edge_connectivity(G):
    return nx.edge_connectivity(G)


def is_k_plus_1_edge_connected(G, k):
    return compute_edge_connectivity(G) >= k + 1


def find_min_cut_edges(G):
    """
    Find edges that are part of a minimum cut in the graph.
    Returns potential bottleneck edges that limit connectivity.
    """
    min_cut_value = compute_edge_connectivity(G)
    min_cut_edges = []
    
    # For each pair of vertices, check if their min cut equals the global min cut
    for u in list(G.nodes())[:10]:  # Limit to avoid excessive computation
        for v in list(G.nodes())[10:20]:
            if u != v:
                try:
                    cut_value, partition = nx.minimum_cut(G, u, v)
                    if cut_value == min_cut_value:
                        # Get the edges that cross this minimum cut
                        part1, part2 = partition
                        crossing_edges = [(n1, n2) for n1 in part1 for n2 in part2 if G.has_edge(n1, n2)]
                        min_cut_edges.extend(crossing_edges)
                        break  # Found a min cut, no need to check more pairs for this u
                except nx.NetworkXError:
                    continue
    
    return list(set(min_cut_edges))  # Remove duplicates


def strategic_edge_addition(G, k):
    """
    Strategically add edges to improve connectivity by:
    1. Finding bottleneck regions (min cuts)
    2. Adding edges that cross these bottlenecks
    """
    G_aug = G.copy()
    original_connectivity = compute_edge_connectivity(G)
    added_edges = []
    
    if original_connectivity > k:
        print(f"[Info] Graph already has connectivity {original_connectivity} > {k}")
        return G_aug, added_edges
    
    # Find minimum cut edges and their endpoints
    min_cut_edges = find_min_cut_edges(G)
    print(f"[Debug] Found {len(min_cut_edges)} minimum cut edges")
    
    if not min_cut_edges:
        print("[Warning] No minimum cut edges found. Using degree-based approach.")
        return force_augmentation(G, k)
    
    # Get endpoints of min cut edges
    endpoints = set()
    for u, v in min_cut_edges:
        endpoints.add(u)
        endpoints.add(v)
    
    # Create complement graph to find potential edges to add
    complement = get_complement_graph(G)
    
    # Add edges that connect across the bottleneck
    potential_edges = []
    for u in endpoints:
        for v in endpoints:
            if u != v and complement.has_edge(u, v):
                potential_edges.append((u, v, nx.shortest_path_length(G, u, v)))
    
    # Sort by path length (prioritize connecting distant nodes)
    potential_edges.sort(key=lambda x: x[2], reverse=True)
    
    # Add edges until connectivity increases
    for u, v, _ in potential_edges:
        G_aug.add_edge(u, v)
        added_edges.append((u, v))
        new_connectivity = compute_edge_connectivity(G_aug)
        print(f"[Debug] Added edge ({u}, {v}), new connectivity: {new_connectivity}")
        
        if new_connectivity > original_connectivity:
            print(f"[Success] Increased connectivity to {new_connectivity}")
            return G_aug, added_edges
        
        if len(added_edges) >= 5:  # Limit number of tries
            break
    
    print("[Warning] Strategic edge addition didn't improve connectivity. Trying force augmentation.")
    return force_augmentation(G, k, start_graph=G_aug, start_edges=added_edges)


def force_augmentation(G, k, limit=10, start_graph=None, start_edges=None):
    """
    Add up to `limit` edges from the complement using a smarter strategy to improve connectivity.
    """
    G_aug = G.copy() if start_graph is None else start_graph
    added = [] if start_edges is None else start_edges.copy()
    original_connectivity = compute_edge_connectivity(G)
    print(f"[Debug] Original connectivity: {original_connectivity}, target: >{k}")
    
    # Get low-degree vertices as they might be bottlenecks
    low_degree_vertices = get_vertices_of_degree_k(G, k)
    print(f"[Debug] Found {len(low_degree_vertices)} vertices of degree {k}")
    
    # Get complement graph for potential edges
    comp = get_complement_graph(G)
    
    # Prioritize edges between low-degree vertices
    priority_edges = []
    for u in low_degree_vertices:
        for v in low_degree_vertices:
            if u != v and comp.has_edge(u, v):
                priority_edges.append((u, v))
    
    # Try adding priority edges first
    for u, v in priority_edges:
        if len(added) >= limit:
            break
        if not G_aug.has_edge(u, v):
            G_aug.add_edge(u, v)
            added.append((u, v))
            new_connectivity = compute_edge_connectivity(G_aug)
            print(f"[Debug] Added priority edge ({u}, {v}), new connectivity: {new_connectivity}")
            
            if new_connectivity > original_connectivity:
                print(f"[Forced Success] Increased connectivity to {new_connectivity} after adding {len(added)} edges.")
                return G_aug, added
    
    # If priority edges didn't help, try random edges from complement
    other_edges = [e for e in comp.edges() if e not in priority_edges]
    import random
    random.shuffle(other_edges)
    
    for u, v in other_edges:
        if len(added) >= limit:
            break
        if not G_aug.has_edge(u, v):
            G_aug.add_edge(u, v)
            added.append((u, v))
            new_connectivity = compute_edge_connectivity(G_aug)
            print(f"[Debug] Added random edge ({u}, {v}), new connectivity: {new_connectivity}")
            
            if new_connectivity > original_connectivity:
                print(f"[Forced Success] Increased connectivity to {new_connectivity} after adding {len(added)} edges.")
                return G_aug, added
    
    new_connectivity = compute_edge_connectivity(G_aug)
    if new_connectivity > original_connectivity:
        print(f"[Partial Success] Increased connectivity to {new_connectivity}, but not beyond {k}.")
    else:
        print(f"[Forced Fallback] Added {len(added)} edges, connectivity still at {new_connectivity}.")
    
    return G_aug, added


def augment_graph_via_matching(G, k):
    """
    Improved matching-based augmentation that properly handles the subgraph.
    """
    original_connectivity = compute_edge_connectivity(G)
    print(f"[Debug] Original connectivity: {original_connectivity}, target: >{k}")
    
    vertices_k = get_vertices_of_degree_k(G, k)
    print(f"[Debug] Found {len(vertices_k)} vertices of degree {k}")
    
    if not vertices_k:
        print(f"[Info] No vertices of degree {k} found. All vertices have degree > {k}.")
        return G, []
    
    G_k = get_subgraph_by_vertices(G, vertices_k)
    complement_G_k = get_complement_graph(G_k)
    
    # Verify the complement graph has edges
    if complement_G_k.number_of_edges() == 0:
        print("[Warning] Complement graph has no edges. All possible edges exist in the subgraph.")
        return strategic_edge_addition(G, k)
    
    matching = compute_maximum_matching(complement_G_k)
    print(f"[Debug] Found matching with {len(matching)} edges")
    
    # The matching is already from the subgraph of vertices with degree k,
    # so we don't need to filter
    new_edges = list(matching)
    
    # If no edges found in matching or matching is too small
    if not new_edges or len(new_edges) < len(vertices_k) // 4:
        print(f"[Fallback] Matching too small ({len(new_edges)} edges). Using strategic edge addition.")
        return strategic_edge_addition(G, k)
    
    # Add matched edges to original graph
    G_aug = G.copy()
    G_aug.add_edges_from(new_edges)
    
    # Check if connectivity improved
    new_connectivity = compute_edge_connectivity(G_aug)
    print(f"[Debug] After matching, connectivity: {new_connectivity}")
    
    if new_connectivity <= original_connectivity:
        print(f"[Backup] Matching didn't improve connectivity. Using strategic forced edge addition...")
        return strategic_edge_addition(G, k)
    else:
        print(f"[Success] Edge-connectivity increased to {new_connectivity} after matching.")
    
    return G_aug, new_edges


def augment_graph_via_paths(G, unmatched_vertices, complement_G_k, k):
    """
    Improved path-based augmentation for unmatched vertices.
    """
    original_connectivity = compute_edge_connectivity(G)
    print(f"[Debug] Original connectivity: {original_connectivity}, target: >{k}")
    print(f"[Debug] Unmatched vertices: {len(unmatched_vertices)}")
    
    G_aug = G.copy()
    new_edges = []
    unmatched = list(unmatched_vertices)
    visited = set()
    
    # First attempt: Try to find paths that connect unmatched vertices through minimum cuts
    min_cut_edges = find_min_cut_edges(G)
    min_cut_vertices = set()
    for u, v in min_cut_edges:
        min_cut_vertices.add(u)
        min_cut_vertices.add(v)
    
    # Try to connect unmatched vertices through min cut vertices
    for u in unmatched:
        if u in visited:
            continue
        for v in unmatched:
            if u == v or v in visited:
                continue
            
            # Try to find a common neighbor in min cut vertices
            for mc_vertex in min_cut_vertices:
                if mc_vertex not in [u, v] and not G.has_edge(u, mc_vertex) and not G.has_edge(v, mc_vertex):
                    G_aug.add_edge(u, mc_vertex)
                    G_aug.add_edge(mc_vertex, v)
                    new_edges.extend([(u, mc_vertex), (mc_vertex, v)])
                    visited.update([u, v])
                    print(f"[Debug] Added path through min cut vertex: {u}-{mc_vertex}-{v}")
                    break
    
    # Second attempt: Connect through common neighbors in complement
    for i in range(len(unmatched)):
        u = unmatched[i]
        if u in visited:
            continue
        for j in range(i + 1, len(unmatched)):
            v = unmatched[j]
            if v in visited:
                continue
            
            # Check for common neighbors in complement
            neighbors_u = set(complement_G_k.neighbors(u))
            neighbors_v = set(complement_G_k.neighbors(v))
            common = neighbors_u & neighbors_v
            
            if common:
                intermediary = list(common)[0]
                if not G_aug.has_edge(u, intermediary) and not G_aug.has_edge(intermediary, v):
                    G_aug.add_edge(u, intermediary)
                    G_aug.add_edge(intermediary, v)
                    new_edges.extend([(u, intermediary), (intermediary, v)])
                    visited.update([u, v])
                    print(f"[Debug] Added path through common neighbor: {u}-{intermediary}-{v}")
                    break
    
    # Third attempt: Direct connections for remaining unmatched vertices
    remaining = [v for v in unmatched if v not in visited]
    for i in range(0, len(remaining) - 1, 2):
        if i+1 < len(remaining):
            u, v = remaining[i], remaining[i+1]
            if not G_aug.has_edge(u, v):
                G_aug.add_edge(u, v)
                new_edges.append((u, v))
                print(f"[Debug] Added direct edge between unmatched: {u}-{v}")
    
    # Check if our efforts improved connectivity
    new_connectivity = compute_edge_connectivity(G_aug)
    print(f"[Debug] After path augmentation, connectivity: {new_connectivity}")
    
    if new_connectivity <= original_connectivity:
        print("[Warning] Path augmentation didn't improve connectivity. Using strategic approach.")
        return strategic_edge_addition(G, k)
    
    print(f"[Success] Edge-connectivity increased to {new_connectivity} after path augmentation.")
    return G_aug, new_edges


def augment_connectivity(edges, k):
    """
    Main function to augment connectivity of a graph.
    
    Args:
        edges: List of edges in the graph
        k: Target connectivity (want to achieve k+1)
        
    Returns:
        Augmented graph and list of new edges added
    """
    G = nx.Graph()
    G.add_edges_from(edges)
    
    # First check current connectivity
    current_connectivity = compute_edge_connectivity(G)
    print(f"Original edge connectivity: {current_connectivity}")
    
    if current_connectivity > k:
        print(f"[Info] Graph already has connectivity > {k}")
        return G, []
    
    # Find vertices of degree exactly k
    vertices_k = get_vertices_of_degree_k(G, k)
    print(f"[Debug] Found {len(vertices_k)} vertices of degree {k}")
    
    # If no vertices of degree k, use strategic approach
    if not vertices_k:
        print("[Info] No vertices of degree k. Using strategic approach.")
        return strategic_edge_addition(G, k)
    
    # Create subgraph of vertices with degree k
    G_k = get_subgraph_by_vertices(G, vertices_k)
    complement_G_k = get_complement_graph(G_k)
    
    # Compute matching in the complement
    matching = compute_maximum_matching(complement_G_k)
    print(f"[Debug] Found matching with {len(matching)} edges")
    
    # Check if matching covers all vertices of degree k
    matched_vertices = set([v for edge in matching for v in edge])
    
    if len(matched_vertices) == len(vertices_k):
        print("Case 1: Matching covers all degree-k vertices.")
        return augment_graph_via_matching(G, k)
    else:
        print("Case 2: Matching does NOT cover all degree-k vertices.")
        unmatched = set(vertices_k) - matched_vertices
        print(f"[Debug] Unmatched vertices: {len(unmatched)}")
        return augment_graph_via_paths(G, unmatched, complement_G_k, k)