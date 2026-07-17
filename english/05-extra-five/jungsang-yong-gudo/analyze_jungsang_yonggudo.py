#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jungsang-yonggudo (象上用九圖) — Modern graph-theoretic and combinatorial deep analysis

A reinterpretation of Jungsang-yonggudo, one of the diagrams of the Gusuryak
(九數略) family, in modern mathematical language.
Analysis target: the numbers 1 through 33 arranged on 4 axes of 9 cells each
(each summing to 147) passing through the center 9, forming 4 concentric
octagonal rings (each summing to 138) — a star (spider) structure.
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
plt.rcParams["axes.unicode_minus"] = False

OUTPUT_DIR = Path(".")
SAVED_FIGURES: list[str] = []


def save_fig(name: str) -> None:
    path = OUTPUT_DIR / name
    plt.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    SAVED_FIGURES.append(name)
    print(f"[Saved] {path}")


# ============================================================
# 1. Source data structuring
# ============================================================

# Coordinates use the same geometry as visualize.py in this directory.
COORDS = {
    27: (-4, 4), 20: (0, 4), 33: (4, 4),
    15: (-2, 3), 16: (0, 3), 1: (2, 3),
    3: (-1.5, 2), 23: (0, 2), 13: (1.5, 2),
    24: (-1, 1), 10: (0, 1), 22: (1, 1),
    28: (-4, 0), 5: (-3, 0), 11: (-2, 0), 25: (-1, 0), 9: (0, 0),
    7: (1, 0), 19: (2, 0), 31: (3, 0), 12: (4, 0),
    18: (-1, -1), 2: (0, -1), 30: (1, -1),
    26: (-1.5, -2), 29: (0, -2), 14: (1.5, -2),
    17: (-2, -3), 32: (0, -3), 21: (2, -3),
    8: (-4, -4), 6: (0, -4), 4: (4, -4),
}

CENTER = 9

# The 4 symmetry axes: 9-cell lines running from one end through the center
# to the opposite end.
AXES = {
    "vertical": [20, 16, 23, 10, 9, 2, 29, 32, 6],
    "horizontal": [28, 5, 11, 25, 9, 7, 19, 31, 12],
    "diagonal1": [27, 15, 3, 24, 9, 30, 14, 21, 4],
    "diagonal2": [33, 1, 13, 22, 9, 18, 26, 17, 8],
}

AXIS_TARGET = 147   # target sum of each axis
RING_TARGET = 138   # target sum of each ring
RAY_TARGET = 69     # target sum of each ray
TOTAL_TARGET = 561  # total sum of 1..33

RESIDUE_STYLE = {
    1: {"face": "#E5E5E5", "edge": "#444444", "name": "Water"},
    2: {"face": "#F6D0D0", "edge": "#B54141", "name": "Fire"},
    3: {"face": "#D5E3FA", "edge": "#3D6DB3", "name": "Wood"},
    4: {"face": "#D7D7D7", "edge": "#1F1F1F", "name": "Metal"},
    0: {"face": "#F7E3A0", "edge": "#B58A00", "name": "Earth"},
}

AXIS_LABELS = {
    "vertical": "Vertical axis",
    "horizontal": "Horizontal axis",
    "diagonal1": "Diagonal axis 1",
    "diagonal2": "Diagonal axis 2",
}

RELATION_LABELS = {
    "generation": "Generation",
    "overcoming": "Overcoming",
    "same_phase": "Same phase",
    "neutral": "Neutral",
}

PHASE_COLOR = {
    "Water": "#4488CC",
    "Fire": "#CC4444",
    "Wood": "#44AA44",
    "Metal": "#888888",
    "Earth": "#CC9944",
}

AXIS_COLORS = {
    "vertical": "#CC4444",
    "horizontal": "#4488CC",
    "diagonal1": "#44AA44",
    "diagonal2": "#CC9944",
}

# Wuxing relations (generation: Wood->Fire->Earth->Metal->Water->Wood,
# overcoming: Wood->Earth->Water->Fire->Metal->Wood)
GENERATION_PAIRS = {
    frozenset(p)
    for p in [
        ("Wood", "Fire"), ("Fire", "Earth"), ("Earth", "Metal"),
        ("Metal", "Water"), ("Water", "Wood"),
    ]
}
OVERCOMING_PAIRS = {
    frozenset(p)
    for p in [
        ("Wood", "Earth"), ("Earth", "Water"), ("Water", "Fire"),
        ("Fire", "Metal"), ("Metal", "Wood"),
    ]
}

DIRECTION_EN = {
    90: "N", 45: "NE", 0: "E", -45: "SE",
    -90: "S", -135: "SW", 180: "W", 135: "NW",
}


def phase_of(n: int) -> str:
    return RESIDUE_STYLE[n % 5]["name"]


def residue_1based(n: int) -> int:
    r = n % 5
    return 5 if r == 0 else r


def compass_of(value: int) -> int:
    """Snap the bearing of `value` (relative to the origin center) to 45 degrees."""
    x, y = COORDS[value]
    ang = math.degrees(math.atan2(y, x))
    return int(round(ang / 45.0) * 45) if abs(ang) <= 180 else 0


def clockwise_from_top(values: list[int]) -> list[int]:
    """Sort by bearing so the list starts at 12 o'clock and runs clockwise."""
    return sorted(
        values,
        key=lambda v: math.atan2(COORDS[v][0], COORDS[v][1]) % (2 * math.pi),
    )


# ============================================================
# 2. Graph construction (spider tree: center + 8 rays)
# ============================================================

EDGES: list[tuple[int, int]] = []
for axis in AXES.values():
    for a, b in zip(axis, axis[1:]):
        EDGES.append(tuple(sorted((a, b))))
EDGES = sorted(set(EDGES))

G = nx.Graph()
G.add_nodes_from(range(1, 34))
G.add_edges_from(EDGES)
for n in G.nodes():
    G.nodes[n]["phase"] = phase_of(n)

# Concentric rings: sets of nodes at equal graph distance (BFS) from center 9.
DIST = nx.single_source_shortest_path_length(G, CENTER)
RINGS: dict[str, list[int]] = {}
for d in range(1, 5):
    RINGS[f"d{d}"] = sorted([n for n, dist in DIST.items() if dist == d])

# Rays: the 4-cell line on one side of the center within an axis
# (ordered from the center outward).
RAYS: dict[str, list[int]] = {}
for axis in AXES.values():
    i = axis.index(CENTER)
    for side in (axis[:i][::-1], axis[i + 1:]):
        direction = DIRECTION_EN[compass_of(side[-1])]
        RAYS[direction] = list(side)

RAY_COLORS = {
    "N": "#E41A1C", "NE": "#FF7F00", "E": "#B8860B", "SE": "#4DAF4A",
    "S": "#377EB8", "SW": "#984EA3", "W": "#A65628", "NW": "#F781BF",
}

RING_COLORS = {"d1": "#555555", "d2": "#777777", "d3": "#999999", "d4": "#BBBBBB"}


# ============================================================
# 3. Combinatorial and graph-theoretic analysis
# ============================================================

def validate() -> None:
    """Verify every key property of the source data; abort on any mismatch."""
    values = sorted(COORDS)
    if values != list(range(1, 34)):
        raise ValueError("Value set is not 1..33 each used once")
    total = sum(values)
    if total != TOTAL_TARGET:
        raise ValueError(f"Total sum is not {TOTAL_TARGET}: {total}")

    for name, axis in AXES.items():
        label = AXIS_LABELS[name]
        if len(axis) != 9:
            raise ValueError(f"{label} does not have 9 cells")
        if len(set(axis)) != 9:
            raise ValueError(f"{label} contains duplicate values")
        if sum(axis) != AXIS_TARGET:
            raise ValueError(f"{label} sum is not {AXIS_TARGET}: {sum(axis)}")
        if axis.count(CENTER) != 1 or axis[4] != CENTER:
            raise ValueError(f"Middle cell of {label} is not {CENTER}")

    # Overlap check: any two axes must meet only at the center 9.
    names = list(AXES)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            inter = set(AXES[names[i]]) & set(AXES[names[j]])
            if inter != {CENTER}:
                raise ValueError(f"{names[i]} and {names[j]} share more than the center: {inter}")
    k_times_s = len(AXES) * AXIS_TARGET
    duplication = (len(AXES) - 1) * CENTER  # center counted 4 times -> 3 extra
    if k_times_s != total + duplication:
        raise ValueError("Duplication equation k*S = T + D does not hold")

    # Ring check: 4 concentric rings of 8 cells each, every sum 138.
    for d, ring in RINGS.items():
        if len(ring) != 8:
            raise ValueError(f"Ring {d} does not have 8 cells")
        if sum(ring) != RING_TARGET:
            raise ValueError(f"Ring {d} sum is not {RING_TARGET}: {sum(ring)}")

    # Ray check: 8 rays of 4 cells each, every sum 69.
    if len(RAYS) != 8:
        raise ValueError("There are not exactly 8 rays")
    for direction, ray in RAYS.items():
        if len(ray) != 4:
            raise ValueError(f"Ray {direction} does not have 4 cells")
        if sum(ray) != RAY_TARGET:
            raise ValueError(f"Ray {direction} sum is not {RAY_TARGET}: {sum(ray)}")

    # All checks passed -- print the verified sum equations.
    print("[Validation passed] Verified sum equations:")
    for name, axis in AXES.items():
        print(f"  {AXIS_LABELS[name]}: {'+'.join(map(str, axis))} = {sum(axis)}")
    print(f"  Total sum: 1+...+33 = {total}")
    print(f"  Duplication: 4x{AXIS_TARGET} = {k_times_s} = {total} + 3x{CENTER} (33 made, 36 used)")
    for d, ring in RINGS.items():
        print(f"  Ring {d}: {'+'.join(map(str, ring))} = {sum(ring)}")
    print(f"  Ring balance: 4x{RING_TARGET} = {4 * RING_TARGET} = {total} - {CENTER}")
    for direction, ray in RAYS.items():
        print(f"  Ray {direction}: {'+'.join(map(str, ray))} = {sum(ray)}")


validate()

print()
print("=" * 60)
print("Jungsang-yonggudo -- modern graph and combinatorial analysis")
print("=" * 60)
print(f"Nodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")
print(f"Connected components: {nx.number_connected_components(G)}")
print(f"Is tree: {nx.is_tree(G)}")
print(f"Diameter: {nx.diameter(G)}")

deg_seq = sorted([d for _, d in G.degree()], reverse=True)
deg_counter = Counter(d for _, d in G.degree())
print(f"Degree sequence: {deg_seq}")
print(f"Degree distribution: {dict(sorted(deg_counter.items(), reverse=True))}")

print("\nWuxing class sums:")
WUXING_SUMS: dict[str, int] = {}
for r in [1, 2, 3, 4, 5]:
    nodes = [n for n in range(1, 34) if residue_1based(n) == r]
    wx = RESIDUE_STYLE[r % 5]["name"]
    WUXING_SUMS[wx] = sum(nodes)
    print(f"  {wx} ({r}): {len(nodes)} numbers, sum={sum(nodes)}, values={nodes}")

print("\nWuxing distribution per axis:")
for name, axis in AXES.items():
    counts = Counter(phase_of(v) for v in axis)
    print(f"  {AXIS_LABELS[name]}: {dict(sorted(counts.items()))}")

print("\nWuxing distribution per ring:")
for d, ring in RINGS.items():
    counts = Counter(phase_of(v) for v in ring)
    print(f"  {d}: {dict(sorted(counts.items()))}")

betw = nx.betweenness_centrality(G)
print("\nBetweenness centrality (Top 10):")
for n, v in sorted(betw.items(), key=lambda x: (-x[1], x[0]))[:10]:
    print(f"  {n} ({phase_of(n)}, distance {DIST[n]}): {v:.3f}")

cycle_basis = nx.cycle_basis(G)
print(f"\nCycle basis size: {len(cycle_basis)} (tree -- no cycles)")

# Wuxing edge classification
wx_edge_counts: dict[str, int] = {}
for u, v in G.edges():
    pair = frozenset((phase_of(u), phase_of(v)))
    if phase_of(u) == phase_of(v):
        key = "same_phase"
    elif pair in GENERATION_PAIRS:
        key = "generation"
    elif pair in OVERCOMING_PAIRS:
        key = "overcoming"
    else:
        key = "neutral"
    wx_edge_counts[key] = wx_edge_counts.get(key, 0) + 1

print("\nWuxing edge distribution:")
total_edges = G.number_of_edges()
for key in ["generation", "overcoming", "same_phase", "neutral"]:
    cnt = wx_edge_counts.get(key, 0)
    print(f"  {RELATION_LABELS[key]}: {cnt} ({100.0 * cnt / total_edges:.1f}%)")

# Spectral analysis
RESIDUE_ORDER = {1: 0, 2: 1, 3: 2, 4: 3, 0: 4}
nodelist = sorted(G.nodes(), key=lambda n: (RESIDUE_ORDER[n % 5], n))
adj = nx.to_numpy_array(G, nodelist=nodelist)
eigenvalues = np.linalg.eigvalsh(adj)
lambda_max = float(max(eigenvalues))
lambda_min = float(min(eigenvalues))
print(f"\nAdjacency spectrum: lambda_max = {lambda_max:.4f}, lambda_min = {lambda_min:.4f}")

# ============================================================
# 4. Position-based analysis (rings / rays / axes)
# ============================================================

RING_SUMS = {d: sum(ring) for d, ring in RINGS.items()}
RAY_SUMS = {direction: sum(ray) for direction, ray in RAYS.items()}
AXIS_SUMS = {name: sum(axis) for name, axis in AXES.items()}

print("\nRing sums:")
for d, ring in RINGS.items():
    print(f"  {d} (distance {d[1]}): {ring} -> sum {RING_SUMS[d]}")

print("\nRay sums (center -> outward):")
for direction, ray in RAYS.items():
    print(f"  {direction}: {ray} -> sum {RAY_SUMS[direction]}")

print("\nAxis decomposition (ray + center + ray):")
for name, axis in AXES.items():
    i = axis.index(CENTER)
    left, right = axis[:i], axis[i + 1:]
    print(
        f"  {AXIS_LABELS[name]}: {sum(left)} + {CENTER} + {sum(right)} = {AXIS_SUMS[name]}"
    )

# ============================================================
# 5. Generalization family (star family: a axes of L cells)
# ============================================================

def family_params(a: int, L: int) -> tuple[int, int, int, int, int]:
    """Structural parameters for a axes of L cells (shared center), center value c=L."""
    N = a * (L - 1) + 1
    T = N * (N + 1) // 2
    c = L
    S = (T + (a - 1) * c) // a
    R = 2 * (T - c) // (L - 1)
    return N, T, c, S, R


FAMILY = [
    ("Beomsu-yong-odo", 2, 5),
    ("Jangchaek-yong-chil-do", 3, 7),
    ("Jungsang-yonggudo", 4, 9),
]

print("\nGeneralization family (a axes, L cells per axis, center c=L, N=a(L-1)+1):")
for label, a, L in FAMILY:
    N, T, c, S, R = family_params(a, L)
    print(f"  {label}: a={a}, L={L} -> N={N}, T={T}, c={c}, axis sum S={S}, ring sum R={R}")

# ============================================================
# 6. Visualization
# ============================================================

def draw_ring_polygons(ax, labeled: bool = True, colorful: bool = False) -> None:
    for d, ring in RINGS.items():
        order = clockwise_from_top(ring)
        xs = [COORDS[v][0] for v in order] + [COORDS[order[0]][0]]
        ys = [COORDS[v][1] for v in order] + [COORDS[order[0]][1]]
        color = PHASE_COLOR[["Water", "Fire", "Wood", "Metal"][int(d[1]) - 1]] if colorful else RING_COLORS[d]
        ax.plot(xs, ys, color=color, linewidth=1.5, linestyle=(0, (4, 4)), alpha=0.9, zorder=0)
        if labeled:
            top = max(ring, key=lambda v: COORDS[v][1])
            tx, ty = COORDS[top]
            ax.text(
                tx + 0.15, ty + 0.35,
                f"Ring {d} sum={RING_SUMS[d]}",
                ha="left", va="bottom", fontsize=9, color="#333333",
            )


def draw_nodes(ax, values=None, radius=0.34, fontsize=10) -> None:
    for value, (x, y) in COORDS.items():
        if values is not None and value not in values:
            continue
        style = RESIDUE_STYLE[value % 5]
        face, edge, lw, rad = style["face"], style["edge"], 2.0, radius
        if value == CENTER:
            edge, lw, rad = "#000000", 3.5, radius + 0.08
        ax.add_patch(
            plt.Circle((x, y), rad, facecolor=face, edgecolor=edge, linewidth=lw, zorder=2)
        )
        ax.text(x, y, str(value), ha="center", va="center",
                fontsize=fontsize, fontweight="bold", zorder=3)


def draw_axis_edges(ax, alpha=0.6, linewidth=2.5) -> None:
    for name, axis in AXES.items():
        for a, b in zip(axis, axis[1:]):
            x1, y1 = COORDS[a]
            x2, y2 = COORDS[b]
            ax.plot([x1, x2], [y1, y2], color=AXIS_COLORS[name],
                    linewidth=linewidth, alpha=alpha, zorder=1)


# --- 01: Original graph ---
fig, ax = plt.subplots(figsize=(12, 12))
draw_ring_polygons(ax)
draw_axis_edges(ax)
draw_nodes(ax)
ax.set_title(
    "Jungsang-yonggudo -- Original star structure\n"
    "4 axes of 9 cells, axis sum 147, 4 ring sums 138, total 561",
    fontsize=16, fontweight="bold",
)
ax.set_xlim(-5.4, 5.4)
ax.set_ylim(-5.4, 5.9)
ax.set_aspect("equal")
ax.axis("off")
wuxing_handles = [
    mpatches.Patch(facecolor=PHASE_COLOR[wx], edgecolor="black", label=wx)
    for wx in ["Water", "Fire", "Wood", "Metal", "Earth"]
]
leg1 = ax.legend(handles=wuxing_handles, loc="lower right", fontsize=10, framealpha=0.9)
ax.add_artist(leg1)
axis_handles = [
    Line2D([0], [0], color=AXIS_COLORS[name], lw=2.5, label=AXIS_LABELS[name])
    for name in AXES
]
ax.legend(handles=axis_handles, loc="upper left", fontsize=10, framealpha=0.9)
save_fig("01_original_graph.png")
plt.close()

# --- 02: Wuxing subgraph decomposition ---
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()
ax = axes[0]
draw_ring_polygons(ax, labeled=False)
draw_axis_edges(ax, alpha=0.3, linewidth=1.5)
draw_nodes(ax, radius=0.3, fontsize=9)
ax.set_title("Full graph", fontsize=13, fontweight="bold")
ax.set_xlim(-5.2, 5.2)
ax.set_ylim(-5.2, 5.2)
ax.set_aspect("equal")
ax.axis("off")

for idx, wx in enumerate(["Water", "Fire", "Wood", "Metal", "Earth"]):
    ax = axes[idx + 1]
    wx_nodes = [n for n in range(1, 34) if phase_of(n) == wx]
    for a, b in EDGES:
        x1, y1 = COORDS[a]
        x2, y2 = COORDS[b]
        ax.plot([x1, x2], [y1, y2], color="#EEEEEE", linewidth=1, alpha=0.5, zorder=0)
    for n in range(1, 34):
        if n in wx_nodes:
            continue
        x, y = COORDS[n]
        ax.add_patch(plt.Circle((x, y), 0.24, facecolor="#F0F0F0",
                                edgecolor="#CCCCCC", linewidth=1, zorder=1))
        ax.text(x, y, str(n), ha="center", va="center", fontsize=8, color="#AAAAAA", zorder=2)
    for n in wx_nodes:
        x, y = COORDS[n]
        ax.add_patch(plt.Circle((x, y), 0.36, facecolor=PHASE_COLOR[wx],
                                edgecolor="black", linewidth=2.5, zorder=2))
        ax.text(x, y, str(n), ha="center", va="center", fontsize=10,
                fontweight="bold",
                color="white" if wx in ["Water", "Wood"] else "black", zorder=3)
    ax.set_title(
        f"{wx} - {len(wx_nodes)} numbers - sum {WUXING_SUMS[wx]}",
        fontsize=12, fontweight="bold", color=PHASE_COLOR[wx],
    )
    ax.set_xlim(-5.2, 5.2)
    ax.set_ylim(-5.2, 5.2)
    ax.set_aspect("equal")
    ax.axis("off")

plt.suptitle("Wuxing (five phases) subgraph decomposition", fontsize=16, fontweight="bold", y=1.0)
plt.tight_layout()
save_fig("02_wuxing_decomposition.png")
plt.close()

# --- 03: Adjacency matrix + spectrum ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
im = ax.imshow(adj, cmap="YlOrRd", interpolation="nearest")
ax.set_xticks(range(33))
ax.set_yticks(range(33))
ax.set_xticklabels(nodelist, fontsize=6)
ax.set_yticklabels(nodelist, fontsize=6)
wx_sorted = [phase_of(n) for n in nodelist]
boundaries = [i - 0.5 for i in range(1, 33) if wx_sorted[i] != wx_sorted[i - 1]]
for b in boundaries:
    ax.axhline(y=b, color="blue", linewidth=1.5, alpha=0.7)
    ax.axvline(x=b, color="blue", linewidth=1.5, alpha=0.7)
plt.colorbar(im, ax=ax, shrink=0.8)
ax.set_title("Adjacency matrix (wuxing block order)", fontsize=13, fontweight="bold")

ax = axes[1]
ax.bar(range(len(eigenvalues)), sorted(eigenvalues, reverse=True),
       color="#4488CC", edgecolor="black", alpha=0.8)
ax.axhline(y=0, color="red", linestyle="--", linewidth=1)
ax.set_xlabel("Index", fontsize=11)
ax.set_ylabel("Eigenvalue", fontsize=11)
ax.set_title(
    f"Graph spectrum\nlambda_max={lambda_max:.2f}, lambda_min={lambda_min:.2f}",
    fontsize=13, fontweight="bold",
)
ax.grid(True, alpha=0.3)
plt.tight_layout()
save_fig("03_adjacency_spectrum.png")
plt.close()

# --- 04: Cycle analysis (tree -> ray/ring structure instead) ---
fig, axes = plt.subplots(2, 2, figsize=(16, 14))

ax = axes[0, 0]
# Color each edge by the ray it belongs to.
edge_ray: dict[tuple[int, int], str] = {}
for direction, ray in RAYS.items():
    chain = [CENTER] + ray
    for a, b in zip(chain, chain[1:]):
        edge_ray[tuple(sorted((a, b)))] = direction
for (a, b), direction in edge_ray.items():
    x1, y1 = COORDS[a]
    x2, y2 = COORDS[b]
    ax.plot([x1, x2], [y1, y2], color=RAY_COLORS[direction], linewidth=3, alpha=0.75, zorder=1)
draw_nodes(ax)
ax.set_title("Eight-ray structure -- spider tree", fontsize=13, fontweight="bold")
ax.set_xlim(-5.2, 5.2)
ax.set_ylim(-5.2, 5.2)
ax.set_aspect("equal")
ax.axis("off")

ax = axes[0, 1]
for a, b in EDGES:
    x1, y1 = COORDS[a]
    x2, y2 = COORDS[b]
    ax.plot([x1, x2], [y1, y2], color="#DDDDDD", linewidth=1.2, alpha=0.6, zorder=0)
draw_ring_polygons(ax, colorful=True)
draw_nodes(ax, radius=0.28, fontsize=9)
ax.set_title("Concentric ring levels (graph distance d1-d4 from center)", fontsize=13, fontweight="bold")
ax.set_xlim(-5.2, 5.2)
ax.set_ylim(-5.2, 5.9)
ax.set_aspect("equal")
ax.axis("off")

ax = axes[1, 0]
ray_names = list(RAYS)
ray_vals = [RAY_SUMS[direction] for direction in ray_names]
ax.bar(ray_names, ray_vals, color=[RAY_COLORS[d] for d in ray_names],
       edgecolor="black", linewidth=1.5)
ax.axhline(y=RAY_TARGET, color="red", linestyle="--", linewidth=2)
for bar, val in zip(ax.patches, ray_vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, str(val),
            ha="center", fontsize=12, fontweight="bold")
ax.set_ylim(0, 82)
ax.set_title("4-cell sum of each ray -- all equal to 69", fontsize=13, fontweight="bold")
ax.set_ylabel("Sum", fontsize=10)

ax = axes[1, 1]
ax.text(
    0.5, 0.5,
    "Tree graph (no cycles)\n\n"
    f"Nodes N = 33, edges E = 32 = N - 1\n"
    f"Components: 1 - cycle basis size: {len(cycle_basis)}\n"
    f"Diameter: {nx.diameter(G)} (leaf -> center -> leaf)\n"
    "Bipartite graph => spectrum symmetric about 0",
    ha="center", va="center", fontsize=13, fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.6", facecolor="lightyellow", edgecolor="black"),
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
degrees = dict(G.degree())
nodes_sorted = sorted(G.nodes(), key=lambda n: (-degrees[n], n))
ax.bar(range(33), [degrees[n] for n in nodes_sorted],
       color=[PHASE_COLOR[phase_of(n)] for n in nodes_sorted], edgecolor="black")
ax.set_xticks(range(33))
ax.set_xticklabels([str(n) for n in nodes_sorted], fontsize=7)
ax.set_title("Degree (center 8; 24 inner nodes 2; 8 leaves 1)", fontsize=12, fontweight="bold")
ax.set_ylabel("Degree", fontsize=10)

ax = axes[0, 1]
betw_sorted = sorted(G.nodes(), key=lambda n: (-betw[n], n))
ax.bar(range(33), [betw[n] for n in betw_sorted],
       color=[PHASE_COLOR[phase_of(n)] for n in betw_sorted], edgecolor="black")
ax.set_xticks(range(33))
ax.set_xticklabels([str(n) for n in betw_sorted], fontsize=7)
ax.set_title("Betweenness centrality (constant per ring level)", fontsize=12, fontweight="bold")
ax.set_ylabel("Centrality", fontsize=10)

ax = axes[1, 0]
wx_names = ["Water", "Fire", "Wood", "Metal", "Earth"]
wx_vals = [WUXING_SUMS[w] for w in wx_names]
ax.bar(wx_names, wx_vals,
       color=[PHASE_COLOR[w] for w in wx_names], edgecolor="black", linewidth=1.5)
for bar, val in zip(ax.patches, wx_vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2, str(val),
            ha="center", fontsize=12, fontweight="bold")
ax.set_title("Wuxing class sums (112, 119, 126, 99, 105)", fontsize=12, fontweight="bold")
ax.set_ylabel("Sum", fontsize=10)

ax = axes[1, 1]
axis_names = list(AXES)
axis_vals = [AXIS_SUMS[n] for n in axis_names]
ax.bar([AXIS_LABELS[n] for n in axis_names], axis_vals,
       color=[AXIS_COLORS[n] for n in axis_names], edgecolor="black", linewidth=1.5)
ax.axhline(y=AXIS_TARGET, color="red", linestyle="--", linewidth=2)
for bar, val in zip(ax.patches, axis_vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2, str(val),
            ha="center", fontsize=12, fontweight="bold")
ax.set_ylim(0, 175)
ax.set_title("9-cell sum of each axis -- all equal to 147", fontsize=12, fontweight="bold")
ax.set_ylabel("Sum", fontsize=10)
plt.setp(ax.xaxis.get_majorticklabels(), rotation=15, ha="right")

plt.tight_layout()
save_fig("05_centrality_invariants.png")
plt.close()

# --- 06: Wuxing generation/overcoming relations ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
phase_graph = nx.DiGraph()
phase_relations = [
    ("Water", "Wood", "generation"),
    ("Wood", "Fire", "generation"),
    ("Fire", "Earth", "generation"),
    ("Earth", "Metal", "generation"),
    ("Metal", "Water", "generation"),
    ("Water", "Fire", "overcoming"),
    ("Fire", "Metal", "overcoming"),
    ("Metal", "Wood", "overcoming"),
    ("Wood", "Earth", "overcoming"),
    ("Earth", "Water", "overcoming"),
]
for u, v, r in phase_relations:
    phase_graph.add_edge(u, v, relation=r)
wx_pos = {"Water": (0, 2), "Wood": (2, 1), "Fire": (1, -1), "Earth": (-1, -1), "Metal": (-2, 1)}
sheng_edges = [(u, v) for u, v, r in phase_relations if r == "generation"]
ke_edges = [(u, v) for u, v, r in phase_relations if r == "overcoming"]
nx.draw_networkx_edges(phase_graph, wx_pos, edgelist=sheng_edges,
                       edge_color="#44AA44", width=3, alpha=0.8, arrows=True,
                       arrowsize=20, connectionstyle="arc3,rad=0.15", ax=ax)
nx.draw_networkx_edges(phase_graph, wx_pos, edgelist=ke_edges,
                       edge_color="#CC4444", width=2, alpha=0.6, style="--",
                       arrows=True, arrowsize=15, connectionstyle="arc3,rad=-0.15", ax=ax)
nx.draw_networkx_nodes(phase_graph, wx_pos,
                       node_color=[PHASE_COLOR[w] for w in phase_graph.nodes()],
                       node_size=3000, edgecolors="black", linewidths=2.5, ax=ax)
nx.draw_networkx_labels(phase_graph, wx_pos, font_size=13, ax=ax)
ax.legend(handles=[
    Line2D([0], [0], color="#44AA44", lw=3, label="Generation"),
    Line2D([0], [0], color="#CC4444", lw=2, linestyle="--", label="Overcoming"),
], loc="upper right", fontsize=11)
ax.set_title("Wuxing generation/overcoming relation diagram", fontsize=13, fontweight="bold")
ax.set_xlim(-3, 3.5)
ax.set_ylim(-2.5, 3)
ax.axis("off")

ax = axes[1]
pie_keys = [k for k in ["generation", "overcoming", "same_phase", "neutral"]
            if wx_edge_counts.get(k, 0) > 0]
pie_colors = {"generation": "#44AA44", "overcoming": "#CC4444",
              "same_phase": "#CC9944", "neutral": "#4488CC"}
ax.pie(
    [wx_edge_counts[k] for k in pie_keys],
    labels=[f"{RELATION_LABELS[k]}\n{wx_edge_counts[k]} edges" for k in pie_keys],
    autopct="%1.1f%%",
    colors=[pie_colors[k] for k in pie_keys],
    explode=[0.05] * len(pie_keys),
    textprops={"fontsize": 12, "fontweight": "bold"},
)
ax.set_title(f"Wuxing edge distribution (N={total_edges})", fontsize=13, fontweight="bold")
plt.tight_layout()
save_fig("06_wuxing_relations.png")
plt.close()

# --- 07: Extensions and generalization ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

ax = axes[0]
fam_labels = []
fam_S = []
fam_R = []
for label, a, L in FAMILY:
    N, T, c, S, R = family_params(a, L)
    fam_labels.append(f"{label}\na={a}, L={L}")
    fam_S.append(S)
    fam_R.append(R)
x = np.arange(len(FAMILY))
width = 0.35
bars1 = ax.bar(x - width / 2, fam_S, width, label="Axis sum S", color="#4488CC", edgecolor="black")
bars2 = ax.bar(x + width / 2, fam_R, width, label="Ring sum R", color="#CC9944", edgecolor="black")
for bars in (bars1, bars2):
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                str(int(bar.get_height())), ha="center", fontsize=11, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(fam_labels, fontsize=9)
ax.set_title("Star generalization family: a axes, L cells, center c=L", fontsize=13, fontweight="bold")
ax.legend(fontsize=11)
ax.set_ylabel("Sum", fontsize=10)

ax = axes[1]
for k in range(4):
    ang = math.radians(90 + k * 45)
    dx, dy = math.cos(ang), math.sin(ang)
    ax.plot([-4.6 * dx, 4.6 * dx], [-4.6 * dy, 4.6 * dy],
            color="#999999", linewidth=1.5, linestyle=(0, (4, 4)), zorder=0)
for r in [1.3, 2.3, 3.3, 4.3]:
    ax.add_patch(plt.Circle((0, 0), r, fill=False, color="#4488CC",
                            linewidth=1.2, linestyle=":", alpha=0.8))
ax.add_patch(plt.Circle((0, 0), 0.42, facecolor="#F7E3A0", edgecolor="black", linewidth=2, zorder=2))
ax.text(0, 0, "c", ha="center", va="center", fontsize=12, fontweight="bold", zorder=3)
ax.text(
    0, -5.6,
    "N = a(L-1)+1, T = N(N+1)/2, S = (T+(a-1)c)/a, R = 2(T-c)/(L-1)\n"
    "Next candidate: a=5, L=11 -> N=51, S=274, R=263 (hypothesis, unverified)",
    ha="center", va="center", fontsize=11,
    bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", edgecolor="black"),
)
ax.set_xlim(-5.6, 5.6)
ax.set_ylim(-6.4, 5.4)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("General schema of the star structure (a axes, L cells, rings)", fontsize=13, fontweight="bold")

plt.tight_layout()
save_fig("07_local_extensions.png")
plt.close()

# --- 08: Position patterns (rings / rays / axis decomposition) ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

ax = axes[0]
ring_names = list(RINGS)
ring_vals = [RING_SUMS[d] for d in ring_names]
ax.bar(ring_names, ring_vals,
       color=[RING_COLORS[d] for d in ring_names], edgecolor="black", linewidth=1.5)
ax.axhline(y=RING_TARGET, color="red", linestyle="--", linewidth=2)
for bar, val in zip(ax.patches, ring_vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2, str(val),
            ha="center", fontsize=12, fontweight="bold")
ax.set_ylim(0, 165)
ax.set_title("8-cell sum of each ring -- all equal to 138 = (561-9)/4", fontsize=13, fontweight="bold")
ax.set_ylabel("Sum", fontsize=10)

ax = axes[1]
stack_names = [AXIS_LABELS[n] for n in AXES]
left_sums = []
right_sums = []
for name, axis in AXES.items():
    i = axis.index(CENTER)
    left_sums.append(sum(axis[:i]))
    right_sums.append(sum(axis[i + 1:]))
x = np.arange(len(AXES))
b1 = ax.bar(x, left_sums, 0.5, label="Ray A (69)", color="#4488CC", edgecolor="black")
b2 = ax.bar(x, [CENTER] * 4, 0.5, bottom=left_sums, label=f"Center ({CENTER})",
            color="#CC9944", edgecolor="black")
b3 = ax.bar(x, right_sums, 0.5,
            bottom=[l + CENTER for l in left_sums], label="Ray B (69)",
            color="#44AA44", edgecolor="black")
for bars in (b1, b2, b3):
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + h / 2, str(int(h)),
                ha="center", va="center", fontsize=11, fontweight="bold", color="white")
ax.axhline(y=AXIS_TARGET, color="red", linestyle="--", linewidth=2)
ax.set_xticks(x)
ax.set_xticklabels(stack_names, fontsize=9)
ax.set_ylim(0, 175)
ax.set_title("Axis decomposition: ray 69 + center 9 + ray 69 = 147", fontsize=13, fontweight="bold")
ax.legend(fontsize=11, loc="lower right")
ax.set_ylabel("Sum", fontsize=10)

plt.tight_layout()
save_fig("08_position_patterns.png")
plt.close()

# ============================================================
# 7. Summary
# ============================================================

print()
print("=" * 60)
print("Summary of verified key properties")
print("=" * 60)
print("  1. Value set: 1..33 each once, total sum 561")
print("  2. 4 axes each sum 147; 4x147 = 588 = 561 + 3x9 (center counted 4 times)")
print(f"  3. Graph: tree (nodes {G.number_of_nodes()}, edges {G.number_of_edges()}), "
      f"center degree 8, 8 leaves, diameter {nx.diameter(G)}")
print("  4. 8 rays each sum 69; axis = 69+9+69 = 147")
print("  5. 4 concentric rings each sum 138 = (561-9)/4; 147 with the center adjoined")
print(f"  6. Wuxing sums: Water {WUXING_SUMS['Water']}, Fire {WUXING_SUMS['Fire']}, "
      f"Wood {WUXING_SUMS['Wood']}, Metal {WUXING_SUMS['Metal']}, Earth {WUXING_SUMS['Earth']}")
print(f"  7. Edge relations: generation {wx_edge_counts.get('generation', 0)}, "
      f"overcoming {wx_edge_counts.get('overcoming', 0)}, "
      f"same-phase {wx_edge_counts.get('same_phase', 0)}, neutral {wx_edge_counts.get('neutral', 0)}")
print(f"  8. Spectrum: lambda_max ~= {lambda_max:.3f}, lambda_min ~= {lambda_min:.3f}")

print("\nGenerated files:")
for name in SAVED_FIGURES:
    print(f"  {name}")
print("=" * 60)
