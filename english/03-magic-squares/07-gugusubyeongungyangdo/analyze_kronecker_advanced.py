#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gugusubyeongungyangdo (九九數變宮陽圖/陰圖) Kronecker Product & Advanced Analysis.

This module automates the construction of 9x9 Yangdo and Yin matrices via
Kronecker tensor products (L1 ⊗ L2) of 3x3 Luoshu magic squares, computes
adjacency matrix spectra, diagonal invariants, and graph topology.
"""

import sys
import time
from pathlib import Path
import numpy as np
import networkx as nx

# Add repository root to python path to import shared rotation_analysis
REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from rotation_analysis import (
    compute_advanced_spectral_analysis,
    get_canonical_matrix_d8,
    kronecker_product_2d,
)

# 3x3 Luoshu Base Magic Square
LUOSHU = np.array([
    [4, 9, 2],
    [3, 5, 7],
    [8, 1, 6]
])

# 9x9 Yin Matrix (陰圖) from Gusuryak original text / transcription
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
    """Generate 9x9 Yangdo matrix via Kronecker product of two 3x3 bases."""
    return kronecker_product_2d(L1, L2)


def build_grid_graph(matrix: np.ndarray) -> nx.Graph:
    """Construct a 2D 9x9 grid graph with node values from the matrix."""
    rows, cols = matrix.shape
    G = nx.grid_2d_graph(rows, cols)
    # Assign matrix values as node attribute
    for r in range(rows):
        for c in range(cols):
            G.nodes[(r, c)]["val"] = float(matrix[r, c])
    return G


def analyze_invariants(matrix: np.ndarray) -> dict:
    """Calculate row, column, palace block, and diagonal/anti-diagonal invariants."""
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


def plot_visualization(yangdo: np.ndarray, yin: np.ndarray, spec_yang: dict, spec_yin: dict, output_path: str = "gugusubyeongung_kronecker_spectrum.png"):
    """Plot Yangdo/Yin matrices and their eigenvalue/spectral distributions."""
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Heatmap of Yangdo
    im0 = axes[0, 0].imshow(yangdo, cmap="YlGnBu")
    axes[0, 0].set_title("Yangdo Matrix (L1 ⊗ L2)", fontsize=12, fontweight="bold")
    plt.colorbar(im0, ax=axes[0, 0])
    
    # Heatmap of Yin
    im1 = axes[0, 1].imshow(yin, cmap="YlOrRd")
    axes[0, 1].set_title("Yin Matrix (Gusuryak Text)", fontsize=12, fontweight="bold")
    plt.colorbar(im1, ax=axes[0, 1])
    
    # Eigenvalues distribution
    ev_yang = np.abs(spec_yang["eigenvalues"])
    ev_yin = np.abs(spec_yin["eigenvalues"])
    axes[1, 0].plot(ev_yang, "o-", color="#2ECC71", label=f"Yangdo (Max={max(ev_yang):.1f})")
    axes[1, 0].plot(ev_yin, "s--", color="#E74C3C", label=f"Yin (Max={max(ev_yin):.1f})")
    axes[1, 0].set_title("Adjacency Eigenvalues Magnitude", fontsize=12, fontweight="bold")
    axes[1, 0].set_xlabel("Eigenvalue Index")
    axes[1, 0].set_ylabel("Magnitude |λ|")
    axes[1, 0].grid(True, linestyle=":", alpha=0.6)
    axes[1, 0].legend()
    
    # Diagonal Invariants Comparison
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

    # 1. Automatic generation via Kronecker product
    yangdo = generate_yangdo(LUOSHU, LUOSHU)
    yin = YIN_MATRIX

    # Check non-isomorphism between Yangdo and Yin under D8
    canon_yang = get_canonical_matrix_d8(yangdo)
    canon_yin = get_canonical_matrix_d8(yin)
    non_isomorphic_count = 2 if canon_yang != canon_yin else 1

    # 2. Graph topology & Spectral analysis
    G_yang = build_grid_graph(yangdo)
    G_yin = build_grid_graph(yin)

    spec_yang = compute_advanced_spectral_analysis(G_yang)
    spec_yin = compute_advanced_spectral_analysis(G_yin)

    # Calculate matrix-level spectral radius
    mat_spec_yang = compute_advanced_spectral_analysis(yangdo)
    mat_spec_yin = compute_advanced_spectral_analysis(yin)

    inv_yang = analyze_invariants(yangdo)
    inv_yin = analyze_invariants(yin)

    # 3. Generate visualization plot
    img_path = Path(__file__).parent / "gugusubyeongung_kronecker_spectrum.png"
    plot_visualization(yangdo, yin, mat_spec_yang, mat_spec_yin, str(img_path))

    exec_time = time.time() - start_time

    # Output in standard required report format
    print("[Gugusubyeongungyangdo] Advanced Analysis Report")
    print(f"1. Non-Isomorphic Solutions Count: {non_isomorphic_count}")
    print(f"2. Spectral Radius (Eigenvalues): [{mat_spec_yang['spectral_radius']:.4f}, {mat_spec_yin['spectral_radius']:.4f}]")
    
    top_yang_betw = max(spec_yang['betweenness_centrality'].values())
    top_yin_betw = max(spec_yin['betweenness_centrality'].values())
    print(f"3. Graph Betweenness Centrality: [{top_yang_betw:.4f}, {top_yin_betw:.4f}]")
    print(f"4. Execution Time: {exec_time:.2f} sec")

    print()
    print("--- Detailed Invariants & Comparative Analysis ---")
    print(f"Yangdo Main Diag: {inv_yang['main_diag']}, Anti-Diag: {inv_yang['anti_diag']}")
    print(f"Yin Main Diag:    {inv_yin['main_diag']}, Anti-Diag: {inv_yin['anti_diag']}")
    print(f"Yangdo Block Sums: {inv_yang['block_sums']}")
    print(f"Yin Block Sums:    {inv_yin['block_sums']}")


if __name__ == "__main__":
    main()
