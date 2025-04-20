import networkx as nx
import matplotlib.pyplot as plt
import time

def generate_graph():
    """Generate a k-edge-connected simple graph."""
    G = nx.Graph()
    edges = [(0,1), (1,2), (2,3), (3,0), (0,2), (1,3)]  # Example 2-edge-connected graph
    G.add_edges_from(edges)
    return G

def complement_graph(G):
    """Compute the complement graph G'."""
    nodes = set(G.nodes())
    G_comp = nx.Graph()
    G_comp.add_nodes_from(nodes)
    
    for u in nodes:
        for v in nodes:
            if u != v and not G.has_edge(u, v):
                G_comp.add_edge(u, v)
    
    return G_comp

def find_maximum_matching(G_comp):
    """Find a maximum matching in the complement graph using Edmonds' algorithm."""
    matching = nx.max_weight_matching(G_comp, maxcardinality=True)
    return matching

def augment_graph(G, matching):
    """Augment the graph using the matching from the complement graph."""
    for u, v in matching:
        G.add_edge(u, v)
    return G

def visualize_graph(G, title):
    """Visualize the graph using matplotlib."""
    plt.figure(figsize=(6,6))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=700, font_size=14)
    plt.title(title)
    plt.show()

def analyze_complexity():
    """Measure execution time for increasing graph sizes."""
    sizes = list(range(10, 101, 10))  # Graph sizes from 10 to 100 nodes
    times = []
    
    for size in sizes:
        G = nx.erdos_renyi_graph(size, 0.5)  # Generate random graph
        G_comp = complement_graph(G)
        
        start_time = time.time()
        matching = find_maximum_matching(G_comp)
        G_augmented = augment_graph(G, matching)
        end_time = time.time()
        
        times.append(end_time - start_time)
    
    plt.figure(figsize=(8,5))
    plt.plot(sizes, times, marker='o', linestyle='-', color='b')
    plt.xlabel("Graph Size (Nodes)")
    plt.ylabel("Execution Time (Seconds)")
    plt.title("Time Complexity Analysis")
    plt.grid(True)
    plt.show()

# Generate graph and its complement
G = generate_graph()
G_comp = complement_graph(G)
matching = find_maximum_matching(G_comp)

# Visualize before augmentation
visualize_graph(G, "Original Graph")

# Augment graph
G_augmented = augment_graph(G, matching)

# Visualize after augmentation
visualize_graph(G_augmented, "Augmented Graph")

# Print results
print("Original Graph Edges:", G.edges())
print("Complement Graph Edges:", G_comp.edges())
print("Maximum Matching in Complement Graph:", matching)
print("Augmented Graph Edges:", G_augmented.edges())

# Run complexity analysis
analyze_complexity()
