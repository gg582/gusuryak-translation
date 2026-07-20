import matplotlib.pyplot as plt
import networkx as nx

from cjk_font_config import configure_matplotlib_fonts

configure_matplotlib_fonts()

# Forward-direction node coordinates
positions = {
    3: (-2, 0),
    7: (-1, 0),
    5: (0, 0),
    4: (1, 0),
    6: (2, 0),
    2: (0, 2),
    8: (0, 1),
    1: (0, -1),
    9: (0, -2)
}

G = nx.Graph()
for node in positions:
    G.add_node(node)

# Forward-direction edges
edges = [
    (3, 7), (7, 5), (5, 4), (4, 6),  # horizontal line
    (2, 8), (8, 5), (5, 1), (1, 9)   # vertical line
]
G.add_edges_from(edges)

plt.figure(figsize=(6, 6))

# Render nodes and labels
nx.draw_networkx_nodes(G, positions, node_color='lightblue', node_size=1200, edgecolors='black')
nx.draw_networkx_labels(G, positions, font_size=16, font_weight='bold')
nx.draw_networkx_edges(G, positions, width=2, edge_color='gray')

plt.title("Beomsu-yong-odo (範數用五圖) (Sum = 25)", fontsize=14, pad=20)
plt.axis('off')
plt.tight_layout()
plt.show()
