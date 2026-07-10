#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nakseo Sagudo — modern graph-theoretic analysis script
《Gusuryeok》Choi Seok-jeong text Nakseo Sagudo(Nakseo Sagudo) text text analysis
analysis text: corrected source 20text text (3×2 rectangle structure 4 hexagon faces  vertices  text)
"""

import os
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm
from matplotlib.lines import Line2D

# matplotlib text text text text/CJK text text
fm._load_fontmanager(try_read_cache=False)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ============================================
# 0. output directory text
# ============================================
OUTPUT_DIR = '.'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================
# 1. graph data structure (corrected source)
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

# outer 20-cycle (core structure finding): all text text text visits
PERIMETER_20 = [19, 2, 14, 5, 18, 3, 13, 8, 11, 15, 20, 1, 6, 10, 12, 9, 17, 4, 16, 7]

# inner 4-cycle (3×2 rectangle structure 4 faces  center vertices  formed by)
INNER_4 = [5, 16, 10, 11]

# annotation "Neighboring Stars Combinetext  Nine PalacesFour Numbers per Palace Each Obtains 42" based Nine Palaces construction
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

# five phases (mod 5) color classification
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

# ============================================
# 2. text text analysis
# ============================================

print("=" * 60)
print("Nakseo Sagudo graph-theoretic analysis results")
print("=" * 60)
print(f"node count: {G.number_of_nodes()}")
print(f"edge count: {G.number_of_edges()}")
print(f"connected components: {nx.number_connected_components(G)}")

deg_seq = sorted([d for _, d in G.degree()], reverse=True)
print(f"degree text: {deg_seq}")
print(f"degree 4 vertices: {[n for n, d in G.degree() if d == 4]} (4)")
print(f"degree 2 vertices: {len([n for n, d in G.degree() if d == 2])}")

try:
    girth = min(len(c) for c in nx.cycle_basis(G))
    print(f"Girth (minimum cycle length): {girth}")
except Exception:
    girth = None

print("\n3×2 rectangle structure 4 face(hexagon):")
for name, cycle in HEXAGONS.items():
    print(f"  {name}: {'-'.join(map(str, cycle))} (sum={sum(cycle)})")

print(f"\nouter 20-Cycle sum: {sum(PERIMETER_20)}")
print(f"inner 4-Cycle sum: {sum(INNER_4)}")

print("\nby five phase sum (arithmetic progression):")
for wx in ['Water', 'Fire', 'Wood', 'Metal', 'Earth']:
    wx_nodes = [n for n in G.nodes() if wuxing[n] == wx]
    print(f"  {wx}: {sum(wx_nodes)} ({wx_nodes})")

print("\nNine Palaces each palace sum (annotation based):")
for name, palace in NINE_PALACES.items():
    print(f"  {name}: {palace} (sum={sum(palace)})")

betw = nx.betweenness_centrality(G)
print(f"\nBetweenness Centrality (Top 5):")
for n, v in sorted(betw.items(), key=lambda x: -x[1])[:5]:
    print(f"  {n}({wuxing[n]}): {v:.3f}")

# ============================================
# 3. visualization text 7text generated
# ============================================

def save_fig(name):
    plt.savefig(f'{OUTPUT_DIR}/{name}', dpi=200, bbox_inches='tight')
    print(f"[Saved] {name}")

hex_edges = {}
for name, cycle in HEXAGONS.items():
    hex_edges[name] = [(cycle[i], cycle[(i+1)%6]) for i in range(6)]

perimeter_edges = [(PERIMETER_20[i], PERIMETER_20[(i+1)%20]) for i in range(20)]
inner_edges = [(INNER_4[i], INNER_4[(i+1)%4]) for i in range(4)]

# --- 01: source graph ---
fig, ax = plt.subplots(1, 1, figsize=(12, 12))
hex_colors = {'NW': '#CC4444', 'NE': '#4488CC', 'SW': '#44AA44', 'SE': '#CC9944'}
for name, hedges in hex_edges.items():
    nx.draw_networkx_edges(G, POSITIONS, edgelist=hedges, edge_color=hex_colors[name], width=3, alpha=0.8, ax=ax)
node_colors = [G.nodes[n]['color'] for n in G.nodes()]
nx.draw_networkx_nodes(G, POSITIONS, node_color=node_colors, node_size=1500, edgecolors='black', linewidths=2, ax=ax)
nx.draw_networkx_labels(G, POSITIONS, font_size=14, font_weight='bold', ax=ax)
shared_nodes = [5, 16, 10, 11]
nx.draw_networkx_nodes(G, POSITIONS, nodelist=shared_nodes, node_color='white', node_size=1500, edgecolors='red', linewidths=3, ax=ax)
ax.set_title('Nakseo Sagudo - corrected source graph\n3×2 rectangle structure + outer 20-Cycle + inner 4-Cycle', fontsize=16, fontweight='bold')
ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5); ax.axis('off')
legend_elements = [mpatches.Patch(facecolor=wuxing_color[wx], edgecolor='black', label=f'{wx} ({wuxing_en[wx]})') for wx in ['Water', 'Fire', 'Wood', 'Metal', 'Earth']]
legend_elements += [Line2D([0], [0], marker='o', color='w', markeredgecolor='red', markerfacecolor='white', markersize=10, label='shared vertices(degree 4)')]
ax.legend(handles=legend_elements, loc='lower right', fontsize=10, framealpha=0.9, edgecolor='black')
save_fig('01_original_graph.png'); plt.close()

# --- 02: by five phase subgraph decomposition ---
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()
ax = axes[0]
for name, hedges in hex_edges.items():
    nx.draw_networkx_edges(G, POSITIONS, edgelist=hedges, edge_color=hex_colors[name], width=2.5, alpha=0.7, ax=ax)
nx.draw_networkx_nodes(G, POSITIONS, node_color=node_colors, node_size=1200, edgecolors='black', linewidths=1.5, ax=ax)
nx.draw_networkx_labels(G, POSITIONS, font_size=11, font_weight='bold', ax=ax)
ax.set_title('full graph', fontsize=13, fontweight='bold'); ax.axis('off')

for idx, wx in enumerate(['Water', 'Fire', 'Wood', 'Metal', 'Earth']):
    ax = axes[idx + 1]
    wx_nodes = [n for n in G.nodes() if wuxing[n] == wx]
    wx_edges = [(u, v) for u, v in G.edges() if u in wx_nodes and v in wx_nodes]
    cross_edges = [(u, v) for u, v in G.edges() if (u in wx_nodes) != (v in wx_nodes)]
    nx.draw_networkx_edges(G, POSITIONS, edge_color='#EEEEEE', width=1, alpha=0.3, ax=ax)
    if cross_edges: nx.draw_networkx_edges(G, POSITIONS, edgelist=cross_edges, edge_color=wuxing_color[wx], width=2, alpha=0.3, style=':', ax=ax)
    if wx_edges: nx.draw_networkx_edges(G, POSITIONS, edgelist=wx_edges, edge_color=wuxing_color[wx], width=3.5, alpha=0.95, ax=ax)
    other_nodes = [n for n in G.nodes() if n not in wx_nodes]
    if other_nodes: nx.draw_networkx_nodes(G, POSITIONS, nodelist=other_nodes, node_color='#F0F0F0', node_size=500, edgecolors='#CCCCCC', linewidths=1, ax=ax)
    nx.draw_networkx_nodes(G, POSITIONS, nodelist=wx_nodes, node_color=wuxing_color[wx], node_size=1800, edgecolors='black', linewidths=2.5, ax=ax)
    nx.draw_networkx_labels(G, POSITIONS, font_size=10, font_weight='bold', ax=ax)
    ax.set_title(f'{wx} ({wuxing_en[wx]})', fontsize=12, fontweight='bold', color=wuxing_color[wx]); ax.axis('off')

plt.suptitle('five-phase subgraph decomposition', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout(); save_fig('02_wuxing_decomposition.png'); plt.close()

# --- 03: adjacency matrix + spectrum ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
adj = nx.adjacency_matrix(G, nodelist=sorted(G.nodes())).todense()
im = ax.imshow(adj, cmap='YlOrRd', interpolation='nearest')
ax.set_xticks(range(20)); ax.set_yticks(range(20))
ax.set_xticklabels(sorted(G.nodes()), fontsize=9); ax.set_yticklabels(sorted(G.nodes()), fontsize=9)
wx_sorted = [wuxing[n] for n in sorted(G.nodes())]
boundaries = [i - 0.5 for i in range(1, 20) if wx_sorted[i] != wx_sorted[i-1]]
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

# --- 04: cycle analysis ---
fig, axes = plt.subplots(2, 2, figsize=(18, 16))

ax = axes[0, 0]
for name, hedges in hex_edges.items():
    nx.draw_networkx_edges(G, POSITIONS, edgelist=hedges, edge_color=hex_colors[name], width=3, alpha=0.8, ax=ax)
nx.draw_networkx_nodes(G, POSITIONS, node_color=node_colors, node_size=1500, edgecolors='black', linewidths=2, ax=ax)
nx.draw_networkx_labels(G, POSITIONS, font_size=12, font_weight='bold', ax=ax)
ax.set_title('3×2 rectangletext 4 face(6-Cycle) structure', fontsize=13, fontweight='bold')
ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5); ax.axis('off'); ax.set_aspect('equal')

ax = axes[0, 1]
nx.draw_networkx_edges(G, POSITIONS, edgelist=perimeter_edges, edge_color='#333333', width=3, alpha=0.9, ax=ax)
nx.draw_networkx_edges(G, POSITIONS, edgelist=inner_edges, edge_color='red', width=2.5, alpha=0.7, style='--', ax=ax)
nx.draw_networkx_nodes(G, POSITIONS, nodelist=INNER_4, node_color='#CC9944', node_size=1800, edgecolors='red', linewidths=2.5, ax=ax)
other_nodes = [n for n in G.nodes() if n not in INNER_4]
nx.draw_networkx_nodes(G, POSITIONS, nodelist=other_nodes, node_color='white', node_size=1000, edgecolors='black', linewidths=1.5, ax=ax)
nx.draw_networkx_labels(G, POSITIONS, font_size=11, font_weight='bold', ax=ax)
ax.set_title(f'outer 20-Cycle + inner 4-Cycle\n(20-Cycle sum={sum(PERIMETER_20)}, 4-Cycle sum={sum(INNER_4)})', fontsize=13, fontweight='bold')
ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5); ax.axis('off'); ax.set_aspect('equal')

ax = axes[1, 0]
hex_names = list(HEXAGONS.keys())
hex_sums = [sum(HEXAGONS[h]) for h in hex_names]
hex_bar_colors = [hex_colors[h] for h in hex_names]
ax.bar(hex_names, hex_sums, color=hex_bar_colors, edgecolor='black', linewidth=1.5)
ax.set_title('Node sums of the four faces', fontsize=13, fontweight='bold')
for bar, val in zip(ax.patches, hex_sums):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, str(val), ha='center', fontsize=12, fontweight='bold')

ax = axes[1, 1]
cumsum = np.cumsum([n for n in PERIMETER_20])
ax.plot(range(20), cumsum, 'o-', color='#CC4444', linewidth=2.5, markersize=8, markeredgecolor='black')
ax.fill_between(range(20), cumsum, alpha=0.2, color='#CC4444')
ax.set_xticks(range(20)); ax.set_xticklabels([str(n) for n in PERIMETER_20], fontsize=9)
ax.set_title(f'outer 20-Cycle cumulative sum (Total={sum(PERIMETER_20)})', fontsize=13, fontweight='bold')
ax.grid(True, alpha=0.3); ax.axhline(y=sum(PERIMETER_20)/2, color='blue', linestyle='--', alpha=0.5)

plt.tight_layout(); save_fig('04_cycle_analysis.png'); plt.close()

# --- 05: centrality + sum invariants ---
fig, axes = plt.subplots(2, 2, figsize=(16, 14))
ax = axes[0, 0]
betw = nx.betweenness_centrality(G)
nodes_sorted = sorted(G.nodes(), key=lambda n: betw[n], reverse=True)
colors_sorted = [G.nodes[n]['color'] for n in nodes_sorted]
ax.bar(range(20), [betw[n] for n in nodes_sorted], color=colors_sorted, edgecolor='black')
ax.set_xticks(range(20)); ax.set_xticklabels([str(n) for n in nodes_sorted], fontsize=9)
ax.set_title('Betweenness Centrality', fontsize=12, fontweight='bold'); ax.set_ylabel('Centrality', fontsize=10)

ax = axes[0, 1]
wx_sums = {wx: sum([n for n in G.nodes() if wuxing[n] == wx]) for wx in ['Water', 'Fire', 'Wood', 'Metal', 'Earth']}
wx_names = list(wx_sums.keys()); wx_vals = list(wx_sums.values()); wx_colors_bar = [wuxing_color[w] for w in wx_names]
ax.bar(wx_names, wx_vals, color=wx_colors_bar, edgecolor='black', linewidth=1.5)
ax.set_title('by five phase number sum (34, 38, 42, 46, 50)', fontsize=12, fontweight='bold')
for bar, val in zip(ax.patches, wx_vals): ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, str(val), ha='center', fontsize=12, fontweight='bold')
ax.plot(range(5), wx_vals, 'o--', color='black', alpha=0.5, linewidth=2)

ax = axes[1, 0]
components = {'NW face': sum(HEXAGONS['NW']), 'NE face': sum(HEXAGONS['NE']),
              'SW face': sum(HEXAGONS['SW']), 'SE face': sum(HEXAGONS['SE']),
              'outer 20-Cycle': sum(PERIMETER_20), 'inner 4-Cycle': sum(INNER_4), 'text': sum(range(1, 21))}
ax.bar(list(components.keys()), list(components.values()), color=['#CC4444', '#4488CC', '#44AA44', '#CC9944', '#888888', '#CC9944', '#333333'], edgecolor='black', linewidth=1.5)
ax.set_title('structural subset sums', fontsize=12, fontweight='bold'); ax.set_ylabel('Sum', fontsize=10)
plt.setp(ax.xaxis.get_majorticklabels(), rotation=15, ha='right')

ax = axes[1, 1]
neighbor_sums = {n: sum(G.neighbors(n)) for n in G.nodes()}
nodes_ns = sorted(G.nodes()); ns_vals = [neighbor_sums[n] for n in nodes_ns]; ns_colors = [G.nodes[n]['color'] for n in nodes_ns]
ax.bar(range(20), ns_vals, color=ns_colors, edgecolor='black')
ax.set_xticks(range(20)); ax.set_xticklabels([str(n) for n in nodes_ns], fontsize=9)
ax.set_title('Neighbor sum at each node', fontsize=12, fontweight='bold')
ax.axhline(y=np.mean(ns_vals), color='red', linestyle='--', alpha=0.5)
plt.tight_layout(); save_fig('05_centrality_invariants.png'); plt.close()

# --- 06: five phases generatingovercoming ---
fig, axes = plt.subplots(1, 2, figsize=(18, 8))
ax = axes[0]
wuxing_graph = nx.DiGraph()
wuxing_relations = [
    ('Water', 'Wood', 'generating'), ('Wood', 'Fire', 'generating'), ('Fire', 'Earth', 'generating'), ('Earth', 'Metal', 'generating'), ('Metal', 'Water', 'generating'),
    ('Water', 'Fire', 'overcoming'), ('Fire', 'Metal', 'overcoming'), ('Metal', 'Wood', 'overcoming'), ('Wood', 'Earth', 'overcoming'), ('Earth', 'Water', 'overcoming'),
]
for u, v, r in wuxing_relations: wuxing_graph.add_edge(u, v, relation=r)
wx_pos = {'Water': (0, 2), 'Wood': (2, 1), 'Fire': (1, -1), 'Earth': (-1, -1), 'Metal': (-2, 1)}
sheng_edges = [(u, v) for u, v, r in wuxing_relations if r == 'generating']
ke_edges = [(u, v) for u, v, r in wuxing_relations if r == 'overcoming']
nx.draw_networkx_edges(wuxing_graph, wx_pos, edgelist=sheng_edges, edge_color='#44AA44', width=3, alpha=0.8, arrows=True, arrowsize=20, connectionstyle='arc3,rad=0.15', ax=ax)
nx.draw_networkx_edges(wuxing_graph, wx_pos, edgelist=ke_edges, edge_color='#CC4444', width=2, alpha=0.6, style='--', arrows=True, arrowsize=15, connectionstyle='arc3,rad=-0.15', ax=ax)
wx_node_colors = [wuxing_color[w] for w in wuxing_graph.nodes()]
nx.draw_networkx_nodes(wuxing_graph, wx_pos, node_color=wx_node_colors, node_size=3000, edgecolors='black', linewidths=2.5, ax=ax)
nx.draw_networkx_labels(wuxing_graph, wx_pos, font_size=14, font_weight='normal', ax=ax)
legend_elements = [Line2D([0], [0], color='#44AA44', lw=3, label='generating'), Line2D([0], [0], color='#CC4444', lw=2, linestyle='--', label='overcoming')]
ax.legend(handles=legend_elements, loc='upper right', fontsize=11)
ax.set_title('five phases generatingovercoming relation diagram', fontsize=13, fontweight='bold'); ax.set_xlim(-3, 3.5); ax.set_ylim(-2.5, 3); ax.axis('off')

ax = axes[1]
wx_edge_counts = {}
for u, v in G.edges():
    wu, wv = wuxing[u], wuxing[v]
    if wu == wv: key = f'{wu}same-phase'
    elif (wu, wv) in [('Water','Wood'), ('Wood','Fire'), ('Fire','Earth'), ('Earth','Metal'), ('Metal','Water')] or (wv, wu) in [('Water','Wood'), ('Wood','Fire'), ('Fire','Earth'), ('Earth','Metal'), ('Metal','Water')]: key = 'generating'
    elif (wu, wv) in [('Water','Fire'), ('Fire','Metal'), ('Metal','Wood'), ('Wood','Earth'), ('Earth','Water')] or (wv, wu) in [('Water','Fire'), ('Fire','Metal'), ('Metal','Wood'), ('Wood','Earth'), ('Earth','Water')]: key = 'overcoming'
    else: key = 'neutral'
    wx_edge_counts[key] = wx_edge_counts.get(key, 0) + 1
colors_pie = ['#44AA44', '#CC4444', '#CC9944', '#4488CC']
ax.pie(list(wx_edge_counts.values()), labels=list(wx_edge_counts.keys()), autopct='%1.0f%%',
       colors=colors_pie[:len(wx_edge_counts)], explode=[0.05]*len(wx_edge_counts),
       textprops={'fontsize': 12, 'fontweight': 'bold'})
ax.set_title(f'five phases edge distribution (N={G.number_of_edges()})', fontsize=13, fontweight='bold')
plt.tight_layout(); save_fig('06_wuxing_relations.png'); plt.close()

# --- 07: source based text text ---
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
ax.set_title('120-node construction (20 x 6 copies)', fontsize=13, fontweight='bold'); ax.axis('off')

ax = axes[1]
quad = np.array([[0, 1], [1, 1], [1, 0], [0, 0], [0, 1]]) * 3
ax.plot(quad[:,0], quad[:,1], 'o-', color='black', linewidth=2, markersize=12, markerfacecolor='#CC9944')
for i, (x, y) in enumerate([[0,1],[1,1],[1,0],[0,0]]):
    label = ['NW\n(5,16)', 'NE\n(16,10)', 'SE\n(10,11)', 'SW\n(11,5)'][i]
    ax.text(x*3, y*3, label, ha='center', va='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', edgecolor='black'))
ax.set_xlim(-1, 4); ax.set_ylim(-1, 4); ax.set_aspect('equal')
ax.set_title('Dual structure of the 3x2 rectangle\nshared vertices 5-16-10-11', fontsize=13, fontweight='bold'); ax.axis('off')
plt.tight_layout(); save_fig('07_local_extensions.png'); plt.close()

# ============================================
# 4. source annotation based origin_ text generated
# ============================================

print("\n" + "-" * 60)
print("generating source-annotation analysis images")
print("-" * 60)

# --- origin_01: Hado 4-5 basis and five palaces ---
fig, axes = plt.subplots(1, 2, figsize=(18, 8))
ax = axes[0]
# Hado 4-5: 4text 5text layout
hutu_pos = {
    '1/6\nWater': (0, 2), '2/7\nFire': (0, -2),
    '3/8\nWood': (-2, 0), '4/9\nMetal': (2, 0),
    '5/10\nEarth': (0, 0),
}
for label, (x, y) in hutu_pos.items():
    wx = label.split('\n')[1]
    ax.add_patch(plt.Circle((x, y), 0.6, facecolor=wuxing_color[wx], edgecolor='black', linewidth=2))
    ax.text(x, y, label, ha='center', va='center', fontsize=11, fontweight='bold')
# connectiontext: generating cycle
for a, b in [('1/6\nWater','3/8\nWood'), ('3/8\nWood','2/7\nFire'), ('2/7\nFire','5/10\nEarth'), ('5/10\nEarth','4/9\nMetal'), ('4/9\nMetal','1/6\nWater')]:
    x1, y1 = hutu_pos[a]; x2, y2 = hutu_pos[b]
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='#44AA44', lw=2, connectionstyle='arc3,rad=0.15'))
ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('Hado 4-5 Basis (Four Directions + Five at Center)\n4×5=20, 4+5=9', fontsize=14, fontweight='bold')

ax = axes[1]
# five palaces = five phases text
wx_groups = {
    'Water': [1, 6, 11, 16], 'Fire': [2, 7, 12, 17], 'Wood': [3, 8, 13, 18],
    'Metal': [4, 9, 14, 19], 'Earth': [5, 10, 15, 20]
}
positions_5 = [(0, 2), (-2, 0.5), (2, 0.5), (-1, -2), (1, -2)]
for (wx, nodes), (x, y) in zip(wx_groups.items(), positions_5):
    ax.add_patch(plt.Circle((x, y), 0.7, facecolor=wuxing_color[wx], edgecolor='black', linewidth=2))
    ax.text(x, y+0.15, f'{wx}\n{" ".join(map(str, nodes))}\nsum={sum(nodes)}', ha='center', va='center', fontsize=10, fontweight='bold')
ax.set_xlim(-3, 3); ax.set_ylim(-3.5, 3.5); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('Five Palaces: four-number groups by phase\ntotal sum 210, average 42', fontsize=14, fontweight='bold')
plt.tight_layout(); save_fig('origin_01_hutu_5palaces.png'); plt.close()

# --- origin_02: Neighboring Stars Combine → Nine Palaces 42-sum grid ---
fig, ax = plt.subplots(1, 1, figsize=(12, 12))
grid_pos = {
    'NW': (-2, 2), 'N': (0, 2), 'NE': (2, 2),
    'W': (-2, 0), 'C': (0, 0), 'E': (2, 0),
    'SW': (-2, -2), 'S': (0, -2), 'SE': (2, -2),
}
for name, (x, y) in grid_pos.items():
    palace_nodes = NINE_PALACES[name]
    # palace boundary
    rect = plt.Rectangle((x-0.9, y-0.9), 1.8, 1.8, fill=True, facecolor='lightyellow', edgecolor='black', linewidth=2)
    ax.add_patch(rect)
    # 4numbers layout
    offsets = [(-0.4, 0.3), (0.4, 0.3), (-0.4, -0.3), (0.4, -0.3)]
    for node, (dx, dy) in zip(palace_nodes, offsets):
        circle = plt.Circle((x+dx, y+dy), 0.22, facecolor=wuxing_color[wuxing[node]], edgecolor='black', linewidth=1.5)
        ax.add_patch(circle)
        ax.text(x+dx, y+dy, str(node), ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(x, y+0.72, f'{name}', ha='center', va='center', fontsize=13, fontweight='bold')
    ax.text(x, y-0.72, f'sum=42', ha='center', va='center', fontsize=12, fontweight='bold', color='red')

# text text(clockwise) text
arrow_style = dict(arrowstyle='->', color='purple', lw=2.5, connectionstyle='arc3,rad=0.2')
for start, end in [('NW','N'), ('N','NE'), ('NE','E'), ('E','SE'), ('SE','S'), ('S','SW'), ('SW','W'), ('W','NW')]:
    x1, y1 = grid_pos[start]; x2, y2 = grid_pos[end]
    ax.annotate('', xy=(x2-0.5*np.sign(x2), y2-0.5*np.sign(y2)), xytext=(x1+0.5*np.sign(x1), y1+0.5*np.sign(y1)),
                arrowprops=arrow_style)
ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('Neighboring Stars Combine Five Palaces Nine Palaces\n Each Obtains 42', fontsize=16, fontweight='bold')
plt.tight_layout(); save_fig('origin_02_9palace_grid.png'); plt.close()

# --- origin_03: Right Rotation text ---
fig, ax = plt.subplots(1, 1, figsize=(12, 10))
# text: five palaces
left_pos = {'Water': (0, 2), 'Wood': (-1.5, 0.5), 'Fire': (1.5, 0.5), 'Metal': (-0.8, -1.5), 'Earth': (0.8, -1.5)}
for wx, (x, y) in left_pos.items():
    ax.add_patch(plt.Circle((x-5, y), 0.6, facecolor=wuxing_color[wx], edgecolor='black', linewidth=2))
    ax.text(x-5, y, wx, ha='center', va='center', fontsize=14, fontweight='bold')
# text: Nine Palaces (3x3)
for name, (x, y) in grid_pos.items():
    ax.add_patch(plt.Rectangle((x+2.1, y-0.4), 0.8, 0.8, fill=True, facecolor='lightyellow', edgecolor='black', linewidth=1.5))
    ax.text(x+2.5, y, '42', ha='center', va='center', fontsize=11, fontweight='bold')
# text + text text
ax.annotate('', xy=(1, 0), xytext=(-3, 0), arrowprops=dict(arrowstyle='->', color='black', lw=3))
ax.text(-1, 0.6, 'Right Rotation (clockwise)', ha='center', va='center', fontsize=14, fontweight='bold')
ax.text(-1, -0.6, 'five palaces → 9palace', ha='center', va='center', fontsize=13, fontweight='bold')
ax.set_xlim(-7, 5.5); ax.set_ylim(-3.5, 3.5); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('Hadotext Right Rotationtext\nFive Palacestext text Nine Palacestext text', fontsize=16, fontweight='bold')
plt.tight_layout(); save_fig('origin_03_right_rotation.png'); plt.close()

# --- origin_04: Mutual Transformation 1890 ---
fig, ax = plt.subplots(1, 1, figsize=(14, 10))
# five palaces (text text)
wx_list = ['Water', 'Fire', 'Wood', 'Metal', 'Earth']
for i, wx in enumerate(wx_list):
    y = 2 - i * 1.0
    ax.add_patch(plt.Circle((-3, y), 0.35, facecolor=wuxing_color[wx], edgecolor='black', linewidth=2))
    ax.text(-3, y, wx, ha='center', va='center', fontsize=12, fontweight='bold')
# 9palace (text text)
palace_names = list(grid_pos.keys())
for j, name in enumerate(palace_names):
    x = -2 + j * 0.9
    ax.add_patch(plt.Rectangle((x-0.3, 3.2), 0.6, 0.6, fill=True, facecolor='lightyellow', edgecolor='black', linewidth=1.5))
    ax.text(x, 3.5, name, ha='center', va='center', fontsize=9, fontweight='bold')
# connectiontext: 5 × 9 = 45
for i in range(5):
    for j in range(9):
        x = -2 + j * 0.9
        y = 2 - i * 1.0
        ax.plot([-3+0.3, x], [y, 3.2], '-', color='gray', alpha=0.15, linewidth=0.5)
# text
ax.text(0, -3, 'Mutual Transformation: five palaces × 9palace = 45', ha='center', va='center', fontsize=18, fontweight='bold')
ax.text(0, -3.7, '45 × 42 = 1,890', ha='center', va='center', fontsize=22, fontweight='bold', color='red')
ax.set_xlim(-4, 6.5); ax.set_ylim(-4.5, 4.5); ax.axis('off')
ax.set_title('Mutual Transformationtext', fontsize=18, fontweight='bold')
plt.tight_layout(); save_fig('origin_04_mutual_transformation_1890.png'); plt.close()

# --- origin_05: 42 invariants analysis ---
fig, axes = plt.subplots(2, 2, figsize=(16, 14))

# 3×2 rectangletext 4 face outer 4vertices + inner 4-cycle
ax = axes[0, 0]
labels_42 = ['NW\nouter', 'NE\nouter', 'SW\nouter', 'SE\nouter', 'inner\n4-Cycle']
values_42 = [sum(NINE_PALACES[k]) for k in ['NW', 'NE', 'SW', 'SE', 'C']]
colors_42 = ['#CC4444', '#4488CC', '#44AA44', '#CC9944', '#888888']
ax.bar(labels_42, values_42, color=colors_42, edgecolor='black', linewidth=1.5)
ax.axhline(y=42, color='red', linestyle='--', linewidth=2)
ax.set_title('42-sum five palaces structure', fontsize=13, fontweight='bold')
for bar, val in zip(ax.patches, values_42):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, str(val), ha='center', fontsize=12, fontweight='bold')

# Nine Palaces grid colorstext
ax = axes[0, 1]
for name, (x, y) in grid_pos.items():
    palace_nodes = NINE_PALACES[name]
    rect = plt.Rectangle((x-0.9, y-0.9), 1.8, 1.8, fill=True, facecolor='#FFF8DC', edgecolor='black', linewidth=2)
    ax.add_patch(rect)
    ax.text(x, y+0.6, name, ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(x, y-0.6, 'Σ=42', ha='center', va='center', fontsize=11, fontweight='bold', color='red')
    # text colors text text
    for k, node in enumerate(palace_nodes):
        angle = 2 * np.pi * k / 4
        px, py = x + 0.45 * np.cos(angle), y + 0.45 * np.sin(angle)
        ax.add_patch(plt.Circle((px, py), 0.15, facecolor=wuxing_color[wuxing[node]], edgecolor='black', linewidth=1))
        ax.text(px, py, str(node), ha='center', va='center', fontsize=9, fontweight='bold')
ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('Nine Palaces 42-invariants distribution', fontsize=13, fontweight='bold')

# five palaces → 9palace → 1890 text
ax = axes[1, 0]
ax.text(0.5, 0.8, 'Five Palaces (5 palaces)', ha='center', va='center', fontsize=14, fontweight='bold')
ax.text(0.5, 0.65, 'avg sum = 42', ha='center', va='center', fontsize=12)
ax.annotate('', xy=(0.5, 0.45), xytext=(0.5, 0.55), arrowprops=dict(arrowstyle='->', color='black', lw=2))
ax.text(0.5, 0.35, 'Right Rotation → Nine Palaces (9 palaces)', ha='center', va='center', fontsize=14, fontweight='bold')
ax.text(0.5, 0.2, 'each sum = 42', ha='center', va='center', fontsize=12)
ax.annotate('', xy=(0.5, 0.0), xytext=(0.5, 0.1), arrowprops=dict(arrowstyle='->', color='black', lw=2))
ax.text(0.5, -0.15, 'Mutual Transformation: 5 × 9 = 45 interactions', ha='center', va='center', fontsize=14, fontweight='bold')
ax.text(0.5, -0.35, '45 × 42 = 1,890', ha='center', va='center', fontsize=20, fontweight='bold', color='red')
ax.set_xlim(0, 1); ax.set_ylim(-0.6, 1); ax.axis('off')
ax.set_title('annotationtext mathematical flow', fontsize=13, fontweight='bold')

# each palace five phases distribution
ax = axes[1, 1]
palace_names_ordered = ['NW', 'N', 'NE', 'W', 'C', 'E', 'SW', 'S', 'SE']
wx_counts_per_palace = {name: {} for name in palace_names_ordered}
for name in palace_names_ordered:
    for node in NINE_PALACES[name]:
        wx = wuxing[node]
        wx_counts_per_palace[name][wx] = wx_counts_per_palace[name].get(wx, 0) + 1

bottom = np.zeros(9)
for wx in ['Water', 'Fire', 'Wood', 'Metal', 'Earth']:
    counts = [wx_counts_per_palace[name].get(wx, 0) for name in palace_names_ordered]
    ax.bar(palace_names_ordered, counts, bottom=bottom, label=wx, color=wuxing_color[wx], edgecolor='black', linewidth=1)
    bottom += counts
ax.set_title('Nine Palaces each palace five phases distribution', fontsize=13, fontweight='bold')
ax.legend(loc='upper right')
ax.set_ylabel('Count')

plt.tight_layout(); save_fig('origin_05_42_invariants.png'); plt.close()

# --- origin_06: corrected text on Nine Palaces text ---
fig, ax = plt.subplots(1, 1, figsize=(14, 14))
for name, hedges in hex_edges.items():
    nx.draw_networkx_edges(G, POSITIONS, edgelist=hedges, edge_color=hex_colors[name], width=2.5, alpha=0.6, ax=ax)
nx.draw_networkx_nodes(G, POSITIONS, node_color=node_colors, node_size=1200, edgecolors='black', linewidths=1.5, ax=ax)
nx.draw_networkx_labels(G, POSITIONS, font_size=11, font_weight='bold', ax=ax)
# Nine Palaces text text
palace_regions = {
    'NW': (-2.3, 2.3), 'N': (0, 2.3), 'NE': (2.3, 2.3),
    'W': (-2.3, 0), 'C': (0, 0), 'E': (2.3, 0),
    'SW': (-2.3, -2.3), 'S': (0, -2.3), 'SE': (2.3, -2.3),
}
for name, (x, y) in palace_regions.items():
    ax.text(x, y, f'{name}\nΣ42', ha='center', va='center', fontsize=13, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='red', alpha=0.85))
ax.set_title('source graph text Nine Palaces interpretation\nNeighboring Stars Combinetext text text text', fontsize=16, fontweight='bold')
ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5); ax.axis('off')
plt.tight_layout(); save_fig('origin_06_graph_with_9palace.png'); plt.close()

# ============================================
# 5. source annotationtext text textsumtext translation text generated
# ============================================

print("\n" + "-" * 60)
print("source annotationtext text textsumtext translation text generated")
print("-" * 60)

modern_terms = [
    ('Neighboring Stars Combine', 'adjacent blocks overlap / neighboring 4-subsets are combined'),
    ('Five Palaces Nine Palaces', '5 residue classes are reorganized into 9 blocks'),
    ('text', 'each block has cardinality 4'),
    ('Each Obtains 42', 'each block has invariant sum 42'),
    ('Right Rotation', 'clockwise cyclic action on the boundary blocks'),
    ('Mutual Transformationtext', '5 × 9 incidence product, weighted by 42 = 1,890'),
]

# --- origin_translated_01: text text text textsumtext as propositions translation ---
fig, ax = plt.subplots(1, 1, figsize=(16, 10))
ax.axis('off')
ax.set_title('source annotation → text textsumtext terms', fontsize=20, fontweight='bold', pad=20)
for i, (classical, modern) in enumerate(modern_terms):
    y = 0.88 - i * 0.14
    ax.text(0.05, y, classical, ha='left', va='center', fontsize=18, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF8DC', edgecolor='black'))
    ax.annotate('', xy=(0.42, y), xytext=(0.32, y),
                arrowprops=dict(arrowstyle='->', lw=2.5, color='black'))
    ax.text(0.45, y, modern, ha='left', va='center', fontsize=15,
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#EAF3FF', edgecolor='#336699'))
ax.text(0.5, 0.03,
        'core translation: text not a mystical metaphor but, 20numberstext text 4-subsets (blocks)text rearranges\n'
        'all blocktext sumtext 42text fixing balanced block structure describes.',
        ha='center', va='center', fontsize=15, fontweight='bold', color='#333333')
plt.tight_layout(); save_fig('origin_translated_01_terms.png'); plt.close()

# --- origin_translated_02: 5 residue classtext 9 blocktext ---
fig, axes = plt.subplots(1, 2, figsize=(18, 9))
ax = axes[0]
for i, wx in enumerate(['Water', 'Fire', 'Wood', 'Metal', 'Earth']):
    nodes = [n for n in sorted(G.nodes()) if wuxing[n] == wx]
    y = 4 - i
    ax.add_patch(plt.Rectangle((-0.7, y-0.35), 4.1, 0.7, facecolor=wuxing_color[wx], edgecolor='black', alpha=0.85))
    ax.text(-1.0, y, f'{wx}', ha='right', va='center', fontsize=14, fontweight='bold')
    ax.text(1.35, y, f'{{{", ".join(map(str, nodes))}}}', ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(3.75, y, f'Σ={sum(nodes)}', ha='left', va='center', fontsize=12)
ax.set_xlim(-1.5, 5.2); ax.set_ylim(-0.8, 4.8); ax.axis('off')
ax.set_title('input: 5 residue class\nmod 5text text five phases text', fontsize=15, fontweight='bold')

ax = axes[1]
for name, (x, y) in grid_pos.items():
    nodes = NINE_PALACES[name]
    ax.add_patch(plt.Rectangle((x-0.88, y-0.75), 1.76, 1.5, facecolor='#F7FBFF', edgecolor='black', linewidth=2))
    ax.text(x, y+0.48, f'B_{name}', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(x, y+0.05, '{' + ', '.join(map(str, nodes)) + '}', ha='center', va='center', fontsize=10)
    ax.text(x, y-0.48, '|B|=4, Σ=42', ha='center', va='center', fontsize=10, color='red', fontweight='bold')
ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('output: 9 4-block\nall blocktext sumtext 42', fontsize=15, fontweight='bold')
fig.suptitle('Five Palaces Nine Palaces = 5classes into 9 balanced blocktext textconstruction', fontsize=18, fontweight='bold')
plt.tight_layout(); save_fig('origin_translated_02_blocks.png'); plt.close()

# --- origin_translated_03: Neighboring Stars Combinetext block overlaptext interpretation ---
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
ax.set_title('Neighboring Stars Combine = adjacent blocktext overlap(overlap)text using 9palace construction', fontsize=17, fontweight='bold')
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
ax.set_title(' Each Obtains 42 = 9text 4-blocktext same sum invariants 42text has', fontsize=17, fontweight='bold')
plt.tight_layout(); save_fig('origin_translated_04_invariant_table.png'); plt.close()

# --- origin_translated_05: Right Rotation as cyclic permutation ---
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
ax.set_title('Right Rotation = center blocktext fixedtext boundary 8-blocktext clockwise text action', fontsize=17, fontweight='bold')
plt.tight_layout(); save_fig('origin_translated_05_cyclic_action.png'); plt.close()

# --- origin_translated_06: Mutual Transformation 1890 as weighted incidence product ---
fig, axes = plt.subplots(1, 2, figsize=(18, 9))
ax = axes[0]
incidence = np.ones((5, 9))
im = ax.imshow(incidence, cmap='Blues', vmin=0, vmax=1)
ax.set_xticks(range(9)); ax.set_xticklabels([f'B_{n}' for n in palace_names_ordered], rotation=45, ha='right')
ax.set_yticks(range(5)); ax.set_yticklabels([f'{wx} class' for wx in ['Water', 'Fire', 'Wood', 'Metal', 'Earth']])
for i in range(5):
    for j in range(9):
        ax.text(j, i, '1', ha='center', va='center', fontsize=10, fontweight='bold')
ax.set_title('incidence product: 5 classes × 9 blocks = 45', fontsize=14, fontweight='bold')

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
        'Mutual Transformationtext 5text 9-block text counts all combinations,\n'
        'each textsumtext common weight 42text assigned can be read as a total.',
        ha='center', va='center', fontsize=14, fontweight='bold')
fig.suptitle('Mutual Transformationtext = weighted incidence count', fontsize=18, fontweight='bold')
plt.tight_layout(); save_fig('origin_translated_06_weighted_incidence.png'); plt.close()

print("\n" + "=" * 60)
print("All images generated!")
print(f"output directory: {OUTPUT_DIR}/")
print("=" * 60)
