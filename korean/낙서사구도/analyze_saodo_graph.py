#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
洛書四九圖 (낙서사구도) — 현대 그래프 이론적 분석 스크립트
《구수력(九數略)》최석정 원저작의 낙서사구도(洛書四九圖) 그래프 표기법 분석
분석 대상: 교정된 원본 20노드 그래프 (3×2 사각형 구조의 4개 육각형 면이 정점을 공유)
"""

import os
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm
from matplotlib.lines import Line2D

# matplotlib 캐시 갱신 및 한국어/CJK 폰트 설정
fm._load_fontmanager(try_read_cache=False)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ============================================
# 0. 출력 디렉토리 설정
# ============================================
OUTPUT_DIR = '.'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================
# 1. 그래프 데이터 구조화 (교정된 원본)
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

# 외곽 20-cycle (핵심 구조적 발견): 모든 노드를 한 번씩 방문
PERIMETER_20 = [19, 2, 14, 5, 18, 3, 13, 8, 11, 15, 20, 1, 6, 10, 12, 9, 17, 4, 16, 7]

# 내장 4-cycle (3×2 사각형 구조의 4개 면의 중심 정점들이 형성)
INNER_4 = [5, 16, 10, 11]

# 주석 "鄰星相兼五宫化 爲九宫每宫四子 各得四十二數" 기반 九宫 구성
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

# 오행 (mod 5) 색상 분류
wuxing = {
    1: '수', 6: '수', 11: '수', 16: '수',
    2: '화', 7: '화', 12: '화', 17: '화',
    3: '목', 8: '목', 13: '목', 18: '목',
    4: '금', 9: '금', 14: '금', 19: '금',
    5: '토', 10: '토', 15: '토', 20: '토',
}

wuxing_color = {
    '수': '#4488CC', '화': '#CC4444', '목': '#44AA44',
    '금': '#888888', '토': '#CC9944',
}

wuxing_en = {
    '수': 'Water', '화': 'Fire', '목': 'Wood', '금': 'Metal', '토': 'Earth'
}

for node in G.nodes():
    G.nodes[node]['wuxing'] = wuxing[node]
    G.nodes[node]['color'] = wuxing_color[wuxing[node]]
    G.nodes[node]['remainder'] = node % 5 if node % 5 != 0 else 5

# ============================================
# 2. 그래프 이론 분석
# ============================================

print("=" * 60)
print("洛書四九圖 그래프 이론 분석 결과")
print("=" * 60)
print(f"노드 수: {G.number_of_nodes()}")
print(f"엣지 수: {G.number_of_edges()}")
print(f"연결 성분: {nx.number_connected_components(G)}")

deg_seq = sorted([d for _, d in G.degree()], reverse=True)
print(f"차수 시퀀스: {deg_seq}")
print(f"차수 4 정점: {[n for n, d in G.degree() if d == 4]} (4개)")
print(f"차수 2 정점: {len([n for n, d in G.degree() if d == 2])}개")

try:
    girth = min(len(c) for c in nx.cycle_basis(G))
    print(f"Girth (최소 사이클 길이): {girth}")
except Exception:
    girth = None

print("\n3×2 사각형 구조의 4개 면(육각형):")
for name, cycle in HEXAGONS.items():
    print(f"  {name}: {'-'.join(map(str, cycle))} (합={sum(cycle)})")

print(f"\n외곽 20-Cycle 합: {sum(PERIMETER_20)}")
print(f"내장 4-Cycle 합: {sum(INNER_4)}")

print("\n오행별 합 (등차수열):")
for wx in ['수', '화', '목', '금', '토']:
    wx_nodes = [n for n in G.nodes() if wuxing[n] == wx]
    print(f"  {wx}: {sum(wx_nodes)} ({wx_nodes})")

print("\n九宫 각 궁 합 (주석 기반):")
for name, palace in NINE_PALACES.items():
    print(f"  {name}: {palace} (합={sum(palace)})")

betw = nx.betweenness_centrality(G)
print(f"\nBetweenness Centrality (Top 5):")
for n, v in sorted(betw.items(), key=lambda x: -x[1])[:5]:
    print(f"  {n}({wuxing[n]}): {v:.3f}")

# ============================================
# 3. 시각화 이미지 7장 생성
# ============================================

def save_fig(name):
    plt.savefig(f'{OUTPUT_DIR}/{name}', dpi=200, bbox_inches='tight')
    print(f"[저장] {name}")

hex_edges = {}
for name, cycle in HEXAGONS.items():
    hex_edges[name] = [(cycle[i], cycle[(i+1)%6]) for i in range(6)]

perimeter_edges = [(PERIMETER_20[i], PERIMETER_20[(i+1)%20]) for i in range(20)]
inner_edges = [(INNER_4[i], INNER_4[(i+1)%4]) for i in range(4)]

# --- 01: 원본 그래프 ---
fig, ax = plt.subplots(1, 1, figsize=(12, 12))
hex_colors = {'NW': '#CC4444', 'NE': '#4488CC', 'SW': '#44AA44', 'SE': '#CC9944'}
for name, hedges in hex_edges.items():
    nx.draw_networkx_edges(G, POSITIONS, edgelist=hedges, edge_color=hex_colors[name], width=3, alpha=0.8, ax=ax)
node_colors = [G.nodes[n]['color'] for n in G.nodes()]
nx.draw_networkx_nodes(G, POSITIONS, node_color=node_colors, node_size=1500, edgecolors='black', linewidths=2, ax=ax)
nx.draw_networkx_labels(G, POSITIONS, font_size=14, font_weight='bold', ax=ax)
shared_nodes = [5, 16, 10, 11]
nx.draw_networkx_nodes(G, POSITIONS, nodelist=shared_nodes, node_color='white', node_size=1500, edgecolors='red', linewidths=3, ax=ax)
ax.set_title('낙서사구도 (洛書四九圖) - 교정된 원본 그래프\n3×2 사각형 구조 + 외곽 20-Cycle + 내장 4-Cycle', fontsize=16, fontweight='bold')
ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5); ax.axis('off')
legend_elements = [mpatches.Patch(facecolor=wuxing_color[wx], edgecolor='black', label=f'{wx} ({wuxing_en[wx]})') for wx in ['수', '화', '목', '금', '토']]
legend_elements += [Line2D([0], [0], marker='o', color='w', markeredgecolor='red', markerfacecolor='white', markersize=10, label='공유 정점(차수 4)')]
ax.legend(handles=legend_elements, loc='lower right', fontsize=10, framealpha=0.9, edgecolor='black')
save_fig('01_original_graph.png'); plt.close()

# --- 02: 오행별 서브그래프 분해 ---
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()
ax = axes[0]
for name, hedges in hex_edges.items():
    nx.draw_networkx_edges(G, POSITIONS, edgelist=hedges, edge_color=hex_colors[name], width=2.5, alpha=0.7, ax=ax)
nx.draw_networkx_nodes(G, POSITIONS, node_color=node_colors, node_size=1200, edgecolors='black', linewidths=1.5, ax=ax)
nx.draw_networkx_labels(G, POSITIONS, font_size=11, font_weight='bold', ax=ax)
ax.set_title('전체 그래프', fontsize=13, fontweight='bold'); ax.axis('off')

for idx, wx in enumerate(['수', '화', '목', '금', '토']):
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

plt.suptitle('오행(五行)별 서브그래프 분해', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout(); save_fig('02_wuxing_decomposition.png'); plt.close()

# --- 03: 인접 행렬 + 스펙트럼 ---
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

# --- 04: 사이클 분석 ---
fig, axes = plt.subplots(2, 2, figsize=(18, 16))

ax = axes[0, 0]
for name, hedges in hex_edges.items():
    nx.draw_networkx_edges(G, POSITIONS, edgelist=hedges, edge_color=hex_colors[name], width=3, alpha=0.8, ax=ax)
nx.draw_networkx_nodes(G, POSITIONS, node_color=node_colors, node_size=1500, edgecolors='black', linewidths=2, ax=ax)
nx.draw_networkx_labels(G, POSITIONS, font_size=12, font_weight='bold', ax=ax)
ax.set_title('3×2 사각형의 4개 면(6-Cycle) 구조', fontsize=13, fontweight='bold')
ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5); ax.axis('off'); ax.set_aspect('equal')

ax = axes[0, 1]
nx.draw_networkx_edges(G, POSITIONS, edgelist=perimeter_edges, edge_color='#333333', width=3, alpha=0.9, ax=ax)
nx.draw_networkx_edges(G, POSITIONS, edgelist=inner_edges, edge_color='red', width=2.5, alpha=0.7, style='--', ax=ax)
nx.draw_networkx_nodes(G, POSITIONS, nodelist=INNER_4, node_color='#CC9944', node_size=1800, edgecolors='red', linewidths=2.5, ax=ax)
other_nodes = [n for n in G.nodes() if n not in INNER_4]
nx.draw_networkx_nodes(G, POSITIONS, nodelist=other_nodes, node_color='white', node_size=1000, edgecolors='black', linewidths=1.5, ax=ax)
nx.draw_networkx_labels(G, POSITIONS, font_size=11, font_weight='bold', ax=ax)
ax.set_title(f'외곽 20-Cycle + 내장 4-Cycle\n(20-Cycle 합={sum(PERIMETER_20)}, 4-Cycle 합={sum(INNER_4)})', fontsize=13, fontweight='bold')
ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5); ax.axis('off'); ax.set_aspect('equal')

ax = axes[1, 0]
hex_names = list(HEXAGONS.keys())
hex_sums = [sum(HEXAGONS[h]) for h in hex_names]
hex_bar_colors = [hex_colors[h] for h in hex_names]
ax.bar(hex_names, hex_sums, color=hex_bar_colors, edgecolor='black', linewidth=1.5)
ax.set_title('3×2 사각형 각 면의 노드 합', fontsize=13, fontweight='bold')
for bar, val in zip(ax.patches, hex_sums):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, str(val), ha='center', fontsize=12, fontweight='bold')

ax = axes[1, 1]
cumsum = np.cumsum([n for n in PERIMETER_20])
ax.plot(range(20), cumsum, 'o-', color='#CC4444', linewidth=2.5, markersize=8, markeredgecolor='black')
ax.fill_between(range(20), cumsum, alpha=0.2, color='#CC4444')
ax.set_xticks(range(20)); ax.set_xticklabels([str(n) for n in PERIMETER_20], fontsize=9)
ax.set_title(f'외곽 20-Cycle 누적 합 (Total={sum(PERIMETER_20)})', fontsize=13, fontweight='bold')
ax.grid(True, alpha=0.3); ax.axhline(y=sum(PERIMETER_20)/2, color='blue', linestyle='--', alpha=0.5)

plt.tight_layout(); save_fig('04_cycle_analysis.png'); plt.close()

# --- 05: 중심성 + 합 불변량 ---
fig, axes = plt.subplots(2, 2, figsize=(16, 14))
ax = axes[0, 0]
betw = nx.betweenness_centrality(G)
nodes_sorted = sorted(G.nodes(), key=lambda n: betw[n], reverse=True)
colors_sorted = [G.nodes[n]['color'] for n in nodes_sorted]
ax.bar(range(20), [betw[n] for n in nodes_sorted], color=colors_sorted, edgecolor='black')
ax.set_xticks(range(20)); ax.set_xticklabels([str(n) for n in nodes_sorted], fontsize=9)
ax.set_title('Betweenness Centrality', fontsize=12, fontweight='bold'); ax.set_ylabel('Centrality', fontsize=10)

ax = axes[0, 1]
wx_sums = {wx: sum([n for n in G.nodes() if wuxing[n] == wx]) for wx in ['수', '화', '목', '금', '토']}
wx_names = list(wx_sums.keys()); wx_vals = list(wx_sums.values()); wx_colors_bar = [wuxing_color[w] for w in wx_names]
ax.bar(wx_names, wx_vals, color=wx_colors_bar, edgecolor='black', linewidth=1.5)
ax.set_title('오행별 수 합 (34, 38, 42, 46, 50)', fontsize=12, fontweight='bold')
for bar, val in zip(ax.patches, wx_vals): ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, str(val), ha='center', fontsize=12, fontweight='bold')
ax.plot(range(5), wx_vals, 'o--', color='black', alpha=0.5, linewidth=2)

ax = axes[1, 0]
components = {'NW 면': sum(HEXAGONS['NW']), 'NE 면': sum(HEXAGONS['NE']),
              'SW 면': sum(HEXAGONS['SW']), 'SE 면': sum(HEXAGONS['SE']),
              '외곽 20-Cycle': sum(PERIMETER_20), '내장 4-Cycle': sum(INNER_4), '전체': sum(range(1, 21))}
ax.bar(list(components.keys()), list(components.values()), color=['#CC4444', '#4488CC', '#44AA44', '#CC9944', '#888888', '#CC9944', '#333333'], edgecolor='black', linewidth=1.5)
ax.set_title('구조적 부분집합 합', fontsize=12, fontweight='bold'); ax.set_ylabel('Sum', fontsize=10)
plt.setp(ax.xaxis.get_majorticklabels(), rotation=15, ha='right')

ax = axes[1, 1]
neighbor_sums = {n: sum(G.neighbors(n)) for n in G.nodes()}
nodes_ns = sorted(G.nodes()); ns_vals = [neighbor_sums[n] for n in nodes_ns]; ns_colors = [G.nodes[n]['color'] for n in nodes_ns]
ax.bar(range(20), ns_vals, color=ns_colors, edgecolor='black')
ax.set_xticks(range(20)); ax.set_xticklabels([str(n) for n in nodes_ns], fontsize=9)
ax.set_title('각 노드의 이웃 합', fontsize=12, fontweight='bold')
ax.axhline(y=np.mean(ns_vals), color='red', linestyle='--', alpha=0.5)
plt.tight_layout(); save_fig('05_centrality_invariants.png'); plt.close()

# --- 06: 오행 상생상극 ---
fig, axes = plt.subplots(1, 2, figsize=(18, 8))
ax = axes[0]
wuxing_graph = nx.DiGraph()
wuxing_relations = [
    ('수', '목', '생'), ('목', '화', '생'), ('화', '토', '생'), ('토', '금', '생'), ('금', '수', '생'),
    ('수', '화', '극'), ('화', '금', '극'), ('금', '목', '극'), ('목', '토', '극'), ('토', '수', '극'),
]
for u, v, r in wuxing_relations: wuxing_graph.add_edge(u, v, relation=r)
wx_pos = {'수': (0, 2), '목': (2, 1), '화': (1, -1), '토': (-1, -1), '금': (-2, 1)}
sheng_edges = [(u, v) for u, v, r in wuxing_relations if r == '생']
ke_edges = [(u, v) for u, v, r in wuxing_relations if r == '극']
nx.draw_networkx_edges(wuxing_graph, wx_pos, edgelist=sheng_edges, edge_color='#44AA44', width=3, alpha=0.8, arrows=True, arrowsize=20, connectionstyle='arc3,rad=0.15', ax=ax)
nx.draw_networkx_edges(wuxing_graph, wx_pos, edgelist=ke_edges, edge_color='#CC4444', width=2, alpha=0.6, style='--', arrows=True, arrowsize=15, connectionstyle='arc3,rad=-0.15', ax=ax)
wx_node_colors = [wuxing_color[w] for w in wuxing_graph.nodes()]
nx.draw_networkx_nodes(wuxing_graph, wx_pos, node_color=wx_node_colors, node_size=3000, edgecolors='black', linewidths=2.5, ax=ax)
nx.draw_networkx_labels(wuxing_graph, wx_pos, font_size=14, font_weight='normal', ax=ax)
legend_elements = [Line2D([0], [0], color='#44AA44', lw=3, label='상생'), Line2D([0], [0], color='#CC4444', lw=2, linestyle='--', label='상극')]
ax.legend(handles=legend_elements, loc='upper right', fontsize=11)
ax.set_title('오행 상생상극 관계도', fontsize=13, fontweight='bold'); ax.set_xlim(-3, 3.5); ax.set_ylim(-2.5, 3); ax.axis('off')

ax = axes[1]
wx_edge_counts = {}
for u, v in G.edges():
    wu, wv = wuxing[u], wuxing[v]
    if wu == wv: key = f'{wu}동질'
    elif (wu, wv) in [('수','목'), ('목','화'), ('화','토'), ('토','금'), ('금','수')] or (wv, wu) in [('수','목'), ('목','화'), ('화','토'), ('토','금'), ('금','수')]: key = '상생'
    elif (wu, wv) in [('수','화'), ('화','금'), ('금','목'), ('목','토'), ('토','수')] or (wv, wu) in [('수','화'), ('화','금'), ('금','목'), ('목','토'), ('토','수')]: key = '상극'
    else: key = '중성'
    wx_edge_counts[key] = wx_edge_counts.get(key, 0) + 1
colors_pie = ['#44AA44', '#CC4444', '#CC9944', '#4488CC']
ax.pie(list(wx_edge_counts.values()), labels=list(wx_edge_counts.keys()), autopct='%1.0f%%',
       colors=colors_pie[:len(wx_edge_counts)], explode=[0.05]*len(wx_edge_counts),
       textprops={'fontsize': 12, 'fontweight': 'bold'})
ax.set_title(f'오행 엣지 분포 (N={G.number_of_edges()})', fontsize=13, fontweight='bold')
plt.tight_layout(); save_fig('06_wuxing_relations.png'); plt.close()

# --- 07: 원본 기반 확장 설계 ---
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
ax.set_title('120子作 구조 (20×6 복제)', fontsize=13, fontweight='bold'); ax.axis('off')

ax = axes[1]
quad = np.array([[0, 1], [1, 1], [1, 0], [0, 0], [0, 1]]) * 3
ax.plot(quad[:,0], quad[:,1], 'o-', color='black', linewidth=2, markersize=12, markerfacecolor='#CC9944')
for i, (x, y) in enumerate([[0,1],[1,1],[1,0],[0,0]]):
    label = ['NW\n(5,16)', 'NE\n(16,10)', 'SE\n(10,11)', 'SW\n(11,5)'][i]
    ax.text(x*3, y*3, label, ha='center', va='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', edgecolor='black'))
ax.set_xlim(-1, 4); ax.set_ylim(-1, 4); ax.set_aspect('equal')
ax.set_title('3×2 사각형 구조의 쌍대(Dual) 구조\n공유 정점 5-16-10-11', fontsize=13, fontweight='bold'); ax.axis('off')
plt.tight_layout(); save_fig('07_local_extensions.png'); plt.close()

# ============================================
# 4. 원문 주석 기반 origin_ 이미지 생성
# ============================================

print("\n" + "-" * 60)
print("원문 주석 기반 분석 이미지 생성")
print("-" * 60)

# --- origin_01: 河圖 4-5 기초와 5궁 ---
fig, axes = plt.subplots(1, 2, figsize=(18, 8))
ax = axes[0]
# 河圖 4-5: 4방 5행 배치
hutu_pos = {
    '1/6\n수': (0, 2), '2/7\n화': (0, -2),
    '3/8\n목': (-2, 0), '4/9\n금': (2, 0),
    '5/10\n토': (0, 0),
}
for label, (x, y) in hutu_pos.items():
    wx = label.split('\n')[1]
    ax.add_patch(plt.Circle((x, y), 0.6, facecolor=wuxing_color[wx], edgecolor='black', linewidth=2))
    ax.text(x, y, label, ha='center', va='center', fontsize=11, fontweight='bold')
# 연결선: 상생순환
for a, b in [('1/6\n수','3/8\n목'), ('3/8\n목','2/7\n화'), ('2/7\n화','5/10\n토'), ('5/10\n토','4/9\n금'), ('4/9\n금','1/6\n수')]:
    x1, y1 = hutu_pos[a]; x2, y2 = hutu_pos[b]
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='#44AA44', lw=2, connectionstyle='arc3,rad=0.15'))
ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('河圖 4-5 基礎 (四象+五居中央)\n4×5=20, 4+5=9', fontsize=14, fontweight='bold')

ax = axes[1]
# 5궁 = 오행 그룹
wx_groups = {
    '수': [1, 6, 11, 16], '화': [2, 7, 12, 17], '목': [3, 8, 13, 18],
    '금': [4, 9, 14, 19], '토': [5, 10, 15, 20]
}
positions_5 = [(0, 2), (-2, 0.5), (2, 0.5), (-1, -2), (1, -2)]
for (wx, nodes), (x, y) in zip(wx_groups.items(), positions_5):
    ax.add_patch(plt.Circle((x, y), 0.7, facecolor=wuxing_color[wx], edgecolor='black', linewidth=2))
    ax.text(x, y+0.15, f'{wx}\n{" ".join(map(str, nodes))}\n합={sum(nodes)}', ha='center', va='center', fontsize=10, fontweight='bold')
ax.set_xlim(-3, 3); ax.set_ylim(-3.5, 3.5); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('五宮: 오행별 4자 그룹\n총합 210, 평균 42', fontsize=14, fontweight='bold')
plt.tight_layout(); save_fig('origin_01_hutu_5palaces.png'); plt.close()

# --- origin_02: 鄰星相兼 → 九宫 42-sum grid ---
fig, ax = plt.subplots(1, 1, figsize=(12, 12))
grid_pos = {
    'NW': (-2, 2), 'N': (0, 2), 'NE': (2, 2),
    'W': (-2, 0), 'C': (0, 0), 'E': (2, 0),
    'SW': (-2, -2), 'S': (0, -2), 'SE': (2, -2),
}
for name, (x, y) in grid_pos.items():
    palace_nodes = NINE_PALACES[name]
    # 궁 경계
    rect = plt.Rectangle((x-0.9, y-0.9), 1.8, 1.8, fill=True, facecolor='lightyellow', edgecolor='black', linewidth=2)
    ax.add_patch(rect)
    # 4자 배치
    offsets = [(-0.4, 0.3), (0.4, 0.3), (-0.4, -0.3), (0.4, -0.3)]
    for node, (dx, dy) in zip(palace_nodes, offsets):
        circle = plt.Circle((x+dx, y+dy), 0.22, facecolor=wuxing_color[wuxing[node]], edgecolor='black', linewidth=1.5)
        ax.add_patch(circle)
        ax.text(x+dx, y+dy, str(node), ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(x, y+0.72, f'{name}', ha='center', va='center', fontsize=13, fontweight='bold')
    ax.text(x, y-0.72, f'합=42', ha='center', va='center', fontsize=12, fontweight='bold', color='red')

# 화살표로 우회전(시계방향) 표시
arrow_style = dict(arrowstyle='->', color='purple', lw=2.5, connectionstyle='arc3,rad=0.2')
for start, end in [('NW','N'), ('N','NE'), ('NE','E'), ('E','SE'), ('SE','S'), ('S','SW'), ('SW','W'), ('W','NW')]:
    x1, y1 = grid_pos[start]; x2, y2 = grid_pos[end]
    ax.annotate('', xy=(x2-0.5*np.sign(x2), y2-0.5*np.sign(y2)), xytext=(x1+0.5*np.sign(x1), y1+0.5*np.sign(y1)),
                arrowprops=arrow_style)
ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('鄰星相兼 五宮化爲九宫\n每宮四子 各得四十二數', fontsize=16, fontweight='bold')
plt.tight_layout(); save_fig('origin_02_9palace_grid.png'); plt.close()

# --- origin_03: 右旋 변환 ---
fig, ax = plt.subplots(1, 1, figsize=(12, 10))
# 왼쪽: 5궁
left_pos = {'수': (0, 2), '목': (-1.5, 0.5), '화': (1.5, 0.5), '금': (-0.8, -1.5), '토': (0.8, -1.5)}
for wx, (x, y) in left_pos.items():
    ax.add_patch(plt.Circle((x-5, y), 0.6, facecolor=wuxing_color[wx], edgecolor='black', linewidth=2))
    ax.text(x-5, y, wx, ha='center', va='center', fontsize=14, fontweight='bold')
# 오른쪽: 九宫 (3x3)
for name, (x, y) in grid_pos.items():
    ax.add_patch(plt.Rectangle((x+2.1, y-0.4), 0.8, 0.8, fill=True, facecolor='lightyellow', edgecolor='black', linewidth=1.5))
    ax.text(x+2.5, y, '42', ha='center', va='center', fontsize=11, fontweight='bold')
# 화살표 + 회전 기호
ax.annotate('', xy=(1, 0), xytext=(-3, 0), arrowprops=dict(arrowstyle='->', color='black', lw=3))
ax.text(-1, 0.6, '右旋 (시계방향)', ha='center', va='center', fontsize=14, fontweight='bold')
ax.text(-1, -0.6, '5궁 → 9궁', ha='center', va='center', fontsize=13, fontweight='bold')
ax.set_xlim(-7, 5.5); ax.set_ylim(-3.5, 3.5); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('河圖四五画 右旋者\n五宮이 우회전하여 九宫으로 변화', fontsize=16, fontweight='bold')
plt.tight_layout(); save_fig('origin_03_right_rotation.png'); plt.close()

# --- origin_04: 互化 1890 ---
fig, ax = plt.subplots(1, 1, figsize=(14, 10))
# 5궁 (왼쪽 세로)
wx_list = ['수', '화', '목', '금', '토']
for i, wx in enumerate(wx_list):
    y = 2 - i * 1.0
    ax.add_patch(plt.Circle((-3, y), 0.35, facecolor=wuxing_color[wx], edgecolor='black', linewidth=2))
    ax.text(-3, y, wx, ha='center', va='center', fontsize=12, fontweight='bold')
# 9궁 (위쪽 가로)
palace_names = list(grid_pos.keys())
for j, name in enumerate(palace_names):
    x = -2 + j * 0.9
    ax.add_patch(plt.Rectangle((x-0.3, 3.2), 0.6, 0.6, fill=True, facecolor='lightyellow', edgecolor='black', linewidth=1.5))
    ax.text(x, 3.5, name, ha='center', va='center', fontsize=9, fontweight='bold')
# 연결선: 5 × 9 = 45
for i in range(5):
    for j in range(9):
        x = -2 + j * 0.9
        y = 2 - i * 1.0
        ax.plot([-3+0.3, x], [y, 3.2], '-', color='gray', alpha=0.15, linewidth=0.5)
# 수식
ax.text(0, -3, '互化: 5궁 × 9궁 = 45', ha='center', va='center', fontsize=18, fontweight='bold')
ax.text(0, -3.7, '45 × 42 = 1,890', ha='center', va='center', fontsize=22, fontweight='bold', color='red')
ax.set_xlim(-4, 6.5); ax.set_ylim(-4.5, 4.5); ax.axis('off')
ax.set_title('互化則一千八百九十數', fontsize=18, fontweight='bold')
plt.tight_layout(); save_fig('origin_04_mutual_transformation_1890.png'); plt.close()

# --- origin_05: 42 불변량 분석 ---
fig, axes = plt.subplots(2, 2, figsize=(16, 14))

# 3×2 사각형의 4개 면 외곽 4정점 + 내장 4-cycle
ax = axes[0, 0]
labels_42 = ['NW\n외곽', 'NE\n외곽', 'SW\n외곽', 'SE\n외곽', '내장\n4-Cycle']
values_42 = [sum(NINE_PALACES[k]) for k in ['NW', 'NE', 'SW', 'SE', 'C']]
colors_42 = ['#CC4444', '#4488CC', '#44AA44', '#CC9944', '#888888']
ax.bar(labels_42, values_42, color=colors_42, edgecolor='black', linewidth=1.5)
ax.axhline(y=42, color='red', linestyle='--', linewidth=2)
ax.set_title('42 합의 5궁 구조', fontsize=13, fontweight='bold')
for bar, val in zip(ax.patches, values_42):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, str(val), ha='center', fontsize=12, fontweight='bold')

# 九宫 grid 색상화
ax = axes[0, 1]
for name, (x, y) in grid_pos.items():
    palace_nodes = NINE_PALACES[name]
    rect = plt.Rectangle((x-0.9, y-0.9), 1.8, 1.8, fill=True, facecolor='#FFF8DC', edgecolor='black', linewidth=2)
    ax.add_patch(rect)
    ax.text(x, y+0.6, name, ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(x, y-0.6, 'Σ=42', ha='center', va='center', fontsize=11, fontweight='bold', color='red')
    # 노드 색상 점으로 표시
    for k, node in enumerate(palace_nodes):
        angle = 2 * np.pi * k / 4
        px, py = x + 0.45 * np.cos(angle), y + 0.45 * np.sin(angle)
        ax.add_patch(plt.Circle((px, py), 0.15, facecolor=wuxing_color[wuxing[node]], edgecolor='black', linewidth=1))
        ax.text(px, py, str(node), ha='center', va='center', fontsize=9, fontweight='bold')
ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('九宫 42-불변량 분포', fontsize=13, fontweight='bold')

# 5궁 → 9궁 → 1890 흐름
ax = axes[1, 0]
ax.text(0.5, 0.8, '五宮 (5 palaces)', ha='center', va='center', fontsize=14, fontweight='bold')
ax.text(0.5, 0.65, 'avg sum = 42', ha='center', va='center', fontsize=12)
ax.annotate('', xy=(0.5, 0.45), xytext=(0.5, 0.55), arrowprops=dict(arrowstyle='->', color='black', lw=2))
ax.text(0.5, 0.35, '右旋 → 九宫 (9 palaces)', ha='center', va='center', fontsize=14, fontweight='bold')
ax.text(0.5, 0.2, 'each sum = 42', ha='center', va='center', fontsize=12)
ax.annotate('', xy=(0.5, 0.0), xytext=(0.5, 0.1), arrowprops=dict(arrowstyle='->', color='black', lw=2))
ax.text(0.5, -0.15, '互化: 5 × 9 = 45 interactions', ha='center', va='center', fontsize=14, fontweight='bold')
ax.text(0.5, -0.35, '45 × 42 = 1,890', ha='center', va='center', fontsize=20, fontweight='bold', color='red')
ax.set_xlim(0, 1); ax.set_ylim(-0.6, 1); ax.axis('off')
ax.set_title('주석의 수학적 흐름', fontsize=13, fontweight='bold')

# 각 궁의 오행 분포
ax = axes[1, 1]
palace_names_ordered = ['NW', 'N', 'NE', 'W', 'C', 'E', 'SW', 'S', 'SE']
wx_counts_per_palace = {name: {} for name in palace_names_ordered}
for name in palace_names_ordered:
    for node in NINE_PALACES[name]:
        wx = wuxing[node]
        wx_counts_per_palace[name][wx] = wx_counts_per_palace[name].get(wx, 0) + 1

bottom = np.zeros(9)
for wx in ['수', '화', '목', '금', '토']:
    counts = [wx_counts_per_palace[name].get(wx, 0) for name in palace_names_ordered]
    ax.bar(palace_names_ordered, counts, bottom=bottom, label=wx, color=wuxing_color[wx], edgecolor='black', linewidth=1)
    bottom += counts
ax.set_title('九宫 각 궁의 오행 분포', fontsize=13, fontweight='bold')
ax.legend(loc='upper right')
ax.set_ylabel('Count')

plt.tight_layout(); save_fig('origin_05_42_invariants.png'); plt.close()

# --- origin_06: 교정된 그래프 위에 九宫 오버레이 ---
fig, ax = plt.subplots(1, 1, figsize=(14, 14))
for name, hedges in hex_edges.items():
    nx.draw_networkx_edges(G, POSITIONS, edgelist=hedges, edge_color=hex_colors[name], width=2.5, alpha=0.6, ax=ax)
nx.draw_networkx_nodes(G, POSITIONS, node_color=node_colors, node_size=1200, edgecolors='black', linewidths=1.5, ax=ax)
nx.draw_networkx_labels(G, POSITIONS, font_size=11, font_weight='bold', ax=ax)
# 九宫 구역 표시
palace_regions = {
    'NW': (-2.3, 2.3), 'N': (0, 2.3), 'NE': (2.3, 2.3),
    'W': (-2.3, 0), 'C': (0, 0), 'E': (2.3, 0),
    'SW': (-2.3, -2.3), 'S': (0, -2.3), 'SE': (2.3, -2.3),
}
for name, (x, y) in palace_regions.items():
    ax.text(x, y, f'{name}\nΣ42', ha='center', va='center', fontsize=13, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='red', alpha=0.85))
ax.set_title('원본 그래프 위의 九宫 해석\n鄰星相兼에 의한 구역 분할', fontsize=16, fontweight='bold')
ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5); ax.axis('off')
plt.tight_layout(); save_fig('origin_06_graph_with_9palace.png'); plt.close()

# ============================================
# 5. 원문 주석의 현대 조합론 번역 이미지 생성
# ============================================

print("\n" + "-" * 60)
print("원문 주석의 현대 조합론 번역 이미지 생성")
print("-" * 60)

modern_terms = [
    ('鄰星相兼', 'adjacent blocks overlap / neighboring 4-subsets are combined'),
    ('五宮化爲九宫', '5 residue classes are reorganized into 9 blocks'),
    ('每宮四子', 'each block has cardinality 4'),
    ('各得四十二數', 'each block has invariant sum 42'),
    ('右旋', 'clockwise cyclic action on the boundary blocks'),
    ('互化則一千八百九十數', '5 × 9 incidence product, weighted by 42 = 1,890'),
]

# --- origin_translated_01: 한문 구절을 현대 조합론 명제로 번역 ---
fig, ax = plt.subplots(1, 1, figsize=(16, 10))
ax.axis('off')
ax.set_title('원문 주석 → 현대 조합론 용어', fontsize=20, fontweight='bold', pad=20)
for i, (classical, modern) in enumerate(modern_terms):
    y = 0.88 - i * 0.14
    ax.text(0.05, y, classical, ha='left', va='center', fontsize=18, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF8DC', edgecolor='black'))
    ax.annotate('', xy=(0.42, y), xytext=(0.32, y),
                arrowprops=dict(arrowstyle='->', lw=2.5, color='black'))
    ax.text(0.45, y, modern, ha='left', va='center', fontsize=15,
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#EAF3FF', edgecolor='#336699'))
ax.text(0.5, 0.03,
        '핵심 번역: 원문은 신비한 비유가 아니라, 20개 수를 여러 4-부분집합(block)으로 재배열해\n'
        '모든 block의 합을 42로 고정하는 균형 블록 구조를 설명한다.',
        ha='center', va='center', fontsize=15, fontweight='bold', color='#333333')
plt.tight_layout(); save_fig('origin_translated_01_terms.png'); plt.close()

# --- origin_translated_02: 5개 residue class에서 9개 block으로 ---
fig, axes = plt.subplots(1, 2, figsize=(18, 9))
ax = axes[0]
for i, wx in enumerate(['수', '화', '목', '금', '토']):
    nodes = [n for n in sorted(G.nodes()) if wuxing[n] == wx]
    y = 4 - i
    ax.add_patch(plt.Rectangle((-0.7, y-0.35), 4.1, 0.7, facecolor=wuxing_color[wx], edgecolor='black', alpha=0.85))
    ax.text(-1.0, y, f'{wx}', ha='right', va='center', fontsize=14, fontweight='bold')
    ax.text(1.35, y, f'{{{", ".join(map(str, nodes))}}}', ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(3.75, y, f'Σ={sum(nodes)}', ha='left', va='center', fontsize=12)
ax.set_xlim(-1.5, 5.2); ax.set_ylim(-0.8, 4.8); ax.axis('off')
ax.set_title('입력: 5개 residue class\nmod 5로 나눈 오행 그룹', fontsize=15, fontweight='bold')

ax = axes[1]
for name, (x, y) in grid_pos.items():
    nodes = NINE_PALACES[name]
    ax.add_patch(plt.Rectangle((x-0.88, y-0.75), 1.76, 1.5, facecolor='#F7FBFF', edgecolor='black', linewidth=2))
    ax.text(x, y+0.48, f'B_{name}', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(x, y+0.05, '{' + ', '.join(map(str, nodes)) + '}', ha='center', va='center', fontsize=10)
    ax.text(x, y-0.48, '|B|=4, Σ=42', ha='center', va='center', fontsize=10, color='red', fontweight='bold')
ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('출력: 9개 4-block\n모든 block의 합이 42', fontsize=15, fontweight='bold')
fig.suptitle('五宮化爲九宫 = 5분류를 9개 균형 블록으로 재구성', fontsize=18, fontweight='bold')
plt.tight_layout(); save_fig('origin_translated_02_blocks.png'); plt.close()

# --- origin_translated_03: 鄰星相兼을 block overlap으로 해석 ---
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
ax.set_title('鄰星相兼 = 인접 block의 겹침(overlap)을 이용한 9궁 구성', fontsize=17, fontweight='bold')
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
ax.set_title('每宮四子 各得四十二數 = 9개의 4-block이 같은 합 불변량 42를 가진다', fontsize=17, fontweight='bold')
plt.tight_layout(); save_fig('origin_translated_04_invariant_table.png'); plt.close()

# --- origin_translated_05: 右旋 as cyclic permutation ---
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
ax.set_title('右旋 = 중앙 block을 고정한 경계 8-block의 시계방향 순환 작용', fontsize=17, fontweight='bold')
plt.tight_layout(); save_fig('origin_translated_05_cyclic_action.png'); plt.close()

# --- origin_translated_06: 互化 1890 as weighted incidence product ---
fig, axes = plt.subplots(1, 2, figsize=(18, 9))
ax = axes[0]
incidence = np.ones((5, 9))
im = ax.imshow(incidence, cmap='Blues', vmin=0, vmax=1)
ax.set_xticks(range(9)); ax.set_xticklabels([f'B_{n}' for n in palace_names_ordered], rotation=45, ha='right')
ax.set_yticks(range(5)); ax.set_yticklabels([f'{wx} class' for wx in ['수', '화', '목', '금', '토']])
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
        '互化는 5분류와 9-block 사이의 모든 조합을 세고,\n'
        '각 조합에 공통 가중치 42를 부여한 총합으로 읽을 수 있다.',
        ha='center', va='center', fontsize=14, fontweight='bold')
fig.suptitle('互化則一千八百九十數 = weighted incidence count', fontsize=18, fontweight='bold')
plt.tight_layout(); save_fig('origin_translated_06_weighted_incidence.png'); plt.close()

print("\n" + "=" * 60)
print("모든 이미지 생성 완료!")
print(f"출력 디렉토리: {OUTPUT_DIR}/")
print("=" * 60)
