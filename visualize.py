import matplotlib.pyplot as plt
import networkx as nx

def draw_graph(G, title="Graph", highlight_edges=None):
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=700)
    if highlight_edges:
        nx.draw_networkx_edges(G, pos, edgelist=highlight_edges, edge_color='red', width=2)
    plt.title(title)
    # plt.show()
    plt.savefig(f"{draw_graph}.png")
    plt.close()