#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jungui-yongyukdo (重儀用六圖) — Modern graph and combinatorial deep analysis

A reinterpretation of Jungui-yongyukdo, one of the diagrams in the
Gusuryak (九數略) series, in modern mathematical language.

Analysis target: the numbers 1 through 16 arranged into 4 overlapping
6-number groups (top, left, bottom, right). Each group sums to 51, and
adjacent groups share exactly 2 values.

Two graph views are used:
  (a) T-forest: the four T-shaped arrows drawn in the source diagram
      (12 edges, a forest)
  (b) co-membership graph: connect every pair of values belonging to the
      same group (each group = a K6 clique)
"""

import itertools
import os
from collections import Counter
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.lines import Line2D

# ============================================================
# 0. Output settings
# ============================================================

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

os.chdir(Path(__file__).parent)
OUTPUT_DIR = Path(".")


def save_fig(name: str) -> None:
    path = OUTPUT_DIR / name
    plt.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    print(f"[Saved] {path}")


# ============================================================
# 1. Source data structuring (coordinates/edges from visualize.py)
# ============================================================

# 2-D coordinates of the 16 nodes
POSITIONS = {
    7: (-2.5, 3), 16: (-1, 3.2), 1: (1, 3.2), 6: (2.5, 3),
    13: (-3, 1.5), 11: (-1, 1), 10: (1, 1), 4: (3, 1.5),
    3: (-3, -1.5), 9: (-1, -1), 12: (1, -1), 14: (3, -1.5),
    8: (-2.5, -3), 2: (-1, -3.2), 15: (1, -3.2), 5: (2.5, -3),
}

# The four T-shaped arrow edges (each T center has degree 3)
T_EDGES = [
    # Upper-left T (center 7 -> 16, 13, 11)
    (7, 16), (7, 13), (7, 11),
    # Upper-right T (center 6 -> 1, 10, 4)
    (6, 1), (6, 10), (6, 4),
    # Lower-left T (center 8 -> 3, 9, 2)
    (8, 3), (8, 9), (8, 2),
    # Lower-right T (center 5 -> 12, 14, 15)
    (5, 12), (5, 14), (5, 15),
]

# The four 6-number groups, each summing to 51
GROUPS = {
    "Top": [7, 16, 1, 6, 11, 10],
    "Left": [7, 13, 11, 3, 9, 8],
    "Bottom": [8, 2, 9, 12, 15, 5],
    "Right": [6, 10, 4, 12, 14, 5],
}

# Same group region ellipses as in visualize.py
GROUP_REGIONS = {
    "Top": ((0, 2.5), 6.8, 3.0, "#FFD700"),
    "Left": ((-2.0, 0), 3.5, 6.8, "#87CEEB"),
    "Bottom": ((0, -2.5), 6.8, 3.0, "#3CB371"),
    "Right": ((2.0, 0), 3.5, 6.8, "#F08080"),
}

RELATION_LABELS = {
    "generation": "Generation",
    "overcoming": "Overcoming",
    "same_phase": "Same phase",
    "neutral": "Neutral",
}

TARGET_SUM = 51
TOTAL_SUM = 136

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
    return RESIDUE_STYLE[n % 5]["name"]


def residue_1based(n: int) -> int:
    r = n % 5
    return 5 if r == 0 else r


# ============================================================
# 2. Graph construction
# ============================================================

# (a) T-forest: the four T-shaped arrows of the source diagram
G_T = nx.Graph()
G_T.add_nodes_from(range(1, 17))
G_T.add_edges_from(tuple(sorted(e)) for e in T_EDGES)

# (b) Co-membership graph: connect every pair of values in the same group
G_co = nx.Graph()
G_co.add_nodes_from(range(1, 17))
for members in GROUPS.values():
    for u, v in itertools.combinations(sorted(members), 2):
        G_co.add_edge(u, v)

T_CENTERS = sorted(n for n, d in G_T.degree() if d == 3)
T_SPOKES = sorted(n for n, d in G_T.degree() if d == 1)

# Shared values: the 8 values belonging to two groups
membership_count = Counter(v for members in GROUPS.values() for v in members)
SHARED_VALUES = sorted(v for v, c in membership_count.items() if c == 2)
UNSHARED_VALUES = sorted(v for v, c in membership_count.items() if c == 1)

# Positional structure: perimeter 12-cycle (clockwise from top-left 7)
# and the inner 4-cycle
PERIMETER = [7, 16, 1, 6, 4, 14, 5, 15, 2, 8, 3, 13]
INNER = [11, 10, 12, 9]


# ============================================================
# 3. Validation
# ============================================================

def validate() -> None:
    all_values = [v for members in GROUPS.values() for v in members]
    distinct = sorted(set(all_values))
    if distinct != list(range(1, 17)):
        raise ValueError(f"value set is not 1..16: {distinct}")
    if len(all_values) != 24:
        raise ValueError(f"group membership count is not 24: {len(all_values)}")
    if sum(distinct) != TOTAL_SUM:
        raise ValueError(f"total sum is not {TOTAL_SUM}: {sum(distinct)}")
    for key, members in GROUPS.items():
        if len(members) != 6:
            raise ValueError(f"{key} group is not 6 numbers: {members}")
        if sum(members) != TARGET_SUM:
            raise ValueError(f"{key} group sum is not {TARGET_SUM}: {sum(members)}")

    # Verify the shared pairs of adjacent groups
    expected_overlaps = {
        ("Top", "Left"): {7, 11},
        ("Top", "Right"): {6, 10},
        ("Left", "Bottom"): {8, 9},
        ("Right", "Bottom"): {5, 12},
    }
    for (a, b), expected in expected_overlaps.items():
        actual = set(GROUPS[a]) & set(GROUPS[b])
        if actual != expected:
            raise ValueError(f"{a}∩{b} shared pair mismatch: {actual} != {expected}")
    for a, b in itertools.combinations(GROUPS, 2):
        if (a, b) in expected_overlaps or (b, a) in expected_overlaps:
            continue
        if set(GROUPS[a]) & set(GROUPS[b]):
            raise ValueError(f"diagonal groups {a}∩{b} must be disjoint")

    duplication = sum(SHARED_VALUES)
    if len(SHARED_VALUES) != 8:
        raise ValueError(f"shared values are not 8: {SHARED_VALUES}")
    if 4 * TARGET_SUM != TOTAL_SUM + duplication:
        raise ValueError("duplication checksum k*S = T + D fails")

    print("[Check] values: 1..16 each once (make 16, use 24) ✓")
    print("[Check] total sum: 1+2+...+16 = 136 ✓")
    for key, members in GROUPS.items():
        eq = "+".join(map(str, members))
        print(f"[Check] {key} group: {eq} = {sum(members)} ✓")
    for (a, b), expected in expected_overlaps.items():
        print(f"[Check] {a} ∩ {b} = {sorted(expected)} ✓")
    print(f"[Check] shared 8 values {SHARED_VALUES} sum D = {duplication} ✓")
    print(f"[Check] 4 × 51 = {4 * TARGET_SUM} = 136 + {duplication} (k·S = T + D) ✓")


validate()

# ============================================================
# 4. Combinatorial and graph-theoretic analysis
# ============================================================

print("\n" + "=" * 60)
print("Jungui-yongyukdo — Modern graph and combinatorial analysis")
print("=" * 60)

print("\n--- Graph summary ---")
print(f"T-forest: nodes {G_T.number_of_nodes()}, edges {G_T.number_of_edges()}, "
      f"components {nx.number_connected_components(G_T)}")
print(f"Co-membership graph: nodes {G_co.number_of_nodes()}, edges {G_co.number_of_edges()}, "
      f"components {nx.number_connected_components(G_co)}")

deg_T = Counter(d for _, d in G_T.degree())
deg_co = Counter(d for _, d in G_co.degree())
print(f"Degree distribution (T-forest): {dict(sorted(deg_T.items()))}")
print(f"  T centers (degree 3): {T_CENTERS} (sum {sum(T_CENTERS)})")
print(f"  T spokes (degree 1): {T_SPOKES} (sum {sum(T_SPOKES)})")
print(f"Degree distribution (co-membership): {dict(sorted(deg_co.items()))}")


def girth(G: nx.Graph) -> int | None:
    """Minimum cycle length, by removing each edge and re-measuring the distance."""
    best = None
    for u, v in G.edges():
        H = G.copy()
        H.remove_edge(u, v)
        try:
            d = nx.shortest_path_length(H, u, v)
        except nx.NetworkXNoPath:
            continue
        if best is None or d + 1 < best:
            best = d + 1
    return best


girth_T = girth(G_T)
girth_co = girth(G_co)
cycle_rank_co = G_co.number_of_edges() - G_co.number_of_nodes() + nx.number_connected_components(G_co)
print(f"\nGirth (T-forest): {girth_T} (no cycles, it is a forest)")
print(f"Girth (co-membership): {girth_co}, cycle rank: {cycle_rank_co}")

betw_co = nx.betweenness_centrality(G_co)
betw_T = nx.betweenness_centrality(G_T)
print("\nBetweenness centrality Top 10 (co-membership graph):")
for n, v in sorted(betw_co.items(), key=lambda x: (-x[1], x[0]))[:10]:
    shared = "shared" if n in SHARED_VALUES else "unshared"
    print(f"  {n}({phase_of(n)}, {shared}): {v:.4f}")
print("Betweenness centrality (T-forest, nonzero nodes):")
for n, v in sorted(betw_T.items(), key=lambda x: (-x[1], x[0])):
    if v > 0:
        print(f"  {n}({phase_of(n)}, T center): {v:.4f}")


# --- Complementary-pair (sum 17 = N+1) perfect matching check ---
def perfect_matchings(values: tuple[int, ...]):
    if not values:
        yield []
        return
    first = values[0]
    for i in range(1, len(values)):
        second = values[i]
        rest = values[1:i] + values[i + 1:]
        for matching in perfect_matchings(rest):
            yield [(first, second)] + matching


def complement_matching(values: list[int], target: int):
    for matching in perfect_matchings(tuple(sorted(values))):
        if all(a + b == target for a, b in matching):
            return matching
    return None


print("\n--- Complementary-pair (sum 17) perfect matching per group ---")
COMPLEMENT_MATCHINGS = {}
for key, members in GROUPS.items():
    matching = complement_matching(members, 17)
    COMPLEMENT_MATCHINGS[key] = matching
    if matching:
        pairs = ", ".join(f"({a},{b})" for a, b in matching)
        print(f"  {key} group: {pairs} — all 3 pairs sum to 17")
    else:
        print(f"  {key} group: no sum-17 perfect matching (all 15 matchings checked)")

print("\n--- Shared-pair sums ---")
SHARED_PAIR_SUMS = {}
for (a, b), pair in {
    ("Top", "Left"): (7, 11),
    ("Top", "Right"): (6, 10),
    ("Left", "Bottom"): (8, 9),
    ("Right", "Bottom"): (5, 12),
}.items():
    SHARED_PAIR_SUMS[pair] = pair[0] + pair[1]
    print(f"  {a} ∩ {b} = {pair}: sum {pair[0] + pair[1]}")

print("\n--- Positional subset sums ---")
print(f"  Perimeter 12-cycle {PERIMETER}: sum {sum(PERIMETER)}")
print(f"  Inner 4-cycle (rectangle) {INNER}: sum {sum(INNER)}")
print(f"  T centers {T_CENTERS}: sum {sum(T_CENTERS)} (4 consecutive integers)")
print(f"  T spokes (12 values): sum {sum(T_SPOKES)}")
print(f"  Shared 8 values: sum {sum(SHARED_VALUES)}, unshared 8 values {UNSHARED_VALUES}: sum {sum(UNSHARED_VALUES)}")

# Row sums by y coordinate (top to bottom)
rows: dict[float, list[int]] = {}
for value, (x, y) in POSITIONS.items():
    rows.setdefault(y, []).append(value)
ROW_SUMS = []
print("\n--- Row sums by y coordinate (top to bottom) ---")
for y in sorted(rows, reverse=True):
    vals = sorted(rows[y])
    ROW_SUMS.append(sum(vals))
    print(f"  y={y:+.1f}: {vals} sum {sum(vals)}")
print(f"  Row-sum sequence: {ROW_SUMS} — palindrome: {ROW_SUMS == ROW_SUMS[::-1]}")

# Left-right mirror pairs (x -> -x)
pos_to_value = {pos: value for value, pos in POSITIONS.items()}
print("\n--- Left-right mirror pairs (x <-> -x) ---")
MIRROR_PAIR_SUMS = []
seen = set()
for value, (x, y) in POSITIONS.items():
    if value in seen:
        continue
    mirror = pos_to_value[(-x, y)]
    seen.add(value)
    seen.add(mirror)
    MIRROR_PAIR_SUMS.append(value + mirror)
    print(f"  ({value},{mirror}): sum {value + mirror}")
print(f"  Mirror-pair sum distribution: {Counter(MIRROR_PAIR_SUMS)}")

# ============================================================
# 5. Wuxing (five phases) mod 5 analysis
# ============================================================

print("\n--- Wuxing classes and sums ---")
WX_SUMS = {}
for r in [1, 2, 3, 4, 5]:
    nodes = [n for n in range(1, 17) if residue_1based(n) == r]
    wx = RESIDUE_STYLE[r % 5]["name"]
    WX_SUMS[wx] = sum(nodes)
    print(f"  {wx} (mod5={r}): {nodes} sum {sum(nodes)}")

print("\n--- Wuxing distribution per group ---")
GROUP_WX_DIST = {}
for key, members in GROUPS.items():
    counts = Counter(phase_of(v) for v in members)
    GROUP_WX_DIST[key] = counts
    print(f"  {key} group: {dict(sorted(counts.items()))}")

GENERATION = [
    ("Wood", "Fire"), ("Fire", "Earth"), ("Earth", "Metal"),
    ("Metal", "Water"), ("Water", "Wood"),
]
OVERCOMING = [
    ("Wood", "Earth"), ("Earth", "Water"), ("Water", "Fire"),
    ("Fire", "Metal"), ("Metal", "Wood"),
]


def classify_edge(u: int, v: int) -> str:
    wu, wv = phase_of(u), phase_of(v)
    if wu == wv:
        return "same_phase"
    pair = (wu, wv)
    if pair in GENERATION or (wv, wu) in GENERATION:
        return "generation"
    if pair in OVERCOMING or (wv, wu) in OVERCOMING:
        return "overcoming"
    return "neutral"


def classify_graph_edges(G: nx.Graph) -> Counter:
    counts: Counter = Counter()
    for u, v in G.edges():
        counts[classify_edge(u, v)] += 1
    return counts


wx_edges_T = classify_graph_edges(G_T)
wx_edges_co = classify_graph_edges(G_co)
print("\n--- Wuxing edge-relation classification ---")
for label, G, counts in [("T-forest", G_T, wx_edges_T), ("Co-membership", G_co, wx_edges_co)]:
    total = G.number_of_edges()
    print(f"  [{label}, {total} edges]")
    for key in ["generation", "overcoming", "same_phase", "neutral"]:
        cnt = counts.get(key, 0)
        if cnt or key != "neutral":
            print(f"    {RELATION_LABELS[key]}: {cnt} ({100 * cnt / total:.1f}%)")

# ============================================================
# 6. Spectral analysis
# ============================================================

A_co = nx.to_numpy_array(G_co, nodelist=list(range(1, 17)))
A_T = nx.to_numpy_array(G_T, nodelist=list(range(1, 17)))
eig_co = np.linalg.eigvalsh(A_co)
eig_T = np.linalg.eigvalsh(A_T)
print("\n--- Graph spectra ---")
print(f"  Co-membership graph: lambda_max = {eig_co[-1]:.4f}, lambda_min = {eig_co[0]:.4f}")
print(f"  T-forest: lambda_max = {eig_T[-1]:.4f} (= sqrt(3), multiplicity 4), "
      f"lambda_min = {eig_T[0]:.4f} (= -sqrt(3), multiplicity 4)")

# ============================================================
# 7. Visualization
# ============================================================


def draw_group_regions(ax, with_sum_labels: bool = True) -> None:
    for key, (center, w, h, color) in GROUP_REGIONS.items():
        ax.add_patch(
            mpatches.Ellipse(
                center, w, h,
                facecolor=color, alpha=0.15, edgecolor=color, linewidth=1.2, zorder=0,
            )
        )
    if with_sum_labels:
        label_font = {"weight": "bold", "color": "#333333"}
        ax.text(0, 4.35, "Sum = 51", ha="center", fontdict=label_font, fontsize=12)
        ax.text(-4.35, 0, "Sum = 51", va="center", rotation=90, fontdict=label_font, fontsize=12)
        ax.text(0, -4.35, "Sum = 51", ha="center", fontdict=label_font, fontsize=12)
        ax.text(4.35, 0, "Sum = 51", va="center", rotation=-90, fontdict=label_font, fontsize=12)


def draw_t_edges(ax, color="#333333", lw=2.2, alpha=0.85, zorder=1, per_center=False) -> None:
    center_colors = {7: "#CC4444", 6: "#4488CC", 8: "#44AA44", 5: "#CC9944"}
    for u, v in T_EDGES:
        x1, y1 = POSITIONS[u]
        x2, y2 = POSITIONS[v]
        c = center_colors.get(u if u in T_CENTERS else v, color) if per_center else color
        ax.plot([x1, x2], [y1, y2], color=c, linewidth=lw, alpha=alpha, zorder=zorder)


def draw_nodes(ax, values=None, radius=0.34, fontsize=11, dim_values=None,
               highlight=None, zorder=2) -> None:
    values = values if values is not None else list(POSITIONS)
    for value in values:
        x, y = POSITIONS[value]
        style = RESIDUE_STYLE[value % 5]
        face, edge, lw = style["face"], style["edge"], 2.0
        if dim_values is not None and value in dim_values:
            face, edge, lw = "#F5F5F5", "#CCCCCC", 1.0
        if highlight and value in highlight:
            edge, lw = "red", 3.5
        ax.add_patch(
            plt.Circle((x, y), radius, facecolor=face, edgecolor=edge,
                       linewidth=lw, zorder=zorder)
        )
        text_color = "#AAAAAA" if (dim_values is not None and value in dim_values) else "black"
        ax.text(x, y, str(value), ha="center", va="center", fontsize=fontsize,
                fontweight="bold", color=text_color, zorder=zorder + 1)


def phase_legend(ax, loc="lower right") -> None:
    handles = [
        mpatches.Patch(facecolor=PHASE_COLOR[w], edgecolor="black", label=w)
        for w in ["Water", "Fire", "Wood", "Metal", "Earth"]
    ]
    ax.legend(handles=handles, loc=loc, fontsize=10, framealpha=0.9)


def setup_geo_ax(ax, title: str) -> None:
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlim(-5.0, 5.0)
    ax.set_ylim(-5.2, 5.2)
    ax.set_aspect("equal")
    ax.axis("off")


# --- 01: Source graph ---
fig, ax = plt.subplots(figsize=(10, 10))
draw_group_regions(ax)
draw_t_edges(ax)
draw_nodes(ax)
setup_geo_ax(
    ax,
    "Jungui-yongyukdo — Source structure\n"
    "4 groups × 6 numbers · each group sum 51 · total sum 136 (1–16, each once)",
)
phase_legend(ax)
save_fig("01_original_graph.png")
plt.close()

# --- 02: Wuxing subgraph decomposition ---
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()
ax = axes[0]
draw_group_regions(ax, with_sum_labels=False)
draw_t_edges(ax, color="#CCCCCC", lw=1.5, alpha=0.7)
draw_nodes(ax)
setup_geo_ax(ax, "Full graph")

for idx, wx in enumerate(["Water", "Fire", "Wood", "Metal", "Earth"]):
    ax = axes[idx + 1]
    draw_group_regions(ax, with_sum_labels=False)
    draw_t_edges(ax, color="#EEEEEE", lw=1.2, alpha=0.6, zorder=0)
    wx_nodes = [n for n in range(1, 17) if phase_of(n) == wx]
    others = [n for n in range(1, 17) if n not in wx_nodes]
    draw_nodes(ax, values=others, radius=0.26, fontsize=8, dim_values=set(others), zorder=1)
    for n in wx_nodes:
        x, y = POSITIONS[n]
        ax.add_patch(
            plt.Circle((x, y), 0.36, facecolor=PHASE_COLOR[wx], edgecolor="black",
                       linewidth=2.5, zorder=2)
        )
        ax.text(x, y, str(n), ha="center", va="center", fontsize=11,
                fontweight="bold",
                color="white" if wx in ["Water", "Wood"] else "black", zorder=3)
    setup_geo_ax(ax, f"{wx} · {len(wx_nodes)} values · sum {WX_SUMS[wx]}")
    ax.title.set_color(PHASE_COLOR[wx])

plt.suptitle("Wuxing (five phases) subgraph decomposition", fontsize=16, fontweight="bold", y=1.02)
plt.tight_layout()
save_fig("02_wuxing_decomposition.png")
plt.close()

# --- 03: Adjacency matrix + spectrum ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
im = ax.imshow(A_co, cmap="YlOrRd", interpolation="nearest")
ax.set_xticks(range(16))
ax.set_yticks(range(16))
ax.set_xticklabels(range(1, 17), fontsize=8)
ax.set_yticklabels(range(1, 17), fontsize=8)
plt.colorbar(im, ax=ax, shrink=0.8)
ax.set_title("Adjacency matrix (co-membership graph)", fontsize=13, fontweight="bold")

ax = axes[1]
x = np.arange(16)
ax.bar(x - 0.2, sorted(eig_co, reverse=True), width=0.4, color="#4488CC",
       edgecolor="black", alpha=0.85, label="Co-membership graph")
ax.bar(x + 0.2, sorted(eig_T, reverse=True), width=0.4, color="#CC4444",
       edgecolor="black", alpha=0.85, label="T-forest (4 × K(1,3))")
ax.axhline(y=0, color="black", linestyle="--", linewidth=1)
ax.set_xlabel("Index", fontsize=11)
ax.set_ylabel("Eigenvalue", fontsize=11)
ax.set_title(
    f"Graph spectra\nco-membership λ_max={eig_co[-1]:.2f}, λ_min={eig_co[0]:.2f} · "
    f"T-forest λ=±√3≈±1.73",
    fontsize=13,
    fontweight="bold",
)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
plt.tight_layout()
save_fig("03_adjacency_spectrum.png")
plt.close()

# --- 04: Cycle analysis (the T-forest is a forest, so show structure/ring levels) ---
fig, axes = plt.subplots(2, 2, figsize=(17, 15))

ax = axes[0, 0]
draw_group_regions(ax, with_sum_labels=False)
draw_t_edges(ax, per_center=True, lw=3.0, alpha=0.9)
draw_nodes(ax, highlight=set(T_CENTERS))
setup_geo_ax(ax, "T-forest: four T-stars K(1,3)\nno cycles (forest) · centers 7·6·8·5 (degree 3)")

ax = axes[0, 1]
draw_group_regions(ax, with_sum_labels=False)
for u, v in G_co.edges():
    x1, y1 = POSITIONS[u]
    x2, y2 = POSITIONS[v]
    ax.plot([x1, x2], [y1, y2], color="#BBBBBB", linewidth=0.8, alpha=0.5, zorder=0)
triangle = [7, 16, 11]
for i in range(3):
    u, v = triangle[i], triangle[(i + 1) % 3]
    x1, y1 = POSITIONS[u]
    x2, y2 = POSITIONS[v]
    ax.plot([x1, x2], [y1, y2], color="red", linewidth=3.5, alpha=0.9, zorder=1)
draw_nodes(ax, highlight=set(triangle))
setup_geo_ax(ax, f"Co-membership graph: girth {girth_co}\nminimum cycle example: 7-16-11-7 (Top group K6 clique)")

ax = axes[1, 0]
per_x = [POSITIONS[v][0] for v in PERIMETER] + [POSITIONS[PERIMETER[0]][0]]
per_y = [POSITIONS[v][1] for v in PERIMETER] + [POSITIONS[PERIMETER[0]][1]]
ax.plot(per_x, per_y, color="#4488CC", linewidth=2, linestyle="--", alpha=0.8, zorder=1)
inn_x = [POSITIONS[v][0] for v in INNER] + [POSITIONS[INNER[0]][0]]
inn_y = [POSITIONS[v][1] for v in INNER] + [POSITIONS[INNER[0]][1]]
ax.plot(inn_x, inn_y, color="#CC4444", linewidth=2, linestyle="--", alpha=0.8, zorder=1)
draw_nodes(ax, values=PERIMETER, zorder=2)
draw_nodes(ax, values=INNER, zorder=2, highlight=set(INNER))
setup_geo_ax(ax, f"Ring levels: perimeter 12-cycle Σ={sum(PERIMETER)} · inner 4-cycle Σ={sum(INNER)}")
ring_handles = [
    Line2D([0], [0], color="#4488CC", lw=2, linestyle="--", label=f"Perimeter 12-cycle (Σ={sum(PERIMETER)})"),
    Line2D([0], [0], color="#CC4444", lw=2, linestyle="--", label=f"Inner 4-cycle (Σ={sum(INNER)})"),
]
ax.legend(handles=ring_handles, loc="lower right", fontsize=10)

ax = axes[1, 1]
cycle_text = (
    "Cycle structure summary\n\n"
    "T-forest (edges drawn in the diagram)\n"
    "· 4 connected components (T-stars K(1,3) × 4)\n"
    "· no cycles — a forest\n\n"
    "Co-membership graph (group = K6 clique)\n"
    f"· 56 edges = 4 × C(6,2) - 4 (shared-pair edges duplicated)\n"
    f"· cycle rank {cycle_rank_co}\n"
    f"· girth {girth_co} (triangle, e.g. 7-16-11)"
)
ax.text(0.5, 0.5, cycle_text, ha="center", va="center", fontsize=13,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.6", facecolor="lightyellow", edgecolor="black"))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

plt.tight_layout()
save_fig("04_cycle_analysis.png")
plt.close()

# --- 05: Centrality + sum invariants ---
fig, axes = plt.subplots(2, 2, figsize=(16, 13))

ax = axes[0, 0]
degrees = dict(G_co.degree())
nodes_sorted = sorted(G_co.nodes(), key=lambda n: (-degrees[n], n))
ax.bar(range(16), [degrees[n] for n in nodes_sorted],
       color=[PHASE_COLOR[phase_of(n)] for n in nodes_sorted], edgecolor="black")
ax.set_xticks(range(16))
ax.set_xticklabels([str(n) for n in nodes_sorted], fontsize=8)
ax.set_title("Degree (co-membership graph): shared 8 values have 9, unshared have 5",
             fontsize=12, fontweight="bold")
ax.set_ylabel("Degree", fontsize=10)

ax = axes[0, 1]
betw_sorted = sorted(G_co.nodes(), key=lambda n: (-betw_co[n], n))
ax.bar(range(16), [betw_co[n] for n in betw_sorted],
       color=[PHASE_COLOR[phase_of(n)] for n in betw_sorted], edgecolor="black")
ax.set_xticks(range(16))
ax.set_xticklabels([str(n) for n in betw_sorted], fontsize=8)
ax.set_title("Betweenness centrality (co-membership graph)", fontsize=12, fontweight="bold")
ax.set_ylabel("Centrality", fontsize=10)

ax = axes[1, 0]
wx_names = ["Water", "Fire", "Wood", "Metal", "Earth"]
wx_vals = [WX_SUMS[w] for w in wx_names]
ax.bar(wx_names, wx_vals,
       color=[PHASE_COLOR[w] for w in wx_names], edgecolor="black", linewidth=1.5)
ax.set_title("Wuxing class sums", fontsize=12, fontweight="bold")
for bar, val in zip(ax.patches, wx_vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, str(val),
            ha="center", fontsize=12, fontweight="bold")

ax = axes[1, 1]
group_keys = list(GROUPS.keys())
group_sums = [sum(GROUPS[k]) for k in group_keys]
group_colors = [GROUP_REGIONS[k][3] for k in group_keys]
ax.bar(group_keys, group_sums,
       color=group_colors, edgecolor="black", linewidth=1.5)
ax.axhline(y=TARGET_SUM, color="red", linestyle="--", linewidth=2)
ax.set_ylim(0, 60)
ax.set_title("Six-number sum of each group (all 51)", fontsize=12, fontweight="bold")
for bar, val in zip(ax.patches, group_sums):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, str(val),
            ha="center", fontsize=12, fontweight="bold")

plt.tight_layout()
save_fig("05_centrality_invariants.png")
plt.close()

# --- 06: Wuxing generation/overcoming ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
phase_graph = nx.DiGraph()
phase_relations = [(u, v, "generation") for u, v in GENERATION] + [
    (u, v, "overcoming") for u, v in OVERCOMING
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
nx.draw_networkx_labels(phase_graph, wx_pos, font_size=12, ax=ax)
rel_handles = [
    Line2D([0], [0], color="#44AA44", lw=3, label="Generation"),
    Line2D([0], [0], color="#CC4444", lw=2, linestyle="--", label="Overcoming"),
]
ax.legend(handles=rel_handles, loc="upper right", fontsize=11)
ax.set_title("Wuxing generation/overcoming relations", fontsize=13, fontweight="bold")
ax.set_xlim(-3, 3.5)
ax.set_ylim(-2.5, 3)
ax.axis("off")

ax = axes[1]
categories = ["generation", "overcoming", "same_phase"]
cat_labels = [RELATION_LABELS[c] for c in categories]
counts_T = [wx_edges_T.get(c, 0) for c in categories]
counts_co = [wx_edges_co.get(c, 0) for c in categories]
x = np.arange(3)
bars1 = ax.bar(x - 0.2, counts_T, width=0.4, color="#4488CC", edgecolor="black",
               label="T-forest (12 edges)")
bars2 = ax.bar(x + 0.2, counts_co, width=0.4, color="#CC9944", edgecolor="black",
               label="Co-membership (56 edges)")
for bars, total in [(bars1, 12), (bars2, 56)]:
    for bar, cnt in zip(bars, [c for c in (counts_T if total == 12 else counts_co)]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.4,
                f"{cnt}\n({100 * cnt / total:.0f}%)", ha="center", fontsize=10,
                fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(cat_labels, fontsize=12)
ax.set_title("Wuxing edge-relation classification", fontsize=13, fontweight="bold")
ax.set_ylabel("Edge count", fontsize=10)
ax.legend(fontsize=10)
plt.tight_layout()
save_fig("06_wuxing_relations.png")
plt.close()

# --- 07: Generalization family / extension schematic ---
fig, axes = plt.subplots(1, 2, figsize=(17, 8))

ax = axes[0]
draw_group_regions(ax, with_sum_labels=False)
draw_nodes(ax, radius=0.28, fontsize=9)
hinge_annotations = [
    ((7, 11), "7·11\nΣ=18", (-2.6, 2.0)),
    ((6, 10), "6·10\nΣ=16", (2.6, 2.0)),
    ((8, 9), "8·9\nΣ=17", (-2.6, -2.0)),
    ((5, 12), "5·12\nΣ=17", (2.6, -2.0)),
]
for (a, b), label, (lx, ly) in hinge_annotations:
    x1, y1 = POSITIONS[a]
    x2, y2 = POSITIONS[b]
    ax.plot([x1, x2], [y1, y2], color="red", linewidth=2.5, alpha=0.8, zorder=2)
    ax.text(lx, ly, label, ha="center", va="center", fontsize=10, fontweight="bold",
            color="red",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="red",
                      alpha=0.9),
            zorder=3)
setup_geo_ax(ax, "Structural blueprint: four 6-number groups + 4 shared pairs (hinges)")
ax.text(0, -4.9, "Checksum: 4 × 51 = 204 = 136 + 68   (k·S = T + D, shared 8 values counted twice)",
        ha="center", fontsize=12, fontweight="bold", color="#333333")

ax = axes[1]
pair_lines = [
    ("Top group (sum 51 = 3 × 17)", [(16, 1), (6, 11), (7, 10)], True),
    ("Bottom group (sum 51 = 3 × 17)", [(8, 9), (2, 15), (12, 5)], True),
    ("Left group", [(7, 10), (13, 4), (11, 6)], False),
    ("Right group", [(6, 11), (10, 7), (4, 13)], False),
]
y_cursor = 0.92
for title, pairs, ok in pair_lines:
    color = "#226622" if ok else "#AA2222"
    ax.text(0.03, y_cursor, title, fontsize=13, fontweight="bold", color=color,
            transform=ax.transAxes)
    y_cursor -= 0.09
    if ok:
        for i, (a, b) in enumerate(pairs):
            x0 = 0.06 + i * 0.31
            ax.text(x0 + 0.09, y_cursor, f"{a} + {b} = 17", fontsize=12,
                    ha="center", transform=ax.transAxes,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="#E8F5E9",
                              edgecolor="#226622"))
    else:
        missing = ", ".join(f"complement {b} of {a} missing" for a, b in pairs[:2]) + " …"
        ax.text(0.06, y_cursor, f"no sum-17 perfect matching: {missing}", fontsize=11,
                color="#AA2222", transform=ax.transAxes)
    y_cursor -= 0.12
ax.text(0.03, y_cursor - 0.02,
        "The complementary-pair device (sum 17 = N+1) is the same principle\n"
        "as in the 4×4 magic-square tradition.\n"
        "Only the top/bottom groups implement it fully;\n"
        "the left/right groups sacrifice it to host the shared pairs.",
        fontsize=11, transform=ax.transAxes, va="top",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="lightyellow", edgecolor="black"))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")
ax.set_title("Generalization observation: the complementary-pair (Σ=17) device",
             fontsize=13, fontweight="bold")

plt.tight_layout()
save_fig("07_local_extensions.png")
plt.close()

# --- 08: Position patterns ---
fig, axes = plt.subplots(1, 3, figsize=(21, 7.5))

ax = axes[0]
per_x = [POSITIONS[v][0] for v in PERIMETER] + [POSITIONS[PERIMETER[0]][0]]
per_y = [POSITIONS[v][1] for v in PERIMETER] + [POSITIONS[PERIMETER[0]][1]]
ax.plot(per_x, per_y, color="#4488CC", linewidth=1.8, linestyle="--", alpha=0.7, zorder=1)
inn_x = [POSITIONS[v][0] for v in INNER] + [POSITIONS[INNER[0]][0]]
inn_y = [POSITIONS[v][1] for v in INNER] + [POSITIONS[INNER[0]][1]]
ax.plot(inn_x, inn_y, color="#CC4444", linewidth=1.8, linestyle="--", alpha=0.7, zorder=1)
draw_t_edges(ax, color="#DDDDDD", lw=1.5, alpha=0.8, zorder=0)
draw_nodes(ax, highlight=set(T_CENTERS))
setup_geo_ax(ax, "Positional roles: T centers (red border) · perimeter/inner rings")
role_handles = [
    Line2D([0], [0], marker="o", color="w", markerfacecolor="#F6D0D0",
           markeredgecolor="red", markersize=12, label=f"T centers (Σ={sum(T_CENTERS)})"),
    Line2D([0], [0], color="#4488CC", lw=2, linestyle="--", label=f"Perimeter 12-cycle (Σ={sum(PERIMETER)})"),
    Line2D([0], [0], color="#CC4444", lw=2, linestyle="--", label=f"Inner 4-cycle (Σ={sum(INNER)})"),
]
ax.legend(handles=role_handles, loc="lower right", fontsize=9)

ax = axes[1]
pos_subsets = [
    ("Perimeter\n12-ring", sum(PERIMETER), "#4488CC"),
    ("Inner\n4-ring", sum(INNER), "#CC4444"),
    ("T centers\n4 values", sum(T_CENTERS), "#44AA44"),
    ("T spokes\n12 values", sum(T_SPOKES), "#CC9944"),
    ("Shared\n8 values", sum(SHARED_VALUES), "#9966CC"),
    ("Unshared\n8 values", sum(UNSHARED_VALUES), "#669999"),
]
ax.bar([s[0] for s in pos_subsets], [s[1] for s in pos_subsets],
       color=[s[2] for s in pos_subsets], edgecolor="black", linewidth=1.5)
for bar, (_, val, _) in zip(ax.patches, pos_subsets):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5, str(val),
            ha="center", fontsize=12, fontweight="bold")
ax.set_ylim(0, 125)
ax.set_title("Positional subset sums", fontsize=13, fontweight="bold")
ax.set_ylabel("Sum", fontsize=10)
ax.axhline(y=68, color="#9966CC", linestyle=":", linewidth=1.5, alpha=0.8)

ax = axes[2]
y_levels = sorted(rows, reverse=True)
row_labels = []
for y in y_levels:
    vals = sorted(rows[y])
    row_labels.append("+".join(map(str, vals)))
bar_colors = ["#4488CC" if i < 4 else "#CC9944" for i in range(8)]
ax.bar(range(8), ROW_SUMS, color=bar_colors, edgecolor="black", linewidth=1.5)
for i, val in enumerate(ROW_SUMS):
    ax.text(i, val + 0.3, str(val), ha="center", fontsize=12, fontweight="bold")
ax.set_xticks(range(8))
ax.set_xticklabels(row_labels, fontsize=8, rotation=30, ha="right")
ax.set_title(f"Row sums by y coordinate: {ROW_SUMS}\ntop-bottom symmetric (palindrome)",
             fontsize=13, fontweight="bold")
ax.set_ylabel("Row sum", fontsize=10)
ax.set_ylim(0, 25)

plt.tight_layout()
save_fig("08_position_patterns.png")
plt.close()

# ============================================================
# 8. Summary
# ============================================================

print("\n" + "=" * 60)
print("Verified key properties — summary")
print("=" * 60)
print("1. 1..16 each once, total sum 136, 4 groups each summing to 51")
print("2. k·S = T + D: 4 × 51 = 204 = 136 + 68 (shared 8 values counted twice)")
print(f"3. T centers {T_CENTERS}: 4 consecutive integers, sum {sum(T_CENTERS)}")
print(f"4. T spokes (12 values) sum {sum(T_SPOKES)}")
print("5. Top/bottom groups decompose into 3 complementary pairs (sum 17); left/right do not (asymmetry)")
print("6. Shared-pair sums: 7+11=18, 6+10=16, 8+9=17, 5+12=17")
print(f"7. Inner 4-cycle sum {sum(INNER)}, perimeter 12-cycle sum {sum(PERIMETER)}")
print(f"8. Shared 8 values sum {sum(SHARED_VALUES)} = unshared 8 values sum {sum(UNSHARED_VALUES)} = 68")
print(f"9. Row-sum palindrome: {ROW_SUMS}")
print(f"10. Spectra: co-membership λ_max={eig_co[-1]:.4f}, λ_min={eig_co[0]:.4f}; T-forest λ=±√3")

print("\n" + "=" * 60)
print("All figures generated!")
print(f"Output directory: {OUTPUT_DIR.resolve()}/")
print("=" * 60)
