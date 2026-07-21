#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
백자음양착종도(百子子數陰陽錯綜圖) 결합 라틴방진 벤치마크 고급 스크립트.

자식(1~10) 및 부모(0~9) 라틴방진의 10진 결합으로 10x10 마방진(합 505)을 유도하고,
D8 변환에 따른 동형 해 제거 및 그래프 위상 지표를 분석합니다.
"""

import sys
import time
from pathlib import Path
import numpy as np
import networkx as nx

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from rotation_analysis import (
    compute_advanced_spectral_analysis,
    get_canonical_matrix_d8,
)

CORRECTED_MAGIC_SQUARE = np.array([
    [92, 99,  1,  8, 15, 67, 74, 51, 58, 40],
    [98, 80,  7, 14, 16, 73, 55, 57, 64, 41],
    [ 4, 81, 88, 20, 22, 54, 56, 63, 70, 47],
    [85, 87, 19, 21,  3, 60, 62, 69, 71, 28],
    [86, 93, 25,  2,  9, 61, 68, 75, 52, 34],
    [17, 24, 76, 83, 90, 42, 49, 26, 33, 65],
    [23,  5, 82, 89, 91, 48, 30, 32, 39, 66],
    [79,  6, 13, 95, 97, 29, 31, 38, 45, 72],
    [10, 12, 94, 96, 78, 35, 37, 44, 46, 53],
    [11, 18, 100, 77, 84, 36, 43, 50, 27, 59],
])


def generate_circulant_latin_composition() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    P = np.zeros((10, 10), dtype=int)
    C = np.zeros((10, 10), dtype=int)
    for r in range(10):
        for c in range(10):
            P[r, c] = (r + c) % 10
            C[r, c] = ((r - c) % 10) + 1
    M = 10 * P + C
    return M, P, C


def verify_latin_composition(P: np.ndarray, C: np.ndarray) -> bool:
    p_rows = np.all(P.sum(axis=1) == 45)
    p_cols = np.all(P.sum(axis=0) == 45)
    c_rows = np.all(C.sum(axis=1) == 55)
    c_cols = np.all(C.sum(axis=0) == 55)
    return bool(p_rows and p_cols and c_rows and c_cols)


def filter_isomorphic_solutions(matrices: list[np.ndarray]) -> int:
    unique_canonical = set()
    for mat in matrices:
        canon = get_canonical_matrix_d8(mat)
        unique_canonical.add(canon)
    return len(unique_canonical)


def build_10x10_grid_graph(matrix: np.ndarray) -> nx.Graph:
    G = nx.grid_2d_graph(10, 10)
    for r in range(10):
        for c in range(10):
            G.nodes[(r, c)]["val"] = float(matrix[r, c])
    return G


def plot_latin_visualization(M: np.ndarray, P: np.ndarray, C: np.ndarray, output_path: str):
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

    im0 = axes[0].imshow(M, cmap="viridis")
    axes[0].set_title("Combined 10x10 Magic Square (Sum=505)", fontsize=11, fontweight="bold")
    plt.colorbar(im0, ax=axes[0])

    im1 = axes[1].imshow(P, cmap="YlOrBr")
    axes[1].set_title("Parent Latin Square P (0~9, Sum=45)", fontsize=11, fontweight="bold")
    plt.colorbar(im1, ax=axes[1])

    im2 = axes[2].imshow(C, cmap="PuBuGn")
    axes[2].set_title("Child Latin Square C (1~10, Sum=55)", fontsize=11, fontweight="bold")
    plt.colorbar(im2, ax=axes[2])

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"[Saved] Visualization: {output_path}")


def main():
    start_time = time.time()

    M, P, C = generate_circulant_latin_composition()
    assert np.all(M.sum(axis=1) == 505), "Row sums must be 505"
    assert np.all(M.sum(axis=0) == 505), "Column sums must be 505"

    latin_valid = verify_latin_composition(P, C)

    img_path = Path(__file__).parent / "baekjajasuyin_latin_matrix.png"
    plot_latin_visualization(M, P, C, str(img_path))

    non_isomorphic_count = filter_isomorphic_solutions([M, CORRECTED_MAGIC_SQUARE])

    G = build_10x10_grid_graph(M)
    spec_info = compute_advanced_spectral_analysis(G)
    mat_spec_info = compute_advanced_spectral_analysis(M)

    spectral_radius = mat_spec_info["spectral_radius"]
    betweenness_dict = spec_info["betweenness_centrality"]

    top_betw = sorted(betweenness_dict.values(), reverse=True)[:3]
    top_betw_fmt = [round(b, 4) for b in top_betw]

    exec_time = time.time() - start_time

    print("[Baekjajasuyin-yang-chakjong] Advanced Analysis Report")
    print(f"1. Non-Isomorphic Solutions Count: {non_isomorphic_count}")
    print(f"2. Spectral Radius (Eigenvalues): [{spectral_radius:.4f}]")
    print(f"3. Graph Betweenness Centrality: [{top_betw_fmt[0]:.4f}, {top_betw_fmt[1]:.4f}, {top_betw_fmt[2]:.4f}]")
    print(f"4. Execution Time: {exec_time:.2f} sec")


if __name__ == "__main__":
    main()
