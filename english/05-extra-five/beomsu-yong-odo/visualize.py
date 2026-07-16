import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import networkx as nx

# Automatic Korean/English font setup (kept for cross-platform compatibility)
preferred_fonts = ['NanumGothic', 'Noto Sans CJK KR', 'Malgun Gothic', 'AppleGothic']
available_fonts = {f.name for f in fm.fontManager.ttflist}
selected_font = next(
    (name for name in preferred_fonts if name in available_fonts),
    None
)
if selected_font is None:
    # Fall back to any CJK-capable font if the preferred ones are absent
    for f in fm.fontManager.ttflist:
        if any(keyword in f.name for keyword in ('CJK', 'Nanum', 'Gothic', 'Malgun', 'AppleGothic')):
            selected_font = f.name
            break

if selected_font:
    plt.rcParams['font.family'] = selected_font
plt.rcParams['axes.unicode_minus'] = False

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
