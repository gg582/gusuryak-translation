#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paljagakdeuk — modern graph and combinatorial deep analysis

《Gusuryeok》text text text Paljagakdeuk(Paljagakdeuk)text text text text textinterpretation.
analysis text: 1through 40text text 5 palace(text)text 8numberstext layouttext text structure.
"""

import os
from collections import Counter
from itertools import combinations

import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.lines import Line2D

# ============================================================
# 0. font and output setup
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
# 1. source text structuretext
# ============================================================

PALACES = {
    "Top": [
        [39, 7, 34],
        [12, None, 19],
        [24, 2, 27],
    ],
    "Left": [
        [33, 18, 28],
        [8, None, 3],
        [38, 13, 23],
    ],
    "Center": [
        [30, 5, 21],
        [16, None, 15],
        [31, 10, 36],
    ],
    "Right": [
        [22, 14, 37],
        [4, None, 9],
        [29, 17, 32],
    ],
    "Bottom": [
        [26, 1, 25],
        [20, None, 11],
        [35, 6, 40],
    ],
}

# textnumbers layouttext each palace origin(lower-left basis).
PALACE_ORIGINS = {
    "Top": (3, 6),
    "Left": (0, 3),
    "Center": (3, 3),
    "Right": (6, 3),
    "Bottom": (3, 0),
}

# text text mod 5 residue class colors.
RESIDUE_STYLE = {
    1: {"face": "#D9D9D9", "edge": "#555555", "name": "Water", "en": "Water"},
    2: {"face": "#F3C2C2", "edge": "#A33A3A", "name": "Fire", "en": "Fire"},
    3: {"face": "#C7D8F5", "edge": "#315C9A", "name": "Wood", "en": "Wood"},
    4: {"face": "#BFBFBF", "edge": "#222222", "name": "Metal", "en": "Metal"},
    0: {"face": "#F3D58A", "edge": "#A67C00", "name": "Earth", "en": "Earth"},
}

# compact five phases colors (subgraph decomposition used in related plots).
WUXING_COLOR = {
    "Water": "#4488CC",
    "Fire": "#CC4444",
    "Wood": "#44AA44",
    "Metal": "#888888",
    "Earth": "#CC9944",
}


def wuxing_of(n: int) -> str:
    """1 based on mod-5 residue five phases."""
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
                if value is None:
                    continue
                x = origin_x + col_index
                y = origin_y + (2 - row_index)
                positions[value] = (x, y)
    return positions


POSITIONS = build_positions()


def palace_cells(palace_name: str) -> list[tuple[int, int, int]]:
    """palace text (value, row, column) text. rows and columns are zero-based."""
    cells = []
    grid = PALACES[palace_name]
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value is not None:
                cells.append((value, r, c))
    return cells


def cell_role(palace_name: str, row: int, col: int) -> str:
    """3×3 grid centertext text 8numberstext position role."""
    if (row, col) in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        return "corner"
    return "edge"


# ============================================================
# 2. text construction
# ============================================================

INTRA_EDGES: list[tuple[int, int]] = []
FULL_EDGES: list[tuple[int, int]] = []

# same palace internal adjacency edges.
for palace_name, grid in PALACES.items():
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value is None:
                continue
            # right neighbor
            if c + 1 < 3:
                right = grid[r][c + 1]
                if right is not None:
                    INTRA_EDGES.append(tuple(sorted((value, right))))  # type: ignore[arg-type]
            # lower neighbor
            if r + 1 < 3:
                down = grid[r + 1][c]
                if down is not None:
                    INTRA_EDGES.append(tuple(sorted((value, down))))  # type: ignore[arg-type]

# full grid adjacent text (palace crossing palace boundaries).
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
for n in range(1, 41):
    G_intra.add_node(n)
    G_intra.nodes[n]["wuxing"] = wuxing_of(n)

G_full = nx.Graph()
G_full.add_edges_from(FULL_EDGES)
for n in range(1, 41):
    G_full.add_node(n)
    G_full.nodes[n]["wuxing"] = wuxing_of(n)

# ============================================================
# 3. textsumtext·text text analysis
# ============================================================


def palace_values(palace_name: str) -> list[int]:
    return [v for v, _, _ in palace_cells(palace_name)]


def palace_values_from_grid(grid: list[list[int | None]]) -> list[int]:
    return [v for row in grid for v in row if v is not None]


# each palace 8-text text(clockwise/counterclockwise irrelevant).
PALACE_CYCLES: dict[str, list[int]] = {}
for palace_name in PALACES:
    cycle = list(nx.cycle_basis(G_intra.subgraph(palace_values(palace_name)))[0])
    PALACE_CYCLES[palace_name] = cycle


def validate():
    all_values = [v for vals in PALACES.values() for v in palace_values_from_grid(vals)]
    assert sorted(all_values) == list(range(1, 41)), "1~40text must appear exactly once each"
    assert sum(all_values) == 820, "total sum is 820"
    for palace_name, grid in PALACES.items():
        vals = palace_values_from_grid(grid)
        assert len(vals) == 8, f"{palace_name}text 8numbers"
        assert sum(vals) == 164, f"{palace_name} sumtext 164"


validate()

print("=" * 60)
print("Paljagakdeuk modern graph and combinatorial analysis")
print("=" * 60)
print(f"node count: {G_full.number_of_nodes()}")
print(f"edge count(palace internaltext): {G_intra.number_of_edges()}")
print(f"edge count(full grid): {G_full.number_of_edges()}")
print(f"connected components(palace internaltext): {nx.number_connected_components(G_intra)}")
print(f"connected components(full grid): {nx.number_connected_components(G_full)}")

deg_seq_intra = sorted([d for _, d in G_intra.degree()], reverse=True)
deg_seq_full = sorted([d for _, d in G_full.degree()], reverse=True)
print(f"degree text(palace internaltext): {deg_seq_intra}")
print(f"degree text(full grid): {deg_seq_full}")

print("\neach palace 8-text text sum:")
for palace_name, cycle in PALACE_CYCLES.items():
    print(f"  {palace_name}: {' → '.join(map(str, cycle))} (sum={sum(cycle)})")

print("\nby five phase number sum:")
for r in [1, 2, 3, 4, 5]:
    nodes = [n for n in range(1, 41) if residue_1based(n) == r]
    wx = RESIDUE_STYLE[r % 5]["name"]
    print(f"  {wx}({r}): sum={sum(nodes)}, numbers={nodes}")

print("\nby palace five phases distribution:")
for palace_name in PALACES:
    vals = palace_values(palace_name)
    counts = Counter(wuxing_of(v) for v in vals)
    print(f"  {palace_name}: {dict(counts)}")

betw_full = nx.betweenness_centrality(G_full)
print("\nBetweenness Centrality (Top 10):")
for n, v in sorted(betw_full.items(), key=lambda x: -x[1])[:10]:
    print(f"  {n}({wuxing_of(n)}): {v:.3f}")

try:
    girth = min(len(c) for c in nx.cycle_basis(G_full))
    print(f"\nGirth (minimum cycle length): {girth}")
except Exception:
    girth = None

# five phases text classification output
wx_edge_counts = {}
for u, v in G_full.edges():
    wu, wv = wuxing_of(u), wuxing_of(v)
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
    wx_edge_counts[key] = wx_edge_counts.get(key, 0) + 1

print("\nfive phases edge distribution:")
for key, cnt in wx_edge_counts.items():
    print(f"  {key}: {cnt}")

# ============================================================
# 4. text based analysis (corner vs edge midpoint)
# ============================================================

CORNER_SUMS: dict[str, int] = {}
EDGE_SUMS: dict[str, int] = {}
for palace_name in PALACES:
    corner_vals = []
    edge_vals = []
    for value, r, c in palace_cells(palace_name):
        if cell_role(palace_name, r, c) == "corner":
            corner_vals.append(value)
        else:
            edge_vals.append(value)
    CORNER_SUMS[palace_name] = sum(corner_vals)
    EDGE_SUMS[palace_name] = sum(edge_vals)

print("\nby palace corner/edge midpoint sum:")
for palace_name in PALACES:
    print(
        f"  {palace_name}: corner={CORNER_SUMS[palace_name]}, "
        f"edge midpoint={EDGE_SUMS[palace_name]}"
    )

# ============================================================
# 5. generalized family
# ============================================================

FAMILY = [(m0, 148 + (m0 - 1) * 8) for m0 in range(1, 6)]
print("\nM0 generalized family:")
for m0, total in FAMILY:
    wx = RESIDUE_STYLE[m0 % 5]["name"]
    print(f"  M0={m0}({wx}): palace sum={total}")

# ============================================================
# 6. visualization
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
            f"{palace_name} · Σ=164",
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


def value_to_palace(value: int) -> str:
    for palace_name, grid in PALACES.items():
        for row in grid:
            if value in row:
                return palace_name
    raise ValueError(value)


# --- 01: source graph ---
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

# empty center text
for palace_name, origin in PALACE_ORIGINS.items():
    ox, oy = origin
    ax.add_patch(
        plt.Circle(
            (ox + 1, oy + 1),
            0.18,
            facecolor="white",
            edgecolor="#999999",
            linewidth=1.5,
            linestyle="--",
            zorder=1,
        )
    )

draw_nodes(ax)
ax.set_title(
    "Paljagakdeuk - source cross structure\nfive palaces · 8numbers · each palace sum 164 · total sum 820",
    fontsize=16,
    fontweight="bold",
)
ax.set_xlim(-0.8, 8.8)
ax.set_ylim(-0.8, 8.8)
ax.set_aspect("equal")
ax.axis("off")
legend_elements = [
    mpatches.Patch(facecolor=WUXING_COLOR[wx], edgecolor="black", label=f"{wx}")
    for wx in ["Water", "Fire", "Wood", "Metal", "Earth"]
]
legend_elements.append(
    Line2D(
        [0],
        [0],
        marker="o",
        color="w",
        markeredgecolor="#999999",
        markerfacecolor="white",
        markersize=8,
        label="empty center",
    )
)
ax.legend(handles=legend_elements, loc="lower right", fontsize=10, framealpha=0.9)
save_fig("01_original_graph.png")
plt.close()

# --- 02: by five phase subgraph decomposition ---
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()
ax = axes[0]
draw_palace_boundaries(ax)
for u, v in FULL_EDGES:
    x1, y1 = POSITIONS[u]
    x2, y2 = POSITIONS[v]
    ax.plot([x1, x2], [y1, y2], color="#CCCCCC", linewidth=1, alpha=0.5, zorder=0)
draw_nodes(ax)
ax.set_title("full graph", fontsize=13, fontweight="bold")
ax.set_xlim(-0.8, 8.8)
ax.set_ylim(-0.8, 8.8)
ax.set_aspect("equal")
ax.axis("off")

for idx, wx in enumerate(["Water", "Fire", "Wood", "Metal", "Earth"]):
    ax = axes[idx + 1]
    draw_palace_boundaries(ax)
    wx_nodes = [n for n in range(1, 41) if wuxing_of(n) == wx]
    other_nodes = [n for n in range(1, 41) if n not in wx_nodes]

    # background edges
    for u, v in FULL_EDGES:
        x1, y1 = POSITIONS[u]
        x2, y2 = POSITIONS[v]
        ax.plot([x1, x2], [y1, y2], color="#EEEEEE", linewidth=1, alpha=0.4, zorder=0)

    # textfive phases text text
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

    # five phases node highlight
    for n in wx_nodes:
        x, y = POSITIONS[n]
        ax.add_patch(
            plt.Circle(
                (x, y),
                0.34,
                facecolor=WUXING_COLOR[wx],
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
            color="white" if wx in ["Water", "Wood"] else "black",
            zorder=3,
        )

    ax.set_title(
        f"{wx} · sum {sum(wx_nodes)}",
        fontsize=12,
        fontweight="bold",
        color=WUXING_COLOR[wx],
    )
    ax.set_xlim(-0.8, 8.8)
    ax.set_ylim(-0.8, 8.8)
    ax.set_aspect("equal")
    ax.axis("off")

plt.suptitle("five phases(text)text subgraph decomposition", fontsize=16, fontweight="bold", y=1.02)
plt.tight_layout()
save_fig("02_wuxing_decomposition.png")
plt.close()

# --- 03: adjacency matrix + spectrum ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
adj = nx.adjacency_matrix(G_full, nodelist=sorted(G_full.nodes())).todense()
im = ax.imshow(adj, cmap="YlOrRd", interpolation="nearest")
ax.set_xticks(range(40))
ax.set_yticks(range(40))
ax.set_xticklabels(sorted(G_full.nodes()), fontsize=7)
ax.set_yticklabels(sorted(G_full.nodes()), fontsize=7)
# by five phase boundary lines
wx_sorted = [wuxing_of(n) for n in sorted(G_full.nodes())]
boundaries = [i - 0.5 for i in range(1, 40) if wx_sorted[i] != wx_sorted[i - 1]]
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

# --- 04: cycle analysis ---
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
ax.set_title("five-palace internal 8-Cycle", fontsize=13, fontweight="bold")
ax.set_xlim(-0.8, 8.8)
ax.set_ylim(-0.8, 8.8)
ax.set_aspect("equal")
ax.axis("off")

ax = axes[0, 1]
# palace highlight inter-palace edges only
for u, v in FULL_EDGES:
    x1, y1 = POSITIONS[u]
    x2, y2 = POSITIONS[v]
    palace_u = value_to_palace(u)
    palace_v = value_to_palace(v)
    if palace_u != palace_v:
        ax.plot([x1, x2], [y1, y2], color="#333333", linewidth=2.5, alpha=0.9, zorder=1)
    else:
        ax.plot([x1, x2], [y1, y2], color="#DDDDDD", linewidth=1, alpha=0.5, zorder=0)
# Center node highlight
for n in palace_values("Center"):
    x, y = POSITIONS[n]
    ax.add_patch(
        plt.Circle(
            (x, y),
            0.34,
            facecolor="#44AA44",
            edgecolor="red",
            linewidth=2.5,
            zorder=2,
        )
    )
    ax.text(x, y, str(n), ha="center", va="center", fontsize=10, fontweight="bold", zorder=3)
# other nodes
for n in range(1, 41):
    if n in palace_values("Center"):
        continue
    x, y = POSITIONS[n]
    ax.add_patch(
        plt.Circle(
            (x, y),
            0.28,
            facecolor="white",
            edgecolor="#999999",
            linewidth=1.5,
            zorder=1,
        )
    )
    ax.text(x, y, str(n), ha="center", va="center", fontsize=9, zorder=2)
ax.set_title("Centertext centertext text 4directional connections\n(palace text boundary text 12)", fontsize=13, fontweight="bold")
ax.set_xlim(-0.8, 8.8)
ax.set_ylim(-0.8, 8.8)
ax.set_aspect("equal")
ax.axis("off")

ax = axes[1, 0]
palace_names = list(PALACES.keys())
palace_sums = [sum(palace_values(p)) for p in palace_names]
palace_bar_colors = [PALACE_COLORS[p] for p in palace_names]
ax.bar(palace_names, palace_sums, color=palace_bar_colors, edgecolor="black", linewidth=1.5)
ax.axhline(y=164, color="red", linestyle="--", linewidth=2)
ax.set_title("each palace 8numbers sum", fontsize=13, fontweight="bold")
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
# each palace 8-cycle cumulative sum visualization
palace_name = "Center"
cycle = PALACE_CYCLES[palace_name]
cumsum = np.cumsum([n for n in cycle])
ax.plot(range(8), cumsum, "o-", color=PALACE_COLORS[palace_name], linewidth=2.5, markersize=8, markeredgecolor="black")
ax.fill_between(range(8), cumsum, alpha=0.2, color=PALACE_COLORS[palace_name])
ax.set_xticks(range(8))
ax.set_xticklabels([str(n) for n in cycle], fontsize=9)
ax.set_title(f"Center 8-Cycle cumulative sum (Total={sum(cycle)})", fontsize=13, fontweight="bold")
ax.grid(True, alpha=0.3)
ax.axhline(y=sum(cycle) / 2, color="blue", linestyle="--", alpha=0.5)

plt.tight_layout()
save_fig("04_cycle_analysis.png")
plt.close()

# --- 05: centrality + sum invariants ---
fig, axes = plt.subplots(2, 2, figsize=(16, 14))

ax = axes[0, 0]
degrees = dict(G_full.degree())
nodes_sorted = sorted(G_full.nodes(), key=lambda n: degrees[n], reverse=True)
colors_sorted = [WUXING_COLOR[wuxing_of(n)] for n in nodes_sorted]
ax.bar(range(40), [degrees[n] for n in nodes_sorted], color=colors_sorted, edgecolor="black")
ax.set_xticks(range(40))
ax.set_xticklabels([str(n) for n in nodes_sorted], fontsize=8)
ax.set_title("Degree (full grid)", fontsize=12, fontweight="bold")
ax.set_ylabel("Degree", fontsize=10)

ax = axes[0, 1]
betw_sorted = sorted(G_full.nodes(), key=lambda n: betw_full[n], reverse=True)
colors_b = [WUXING_COLOR[wuxing_of(n)] for n in betw_sorted]
ax.bar(range(40), [betw_full[n] for n in betw_sorted], color=colors_b, edgecolor="black")
ax.set_xticks(range(40))
ax.set_xticklabels([str(n) for n in betw_sorted], fontsize=8)
ax.set_title("Betweenness Centrality", fontsize=12, fontweight="bold")
ax.set_ylabel("Centrality", fontsize=10)

ax = axes[1, 0]
wx_sums = {wx: sum([n for n in range(1, 41) if wuxing_of(n) == wx]) for wx in ["Water", "Fire", "Wood", "Metal", "Earth"]}
wx_names = list(wx_sums.keys())
wx_vals = list(wx_sums.values())
wx_colors_bar = [WUXING_COLOR[w] for w in wx_names]
ax.bar(wx_names, wx_vals, color=wx_colors_bar, edgecolor="black", linewidth=1.5)
ax.set_title("by five phase number sum (148, 156, 164, 172, 180)", fontsize=12, fontweight="bold")
for bar, val in zip(ax.patches, wx_vals):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 2,
        str(val),
        ha="center",
        fontsize=12,
        fontweight="bold",
    )
ax.plot(range(5), wx_vals, "o--", color="black", alpha=0.5, linewidth=2)

ax = axes[1, 1]
components = {
    "Top": sum(palace_values("Top")),
    "Left": sum(palace_values("Left")),
    "Center": sum(palace_values("Center")),
    "Right": sum(palace_values("Right")),
    "Bottom": sum(palace_values("Bottom")),
    "text": sum(range(1, 41)),
}
ax.bar(
    list(components.keys()),
    list(components.values()),
    color=[PALACE_COLORS[k] for k in list(components.keys())[:-1]] + ["#333333"],
    edgecolor="black",
    linewidth=1.5,
)
ax.set_title("structural subset sums", fontsize=12, fontweight="bold")
ax.set_ylabel("Sum", fontsize=10)
plt.setp(ax.xaxis.get_majorticklabels(), rotation=15, ha="right")

plt.tight_layout()
save_fig("05_centrality_invariants.png")
plt.close()

# --- 06: five phases generatingovercoming ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
wuxing_graph = nx.DiGraph()
wuxing_relations = [
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
for u, v, r in wuxing_relations:
    wuxing_graph.add_edge(u, v, relation=r)
wx_pos = {"Water": (0, 2), "Wood": (2, 1), "Fire": (1, -1), "Earth": (-1, -1), "Metal": (-2, 1)}
sheng_edges = [(u, v) for u, v, r in wuxing_relations if r == "generating"]
ke_edges = [(u, v) for u, v, r in wuxing_relations if r == "overcoming"]
nx.draw_networkx_edges(
    wuxing_graph,
    wx_pos,
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
    wuxing_graph,
    wx_pos,
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
wx_node_colors = [WUXING_COLOR[w] for w in wuxing_graph.nodes()]
nx.draw_networkx_nodes(
    wuxing_graph,
    wx_pos,
    node_color=wx_node_colors,
    node_size=3000,
    edgecolors="black",
    linewidths=2.5,
    ax=ax,
)
nx.draw_networkx_labels(wuxing_graph, wx_pos, font_size=14, font_weight="normal", ax=ax)
legend_elements = [
    Line2D([0], [0], color="#44AA44", lw=3, label="generating"),
    Line2D([0], [0], color="#CC4444", lw=2, linestyle="--", label="overcoming"),
]
ax.legend(handles=legend_elements, loc="upper right", fontsize=11)
ax.set_title("five phases generatingovercoming relation diagram", fontsize=13, fontweight="bold")
ax.set_xlim(-3, 3.5)
ax.set_ylim(-2.5, 3)
ax.axis("off")

ax = axes[1]
wx_edge_counts = {}
for u, v in G_full.edges():
    wu, wv = wuxing_of(u), wuxing_of(v)
    if wu == wv:
        key = f"{wu}same-phase"
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
    wx_edge_counts[key] = wx_edge_counts.get(key, 0) + 1
colors_pie = ["#44AA44", "#CC4444", "#CC9944", "#4488CC"]
ax.pie(
    list(wx_edge_counts.values()),
    labels=list(wx_edge_counts.keys()),
    autopct="%1.0f%%",
    colors=colors_pie[: len(wx_edge_counts)],
    explode=[0.05] * len(wx_edge_counts),
    textprops={"fontsize": 12, "fontweight": "bold"},
)
ax.set_title(f"five phases edge distribution (N={G_full.number_of_edges()})", fontsize=13, fontweight="bold")
plt.tight_layout()
save_fig("06_wuxing_relations.png")
plt.close()

# --- 07: extension and generalization ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# text: M0 text
ax = axes[0]
m0_labels = [f"M0={m0}" for m0, _ in FAMILY]
m0_values = [total for _, total in FAMILY]
m0_colors = [WUXING_COLOR[RESIDUE_STYLE[m0 % 5]["name"]] for m0, _ in FAMILY]
ax.bar(m0_labels, m0_values, color=m0_colors, edgecolor="black", linewidth=1.5)
ax.set_title("generalized family: palace sumtext textdegreetext\nM(n+1) = M(n) + 8", fontsize=13, fontweight="bold")
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

# text: 40→80→120... text text
ax = axes[1]
n_layers = 3
theta = np.linspace(0, 2 * np.pi, n_layers + 1)[:-1]
for i, t in enumerate(theta):
    r = 2.5 + i * 1.5
    circle = plt.Circle((0, 0), r, fill=False, color=["#CC4444", "#4488CC", "#44AA44"][i], linewidth=2, linestyle="--")
    ax.add_patch(circle)
    ax.text(r * np.cos(np.pi / 4), r * np.sin(np.pi / 4), f"{40 * (i + 1)}numbers", fontsize=10, fontweight="bold")
ax.add_patch(plt.Circle((0, 0), 0.5, facecolor="#CC9944", edgecolor="black", linewidth=2))
ax.text(0, 0, "CORE\n40", ha="center", va="center", fontsize=10, fontweight="bold")
ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("concentric extension: 40knumbers structure", fontsize=13, fontweight="bold")

plt.tight_layout()
save_fig("07_local_extensions.png")
plt.close()

# --- 08: positional patterns (corner vs edge midpoint) ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

ax = axes[0]
palace_names = list(PALACES.keys())
corner_vals_list = [CORNER_SUMS[p] for p in palace_names]
edge_vals_list = [EDGE_SUMS[p] for p in palace_names]
x = np.arange(len(palace_names))
width = 0.35
ax.bar(x - width / 2, corner_vals_list, width, label="corner 4numbers", color="#CC4444", edgecolor="black")
ax.bar(x + width / 2, edge_vals_list, width, label="edge midpoint 4numbers", color="#4488CC", edgecolor="black")
ax.set_xticks(x)
ax.set_xticklabels(palace_names)
ax.set_title("by palace corner/edge midpoint sum", fontsize=13, fontweight="bold")
ax.legend()
ax.set_ylabel("Sum", fontsize=10)

ax = axes[1]
# by palace average positiontext sumtext text
palace_centers = {
    "Top": (4, 7),
    "Left": (1, 4),
    "Center": (4, 4),
    "Right": (7, 4),
    "Bottom": (4, 1),
}
for palace_name in PALACES:
    cx, cy = palace_centers[palace_name]
    total = sum(palace_values(palace_name))
    ax.scatter(cx, cy, s=total * 3, c=PALACE_COLORS[palace_name], edgecolors="black", linewidths=2, alpha=0.7)
    ax.text(cx, cy, f"{palace_name}\n{total}", ha="center", va="center", fontsize=10, fontweight="bold")
# textnumbers connection
for a, b in [("Top", "Center"), ("Left", "Center"), ("Center", "Right"), ("Center", "Bottom")]:
    x1, y1 = palace_centers[a]
    x2, y2 = palace_centers[b]
    ax.plot([x1, x2], [y1, y2], "k-", linewidth=2, alpha=0.3)
ax.set_xlim(-1, 9)
ax.set_ylim(-1, 9)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("textnumbers layouttext sum invariants", fontsize=13, fontweight="bold")

plt.tight_layout()
save_fig("08_position_patterns.png")
plt.close()

print("\n" + "=" * 60)
print("All images generated!")
print(f"output directory: {OUTPUT_DIR}/")
print("=" * 60)
