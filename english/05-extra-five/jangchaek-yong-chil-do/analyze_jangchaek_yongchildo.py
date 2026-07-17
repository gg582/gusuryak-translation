#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jangchaek-yong-chil-do (章策用七圖) — Modern graph and combinatorial deep analysis

A reinterpretation of Jangchaek-yong-chil-do, one of the diagrams in the
Gusuryak (九數略) series, in modern mathematical language.

Analysis target: a star structure arranging the numbers 1 through 19 on three
axes of 7 cells each, all sharing the central cell 7. Each axis sums to 68.
"""

import math
import os
from collections import Counter
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.lines import Line2D

# ============================================================
# 0. Font and output settings
# ============================================================

os.chdir(Path(__file__).parent)

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUTPUT_DIR = Path(".")


def save_fig(name):
    path = OUTPUT_DIR / name
    plt.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    print(f"[Saved] {path}")


# ============================================================
# 1. Source data structuring (same coordinate geometry as visualize.py)
# ============================================================

CENTER = 7
SPACING = 1.2

# Three axes: listed from one end to the opposite end through the center
AXES = {
    "vertical": [5, 18, 9, 7, 12, 2, 15],   # vertical axis (90°), top -> bottom
    "diag150": [4, 10, 19, 7, 1, 14, 13],   # 150° axis, upper-left -> lower-right
    "diag30": [8, 6, 17, 7, 3, 11, 16],     # 30° axis, upper-right -> lower-left
}
AXIS_ANGLE = {"vertical": 90.0, "diag150": 150.0, "diag30": 30.0}
AXIS_LABELS = {"vertical": "Vertical (90°)", "diag150": "Diagonal (150°)", "diag30": "Diagonal (30°)"}

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

PHASES = ["Water", "Fire", "Wood", "Metal", "Earth"]

RELATION_LABELS = {"generation": "Generation", "overcoming": "Overcoming", "same_phase": "Same phase"}


def phase_of(n: int) -> str:
    return RESIDUE_STYLE[n % 5]["name"]


def residue_1based(n: int) -> int:
    r = n % 5
    return 5 if r == 0 else r


def build_positions() -> dict[int, tuple[float, float]]:
    """Same geometric coordinates as visualize.py: center 7 = (0,0), three axis directions."""
    positions: dict[int, tuple[float, float]] = {CENTER: (0.0, 0.0)}
    for axis_name, nodes in AXES.items():
        angle = math.radians(AXIS_ANGLE[axis_name])
        for i, node in enumerate(nodes):
            if node == CENTER:
                continue
            dist = 3 - i
            positions[node] = (
                dist * math.cos(angle) * SPACING,
                dist * math.sin(angle) * SPACING,
            )
    return positions


POSITIONS = build_positions()

# Concentric rings d1, d2, d3 by graph distance from the center
RINGS: dict[int, list[int]] = {1: [], 2: [], 3: []}
for node, (x, y) in POSITIONS.items():
    if node == CENTER:
        continue
    d = round(math.hypot(x, y) / SPACING)
    RINGS[d].append(node)
for d in RINGS:
    RINGS[d].sort()

RING_LABELS = {1: "Inner ring (d1)", 2: "Middle ring (d2)", 3: "Outer ring (d3)"}


def spokes_of(axis_nodes: list[int]) -> tuple[list[int], list[int]]:
    """Split an axis into the two half-rays (spokes) around the center."""
    idx = axis_nodes.index(CENTER)
    return axis_nodes[:idx], axis_nodes[idx + 1:]


def antipodal_pairs(axis_nodes: list[int]) -> list[tuple[int, int, int]]:
    """Antipodal pairs of an axis: (level k, left value, right value)."""
    idx = axis_nodes.index(CENTER)
    return [(k, axis_nodes[idx - k], axis_nodes[idx + k]) for k in range(1, idx + 1)]


# ============================================================
# 2. Graph construction
# ============================================================

EDGES: list[tuple[int, int]] = []
for nodes in AXES.values():
    for i in range(len(nodes) - 1):
        EDGES.append((nodes[i], nodes[i + 1]))

G = nx.Graph()
G.add_nodes_from(range(1, 20))
G.add_edges_from(EDGES)
for n in G.nodes():
    G.nodes[n]["phase"] = phase_of(n)


def role_of(n: int) -> str:
    if n == CENTER:
        return "center"
    x, y = POSITIONS[n]
    d = round(math.hypot(x, y) / SPACING)
    return f"d{d}"


# ============================================================
# 3. Combinatorics and graph theory analysis
# ============================================================

def validate():
    """Verify the basic invariants of the source data; fail hard on any mismatch."""
    all_values = [v for nodes in AXES.values() for v in nodes if v != CENTER] + [CENTER]
    if sorted(all_values) != list(range(1, 20)):
        raise ValueError("1~19 must each appear exactly once")
    total = sum(all_values)
    if total != 190:
        raise ValueError(f"Total sum must be 190: {total}")
    for axis_name, nodes in AXES.items():
        if len(nodes) != 7:
            raise ValueError(f"{AXIS_LABELS[axis_name]} must have 7 cells")
        if sum(nodes) != 68:
            raise ValueError(f"{AXIS_LABELS[axis_name]} sum must be 68: {sum(nodes)}")
        if nodes.count(CENTER) != 1:
            raise ValueError(f"{AXIS_LABELS[axis_name]} must contain center 7 exactly once")
    # Duplication checksum: 3 axis sums = total + center duplication
    k_times_s = 3 * 68
    duplication = 2 * CENTER
    if k_times_s != total + duplication:
        raise ValueError(f"3 × 68 = {k_times_s} ≠ 190 + {duplication}")
    # Ring sum invariant
    ring_target = (total - CENTER) // 3
    for d, members in RINGS.items():
        if sum(members) != ring_target:
            raise ValueError(f"{RING_LABELS[d]} sum must be {ring_target}: {sum(members)}")

    # Print the verified sum equations
    print("Checksum equations:")
    for axis_name, nodes in AXES.items():
        expr = "+".join(map(str, nodes))
        print(f"  {AXIS_LABELS[axis_name]}: {expr} = {sum(nodes)}")
    print(f"  Total: 1+2+...+19 = {total}")
    print(f"  3 × 68 = {k_times_s} = {total} + {duplication}  (center 7 used 3 times: 19 values, 21 cells)")
    for d, members in RINGS.items():
        expr = "+".join(map(str, members))
        print(f"  {RING_LABELS[d]}: {expr} = {sum(members)}  (R = (190-7)/3 = {ring_target})")


validate()

print("=" * 60)
print("Jangchaek-yong-chil-do — Modern graph and combinatorial analysis")
print("=" * 60)
print(f"Node count: {G.number_of_nodes()}")
print(f"Edge count: {G.number_of_edges()}")
print(f"Connected components: {nx.number_connected_components(G)}")
print(f"Is a tree: {nx.is_tree(G)}")

deg_seq = sorted([d for _, d in G.degree()], reverse=True)
deg_counter = Counter(d for _, d in G.degree())
print(f"Degree sequence: {deg_seq}")
print(f"Degree distribution: {dict(sorted(deg_counter.items(), reverse=True))}")

cycle_basis = nx.cycle_basis(G)
print(f"Cycle basis size: {len(cycle_basis)} (a tree has no girth)")

betw = nx.betweenness_centrality(G)
print("\nBetweenness centrality (Top 10):")
for n, v in sorted(betw.items(), key=lambda x: -x[1])[:10]:
    print(f"  {n}({phase_of(n)}, {role_of(n)}): {v:.3f}")

print("\nWuxing class sums:")
WX_SUMS = {}
for r in [1, 2, 3, 4, 5]:
    nodes = [n for n in range(1, 20) if residue_1based(n) == r]
    wx = RESIDUE_STYLE[r % 5]["name"]
    WX_SUMS[wx] = sum(nodes)
    print(f"  {wx}: sum={sum(nodes)}, values={nodes}")

print("\nPer-axis wuxing distribution:")
for axis_name, nodes in AXES.items():
    counts = Counter(phase_of(v) for v in nodes)
    print(f"  {AXIS_LABELS[axis_name]}: {dict(counts)}")

# Wuxing edge classification (generation / overcoming / same phase)
GENERATION = [
    ("Water", "Wood"), ("Wood", "Fire"), ("Fire", "Earth"),
    ("Earth", "Metal"), ("Metal", "Water"),
]
OVERCOMING = [
    ("Water", "Fire"), ("Fire", "Metal"), ("Metal", "Wood"),
    ("Wood", "Earth"), ("Earth", "Water"),
]


def classify_edge(u: int, v: int) -> str:
    wu, wv = phase_of(u), phase_of(v)
    if wu == wv:
        return "same_phase"
    if (wu, wv) in GENERATION or (wv, wu) in GENERATION:
        return "generation"
    if (wu, wv) in OVERCOMING or (wv, wu) in OVERCOMING:
        return "overcoming"
    return "neutral"


wx_edge_counts: dict[str, int] = {}
for u, v in G.edges():
    key = classify_edge(u, v)
    wx_edge_counts[key] = wx_edge_counts.get(key, 0) + 1

print("\nWuxing edge distribution:")
for key, cnt in wx_edge_counts.items():
    print(f"  {RELATION_LABELS.get(key, key)}: {cnt} ({cnt / G.number_of_edges() * 100:.1f}%)")


# ============================================================
# 4. Position-based analysis (rings / spokes / antipodal pairs)
# ============================================================

print("\nRing sums:")
RING_SUMS = {d: sum(members) for d, members in RINGS.items()}
for d, s in RING_SUMS.items():
    print(f"  {RING_LABELS[d]}: {s}")

print("\nSpoke (half-ray) sums:")
SPOKES: dict[str, list[int]] = {}
SPOKE_LABELS = {
    ("vertical", 0): "Vertical top", ("vertical", 1): "Vertical bottom",
    ("diag150", 0): "150° upper-left", ("diag150", 1): "150° lower-right",
    ("diag30", 0): "30° upper-right", ("diag30", 1): "30° lower-left",
}
for axis_name, nodes in AXES.items():
    for side, spoke in enumerate(spokes_of(nodes)):
        label = SPOKE_LABELS[(axis_name, side)]
        SPOKES[label] = spoke
        print(f"  {label}: {spoke} sum={sum(spoke)}")
spoke_sums_sorted = sorted(sum(s) for s in SPOKES.values())
print(f"  Sorted spoke sums: {spoke_sums_sorted} (six consecutive integers: {spoke_sums_sorted == list(range(28, 34))})")

print("\nAntipodal-pair sums per axis (levels d1, d2, d3):")
PAIR_SUM_MATRIX: dict[str, list[int]] = {}
for axis_name, nodes in AXES.items():
    pair_sums = []
    for k, a, b in antipodal_pairs(nodes):
        pair_sums.append(a + b)
        print(f"  {AXIS_LABELS[axis_name]} d{k}: {a}+{b} = {a + b}")
    PAIR_SUM_MATRIX[axis_name] = pair_sums
    print(f"  {AXIS_LABELS[axis_name]} pair-sum total: {sum(pair_sums)} (+center 7 = {sum(pair_sums) + CENTER})")
col_sums = [sum(PAIR_SUM_MATRIX[a][i] for a in AXES) for i in range(3)]
print(f"  Per-level (column) sums: {col_sums}  -> row sums = column sums = 61")


# ============================================================
# 5. Generalization family (a axes × L cells star)
# ============================================================

# Same star family: Beomsu-yong-odo (a=2, L=5), Jangchaek-yong-chil-do (a=3, L=7),
# Jungsang-yong-gudo (a=4, L=9)
FAMILY = [
    ("Beomsu-yong-odo", 2, 5),
    ("Jangchaek-yong-chil-do", 3, 7),
    ("Jungsang-yong-gudo", 4, 9),
]
print("\nGeneralization family (a axes × L cells, center L, N = a(L-1)+1):")
FAMILY_ROWS = []
for name, a, L in FAMILY:
    N = a * (L - 1) + 1
    T = N * (N + 1) // 2
    S = (T + (a - 1) * L) // a
    R = (T - L) // a
    FAMILY_ROWS.append((name, a, L, N, T, S, R))
    print(f"  {name}: a={a}, L={L}, N={N}, T={T}, axis sum S={S}, ring sum R={R}")
    if a == 3:
        assert (N, T, S, R) == (19, 190, 68, 61), "Jangchaek-yong-chil-do parameters mismatch"


# ============================================================
# 6. Graph spectral analysis
# ============================================================

nodelist = sorted(G.nodes())
adj = nx.to_numpy_array(G, nodelist=nodelist)
eigenvalues = np.linalg.eigvalsh(adj)
lambda_max = float(max(eigenvalues))
lambda_min = float(min(eigenvalues))
print(f"\nAdjacency eigenvalues: lambda_max = {lambda_max:.4f}, lambda_min = {lambda_min:.4f}")
print(f"  Bipartite (tree) symmetry: lambda_min = -lambda_max -> {abs(lambda_min + lambda_max) < 1e-9}")


# ============================================================
# 7. Visualization
# ============================================================

AXIS_COLORS = {"vertical": "#CC4444", "diag150": "#4488CC", "diag30": "#44AA44"}


def draw_axis_lines(ax, linewidth=2.5, alpha=0.7):
    for axis_name, nodes in AXES.items():
        for i in range(len(nodes) - 1):
            x1, y1 = POSITIONS[nodes[i]]
            x2, y2 = POSITIONS[nodes[i + 1]]
            ax.plot(
                [x1, x2], [y1, y2],
                color=AXIS_COLORS[axis_name], linewidth=linewidth, alpha=alpha, zorder=1,
            )


def draw_nodes(ax, highlight_values=None, node_radius=0.30, fontsize=10):
    for value, (x, y) in POSITIONS.items():
        style = RESIDUE_STYLE[value % 5]
        edge = style["edge"]
        lw = 2.0
        if value == CENTER:
            edge = "#AA0000"
            lw = 3.5
        if highlight_values and value in highlight_values:
            edge = "red"
            lw = 3.5
        ax.add_patch(
            plt.Circle((x, y), node_radius, facecolor=style["face"],
                       edgecolor=edge, linewidth=lw, zorder=2)
        )
        ax.text(x, y, str(value), ha="center", va="center",
                fontsize=fontsize, fontweight="bold", zorder=3)


def draw_ring_guides(ax):
    for d, label in RING_LABELS.items():
        r = d * SPACING
        ax.add_patch(
            plt.Circle((0, 0), r, fill=False, edgecolor="#999999",
                       linewidth=1.2, linestyle=(0, (4, 4)), zorder=0)
        )
        ax.text(r * math.cos(math.radians(45)), r * math.sin(math.radians(45)) + 0.10,
                f"{label} Σ=61", fontsize=9, color="#666666")


def wuxing_legend(ax, loc="lower right"):
    legend_elements = [
        mpatches.Patch(facecolor=PHASE_COLOR[wx], edgecolor="black", label=wx)
        for wx in PHASES
    ]
    ax.legend(handles=legend_elements, loc=loc, fontsize=10, framealpha=0.9)


# --- 01: Original graph ---
fig, ax = plt.subplots(figsize=(10, 10))
draw_ring_guides(ax)
draw_axis_lines(ax)
draw_nodes(ax)
for axis_name, nodes in AXES.items():
    end = nodes[0]
    x, y = POSITIONS[end]
    ax.text(x * 1.16, y * 1.16, f"{AXIS_LABELS[axis_name]}\nΣ=68",
            ha="center", va="center", fontsize=10, color=AXIS_COLORS[axis_name],
            fontweight="bold")
ax.set_title(
    "Jangchaek-yong-chil-do — Original 3-Axis Structure\n"
    "3 axes · 7 cells · axis sum 68 · total 190 · shared center 7",
    fontsize=15, fontweight="bold",
)
ax.set_xlim(-4.6, 4.6)
ax.set_ylim(-4.6, 4.6)
ax.set_aspect("equal")
ax.axis("off")
wuxing_legend(ax)
save_fig("01_original_graph.png")
plt.close()

# --- 02: Wuxing subgraph decomposition ---
fig, axes = plt.subplots(2, 3, figsize=(16, 11))
axes = axes.flatten()
ax = axes[0]
draw_axis_lines(ax, linewidth=1.5, alpha=0.5)
draw_nodes(ax)
ax.set_title("Full graph", fontsize=13, fontweight="bold")
ax.set_xlim(-4.6, 4.6)
ax.set_ylim(-4.6, 4.6)
ax.set_aspect("equal")
ax.axis("off")

for idx, wx in enumerate(PHASES):
    ax = axes[idx + 1]
    draw_axis_lines(ax, linewidth=1.0, alpha=0.25)
    wx_nodes = [n for n in range(1, 20) if phase_of(n) == wx]
    for n in range(1, 20):
        x, y = POSITIONS[n]
        if n in wx_nodes:
            ax.add_patch(
                plt.Circle((x, y), 0.32, facecolor=PHASE_COLOR[wx],
                           edgecolor="black", linewidth=2.5, zorder=2)
            )
            ax.text(x, y, str(n), ha="center", va="center", fontsize=10,
                    fontweight="bold",
                    color="white" if wx in ["Water", "Wood"] else "black", zorder=3)
        else:
            ax.add_patch(
                plt.Circle((x, y), 0.20, facecolor="#F0F0F0",
                           edgecolor="#CCCCCC", linewidth=1, zorder=1)
            )
            ax.text(x, y, str(n), ha="center", va="center", fontsize=7,
                    color="#AAAAAA", zorder=2)
    ax.set_title(f"{wx} · {len(wx_nodes)} values · sum {WX_SUMS[wx]}",
                 fontsize=12, fontweight="bold", color=PHASE_COLOR[wx])
    ax.set_xlim(-4.6, 4.6)
    ax.set_ylim(-4.6, 4.6)
    ax.set_aspect("equal")
    ax.axis("off")

plt.suptitle("Wuxing (Five Phases) subgraph decomposition — Earth, Water, Fire, Wood, Metal sums: 30, 34, 38, 42, 46",
             fontsize=15, fontweight="bold")
plt.tight_layout()
save_fig("02_wuxing_decomposition.png")
plt.close()

# --- 03: Adjacency matrix + spectrum ---
fig, axes = plt.subplots(1, 2, figsize=(15, 6.5))
ax = axes[0]
im = ax.imshow(adj, cmap="YlOrRd", interpolation="nearest")
ax.set_xticks(range(19))
ax.set_yticks(range(19))
ax.set_xticklabels(nodelist, fontsize=7)
ax.set_yticklabels(nodelist, fontsize=7)
plt.colorbar(im, ax=ax, shrink=0.8)
ax.set_title("Adjacency matrix (19×19)", fontsize=13, fontweight="bold")

ax = axes[1]
ax.bar(range(len(eigenvalues)), sorted(eigenvalues, reverse=True),
       color="#4488CC", edgecolor="black", alpha=0.8)
ax.axhline(y=0, color="red", linestyle="--", linewidth=1)
ax.set_xlabel("Index", fontsize=11)
ax.set_ylabel("Eigenvalue", fontsize=11)
ax.set_title(f"Graph spectrum\nλ_max={lambda_max:.2f}, λ_min={lambda_min:.2f} (tree: symmetric about 0)",
             fontsize=13, fontweight="bold")
ax.grid(True, alpha=0.3)
plt.tight_layout()
save_fig("03_adjacency_spectrum.png")
plt.close()

# --- 04: Cycle analysis (replaced by spoke/ring structure, since G is a tree) ---
fig, axes = plt.subplots(2, 2, figsize=(15, 13))

ax = axes[0, 0]
for axis_name, nodes in AXES.items():
    for i in range(len(nodes) - 1):
        x1, y1 = POSITIONS[nodes[i]]
        x2, y2 = POSITIONS[nodes[i + 1]]
        ax.plot([x1, x2], [y1, y2], color=AXIS_COLORS[axis_name],
                linewidth=3, alpha=0.8, zorder=1)
draw_nodes(ax)
ax.set_title("Spider tree: six spokes of length 3", fontsize=13, fontweight="bold")
ax.set_xlim(-4.6, 4.6)
ax.set_ylim(-4.6, 4.6)
ax.set_aspect("equal")
ax.axis("off")

ax = axes[0, 1]
draw_ring_guides(ax)
draw_axis_lines(ax, linewidth=1.5, alpha=0.4)
ring_colors = {1: "#44AA44", 2: "#CC9944", 3: "#4488CC"}
for d, members in RINGS.items():
    for n in members:
        x, y = POSITIONS[n]
        ax.add_patch(
            plt.Circle((x, y), 0.32, facecolor=ring_colors[d],
                       edgecolor="black", linewidth=2, zorder=2)
        )
        ax.text(x, y, str(n), ha="center", va="center", fontsize=10,
                fontweight="bold", color="white", zorder=3)
cx, cy = POSITIONS[CENTER]
ax.add_patch(plt.Circle((cx, cy), 0.32, facecolor="#FFCCCC",
                        edgecolor="#AA0000", linewidth=3, zorder=2))
ax.text(cx, cy, str(CENTER), ha="center", va="center", fontsize=10,
        fontweight="bold", zorder=3)
ax.set_title("Concentric rings d1·d2·d3 around the center (each sums 61)",
             fontsize=13, fontweight="bold")
ax.set_xlim(-4.6, 4.6)
ax.set_ylim(-4.6, 4.6)
ax.set_aspect("equal")
ax.axis("off")

ax = axes[1, 0]
ax.text(
    0.5, 0.5,
    "Tree graph — no cycles\n\n"
    f"{G.number_of_nodes()} nodes · {G.number_of_edges()} edges · 1 connected component\n"
    "Cycle basis = empty set\n"
    "Girth (minimum cycle length) is undefined\n\n"
    "Instead, the structure consists of\n6 spokes and 3 concentric rings (d1, d2, d3)",
    ha="center", va="center", fontsize=12,
    bbox=dict(boxstyle="round,pad=0.6", facecolor="lightyellow", edgecolor="black"),
)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

ax = axes[1, 1]
levels = ["Center (d0)", "Inner (d1)", "Middle (d2)", "Outer (d3)"]
level_sums = [CENTER] + [RING_SUMS[d] for d in [1, 2, 3]]
bars = ax.bar(levels, level_sums,
              color=["#FFCCCC", ring_colors[1], ring_colors[2], ring_colors[3]],
              edgecolor="black", linewidth=1.5)
ax.axhline(y=61, color="red", linestyle="--", linewidth=2)
ax.text(2.5, 62.5, "61 = (190-7)/3", color="red", fontsize=11, ha="center")
for bar, val in zip(bars, level_sums):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, str(val),
            ha="center", fontsize=12, fontweight="bold")
ax.set_title("Sum by distance level", fontsize=13, fontweight="bold")
ax.set_ylabel("Sum", fontsize=10)
ax.set_ylim(0, 75)

plt.tight_layout()
save_fig("04_cycle_analysis.png")
plt.close()

# --- 05: Centrality + sum invariants ---
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

ax = axes[0, 0]
degrees = dict(G.degree())
nodes_sorted = sorted(G.nodes(), key=lambda n: (degrees[n], n), reverse=True)
colors_sorted = [PHASE_COLOR[phase_of(n)] for n in nodes_sorted]
ax.bar(range(19), [degrees[n] for n in nodes_sorted], color=colors_sorted, edgecolor="black")
ax.set_xticks(range(19))
ax.set_xticklabels([str(n) for n in nodes_sorted], fontsize=7)
ax.set_title("Degree (center 6 · d1/d2 nodes 2 · endpoints 1)", fontsize=12, fontweight="bold")
ax.set_ylabel("Degree", fontsize=10)

ax = axes[0, 1]
betw_sorted = sorted(G.nodes(), key=lambda n: (betw[n], n), reverse=True)
colors_b = [PHASE_COLOR[phase_of(n)] for n in betw_sorted]
ax.bar(range(19), [betw[n] for n in betw_sorted], color=colors_b, edgecolor="black")
ax.set_xticks(range(19))
ax.set_xticklabels([str(n) for n in betw_sorted], fontsize=7)
ax.set_title("Betweenness centrality (center 7 dominates)", fontsize=12, fontweight="bold")
ax.set_ylabel("Centrality", fontsize=10)

ax = axes[1, 0]
wx_names = PHASES
wx_vals = [WX_SUMS[w] for w in wx_names]
wx_colors_bar = [PHASE_COLOR[w] for w in wx_names]
bars = ax.bar(wx_names, wx_vals, color=wx_colors_bar, edgecolor="black", linewidth=1.5)
for bar, val in zip(bars, wx_vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, str(val),
            ha="center", fontsize=12, fontweight="bold")
ax.plot(range(5), [30, 34, 38, 42, 46], "o--", color="black", alpha=0.4, linewidth=1.5)
ax.set_title("Wuxing class sums (Earth..Metal: arithmetic, common difference 4)",
             fontsize=12, fontweight="bold")
ax.set_ylabel("Sum", fontsize=10)

ax = axes[1, 1]
axis_names = list(AXES.keys())
axis_sums = [sum(AXES[a]) for a in axis_names]
bars = ax.bar([AXIS_LABELS[a] for a in axis_names], axis_sums,
              color=[AXIS_COLORS[a] for a in axis_names], edgecolor="black", linewidth=1.5)
ax.axhline(y=68, color="red", linestyle="--", linewidth=2)
for bar, val in zip(bars, axis_sums):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, str(val),
            ha="center", fontsize=12, fontweight="bold")
ax.set_title("Axis sums (3 × 68 = 204 = 190 + 2×7)", fontsize=12, fontweight="bold")
ax.set_ylabel("Sum", fontsize=10)
ax.set_ylim(0, 80)

plt.tight_layout()
save_fig("05_centrality_invariants.png")
plt.close()

# --- 06: Wuxing generation/overcoming ---
fig, axes = plt.subplots(1, 2, figsize=(15, 6.5))
ax = axes[0]
phase_graph = nx.DiGraph()
phase_relations = [(u, v, "generation") for u, v in GENERATION] + \
                  [(u, v, "overcoming") for u, v in OVERCOMING]
for u, v, r in phase_relations:
    phase_graph.add_edge(u, v, relation=r)
wx_pos = {"Water": (0, 2), "Wood": (2, 1), "Fire": (1, -1), "Earth": (-1, -1), "Metal": (-2, 1)}
sheng_edges = [(u, v) for u, v, r in phase_relations if r == "generation"]
ke_edges = [(u, v) for u, v, r in phase_relations if r == "overcoming"]
nx.draw_networkx_edges(phase_graph, wx_pos, edgelist=sheng_edges, edge_color="#44AA44",
                       width=3, alpha=0.8, arrows=True, arrowsize=20,
                       connectionstyle="arc3,rad=0.15", ax=ax)
nx.draw_networkx_edges(phase_graph, wx_pos, edgelist=ke_edges, edge_color="#CC4444",
                       width=2, alpha=0.6, style="--", arrows=True, arrowsize=15,
                       connectionstyle="arc3,rad=-0.15", ax=ax)
wx_node_colors = [PHASE_COLOR[w] for w in phase_graph.nodes()]
nx.draw_networkx_nodes(phase_graph, wx_pos, node_color=wx_node_colors, node_size=3000,
                       edgecolors="black", linewidths=2.5, ax=ax)
nx.draw_networkx_labels(phase_graph, wx_pos,
                        labels={n: n for n in phase_graph.nodes()},
                        font_size=14, ax=ax)
legend_elements = [
    Line2D([0], [0], color="#44AA44", lw=3, label="Generation"),
    Line2D([0], [0], color="#CC4444", lw=2, linestyle="--", label="Overcoming"),
]
ax.legend(handles=legend_elements, loc="upper right", fontsize=11)
ax.set_title("Wuxing generation / overcoming pentagram", fontsize=13, fontweight="bold")
ax.set_xlim(-3, 3.5)
ax.set_ylim(-2.5, 3)
ax.axis("off")

ax = axes[1]
pie_order = ["generation", "overcoming", "same_phase"]
pie_counts = [wx_edge_counts.get(k, 0) for k in pie_order]
colors_pie = ["#44AA44", "#CC4444", "#CC9944"]
ax.pie(pie_counts, labels=[RELATION_LABELS[k] for k in pie_order], autopct="%1.1f%%",
       colors=colors_pie, explode=[0.05] * 3,
       textprops={"fontsize": 12, "fontweight": "bold"})
ax.set_title(f"Wuxing edge distribution (N={G.number_of_edges()})", fontsize=13, fontweight="bold")
plt.tight_layout()
save_fig("06_wuxing_relations.png")
plt.close()

# --- 07: Extensions and generalization ---
fig, axes = plt.subplots(1, 2, figsize=(15, 6.5))

ax = axes[0]
fam_names = [row[0] for row in FAMILY_ROWS]
x = np.arange(len(FAMILY_ROWS))
width = 0.35
bars1 = ax.bar(x - width / 2, [row[5] for row in FAMILY_ROWS], width,
               label="Axis sum S", color="#4488CC", edgecolor="black")
bars2 = ax.bar(x + width / 2, [row[6] for row in FAMILY_ROWS], width,
               label="Ring sum R", color="#CC9944", edgecolor="black")
for bar in list(bars1) + list(bars2):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
            str(int(bar.get_height())), ha="center", fontsize=11, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels([f"{n}\na={r[1]}, L={r[2]}, N={r[3]}" for n, r in zip(fam_names, FAMILY_ROWS)],
                   fontsize=10)
ax.set_title("Star family: N = a(L-1)+1, S = (T+(a-1)L)/a, R = (T-L)/a",
             fontsize=12, fontweight="bold")
ax.legend(fontsize=10)
ax.set_ylabel("Sum", fontsize=10)

ax = axes[1]
# Skeleton schematics of the three family members (center + a axes × (L-1)/2 levels)
offsets = {"Beomsu-yong-odo": (-2.6, 0), "Jangchaek-yong-chil-do": (0, 0), "Jungsang-yong-gudo": (2.8, 0)}
scales = {"Beomsu-yong-odo": 0.5, "Jangchaek-yong-chil-do": 0.38, "Jungsang-yong-gudo": 0.30}
for (name, a, L), (ox, oy) in zip(FAMILY, offsets.values()):
    sc = scales[name]
    levels_per_spoke = (L - 1) // 2
    for i in range(a):
        ang = math.radians(90 + i * 360 / a)
        for sign in [1, -1]:
            prev = (ox, oy)
            for lev in range(1, levels_per_spoke + 1):
                px = ox + sign * lev * sc * math.cos(ang)
                py = oy + sign * lev * sc * math.sin(ang)
                ax.plot([prev[0], px], [prev[1], py], color="#888888", linewidth=1.2, zorder=1)
                ax.add_patch(plt.Circle((px, py), 0.09, facecolor="white",
                                        edgecolor="#333333", linewidth=1.2, zorder=2))
                prev = (px, py)
    ax.add_patch(plt.Circle((ox, oy), 0.16, facecolor="#FFCCCC",
                            edgecolor="#AA0000", linewidth=2, zorder=3))
    ax.text(ox, oy, str(L), ha="center", va="center", fontsize=8,
            fontweight="bold", zorder=4)
    ax.text(ox, oy - 1.6, f"{name}\na={a}, L={L}, N={a * (L - 1) + 1}",
            ha="center", va="top", fontsize=10, fontweight="bold")
ax.set_xlim(-4.3, 4.3)
ax.set_ylim(-2.6, 1.6)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("Star skeletons: center L + a axes × (L-1)/2 levels", fontsize=12, fontweight="bold")

plt.tight_layout()
save_fig("07_local_extensions.png")
plt.close()

# --- 08: Position patterns (rings / spokes / antipodal pairs) ---
fig, axes = plt.subplots(1, 2, figsize=(15, 6.5))

ax = axes[0]
ring_items = [(RING_LABELS[d], RING_SUMS[d]) for d in [1, 2, 3]]
spoke_items = sorted(SPOKES.items(), key=lambda kv: sum(kv[1]))
labels_bar = [k for k, _ in ring_items] + [k for k, _ in spoke_items]
vals_bar = [v for _, v in ring_items] + [sum(s) for _, s in spoke_items]
colors_bar = ["#44AA44"] * 3 + ["#4488CC"] * 6
bars = ax.bar(range(len(vals_bar)), vals_bar, color=colors_bar, edgecolor="black", linewidth=1.2)
ax.axhline(y=61, color="red", linestyle="--", linewidth=2)
ax.text(len(vals_bar) - 1, 62.5, "61", color="red", fontsize=11, ha="right", fontweight="bold")
for bar, val in zip(bars, vals_bar):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, str(val),
            ha="center", fontsize=10, fontweight="bold")
ax.set_xticks(range(len(labels_bar)))
ax.set_xticklabels(labels_bar, fontsize=8, rotation=30, ha="right")
ax.set_title("Ring sums (61×3) and spoke sums (28–33, six consecutive integers)",
             fontsize=12, fontweight="bold")
ax.set_ylabel("Sum", fontsize=10)
ax.set_ylim(0, 72)

ax = axes[1]
matrix = np.array([PAIR_SUM_MATRIX[a] for a in AXES], dtype=float)
im = ax.imshow(matrix, cmap="YlOrRd", interpolation="nearest", vmin=15, vmax=26)
ax.set_xticks(range(3))
ax.set_yticks(range(3))
ax.set_xticklabels(["d1 pair", "d2 pair", "d3 pair"], fontsize=10)
ax.set_yticklabels([AXIS_LABELS[a] for a in AXES], fontsize=10)
for i in range(3):
    for j in range(3):
        ax.text(j, i, int(matrix[i, j]), ha="center", va="center",
                fontsize=13, fontweight="bold")
ax.set_title("Antipodal-pair sum matrix — row sums = column sums = 61\n(values only 17·20·21·24; 20 = 2×mean(1..19))",
             fontsize=12, fontweight="bold")
plt.colorbar(im, ax=ax, shrink=0.8)

plt.tight_layout()
save_fig("08_position_patterns.png")
plt.close()

print("\n" + "=" * 60)
print("Summary of verified key properties")
print("=" * 60)
print(f"  - Values: 1~19 each once, total 190")
print(f"  - 3 axes × 7 cells, axis sum 68, shared center 7: 3×68 = 204 = 190 + 2×7 (19 values, 21 cells)")
print(f"  - Graph: tree, 19 nodes 18 edges, degree distribution {dict(sorted(deg_counter.items(), reverse=True))}")
print(f"  - Ring sums: d1 = d2 = d3 = 61 = (190-7)/3")
print(f"  - Spoke sums: {spoke_sums_sorted} (28~33 consecutive), opposite spoke pairs sum 61")
print(f"  - Antipodal-pair sum matrix: row sums = column sums = 61 (values 17·20·21·24)")
print(f"  - Wuxing sums: Earth 30 · Water 34 · Fire 38 · Wood 42 · Metal 46 (common difference 4)")
print(f"  - Wuxing edges: " + ", ".join(
    f"{RELATION_LABELS[k]} {wx_edge_counts.get(k, 0)}" for k in ["generation", "overcoming", "same_phase"]))
print(f"  - Spectrum: lambda_max = {lambda_max:.4f}, lambda_min = {lambda_min:.4f}")
print("\nAll figures generated!")
print(f"Output directory: {OUTPUT_DIR.resolve()}/")
print("=" * 60)
