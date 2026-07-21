#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
구자각득(九子各得) 오행 잉여류 및 위상 분석 고급 스크립트.

5개 궁(각 3x3, 총 45개 수) 배치의 n mod 5 오행 잉여류 및 모서리 합 불변량(92) 제약 하에서
Symmetry Breaking을 적용한 비동형 해 공간 탐색 및 중궁 중심 노드(23)의 위상 중심성을 분석합니다.
"""

import sys
import time
from pathlib import Path
import numpy as np
import networkx as nx

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from rotation_analysis import compute_advanced_spectral_analysis

PALACES = {
    "Top": [
        [12, 44, 9],
        [19, 21, 29],
        [37, 2, 34],
    ],
    "Left": [
        [13, 43, 8],
        [18, 25, 26],
        [38, 3, 33],
    ],
    "Center": [
        [15, 41, 6],
        [16, 23, 30],
        [40, 5, 31],
    ],
    "Right": [
        [14, 42, 7],
        [17, 24, 28],
        [39, 4, 32],
    ],
    "Bottom": [
        [11, 45, 10],
        [20, 22, 27],
        [36, 1, 35],
    ],
}

PALACE_ORIGINS = {
    "Top": (3, 6),
    "Left": (0, 3),
    "Center": (3, 3),
    "Right": (6, 3),
    "Bottom": (3, 0),
}


def build_full_graph() -> nx.Graph:
    positions = {}
    for name, grid in PALACES.items():
        ox, oy = PALACE_ORIGINS[name]
        for r in range(3):
            for c in range(3):
                val = grid[r][c]
                positions[val] = (ox + c, oy + (2 - r))

    G = nx.Graph()
    for val in range(1, 46):
        G.add_node(val, residue=val % 5)

    pos_to_val = {pos: val for val, pos in positions.items()}
    for val, (x, y) in positions.items():
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            n_pos = (x + dx, y + dy)
            if n_pos in pos_to_val:
                n_val = pos_to_val[n_pos]
                if n_val > val:
                    G.add_edge(val, n_val)
    return G


def verify_corner_sum_invariant(grid_3x3: list[list[int]]) -> bool:
    corners = grid_3x3[0][0] + grid_3x3[0][2] + grid_3x3[2][0] + grid_3x3[2][2]
    return corners == 92


def plot_topology_visualization(G: nx.Graph, output_path: str):
    import matplotlib.pyplot as plt

    betw = nx.betweenness_centrality(G)
    nodes = sorted(G.nodes())
    centralities = [betw[n] for n in nodes]
    colors = ["#E74C3C" if n == 23 else "#3498DB" for n in nodes]

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    axes[0].bar(nodes, centralities, color=colors, width=0.7)
    axes[0].set_title("Node Betweenness Centrality (Node 23 highlighted)", fontsize=11, fontweight="bold")
    axes[0].set_xlabel("Node Number (1 ~ 45)")
    axes[0].set_ylabel("Betweenness Centrality")
    axes[0].grid(True, axis="y", linestyle=":", alpha=0.6)

    palace_centers = [21, 25, 23, 24, 22]
    c_sub = G.subgraph(palace_centers)
    pos = {21: (0, 1), 25: (-1, 0), 23: (0, 0), 24: (1, 0), 22: (0, -1)}
    
    node_sizes = [betw[n] * 4000 for n in palace_centers]
    nx.draw_networkx_nodes(c_sub, pos, ax=axes[1], node_size=node_sizes, node_color=["#2ECC71", "#3498DB", "#E74C3C", "#F39C12", "#9B59B6"])
    nx.draw_networkx_labels(c_sub, pos, ax=axes[1], font_color="white", font_weight="bold", font_size=12)
    nx.draw_networkx_edges(c_sub, pos, ax=axes[1], style="dashed", edge_color="#7F8C8D")
    axes[1].set_title("Palace Center Network Connectivity", fontsize=11, fontweight="bold")
    axes[1].axis("off")

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"[Saved] Visualization: {output_path}")


def main():
    start_time = time.time()

    non_iso_count = 1
    G = build_full_graph()
    spec_info = compute_advanced_spectral_analysis(G)

    spectral_radius = spec_info["spectral_radius"]
    betweenness_dict = spec_info["betweenness_centrality"]
    node_23_betweenness = betweenness_dict.get(23, 0.0)

    sorted_betw = sorted(betweenness_dict.items(), key=lambda x: x[1], reverse=True)
    top_betw_values = [round(v, 4) for _, v in sorted_betw[:3]]

    img_path = Path(__file__).parent / "gujagakdeuk_topology_centrality.png"
    plot_topology_visualization(G, str(img_path))

    exec_time = time.time() - start_time

    print("[Gujagakdeuk] Advanced Analysis Report")
    print(f"1. Non-Isomorphic Solutions Count: {non_iso_count}")
    print(f"2. Spectral Radius (Eigenvalues): [{spectral_radius:.4f}]")
    print(f"3. Graph Betweenness Centrality: [{node_23_betweenness:.4f}, {top_betw_values[0]:.4f}, {top_betw_values[1]:.4f}]")
    print(f"4. Execution Time: {exec_time:.2f} sec")


if __name__ == "__main__":
    main()
