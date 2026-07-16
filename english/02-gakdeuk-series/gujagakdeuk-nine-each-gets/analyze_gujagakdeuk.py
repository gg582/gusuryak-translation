#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gujagakdeuk — Modern graph and combinatorial deep analysis

A reinterpretation of Gujagakdeuk (九子各得), one of the diagrams in the
Gusuryak (九數略) series, in modern mathematical language.

Analysis target: a cross structure arranging the numbers 1 through 45 into
5 palaces with 9 numbers each.
"""

import os
from collections import Counter

import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.lines import Line2D

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


def save_fig(name):
    path = f"{OUTPUT_DIR}/{name}"
    plt.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    print(f"[Saved] {path}")


# ============================================================
# 1. Source data structuring
# ============================================================

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

RESIDUE_STYLE = {
    1: {"face": "#E5E5E5", "edge": "#444444", "name": "Water"},
    2: {"face": "#F6D0D0", "edge": "#B54141", "name": "Fire"},
    3: {"face": "#D5E3FA", "edge": "#3D6DB3", "name": "Wood"},
    4: {"face": "#D7D7D7", "edge": "#1F1F1F", "name": "Metal"},
    0: {"face": "#F7E3A0", "edge": "#B58A00", "name": "Earth"},
}

PHASE_COLOR = {
    "Water": "#4488CC",
    "Fire": "#CC4444",
    "Wood": "#44AA44",
    "Metal": "#888888",
    "Earth": "#CC9944",
}


def phase_of(n: int) -> str:
    r = n % 5
    return RESIDUE_STYLE[r]["name"]


def residue_1based(n: int) -> int:
    r = n % 5
    return 5 if r == 0 else r


def build_positions() -> dict[int, tuple[float, float]]:
    positions: dict[int, tuple[float, float]] = {}
    for palace_name, grid in PALACES.items():
        origin_x, origin_y = PALACE_ORIGINS[palace_name]
        for row_index, row in enumerate(grid):
            for col_index, value in enumerate(row):
                x = origin_x + col_index
                y = origin_y + (2 - row_index)
                positions[value] = (x, y)
    return positions


POSITIONS = build_positions()


def palace_values(palace_name: str) -> list[int]:
    return [v for row in PALACES[palace_name] for v in row]


def palace_cells(palace_name: str) -> list[tuple[int, int, int]]:
    """List of (value, row, column) inside a palace."""
    cells = []
    for r, row in enumerate(PALACES[palace_name]):
        for c, value in enumerate(row):
            cells.append((value, r, c))
    return cells


def cell_role(row: int, col: int) -> str:
    if (row, col) == (1, 1):
        return "center"
    if (row, col) in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        return "corner"
    return "edge"


# ============================================================
# 2. Graph construction
# ============================================================

INTRA_EDGES: list[tuple[int, int]] = []
FULL_EDGES: list[tuple[int, int]] = []

# Adjacency edges inside the same palace (3×3 grid).
for palace_name, grid in PALACES.items():
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if c + 1 < 3:
                right = grid[r][c + 1]
                INTRA_EDGES.append(tuple(sorted((value, right))))
            if r + 1 < 3:
                down = grid[r + 1][c]
                INTRA_EDGES.append(tuple(sorted((value, down))))

# Adjacency edges of the full grid (crossing palace boundaries).
pos_to_value = {pos: value for value, pos in POSITIONS.items()}
for value, (x, y) in POSITIONS.items():
    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        neighbor_pos = (x + dx, y + dy)
        if neighbor_pos in pos_to_value:
            neighbor = pos_to_value[neighbor_pos]
            if neighbor > value:
                FULL_EDGES.append((value, neighbor))

G_intra = nx.Graph()
G_intra.add_edges_from(INTRA_EDGES)
for n in range(1, 46):
    G_intra.add_node(n)
    G_intra.nodes[n]["phase"] = phase_of(n)

G_full = nx.Graph()
G_full.add_edges_from(FULL_EDGES)
for n in range(1, 46):
    G_full.add_node(n)
    G_full.nodes[n]["phase"] = phase_of(n)


def value_to_palace(value: int) -> str:
    for palace_name, grid in PALACES.items():
        for row in grid:
            if value in row:
                return palace_name
    raise ValueError(value)


# ============================================================
# 3. Combinatorics and graph theory analysis
# ============================================================

def validate():
    all_values = [v for grid in PALACES.values() for row in grid for v in row]
    assert sorted(all_values) == list(range(1, 46)), "1~45 must each appear exactly once"
    assert sum(all_values) == 1035, "Total sum must be 1035"
    for palace_name, grid in PALACES.items():
        vals = [v for row in grid for v in row]
        assert len(vals) == 9, f"{palace_name} must have 9 numbers"
        assert sum(vals) == 207, f"{palace_name} sum must be 207"


validate()

print("=" * 60)
print("Gujagakdeuk — Modern graph and combinatorial analysis")
print("=" * 60)
print(f"Node count: {G_full.number_of_nodes()}")
print(f"Edge count (intra-palace only): {G_intra.number_of_edges()}")
print(f"Edge count (full grid): {G_full.number_of_edges()}")
print(f"Connected components (intra-palace only): {nx.number_connected_components(G_intra)}")
print(f"Connected components (full grid): {nx.number_connected_components(G_full)}")

deg_seq_intra = sorted([d for _, d in G_intra.degree()], reverse=True)
deg_seq_full = sorted([d for _, d in G_full.degree()], reverse=True)
print(f"Degree sequence (intra-palace only): {deg_seq_intra}")
print(f"Degree sequence (full grid): {deg_seq_full}")

print("\nSum by wuxing (five phases):")
for r in [1, 2, 3, 4, 5]:
    nodes = [n for n in range(1, 46) if residue_1based(n) == r]
    ph = RESIDUE_STYLE[r % 5]["name"]
    print(f"  {ph}({r}): sum={sum(nodes)}, numbers={nodes}")

print("\nWuxing distribution by palace:")
for palace_name in PALACES:
    vals = palace_values(palace_name)
    counts = Counter(phase_of(v) for v in vals)
    print(f"  {palace_name}: {dict(counts)}")

print("\nCenter value by palace:")
for palace_name in PALACES:
    center = [v for v, r, c in palace_cells(palace_name) if cell_role(r, c) == "center"][0]
    print(f"  {palace_name}: center={center}({phase_of(center)})")

betw_full = nx.betweenness_centrality(G_full)
print("\nBetweenness Centrality (Top 10):")
for n, v in sorted(betw_full.items(), key=lambda x: -x[1])[:10]:
    print(f"  {n}({phase_of(n)}): {v:.3f}")

try:
    girth = min(len(c) for c in nx.cycle_basis(G_full))
    print(f"\nGirth (minimum cycle length): {girth}")
except Exception:
    girth = None

# Wuxing edge classification output
ph_edge_counts = {}
for u, v in G_full.edges():
    wu, wv = phase_of(u), phase_of(v)
    if wu == wv:
        key = "same-phase"
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
        key = "generating"
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
        key = "overcoming"
    else:
        key = "neutral"
    ph_edge_counts[key] = ph_edge_counts.get(key, 0) + 1

print("\nWuxing edge distribution:")
for key, cnt in ph_edge_counts.items():
    print(f"  {key}: {cnt}")

# ============================================================
# 4. Position-based analysis (corner / edge midpoint / center)
# ============================================================

CORNER_SUMS: dict[str, int] = {}
EDGE_SUMS: dict[str, int] = {}
CENTER_VALUES: dict[str, int] = {}
for palace_name in PALACES:
    corner_vals = []
    edge_vals = []
    center_val = None
    for value, r, c in palace_cells(palace_name):
        role = cell_role(r, c)
        if role == "corner":
            corner_vals.append(value)
        elif role == "edge":
            edge_vals.append(value)
        else:
            center_val = value
    CORNER_SUMS[palace_name] = sum(corner_vals)
    EDGE_SUMS[palace_name] = sum(edge_vals)
    CENTER_VALUES[palace_name] = center_val  # type: ignore[assignment]

print("\nSum by position within palaces:")
for palace_name in PALACES:
    print(
        f"  {palace_name}: corner={CORNER_SUMS[palace_name]}, "
        f"edge midpoint={EDGE_SUMS[palace_name]}, center={CENTER_VALUES[palace_name]}"
    )

# ============================================================
# 5. Generalized family
# ============================================================

FAMILY = [(m0, 189 + (m0 - 1) * 9) for m0 in range(1, 6)]
print("\nM0 generalized family:")
for m0, total in FAMILY:
    ph = RESIDUE_STYLE[m0 % 5]["name"]
    print(f"  M0={m0}({ph}): palace sum={total}")

# ============================================================
# 6. Visualization
# ============================================================

PALACE_COLORS = {
    "Top": "#CC4444",
    "Left": "#4488CC",
    "Center": "#44AA44",
    "Right": "#CC9944",
    "Bottom": "#888888",
}


def draw_palace_boundaries(ax):
    for palace_name, origin in PALACE_ORIGINS.items():
        ox, oy = origin
        rect = plt.Rectangle(
            (ox - 0.52, oy - 0.52),
            3.04,
            3.04,
            fill=False,
            edgecolor="#777777",
            linewidth=1.5,
            linestyle=(0, (4, 4)),
            zorder=0,
        )
        ax.add_patch(rect)
        ax.text(
            ox + 1.0,
            oy + 2.7,
            f"{palace_name} · Σ=207",
            ha="center",
            va="bottom",
            fontsize=10,
            color="#333333",
        )


def draw_nodes(ax, highlight_palace=None, highlight_values=None, node_size=1000):
    for value, (x, y) in POSITIONS.items():
        palace = value_to_palace(value)
        if highlight_palace and palace != highlight_palace:
            continue
        r = value % 5
        style = RESIDUE_STYLE[r]
        color = style["face"]
        edge = style["edge"]
        lw = 2.5
        if highlight_values and value in highlight_values:
            edge = "red"
            lw = 3.5
        ax.add_patch(
            plt.Circle(
                (x, y),
                0.32,
                facecolor=color,
                edgecolor=edge,
                linewidth=lw,
                zorder=2,
            )
        )
        ax.text(
            x,
            y,
            str(value),
            ha="center",
            va="center",
            fontsize=10,
            fontweight="bold",
            zorder=3,
        )


# --- 01: Source graph ---
fig, ax = plt.subplots(figsize=(12, 12))
draw_palace_boundaries(ax)
for u, v in FULL_EDGES:
    x1, y1 = POSITIONS[u]
    x2, y2 = POSITIONS[v]
    palace_u = value_to_palace(u)
    palace_v = value_to_palace(v)
    if palace_u == palace_v:
        ax.plot([x1, x2], [y1, y2], color=PALACE_COLORS[palace_u], linewidth=2.5, alpha=0.7, zorder=1)
    else:
        ax.plot([x1, x2], [y1, y2], color="#333333", linewidth=1.8, alpha=0.5, zorder=1)
draw_nodes(ax)
ax.set_title(
    "Gujagakdeuk — Source cross structure\n5 palaces · 9 numbers · each palace sum 207 · total sum 1035",
    fontsize=16,
    fontweight="bold",
)
ax.set_xlim(-0.8, 8.8)
ax.set_ylim(-0.8, 8.8)
ax.set_aspect("equal")
ax.axis("off")
legend_elements = [
    mpatches.Patch(facecolor=PHASE_COLOR[ph], edgecolor="black", label=f"{ph}")
    for ph in ["Water", "Fire", "Wood", "Metal", "Earth"]
]
ax.legend(handles=legend_elements, loc="lower right", fontsize=10, framealpha=0.9)
save_fig("01_original_graph.png")
plt.close()

# --- 02: Wuxing subgraph decomposition ---
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()
ax = axes[0]
draw_palace_boundaries(ax)
for u, v in FULL_EDGES:
    x1, y1 = POSITIONS[u]
    x2, y2 = POSITIONS[v]
    ax.plot([x1, x2], [y1, y2], color="#CCCCCC", linewidth=1, alpha=0.5, zorder=0)
draw_nodes(ax)
ax.set_title("Full graph", fontsize=13, fontweight="bold")
ax.set_xlim(-0.8, 8.8)
ax.set_ylim(-0.8, 8.8)
ax.set_aspect("equal")
ax.axis("off")

for idx, ph in enumerate(["Water", "Fire", "Wood", "Metal", "Earth"]):
    ax = axes[idx + 1]
    draw_palace_boundaries(ax)
    ph_nodes = [n for n in range(1, 46) if phase_of(n) == ph]
    other_nodes = [n for n in range(1, 46) if n not in ph_nodes]

    for u, v in FULL_EDGES:
        x1, y1 = POSITIONS[u]
        x2, y2 = POSITIONS[v]
        ax.plot([x1, x2], [y1, y2], color="#EEEEEE", linewidth=1, alpha=0.4, zorder=0)

    for n in other_nodes:
        x, y = POSITIONS[n]
        ax.add_patch(
            plt.Circle(
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
            plt.Circle(
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
    ax.set_xlim(-0.8, 8.8)
    ax.set_ylim(-0.8, 8.8)
    ax.set_aspect("equal")
    ax.axis("off")

plt.suptitle("Wuxing (five phases) subgraph decomposition", fontsize=16, fontweight="bold", y=1.02)
plt.tight_layout()
save_fig("02_wuxing_decomposition.png")
plt.close()

# --- 03: Adjacency matrix + spectrum ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
adj = nx.adjacency_matrix(G_full, nodelist=sorted(G_full.nodes())).todense()
im = ax.imshow(adj, cmap="YlOrRd", interpolation="nearest")
ax.set_xticks(range(45))
ax.set_yticks(range(45))
ax.set_xticklabels(sorted(G_full.nodes()), fontsize=6)
ax.set_yticklabels(sorted(G_full.nodes()), fontsize=6)
ph_sorted = [phase_of(n) for n in sorted(G_full.nodes())]
boundaries = [i - 0.5 for i in range(1, 45) if ph_sorted[i] != ph_sorted[i - 1]]
for b in boundaries:
    ax.axhline(y=b, color="blue", linewidth=1.5, alpha=0.7)
    ax.axvline(x=b, color="blue", linewidth=1.5, alpha=0.7)
plt.colorbar(im, ax=ax, shrink=0.8)
ax.set_title("Adjacency Matrix (full grid)", fontsize=13, fontweight="bold")

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
draw_palace_boundaries(ax)
for u, v in FULL_EDGES:
    x1, y1 = POSITIONS[u]
    x2, y2 = POSITIONS[v]
    palace_u = value_to_palace(u)
    palace_v = value_to_palace(v)
    if palace_u == palace_v:
        ax.plot([x1, x2], [y1, y2], color=PALACE_COLORS[palace_u], linewidth=3, alpha=0.8, zorder=1)
draw_nodes(ax)
ax.set_title("Five-palace 3×3 grid graph", fontsize=13, fontweight="bold")
ax.set_xlim(-0.8, 8.8)
ax.set_ylim(-0.8, 8.8)
ax.set_aspect("equal")
ax.axis("off")

ax = axes[0, 1]
# 4-Cycle example highlight: Center bottom side + Bottom top side
cycle4 = [40, 5, 1, 36]
cycle4_edges = [(cycle4[i], cycle4[(i + 1) % 4]) for i in range(4)]
for u, v in FULL_EDGES:
    x1, y1 = POSITIONS[u]
    x2, y2 = POSITIONS[v]
    if (u, v) in cycle4_edges or (v, u) in cycle4_edges:
        ax.plot([x1, x2], [y1, y2], color="red", linewidth=3.5, alpha=0.9, zorder=2)
    else:
        ax.plot([x1, x2], [y1, y2], color="#DDDDDD", linewidth=1, alpha=0.4, zorder=0)
for n in cycle4:
    x, y = POSITIONS[n]
    ax.add_patch(
        plt.Circle(
            (x, y),
            0.36,
            facecolor="#FFCCCC",
            edgecolor="red",
            linewidth=3,
            zorder=2,
        )
    )
    ax.text(x, y, str(n), ha="center", va="center", fontsize=10, fontweight="bold", zorder=3)
for n in range(1, 46):
    if n in cycle4:
        continue
    x, y = POSITIONS[n]
    ax.add_patch(
        plt.Circle(
            (x, y),
            0.26,
            facecolor="white",
            edgecolor="#999999",
            linewidth=1.2,
            zorder=1,
        )
    )
    ax.text(x, y, str(n), ha="center", va="center", fontsize=8, zorder=2)
ax.set_title(f"Minimum cycle example: 40-5-1-36-40 (sum={sum(cycle4)})", fontsize=13, fontweight="bold")
ax.set_xlim(-0.8, 8.8)
ax.set_ylim(-0.8, 8.8)
ax.set_aspect("equal")
ax.axis("off")

ax = axes[1, 0]
palace_names = list(PALACES.keys())
palace_sums = [sum(palace_values(p)) for p in palace_names]
palace_bar_colors = [PALACE_COLORS[p] for p in palace_names]
ax.bar(palace_names, palace_sums, color=palace_bar_colors, edgecolor="black", linewidth=1.5)
ax.axhline(y=207, color="red", linestyle="--", linewidth=2)
ax.set_title("Nine-number sum of each palace", fontsize=13, fontweight="bold")
for bar, val in zip(ax.patches, palace_sums):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        str(val),
        ha="center",
        fontsize=12,
        fontweight="bold",
    )

ax = axes[1, 1]
# Center 3×3 grid cycle-based decomposition
cycles = nx.cycle_basis(G_intra.subgraph(palace_values("Center")))
ax.text(
    0.5,
    0.5,
    f"Center 3×3 grid\ncycle count: {len(cycles)}\nminimum cycle length: {min(len(c) for c in cycles)}",
    ha="center",
    va="center",
    fontsize=14,
    fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", edgecolor="black"),
)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

plt.tight_layout()
save_fig("04_cycle_analysis.png")
plt.close()

# --- 05: Centrality + sum invariants ---
fig, axes = plt.subplots(2, 2, figsize=(16, 14))

ax = axes[0, 0]
degrees = dict(G_full.degree())
nodes_sorted = sorted(G_full.nodes(), key=lambda n: degrees[n], reverse=True)
colors_sorted = [PHASE_COLOR[phase_of(n)] for n in nodes_sorted]
ax.bar(range(45), [degrees[n] for n in nodes_sorted], color=colors_sorted, edgecolor="black")
ax.set_xticks(range(45))
ax.set_xticklabels([str(n) for n in nodes_sorted], fontsize=7)
ax.set_title("Degree (full grid)", fontsize=12, fontweight="bold")
ax.set_ylabel("Degree", fontsize=10)

ax = axes[0, 1]
betw_sorted = sorted(G_full.nodes(), key=lambda n: betw_full[n], reverse=True)
colors_b = [PHASE_COLOR[phase_of(n)] for n in betw_sorted]
ax.bar(range(45), [betw_full[n] for n in betw_sorted], color=colors_b, edgecolor="black")
ax.set_xticks(range(45))
ax.set_xticklabels([str(n) for n in betw_sorted], fontsize=7)
ax.set_title("Betweenness Centrality", fontsize=12, fontweight="bold")
ax.set_ylabel("Centrality", fontsize=10)

ax = axes[1, 0]
ph_sums = {ph: sum([n for n in range(1, 46) if phase_of(n) == ph]) for ph in ["Water", "Fire", "Wood", "Metal", "Earth"]}
ph_names = list(ph_sums.keys())
ph_vals = list(ph_sums.values())
ph_colors_bar = [PHASE_COLOR[w] for w in ph_names]
ax.bar(ph_names, ph_vals, color=ph_colors_bar, edgecolor="black", linewidth=1.5)
ax.set_title("Sum by wuxing (189, 198, 207, 216, 225)", fontsize=12, fontweight="bold")
for bar, val in zip(ax.patches, ph_vals):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 2,
        str(val),
        ha="center",
        fontsize=12,
        fontweight="bold",
    )
ax.plot(range(5), ph_vals, "o--", color="black", alpha=0.5, linewidth=2)

ax = axes[1, 1]
components = {
    "Top": sum(palace_values("Top")),
    "Left": sum(palace_values("Left")),
    "Center": sum(palace_values("Center")),
    "Right": sum(palace_values("Right")),
    "Bottom": sum(palace_values("Bottom")),
    "Total": sum(range(1, 46)),
}
ax.bar(
    list(components.keys()),
    list(components.values()),
    color=[PALACE_COLORS[k] for k in list(components.keys())[:-1]] + ["#333333"],
    edgecolor="black",
    linewidth=1.5,
)
ax.set_title("Structural subset sums", fontsize=12, fontweight="bold")
ax.set_ylabel("Sum", fontsize=10)
plt.setp(ax.xaxis.get_majorticklabels(), rotation=15, ha="right")

plt.tight_layout()
save_fig("05_centrality_invariants.png")
plt.close()

# --- 06: Wuxing generating-overcoming ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
phase_graph = nx.DiGraph()
phase_relations = [
    ("Water", "Wood", "generating"),
    ("Wood", "Fire", "generating"),
    ("Fire", "Earth", "generating"),
    ("Earth", "Metal", "generating"),
    ("Metal", "Water", "generating"),
    ("Water", "Fire", "overcoming"),
    ("Fire", "Metal", "overcoming"),
    ("Metal", "Wood", "overcoming"),
    ("Wood", "Earth", "overcoming"),
    ("Earth", "Water", "overcoming"),
]
for u, v, r in phase_relations:
    phase_graph.add_edge(u, v, relation=r)
ph_pos = {"Water": (0, 2), "Wood": (2, 1), "Fire": (1, -1), "Earth": (-1, -1), "Metal": (-2, 1)}
sheng_edges = [(u, v) for u, v, r in phase_relations if r == "generating"]
ke_edges = [(u, v) for u, v, r in phase_relations if r == "overcoming"]
nx.draw_networkx_edges(
    phase_graph,
    ph_pos,
    edgelist=sheng_edges,
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
    edgelist=ke_edges,
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
    Line2D([0], [0], color="#44AA44", lw=3, label="generating"),
    Line2D([0], [0], color="#CC4444", lw=2, linestyle="--", label="overcoming"),
]
ax.legend(handles=legend_elements, loc="upper right", fontsize=11)
ax.set_title("Wuxing generating-overcoming relation diagram", fontsize=13, fontweight="bold")
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
m0_labels = [f"M0={m0}" for m0, _ in FAMILY]
m0_values = [total for _, total in FAMILY]
m0_colors = [PHASE_COLOR[RESIDUE_STYLE[m0 % 5]["name"]] for m0, _ in FAMILY]
ax.bar(m0_labels, m0_values, color=m0_colors, edgecolor="black", linewidth=1.5)
ax.set_title("Generalized family: arithmetic sequence of palace sums\nM(n+1) = M(n) + 9", fontsize=13, fontweight="bold")
for bar, val in zip(ax.patches, m0_values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 2,
        str(val),
        ha="center",
        fontsize=12,
        fontweight="bold",
    )
ax.plot(range(5), m0_values, "o--", color="black", alpha=0.5, linewidth=2)
ax.set_ylabel("Palace Sum", fontsize=10)

ax = axes[1]
n_layers = 3
theta = np.linspace(0, 2 * np.pi, n_layers + 1)[:-1]
for i, t in enumerate(theta):
    r = 2.5 + i * 1.5
    circle = plt.Circle((0, 0), r, fill=False, color=["#CC4444", "#4488CC", "#44AA44"][i], linewidth=2, linestyle="--")
    ax.add_patch(circle)
    ax.text(r * np.cos(np.pi / 4), r * np.sin(np.pi / 4), f"{45 * (i + 1)} numbers", fontsize=10, fontweight="bold")
ax.add_patch(plt.Circle((0, 0), 0.5, facecolor="#CC9944", edgecolor="black", linewidth=2))
ax.text(0, 0, "CORE\n45", ha="center", va="center", fontsize=10, fontweight="bold")
ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("Concentric extension: 45k-number structure", fontsize=13, fontweight="bold")

plt.tight_layout()
save_fig("07_local_extensions.png")
plt.close()

# --- 08: Positional patterns (corner / edge midpoint / center) ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

ax = axes[0]
palace_names = list(PALACES.keys())
corner_vals_list = [CORNER_SUMS[p] for p in palace_names]
edge_vals_list = [EDGE_SUMS[p] for p in palace_names]
center_vals_list = [CENTER_VALUES[p] for p in palace_names]
x = np.arange(len(palace_names))
width = 0.25
ax.bar(x - width, corner_vals_list, width, label="corner 4 numbers", color="#CC4444", edgecolor="black")
ax.bar(x, edge_vals_list, width, label="edge midpoint 4 numbers", color="#4488CC", edgecolor="black")
ax.bar(x + width, center_vals_list, width, label="center 1 number", color="#44AA44", edgecolor="black")
ax.set_xticks(x)
ax.set_xticklabels(palace_names)
ax.set_title("Sum by position within palaces", fontsize=13, fontweight="bold")
ax.legend()
ax.set_ylabel("Sum", fontsize=10)

ax = axes[1]
# Center value distribution
ax.bar(palace_names, center_vals_list, color=[PALACE_COLORS[p] for p in palace_names], edgecolor="black")
ax.set_title(f"Center value of each palace: {sorted(center_vals_list)}", fontsize=13, fontweight="bold")
for bar, val in zip(ax.patches, center_vals_list):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.3,
        str(val),
        ha="center",
        fontsize=12,
        fontweight="bold",
    )
ax.set_ylabel("Center Value", fontsize=10)

plt.tight_layout()
save_fig("08_position_patterns.png")
plt.close()

print("\n" + "=" * 60)
print("All images generated!")
print(f"Output directory: {OUTPUT_DIR}/")
print("=" * 60)
