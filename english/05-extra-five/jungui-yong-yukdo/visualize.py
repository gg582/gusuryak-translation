import matplotlib.pyplot as plt
import matplotlib.patches as patches
import networkx as nx

# Font setup for cross-platform compatibility (Korean fonts listed first)
plt.rcParams['font.family'] = ['NanumGothic', 'NanumBarunGothic', 'Malgun Gothic', 'AppleGothic', 'DejaVu Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# 1. 2-D coordinates of the 16 nodes
diagram_positions = {
    7: (-2.5, 3), 16: (-1, 3.2), 1: (1, 3.2), 6: (2.5, 3),
    13: (-3, 1.5), 11: (-1, 1), 10: (1, 1), 4: (3, 1.5),
    3: (-3, -1.5), 9: (-1, -1), 12: (1, -1), 14: (3, -1.5),
    8: (-2.5, -3), 2: (-1, -3.2), 15: (1, -3.2), 5: (2.5, -3)
}

# 2. Define only the four T-shaped arrow edges (independence between groups is kept)
correct_edges = [
    # Upper-left T (center 7 -> 16, 13, 11)
    (7, 16), (7, 13), (7, 11),
    # Upper-right T (center 6 -> 1, 10, 4)
    (6, 1), (6, 10), (6, 4),
    # Lower-left T (center 8 -> 3, 9, 2)
    (8, 3), (8, 9), (8, 2),
    # Lower-right T (center 5 -> 12, 14, 15)
    (5, 12), (5, 14), (5, 15)
]

# 3. Create graph and add edges
G = nx.Graph()
G.add_nodes_from(diagram_positions.keys())
G.add_edges_from(correct_edges)

fig, ax = plt.subplots(figsize=(9, 9))

# 4. Draw nodes and number labels (light yellow background)
nx.draw_networkx_nodes(G, diagram_positions, node_color='#FFFBDE', node_size=1500, edgecolors='black', linewidths=1.5, ax=ax)
nx.draw_networkx_labels(G, diagram_positions, font_size=18, font_weight='bold', ax=ax)

# 5. Draw edges (only the four T-shaped arrows)
nx.draw_networkx_edges(G, diagram_positions, width=2.5, edge_color='black', ax=ax)

# 6. Represent each sum-51 region with a semi-transparent ellipse
ellipse_colors = {
    'top': ('#FFD700', 0.15),    # top (yellow)
    'left': ('#87CEEB', 0.15),   # left (blue)
    'bottom': ('#3CB371', 0.15), # bottom (green)
    'right': ('#F08080', 0.15)   # right (pink)
}

# Top-group ellipse (7, 16, 1, 6, 11, 10)
ellipse_top = patches.Ellipse((0, 2.5), width=6.8, height=3.0, color=ellipse_colors['top'][0], alpha=ellipse_colors['top'][1])
# Left-group ellipse (7, 13, 11, 3, 9, 8)
ellipse_left = patches.Ellipse((-2.0, 0), width=3.5, height=6.8, color=ellipse_colors['left'][0], alpha=ellipse_colors['left'][1])
# Bottom-group ellipse (8, 2, 9, 12, 15, 5)
ellipse_bottom = patches.Ellipse((0, -2.5), width=6.8, height=3.0, color=ellipse_colors['bottom'][0], alpha=ellipse_colors['bottom'][1])
# Right-group ellipse (6, 10, 4, 12, 14, 5)
ellipse_right = patches.Ellipse((2.0, 0), width=3.5, height=6.8, color=ellipse_colors['right'][0], alpha=ellipse_colors['right'][1])

for ell in [ellipse_top, ellipse_left, ellipse_bottom, ellipse_right]:
    ax.add_patch(ell)

# 7. Add sum-51 labels
label_font = {'weight': 'bold', 'color': '#333333'}
ax.text(0, 4.3, "Sum = 51", ha='center', fontdict=label_font, fontsize=13)
ax.text(-4.2, 0, "Sum = 51", va='center', rotation=90, fontdict=label_font, fontsize=13)
ax.text(0, -4.3, "Sum = 51", ha='center', fontdict=label_font, fontsize=13)
ax.text(4.2, 0, "Sum = 51", va='center', rotation=-90, fontdict=label_font, fontsize=13)

# Set title
plt.title("Gusu-ryak — Jungui-yong-yukdo (重儀用六圖)", fontsize=16, pad=40, fontweight='bold')
plt.axis('off')
plt.tight_layout()
plt.show()
