#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Earth-Number Six-Use Diagram (Jisu-yong-yukdo) / Six-Each-Gets —
modern graph and combinatorial deep analysis

A modern mathematical reinterpretation of Jisu-yong-yukdo (地數用六圖)
from the *Gusuryak* (九數略) family of diagrams.
Analysis target: the numbers 1 through 20 placed in 5 hexagons of 6 numbers each,
forming a honeycomb intersection structure.
"""

from __future__ import annotations

import os
import sys
from collections import Counter
from pathlib import Path
from typing import Final

import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.axes import Axes
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Polygon

# ============================================================
# 0. Font and output settings
# ============================================================

fm._load_fontmanager(try_read_cache=False)
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK KR",
    "Noto Sans CJK JP",
    "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False

OUTPUT_DIR = "."
os.makedirs(OUTPUT_DIR, exist_ok=True)

TITLE: Final = "Jisu-yong-yukdo"
HANJA_TITLE: Final = "Earth-Number Six-Use Diagram"
SUBTITLE: Final = "Six-Each-Gets, Sixty-Three"
TARGET_SUM: Final = 63


def find_cjk_font() -> FontProperties:
    candidates = (
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf",
        "/usr/share/fonts/truetype/unfonts-core/UnDotum.ttf",
        "/usr/share/fonts/truetype/baekmuk/dotum.ttf",
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "C:/Windows/Fonts/malgun.ttf",
        "C:/Windows/Fonts/gulim.ttc",
    )
    for candidate in candidates:
        if Path(candidate).exists():
            return FontProperties(fname=candidate)
    return FontProperties()


def save_fig(name: str) -> None:
    path = f"{OUTPUT_DIR}/{name}"
    plt.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    print(f"[Saved] {path}")


# ============================================================
# 1. Original data structure
# ============================================================

# The hand-drawn structure is normalized onto a straight honeycomb lattice.
# The five hexagons share some vertices and edges with adjacent hexagons.
POSITIONS: Final = {
    # Outer vertices of the upper-left hexagon
    5: (-2.0, 4.5),
    18: (-3.0, 3.6),
    16: (-3.0, 2.5),
    3: (-2.0, 1.7),
    8: (-1.0, 2.5),
    13: (-1.0, 3.6),

    # Outer vertices of the upper-right hexagon
    1: (0.0, 4.5),
    7: (1.0, 3.6),
    20: (1.0, 2.5),
    14: (0.0, 1.7),

    # Lower vertices of the center hexagon
    12: (-2.0, 0.3),
    11: (-1.0, -0.5),
    15: (0.0, 0.3),

    # Outer vertices of the lower-left hexagon
    9: (-3.0, -0.5),
    19: (-3.0, -1.7),
    2: (-2.0, -2.5),
    10: (-1.0, -1.7),

    # Outer vertices of the lower-right hexagon
    4: (1.0, -0.5),
    17: (1.0, -1.7),
    6: (0.0, -2.5),
}

# Each hexagon is defined by its six vertices in clockwise order.
HEXAGONS: Final = {
    "upper-left": (5, 18, 16, 3, 8, 13),
    "upper-right": (1, 13, 8, 14, 20, 7),
    "center": (3, 8, 14, 15, 11, 12),
    "lower-left": (12, 11, 10, 2, 19, 9),
    "lower-right": (15, 4, 17, 6, 10, 11),
}

RESIDUE_STYLE: Final = {
    1: {"label": "n mod 5 ≡ 1", "face": "#3F3F3F", "edge": "#161616", "text": "#FFFFFF", "name": "Water", "en": "Water"},
    2: {"label": "n mod 5 ≡ 2", "face": "#F1CDCD", "edge": "#B63E3E", "text": "#782020", "name": "Fire", "en": "Fire"},
    3: {"label": "n mod 5 ≡ 3", "face": "#D4E3F7", "edge": "#3E70AF", "text": "#244C7B", "name": "Wood", "en": "Wood"},
    4: {"label": "n mod 5 ≡ 4", "face": "#E1E1E1", "edge": "#666666", "text": "#222222", "name": "Metal", "en": "Metal"},
    0: {"label": "n mod 5 ≡ 0", "face": "#F5E1A2", "edge": "#B98D00", "text": "#725500", "name": "Earth", "en": "Earth"},
}

PHASE_COLOR: Final = {
    "Water": "#4488CC",
    "Fire": "#CC4444",
    "Wood": "#44AA44",
    "Metal": "#888888",
    "Earth": "#CC9944",
}

HEXAGON_COLORS: Final = {
    "upper-left": "#CC4444",
    "upper-right": "#4488CC",
    "center": "#44AA44",
    "lower-left": "#CC9944",
    "lower-right": "#888888",
}


def phase_of(n: int) -> str:
    r = n % 5
    return RESIDUE_STYLE[r]["name"]


def residue_1based(n: int) -> int:
    r = n % 5
    return 5 if r == 0 else r


# ============================================================
# 2. Graph construction
# ============================================================

FULL_EDGES: list[tuple[int, int]] = []
seen_edges: set[tuple[int, int]] = set()
for vertices in HEXAGONS.values():
    for start, end in zip(vertices, vertices[1:] + vertices[:1]):
        edge = tuple(sorted((start, end)))
        if edge not in seen_edges:
            seen_edges.add(edge)
            FULL_EDGES.append(edge)

G_full = nx.Graph()
G_full.add_edges_from(FULL_EDGES)
for n in range(1, 21):
    G_full.add_node(n)
    G_full.nodes[n]["phase"] = phase_of(n)


# List of hexagons containing each vertex
VERTEX_TO_HEXAGONS: dict[int, list[str]] = {n: [] for n in range(1, 21)}
for hex_name, vertices in HEXAGONS.items():
    for v in vertices:
        VERTEX_TO_HEXAGONS[v].append(hex_name)


def shared_count(v: int) -> int:
    return len(VERTEX_TO_HEXAGONS[v])


# ============================================================
# 3. Combinatorial and graph-theoretic analysis
# ============================================================


def validate() -> None:
    numbers = sorted(POSITIONS)
    if numbers != list(range(1, 21)):
        raise ValueError("The numbers 1 through 20 must appear exactly once.")

    for hex_name, vertices in HEXAGONS.items():
        value_sum = sum(vertices)
        if value_sum != TARGET_SUM:
            raise ValueError(
                f"The {hex_name} hexagon has sum {value_sum}, but it must be {TARGET_SUM}."
            )

    # Verify duplication coefficient total: 5 hexagons × 6 vertices = 30,
    # with shared vertices counted multiple times.
    repeated_total = sum(sum(vertices) for vertices in HEXAGONS.values())
    if repeated_total != TARGET_SUM * len(HEXAGONS):
        raise ValueError(f"Duplication coefficient total is {repeated_total}.")


validate()

print("=" * 60)
print(f"{HANJA_TITLE} ({TITLE}) — modern graph and combinatorial analysis")
print("=" * 60)
print(f"Number of nodes: {G_full.number_of_nodes()}")
print(f"Number of edges: {G_full.number_of_edges()}")
print(f"Connected components: {nx.number_connected_components(G_full)}")

deg_seq_full = sorted([d for _, d in G_full.degree()], reverse=True)
print(f"Degree sequence: {deg_seq_full}")

print("\nSum of six numbers in each hexagon:")
for hex_name, vertices in HEXAGONS.items():
    print(f"  {hex_name}: {' + '.join(map(str, vertices))} = {sum(vertices)}")

print("\nSum by wuxing:")
for r in [1, 2, 3, 4, 5]:
    nodes = [n for n in range(1, 21) if residue_1based(n) == r]
    ph = RESIDUE_STYLE[r % 5]["name"]
    print(f"  {ph}({r}): sum={sum(nodes)}, numbers={nodes}")

print("\nWuxing distribution within each hexagon:")
for hex_name in HEXAGONS:
    vals = list(HEXAGONS[hex_name])
    counts = Counter(phase_of(v) for v in vals)
    print(f"  {hex_name}: {dict(counts)}")

print("\nNumber of hexagons sharing each vertex:")
for v in range(1, 21):
    print(f"  {v}({phase_of(v)}): {shared_count(v)} hexagons {VERTEX_TO_HEXAGONS[v]}")

betw_full = nx.betweenness_centrality(G_full)
print("\nBetweenness Centrality (Top 10):")
for n, v in sorted(betw_full.items(), key=lambda x: -x[1])[:10]:
    print(f"  {n}({phase_of(n)}): {v:.3f}")

# Wuxing edge classification
ph_edge_counts: dict[str, int] = {}
for u, v in G_full.edges():
    wu, wv = phase_of(u), phase_of(v)
    if wu == wv:
        key = "Same-phase"
    elif (wu, wv) in [
        ("Water", "Wood"),
        ("Wood", "Fire"),
        ("Fire", "Earth"),
        ("Earth", "Metal"),
        ("Metal", "Water"),
    ] or (wv, wu) in [
        ("Water", "Wood"),
        ("Wood", "Fire"),
        ("Fire", "Earth"),
        ("Earth", "Metal"),
        ("Metal", "Water"),
    ]:
        key = "Generation"
    elif (wu, wv) in [
        ("Water", "Fire"),
        ("Fire", "Metal"),
        ("Metal", "Wood"),
        ("Wood", "Earth"),
        ("Earth", "Water"),
    ] or (wv, wu) in [
        ("Water", "Fire"),
        ("Fire", "Metal"),
        ("Metal", "Wood"),
        ("Wood", "Earth"),
        ("Earth", "Water"),
    ]:
        key = "Overcoming"
    else:
        key = "Neutral"
    ph_edge_counts[key] = ph_edge_counts.get(key, 0) + 1

print("\nWuxing edge distribution:")
for key, cnt in ph_edge_counts.items():
    print(f"  {key}: {cnt}")

# Cycle basis
hex_cycles = {
    hex_name: list(vertices) for hex_name, vertices in HEXAGONS.items()
}
print("\n6-Cycle of each hexagon:")
for hex_name, cycle in hex_cycles.items():
    print(f"  {hex_name}: {' → '.join(map(str, cycle + [cycle[0]]))}")

# ============================================================
# 4. Position-based analysis (shared vertices vs. unique vertices)
# ============================================================

SHARED_VALUES = [v for v in range(1, 21) if shared_count(v) > 1]
UNIQUE_VALUES = [v for v in range(1, 21) if shared_count(v) == 1]

print("\nShared vertices:", sorted(SHARED_VALUES))
print("Unique vertices:", sorted(UNIQUE_VALUES))

# ============================================================
# 5. Generalized family
# ============================================================

# mod 5 residue class sums: 34, 38, 42, 46, 50 (common difference 4)
FAMILY_RESIDUE = [(m0, 34 + (m0 - 1) * 4) for m0 in range(1, 6)]
print("\nGeneralization of mod 5 residue class sums:")
for m0, total in FAMILY_RESIDUE:
    ph = RESIDUE_STYLE[m0 % 5]["name"]
    print(f"  M0={m0}({ph}): class sum={total}")

# ============================================================
# 6. Visualization helpers
# ============================================================


def draw_hexagon_boundaries(ax: Axes, labels: bool = True) -> None:
    fills = ("#F8F8F8", "#FBFBFB", "#F6F6F6", "#FAFAFA", "#F7F7F7")
    for (hex_name, vertices), fill in zip(HEXAGONS.items(), fills):
        polygon_points = [POSITIONS[number] for number in vertices]
        ax.add_patch(
            Polygon(
                polygon_points,
                closed=True,
                facecolor=fill,
                edgecolor="#777777",
                linewidth=1.5,
                linestyle=(0, (4, 4)),
                zorder=0,
            )
        )
        if labels:
            center_x = sum(point[0] for point in polygon_points) / 6
            center_y = sum(point[1] for point in polygon_points) / 6
            ax.text(
                center_x,
                center_y,
                f"{hex_name}\nΣ={TARGET_SUM}",
                ha="center",
                va="center",
                fontsize=9,
                color="#555555",
                zorder=1,
            )


def draw_edges(ax: Axes, color: str = "#303030", alpha: float = 1.0, lw: float = 2.0) -> None:
    for start, end in FULL_EDGES:
        x1, y1 = POSITIONS[start]
        x2, y2 = POSITIONS[end]
        ax.plot(
            [x1, x2],
            [y1, y2],
            color=color,
            linewidth=lw,
            alpha=alpha,
            solid_capstyle="round",
            zorder=1,
        )


def draw_nodes(
    ax: Axes,
    highlight_values: set[int] | None = None,
    dim_others: bool = False,
    node_radius: float = 0.28,
) -> None:
    for value, (x, y) in POSITIONS.items():
        r = value % 5
        style = RESIDUE_STYLE[r]
        color = style["face"]
        edge = style["edge"]
        lw = 2.0
        text_color = style["text"]
        z_node = 2
        z_text = 3
        fs = 10

        if highlight_values is not None:
            if value in highlight_values:
                z_node = 4
                z_text = 5
                fs = 11
                lw = 3.0
            else:
                if dim_others:
                    color = "#F0F0F0"
                    edge = "#CCCCCC"
                    text_color = "#AAAAAA"
                    lw = 1.0
                    fs = 8
                    z_node = 1
                    z_text = 2

        ax.add_patch(
            Circle(
                (x, y),
                node_radius,
                facecolor=color,
                edgecolor=edge,
                linewidth=lw,
                zorder=z_node,
            )
        )
        ax.text(
            x,
            y,
            str(value),
            ha="center",
            va="center",
            fontsize=fs,
            fontweight="bold" if highlight_values and value in highlight_values else "normal",
            color=text_color,
            zorder=z_text,
        )


def set_ax_lims(ax: Axes) -> None:
    ax.set_xlim(-3.7, 1.7)
    ax.set_ylim(-3.2, 5.2)
    ax.set_aspect("equal")
    ax.axis("off")


# ============================================================
# 7. Visualizations
# ============================================================

# --- 01: Original graph ---
fig, ax = plt.subplots(figsize=(12, 11))
draw_hexagon_boundaries(ax)
for start, end in FULL_EDGES:
    x1, y1 = POSITIONS[start]
    x2, y2 = POSITIONS[end]
    hex_start = VERTEX_TO_HEXAGONS[start][0]
    hex_end = VERTEX_TO_HEXAGONS[end][0]
    if hex_start == hex_end:
        ax.plot([x1, x2], [y1, y2], color=HEXAGON_COLORS[hex_start], linewidth=2.5, alpha=0.7, zorder=1)
    else:
        ax.plot([x1, x2], [y1, y2], color="#333333", linewidth=1.8, alpha=0.5, zorder=1)
draw_nodes(ax)
ax.set_title(
    f"{HANJA_TITLE} ({TITLE}) — Original honeycomb intersection structure\n"
    "5 hexagons · 6 numbers each · each hexagon sum 63 · total sum 210",
    fontsize=16,
    fontweight="bold",
)
set_ax_lims(ax)
legend_elements = [
    mpatches.Patch(facecolor=PHASE_COLOR[ph], edgecolor="black", label=f"{ph}")
    for ph in ["Water", "Fire", "Wood", "Metal", "Earth"]
]
ax.legend(handles=legend_elements, loc="lower right", fontsize=10, framealpha=0.9)
save_fig("01_original_graph.png")
plt.close()

# --- 02: Wuxing subgroup decomposition ---
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()
ax = axes[0]
draw_hexagon_boundaries(ax, labels=False)
draw_edges(ax, color="#CCCCCC", alpha=0.5, lw=1)
draw_nodes(ax)
ax.set_title("Full graph", fontsize=13, fontweight="bold")
set_ax_lims(ax)

for idx, ph in enumerate(["Water", "Fire", "Wood", "Metal", "Earth"]):
    ax = axes[idx + 1]
    draw_hexagon_boundaries(ax, labels=False)
    ph_nodes = [n for n in range(1, 21) if phase_of(n) == ph]
    other_nodes = [n for n in range(1, 21) if n not in ph_nodes]

    draw_edges(ax, color="#EEEEEE", alpha=0.4, lw=1)

    for n in other_nodes:
        x, y = POSITIONS[n]
        ax.add_patch(
            Circle(
                (x, y),
                0.22,
                facecolor="#F0F0F0",
                edgecolor="#CCCCCC",
                linewidth=1,
                zorder=1,
            )
        )
        ax.text(x, y, str(n), ha="center", va="center", fontsize=8, color="#AAAAAA", zorder=2)

    for n in ph_nodes:
        x, y = POSITIONS[n]
        ax.add_patch(
            Circle(
                (x, y),
                0.34,
                facecolor=PHASE_COLOR[ph],
                edgecolor="black",
                linewidth=2.5,
                zorder=2,
            )
        )
        ax.text(
            x,
            y,
            str(n),
            ha="center",
            va="center",
            fontsize=10,
            fontweight="bold",
            color="white" if ph in ["Water", "Wood"] else "black",
            zorder=3,
        )

    ax.set_title(
        f"{ph} · sum {sum(ph_nodes)}",
        fontsize=12,
        fontweight="bold",
        color=PHASE_COLOR[ph],
    )
    set_ax_lims(ax)

plt.suptitle("Wuxing (five-phase) subgroup decomposition", fontsize=16, fontweight="bold", y=1.02)
plt.tight_layout()
save_fig("02_wuxing_decomposition.png")
plt.close()

# --- 03: Adjacency matrix + spectrum ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
adj = nx.adjacency_matrix(G_full, nodelist=sorted(G_full.nodes())).todense()
im = ax.imshow(adj, cmap="YlOrRd", interpolation="nearest")
ax.set_xticks(range(20))
ax.set_yticks(range(20))
ax.set_xticklabels(sorted(G_full.nodes()), fontsize=8)
ax.set_yticklabels(sorted(G_full.nodes()), fontsize=8)
ph_sorted = [phase_of(n) for n in sorted(G_full.nodes())]
boundaries = [i - 0.5 for i in range(1, 20) if ph_sorted[i] != ph_sorted[i - 1]]
for b in boundaries:
    ax.axhline(y=b, color="blue", linewidth=1.5, alpha=0.7)
    ax.axvline(x=b, color="blue", linewidth=1.5, alpha=0.7)
plt.colorbar(im, ax=ax, shrink=0.8)
ax.set_title("Adjacency Matrix (hexagon graph)", fontsize=13, fontweight="bold")

ax = axes[1]
eigenvalues = np.linalg.eigvalsh(adj)
ax.bar(
    range(len(eigenvalues)),
    sorted(eigenvalues, reverse=True),
    color="#4488CC",
    edgecolor="black",
    alpha=0.8,
)
ax.axhline(y=0, color="red", linestyle="--", linewidth=1)
ax.set_xlabel("Index", fontsize=11)
ax.set_ylabel("Eigenvalue", fontsize=11)
ax.set_title(
    f"Graph Spectrum\nλ_max={max(eigenvalues):.2f}, λ_min={min(eigenvalues):.2f}",
    fontsize=13,
    fontweight="bold",
)
ax.grid(True, alpha=0.3)
plt.tight_layout()
save_fig("03_adjacency_spectrum.png")
plt.close()

# --- 04: Cycle analysis ---
fig, axes = plt.subplots(2, 2, figsize=(16, 14))

ax = axes[0, 0]
draw_hexagon_boundaries(ax, labels=False)
for start, end in FULL_EDGES:
    x1, y1 = POSITIONS[start]
    x2, y2 = POSITIONS[end]
    hex_start = VERTEX_TO_HEXAGONS[start][0]
    ax.plot([x1, x2], [y1, y2], color=HEXAGON_COLORS[hex_start], linewidth=3, alpha=0.8, zorder=1)
draw_nodes(ax)
ax.set_title("6-Cycles of the 5 hexagons", fontsize=13, fontweight="bold")
set_ax_lims(ax)

ax = axes[0, 1]
# Highlight the center hexagon
central_cycle = list(HEXAGONS["center"])
central_edges = [(central_cycle[i], central_cycle[(i + 1) % 6]) for i in range(6)]
draw_hexagon_boundaries(ax, labels=False)
for start, end in FULL_EDGES:
    x1, y1 = POSITIONS[start]
    x2, y2 = POSITIONS[end]
    if (start, end) in central_edges or (end, start) in central_edges:
        ax.plot([x1, x2], [y1, y2], color="red", linewidth=3.5, alpha=0.9, zorder=2)
    else:
        ax.plot([x1, x2], [y1, y2], color="#DDDDDD", linewidth=1, alpha=0.4, zorder=0)
for n in central_cycle:
    x, y = POSITIONS[n]
    ax.add_patch(
        Circle(
            (x, y),
            0.34,
            facecolor="#FFCCCC",
            edgecolor="red",
            linewidth=3,
            zorder=2,
        )
    )
    ax.text(x, y, str(n), ha="center", va="center", fontsize=10, fontweight="bold", zorder=3)
for n in range(1, 21):
    if n in central_cycle:
        continue
    x, y = POSITIONS[n]
    ax.add_patch(
        Circle(
            (x, y),
            0.26,
            facecolor="white",
            edgecolor="#999999",
            linewidth=1.2,
            zorder=1,
        )
    )
    ax.text(x, y, str(n), ha="center", va="center", fontsize=8, zorder=2)
ax.set_title(f"Center hexagon 6-Cycle: {' → '.join(map(str, central_cycle + [central_cycle[0]]))}", fontsize=13, fontweight="bold")
set_ax_lims(ax)

ax = axes[1, 0]
hex_names = list(HEXAGONS.keys())
hex_sums = [sum(HEXAGONS[h]) for h in hex_names]
hex_bar_colors = [HEXAGON_COLORS[h] for h in hex_names]
ax.bar(hex_names, hex_sums, color=hex_bar_colors, edgecolor="black", linewidth=1.5)
ax.axhline(y=TARGET_SUM, color="red", linestyle="--", linewidth=2)
ax.set_title("Six-number sum of each hexagon", fontsize=13, fontweight="bold")
for bar, val in zip(ax.patches, hex_sums):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.3,
        str(val),
        ha="center",
        fontsize=12,
        fontweight="bold",
    )

ax = axes[1, 1]
# Cycle length distribution
cycle_lengths = [len(c) for c in nx.cycle_basis(G_full)]
hist, bins = np.histogram(cycle_lengths, bins=[5.5, 6.5, 7.5, 8.5, 9.5, 10.5])
ax.bar(["6", "7", "8", "9", "10"], hist, color="#44AA44", edgecolor="black")
ax.set_title(f"Cycle-basis length distribution\n{len(cycle_lengths)} basis cycles total", fontsize=13, fontweight="bold")
ax.set_xlabel("Cycle length", fontsize=10)
ax.set_ylabel("Count", fontsize=10)

plt.tight_layout()
save_fig("04_cycle_analysis.png")
plt.close()

# --- 05: Centrality + sum invariants ---
fig, axes = plt.subplots(2, 2, figsize=(16, 14))

ax = axes[0, 0]
degrees = dict(G_full.degree())
nodes_sorted = sorted(G_full.nodes(), key=lambda n: degrees[n], reverse=True)
colors_sorted = [PHASE_COLOR[phase_of(n)] for n in nodes_sorted]
ax.bar(range(20), [degrees[n] for n in nodes_sorted], color=colors_sorted, edgecolor="black")
ax.set_xticks(range(20))
ax.set_xticklabels([str(n) for n in nodes_sorted], fontsize=8)
ax.set_title("Degree (hexagon graph)", fontsize=12, fontweight="bold")
ax.set_ylabel("Degree", fontsize=10)

ax = axes[0, 1]
betw_sorted = sorted(G_full.nodes(), key=lambda n: betw_full[n], reverse=True)
colors_b = [PHASE_COLOR[phase_of(n)] for n in betw_sorted]
ax.bar(range(20), [betw_full[n] for n in betw_sorted], color=colors_b, edgecolor="black")
ax.set_xticks(range(20))
ax.set_xticklabels([str(n) for n in betw_sorted], fontsize=8)
ax.set_title("Betweenness Centrality", fontsize=12, fontweight="bold")
ax.set_ylabel("Centrality", fontsize=10)

ax = axes[1, 0]
ph_sums = {ph: sum([n for n in range(1, 21) if phase_of(n) == ph]) for ph in ["Water", "Fire", "Wood", "Metal", "Earth"]}
ph_names = list(ph_sums.keys())
ph_vals = list(ph_sums.values())
ph_colors_bar = [PHASE_COLOR[w] for w in ph_names]
ax.bar(ph_names, ph_vals, color=ph_colors_bar, edgecolor="black", linewidth=1.5)
ax.set_title("Sum by wuxing (34, 38, 42, 46, 50)", fontsize=12, fontweight="bold")
for bar, val in zip(ax.patches, ph_vals):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        str(val),
        ha="center",
        fontsize=12,
        fontweight="bold",
    )
ax.plot(range(5), ph_vals, "o--", color="black", alpha=0.5, linewidth=2)

ax = axes[1, 1]
components = {
    "upper-left": sum(HEXAGONS["upper-left"]),
    "upper-right": sum(HEXAGONS["upper-right"]),
    "center": sum(HEXAGONS["center"]),
    "lower-left": sum(HEXAGONS["lower-left"]),
    "lower-right": sum(HEXAGONS["lower-right"]),
    "total": sum(range(1, 21)),
}
ax.bar(
    list(components.keys()),
    list(components.values()),
    color=[HEXAGON_COLORS[k] for k in list(components.keys())[:-1]] + ["#333333"],
    edgecolor="black",
    linewidth=1.5,
)
ax.set_title("Sum by structural subset", fontsize=12, fontweight="bold")
ax.set_ylabel("Sum", fontsize=10)
plt.setp(ax.xaxis.get_majorticklabels(), rotation=15, ha="right")

plt.tight_layout()
save_fig("05_centrality_invariants.png")
plt.close()

# --- 06: Wuxing generation/overcoming ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
phase_graph = nx.DiGraph()
phase_relations = [
    ("Water", "Wood", "Generation"),
    ("Wood", "Fire", "Generation"),
    ("Fire", "Earth", "Generation"),
    ("Earth", "Metal", "Generation"),
    ("Metal", "Water", "Generation"),
    ("Water", "Fire", "Overcoming"),
    ("Fire", "Metal", "Overcoming"),
    ("Metal", "Wood", "Overcoming"),
    ("Wood", "Earth", "Overcoming"),
    ("Earth", "Water", "Overcoming"),
]
for u, v, r in phase_relations:
    phase_graph.add_edge(u, v, relation=r)
ph_pos = {"Water": (0, 2), "Wood": (2, 1), "Fire": (1, -1), "Earth": (-1, -1), "Metal": (-2, 1)}
generation_edges = [(u, v) for u, v, r in phase_relations if r == "Generation"]
overcoming_edges = [(u, v) for u, v, r in phase_relations if r == "Overcoming"]
nx.draw_networkx_edges(
    phase_graph,
    ph_pos,
    edgelist=generation_edges,
    edge_color="#44AA44",
    width=3,
    alpha=0.8,
    arrows=True,
    arrowsize=20,
    connectionstyle="arc3,rad=0.15",
    ax=ax,
)
nx.draw_networkx_edges(
    phase_graph,
    ph_pos,
    edgelist=overcoming_edges,
    edge_color="#CC4444",
    width=2,
    alpha=0.6,
    style="--",
    arrows=True,
    arrowsize=15,
    connectionstyle="arc3,rad=-0.15",
    ax=ax,
)
ph_node_colors = [PHASE_COLOR[w] for w in phase_graph.nodes()]
nx.draw_networkx_nodes(
    phase_graph,
    ph_pos,
    node_color=ph_node_colors,
    node_size=3000,
    edgecolors="black",
    linewidths=2.5,
    ax=ax,
)
nx.draw_networkx_labels(phase_graph, ph_pos, font_size=14, font_weight="normal", ax=ax)
legend_elements = [
    Line2D([0], [0], color="#44AA44", lw=3, label="Generation"),
    Line2D([0], [0], color="#CC4444", lw=2, linestyle="--", label="Overcoming"),
]
ax.legend(handles=legend_elements, loc="upper right", fontsize=11)
ax.set_title("Wuxing generation/overcoming relation diagram", fontsize=13, fontweight="bold")
ax.set_xlim(-3, 3.5)
ax.set_ylim(-2.5, 3)
ax.axis("off")

ax = axes[1]
colors_pie = ["#44AA44", "#CC4444", "#CC9944", "#4488CC"]
ax.pie(
    list(ph_edge_counts.values()),
    labels=list(ph_edge_counts.keys()),
    autopct="%1.0f%%",
    colors=colors_pie[: len(ph_edge_counts)],
    explode=[0.05] * len(ph_edge_counts),
    textprops={"fontsize": 12, "fontweight": "bold"},
)
ax.set_title(f"Wuxing edge distribution (N={G_full.number_of_edges()})", fontsize=13, fontweight="bold")
plt.tight_layout()
save_fig("06_wuxing_relations.png")
plt.close()

# --- 07: Extension and generalization ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

ax = axes[0]
m0_labels = [f"M0={m0}" for m0, _ in FAMILY_RESIDUE]
m0_values = [total for _, total in FAMILY_RESIDUE]
m0_colors = [PHASE_COLOR[RESIDUE_STYLE[m0 % 5]["name"]] for m0, _ in FAMILY_RESIDUE]
ax.bar(m0_labels, m0_values, color=m0_colors, edgecolor="black", linewidth=1.5)
ax.set_title("Arithmetic progression of mod 5 residue-class sums\nM(n+1) = M(n) + 4", fontsize=13, fontweight="bold")
for bar, val in zip(ax.patches, m0_values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        str(val),
        ha="center",
        fontsize=12,
        fontweight="bold",
    )
ax.plot(range(5), m0_values, "o--", color="black", alpha=0.5, linewidth=2)
ax.set_ylabel("Residue-class sum", fontsize=10)

ax = axes[1]
n_layers = 3
theta = np.linspace(0, 2 * np.pi, n_layers + 1)[:-1]
for i, t in enumerate(theta):
    r = 2.5 + i * 1.5
    circle = plt.Circle((0, 0), r, fill=False, color=["#CC4444", "#4488CC", "#44AA44"][i], linewidth=2, linestyle="--")
    ax.add_patch(circle)
    ax.text(r * np.cos(np.pi / 4), r * np.sin(np.pi / 4), f"{20 * (i + 1)} nodes", fontsize=10, fontweight="bold")
ax.add_patch(plt.Circle((0, 0), 0.5, facecolor="#CC9944", edgecolor="black", linewidth=2))
ax.text(0, 0, "CORE\n20", ha="center", va="center", fontsize=10, fontweight="bold")
ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("Concentric extension: 20k-node structure", fontsize=13, fontweight="bold")

plt.tight_layout()
save_fig("07_local_extensions.png")
plt.close()

# --- 08: Position patterns (shared vertices vs. unique vertices) ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

ax = axes[0]
draw_hexagon_boundaries(ax, labels=False)
for n in SHARED_VALUES:
    x, y = POSITIONS[n]
    ax.add_patch(
        Circle(
            (x, y),
            0.34,
            facecolor="#FFCCCC",
            edgecolor="red",
            linewidth=3,
            zorder=2,
        )
    )
    ax.text(x, y, str(n), ha="center", va="center", fontsize=10, fontweight="bold", zorder=3)
for n in UNIQUE_VALUES:
    x, y = POSITIONS[n]
    ax.add_patch(
        Circle(
            (x, y),
            0.28,
            facecolor="#E8F4FF",
            edgecolor="#4488CC",
            linewidth=2,
            zorder=1,
        )
    )
    ax.text(x, y, str(n), ha="center", va="center", fontsize=9, zorder=2)
draw_edges(ax, color="#303030", alpha=0.3, lw=1.5)
ax.set_title("Shared vertices (red) vs. unique vertices (blue)", fontsize=13, fontweight="bold")
set_ax_lims(ax)

ax = axes[1]
share_counts = [shared_count(v) for v in range(1, 21)]
colors_sc = [PHASE_COLOR[phase_of(v)] for v in range(1, 21)]
ax.bar(range(1, 21), share_counts, color=colors_sc, edgecolor="black")
ax.set_xticks(range(1, 21))
ax.set_xticklabels([str(n) for n in range(1, 21)], fontsize=8)
ax.set_title("Number of hexagons sharing each vertex", fontsize=13, fontweight="bold")
ax.set_ylabel("Shared hexagons", fontsize=10)
ax.set_xlabel("Value", fontsize=10)

plt.tight_layout()
save_fig("08_position_patterns.png")
plt.close()

# ============================================================
# 8. Basic visualization (same as the original analyze_basic.py)
# ============================================================


def draw_basic(
    png_output: str | Path = "jisu_yong_yukdo.png",
    svg_output: str | Path = "jisu_yong_yukdo.svg",
) -> None:
    font = find_cjk_font()

    fig = plt.figure(figsize=(12.5, 9.0), dpi=220)
    graph_ax = fig.add_axes([0.04, 0.07, 0.63, 0.86])
    legend_ax = fig.add_axes([0.71, 0.08, 0.26, 0.84])

    graph_ax.set_aspect("equal")
    graph_ax.set_xlim(-3.7, 1.7)
    graph_ax.set_ylim(-3.2, 5.2)
    graph_ax.axis("off")

    # Hexagon regions
    fills = ("#F8F8F8", "#FBFBFB", "#F6F6F6", "#FAFAFA", "#F7F7F7")
    for (name, vertices), fill in zip(HEXAGONS.items(), fills):
        polygon_points = [POSITIONS[number] for number in vertices]
        graph_ax.add_patch(
            Polygon(
                polygon_points,
                closed=True,
                facecolor=fill,
                edgecolor="#A8A8A8",
                linewidth=1.1,
                linestyle=(0, (4, 4)),
                zorder=0,
            )
        )
        center_x = sum(point[0] for point in polygon_points) / 6
        center_y = sum(point[1] for point in polygon_points) / 6
        graph_ax.text(
            center_x,
            center_y,
            "sum 63",
            ha="center",
            va="center",
            fontsize=9.5,
            color="#9A9A9A",
            zorder=1,
        )

    # Edges
    for start, end in FULL_EDGES:
        x1, y1 = POSITIONS[start]
        x2, y2 = POSITIONS[end]
        graph_ax.plot(
            [x1, x2],
            [y1, y2],
            color="#303030",
            linewidth=2.0,
            solid_capstyle="round",
            zorder=2,
        )

    # Nodes
    radius = 0.28
    for number, (x, y) in POSITIONS.items():
        residue = number % 5
        style = RESIDUE_STYLE[residue]
        graph_ax.add_patch(
            Circle(
                (x, y),
                radius,
                facecolor=style["face"],
                edgecolor=style["edge"],
                linewidth=2.0,
                zorder=3,
            )
        )
        graph_ax.text(
            x,
            y,
            str(number),
            ha="center",
            va="center",
            fontproperties=font,
            fontsize=12,
            color=style["text"],
            zorder=4,
        )

    # Legend
    legend_ax.axis("off")
    legend_ax.text(
        0.0,
        0.98,
        f"{TITLE} ({HANJA_TITLE})",
        transform=legend_ax.transAxes,
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=17,
        weight="bold",
    )
    legend_ax.text(
        0.0,
        0.92,
        SUBTITLE,
        transform=legend_ax.transAxes,
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=13,
    )

    y = 0.84
    summary = (
        "Vertices: 1–20, each once",
        "Hexagons: 5",
        "Each hexagon: 6 vertices",
        "Each hexagon sum: 63",
        "Total vertex usages across hexagons: 30",
    )
    for line in summary:
        legend_ax.text(
            0.0,
            y,
            f"• {line}",
            transform=legend_ax.transAxes,
            ha="left",
            va="top",
            fontproperties=font,
            fontsize=11,
        )
        y -= 0.053

    y -= 0.02
    legend_ax.text(
        0.0,
        y,
        "mod 5 residue groups",
        transform=legend_ax.transAxes,
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=14,
        weight="bold",
    )
    y -= 0.08
    for residue in (1, 2, 3, 4, 0):
        style = RESIDUE_STYLE[residue]
        group = [n for n in range(1, 21) if n % 5 == residue]
        legend_ax.add_patch(
            Circle(
                (0.04, y + 0.012),
                0.023,
                transform=legend_ax.transAxes,
                facecolor=style["face"],
                edgecolor=style["edge"],
                linewidth=1.5,
            )
        )
        legend_ax.text(
            0.09,
            y + 0.012,
            f"{style['label']} · 4",
            transform=legend_ax.transAxes,
            ha="left",
            va="center",
            fontproperties=font,
            fontsize=10.8,
            weight="bold",
            color=style["text"],
        )
        legend_ax.text(
            0.09,
            y - 0.026,
            "{ " + ", ".join(str(number) for number in group) + " }",
            transform=legend_ax.transAxes,
            ha="left",
            va="top",
            fontproperties=font,
            fontsize=10,
            color="#333333",
        )
        y -= 0.10

    y -= 0.005
    legend_ax.text(
        0.0,
        y,
        "Verification by hexagon",
        transform=legend_ax.transAxes,
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=14,
        weight="bold",
    )
    y -= 0.065
    for name, vertices in HEXAGONS.items():
        expression = " + ".join(str(number) for number in vertices)
        legend_ax.text(
            0.0,
            y,
            f"{name}: {expression} = 63",
            transform=legend_ax.transAxes,
            ha="left",
            va="top",
            fontproperties=font,
            fontsize=9.7,
        )
        y -= 0.052

    graph_ax.set_title(
        f"{TITLE} ({HANJA_TITLE})",
        fontproperties=font,
        fontsize=18,
        pad=18,
    )

    fig.savefig(
        png_output,
        dpi=300,
        bbox_inches="tight",
        pad_inches=0.12,
        facecolor="white",
    )
    fig.savefig(
        svg_output,
        bbox_inches="tight",
        pad_inches=0.12,
        facecolor="white",
    )
    plt.close(fig)
    print(f"[Saved] {png_output}")
    print(f"[Saved] {svg_output}")


draw_basic()

# ============================================================
# 9. Report generation
# ============================================================

degrees = dict(G_full.degree())
betw_full = nx.betweenness_centrality(G_full)
adj = nx.adjacency_matrix(G_full, nodelist=sorted(G_full.nodes())).todense()
eigenvalues = np.linalg.eigvalsh(adj)

report_md = f"""# In-Depth Analysis Report: Jisu-yong-yukdo ({HANJA_TITLE} / Six-Each-Gets)

## 1. Overview

Jisu-yong-yukdo places the natural numbers 1 through 20 into five hexagons of six numbers each.
Adjacent hexagons share vertices and edges, and every hexagon has the same six-number sum 63.

- **Vertices**: 20 (1–20, each once)
- **Hexagons**: 5
- **Edges**: {G_full.number_of_edges()}
- **Connected components**: {nx.number_connected_components(G_full)}
- **Hexagon sum**: {TARGET_SUM}
- **Total sum**: {sum(range(1, 21))}
- **Duplicated total (5×63)**: {TARGET_SUM * len(HEXAGONS)}

## 2. Hexagon Data

| Hexagon | Six vertices | Sum |
|---|---|---|
| upper-left | {' + '.join(map(str, HEXAGONS['upper-left']))} | {sum(HEXAGONS['upper-left'])} |
| upper-right | {' + '.join(map(str, HEXAGONS['upper-right']))} | {sum(HEXAGONS['upper-right'])} |
| center | {' + '.join(map(str, HEXAGONS['center']))} | {sum(HEXAGONS['center'])} |
| lower-left | {' + '.join(map(str, HEXAGONS['lower-left']))} | {sum(HEXAGONS['lower-left'])} |
| lower-right | {' + '.join(map(str, HEXAGONS['lower-right']))} | {sum(HEXAGONS['lower-right'])} |

## 3. Wuxing (Five Phases) Analysis

Classification by `n mod 5` (0 is treated as 5):

| Wuxing | Residue | Numbers | Sum |
|---|---|---|---|
| Water | 1 | {', '.join(map(str, [n for n in range(1, 21) if n % 5 == 1]))} | {sum([n for n in range(1, 21) if n % 5 == 1])} |
| Fire | 2 | {', '.join(map(str, [n for n in range(1, 21) if n % 5 == 2]))} | {sum([n for n in range(1, 21) if n % 5 == 2])} |
| Wood | 3 | {', '.join(map(str, [n for n in range(1, 21) if n % 5 == 3]))} | {sum([n for n in range(1, 21) if n % 5 == 3])} |
| Metal | 4 | {', '.join(map(str, [n for n in range(1, 21) if n % 5 == 4]))} | {sum([n for n in range(1, 21) if n % 5 == 4])} |
| Earth | 0 | {', '.join(map(str, [n for n in range(1, 21) if n % 5 == 0]))} | {sum([n for n in range(1, 21) if n % 5 == 0])} |

The wuxing sums 34, 38, 42, 46, 50 form an arithmetic progression with common difference 4.

## 4. Graph-Theoretic Indicators

- **Degree sequence**: {deg_seq_full}
- **Maximum degree**: {max(deg_seq_full)}
- **Minimum degree**: {min(deg_seq_full)}
- **Top 5 Betweenness Centrality**:
{chr(10).join(f"  - {n}({phase_of(n)}): {v:.3f}" for n, v in sorted(betw_full.items(), key=lambda x: -x[1])[:5])}

## 5. Spectrum

- λ_max = {max(eigenvalues):.4f}
- λ_min = {min(eigenvalues):.4f}
- Eigenvalue range = {max(eigenvalues) - min(eigenvalues):.4f}

## 6. Cycle Structure

Each hexagon forms a 6-cycle.

{chr(10).join(f"- **{name}**: {' → '.join(map(str, cycle + [cycle[0]]))}" for name, cycle in hex_cycles.items())}

## 7. Position Patterns

- **Shared vertices** (belong to 2 or more hexagons): {sorted(SHARED_VALUES)}
- **Unique vertices** (belong to 1 hexagon): {sorted(UNIQUE_VALUES)}

Shared vertices act as junctions between hexagons and strongly influence connectivity and centrality.

## 8. Wuxing Edge Distribution

| Classification | Count |
|---|---|
{chr(10).join(f"| {key} | {cnt} |" for key, cnt in ph_edge_counts.items())}

## 9. Generalization

Arithmetic progression of mod 5 residue-class sums:

| M0 | Wuxing | Class sum |
|---|---|---|
{chr(10).join(f"| {m0} | {RESIDUE_STYLE[m0 % 5]['name']} | {total} |" for m0, total in FAMILY_RESIDUE)}

## 10. Generated Outputs

- `01_original_graph.png`
- `02_wuxing_decomposition.png`
- `03_adjacency_spectrum.png`
- `04_cycle_analysis.png`
- `05_centrality_invariants.png`
- `06_wuxing_relations.png`
- `07_local_extensions.png`
- `08_position_patterns.png`
- `jisu_yong_yukdo.png` / `jisu_yong_yukdo.svg`
- `analysis_report.md`
- `blog.md`
"""

force = "--force" in sys.argv

report_path = Path(f"{OUTPUT_DIR}/analysis_report.md")
if force or not report_path.exists():
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_md)
    print("[Saved] analysis_report.md")
else:
    print("[SKIP] analysis_report.md already exists (use --force to regenerate)")

blog_md = f"""# Deep Dive into Jisu-yong-yukdo ({HANJA_TITLE})

Jisu-yong-yukdo is a traditional mathematical puzzle from the *Gusuryak* family, placing the numbers 1 through 20 into five hexagons so that each hexagon sums to 63.

## Core Structure

- 5 hexagons: upper-left, upper-right, center, lower-left, lower-right
- 6 vertices per hexagon, sum 63
- 20 vertices and {G_full.number_of_edges()} edges in total
- Adjacent hexagons share vertices and edges

## Wuxing Classification

Classifying by `n mod 5` splits the numbers into Water, Fire, Wood, Metal, and Earth, with exactly 4 numbers in each class.
The wuxing sums 34, 38, 42, 46, 50 form an arithmetic progression with common difference 4.

## Graph-Theoretic View

Treating hexagon sides as graph edges, Jisu-yong-yukdo becomes a planar graph with 20 nodes and {G_full.number_of_edges()} edges.
Each hexagon is a 6-cycle, and the five cycles are intertwined through shared vertices.

## Sum Invariant

The rule that every hexagon sums to 63 is the core of the puzzle.
Counting shared vertices with multiplicity, the five hexagons contribute `63 × 5 = 315`, which exceeds the total 1–20 sum 210 by 105.
That 105 is the result of shared vertices being counted multiple times.

## Visualizations

The eight images in the same directory (`01_original_graph.png` through `08_position_patterns.png`) show
original structure, wuxing decomposition, spectrum, cycles, centrality, generation/overcoming relations,
extension, and position patterns from a modern mathematical viewpoint.
"""

blog_path = Path(f"{OUTPUT_DIR}/blog.md")
if force or not blog_path.exists():
    with open(blog_path, "w", encoding="utf-8") as f:
        f.write(blog_md)
    print("[Saved] blog.md")
else:
    print("[SKIP] blog.md already exists (use --force to regenerate)")

print("\n" + "=" * 60)
print("All images and reports generated successfully!")
print(f"Output directory: {OUTPUT_DIR}/")
print("=" * 60)
