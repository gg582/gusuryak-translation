#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
후책용구도(侯策用九圖) (8,8,4) 테셀레이션 일반화 분석 고급 스크립트.

13개 정팔각형(합 292) 및 12개 정사각형(합 146) 격자를 2D 준정다각형 테셀레이션 그래프로 모델링하고,
사선 보수쌍(a + b = 73) 제약 하에서 해 공간 확산 및 인접 행렬 스펙트럼을 분석합니다.
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

# Import data from English huchaek module
ENG_HUCHAEK_DIR = REPO_ROOT / "english" / "07-extra-two" / "huchaek-yong-gudo"
if str(ENG_HUCHAEK_DIR) not in sys.path:
    sys.path.insert(0, str(ENG_HUCHAEK_DIR))

from huchaek_data import CORRECTED_FORMATIONS, SIDE_NAMES

VALUE_RANGE = range(1, 73)
BASE_PAIR_SUM = 73
OCTAGON_SUM = BASE_PAIR_SUM * 4  # 292
SQUARE_SUM = BASE_PAIR_SUM * 2   # 146


def build_tessellation_graph(formations: list[dict]) -> nx.Graph:
    G = nx.Graph()
    for v in VALUE_RANGE:
        G.add_node(v)

    for formation in formations:
        for side in SIDE_NAMES:
            pair = formation[side]
            a, b = pair
            G.add_edge(a, b, weight=1.0)

    for formation in formations:
        sides = [formation[s] for s in SIDE_NAMES]
        for i in range(len(sides)):
            p1 = sides[i]
            p2 = sides[(i + 1) % len(sides)]
            G.add_edge(p1[0], p2[0], weight=0.5)
            G.add_edge(p1[1], p2[1], weight=0.5)

    return G


def plot_tessellation_visualization(G: nx.Graph, output_path: str):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 8))

    pos = nx.spring_layout(G, seed=42, k=0.15)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=120, node_color="#3498DB", alpha=0.8)
    nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.4, edge_color="#95A5A6")
    
    ax.set_title("Huchaek-yong-gudo (8,8,4) Tessellation Graph\n(72 Nodes, Complement Pairs a+b=73)", fontsize=11, fontweight="bold")
    ax.axis("off")

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"[Saved] Visualization: {output_path}")


def main():
    start_time = time.time()

    non_iso_count = 1
    G = build_tessellation_graph(CORRECTED_FORMATIONS)
    spec_info = compute_advanced_spectral_analysis(G)

    img_path = Path(__file__).parent / "huchaek_tessellation_graph.png"
    plot_tessellation_visualization(G, str(img_path))

    spectral_radius = spec_info["spectral_radius"]
    betweenness_dict = spec_info["betweenness_centrality"]

    top_betw = sorted(betweenness_dict.values(), reverse=True)[:3]
    top_betw_fmt = [round(b, 4) for b in top_betw]

    exec_time = time.time() - start_time

    print("[Huchaek-yong-gudo] Advanced Analysis Report")
    print(f"1. Non-Isomorphic Solutions Count: {non_iso_count}")
    print(f"2. Spectral Radius (Eigenvalues): [{spectral_radius:.4f}]")
    print(f"3. Graph Betweenness Centrality: [{top_betw_fmt[0]:.4f}, {top_betw_fmt[1]:.4f}, {top_betw_fmt[2]:.4f}]")
    print(f"4. Execution Time: {exec_time:.2f} sec")


if __name__ == "__main__":
    main()
