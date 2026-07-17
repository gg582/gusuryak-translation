#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Beomsu-yongodo (範數用五圖) — Modern graph and combinatorial deep analysis

A reinterpretation of Beomsu-yongodo, one of the diagrams in the Gusuryak
(九數略) series, in modern mathematical language.

Analysis target: a cross structure arranging the numbers 1 through 9 on two
5-cell axes (one horizontal, one vertical) sharing the center cell 5
(make 9, use 10).
"""

import os
from collections import Counter
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch

# ============================================================
# 0. Font and output settings
# ============================================================

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

os.chdir(Path(__file__).parent)
OUTPUT_DIR = Path(".")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_fig(name):
    path = OUTPUT_DIR / name
    plt.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    print(f"[Saved] {path}")


# ============================================================
# 1. Source data structuring
# ============================================================

# Coordinates taken unchanged from visualize.py.
POSITIONS = {
    3: (-2, 0), 7: (-1, 0), 5: (0, 0), 4: (1, 0), 6: (2, 0),  # horizontal axis
    2: (0, 2), 8: (0, 1), 1: (0, -1), 9: (0, -2),             # vertical axis
}

AXES = {
    "horizontal": [3, 7, 5, 4, 6],  # left -> right
    "vertical": [2, 8, 5, 1, 9],    # top -> bottom
}
AXIS_SUM = 25
CENTER = 5

# Positional roles: center / inner ring (midpoints) / outer ring (endpoints).
# Rings are read clockwise starting at 12 o'clock.
INNER_RING = [8, 4, 1, 7]
OUTER_RING = [2, 6, 9, 3]
ARMS = {  # radial arm: the (outer, inner) pair in one direction
    "top": [2, 8],
    "right": [6, 4],
    "bottom": [9, 1],
    "left": [3, 7],
}
ANTIPODAL = {  # antipodal pairs (opposite positions on a ring)
    "outer_horizontal": (3, 6),
    "outer_vertical": (2, 9),
    "inner_horizontal": (7, 4),
    "inner_vertical": (8, 1),
}

RESIDUE_STYLE = {
    1: {"face": "#E5E5E5", "edge": "#444444", "name": "Water"},
    2: {"face": "#F6D0D0", "edge": "#B54141", "name": "Fire"},
    3: {"face": "#D5E3FA", "edge": "#3D6DB3", "name": "Wood"},
    4: {"face": "#D7D7D7", "edge": "#1F1F1F", "name": "Metal"},
    0: {"face": "#F7E3A0", "edge": "#B58A00", "name": "Earth"},
}

DISPLAY_LABELS = {
    "horizontal": "Horizontal axis",
    "vertical": "Vertical axis",
    "top": "Top",
    "bottom": "Bottom",
    "left": "Left",
    "right": "Right",
    "generation": "generation",
    "overcoming": "overcoming",
    "same_phase": "same-phase",
    "neutral": "neutral",
    "center": "center",
    "inner": "inner ring (midpoints)",
    "outer": "outer ring (endpoints)",
}

PHASE_COLOR = {
    "Water": "#4488CC",
    "Fire": "#CC4444",
    "Wood": "#44AA44",
    "Metal": "#888888",
    "Earth": "#CC9944",
}

AXIS_COLOR = {"horizontal": "#CC4444", "vertical": "#4488CC"}
ROLE_COLOR = {"center": "#F7E3A0", "inner": "#D5E3FA", "outer": "#F6D0D0"}


def phase_of(n: int) -> str:
    return RESIDUE_STYLE[n % 5]["name"]


def residue_1based(n: int) -> int:
    r = n % 5
    return 5 if r == 0 else r


def role_of(n: int) -> str:
    if n == CENTER:
        return "center"
    if n in INNER_RING:
        return "inner"
    return "outer"


# ============================================================
# 2. Graph construction
# ============================================================

# Connect cells that are adjacent on an axis (center 5 is shared by both axes).
EDGES: list[tuple[int, int]] = []
for line in AXES.values():
    for i in range(len(line) - 1):
        EDGES.append((line[i], line[i + 1]))


def axis_of_edge(u: int, v: int) -> str:
    """Axis an edge belongs to (classified by its non-center endpoint)."""
    if u in AXES["horizontal"] and v in AXES["horizontal"]:
        return "horizontal"
    return "vertical"


G = nx.Graph()
G.add_nodes_from(range(1, 10))
G.add_edges_from(EDGES)
for n in G.nodes():
    G.nodes[n]["phase"] = phase_of(n)
    G.nodes[n]["role"] = role_of(n)


# ============================================================
# 3. Combinatorial and graph-theoretic analysis
# ============================================================

def validate():
    """Verify the basic invariants of the source data; hard-fail on any mismatch."""
    all_values = list(POSITIONS.keys())
    if sorted(all_values) != list(range(1, 10)):
        raise ValueError("The value set must be exactly 1..9, each used once")
    total = sum(all_values)
    if total != 45:
        raise ValueError(f"Total sum must be 45 (got {total})")
    for name, line in AXES.items():
        s = sum(line)
        if s != AXIS_SUM:
            raise ValueError(f"{DISPLAY_LABELS[name]} sum must be {AXIS_SUM} (got {s})")
    overlap = set(AXES["horizontal"]) & set(AXES["vertical"])
    if overlap != {CENTER}:
        raise ValueError(f"The two axes must share only the center {CENTER} (got {overlap})")
    if 2 * AXIS_SUM != total + CENTER:
        raise ValueError("Duplication equation 2*S = T + D does not hold")

    print("Validation passed:")
    for name, line in AXES.items():
        eq = " + ".join(map(str, line))
        print(f"  {DISPLAY_LABELS[name]}: {eq} = {sum(line)}")
    print(f"  Duplication equation: 2 x {AXIS_SUM} = {2 * AXIS_SUM} = {total} + {CENTER}"
          f"  (make 9, use 10 — center {CENTER} used twice)")


print("=" * 60)
print("Beomsu-yongodo (範數用五圖) — modern graph and combinatorial analysis")
print("=" * 60)
validate()

print(f"\nNodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")
print(f"Connected components: {nx.number_connected_components(G)}")
print(f"Is a tree: {nx.is_tree(G)}")
print(f"Cycle basis: {nx.cycle_basis(G)}  (empty, since the graph is a tree)")
print(f"Diameter: {nx.diameter(G)}, radius: {nx.radius(G)},"
      f" graph center: {nx.center(G)}")

deg_seq = sorted([d for _, d in G.degree()], reverse=True)
deg_counter = Counter(d for _, d in G.degree())
print(f"Degree sequence: {deg_seq}")
print("Degree distribution: " + ", ".join(f"degree {d}: {c}" for d, c in sorted(deg_counter.items(), reverse=True)))
for role, members in [("center", [CENTER]), ("inner", INNER_RING), ("outer", OUTER_RING)]:
    degs = [G.degree(n) for n in members]
    print(f"  {DISPLAY_LABELS[role]} {members}: degrees {degs}")

betw = nx.betweenness_centrality(G)
print("\nBetweenness centrality (Top 10):")
for n, v in sorted(betw.items(), key=lambda x: -x[1])[:10]:
    print(f"  {n}({phase_of(n)}, {DISPLAY_LABELS[role_of(n)]}): {v:.3f}")

print("\nPhase sums:")
for r in [1, 2, 3, 4, 5]:
    nodes = [n for n in range(1, 10) if residue_1based(n) == r]
    wx = RESIDUE_STYLE[r % 5]["name"]
    print(f"  {wx}({r}): sum={sum(nodes)}, values={nodes}")

print("\nPhase distribution per axis:")
for name, line in AXES.items():
    counts = Counter(phase_of(v) for v in line)
    seq = "->".join(phase_of(v) for v in line)
    print(f"  {DISPLAY_LABELS[name]}: {dict(counts)}  (in layout order: {seq})")

# Wuxing edge classification: generation (Wood->Fire->Earth->Metal->Water->Wood)
# / overcoming (Wood->Earth->Water->Fire->Metal->Wood) / same-phase.
GENERATION_PAIRS = [(3, 2), (2, 0), (0, 4), (4, 1), (1, 3)]   # mod-5 residue pairs
OVERCOMING_PAIRS = [(3, 0), (0, 1), (1, 2), (2, 4), (4, 3)]


def classify_edge(u: int, v: int) -> str:
    ru, rv = u % 5, v % 5
    if ru == rv:
        return "same_phase"
    if (ru, rv) in GENERATION_PAIRS or (rv, ru) in GENERATION_PAIRS:
        return "generation"
    if (ru, rv) in OVERCOMING_PAIRS or (rv, ru) in OVERCOMING_PAIRS:
        return "overcoming"
    return "neutral"


wx_edge_counts: dict[str, int] = {}
print("\nWuxing relation per edge:")
for u, v in G.edges():
    key = classify_edge(u, v)
    wx_edge_counts[key] = wx_edge_counts.get(key, 0) + 1
    print(f"  ({u},{v}) [{phase_of(u)}-{phase_of(v)},"
          f" {DISPLAY_LABELS[axis_of_edge(u, v)]}]: {DISPLAY_LABELS[key]}")
total_edges = G.number_of_edges()
print("Wuxing edge distribution:")
for key in ["generation", "overcoming", "same_phase"]:
    cnt = wx_edge_counts.get(key, 0)
    print(f"  {DISPLAY_LABELS[key]}: {cnt} ({100 * cnt / total_edges:.1f}%)")

# Verify the generation chain on the horizontal axis: residues left->right
# must follow Wood->Fire->Earth->Metal->Water.
h_residues = [v % 5 for v in AXES["horizontal"]]
h_all_generation = all(
    (h_residues[i], h_residues[i + 1]) in GENERATION_PAIRS for i in range(4)
)
print(f"\nHorizontal-axis residues (left->right): {h_residues}"
      f"  -> every neighbor relation is generation: {h_all_generation}")

# ============================================================
# 4. Position-based analysis (center / rings / arms / antipodal pairs)
# ============================================================

inner_sum = sum(INNER_RING)
outer_sum = sum(OUTER_RING)
arm_sums = {name: sum(pair) for name, pair in ARMS.items()}
antipodal_sums = {name: a + b for name, (a, b) in ANTIPODAL.items()}
ring_formula = (45 - CENTER) // 2

print("\nPosition-based sums:")
print(f"  Center: {CENTER}")
print(f"  Inner ring (midpoints) {INNER_RING}: sum = {inner_sum}")
print(f"  Outer ring (endpoints) {OUTER_RING}: sum = {outer_sum}")
print(f"  Equal-ring formula R = (T - center)/2 = (45 - {CENTER})/2 = {ring_formula}")
print("  Arm sums: " + ", ".join(f"{DISPLAY_LABELS[k]} {ARMS[k]}={s}" for k, s in arm_sums.items()))
print("  Antipodal pair sums: " + ", ".join(f"{k}={s}" for k, s in antipodal_sums.items()))
print(f"  Two antipodal pairs per ring: 9 + 11 = {9 + 11} (= ring sum)")

# ============================================================
# 5. Generalization family (equal-axis / equal-ring stars)
# ============================================================

# Beomsu-yongodo's own values are verified directly in this script; the values
# of the other two diagrams are stated claims from their source annotations /
# spec, checked here only for consistency with the formulas.
FAMILY = [
    {"name": "Beomsu-yongodo", "hanja": "範數用五圖", "axes": 2, "cells": 5,
     "N": 9, "center": 5, "S": 25, "R": 20, "self": True},
    {"name": "Jangchaek-yongchildo", "hanja": "章策用七圖", "axes": 3, "cells": 7,
     "N": 19, "center": 7, "S": 68, "R": 61, "self": False},
    {"name": "Jungsang-yonggudo", "hanja": "象上用九圖", "axes": 4, "cells": 9,
     "N": 33, "center": 9, "S": 147, "R": 138, "self": False},
]

print("\nEqual-axis/equal-ring star family (N = a(L-1)+1, S = (T+(a-1)L)/a, R = (T-L)/a):")
for m in FAMILY:
    a, L = m["axes"], m["cells"]
    N_pred = a * (L - 1) + 1
    T = m["N"] * (m["N"] + 1) // 2
    S_pred = (T + (a - 1) * L) / a
    R_pred = (T - L) / a
    ok_N = N_pred == m["N"]
    ok_S = S_pred == m["S"]
    ok_R = R_pred == m["R"]
    tag = "this diagram (verified directly)" if m["self"] else "stated claims (formula consistency only)"
    print(f"  {m['name']} ({m['hanja']}): {a} axes x {L} cells, N={m['N']}, center={m['center']},"
          f" T={T}, S={m['S']}, R={m['R']}  "
          f"[N formula {'match' if ok_N else 'MISMATCH'}, S {'match' if ok_S else 'MISMATCH'},"
          f" R {'match' if ok_R else 'MISMATCH'} — {tag}]")

# ============================================================
# 6. Graph spectrum
# ============================================================

node_order = sorted(G.nodes(), key=lambda n: (residue_1based(n), n))
adj = nx.to_numpy_array(G, nodelist=node_order)
eigenvalues = np.linalg.eigvalsh(adj)
lam_max = float(max(eigenvalues))
lam_min = float(min(eigenvalues))
print("\nSpectrum:")
print(f"  Node order (by phase): {node_order}")
print(f"  Eigenvalues: {np.round(np.sort(eigenvalues)[::-1], 4)}")
print(f"  lambda_max = {lam_max:.4f} (sqrt(5) = {np.sqrt(5):.4f}), lambda_min = {lam_min:.4f}")

# ============================================================
# 7. Visualization
# ============================================================


def draw_axis_bands(ax):
    band_h = FancyBboxPatch(
        (-2.55, -0.52), 5.1, 1.04, boxstyle="round,pad=0.06",
        facecolor=AXIS_COLOR["horizontal"], alpha=0.10,
        edgecolor=AXIS_COLOR["horizontal"], linestyle=(0, (4, 4)), linewidth=1.5, zorder=0,
    )
    band_v = FancyBboxPatch(
        (-0.52, -2.55), 1.04, 5.1, boxstyle="round,pad=0.06",
        facecolor=AXIS_COLOR["vertical"], alpha=0.10,
        edgecolor=AXIS_COLOR["vertical"], linestyle=(0, (4, 4)), linewidth=1.5, zorder=0,
    )
    ax.add_patch(band_h)
    ax.add_patch(band_v)
    ax.text(2.85, 0, f"{DISPLAY_LABELS['horizontal']}\nSum=25", ha="left", va="center",
            fontsize=11, fontweight="bold", color=AXIS_COLOR["horizontal"])
    ax.text(0, 2.85, f"{DISPLAY_LABELS['vertical']} · Sum=25", ha="center", va="bottom",
            fontsize=11, fontweight="bold", color=AXIS_COLOR["vertical"])


def draw_edges(ax, gray=False, lw=3.2, zorder=1):
    for u, v in EDGES:
        x1, y1 = POSITIONS[u]
        x2, y2 = POSITIONS[v]
        if gray:
            ax.plot([x1, x2], [y1, y2], color="#DDDDDD", linewidth=1.2, zorder=0)
        else:
            ax.plot([x1, x2], [y1, y2], color=AXIS_COLOR[axis_of_edge(u, v)],
                    linewidth=lw, alpha=0.75, zorder=zorder)


def draw_nodes(ax, highlight_values=None, dim_values=None, role_colors=False,
               node_radius=0.30, fontsize=11):
    for value, (x, y) in POSITIONS.items():
        style = RESIDUE_STYLE[value % 5]
        face, edge, lw = style["face"], style["edge"], 2.2
        text_color = "black"
        if role_colors:
            face = ROLE_COLOR[role_of(value)]
            edge = "#333333"
        if dim_values is not None and value in dim_values:
            face, edge, lw = "#F2F2F2", "#CCCCCC", 1.0
            text_color = "#AAAAAA"
        if highlight_values and value in highlight_values:
            edge, lw = "red", 3.2
        ax.add_patch(plt.Circle((x, y), node_radius, facecolor=face, edgecolor=edge,
                                linewidth=lw, zorder=2))
        ax.text(x, y, str(value), ha="center", va="center", fontsize=fontsize,
                fontweight="bold", color=text_color, zorder=3)


def wuxing_legend(ax, loc="lower right"):
    legend_elements = [
        mpatches.Patch(facecolor=PHASE_COLOR[wx], edgecolor="black",
                       label=f"{wx}({wx[0]})")
        for wx in ["Water", "Fire", "Wood", "Metal", "Earth"]
    ]
    ax.legend(handles=legend_elements, loc=loc, fontsize=10, framealpha=0.9)


XLIM = (-3.1, 4.3)
YLIM = (-3.1, 3.5)

# --- 01: Original graph ---
fig, ax = plt.subplots(figsize=(10, 9))
draw_axis_bands(ax)
draw_edges(ax)
draw_nodes(ax)
ax.add_patch(plt.Circle((0, 0), 0.44, fill=False, edgecolor="#333333",
                        linewidth=1.5, linestyle=(0, (2, 2)), zorder=1))
ax.text(0.58, 0.55, "center 5\n(shared by both axes)", ha="left", va="bottom",
        fontsize=9, color="#333333")
ax.set_title("Beomsu-yongodo (範數用五圖) — original cross layout\n"
             "1..9 each once · each axis sums to 25 · total 45 · 2x25 = 45+5",
             fontsize=15, fontweight="bold")
ax.set_xlim(*XLIM)
ax.set_ylim(*YLIM)
ax.set_aspect("equal")
ax.axis("off")
wuxing_legend(ax)
save_fig("01_original_graph.png")
plt.close()

# --- 02: Wuxing decomposition ---
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()
ax = axes[0]
draw_axis_bands(ax)
draw_edges(ax)
draw_nodes(ax)
ax.set_title("Full graph", fontsize=13, fontweight="bold")
ax.set_xlim(*XLIM)
ax.set_ylim(*YLIM)
ax.set_aspect("equal")
ax.axis("off")

for idx, wx in enumerate(["Water", "Fire", "Wood", "Metal", "Earth"]):
    ax = axes[idx + 1]
    draw_axis_bands(ax)
    draw_edges(ax, gray=True)
    wx_nodes = [n for n in range(1, 10) if phase_of(n) == wx]
    draw_nodes(ax, dim_values=[n for n in range(1, 10) if n not in wx_nodes])
    for n in wx_nodes:
        x, y = POSITIONS[n]
        ax.add_patch(plt.Circle((x, y), 0.36, facecolor=PHASE_COLOR[wx],
                                edgecolor="black", linewidth=2.5, zorder=3))
        ax.text(x, y, str(n), ha="center", va="center", fontsize=12,
                fontweight="bold", color="white" if wx in ["Water", "Wood"] else "black",
                zorder=4)
    ax.set_title(f"{wx}({wx[0]}) · {len(wx_nodes)} cells · sum {sum(wx_nodes)}",
                 fontsize=13, fontweight="bold", color=PHASE_COLOR[wx])
    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.set_aspect("equal")
    ax.axis("off")

plt.suptitle("Wuxing (Five Phases) subgraph decomposition — each axis holds every phase exactly once",
             fontsize=16, fontweight="bold", y=1.0)
plt.tight_layout()
save_fig("02_wuxing_decomposition.png")
plt.close()

# --- 03: Adjacency matrix + spectrum ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
im = ax.imshow(adj, cmap="YlOrRd", interpolation="nearest")
ax.set_xticks(range(9))
ax.set_yticks(range(9))
ax.set_xticklabels(node_order, fontsize=9)
ax.set_yticklabels(node_order, fontsize=9)
wx_sorted = [phase_of(n) for n in node_order]
boundaries = [i - 0.5 for i in range(1, 9) if wx_sorted[i] != wx_sorted[i - 1]]
for b in boundaries:
    ax.axhline(y=b, color="blue", linewidth=1.5, alpha=0.7)
    ax.axvline(x=b, color="blue", linewidth=1.5, alpha=0.7)
plt.colorbar(im, ax=ax, shrink=0.8)
ax.set_title("Adjacency matrix (sorted by phase)", fontsize=13, fontweight="bold")

ax = axes[1]
sorted_ev = sorted(eigenvalues, reverse=True)
ax.bar(range(9), sorted_ev, color="#4488CC", edgecolor="black", alpha=0.85)
ax.axhline(y=0, color="red", linestyle="--", linewidth=1)
for i, v in enumerate(sorted_ev):
    ax.text(i, v + 0.08 if v >= 0 else v - 0.22, f"{v:.2f}", ha="center", fontsize=9)
ax.set_xlabel("Index", fontsize=11)
ax.set_ylabel("Eigenvalue", fontsize=11)
ax.set_title(f"Graph spectrum\nlambda_max = {lam_max:.4f} (= sqrt(5)), lambda_min = {lam_min:.4f}"
             " — symmetric about 0 (bipartite tree)",
             fontsize=13, fontweight="bold")
ax.grid(True, alpha=0.3)
plt.tight_layout()
save_fig("03_adjacency_spectrum.png")
plt.close()

# --- 04: Cycle analysis (tree: show ring/level structure instead) ---
fig, axes = plt.subplots(2, 2, figsize=(16, 14))

ax = axes[0, 0]
# Concentric distance rings (radii 1 and 2) as dashed circles
for radius, label in [(1, "inner ring (dist 1)"), (2, "outer ring (dist 2)")]:
    ax.add_patch(plt.Circle((0, 0), radius, fill=False, edgecolor="#999999",
                            linewidth=1.5, linestyle=(0, (5, 5)), zorder=0))
    ax.text(radius * np.cos(np.radians(135)), radius * np.sin(np.radians(135)) + 0.16,
            label, ha="center", fontsize=10, color="#555555")
draw_edges(ax)
draw_nodes(ax, role_colors=True)
ax.set_title("Concentric distance-ring structure (tree)", fontsize=13, fontweight="bold")
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect("equal")
ax.axis("off")
role_legend = [
    mpatches.Patch(facecolor=ROLE_COLOR[r], edgecolor="black", label=DISPLAY_LABELS[r])
    for r in ["center", "inner", "outer"]
]
ax.legend(handles=role_legend, loc="lower right", fontsize=10, framealpha=0.9)

ax = axes[0, 1]
# The tree redrawn by distance level from the center (layered layout)
level_pos = {CENTER: (0, 0)}
level1 = [8, 4, 1, 7]
child_of = {8: 2, 4: 6, 1: 9, 7: 3}
for i, n in enumerate(level1):
    level_pos[n] = (1, 1.5 - i)
    level_pos[child_of[n]] = (2, 1.5 - i)
for n in level1:
    ax.plot([0, 1], [0, level_pos[n][1]], color="#999999", linewidth=2, zorder=1)
    c = child_of[n]
    ax.plot([1, 2], [level_pos[n][1], level_pos[c][1]], color="#999999", linewidth=2, zorder=1)
for n, (x, y) in level_pos.items():
    face = ROLE_COLOR[role_of(n)]
    ax.add_patch(plt.Circle((x, y), 0.16, facecolor=face, edgecolor="#333333",
                            linewidth=2, zorder=2))
    ax.text(x, y, str(n), ha="center", va="center", fontsize=10, fontweight="bold", zorder=3)
for x, label in [(0, "distance 0\n(center)"), (1, "distance 1\n(inner)"), (2, "distance 2\n(outer)")]:
    ax.text(x, -2.2, label, ha="center", fontsize=11, fontweight="bold", color="#555555")
ax.set_title("Level (distance) structure from the center", fontsize=13, fontweight="bold")
ax.set_xlim(-0.6, 2.6)
ax.set_ylim(-2.7, 2.1)
ax.set_aspect("equal")
ax.axis("off")

ax = axes[1, 0]
ax.text(
    0.5, 0.5,
    "Tree structure\n\n"
    f"9 nodes · 8 edges (= nodes - 1)\n"
    f"connected · no cycles (cycle rank 0)\n"
    f"girth: undefined\n"
    f"diameter 4 (e.g. 3-7-5-4-6)\n"
    f"radius 2 · graph center = node 5",
    ha="center", va="center", fontsize=13, fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.6", facecolor="lightyellow", edgecolor="black"),
)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

ax = axes[1, 1]
arm_names = list(ARMS.keys())
arm_vals = [arm_sums[k] for k in arm_names]
bars = ax.bar([DISPLAY_LABELS[k] for k in arm_names], arm_vals,
              color=["#CC4444", "#4488CC", "#44AA44", "#CC9944"],
              edgecolor="black", linewidth=1.5)
ax.axhline(y=10, color="red", linestyle="--", linewidth=2)
for bar, val in zip(bars, arm_vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.15, str(val),
            ha="center", fontsize=13, fontweight="bold")
ax.set_ylim(0, 12.5)
ax.set_title("Arm (radial pair) sums — all 10 (= 2 x center 5)", fontsize=13, fontweight="bold")
ax.set_ylabel("Sum", fontsize=10)

plt.suptitle("Cycle analysis — the graph is a tree, so rings/levels are shown instead",
             fontsize=15, fontweight="bold")
plt.tight_layout(rect=[0, 0, 1, 0.97])
save_fig("04_cycle_analysis.png")
plt.close()

# --- 05: Centrality + sum invariants ---
fig, axes = plt.subplots(2, 2, figsize=(16, 13))

ax = axes[0, 0]
degrees = dict(G.degree())
nodes_sorted = sorted(G.nodes(), key=lambda n: (-degrees[n], n))
ax.bar(range(9), [degrees[n] for n in nodes_sorted],
       color=[PHASE_COLOR[phase_of(n)] for n in nodes_sorted], edgecolor="black")
ax.set_xticks(range(9))
ax.set_xticklabels([str(n) for n in nodes_sorted], fontsize=9)
ax.set_title("Degree (only center 5 has degree 4)", fontsize=12, fontweight="bold")
ax.set_ylabel("Degree", fontsize=10)

ax = axes[0, 1]
betw_sorted = sorted(G.nodes(), key=lambda n: (-betw[n], n))
ax.bar(range(9), [betw[n] for n in betw_sorted],
       color=[PHASE_COLOR[phase_of(n)] for n in betw_sorted], edgecolor="black")
ax.set_xticks(range(9))
ax.set_xticklabels([str(n) for n in betw_sorted], fontsize=9)
for i, n in enumerate(betw_sorted):
    ax.text(i, betw[n] + 0.015, f"{betw[n]:.3f}", ha="center", fontsize=8)
ax.set_title("Betweenness centrality (center 5 = 6/7 = 0.857)", fontsize=12, fontweight="bold")
ax.set_ylabel("Centrality", fontsize=10)

ax = axes[1, 0]
wx_names = ["Water", "Fire", "Wood", "Metal", "Earth"]
wx_vals = [sum(n for n in range(1, 10) if phase_of(n) == wx) for wx in wx_names]
bars = ax.bar(wx_names, wx_vals,
              color=[PHASE_COLOR[w] for w in wx_names], edgecolor="black", linewidth=1.5)
for bar, val in zip(bars, wx_vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2, str(val),
            ha="center", fontsize=12, fontweight="bold")
ax.plot(range(4), wx_vals[:4], "o--", color="black", alpha=0.5, linewidth=2)
ax.set_title("Phase sums — Water/Fire/Wood/Metal: 7, 9, 11, 13 (difference 2)",
             fontsize=12, fontweight="bold")
ax.set_ylabel("Sum", fontsize=10)

ax = axes[1, 1]
components = {
    "Horizontal": 25, "Vertical": 25, "Inner ring": inner_sum,
    "Outer ring": outer_sum, "Total": 45,
}
bars = ax.bar(list(components.keys()), list(components.values()),
              color=["#CC4444", "#4488CC", ROLE_COLOR["inner"], ROLE_COLOR["outer"], "#333333"],
              edgecolor="black", linewidth=1.5)
for bar, val in zip(bars, list(components.values())):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.7, str(val),
            ha="center", fontsize=12, fontweight="bold")
ax.set_title("Structural subset sums (axes 25 · rings 20 · total 45)", fontsize=12, fontweight="bold")
ax.set_ylabel("Sum", fontsize=10)
ax.set_ylim(0, 52)

plt.tight_layout()
save_fig("05_centrality_invariants.png")
plt.close()

# --- 06: Wuxing generation/overcoming ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
phase_graph = nx.DiGraph()
phase_relations = [
    ("Wood", "Fire", "generation"),
    ("Fire", "Earth", "generation"),
    ("Earth", "Metal", "generation"),
    ("Metal", "Water", "generation"),
    ("Water", "Wood", "generation"),
    ("Wood", "Earth", "overcoming"),
    ("Earth", "Water", "overcoming"),
    ("Water", "Fire", "overcoming"),
    ("Fire", "Metal", "overcoming"),
    ("Metal", "Wood", "overcoming"),
]
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
nx.draw_networkx_nodes(phase_graph, wx_pos,
                       node_color=[PHASE_COLOR[w] for w in phase_graph.nodes()],
                       node_size=3000, edgecolors="black", linewidths=2.5, ax=ax)
nx.draw_networkx_labels(phase_graph, wx_pos,
                        labels={n: n for n in phase_graph.nodes()},
                        font_size=14, ax=ax)
ax.legend(handles=[
    Line2D([0], [0], color="#44AA44", lw=3, label="generation"),
    Line2D([0], [0], color="#CC4444", lw=2, linestyle="--", label="overcoming"),
], loc="upper right", fontsize=11)
ax.set_title("Wuxing generation/overcoming pentagram", fontsize=13, fontweight="bold")
ax.set_xlim(-3, 3.5)
ax.set_ylim(-2.5, 3)
ax.axis("off")

ax = axes[1]
class_keys = ["generation", "overcoming", "same_phase"]
class_vals = [wx_edge_counts.get(k, 0) for k in class_keys]
bars = ax.bar([DISPLAY_LABELS[k] for k in class_keys], class_vals,
              color=["#44AA44", "#CC4444", "#CC9944"], edgecolor="black", linewidth=1.5)
for bar, val in zip(bars, class_vals):
    pct = 100 * val / total_edges
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
            f"{val} ({pct:.1f}%)", ha="center", fontsize=12, fontweight="bold")
ax.set_ylim(0, 7.5)
ax.set_title(f"Wuxing edge classification (N={total_edges})\n"
             "All 4 horizontal edges are generation; the 2 overcoming edges"
             " touch the center on the vertical axis",
             fontsize=13, fontweight="bold")
ax.set_ylabel("Edges", fontsize=10)

plt.tight_layout()
save_fig("06_wuxing_relations.png")
plt.close()

# --- 07: Extensions and generalization ---
fig, axes = plt.subplots(1, 2, figsize=(17, 7.5))

ax = axes[0]
x = np.arange(len(FAMILY))
width = 0.27
metric_vals = {"N (values)": [m["N"] for m in FAMILY],
               "S (axis sum)": [m["S"] for m in FAMILY],
               "R (ring sum)": [m["R"] for m in FAMILY]}
metric_colors = {"N (values)": "#888888", "S (axis sum)": "#CC4444", "R (ring sum)": "#4488CC"}
for i, (label, vals) in enumerate(metric_vals.items()):
    bars = ax.bar(x + (i - 1) * width, vals, width, label=label,
                  color=metric_colors[label], edgecolor="black")
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2, str(val),
                ha="center", fontsize=9, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels([f"{m['name']}\n{m['axes']} axes x {m['cells']} cells · center {m['center']}"
                    for m in FAMILY], fontsize=10)
ax.set_title("Equal-axis/equal-ring star family\nN = a(L-1)+1 · S = (T+(a-1)L)/a · R = (T-L)/a",
             fontsize=12, fontweight="bold")
ax.legend(fontsize=10)
ax.set_ylabel("Value", fontsize=10)

ax = axes[1]
schem_colors = ["#CC4444", "#44AA44", "#4488CC"]
for i, m in enumerate(FAMILY):
    cx = i * 3.2
    a = m["axes"]
    for k in range(a):
        theta = np.pi / 2 - k * np.pi / a
        dx, dy = np.cos(theta), np.sin(theta)
        ax.plot([cx - 1.15 * dx, cx + 1.15 * dx], [-1.15 * dy, 1.15 * dy],
                color=schem_colors[i], linewidth=2.2, alpha=0.8, zorder=1)
    ax.add_patch(plt.Circle((cx, 0), 0.20, facecolor="#F7E3A0", edgecolor="black",
                            linewidth=2, zorder=3))
    ax.text(cx, 0, str(m["center"]), ha="center", va="center", fontsize=9,
            fontweight="bold", zorder=4)
    ax.text(cx, -1.75, f"{m['name']}\n{a} axes x {m['cells']} cells · N={m['N']}\n"
                       f"S={m['S']} · R={m['R']}",
            ha="center", va="top", fontsize=10, fontweight="bold", color=schem_colors[i])
ax.set_xlim(-1.8, 8.2)
ax.set_ylim(-3.3, 1.8)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("Equal-axis star schematics — axis count a = 2, 3, 4", fontsize=12, fontweight="bold")

plt.tight_layout()
save_fig("07_local_extensions.png")
plt.close()

# --- 08: Position patterns (arms / rings / antipodal pairs) ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

ax = axes[0]
labels = [DISPLAY_LABELS[k] for k in ARMS] + ["Inner ring", "Outer ring"]
vals = [arm_sums[k] for k in ARMS] + [inner_sum, outer_sum]
colors = ["#4488CC"] * 4 + [ROLE_COLOR["inner"], ROLE_COLOR["outer"]]
bars = ax.bar(labels, vals, color=colors, edgecolor="black", linewidth=1.5)
ax.axhline(y=10, color="#4488CC", linestyle="--", linewidth=1.5, alpha=0.7)
ax.axhline(y=20, color="#CC4444", linestyle="--", linewidth=1.5, alpha=0.7)
for bar, val in zip(bars, vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(val),
            ha="center", fontsize=12, fontweight="bold")
ax.set_ylim(0, 24)
ax.set_title("Arm sums = 10 (x4); inner ring sum = outer ring sum = 20",
             fontsize=13, fontweight="bold")
ax.set_ylabel("Sum", fontsize=10)

ax = axes[1]
ap_labels = ["outer L-R\n(3,6)", "outer T-B\n(2,9)", "inner L-R\n(7,4)", "inner T-B\n(8,1)"]
ap_keys = ["outer_horizontal", "outer_vertical", "inner_horizontal", "inner_vertical"]
ap_vals = [antipodal_sums[k] for k in ap_keys]
bars = ax.bar(ap_labels, ap_vals,
              color=[ROLE_COLOR["outer"], ROLE_COLOR["outer"],
                     ROLE_COLOR["inner"], ROLE_COLOR["inner"]],
              edgecolor="black", linewidth=1.5)
for bar, val in zip(bars, ap_vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2, str(val),
            ha="center", fontsize=13, fontweight="bold")
ax.axhline(y=10, color="#999999", linestyle="--", linewidth=1.2)
ax.set_ylim(0, 14)
ax.set_title("Alternating antipodal pair sums: outer 9/11, inner 11/9\n"
             "9 + 11 = 20 = each ring's sum",
             fontsize=13, fontweight="bold")
ax.set_ylabel("Sum", fontsize=10)

plt.tight_layout()
save_fig("08_position_patterns.png")
plt.close()

# ============================================================
# 8. Summary
# ============================================================

print("\n" + "=" * 60)
print("Summary of verified properties")
print("=" * 60)
print("✓ Value set: 1..9 each once, total T = 45")
print("✓ Both axes sum to S = 25; duplication equation 2*25 = 45 + 5 (make 9, use 10)")
print("✓ Graph: 9-node 8-edge tree (center degree 4, midpoints 2, endpoints 1)")
print("✓ Betweenness: center 5 = 0.857, midpoints = 0.250, endpoints = 0.000")
print("✓ Each axis contains every one of the five phases exactly once")
print(f"✓ Horizontal-axis residues {h_residues} = the generation cycle"
      f" (all neighbors generation: {h_all_generation})")
print(f"✓ Wuxing edges: generation {wx_edge_counts.get('generation', 0)} (75.0%),"
      f" overcoming {wx_edge_counts.get('overcoming', 0)} (25.0%), same-phase 0")
print(f"✓ All four arm sums equal 10: {arm_vals}")
print(f"✓ Inner ring sum = outer ring sum = 20 = (45 - 5)/2")
print(f"✓ Alternating antipodal pair sums: {ap_vals} (9 + 11 = 20)")
print(f"✓ Spectrum: lambda_max = {lam_max:.4f} = sqrt(5), lambda_min = {lam_min:.4f}"
      " (symmetric about 0)")

print("\nGenerated files:")
for f in ["01_original_graph.png", "02_wuxing_decomposition.png",
          "03_adjacency_spectrum.png", "04_cycle_analysis.png",
          "05_centrality_invariants.png", "06_wuxing_relations.png",
          "07_local_extensions.png", "08_position_patterns.png"]:
    print(f"  {f}")
print("All figures generated!")
