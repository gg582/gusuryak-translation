#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nakseo Sagudo (洛書四九圖) — Modern graph-theoretic analysis script
Graph notation analysis of the Nakseo Sagudo from the Gusuryak (九數略) by Choi Seok-jeong
Analysis target: corrected original 20-node graph (four hexagonal faces of a 3×2 rectangular structure sharing vertices)
"""

import os
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm
from matplotlib.lines import Line2D

# Refresh matplotlib cache and set Korean/CJK fonts
fm._load_fontmanager(try_read_cache=False)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ============================================
# 0. Output directory setup
# ============================================
OUTPUT_DIR = '.'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================
# 1. Graph data structure (corrected original)
# ============================================

POSITIONS = {
    19: (-2,  3),
    2:  (-3,  2),
    14: (-2,  1),
    5:  (-1,  0),
    16: ( 0,  1),
    7:  (-1,  2),

    17: ( 2,  3),
    4:  ( 1,  2),
    9:  ( 3,  2),
    12: ( 2,  1),
    10: ( 1,  0),

    18: (-2, -1),
    3:  (-3, -2),
    13: (-2, -3),
    8:  (-1, -2),
    11: ( 0, -1),

    6:  ( 2, -1),
    1:  ( 3, -2),
    20: ( 2, -3),
    15: ( 1, -2),
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

# Outer 20-cycle (key structural discovery): visits every node exactly once
PERIMETER_20 = [19, 2, 14, 5, 18, 3, 13, 8, 11, 15, 20, 1, 6, 10, 12, 9, 17, 4, 16, 7]

# Inner 4-cycle (formed by the four central vertices of the faces in the 3×2 rectangular structure)
INNER_4 = [5, 16, 10, 11]

# Nine-palace composition based on the commentary "鄰星相兼五宫化 爲九宫每宫四子 各得四十二數"
NINE_PALACES = {
    'NW': [19, 2, 14, 7],
    'N':  [19, 17, 2, 4],
    'NE': [17, 4, 12, 9],
    'W':  [14, 7, 18, 3],
    'C':  [5, 16, 10, 11],
    'E':  [9, 12, 6, 15],
    'SW': [18, 3, 13, 8],
    'S':  [13, 8, 20, 1],
    'SE': [6, 1, 20, 15],
}

G = nx.Graph()
G.add_edges_from(EDGES)

# Five elements (mod 5) color classification
phase = {
    1: 'Water', 6: 'Water', 11: 'Water', 16: 'Water',
    2: 'Fire', 7: 'Fire', 12: 'Fire', 17: 'Fire',
    3: 'Wood', 8: 'Wood', 13: 'Wood', 18: 'Wood',
    4: 'Metal', 9: 'Metal', 14: 'Metal', 19: 'Metal',
    5: 'Earth', 10: 'Earth', 15: 'Earth', 20: 'Earth',
}

phase_color = {
    'Water': '#4488CC', 'Fire': '#CC4444', 'Wood': '#44AA44',
    'Metal': '#888888', 'Earth': '#CC9944',
}

PHASE_EN = {
    'Water': 'Water', 'Fire': 'Fire', 'Wood': 'Wood', 'Metal': 'Metal', 'Earth': 'Earth'
}

for node in G.nodes():
    G.nodes[node]['phase'] = phase[node]
    G.nodes[node]['color'] = phase_color[phase[node]]
    G.nodes[node]['remainder'] = node % 5 if node % 5 != 0 else 5

# ============================================
# 2. Graph-theoretic analysis
# ============================================

print("=" * 60)
print("Nakseo Sagudo graph-theoretic analysis results")
print("=" * 60)
print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}")
print(f"Connected components: {nx.number_connected_components(G)}")

deg_seq = sorted([d for _, d in G.degree()], reverse=True)
print(f"Degree sequence: {deg_seq}")
print(f"Degree-4 vertices: {[n for n, d in G.degree() if d == 4]} (4 vertices)")
print(f"Degree-2 vertices: {len([n for n, d in G.degree() if d == 2])} vertices")

try:
    girth = min(len(c) for c in nx.cycle_basis(G))
    print(f"Girth (shortest cycle length): {girth}")
except Exception:
    girth = None

print("\nFour faces (hexagons) of the 3×2 rectangular structure:")
for name, cycle in HEXAGONS.items():
    print(f"  {name}: {'-'.join(map(str, cycle))} (sum={sum(cycle)})")

print(f"\nOuter 20-cycle sum: {sum(PERIMETER_20)}")
print(f"Inner 4-cycle sum: {sum(INNER_4)}")

print("\nSums by five-element group (arithmetic sequence):")
for ph in ['Water', 'Fire', 'Wood', 'Metal', 'Earth']:
    ph_nodes = [n for n in G.nodes() if phase[n] == ph]
    print(f"  {ph}: {sum(ph_nodes)} ({ph_nodes})")

print("\nSum of each of the nine palaces (based on commentary):")
for name, palace in NINE_PALACES.items():
    print(f"  {name}: {palace} (sum={sum(palace)})")

betw = nx.betweenness_centrality(G)
print(f"\nBetweenness Centrality (Top 5):")
for n, v in sorted(betw.items(), key=lambda x: -x[1])[:5]:
    print(f"  {n}({phase[n]}): {v:.3f}")

# ============================================
# 3. Generate 7 visualization images
# ============================================

def save_fig(name):
    plt.savefig(f'{OUTPUT_DIR}/{name}', dpi=200, bbox_inches='tight')
    print(f"[Saved] {name}")

hex_edges = {}
for name, cycle in HEXAGONS.items():
    hex_edges[name] = [(cycle[i], cycle[(i+1)%6]) for i in range(6)]

perimeter_edges = [(PERIMETER_20[i], PERIMETER_20[(i+1)%20]) for i in range(20)]
inner_edges = [(INNER_4[i], INNER_4[(i+1)%4]) for i in range(4)]

# --- 01: Original graph ---
fig, ax = plt.subplots(1, 1, figsize=(12, 12))
hex_colors = {'NW': '#CC4444', 'NE': '#4488CC', 'SW': '#44AA44', 'SE': '#CC9944'}
for name, hedges in hex_edges.items():
    nx.draw_networkx_edges(G, POSITIONS, edgelist=hedges, edge_color=hex_colors[name], width=3, alpha=0.8, ax=ax)
node_colors = [G.nodes[n]['color'] for n in G.nodes()]
nx.draw_networkx_nodes(G, POSITIONS, node_color=node_colors, node_size=1500, edgecolors='black', linewidths=2, ax=ax)
nx.draw_networkx_labels(G, POSITIONS, font_size=14, font_weight='bold', ax=ax)
shared_nodes = [5, 16, 10, 11]
nx.draw_networkx_nodes(G, POSITIONS, nodelist=shared_nodes, node_color='white', node_size=1500, edgecolors='red', linewidths=3, ax=ax)
ax.set_title('Nakseo Sagudo (洛書四九圖) - Corrected original graph\n3×2 rectangular structure + outer 20-cycle + inner 4-cycle', fontsize=16, fontweight='bold')
ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5); ax.axis('off')
legend_elements = [mpatches.Patch(facecolor=phase_color[ph], edgecolor='black', label=f'{ph} ({PHASE_EN[ph]})') for ph in ['Water', 'Fire', 'Wood', 'Metal', 'Earth']]
legend_elements += [Line2D([0], [0], marker='o', color='w', markeredgecolor='red', markerfacecolor='white', markersize=10, label='Shared vertex (degree 4)')]
ax.legend(handles=legend_elements, loc='lower right', fontsize=10, framealpha=0.9, edgecolor='black')
save_fig('01_original_graph.png'); plt.close()

# --- 02: Five-element subgraph decomposition ---
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()
ax = axes[0]
for name, hedges in hex_edges.items():
    nx.draw_networkx_edges(G, POSITIONS, edgelist=hedges, edge_color=hex_colors[name], width=2.5, alpha=0.7, ax=ax)
nx.draw_networkx_nodes(G, POSITIONS, node_color=node_colors, node_size=1200, edgecolors='black', linewidths=1.5, ax=ax)
nx.draw_networkx_labels(G, POSITIONS, font_size=11, font_weight='bold', ax=ax)
ax.set_title('Full graph', fontsize=13, fontweight='bold'); ax.axis('off')

for idx, ph in enumerate(['Water', 'Fire', 'Wood', 'Metal', 'Earth']):
    ax = axes[idx + 1]
    ph_nodes = [n for n in G.nodes() if phase[n] == ph]
    ph_edges = [(u, v) for u, v in G.edges() if u in ph_nodes and v in ph_nodes]
    cross_edges = [(u, v) for u, v in G.edges() if (u in ph_nodes) != (v in ph_nodes)]
    nx.draw_networkx_edges(G, POSITIONS, edge_color='#EEEEEE', width=1, alpha=0.3, ax=ax)
    if cross_edges: nx.draw_networkx_edges(G, POSITIONS, edgelist=cross_edges, edge_color=phase_color[ph], width=2, alpha=0.3, style=':', ax=ax)
    if ph_edges: nx.draw_networkx_edges(G, POSITIONS, edgelist=ph_edges, edge_color=phase_color[ph], width=3.5, alpha=0.95, ax=ax)
    other_nodes = [n for n in G.nodes() if n not in ph_nodes]
    if other_nodes: nx.draw_networkx_nodes(G, POSITIONS, nodelist=other_nodes, node_color='#F0F0F0', node_size=500, edgecolors='#CCCCCC', linewidths=1, ax=ax)
    nx.draw_networkx_nodes(G, POSITIONS, nodelist=ph_nodes, node_color=phase_color[ph], node_size=1800, edgecolors='black', linewidths=2.5, ax=ax)
    nx.draw_networkx_labels(G, POSITIONS, font_size=10, font_weight='bold', ax=ax)
    ax.set_title(f'{ph} ({PHASE_EN[ph]})', fontsize=12, fontweight='bold', color=phase_color[ph]); ax.axis('off')

plt.suptitle('Subgraph decomposition by the Five Elements (五行)', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout(); save_fig('02_wuxing_decomposition.png'); plt.close()

# --- 03: Adjacency matrix + spectrum ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
adj = nx.adjacency_matrix(G, nodelist=sorted(G.nodes())).todense()
im = ax.imshow(adj, cmap='YlOrRd', interpolation='nearest')
ax.set_xticks(range(20)); ax.set_yticks(range(20))
ax.set_xticklabels(sorted(G.nodes()), fontsize=9); ax.set_yticklabels(sorted(G.nodes()), fontsize=9)
ph_sorted = [phase[n] for n in sorted(G.nodes())]
boundaries = [i - 0.5 for i in range(1, 20) if ph_sorted[i] != ph_sorted[i-1]]
for b in boundaries: ax.axhline(y=b, color='blue', linewidth=1.5, alpha=0.7); ax.axvline(x=b, color='blue', linewidth=1.5, alpha=0.7)
plt.colorbar(im, ax=ax, shrink=0.8)
ax.set_title('Adjacency Matrix', fontsize=13, fontweight='bold')

ax = axes[1]
eigenvalues = np.linalg.eigvalsh(adj)
ax.bar(range(len(eigenvalues)), sorted(eigenvalues, reverse=True), color='#4488CC', edgecolor='black', alpha=0.8)
ax.axhline(y=0, color='red', linestyle='--', linewidth=1)
ax.set_xlabel('Index', fontsize=11); ax.set_ylabel('Eigenvalue', fontsize=11)
ax.set_title(f'Graph Spectrum\nλ_max={max(eigenvalues):.2f}, λ_min={min(eigenvalues):.2f}', fontsize=13, fontweight='bold')
ax.grid(True, alpha=0.3)
plt.tight_layout(); save_fig('03_adjacency_spectrum.png'); plt.close()

# --- 04: Cycle analysis ---
fig, axes = plt.subplots(2, 2, figsize=(18, 16))

ax = axes[0, 0]
for name, hedges in hex_edges.items():
    nx.draw_networkx_edges(G, POSITIONS, edgelist=hedges, edge_color=hex_colors[name], width=3, alpha=0.8, ax=ax)
nx.draw_networkx_nodes(G, POSITIONS, node_color=node_colors, node_size=1500, edgecolors='black', linewidths=2, ax=ax)
nx.draw_networkx_labels(G, POSITIONS, font_size=12, font_weight='bold', ax=ax)
ax.set_title('Four faces (6-cycles) of the 3×2 rectangular structure', fontsize=13, fontweight='bold')
ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5); ax.axis('off'); ax.set_aspect('equal')

ax = axes[0, 1]
nx.draw_networkx_edges(G, POSITIONS, edgelist=perimeter_edges, edge_color='#333333', width=3, alpha=0.9, ax=ax)
nx.draw_networkx_edges(G, POSITIONS, edgelist=inner_edges, edge_color='red', width=2.5, alpha=0.7, style='--', ax=ax)
nx.draw_networkx_nodes(G, POSITIONS, nodelist=INNER_4, node_color='#CC9944', node_size=1800, edgecolors='red', linewidths=2.5, ax=ax)
other_nodes = [n for n in G.nodes() if n not in INNER_4]
nx.draw_networkx_nodes(G, POSITIONS, nodelist=other_nodes, node_color='white', node_size=1000, edgecolors='black', linewidths=1.5, ax=ax)
nx.draw_networkx_labels(G, POSITIONS, font_size=11, font_weight='bold', ax=ax)
ax.set_title(f'Outer 20-cycle + inner 4-cycle\n(20-cycle sum={sum(PERIMETER_20)}, 4-cycle sum={sum(INNER_4)})', fontsize=13, fontweight='bold')
ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5); ax.axis('off'); ax.set_aspect('equal')

ax = axes[1, 0]
hex_names = list(HEXAGONS.keys())
hex_sums = [sum(HEXAGONS[h]) for h in hex_names]
hex_bar_colors = [hex_colors[h] for h in hex_names]
ax.bar(hex_names, hex_sums, color=hex_bar_colors, edgecolor='black', linewidth=1.5)
ax.set_title('Sum of nodes in each face of the 3×2 rectangular structure', fontsize=13, fontweight='bold')
for bar, val in zip(ax.patches, hex_sums):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, str(val), ha='center', fontsize=12, fontweight='bold')

ax = axes[1, 1]
cumsum = np.cumsum([n for n in PERIMETER_20])
ax.plot(range(20), cumsum, 'o-', color='#CC4444', linewidth=2.5, markersize=8, markeredgecolor='black')
ax.fill_between(range(20), cumsum, alpha=0.2, color='#CC4444')
ax.set_xticks(range(20)); ax.set_xticklabels([str(n) for n in PERIMETER_20], fontsize=9)
ax.set_title(f'Cumulative sum of the outer 20-cycle (Total={sum(PERIMETER_20)})', fontsize=13, fontweight='bold')
ax.grid(True, alpha=0.3); ax.axhline(y=sum(PERIMETER_20)/2, color='blue', linestyle='--', alpha=0.5)

plt.tight_layout(); save_fig('04_cycle_analysis.png'); plt.close()

# --- 05: Centrality + sum invariants ---
fig, axes = plt.subplots(2, 2, figsize=(16, 14))
ax = axes[0, 0]
betw = nx.betweenness_centrality(G)
nodes_sorted = sorted(G.nodes(), key=lambda n: betw[n], reverse=True)
colors_sorted = [G.nodes[n]['color'] for n in nodes_sorted]
ax.bar(range(20), [betw[n] for n in nodes_sorted], color=colors_sorted, edgecolor='black')
ax.set_xticks(range(20)); ax.set_xticklabels([str(n) for n in nodes_sorted], fontsize=9)
ax.set_title('Betweenness Centrality', fontsize=12, fontweight='bold'); ax.set_ylabel('Centrality', fontsize=10)

ax = axes[0, 1]
ph_sums = {ph: sum([n for n in G.nodes() if phase[n] == ph]) for ph in ['Water', 'Fire', 'Wood', 'Metal', 'Earth']}
ph_names = list(ph_sums.keys()); ph_vals = list(ph_sums.values()); ph_colors_bar = [phase_color[w] for w in ph_names]
ax.bar(ph_names, ph_vals, color=ph_colors_bar, edgecolor='black', linewidth=1.5)
ax.set_title('Sums by five-element group (34, 38, 42, 46, 50)', fontsize=12, fontweight='bold')
for bar, val in zip(ax.patches, ph_vals): ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, str(val), ha='center', fontsize=12, fontweight='bold')
ax.plot(range(5), ph_vals, 'o--', color='black', alpha=0.5, linewidth=2)

ax = axes[1, 0]
components = {'NW face': sum(HEXAGONS['NW']), 'NE face': sum(HEXAGONS['NE']),
              'SW face': sum(HEXAGONS['SW']), 'SE face': sum(HEXAGONS['SE']),
              'Outer 20-cycle': sum(PERIMETER_20), 'Inner 4-cycle': sum(INNER_4), 'Total': sum(range(1, 21))}
ax.bar(list(components.keys()), list(components.values()), color=['#CC4444', '#4488CC', '#44AA44', '#CC9944', '#888888', '#CC9944', '#333333'], edgecolor='black', linewidth=1.5)
ax.set_title('Sum of structural subsets', fontsize=12, fontweight='bold'); ax.set_ylabel('Sum', fontsize=10)
plt.setp(ax.xaxis.get_majorticklabels(), rotation=15, ha='right')

ax = axes[1, 1]
neighbor_sums = {n: sum(G.neighbors(n)) for n in G.nodes()}
nodes_ns = sorted(G.nodes()); ns_vals = [neighbor_sums[n] for n in nodes_ns]; ns_colors = [G.nodes[n]['color'] for n in nodes_ns]
ax.bar(range(20), ns_vals, color=ns_colors, edgecolor='black')
ax.set_xticks(range(20)); ax.set_xticklabels([str(n) for n in nodes_ns], fontsize=9)
ax.set_title('Sum of neighbors for each node', fontsize=12, fontweight='bold')
ax.axhline(y=np.mean(ns_vals), color='red', linestyle='--', alpha=0.5)
plt.tight_layout(); save_fig('05_centrality_invariants.png'); plt.close()

# --- 06: Five-element mutual generation and mutual overcoming ---
fig, axes = plt.subplots(1, 2, figsize=(18, 8))
ax = axes[0]
phase_graph = nx.DiGraph()
phase_relations = [
    ('Water', 'Wood', 'generation'), ('Wood', 'Fire', 'generation'), ('Fire', 'Earth', 'generation'), ('Earth', 'Metal', 'generation'), ('Metal', 'Water', 'generation'),
    ('Water', 'Fire', 'overcoming'), ('Fire', 'Metal', 'overcoming'), ('Metal', 'Wood', 'overcoming'), ('Wood', 'Earth', 'overcoming'), ('Earth', 'Water', 'overcoming'),
]
for u, v, r in phase_relations: phase_graph.add_edge(u, v, relation=r)
ph_pos = {'Water': (0, 2), 'Wood': (2, 1), 'Fire': (1, -1), 'Earth': (-1, -1), 'Metal': (-2, 1)}
sheng_edges = [(u, v) for u, v, r in phase_relations if r == 'generation']
ke_edges = [(u, v) for u, v, r in phase_relations if r == 'overcoming']
nx.draw_networkx_edges(phase_graph, ph_pos, edgelist=sheng_edges, edge_color='#44AA44', width=3, alpha=0.8, arrows=True, arrowsize=20, connectionstyle='arc3,rad=0.15', ax=ax)
nx.draw_networkx_edges(phase_graph, ph_pos, edgelist=ke_edges, edge_color='#CC4444', width=2, alpha=0.6, style='--', arrows=True, arrowsize=15, connectionstyle='arc3,rad=-0.15', ax=ax)
ph_node_colors = [phase_color[w] for w in phase_graph.nodes()]
nx.draw_networkx_nodes(phase_graph, ph_pos, node_color=ph_node_colors, node_size=3000, edgecolors='black', linewidths=2.5, ax=ax)
nx.draw_networkx_labels(phase_graph, ph_pos, font_size=14, font_weight='normal', ax=ax)
legend_elements = [Line2D([0], [0], color='#44AA44', lw=3, label='Mutual generation'), Line2D([0], [0], color='#CC4444', lw=2, linestyle='--', label='Mutual overcoming')]
ax.legend(handles=legend_elements, loc='upper right', fontsize=11)
ax.set_title('Five-element mutual generation and mutual overcoming', fontsize=13, fontweight='bold'); ax.set_xlim(-3, 3.5); ax.set_ylim(-2.5, 3); ax.axis('off')

ax = axes[1]
ph_edge_counts = {}
for u, v in G.edges():
    wu, wv = phase[u], phase[v]
    if wu == wv: key = f'{wu} (same)'
    elif (wu, wv) in [('Water','Wood'), ('Wood','Fire'), ('Fire','Earth'), ('Earth','Metal'), ('Metal','Water')] or (wv, wu) in [('Water','Wood'), ('Wood','Fire'), ('Fire','Earth'), ('Earth','Metal'), ('Metal','Water')]: key = 'Mutual generation'
    elif (wu, wv) in [('Water','Fire'), ('Fire','Metal'), ('Metal','Wood'), ('Wood','Earth'), ('Earth','Water')] or (wv, wu) in [('Water','Fire'), ('Fire','Metal'), ('Metal','Wood'), ('Wood','Earth'), ('Earth','Water')]: key = 'Mutual overcoming'
    else: key = 'Neutral'
    ph_edge_counts[key] = ph_edge_counts.get(key, 0) + 1
colors_pie = ['#44AA44', '#CC4444', '#CC9944', '#4488CC']
ax.pie(list(ph_edge_counts.values()), labels=list(ph_edge_counts.keys()), autopct='%1.0f%%',
       colors=colors_pie[:len(ph_edge_counts)], explode=[0.05]*len(ph_edge_counts),
       textprops={'fontsize': 12, 'fontweight': 'bold'})
ax.set_title(f'Five-element edge distribution (N={G.number_of_edges()})', fontsize=13, fontweight='bold')
plt.tight_layout(); save_fig('06_wuxing_relations.png'); plt.close()

# --- 07: Extension designs based on the original ---
fig, axes = plt.subplots(1, 2, figsize=(18, 8))
ax = axes[0]
n_copies = 6; theta = np.linspace(0, 2*np.pi, n_copies + 1)[:-1]; r = 5
for i, t in enumerate(theta):
    cx, cy = r * np.cos(t), r * np.sin(t); offset = i * 20
    ax.plot(cx, cy, 'o', color='#CC9944', markersize=15, markeredgecolor='black', markeredgewidth=1.5)
    ax.text(cx + 0.3, cy + 0.3, f'{5+offset}', fontsize=8, fontweight='bold')
    for j, angle in enumerate([0.5, 1.5, 2.5, 3.5]):
        px, py = cx + 1.5 * np.cos(angle), cy + 1.5 * np.sin(angle)
        ax.plot([cx, px], [cy, py], '-', color=['#4488CC', '#CC4444', '#44AA44', '#888888'][j], alpha=0.5, linewidth=1)
        ax.plot(px, py, '.', color=['#4488CC', '#CC4444', '#44AA44', '#888888'][j], markersize=4)
inner_circle = plt.Circle((0, 0), r*0.3, fill=False, color='red', linewidth=2, linestyle='--')
ax.add_patch(inner_circle); ax.text(0, 0, 'CORE', ha='center', va='center', fontsize=12, fontweight='bold', color='red')
ax.set_xlim(-8, 8); ax.set_ylim(-8, 8); ax.set_aspect('equal')
ax.set_title('120-node structure (20 × 6 copies)', fontsize=13, fontweight='bold'); ax.axis('off')

ax = axes[1]
quad = np.array([[0, 1], [1, 1], [1, 0], [0, 0], [0, 1]]) * 3
ax.plot(quad[:,0], quad[:,1], 'o-', color='black', linewidth=2, markersize=12, markerfacecolor='#CC9944')
for i, (x, y) in enumerate([[0,1],[1,1],[1,0],[0,0]]):
    label = ['NW\n(5,16)', 'NE\n(16,10)', 'SE\n(10,11)', 'SW\n(11,5)'][i]
    ax.text(x*3, y*3, label, ha='center', va='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', edgecolor='black'))
ax.set_xlim(-1, 4); ax.set_ylim(-1, 4); ax.set_aspect('equal')
ax.set_title('Dual structure of the 3×2 rectangular structure\nShared vertices 5-16-10-11', fontsize=13, fontweight='bold'); ax.axis('off')
plt.tight_layout(); save_fig('07_local_extensions.png'); plt.close()

# ============================================
# 4. Generate images based on the original commentary
# ============================================

print("\n" + "-" * 60)
print("Generating analysis images based on the original commentary")
print("-" * 60)

# --- origin_01: Hetu 4-5 basis and five palaces ---
fig, axes = plt.subplots(1, 2, figsize=(18, 8))
ax = axes[0]
# Hetu 4-5: four directions and five elements layout
river_diagram_positions = {
    '1/6\nWater': (0, 2), '2/7\nFire': (0, -2),
    '3/8\nWood': (-2, 0), '4/9\nMetal': (2, 0),
    '5/10\nEarth': (0, 0),
}
for label, (x, y) in river_diagram_positions.items():
    ph = label.split('\n')[1]
    ax.add_patch(plt.Circle((x, y), 0.6, facecolor=phase_color[ph], edgecolor='black', linewidth=2))
    ax.text(x, y, label, ha='center', va='center', fontsize=11, fontweight='bold')
# Connection lines: mutual generation cycle
for a, b in [('1/6\nWater','3/8\nWood'), ('3/8\nWood','2/7\nFire'), ('2/7\nFire','5/10\nEarth'), ('5/10\nEarth','4/9\nMetal'), ('4/9\nMetal','1/6\nWater')]:
    x1, y1 = river_diagram_positions[a]; x2, y2 = river_diagram_positions[b]
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='#44AA44', lw=2, connectionstyle='arc3,rad=0.15'))
ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('Hetu 4-5 basis (Four Images + Five at center)\n4×5=20, 4+5=9', fontsize=14, fontweight='bold')

ax = axes[1]
# Five palaces = five-element groups
ph_groups = {
    'Water': [1, 6, 11, 16], 'Fire': [2, 7, 12, 17], 'Wood': [3, 8, 13, 18],
    'Metal': [4, 9, 14, 19], 'Earth': [5, 10, 15, 20]
}
positions_5 = [(0, 2), (-2, 0.5), (2, 0.5), (-1, -2), (1, -2)]
for (ph, nodes), (x, y) in zip(ph_groups.items(), positions_5):
    ax.add_patch(plt.Circle((x, y), 0.7, facecolor=phase_color[ph], edgecolor='black', linewidth=2))
    ax.text(x, y+0.15, f'{ph}\n{" ".join(map(str, nodes))}\nSum={sum(nodes)}', ha='center', va='center', fontsize=10, fontweight='bold')
ax.set_xlim(-3, 3); ax.set_ylim(-3.5, 3.5); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('Five palaces: four-node groups by five-element\nTotal sum 210, average 42', fontsize=14, fontweight='bold')
plt.tight_layout(); save_fig('origin_01_hutu_5palaces.png'); plt.close()

# --- origin_02: Adjacent stars combined → nine palaces, 42-sum grid ---
fig, ax = plt.subplots(1, 1, figsize=(12, 12))
grid_pos = {
    'NW': (-2, 2), 'N': (0, 2), 'NE': (2, 2),
    'W': (-2, 0), 'C': (0, 0), 'E': (2, 0),
    'SW': (-2, -2), 'S': (0, -2), 'SE': (2, -2),
}
for name, (x, y) in grid_pos.items():
    palace_nodes = NINE_PALACES[name]
    # Palace boundary
    rect = plt.Rectangle((x-0.9, y-0.9), 1.8, 1.8, fill=True, facecolor='lightyellow', edgecolor='black', linewidth=2)
    ax.add_patch(rect)
    # Four-node layout
    offsets = [(-0.4, 0.3), (0.4, 0.3), (-0.4, -0.3), (0.4, -0.3)]
    for node, (dx, dy) in zip(palace_nodes, offsets):
        circle = plt.Circle((x+dx, y+dy), 0.22, facecolor=phase_color[phase[node]], edgecolor='black', linewidth=1.5)
        ax.add_patch(circle)
        ax.text(x+dx, y+dy, str(node), ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(x, y+0.72, f'{name}', ha='center', va='center', fontsize=13, fontweight='bold')
    ax.text(x, y-0.72, f'Sum=42', ha='center', va='center', fontsize=12, fontweight='bold', color='red')

# Arrows indicating clockwise rotation
arrow_style = dict(arrowstyle='->', color='purple', lw=2.5, connectionstyle='arc3,rad=0.2')
for start, end in [('NW','N'), ('N','NE'), ('NE','E'), ('E','SE'), ('SE','S'), ('S','SW'), ('SW','W'), ('W','NW')]:
    x1, y1 = grid_pos[start]; x2, y2 = grid_pos[end]
    ax.annotate('', xy=(x2-0.5*np.sign(x2), y2-0.5*np.sign(y2)), xytext=(x1+0.5*np.sign(x1), y1+0.5*np.sign(y1)),
                arrowprops=arrow_style)
ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('Adjacent stars combined: five palaces become nine palaces\nEach palace has four nodes, each summing to 42', fontsize=16, fontweight='bold')
plt.tight_layout(); save_fig('origin_02_9palace_grid.png'); plt.close()

# --- origin_03: Right rotation transformation ---
fig, ax = plt.subplots(1, 1, figsize=(12, 10))
# Left: five palaces
left_pos = {'Water': (0, 2), 'Wood': (-1.5, 0.5), 'Fire': (1.5, 0.5), 'Metal': (-0.8, -1.5), 'Earth': (0.8, -1.5)}
for ph, (x, y) in left_pos.items():
    ax.add_patch(plt.Circle((x-5, y), 0.6, facecolor=phase_color[ph], edgecolor='black', linewidth=2))
    ax.text(x-5, y, ph, ha='center', va='center', fontsize=14, fontweight='bold')
# Right: nine palaces (3x3)
for name, (x, y) in grid_pos.items():
    ax.add_patch(plt.Rectangle((x+2.1, y-0.4), 0.8, 0.8, fill=True, facecolor='lightyellow', edgecolor='black', linewidth=1.5))
    ax.text(x+2.5, y, '42', ha='center', va='center', fontsize=11, fontweight='bold')
# Arrow + rotation symbol
ax.annotate('', xy=(1, 0), xytext=(-3, 0), arrowprops=dict(arrowstyle='->', color='black', lw=3))
ax.text(-1, 0.6, 'Right rotation (clockwise)', ha='center', va='center', fontsize=14, fontweight='bold')
ax.text(-1, -0.6, '5 palaces → 9 palaces', ha='center', va='center', fontsize=13, fontweight='bold')
ax.set_xlim(-7, 5.5); ax.set_ylim(-3.5, 3.5); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('Hetu 4-5 diagram rotated right\nFive palaces rotate clockwise into nine palaces', fontsize=16, fontweight='bold')
plt.tight_layout(); save_fig('origin_03_right_rotation.png'); plt.close()

# --- origin_04: Mutual transformation 1890 ---
fig, ax = plt.subplots(1, 1, figsize=(14, 10))
# Five palaces (left column)
ph_list = ['Water', 'Fire', 'Wood', 'Metal', 'Earth']
for i, ph in enumerate(ph_list):
    y = 2 - i * 1.0
    ax.add_patch(plt.Circle((-3, y), 0.35, facecolor=phase_color[ph], edgecolor='black', linewidth=2))
    ax.text(-3, y, ph, ha='center', va='center', fontsize=12, fontweight='bold')
# Nine palaces (top row)
palace_names = list(grid_pos.keys())
for j, name in enumerate(palace_names):
    x = -2 + j * 0.9
    ax.add_patch(plt.Rectangle((x-0.3, 3.2), 0.6, 0.6, fill=True, facecolor='lightyellow', edgecolor='black', linewidth=1.5))
    ax.text(x, 3.5, name, ha='center', va='center', fontsize=9, fontweight='bold')
# Connection lines: 5 × 9 = 45
for i in range(5):
    for j in range(9):
        x = -2 + j * 0.9
        y = 2 - i * 1.0
        ax.plot([-3+0.3, x], [y, 3.2], '-', color='gray', alpha=0.15, linewidth=0.5)
# Formula
ax.text(0, -3, 'Mutual transformation: 5 palaces × 9 palaces = 45', ha='center', va='center', fontsize=18, fontweight='bold')
ax.text(0, -3.7, '45 × 42 = 1,890', ha='center', va='center', fontsize=22, fontweight='bold', color='red')
ax.set_xlim(-4, 6.5); ax.set_ylim(-4.5, 4.5); ax.axis('off')
ax.set_title('Mutual transformation yields 1,890', fontsize=18, fontweight='bold')
plt.tight_layout(); save_fig('origin_04_mutual_transformation_1890.png'); plt.close()

# --- origin_05: 42 invariant analysis ---
fig, axes = plt.subplots(2, 2, figsize=(16, 14))

# Outer four vertices of each of the four faces + inner 4-cycle
ax = axes[0, 0]
labels_42 = ['NW\nouter', 'NE\nouter', 'SW\nouter', 'SE\nouter', 'Inner\n4-cycle']
values_42 = [sum(NINE_PALACES[k]) for k in ['NW', 'NE', 'SW', 'SE', 'C']]
colors_42 = ['#CC4444', '#4488CC', '#44AA44', '#CC9944', '#888888']
ax.bar(labels_42, values_42, color=colors_42, edgecolor='black', linewidth=1.5)
ax.axhline(y=42, color='red', linestyle='--', linewidth=2)
ax.set_title('Five-palace structure of the 42 sum', fontsize=13, fontweight='bold')
for bar, val in zip(ax.patches, values_42):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, str(val), ha='center', fontsize=12, fontweight='bold')

# Nine-palace grid colorization
ax = axes[0, 1]
for name, (x, y) in grid_pos.items():
    palace_nodes = NINE_PALACES[name]
    rect = plt.Rectangle((x-0.9, y-0.9), 1.8, 1.8, fill=True, facecolor='#FFF8DC', edgecolor='black', linewidth=2)
    ax.add_patch(rect)
    ax.text(x, y+0.6, name, ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(x, y-0.6, 'Σ=42', ha='center', va='center', fontsize=11, fontweight='bold', color='red')
    # Display nodes as colored dots
    for k, node in enumerate(palace_nodes):
        angle = 2 * np.pi * k / 4
        px, py = x + 0.45 * np.cos(angle), y + 0.45 * np.sin(angle)
        ax.add_patch(plt.Circle((px, py), 0.15, facecolor=phase_color[phase[node]], edgecolor='black', linewidth=1))
        ax.text(px, py, str(node), ha='center', va='center', fontsize=9, fontweight='bold')
ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('Nine-palace 42-invariant distribution', fontsize=13, fontweight='bold')

# Five palaces → nine palaces → 1890 flow
ax = axes[1, 0]
ax.text(0.5, 0.8, 'Five palaces (5 palaces)', ha='center', va='center', fontsize=14, fontweight='bold')
ax.text(0.5, 0.65, 'avg sum = 42', ha='center', va='center', fontsize=12)
ax.annotate('', xy=(0.5, 0.45), xytext=(0.5, 0.55), arrowprops=dict(arrowstyle='->', color='black', lw=2))
ax.text(0.5, 0.35, 'Right rotation → Nine palaces (9 palaces)', ha='center', va='center', fontsize=14, fontweight='bold')
ax.text(0.5, 0.2, 'each sum = 42', ha='center', va='center', fontsize=12)
ax.annotate('', xy=(0.5, 0.0), xytext=(0.5, 0.1), arrowprops=dict(arrowstyle='->', color='black', lw=2))
ax.text(0.5, -0.15, 'Mutual transformation: 5 × 9 = 45 interactions', ha='center', va='center', fontsize=14, fontweight='bold')
ax.text(0.5, -0.35, '45 × 42 = 1,890', ha='center', va='center', fontsize=20, fontweight='bold', color='red')
ax.set_xlim(0, 1); ax.set_ylim(-0.6, 1); ax.axis('off')
ax.set_title('Mathematical flow of the commentary', fontsize=13, fontweight='bold')

# Five-element distribution in each palace
ax = axes[1, 1]
palace_names_ordered = ['NW', 'N', 'NE', 'W', 'C', 'E', 'SW', 'S', 'SE']
ph_counts_per_palace = {name: {} for name in palace_names_ordered}
for name in palace_names_ordered:
    for node in NINE_PALACES[name]:
        ph = phase[node]
        ph_counts_per_palace[name][ph] = ph_counts_per_palace[name].get(ph, 0) + 1

bottom = np.zeros(9)
for ph in ['Water', 'Fire', 'Wood', 'Metal', 'Earth']:
    counts = [ph_counts_per_palace[name].get(ph, 0) for name in palace_names_ordered]
    ax.bar(palace_names_ordered, counts, bottom=bottom, label=ph, color=phase_color[ph], edgecolor='black', linewidth=1)
    bottom += counts
ax.set_title('Five-element distribution in each of the nine palaces', fontsize=13, fontweight='bold')
ax.legend(loc='upper right')
ax.set_ylabel('Count')

plt.tight_layout(); save_fig('origin_05_42_invariants.png'); plt.close()

# --- origin_06: Nine-palace overlay on the corrected graph ---
fig, ax = plt.subplots(1, 1, figsize=(14, 14))
for name, hedges in hex_edges.items():
    nx.draw_networkx_edges(G, POSITIONS, edgelist=hedges, edge_color=hex_colors[name], width=2.5, alpha=0.6, ax=ax)
nx.draw_networkx_nodes(G, POSITIONS, node_color=node_colors, node_size=1200, edgecolors='black', linewidths=1.5, ax=ax)
nx.draw_networkx_labels(G, POSITIONS, font_size=11, font_weight='bold', ax=ax)
# Mark nine-palace regions
palace_regions = {
    'NW': (-2.3, 2.3), 'N': (0, 2.3), 'NE': (2.3, 2.3),
    'W': (-2.3, 0), 'C': (0, 0), 'E': (2.3, 0),
    'SW': (-2.3, -2.3), 'S': (0, -2.3), 'SE': (2.3, -2.3),
}
for name, (x, y) in palace_regions.items():
    ax.text(x, y, f'{name}\nΣ42', ha='center', va='center', fontsize=13, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='red', alpha=0.85))
ax.set_title('Nine-palace interpretation overlaid on the original graph\nRegional division by adjacent stars combined', fontsize=16, fontweight='bold')
ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5); ax.axis('off')
plt.tight_layout(); save_fig('origin_06_graph_with_9palace.png'); plt.close()

# ============================================
# 5. Generate modern combinatorial translation images of the original commentary
# ============================================

print("\n" + "-" * 60)
print("Generating modern combinatorial translation images of the original commentary")
print("-" * 60)

modern_terms = [
    ('鄰星相兼', 'adjacent blocks overlap / neighboring 4-subsets are combined'),
    ('五宮化爲九宫', '5 residue classes are reorganized into 9 blocks'),
    ('每宮四子', 'each block has cardinality 4'),
    ('各得四十二數', 'each block has invariant sum 42'),
    ('右旋', 'clockwise cyclic action on the boundary blocks'),
    ('互化則一千八百九十數', '5 × 9 incidence product, weighted by 42 = 1,890'),
]

# --- origin_translated_01: Translate classical phrases into modern combinatorial propositions ---
fig, ax = plt.subplots(1, 1, figsize=(16, 10))
ax.axis('off')
ax.set_title('Original commentary → Modern combinatorial terms', fontsize=20, fontweight='bold', pad=20)
for i, (classical, modern) in enumerate(modern_terms):
    y = 0.88 - i * 0.14
    ax.text(0.05, y, classical, ha='left', va='center', fontsize=18, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF8DC', edgecolor='black'))
    ax.annotate('', xy=(0.42, y), xytext=(0.32, y),
                arrowprops=dict(arrowstyle='->', lw=2.5, color='black'))
    ax.text(0.45, y, modern, ha='left', va='center', fontsize=15,
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#EAF3FF', edgecolor='#336699'))
ax.text(0.5, 0.03,
        'Core translation: the commentary is not a mystical metaphor, but a description of a balanced block structure\n'
        'that rearranges the 20 numbers into several 4-subsets (blocks) all having the same sum of 42.',
        ha='center', va='center', fontsize=15, fontweight='bold', color='#333333')
plt.tight_layout(); save_fig('origin_translated_01_terms.png'); plt.close()

# --- origin_translated_02: From 5 residue classes to 9 blocks ---
fig, axes = plt.subplots(1, 2, figsize=(18, 9))
ax = axes[0]
for i, ph in enumerate(['Water', 'Fire', 'Wood', 'Metal', 'Earth']):
    nodes = [n for n in sorted(G.nodes()) if phase[n] == ph]
    y = 4 - i
    ax.add_patch(plt.Rectangle((-0.7, y-0.35), 4.1, 0.7, facecolor=phase_color[ph], edgecolor='black', alpha=0.85))
    ax.text(-1.0, y, f'{ph}', ha='right', va='center', fontsize=14, fontweight='bold')
    ax.text(1.35, y, f'{{{", ".join(map(str, nodes))}}}', ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(3.75, y, f'Σ={sum(nodes)}', ha='left', va='center', fontsize=12)
ax.set_xlim(-1.5, 5.2); ax.set_ylim(-0.8, 4.8); ax.axis('off')
ax.set_title('Input: 5 residue classes\nFive-element groups by mod 5', fontsize=15, fontweight='bold')

ax = axes[1]
for name, (x, y) in grid_pos.items():
    nodes = NINE_PALACES[name]
    ax.add_patch(plt.Rectangle((x-0.88, y-0.75), 1.76, 1.5, facecolor='#F7FBFF', edgecolor='black', linewidth=2))
    ax.text(x, y+0.48, f'B_{name}', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(x, y+0.05, '{' + ', '.join(map(str, nodes)) + '}', ha='center', va='center', fontsize=10)
    ax.text(x, y-0.48, '|B|=4, Σ=42', ha='center', va='center', fontsize=10, color='red', fontweight='bold')
ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('Output: 9 four-blocks\nEvery block has sum 42', fontsize=15, fontweight='bold')
fig.suptitle('Five palaces become nine palaces = reorganizing 5 classes into 9 balanced blocks', fontsize=18, fontweight='bold')
plt.tight_layout(); save_fig('origin_translated_02_blocks.png'); plt.close()

# --- origin_translated_03: Interpreting "adjacent stars combined" as block overlap ---
fig, ax = plt.subplots(1, 1, figsize=(14, 12))
for name, (x, y) in grid_pos.items():
    nodes = NINE_PALACES[name]
    ax.add_patch(plt.Rectangle((x-0.78, y-0.78), 1.56, 1.56, facecolor='#FFFDF2', edgecolor='black', linewidth=2))
    ax.text(x, y+0.55, name, ha='center', va='center', fontsize=13, fontweight='bold')
    ax.text(x, y, '\n'.join(map(str, nodes)), ha='center', va='center', fontsize=12)
    ax.text(x, y-0.58, 'Σ42', ha='center', va='center', fontsize=11, color='red', fontweight='bold')

for a, b in [('NW','N'), ('N','NE'), ('W','C'), ('C','E'), ('SW','S'), ('S','SE'), ('NW','W'), ('W','SW'), ('N','C'), ('C','S'), ('NE','E'), ('E','SE')]:
    ax1, ay1 = grid_pos[a]; ax2, ay2 = grid_pos[b]
    inter = sorted(set(NINE_PALACES[a]) & set(NINE_PALACES[b]))
    if inter:
        mx, my = (ax1 + ax2) / 2, (ay1 + ay2) / 2
        ax.plot([ax1, ax2], [ay1, ay2], color='#336699', linewidth=1.8, alpha=0.55)
        ax.text(mx, my, '∩={' + ','.join(map(str, inter)) + '}', ha='center', va='center', fontsize=9,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#336699', alpha=0.9))

ax.set_xlim(-3.2, 3.2); ax.set_ylim(-3.2, 3.2); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('Adjacent stars combined = constructing the nine palaces from overlaps of neighboring blocks', fontsize=17, fontweight='bold')
plt.tight_layout(); save_fig('origin_translated_03_overlap.png'); plt.close()

# --- origin_translated_04: 42-sum invariant as a block design table ---
fig, ax = plt.subplots(1, 1, figsize=(15, 9))
palace_names_ordered = ['NW', 'N', 'NE', 'W', 'C', 'E', 'SW', 'S', 'SE']
table_data = []
for name in palace_names_ordered:
    nodes = NINE_PALACES[name]
    table_data.append([f'B_{name}', '{' + ', '.join(map(str, nodes)) + '}', len(nodes), sum(nodes)])
table = ax.table(
    cellText=table_data,
    colLabels=['block', 'elements', 'cardinality', 'sum invariant'],
    cellLoc='center',
    colLoc='center',
    loc='center',
    colWidths=[0.14, 0.42, 0.18, 0.22],
)
table.auto_set_font_size(False)
table.set_fontsize(13)
table.scale(1, 2.0)
for (row, col), cell in table.get_celld().items():
    cell.set_edgecolor('black')
    if row == 0:
        cell.set_facecolor('#DDEEFF')
        cell.set_text_props(fontweight='bold')
    elif col == 3:
        cell.set_facecolor('#FFF1F1')
        cell.set_text_props(color='red', fontweight='bold')
ax.axis('off')
ax.set_title('Each palace has four nodes, each summing to 42 = nine 4-blocks share the same sum invariant 42', fontsize=17, fontweight='bold')
plt.tight_layout(); save_fig('origin_translated_04_invariant_table.png'); plt.close()

# --- origin_translated_05: Right rotation as cyclic permutation ---
fig, ax = plt.subplots(1, 1, figsize=(13, 13))
cycle_order = ['NW', 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W']
theta = np.linspace(np.pi * 3/4, np.pi * 3/4 - 2*np.pi, len(cycle_order), endpoint=False)
cycle_pos = {name: (2.4*np.cos(t), 2.4*np.sin(t)) for name, t in zip(cycle_order, theta)}
for name in cycle_order:
    x, y = cycle_pos[name]
    ax.add_patch(plt.Circle((x, y), 0.55, facecolor='#EAF3FF', edgecolor='black', linewidth=2))
    ax.text(x, y+0.12, f'B_{name}', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(x, y-0.18, 'Σ42', ha='center', va='center', fontsize=10, color='red', fontweight='bold')
for i, name in enumerate(cycle_order):
    nxt = cycle_order[(i + 1) % len(cycle_order)]
    x1, y1 = cycle_pos[name]; x2, y2 = cycle_pos[nxt]
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='purple', lw=2.5, shrinkA=28, shrinkB=28,
                                connectionstyle='arc3,rad=-0.15'))
ax.add_patch(plt.Circle((0, 0), 0.75, facecolor='#FFF8DC', edgecolor='black', linewidth=2))
ax.text(0, 0.12, 'B_C', ha='center', va='center', fontsize=14, fontweight='bold')
ax.text(0, -0.18, '{5,16,10,11}\nΣ42', ha='center', va='center', fontsize=11, color='red', fontweight='bold')
ax.text(0, -3.25, 'cyclic permutation: (NW N NE E SE S SW W)', ha='center', va='center', fontsize=14, fontweight='bold')
ax.set_xlim(-3.6, 3.6); ax.set_ylim(-3.6, 3.6); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('Right rotation = clockwise cyclic action on the 8 boundary blocks, fixing the central block', fontsize=17, fontweight='bold')
plt.tight_layout(); save_fig('origin_translated_05_cyclic_action.png'); plt.close()

# --- origin_translated_06: Mutual transformation 1890 as weighted incidence product ---
fig, axes = plt.subplots(1, 2, figsize=(18, 9))
ax = axes[0]
incidence = np.ones((5, 9))
im = ax.imshow(incidence, cmap='Blues', vmin=0, vmax=1)
ax.set_xticks(range(9)); ax.set_xticklabels([f'B_{n}' for n in palace_names_ordered], rotation=45, ha='right')
ax.set_yticks(range(5)); ax.set_yticklabels([f'{ph} class' for ph in ['Water', 'Fire', 'Wood', 'Metal', 'Earth']])
for i in range(5):
    for j in range(9):
        ax.text(j, i, '1', ha='center', va='center', fontsize=10, fontweight='bold')
ax.set_title('Incidence product: 5 classes × 9 blocks = 45', fontsize=14, fontweight='bold')

ax = axes[1]
ax.axis('off')
formula_lines = [
    ('number of residue classes', '5'),
    ('number of 4-blocks', '9'),
    ('block sum invariant', '42'),
    ('weighted total', '5 × 9 × 42 = 1,890'),
]
for i, (label, value) in enumerate(formula_lines):
    y = 0.78 - i * 0.18
    ax.text(0.12, y, label, ha='left', va='center', fontsize=15)
    ax.text(0.72, y, value, ha='center', va='center', fontsize=18 if i < 3 else 23,
            fontweight='bold', color='red' if i == 3 else 'black',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#FFF8DC' if i == 3 else '#F7FBFF', edgecolor='black'))
ax.text(0.5, 0.06,
        'Mutual transformation can be read as counting all combinations between the 5 classes and 9 blocks,\n'
        'then assigning the common weight 42 to each combination.',
        ha='center', va='center', fontsize=14, fontweight='bold')
fig.suptitle('Mutual transformation yields 1,890 = weighted incidence count', fontsize=18, fontweight='bold')
plt.tight_layout(); save_fig('origin_translated_06_weighted_incidence.png'); plt.close()

print("\n" + "=" * 60)
print("All images generated successfully!")
print(f"Output directory: {OUTPUT_DIR}/")
print("=" * 60)
