#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nakseo Sagudo — advanced graph and combinatorial analysis script
《Gusuryeok》Choi Seok-jeong text Nakseo Sagudotext text text text text
invariants(invariant)text text text analysistext.
"""

import os
import itertools
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm
from collections import Counter, defaultdict
from matplotlib.lines import Line2D

# matplotlib text text text text/CJK text text
fm._load_fontmanager(try_read_cache=False)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

OUTPUT_DIR = '.'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================
# 1. graph data (corrected source)
# ============================================

POSITIONS = {
    19: (-2,  3), 2:  (-3,  2), 14: (-2,  1), 5:  (-1,  0),
    16: ( 0,  1), 7:  (-1,  2),
    17: ( 2,  3), 4:  ( 1,  2), 9:  ( 3,  2), 12: ( 2,  1),
    10: ( 1,  0),
    18: (-2, -1), 3:  (-3, -2), 13: (-2, -3), 8:  (-1, -2),
    11: ( 0, -1),
    6:  ( 2, -1), 1:  ( 3, -2), 20: ( 2, -3), 15: ( 1, -2),
}

EDGES = [
    (19, 2), (2, 14), (14, 5), (5, 16), (16, 7), (7, 19),
    (17, 4), (4, 16), (16, 10), (10, 12), (12, 9), (9, 17),
    (5, 18), (18, 3), (3, 13), (13, 8), (8, 11), (11, 5),
    (10, 6), (6, 1), (1, 20), (20, 15), (15, 11), (11, 10),
]

HEXAGONS = {
    'NW': [19, 2, 14, 5, 16, 7],
    'NE': [17, 4, 16, 10, 12, 9],
    'SW': [5, 18, 3, 13, 8, 11],
    'SE': [10, 6, 1, 20, 15, 11],
}

PERIMETER_20 = [19, 2, 14, 5, 18, 3, 13, 8, 11, 15, 20, 1, 6, 10, 12, 9, 17, 4, 16, 7]
INNER_4 = [5, 16, 10, 11]

NINE_PALACES = {
    'NW': [19, 2, 14, 7], 'N':  [19, 17, 2, 4], 'NE': [17, 4, 12, 9],
    'W':  [14, 7, 18, 3], 'C':  [5, 16, 10, 11], 'E':  [9, 12, 6, 15],
    'SW': [18, 3, 13, 8], 'S':  [13, 8, 20, 1], 'SE': [6, 1, 20, 15],
}

G = nx.Graph()
G.add_edges_from(EDGES)

wuxing = {
    1: 'Water', 6: 'Water', 11: 'Water', 16: 'Water',
    2: 'Fire', 7: 'Fire', 12: 'Fire', 17: 'Fire',
    3: 'Wood', 8: 'Wood', 13: 'Wood', 18: 'Wood',
    4: 'Metal', 9: 'Metal', 14: 'Metal', 19: 'Metal',
    5: 'Earth', 10: 'Earth', 15: 'Earth', 20: 'Earth',
}

wuxing_color = {
    'Water': '#4488CC', 'Fire': '#CC4444', 'Wood': '#44AA44',
    'Metal': '#888888', 'Earth': '#CC9944',
}

wuxing_en = {
    'Water': 'Water', 'Fire': 'Fire', 'Wood': 'Wood', 'Metal': 'Metal', 'Earth': 'Earth'
}

for node in G.nodes():
    G.nodes[node]['wuxing'] = wuxing[node]
    G.nodes[node]['color'] = wuxing_color[wuxing[node]]
    G.nodes[node]['remainder'] = node % 5 if node % 5 != 0 else 5

node_colors = [G.nodes[n]['color'] for n in G.nodes()]
hex_colors = {'NW': '#CC4444', 'NE': '#4488CC', 'SW': '#44AA44', 'SE': '#CC9944'}

def save_fig(name):
    plt.savefig(f'{OUTPUT_DIR}/{name}', dpi=200, bbox_inches='tight')
    print(f"[Saved] {name}")

# ============================================
# 2. core text invariants text
# ============================================

print("=" * 70)
print("Nakseo Sagudo advanced graph-theoretic analysis")
print("=" * 70)

# text invariants
n = G.number_of_nodes()
m = G.number_of_edges()
print(f"\n[text]")
print(f"  node count n = {n}, edge count m = {m}")
print(f"  average degree = {2*m/n:.3f}")
print(f"  connected components = {nx.number_connected_components(G)}")
print(f"  bridges(bridge) text = {len(list(nx.bridges(G)))}")
print(f"  articulation points(articulation point) text = {len(list(nx.articulation_points(G)))}")

# degree
print(f"\n[degree]")
deg = dict(G.degree())
for d in sorted(set(deg.values()), reverse=True):
    nodes_d = [v for v, k in deg.items() if k == d]
    print(f"  degree {d}: {nodes_d} ({len(nodes_d)})")

# distance invariants
print(f"\n[distance]")
sp = dict(nx.shortest_path_length(G))
all_pairs = [sp[u][v] for u in G.nodes() for v in G.nodes() if u != v]
diameter = max(all_pairs)
radius = min(max(sp[v].values()) for v in G.nodes())
print(f"  diameter(diameter) = {diameter}")
print(f"  radius(radius) = {radius}")
print(f"  average text distance = {np.mean(all_pairs):.3f}")
print(f"  distance distribution: {dict(sorted(Counter(all_pairs).items()))}")

# centrality
print(f"\n[centrality]")
betw = nx.betweenness_centrality(G)
close = nx.closeness_centrality(G)
eigen = nx.eigenvector_centrality(G, max_iter=1000)
print("  Betweenness Top 5:")
for v, c in sorted(betw.items(), key=lambda x: -x[1])[:5]:
    print(f"    {v}({wuxing[v]}): {c:.4f}")
print("  Closeness:")
for v, c in sorted(close.items(), key=lambda x: -x[1])[:5]:
    print(f"    {v}({wuxing[v]}): {c:.4f}")
print("  Eigenvector:")
for v, c in sorted(eigen.items(), key=lambda x: -x[1])[:5]:
    print(f"    {v}({wuxing[v]}): {c:.4f}")

# text
print(f"\n[text]")
cycle_basis = nx.cycle_basis(G)
print(f"  cycle basis count = {len(cycle_basis)}")

def find_cycles_of_length(G, length):
    """text text text text text lengthtext text text"""
    cycles = set()
    for start in G.nodes():
        # DFStext length text text text
        stack = [(start, [start])]
        while stack:
            node, path = stack.pop()
            if len(path) == length + 1:
                if path[-1] == start and len(set(path[:-1])) == length:
                    c = tuple(sorted(path[:-1]))
                    cycles.add(c)
                continue
            for nb in G.neighbors(node):
                if nb == start and len(path) == length:
                    new_path = path + [nb]
                    if len(set(new_path[:-1])) == length:
                        c = tuple(sorted(new_path[:-1]))
                        cycles.add(c)
                elif nb not in path:
                    stack.append((nb, path + [nb]))
    return [list(c) for c in cycles]

for L in [4, 6, 8, 10, 12]:
    cycs = find_cycles_of_length(G, L)
    print(f"  length {L} text count = {len(cycs)}")
    if cycs and L <= 8:
        for c in cycs:
            print(f"    {sorted(c)} (sum={sum(c)})")

# all text sum distribution
all_cycles = []
for L in range(4, 21):
    all_cycles.extend(find_cycles_of_length(G, L))
cycle_sum_counter = Counter([sum(c) for c in all_cycles])
print(f"\n  text text text count = {len(all_cycles)}")
print(f"  text sum distribution (text 10): {cycle_sum_counter.most_common(10)}")

# text text text set
print(f"\n[text/textset]")
# greedy_colortext text colors text text text; max+1text text text text
chi_lf = max(nx.coloring.greedy_color(G, strategy='largest_first').values()) + 1
chi_ds = max(nx.coloring.greedy_color(G, strategy='DSATUR').values()) + 1
print(f"  greedy color-count upper bound (largest_first) = {chi_lf}")
print(f"  greedy color-count upper bound (DSATUR) = {chi_ds}")
print(f"  maximum independent set size(approx) = {len(nx.approximation.maximum_independent_set(G))}")
print(f"  minimum dominating set size(approx) = {len(nx.approximation.min_weighted_dominating_set(G))}")

# spectrum
print(f"\n[spectrum]")
A = nx.adjacency_matrix(G, nodelist=sorted(G.nodes())).toarray()
L = np.diag(np.array(A.sum(axis=1)).flatten()) - A
adj_eig = np.linalg.eigvalsh(A)
lap_eig = np.linalg.eigvalsh(L)
print(f"  adjacency matrix eigenvalues range: [{min(adj_eig):.3f}, {max(adj_eig):.3f}]")
print(f"  Laplacian eigenvalues: {sorted(lap_eig)}")
print(f"  Algebraic connectivity (Fiedler value) = {sorted(lap_eig)[1]:.4f}")

# numberstext (symmetry)
print(f"\n[symmetry]")
# 4 shared verticestext betweennesstext same text text
shared = [5, 10, 11, 16]
print(f"  shared vertices {shared}text betweenness: {[round(betw[v], 4) for v in shared]}")
print(f"  shared vertices {shared}text closeness: {[round(close[v], 4) for v in shared]}")
print(f"  shared vertices {shared}text eigenvector centrality: {[round(eigen[v], 4) for v in shared]}")

# structuretext symmetry: 4 shared verticestext same degree, same all centralitytext text
print(f"  4 shared verticestext degree: {[deg[v] for v in shared]} (text 4)")
print(f"  → text 3×2 rectangle structuretext 4 facetext connectiontext structural gatewaystext,")
print(f"    symmetric graph positionstext text text all measures agree.")

# ============================================
# 3. Dual graph (3×2 rectangle structuretext dual)
# ============================================

print(f"\n[Dual graph]")
dual = nx.Graph()
for name in HEXAGONS:
    dual.add_node(name, sum=sum(HEXAGONS[name]))
# text facetext shared verticestext textface dualtext text
dual_edges = []
for a, b in itertools.combinations(HEXAGONS, 2):
    shared_nodes = set(HEXAGONS[a]) & set(HEXAGONS[b])
    if shared_nodes:
        dual.add_edge(a, b, shared=sorted(shared_nodes))
        dual_edges.append((a, b, sorted(shared_nodes)))
print(f"  Dual nodes: {list(dual.nodes())}")
print(f"  Dual edges:")
for a, b, s in dual_edges:
    print(f"    {a} -- {b}, shared vertices={s}, sum={sum(s)}")

# ============================================
# 4. visualization
# ============================================

hex_edges = {}
for name, cycle in HEXAGONS.items():
    hex_edges[name] = [(cycle[i], cycle[(i+1)%6]) for i in range(6)]
perimeter_edges = [(PERIMETER_20[i], PERIMETER_20[(i+1)%20]) for i in range(20)]
inner_edges = [(INNER_4[i], INNER_4[(i+1)%4]) for i in range(4)]

# --- 08: Laplacian spectrum + Fiedler vector ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
lap_eig_sorted = sorted(lap_eig)
ax.bar(range(n), lap_eig_sorted, color='#44AA44', edgecolor='black', alpha=0.8)
ax.axhline(y=0, color='red', linestyle='--', linewidth=1)
ax.set_xlabel('Index', fontsize=11)
ax.set_ylabel('Laplacian Eigenvalue', fontsize=11)
ax.set_title(f'Laplacian Spectrum\nλ_2 (algebraic connectivity) = {lap_eig_sorted[1]:.4f}', fontsize=13, fontweight='bold')
ax.grid(True, alpha=0.3)

ax = axes[1]
# Fiedler vector visualization
lap_vals, lap_vecs = np.linalg.eigh(L)
fiedler_vec = lap_vecs[:, 1]
node_order = sorted(G.nodes())
colors_fiedler = ['#CC4444' if v > 0 else '#4488CC' for v in fiedler_vec]
ax.bar(range(n), fiedler_vec, color=colors_fiedler, edgecolor='black')
ax.set_xticks(range(n))
ax.set_xticklabels([str(v) for v in node_order], fontsize=9)
ax.axhline(y=0, color='black', linewidth=1)
ax.set_title('Fiedler Vector (2nd Laplacian eigenvector)\ntext/text text text 2text', fontsize=13, fontweight='bold')
ax.grid(True, alpha=0.3)
plt.tight_layout(); save_fig('08_laplacian_spectrum.png'); plt.close()

# --- 09: distance matrix + eccentricity ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
D = np.zeros((n, n), dtype=int)
for i, u in enumerate(node_order):
    for j, v in enumerate(node_order):
        D[i, j] = sp[u][v]
im = ax.imshow(D, cmap='YlOrRd', interpolation='nearest')
ax.set_xticks(range(n)); ax.set_xticklabels(node_order, fontsize=9)
ax.set_yticks(range(n)); ax.set_yticklabels(node_order, fontsize=9)
plt.colorbar(im, ax=ax, shrink=0.8)
ax.set_title('Shortest Path Distance Matrix', fontsize=13, fontweight='bold')

ax = axes[1]
ecc = {v: max(sp[v].values()) for v in G.nodes()}
nodes_sorted_ecc = sorted(G.nodes(), key=lambda x: ecc[x])
colors_ecc = [G.nodes[v]['color'] for v in nodes_sorted_ecc]
ax.bar(range(n), [ecc[v] for v in nodes_sorted_ecc], color=colors_ecc, edgecolor='black')
ax.set_xticks(range(n)); ax.set_xticklabels([str(v) for v in nodes_sorted_ecc], fontsize=9)
ax.set_ylabel('Eccentricity', fontsize=11)
ax.set_title(f'Eccentricity by Node (diameter={diameter}, radius={radius})', fontsize=13, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout(); save_fig('09_distance_matrix.png'); plt.close()

# --- 10: text sum distribution text lengthtext distribution ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
length_counts = Counter([len(c) for c in all_cycles])
ax = axes[0]
lengths = sorted(length_counts.keys())
counts = [length_counts[L] for L in lengths]
ax.bar(lengths, counts, color='#CC9944', edgecolor='black')
ax.set_xlabel('Cycle Length', fontsize=11)
ax.set_ylabel('Count', fontsize=11)
ax.set_title('Number of Simple Cycles by Length', fontsize=13, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')
for L, c in zip(lengths, counts):
    ax.text(L, c + 0.3, str(c), ha='center', fontsize=10, fontweight='bold')

ax = axes[1]
sums = sorted(cycle_sum_counter.keys())
sum_counts = [cycle_sum_counter[s] for s in sums]
ax.bar(range(len(sums)), sum_counts, color='#4488CC', edgecolor='black')
ax.set_xticks(range(len(sums)))
ax.set_xticklabels([str(s) for s in sums], rotation=45, ha='right', fontsize=9)
ax.set_xlabel('Cycle Sum', fontsize=11)
ax.set_ylabel('Count', fontsize=11)
ax.set_title('Distribution of Cycle Sums', fontsize=13, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout(); save_fig('10_cycle_distributions.png'); plt.close()

# --- 11: Dual graph + shared vertices highlight ---
fig, axes = plt.subplots(1, 2, figsize=(16, 8))
ax = axes[0]
dual_pos = {'NW': (-1, 1), 'NE': (1, 1), 'SW': (-1, -1), 'SE': (1, -1)}
dual_node_colors = [hex_colors[v] for v in dual.nodes()]
nx.draw_networkx_nodes(dual, dual_pos, node_color=dual_node_colors, node_size=4000, edgecolors='black', linewidths=2.5, ax=ax)
nx.draw_networkx_labels(dual, dual_pos, font_size=14, font_weight='bold', ax=ax)
for u, v, d in dual.edges(data=True):
    x1, y1 = dual_pos[u]; x2, y2 = dual_pos[v]
    mx, my = (x1+x2)/2, (y1+y2)/2
    shared_nodes = d['shared']
    ax.text(mx, my, f"text\n{shared_nodes}\nsum={sum(shared_nodes)}", ha='center', va='center', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='black', alpha=0.9))
nx.draw_networkx_edges(dual, dual_pos, edge_color='black', width=2, ax=ax)
ax.set_xlim(-2, 2); ax.set_ylim(-2, 2); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('3×2 rectangle structuretext Dual Graph\n(face=vertices, shared vertices=text weight)', fontsize=14, fontweight='bold')

ax = axes[1]
# source graph on dual overlay
for name, hedges in hex_edges.items():
    nx.draw_networkx_edges(G, POSITIONS, edgelist=hedges, edge_color=hex_colors[name], width=2.5, alpha=0.6, ax=ax)
nx.draw_networkx_nodes(G, POSITIONS, node_color=node_colors, node_size=1200, edgecolors='black', linewidths=1.5, ax=ax)
nx.draw_networkx_labels(G, POSITIONS, font_size=11, font_weight='bold', ax=ax)
# dual face label positions
region_centers = {'NW': (-1.5, 2), 'NE': (1.5, 2), 'SW': (-1.5, -2), 'SE': (1.5, -2)}
for name, (x, y) in region_centers.items():
    ax.text(x, y, f"{name} face\nΣ={sum(HEXAGONS[name])}", ha='center', va='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor=hex_colors[name], edgecolor='black', alpha=0.7))
ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5); ax.axis('off')
ax.set_title('source graphtext 4 facetext Dual corresponding', fontsize=14, fontweight='bold')
plt.tight_layout(); save_fig('11_dual_graph.png'); plt.close()

# --- 12: five phases block matrix text generatingovercoming adjacency matrix ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
wx_list = ['Water', 'Fire', 'Wood', 'Metal', 'Earth']
block = np.zeros((5, 5), dtype=int)
for u, v in G.edges():
    i = wx_list.index(wuxing[u])
    j = wx_list.index(wuxing[v])
    block[i, j] += 1
    if i != j:
        block[j, i] += 1
im = ax.imshow(block, cmap='YlOrRd', interpolation='nearest')
ax.set_xticks(range(5)); ax.set_xticklabels(wx_list, fontsize=12)
ax.set_yticks(range(5)); ax.set_yticklabels(wx_list, fontsize=12)
for i in range(5):
    for j in range(5):
        ax.text(j, i, str(block[i, j]), ha='center', va='center', fontsize=12, fontweight='bold')
plt.colorbar(im, ax=ax, shrink=0.8)
ax.set_title('five phases text text block matrix', fontsize=13, fontweight='bold')

ax = axes[1]
# generating/overcoming/same-phase adjacency matrix
relation_types = ['same-phase', 'generating', 'overcoming']
rel_color = {'same-phase': '#CC9944', 'generating': '#44AA44', 'overcoming': '#CC4444'}
rel_matrix = {r: np.zeros((n, n), dtype=int) for r in relation_types}
node_order = sorted(G.nodes())
for u, v in G.edges():
    i, j = node_order.index(u), node_order.index(v)
    if wuxing[u] == wuxing[v]:
        rel_matrix['same-phase'][i, j] = rel_matrix['same-phase'][j, i] = 1
    elif (wuxing[u], wuxing[v]) in [('Water','Wood'), ('Wood','Fire'), ('Fire','Earth'), ('Earth','Metal'), ('Metal','Water')] or \
         (wuxing[v], wuxing[u]) in [('Water','Wood'), ('Wood','Fire'), ('Fire','Earth'), ('Earth','Metal'), ('Metal','Water')]:
        rel_matrix['generating'][i, j] = rel_matrix['generating'][j, i] = 1
    else:
        rel_matrix['overcoming'][i, j] = rel_matrix['overcoming'][j, i] = 1

# 3 matrixtext RGB channelstext composition
rgb = np.zeros((n, n, 3))
for idx, r in enumerate(relation_types):
    c = rel_color[r]
    val = 0.8 if r == 'overcoming' else 0.7
    if r == 'same-phase':
        rgb[:, :, 0] += rel_matrix[r] * 0.8
        rgb[:, :, 1] += rel_matrix[r] * 0.6
        rgb[:, :, 2] += rel_matrix[r] * 0.27
    elif r == 'generating':
        rgb[:, :, 1] += rel_matrix[r] * 0.67
    else:
        rgb[:, :, 0] += rel_matrix[r] * 0.8
rgb = np.clip(rgb, 0, 1)
ax.imshow(rgb, interpolation='nearest')
ax.set_xticks(range(n)); ax.set_xticklabels(node_order, fontsize=9)
ax.set_yticks(range(n)); ax.set_yticklabels(node_order, fontsize=9)
legend_elements = [Line2D([0], [0], color=rel_color[r], lw=4, label=r) for r in relation_types]
ax.legend(handles=legend_elements, loc='upper right', fontsize=11)
ax.set_title('text by type adjacency matrix (same-phase/generating/overcoming)', fontsize=13, fontweight='bold')
plt.tight_layout(); save_fig('12_wuxing_block_matrix.png'); plt.close()

# --- 13: 120-Node Construction text text ---
fig, axes = plt.subplots(1, 2, figsize=(18, 8))
ax = axes[0]
# 6 copytext circulartext layout
n_copies = 6
theta = np.linspace(0, 2*np.pi, n_copies, endpoint=False)
R = 6
colors_copy = plt.cm.tab10(np.linspace(0, 1, n_copies))
for i, t in enumerate(theta):
    cx, cy = R*np.cos(t), R*np.sin(t)
    # each copytext 4 shared verticestext text
    offsets = [(0, 0), (0.5, 0.5), (0.5, -0.5), (-0.5, 0)]
    for j, (dx, dy) in enumerate(offsets):
        x, y = cx + dx, cy + dy
        ax.plot(x, y, 'o', color=colors_copy[i], markersize=12, markeredgecolor='black', markeredgewidth=1.2)
        ax.text(x + 0.2, y + 0.2, f'{shared[j]+20*i}', fontsize=8, fontweight='bold')
    # adjacent copytext connection (circular)
    t2 = theta[(i+1) % n_copies]
    cx2, cy2 = R*np.cos(t2), R*np.sin(t2)
    ax.plot([cx, cx2], [cy, cy2], 'k--', alpha=0.3, linewidth=1)
inner = plt.Circle((0, 0), R*0.25, fill=False, color='red', linewidth=2, linestyle='--')
ax.add_patch(inner); ax.text(0, 0, 'CORE\n(source)', ha='center', va='center', fontsize=11, fontweight='bold', color='red')
ax.set_xlim(-8, 8); ax.set_ylim(-8, 8); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('120-Node Construction text: 20text × 6 copy (circular connection)', fontsize=14, fontweight='bold')

ax = axes[1]
# text text text
summary_text = (
    "120-Node Construction text combinatorial summary\n\n"
    "• copy text k = 0, 1, ..., 5\n"
    "• each copytext text set: {1+20k, ..., 20+20k}\n"
    "• text node count: 20 × 6 = 120\n"
    "• each copy internal text: 24 × 6 = 144\n"
    "• adjacent copy text connection: shared vertices 5+20k, 10+20k, 11+20k, 16+20k\n"
    "  text text copytext corresponding verticestext connection\n"
    "• text edge count: 144 + 4 × 6 = 168\n"
    "• text number sum: 6 × 210 + 20 × (0+1+...+5) × 20\n"
    "           = 1260 + 1200 = 2460\n"
    "• each copytext five phases sum: 34+38+42+46+50 = 210\n"
    "  → 6x extension five phases by group sumtext\n"
    "    204, 228, 252, 276, 300"
)
ax.axis('off')
ax.text(0.5, 0.5, summary_text, transform=ax.transAxes, fontsize=13,
        verticalalignment='center', horizontalalignment='center',
        bbox=dict(boxstyle='round,pad=0.8', facecolor='#FFF8DC', edgecolor='black', linewidth=2))
plt.tight_layout(); save_fig('13_extension_120.png'); plt.close()

# --- 14: 4 shared verticestext symmetry analysis ---
fig, ax = plt.subplots(1, 1, figsize=(14, 10))
# source graph on centrality/symmetry information text
for name, hedges in hex_edges.items():
    nx.draw_networkx_edges(G, POSITIONS, edgelist=hedges, edge_color=hex_colors[name], width=2.5, alpha=0.6, ax=ax)
nx.draw_networkx_nodes(G, POSITIONS, node_color=node_colors, node_size=1200, edgecolors='black', linewidths=1.5, ax=ax)
nx.draw_networkx_labels(G, POSITIONS, font_size=11, font_weight='bold', ax=ax)
# shared verticestext information text
for v in shared:
    x, y = POSITIONS[v]
    ax.text(x, y + 0.45, f"B={betw[v]:.3f}\nC={close[v]:.3f}", ha='center', va='bottom', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor='red', alpha=0.9))
ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5); ax.axis('off')
ax.set_title('shared vertices 5, 16, 10, 11text same centrality\n(structuretext text evidence)', fontsize=15, fontweight='bold')
plt.tight_layout(); save_fig('14_shared_vertex_symmetry.png'); plt.close()

# --- 15: text "Two Woods Rub Together" analysis (SW face text concentration) ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
# SW face highlight
sw_edges = hex_edges['SW']
nx.draw_networkx_edges(G, POSITIONS, edge_color='#EEEEEE', width=1, alpha=0.4, ax=ax)
nx.draw_networkx_edges(G, POSITIONS, edgelist=sw_edges, edge_color='#44AA44', width=5, alpha=0.95, ax=ax)
sw_nodes = HEXAGONS['SW']
nx.draw_networkx_nodes(G, POSITIONS, nodelist=sw_nodes, node_color='#44AA44', node_size=2500, edgecolors='black', linewidths=2.5, ax=ax)
other = [v for v in G.nodes() if v not in sw_nodes]
nx.draw_networkx_nodes(G, POSITIONS, nodelist=other, node_color='#F0F0F0', node_size=600, edgecolors='#CCCCCC', linewidths=1, ax=ax)
nx.draw_networkx_labels(G, POSITIONS, font_size=11, font_weight='bold', ax=ax)
ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5); ax.axis('off')
ax.set_title('SW face: Wood text 4vertices concentration\n"Two Woods Rub Together"text graph expression', fontsize=14, fontweight='bold')

ax = axes[1]
# each face five phases distribution (stacked bar)
face_names = ['NW', 'NE', 'SW', 'SE']
wx_counts = {name: Counter(wuxing[v] for v in HEXAGONS[name]) for name in face_names}
bottom = np.zeros(4)
for wx in wx_list:
    vals = [wx_counts[name].get(wx, 0) for name in face_names]
    ax.bar(face_names, vals, bottom=bottom, label=wx, color=wuxing_color[wx], edgecolor='black', linewidth=1)
    bottom += vals
ax.set_ylabel('Count', fontsize=11)
ax.set_title('3×2 rectangle each face five phases distribution', fontsize=13, fontweight='bold')
ax.legend(loc='upper right', fontsize=10)
for i, name in enumerate(face_names):
    ax.text(i, 6.3, f"Σ={sum(HEXAGONS[name])}", ha='center', fontsize=11, fontweight='bold')
plt.tight_layout(); save_fig('15_sw_wood_concentration.png'); plt.close()

print("\n" + "=" * 70)
print("All advanced analysis images generated")
print("=" * 70)
