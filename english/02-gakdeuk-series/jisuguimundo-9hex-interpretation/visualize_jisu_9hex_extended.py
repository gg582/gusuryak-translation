#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extended visualisations for the 30-vertex 9-hex Jisuguimundo.

Generates interpretive figures that connect the original commentary to the
solved graph structure:
  1. made/used (作/用) multiplicity
  2. mod 2 parity with reflection symmetry axes
  3. 9 palaces → 12 palaces reinterpretation
  4. centre-manages-3-palaces structure
  5. adjacency matrix and graph spectrum
  6. per-hexagon magic-constant emphasis

All identifiers are in English so the script can be mirrored in the English
folder without transliteration.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Polygon


plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Noto Sans CJK KR", "Noto Sans CJK JP", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


ROOT = Path(__file__).resolve().parent


def load_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def residue_1based(value: int, mod: int) -> int:
    r = value % mod
    return mod if r == 0 else r


def build_coords(topology: dict[str, Any]) -> dict[int, tuple[float, float]]:
    return {int(k): (v["x"], v["y"]) for k, v in topology["vertices"].items()}


def build_unique_edges(topology: dict[str, Any]) -> set[tuple[int, int]]:
    return {tuple(sorted((int(u), int(v)))) for u, v in topology["edges"]}


def draw_base_graph(
    ax: Any,
    coords: dict[int, tuple[float, float]],
    edges: set[tuple[int, int]],
    edge_color: str = "#CCCCCC",
    edge_width: float = 1.5,
) -> None:
    for u, v in edges:
        x_pts = [coords[u][0], coords[v][0]]
        y_pts = [coords[u][1], coords[v][1]]
        ax.plot(x_pts, y_pts, color=edge_color, linewidth=edge_width, zorder=1)


def draw_multiplicity(
    topology: dict[str, Any],
    solution: dict[str, Any],
    output_path: Path,
) -> None:
    """Visualise 作/用 separation via vertex multiplicity on the 9 hexagons."""
    coords = build_coords(topology)
    edges = build_unique_edges(topology)
    assignment = solution["assignment"]
    hexagons = topology["hexagons"]
    node_count = topology["node_count"]

    mult = [0] * node_count
    for hx in hexagons:
        for v in hx:
            mult[v - 1] += 1

    colors = {1: "#4A90E2", 2: "#E94B3C", 3: "#6AB04C"}
    labels = {1: "1 time", 2: "2 times", 3: "3 times"}

    fig, ax = plt.subplots(figsize=(10, 12), facecolor="#FDFBF7")
    ax.set_aspect("equal")
    ax.axis("off")
    draw_base_graph(ax, coords, edges)

    for node_id in sorted(coords):
        x, y = coords[node_id]
        m = mult[node_id - 1]
        size = 400 + 450 * m
        ax.scatter(
            x, y,
            color=colors[m],
            edgecolors="#333333",
            s=size,
            linewidths=2,
            zorder=2,
        )
        ax.text(
            x, y, str(assignment[node_id - 1]),
            color="white",
            fontsize=13,
            fontweight="bold",
            va="center",
            ha="center",
            zorder=3,
        )

    # Legend
    for m in [1, 2, 3]:
        count = sum(1 for x in mult if x == m)
        ax.scatter([], [], color=colors[m], s=200, edgecolors="#333333", linewidths=1.5,
                   label=f"{labels[m]} ({count} vertices)")
    ax.legend(loc="upper right", fontsize=11, frameon=True, fancybox=True)

    ax.set_title(
        "作/用 (made/used) separation\n30 written numbers → 54 used positions",
        fontsize=15, fontweight="bold", color="#2C3E50", pad=12,
    )

    # Summary box
    total_used = sum(len(hx) for hx in hexagons)
    duplicate_positions = total_used - node_count
    text = (
        f"Made (作): {node_count} numbers\n"
        f"Used (用): {total_used} positions\n"
        f"Duplicate positions: {duplicate_positions}"
    )
    ax.text(
        0.02, 0.98, text,
        transform=ax.transAxes,
        fontsize=11,
        verticalalignment="top",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="#999999", alpha=0.9),
    )

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {output_path}")


def draw_mod2_symmetry(
    topology: dict[str, Any],
    solution: dict[str, Any],
    output_path: Path,
) -> None:
    """Parity distribution with vertical/horizontal reflection axes."""
    coords = build_coords(topology)
    edges = build_unique_edges(topology)
    assignment = solution["assignment"]

    parity = [residue_1based(v, 2) for v in assignment]
    odd_color, even_color = "#E94B3C", "#4A90E2"

    fig, ax = plt.subplots(figsize=(10, 12), facecolor="#FDFBF7")
    ax.set_aspect("equal")
    ax.axis("off")
    draw_base_graph(ax, coords, edges)

    for node_id in sorted(coords):
        x, y = coords[node_id]
        p = parity[node_id - 1]
        color = odd_color if p == 1 else even_color
        ax.scatter(
            x, y,
            color=color,
            edgecolors="#333333",
            s=900,
            linewidths=2,
            zorder=2,
        )
        ax.text(
            x, y, str(assignment[node_id - 1]),
            color="white",
            fontsize=13,
            fontweight="bold",
            va="center",
            ha="center",
            zorder=3,
        )

    # Reflection axes
    ax.axvline(0, color="#2C3E50", linestyle="--", linewidth=1.5, alpha=0.6, zorder=0)
    ax.axhline(0, color="#2C3E50", linestyle="--", linewidth=1.5, alpha=0.6, zorder=0)
    ax.text(0.05, 0.98, "vertical axis", transform=ax.transAxes, fontsize=10, color="#555555")
    ax.text(0.98, 0.52, "horizontal axis", transform=ax.transAxes, fontsize=10,
            color="#555555", ha="right")

    # Quadrant counts for odd numbers
    quadrants = {"Q1 (right/top)": 0, "Q2 (left/top)": 0, "Q3 (left/bottom)": 0, "Q4 (right/bottom)": 0}
    for nid in coords:
        x, y = coords[nid]
        if parity[nid - 1] == 1:
            if x >= 0 and y >= 0:
                quadrants["Q1 (right/top)"] += 1
            elif x < 0 and y >= 0:
                quadrants["Q2 (left/top)"] += 1
            elif x < 0 and y < 0:
                quadrants["Q3 (left/bottom)"] += 1
            else:
                quadrants["Q4 (right/bottom)"] += 1

    odd_count = sum(1 for p in parity if p == 1)
    even_count = len(parity) - odd_count
    stats = (
        f"Odd (red): {odd_count}\n"
        f"Even (blue): {even_count}\n\n"
        "Odd numbers by quadrant:\n" +
        "\n".join(f"  {k}: {v}" for k, v in quadrants.items())
    )
    ax.text(
        0.02, 0.98, stats,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="#999999", alpha=0.9),
    )

    ax.scatter([], [], color=odd_color, s=120, edgecolors="#333333", linewidths=1.5, label="Odd")
    ax.scatter([], [], color=even_color, s=120, edgecolors="#333333", linewidths=1.5, label="Even")
    ax.legend(loc="upper right", fontsize=11)

    ax.set_title(
        "mod 2 parity and reflection symmetry",
        fontsize=15, fontweight="bold", color="#2C3E50", pad=12,
    )

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {output_path}")


def draw_9to12_palaces(
    topology: dict[str, Any],
    output_path: Path,
) -> None:
    """Visualise the reinterpretation of 9 hex palaces as 12 palace units."""
    hex_centers = topology["hex_centers"]

    # 12 zodiac / directional palace labels around the centre
    palace_labels = [
        "子 N", "丑 NNE", "寅 NE", "卯 ENE", "辰 E", "巳 ESE",
        "午 SE", "未 SSE", "申 S", "酉 SSW", "戌 SW", "亥 WSW", "子 W", "丑 WNW", "寅 NW", "卯 NNW"
    ]
    # Use 12 evenly spaced directions
    angles = np.linspace(90, 90 - 360, 13)[:-1]  # start at top, clockwise
    radius = 3.8

    fig, ax = plt.subplots(figsize=(10, 10), facecolor="#FDFBF7")
    ax.set_aspect("equal")
    ax.axis("off")

    # Outer 12-palace ring
    for angle, label in zip(angles, palace_labels[:12]):
        rad = np.deg2rad(angle)
        x, y = radius * np.cos(rad), radius * np.sin(rad)
        ax.scatter(x, y, color="#F39C12", edgecolors="#333333", s=1200, linewidths=2, zorder=2)
        ax.text(x, y, label, ha="center", va="center", fontsize=9,
                fontweight="bold", color="#2C3E50", zorder=3)

    # Inner 9 hex palace centres
    for hc in hex_centers:
        x, y = hc["x"], hc["y"]
        ax.scatter(x, y, color="#4A90E2", edgecolors="#333333", s=900, linewidths=2, zorder=2)
        ax.text(x, y, hc["label"], ha="center", va="center", fontsize=10,
                fontweight="bold", color="white", zorder=3)

    # Connections: each hex centre to nearest palace directions
    for hc in hex_centers:
        hx, hy = hc["x"], hc["y"]
        angle = np.arctan2(hy, hx)
        # nearest two palace angles
        idx = int(np.round((np.rad2deg(angle) - 90) / -30)) % 12
        for di in [0, 1]:
            pidx = (idx + di) % 12
            pangle = np.deg2rad(angles[pidx])
            px, py = radius * np.cos(pangle), radius * np.sin(pangle)
            ax.plot([hx, px], [hy, py], color="#BBBBBB", linewidth=1, alpha=0.5, zorder=1)

    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_title(
        "9 palaces (hexagons) → 12 palaces (directional units)\n"
        "Reinterpreting the nine hexagon palaces as twelve directional palaces",
        fontsize=14, fontweight="bold", color="#2C3E50", pad=12,
    )

    explanation = (
        "Inner blue: 9 hexagon palaces\n"
        "Outer orange: 12 directional palace units\n"
        "Grey lines: mapping from each hex to adjacent directional sectors"
    )
    ax.text(
        0.02, 0.02, explanation,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="bottom",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="#999999", alpha=0.9),
    )

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {output_path}")


def draw_center_periphery(
    topology: dict[str, Any],
    solution: dict[str, Any],
    output_path: Path,
) -> None:
    """Highlight the central three palaces that govern the rest."""
    coords = build_coords(topology)
    edges = build_unique_edges(topology)
    assignment = solution["assignment"]
    hexagons = topology["hexagons"]
    hex_centers = topology["hex_centers"]

    # Central column: Hex2, Hex5, Hex8
    central_hexes = {2, 5, 8}
    central_nodes = set()
    for idx in central_hexes:
        central_nodes.update(hexagons[idx - 1])

    fig, ax = plt.subplots(figsize=(10, 12), facecolor="#FDFBF7")
    ax.set_aspect("equal")
    ax.axis("off")
    draw_base_graph(ax, coords, edges)

    # Draw all hexagon centres and labels
    for hc in hex_centers:
        x, y = hc["x"], hc["y"]
        color = "#E94B3C" if int(hc["label"][3:]) in central_hexes else "#BDC3C7"
        ax.scatter(x, y, color=color, edgecolors="#333333", s=600, linewidths=2, zorder=2)
        ax.text(x, y, hc["label"], ha="center", va="center", fontsize=9,
                fontweight="bold", color="white" if int(hc["label"][3:]) in central_hexes else "#2C3E50",
                zorder=3)

    # Nodes: central column highlighted
    for node_id in sorted(coords):
        x, y = coords[node_id]
        if node_id in central_nodes:
            color = "#E94B3C"
            size = 1000
        else:
            color = "#BDC3C7"
            size = 700
        ax.scatter(x, y, color=color, edgecolors="#333333", s=size, linewidths=2, zorder=2)
        ax.text(x, y, str(assignment[node_id - 1]), color="white",
                fontsize=12, fontweight="bold", va="center", ha="center", zorder=3)

    ax.set_title(
        "Central three palaces (Hex2, Hex5, Hex8) govern the structure",
        fontsize=14, fontweight="bold", color="#2C3E50", pad=12,
    )

    explanation = (
        "Red: central vertical column of three hexagons\n"
        "Grey: surrounding six hexagons\n"
        "The three central palaces act as the core (中眷三宮, 三宮爲主則)."
    )
    ax.text(
        0.02, 0.98, explanation,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="#999999", alpha=0.9),
    )

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {output_path}")


def draw_adjacency_spectrum(
    topology: dict[str, Any],
    solution: dict[str, Any],
    output_path: Path,
) -> None:
    """Adjacency matrix heatmap and graph spectrum (eigenvalues)."""
    coords = build_coords(topology)
    edges = build_unique_edges(topology)
    assignment = solution["assignment"]
    node_count = topology["node_count"]

    # Build adjacency matrix in solved-value order (node 1..30)
    adj = np.zeros((node_count, node_count), dtype=int)
    for u, v in edges:
        adj[u - 1, v - 1] = 1
        adj[v - 1, u - 1] = 1

    # Degree and Laplacian
    degree = np.diag(adj.sum(axis=1))
    laplacian = degree - adj

    # Eigenvalues
    adj_eigvals = np.linalg.eigvalsh(adj.astype(float))
    lap_eigvals = np.linalg.eigvalsh(laplacian.astype(float))

    fig = plt.figure(figsize=(16, 12), facecolor="#FDFBF7")
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

    # Adjacency matrix
    ax1 = fig.add_subplot(gs[0, 0])
    im = ax1.imshow(adj, cmap="Greys", aspect="equal")
    ax1.set_title("Adjacency matrix (30 vertices)", fontsize=13, fontweight="bold")
    ax1.set_xlabel("vertex index")
    ax1.set_ylabel("vertex index")
    fig.colorbar(im, ax=ax1, fraction=0.046)

    # Degree sequence
    ax2 = fig.add_subplot(gs[0, 1])
    deg_seq = adj.sum(axis=1)
    unique_deg, counts = np.unique(deg_seq, return_counts=True)
    bars = ax2.bar(unique_deg.astype(str), counts, color="#4A90E2", edgecolor="#333333")
    ax2.set_title("Degree distribution", fontsize=13, fontweight="bold")
    ax2.set_xlabel("degree")
    ax2.set_ylabel("count")
    for bar, c in zip(bars, counts):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                 str(int(c)), ha="center", fontsize=10)

    # Adjacency eigenvalues
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.scatter(range(len(adj_eigvals)), sorted(adj_eigvals, reverse=True),
                color="#E94B3C", edgecolors="#333333", s=60, zorder=2)
    ax3.axhline(0, color="#999999", linestyle="--", linewidth=1, zorder=1)
    ax3.set_title("Adjacency eigenvalues", fontsize=13, fontweight="bold")
    ax3.set_xlabel("index")
    ax3.set_ylabel("eigenvalue")

    # Laplacian eigenvalues
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.scatter(range(len(lap_eigvals)), sorted(lap_eigvals),
                color="#6AB04C", edgecolors="#333333", s=60, zorder=2)
    ax4.set_title("Laplacian eigenvalues", fontsize=13, fontweight="bold")
    ax4.set_xlabel("index")
    ax4.set_ylabel("eigenvalue")

    fig.suptitle(
        "Graph-theoretic spectrum of the 9-hex Jisuguimundo",
        fontsize=15, fontweight="bold", color="#2C3E50",
    )

    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {output_path}")


def draw_hexagon_sums(
    topology: dict[str, Any],
    solution: dict[str, Any],
    output_path: Path,
) -> None:
    """Emphasise the magic constant 93 in every hexagon."""
    coords = build_coords(topology)
    edges = build_unique_edges(topology)
    assignment = solution["assignment"]
    hexagons = topology["hexagons"]
    hex_centers = topology["hex_centers"]
    magic_constant = solution["S"]

    fig, ax = plt.subplots(figsize=(10, 12), facecolor="#5e5e5e")
    ax.set_aspect("equal")
    ax.axis("off")

    for u, v in edges:
        x_pts = [coords[u][0], coords[v][0]]
        y_pts = [coords[u][1], coords[v][1]]
        ax.plot(x_pts, y_pts, color="#7f7f7f", linewidth=4, zorder=1)

    for node_id in sorted(coords):
        x, y = coords[node_id]
        ax.scatter(x, y, color="#ffffff", edgecolors="#a6a6a6", s=1500,
                   linewidths=3.5, zorder=2)
        ax.text(x, y, str(assignment[node_id - 1]), color="#2c2c2c",
                fontsize=18, fontweight="bold", va="center", ha="center", zorder=3)

    for hc in hex_centers:
        cx, cy = hc["x"], hc["y"]
        ax.text(cx, cy, str(magic_constant), color="#757575", fontsize=22,
                fontweight="bold", va="center", ha="center", zorder=1)
        vals = [assignment[v - 1] for v in hexagons[int(hc["label"][3:]) - 1]]
        ax.text(cx, cy - 0.55, f"{vals}", color="#999999", fontsize=8,
                ha="center", va="top", zorder=1)

    ax.set_title(
        f"Every hexagon sums to {magic_constant}",
        fontsize=15, fontweight="bold", color="#DDDDDD", pad=12,
    )

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {output_path}")


def main() -> None:
    topology = load_json(ROOT / "jisu_9hex_topology.json")
    solution = load_json(ROOT / "jisu_9hex_solution.json")

    draw_multiplicity(topology, solution, ROOT / "jisu_9hex_multiplicity.png")
    draw_mod2_symmetry(topology, solution, ROOT / "jisu_9hex_mod2_symmetry.png")
    draw_9to12_palaces(topology, ROOT / "jisu_9hex_9to12_palaces.png")
    draw_center_periphery(topology, solution, ROOT / "jisu_9hex_center_periphery.png")
    draw_adjacency_spectrum(topology, solution, ROOT / "jisu_9hex_adjacency_spectrum.png")
    draw_hexagon_sums(topology, solution, ROOT / "jisu_9hex_magic_constant.png")


if __name__ == "__main__":
    main()
