#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
09 구구자수변궁양도/음도(九九子數變宮陽圖/陰圖) 크로네커 곱 및 고급 분석 스크립트.

3x3 낙서 마방진 기저 두 개(L1 ⊗ L2)의 Kronecker 곱을 이용해 9x9 양도 및 음도를 자동 생성하고,
인접 행렬 스펙트럼, 대각선 불변량 및 그래프 위상을 분석합니다.
"""

import sys
import time
from pathlib import Path
import numpy as np
import networkx as nx

# 루트 디렉토리 모듈 로드
REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from rotation_analysis import (
    compute_advanced_spectral_analysis,
    get_canonical_matrix_d8,
    kronecker_product_2d,
)

LUOSHU = np.array([
    [4, 9, 2],
    [3, 5, 7],
    [8, 1, 6]
])

YIN_MATRIX = np.array([
    [ 9,  8,  7,  6,  5, 54, 63, 72,  1],
    [18, 21, 14,  8, 10, 12,  6, 64, 72],
    [27, 24, 24, 12, 35, 18, 16,  6, 63],
    [36, 32, 28, 16, 20,  9, 18, 12, 54],
    [45, 30, 15, 40, 25, 20, 35, 10,  5],
    [ 4, 48, 42, 49, 40, 16, 12,  8,  6],
    [ 3, 56, 36, 42, 15, 28, 24, 14,  7],
    [ 2,  4, 56, 48, 30, 32, 24, 21,  8],
    [81,  2,  3,  4, 45, 36, 27, 18,  9],
])


def generate_yangdo(L1: np.ndarray = LUOSHU, L2: np.ndarray = LUOSHU) -> np.ndarray:
    return kronecker_product_2d(L1, L2)


def build_grid_graph(matrix: np.ndarray) -> nx.Graph:
    rows, cols = matrix.shape
    G = nx.grid_2d_graph(rows, cols)
    for r in range(rows):
        for c in range(cols):
            G.nodes[(r, c)]["val"] = float(matrix[r, c])
    return G


def analyze_invariants(matrix: np.ndarray) -> dict:
    main_diag = int(np.trace(matrix))
    anti_diag = int(np.trace(np.fliplr(matrix)))
    row_sums = [int(s) for s in matrix.sum(axis=1)]
    col_sums = [int(s) for s in matrix.sum(axis=0)]
    
    block_sums = []
    for br in (0, 3, 6):
        for bc in (0, 3, 6):
            block_sums.append(int(matrix[br:br+3, bc:bc+3].sum()))
            
    return {
        "main_diag": main_diag,
        "anti_diag": anti_diag,
        "row_sums": row_sums,
        "col_sums": col_sums,
        "block_sums": block_sums,
    }


def plot_visualization(yangdo: np.ndarray, yin: np.ndarray, spec_yang: dict, spec_yin: dict, output_path: str):
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    im0 = axes[0, 0].imshow(yangdo, cmap="YlGnBu")
    axes[0, 0].set_title("Yangdo Matrix (L1 ⊗ L2)", fontsize=12, fontweight="bold")
    plt.colorbar(im0, ax=axes[0, 0])
    
    im1 = axes[0, 1].imshow(yin, cmap="YlOrRd")
    axes[0, 1].set_title("Yin Matrix (Gusuryak Text)", fontsize=12, fontweight="bold")
    plt.colorbar(im1, ax=axes[0, 1])
    
    ev_yang = np.abs(spec_yang["eigenvalues"])
    ev_yin = np.abs(spec_yin["eigenvalues"])
    axes[1, 0].plot(ev_yang, "o-", color="#2ECC71", label=f"Yangdo (Max={max(ev_yang):.1f})")
    axes[1, 0].plot(ev_yin, "s--", color="#E74C3C", label=f"Yin (Max={max(ev_yin):.1f})")
    axes[1, 0].set_title("Adjacency Eigenvalues Magnitude", fontsize=12, fontweight="bold")
    axes[1, 0].set_xlabel("Eigenvalue Index")
    axes[1, 0].set_ylabel("Magnitude |λ|")
    axes[1, 0].grid(True, linestyle=":", alpha=0.6)
    axes[1, 0].legend()
    
    yang_inv = analyze_invariants(yangdo)
    yin_inv = analyze_invariants(yin)
    categories = ["Main Diag", "Anti Diag"]
    yang_vals = [yang_inv["main_diag"], yang_inv["anti_diag"]]
    yin_vals = [yin_inv["main_diag"], yin_inv["anti_diag"]]
    
    x = np.arange(len(categories))
    width = 0.35
    axes[1, 1].bar(x - width/2, yang_vals, width, label="Yangdo", color="#3498DB")
    axes[1, 1].bar(x + width/2, yin_vals, width, label="Yin", color="#E67E22")
    axes[1, 1].set_xticks(x)
    axes[1, 1].set_xticklabels(categories)
    axes[1, 1].set_title("Diagonal Sum Invariants", fontsize=12, fontweight="bold")
    axes[1, 1].grid(True, axis="y", linestyle=":", alpha=0.6)
    axes[1, 1].legend()

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"[Saved] Visualization: {output_path}")


def main():
    start_time = time.time()

    yangdo = generate_yangdo(LUOSHU, LUOSHU)
    yin = YIN_MATRIX

    canon_yang = get_canonical_matrix_d8(yangdo)
    canon_yin = get_canonical_matrix_d8(yin)
    non_isomorphic_count = 2 if canon_yang != canon_yin else 1

    G_yang = build_grid_graph(yangdo)
    G_yin = build_grid_graph(yin)

    spec_yang = compute_advanced_spectral_analysis(G_yang)
    spec_yin = compute_advanced_spectral_analysis(G_yin)

    mat_spec_yang = compute_advanced_spectral_analysis(yangdo)
    mat_spec_yin = compute_advanced_spectral_analysis(yin)

    img_path = Path(__file__).parent / "gugusubyeongung_kronecker_spectrum.png"
    plot_visualization(yangdo, yin, mat_spec_yang, mat_spec_yin, str(img_path))

    exec_time = time.time() - start_time

    print("[Gugusubyeongungyangdo] Advanced Analysis Report")
    print(f"1. Non-Isomorphic Solutions Count: {non_isomorphic_count}")
    print(f"2. Spectral Radius (Eigenvalues): [{mat_spec_yang['spectral_radius']:.4f}, {mat_spec_yin['spectral_radius']:.4f}]")
    
    top_yang_betw = max(spec_yang['betweenness_centrality'].values())
    top_yin_betw = max(spec_yin['betweenness_centrality'].values())
    print(f"3. Graph Betweenness Centrality: [{top_yang_betw:.4f}, {top_yin_betw:.4f}]")
    print(f"4. Execution Time: {exec_time:.2f} sec")


if __name__ == "__main__":
    main()
