import matplotlib.pyplot as plt
import networkx as nx

def draw_graph(G, title="Graph", highlight_edges=None, filename=None):
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=700)

    if highlight_edges:
        nx.draw_networkx_edges(G, pos, edgelist=highlight_edges, edge_color='red', width=2)

    plt.title(title)
    if filename:
    #     plt.savefig(f"outputs/{filename}")
    # plt.show()

        plt.savefig(f"output/{filename}.png")
    plt.close()
