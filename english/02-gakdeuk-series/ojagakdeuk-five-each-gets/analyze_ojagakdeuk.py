#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ojagakdeuk (Five-Each-Gets / Heaven-Water Five-Use Diagram) — modern combinatorial and positional analysis

A modern mathematical reinterpretation of Ojagakdeuk (五子各得), also known as
Cheonsu-yong-odo (天水用五圖), from the *Gusuryak* (九數略) family of diagrams.
Analysis target: a diagram placing 21 of the numbers 1–24 in the Cheonsu-yong-odo form.

This script analyzes only positional, wuxing (five-phase), and combinatorial
invariants, because the original diagram has no edges.
"""

import os
from collections import Counter

import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
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
# 1. Original data structure
# ============================================================

POSITIONS: dict[int, tuple[float, float]] = {
    19: (0.0, 6.0),
    12: (-1.5, 5.0),
    8:  (1.5, 5.0),
    6:  (0.0, 4.2),
    4:  (-2.8, 3.3),
    20: (0.0, 3.3),
    7:  (2.8, 3.3),
    21: (-4.2, 2.0),
    23: (-2.8, 2.0),
    1:  (-1.4, 2.0),
    5:  (0.0, 2.0),
    15: (1.4, 2.0),
    14: (2.8, 2.0),
    18: (4.2, 2.0),
    16: (-2.8, 0.8),
    24: (0.0, 0.8),
    11: (2.8, 0.8),
    9:  (-1.8, -0.4),
    17: (0.0, -0.4),
    13: (1.8, -0.4),
    2:  (0.0, -1.7),
}

GROUPS: dict[int, list[int]] = {
    1: [1, 6, 11, 16, 21],
    2: [2, 7, 12, 17],
    3: [8, 13, 18, 23],
    4: [4, 9, 14, 19, 24],
    0: [5, 15, 20],
}

RESIDUE_STYLE: dict[int, dict[str, str]] = {
    1: {"face": "#E0E0E0", "edge": "#333333", "name": "Water", "en": "Water"},
    2: {"face": "#F4D0D0", "edge": "#B33B3B", "name": "Fire", "en": "Fire"},
    3: {"face": "#D4E4F8", "edge": "#3A6FAE", "name": "Wood", "en": "Wood"},
    4: {"face": "#E5E5E5", "edge": "#666666", "name": "Metal", "en": "Metal"},
    0: {"face": "#F6E5A3", "edge": "#C39A00", "name": "Earth", "en": "Earth"},
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
# 2. Combinatorial and positional analysis
# ============================================================


def validate() -> None:
    all_values = sorted(POSITIONS.keys())
    assert all_values == sorted(set(POSITIONS)), "21 distinct numbers"
    assert set(all_values) == set(range(1, 25)) - {3, 10, 22}, "1–24 excluding 3, 10, 22"
    assert sum(all_values) == 265, "total sum is 265"
    grouped = [n for nums in GROUPS.values() for n in nums]
    assert sorted(grouped) == all_values, "GROUPS partition all numbers exactly"


validate()

print("=" * 60)
print("Ojagakdeuk (Five-Each-Gets / Heaven-Water Five-Use Diagram)")
print("Modern combinatorial and positional analysis")
print("=" * 60)
print(f"Number of nodes: {len(POSITIONS)}")
print("Because the original has no edges, graph-theoretic metrics (degree, betweenness, cycles, spectrum) are not analyzed.")

print("\nSum by wuxing:")
for r in [1, 2, 3, 4, 5]:
    nodes = [n for n in POSITIONS if residue_1based(n) == r]
    ph = RESIDUE_STYLE[r % 5]["name"]
    print(f"  {ph}({r}): sum={sum(nodes)}, numbers={sorted(nodes)}")

print("\nPositional distribution by wuxing:")
for r in [1, 2, 3, 4, 0]:
    nums = GROUPS[r]
    ph = RESIDUE_STYLE[r]["name"]
    print(f"  {ph}: {len(nums)} numbers - {sorted(nums)}")

# Sum by horizontal level (y-coordinate)
LEVELS: dict[float, list[int]] = {}
for n, (x, y) in POSITIONS.items():
    LEVELS.setdefault(round(y, 1), []).append(n)
LEVEL_ORDER = sorted(LEVELS.keys(), reverse=True)

# Left / center / right partition
LEFT_VALUES = [n for n, (x, _) in POSITIONS.items() if x < -0.5]
MID_VALUES = [n for n, (x, _) in POSITIONS.items() if -0.5 <= x <= 0.5]
RIGHT_VALUES = [n for n, (x, _) in POSITIONS.items() if x > 0.5]

print("\nSum by horizontal level:")
for y in LEVEL_ORDER:
    nums = LEVELS[y]
    print(f"  y={y}: {sorted(nums)} sum={sum(nums)}")

print(f"\nLeft / center / right partition:")
print(f"  Left: {sorted(LEFT_VALUES)} sum={sum(LEFT_VALUES)}")
print(f"  Center: {sorted(MID_VALUES)} sum={sum(MID_VALUES)}")
print(f"  Right: {sorted(RIGHT_VALUES)} sum={sum(RIGHT_VALUES)}")

# ============================================================
# 3. Visualizations
# ============================================================


def draw_nodes(ax, highlight_values=None, alpha_other=1.0, radius=0.32):
    """Basic node drawing."""
    for value, (x, y) in POSITIONS.items():
        r = value % 5
        style = RESIDUE_STYLE[r]
        color = style["face"]
        edge = style["edge"]
        lw = 2.5
        if highlight_values is not None and value not in highlight_values:
            color = "#F0F0F0"
            edge = "#CCCCCC"
            lw = 1.2
        ax.add_patch(
            plt.Circle(
                (x, y),
                radius,
                facecolor=color,
                edgecolor=edge,
                linewidth=lw,
                zorder=2,
            )
        )
        text_color = "black"
        if highlight_values is not None and value not in highlight_values:
            text_color = "#AAAAAA"
        ax.text(
            x,
            y,
            str(value),
            ha="center",
            va="center",
            fontsize=10,
            fontweight="bold",
            color=text_color,
            zorder=3,
        )


# --- 01: Original structure (no edges) ---
fig, ax = plt.subplots(figsize=(12, 12))
draw_nodes(ax)
ax.set_title(
    "Ojagakdeuk (Five-Each-Gets / Heaven-Water Five-Use Diagram) — Original placement\n"
    "21 numbers · mod 5 wuxing classification · Cheonsu-yong-odo geometric structure",
    fontsize=16,
    fontweight="bold",
)
ax.set_xlim(-5.0, 5.0)
ax.set_ylim(-2.4, 6.8)
ax.set_aspect("equal")
ax.axis("off")
legend_elements = [
    mpatches.Patch(facecolor=PHASE_COLOR[ph], edgecolor="black", label=f"{ph}")
    for ph in ["Water", "Fire", "Wood", "Metal", "Earth"]
]
ax.legend(handles=legend_elements, loc="lower right", fontsize=10, framealpha=0.9)
save_fig("01_original_graph.png")
plt.close()

# --- 02: Wuxing subgroup decomposition (no edges) ---
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()

ax = axes[0]
draw_nodes(ax)
ax.set_title("Full placement", fontsize=13, fontweight="bold")
ax.set_xlim(-5.0, 5.0)
ax.set_ylim(-2.4, 6.8)
ax.set_aspect("equal")
ax.axis("off")

for idx, ph in enumerate(["Water", "Fire", "Wood", "Metal", "Earth"]):
    ax = axes[idx + 1]
    ph_nodes = [n for n in POSITIONS if phase_of(n) == ph]
    other_nodes = [n for n in POSITIONS if n not in ph_nodes]

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
    ax.set_xlim(-5.0, 5.0)
    ax.set_ylim(-2.4, 6.8)
    ax.set_aspect("equal")
    ax.axis("off")

plt.suptitle("Wuxing (five-phase) subgroup decomposition", fontsize=16, fontweight="bold", y=1.02)
plt.tight_layout()
save_fig("02_wuxing_decomposition.png")
plt.close()

# --- 03: mod 5 residue spatial distribution (heatmap) ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

ax = axes[0]
# x-axis: coordinate column (rounded), y-axis: horizontal level
xs = sorted(set(round(x, 1) for x, _ in POSITIONS.values()))
ys = LEVEL_ORDER
# Map residue values onto the grid
grid = np.full((len(ys), len(xs)), np.nan)
for n, (x, y) in POSITIONS.items():
    r = residue_1based(n)
    i = ys.index(round(y, 1))
    j = xs.index(round(x, 1))
    grid[i, j] = r

im = ax.imshow(grid, cmap="tab10", vmin=1, vmax=5, aspect="auto")
ax.set_xticks(range(len(xs)))
ax.set_yticks(range(len(ys)))
ax.set_xticklabels([str(x) for x in xs], fontsize=9)
ax.set_yticklabels([f"y={y}" for y in ys], fontsize=9)
ax.set_title("mod 5 residue spatial distribution", fontsize=13, fontweight="bold")
ax.set_xlabel("x-coordinate", fontsize=11)
ax.set_ylabel("y-coordinate", fontsize=11)

# Show numbers inside cells
for n, (x, y) in POSITIONS.items():
    i = ys.index(round(y, 1))
    j = xs.index(round(x, 1))
    ax.text(j, i, str(n), ha="center", va="center", fontsize=9, fontweight="bold",
            color="white" if n % 5 in [3, 0] else "black")

# Colorbar
from matplotlib.colors import BoundaryNorm
sm = plt.cm.ScalarMappable(cmap="tab10", norm=BoundaryNorm([0.5, 1.5, 2.5, 3.5, 4.5, 5.5], 5))
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, ticks=[1, 2, 3, 4, 5], shrink=0.8)
cbar.ax.set_yticklabels(["Water", "Fire", "Wood", "Metal", "Earth"])

ax = axes[1]
# x-coordinate distribution for each wuxing
for ph in ["Water", "Fire", "Wood", "Metal", "Earth"]:
    nodes = [n for n in POSITIONS if phase_of(n) == ph]
    xvals = [POSITIONS[n][0] for n in nodes]
    yvals = [POSITIONS[n][1] for n in nodes]
    ax.scatter(xvals, yvals, c=PHASE_COLOR[ph], s=200, edgecolors="black", linewidths=1.5, label=ph, zorder=2)
    for n in nodes:
        ax.text(POSITIONS[n][0], POSITIONS[n][1], str(n), ha="center", va="center",
                fontsize=8, fontweight="bold", zorder=3)
ax.set_xlim(-5.0, 5.0)
ax.set_ylim(-2.4, 6.8)
ax.set_aspect("equal")
ax.axvline(x=0, color="gray", linestyle="--", linewidth=1, alpha=0.5)
ax.axhline(y=0, color="gray", linestyle="--", linewidth=1, alpha=0.5)
ax.set_title("Coordinate distribution by wuxing", fontsize=13, fontweight="bold")
ax.legend(loc="lower right", fontsize=10)
ax.axis("off")

plt.tight_layout()
save_fig("03_spatial_distribution.png")
plt.close()

# --- 04: Symmetry analysis ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

ax = axes[0]
# Left-right symmetry: color nodes by x sign
for n, (x, y) in POSITIONS.items():
    if x < -0.5:
        color = "#4488CC"
        label = "Left"
    elif x > 0.5:
        color = "#CC4444"
        label = "Right"
    else:
        color = "#44AA44"
        label = "Center"
    ax.add_patch(
        plt.Circle(
            (x, y),
            0.32,
            facecolor=color,
            edgecolor="black",
            linewidth=2,
            zorder=2,
        )
    )
    ax.text(x, y, str(n), ha="center", va="center", fontsize=9, fontweight="bold", zorder=3)

# Legend
legend_elements = [
    mpatches.Patch(facecolor="#4488CC", edgecolor="black", label=f"Left (sum {sum(LEFT_VALUES)})"),
    mpatches.Patch(facecolor="#44AA44", edgecolor="black", label=f"Center (sum {sum(MID_VALUES)})"),
    mpatches.Patch(facecolor="#CC4444", edgecolor="black", label=f"Right (sum {sum(RIGHT_VALUES)})"),
]
ax.legend(handles=legend_elements, loc="lower right", fontsize=10)
ax.set_xlim(-5.0, 5.0)
ax.set_ylim(-2.4, 6.8)
ax.set_aspect("equal")
ax.axvline(x=0, color="gray", linestyle="--", linewidth=1.5, alpha=0.5)
ax.set_title("Left · Center · Right symmetric distribution", fontsize=13, fontweight="bold")
ax.axis("off")

ax = axes[1]
# Sum by horizontal level
level_sums = [sum(LEVELS[y]) for y in LEVEL_ORDER]
level_names = [f"y={y}" for y in LEVEL_ORDER]
colors_level = ["#CC4444", "#4488CC", "#44AA44", "#CC9944", "#888888", "#AA44AA", "#44AAAA", "#CC8844"]
ax.barh(level_names, level_sums, color=colors_level[:len(level_names)], edgecolor="black", linewidth=1.5)
ax.set_title("Sum by horizontal level", fontsize=13, fontweight="bold")
ax.set_xlabel("Sum", fontsize=11)
for i, val in enumerate(level_sums):
    ax.text(val + 1, i, str(val), va="center", fontsize=11, fontweight="bold")

plt.tight_layout()
save_fig("04_symmetry_analysis.png")
plt.close()

# --- 05: Sum invariants ---
fig, axes = plt.subplots(2, 2, figsize=(16, 14))

ax = axes[0, 0]
ph_sums = {ph: sum([n for n in POSITIONS if phase_of(n) == ph]) for ph in ["Water", "Fire", "Wood", "Metal", "Earth"]}
ph_names = list(ph_sums.keys())
ph_vals = list(ph_sums.values())
ph_colors_bar = [PHASE_COLOR[w] for w in ph_names]
ax.bar(ph_names, ph_vals, color=ph_colors_bar, edgecolor="black", linewidth=1.5)
ax.set_title("Sum by wuxing (55, 38, 62, 70, 40)", fontsize=12, fontweight="bold")
for bar, val in zip(ax.patches, ph_vals):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        str(val),
        ha="center",
        fontsize=12,
        fontweight="bold",
    )

ax = axes[0, 1]
components = {
    "Left": sum(LEFT_VALUES),
    "Center": sum(MID_VALUES),
    "Right": sum(RIGHT_VALUES),
    "Total": sum(POSITIONS),
}
ax.bar(
    list(components.keys()),
    list(components.values()),
    color=["#4488CC", "#44AA44", "#CC4444", "#333333"],
    edgecolor="black",
    linewidth=1.5,
)
ax.set_title("Left · Center · Right symmetric sums (Left = Right = 86)", fontsize=12, fontweight="bold")
ax.set_ylabel("Sum", fontsize=10)
for bar, val in zip(ax.patches, components.values()):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 2,
        str(val),
        ha="center",
        fontsize=12,
        fontweight="bold",
    )

ax = axes[1, 0]
# Sum by horizontal level (vertical bars)
level_sums_v = [sum(LEVELS[y]) for y in LEVEL_ORDER]
ax.bar(level_names, level_sums_v, color="#CC4444", edgecolor="black", linewidth=1.5)
ax.set_title("Sum by horizontal level", fontsize=12, fontweight="bold")
ax.set_ylabel("Sum", fontsize=10)
plt.setp(ax.xaxis.get_majorticklabels(), rotation=15, ha="right")
for bar, val in zip(ax.patches, level_sums_v):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        str(val),
        ha="center",
        fontsize=10,
        fontweight="bold",
    )

ax = axes[1, 1]
# Rule Variation Model counts per Wuxing
extended_counts = []
for r in [1, 2, 3, 4, 0]:
    base = GROUPS[r]
    missing_same = [n for n in range(1, 26) if n % 5 == r and n not in base]
    extended = base + missing_same[: 5 - len(base)]
    extended_counts.append((RESIDUE_STYLE[r]["name"], len(extended)))
labels = [f"{ph}\n({cnt} elements)" for ph, cnt in extended_counts]
counts = [cnt for _, cnt in extended_counts]
colors_cnt = [PHASE_COLOR[ph] for ph, _ in extended_counts]
ax.bar(labels, counts, color=colors_cnt, edgecolor="black", linewidth=1.5)
ax.set_title("Full 5×5 Rule Variation Model (Count per Wuxing)", fontsize=12, fontweight="bold")
for bar, val in zip(ax.patches, counts):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.05,
        str(val),
        ha="center",
        fontsize=12,
        fontweight="bold",
    )

plt.tight_layout()
save_fig("05_invariants.png")
plt.close()

# --- 06: Wuxing Mutual Generation and Overcoming ---
fig, ax = plt.subplots(figsize=(10, 8))
wuxing_graph_relations = [
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
wx_pos = {"Water": (0, 2), "Wood": (2, 1), "Fire": (1, -1), "Earth": (-1, -1), "Metal": (-2, 1)}
for u, v, r in wuxing_graph_relations:
    x1, y1 = wx_pos[u]
    x2, y2 = wx_pos[v]
    color = "#44AA44" if r == "generation" else "#CC4444"
    style = "-" if r == "generation" else "--"
    rad = 0.15 if r == "generation" else -0.15
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(arrowstyle="->", color=color, lw=2.5 if r == "generation" else 2,
                        connectionstyle=f"arc3,rad={rad}"),
    )

for wx, (x, y) in wx_pos.items():
    ax.add_patch(
        plt.Circle(
            (x, y),
            0.35,
            facecolor=PHASE_COLOR[wx],
            edgecolor="black",
            linewidth=2.5,
            zorder=2,
        )
    )
    ax.text(x, y, wx, ha="center", va="center", fontsize=14, fontweight="bold", zorder=3)

legend_elements = [
    Line2D([0], [0], color="#44AA44", lw=3, label="Generation"),
    Line2D([0], [0], color="#CC4444", lw=2, linestyle="--", label="Overcoming"),
]
ax.legend(handles=legend_elements, loc="upper right", fontsize=12)
ax.set_title("Wuxing Cycle & Relations", fontsize=15, fontweight="bold")
ax.axis("off")
plt.tight_layout()
save_fig("06_wuxing_relations.png")
plt.close()

# --- 07: Rule Variation and Layer Model ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

ax = axes[0]
extended_totals = []
for r in [1, 2, 3, 4, 0]:
    base = GROUPS[r]
    missing_same_residue = [n for n in range(1, 26) if n % 5 == r and n not in base]
    extended = base + missing_same_residue[: 5 - len(base)]
    extended_totals.append((RESIDUE_STYLE[r]["name"], sum(extended), len(extended)))

labels = [f"{ph}\n({cnt} elements)" for ph, _, cnt in extended_totals]
values = [t for _, t, _ in extended_totals]
colors_ext = [PHASE_COLOR[wx] for wx, _, _ in extended_totals]
ax.bar(labels, values, color=colors_ext, edgecolor="black", linewidth=1.5)
ax.set_title("Full 5×5 Rule Variation Model (25-System)", fontsize=13, fontweight="bold")
for bar, val in zip(ax.patches, values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        str(val),
        ha="center",
        fontsize=12,
        fontweight="bold",
    )
ax.set_ylabel("Sum", fontsize=10)

ax = axes[1]
layer_names = ["Top Vertex\n(y=6.0)", "Upper Spoke\n(y=5.0~4.2)", "Central Band\n(y=3.3~2.0)", "Lower Spoke\n(y=0.8~-0.4)", "Bottom Vertex\n(y=-1.7)"]
layer_values = [
    sum(LEVELS[6.0]),
    sum(LEVELS[5.0]) + sum(LEVELS[4.2]),
    sum(LEVELS[3.3]) + sum(LEVELS[2.0]),
    sum(LEVELS[0.8]) + sum(LEVELS[-0.4]),
    sum(LEVELS[-1.7]),
]
layer_colors = ["#CC4444", "#4488CC", "#44AA44", "#CC9944", "#888888"]
ax.barh(layer_names, layer_values, color=layer_colors, edgecolor="black", linewidth=1.5)
ax.set_title("Vertical Layer Sum Distribution", fontsize=13, fontweight="bold")
for bar, val in zip(ax.patches, layer_values):
    ax.text(
        bar.get_width() + 1,
        bar.get_y() + bar.get_height() / 2,
        str(val),
        ha="left",
        va="center",
        fontsize=11,
        fontweight="bold",
    )
ax.set_xlabel("Sum", fontsize=10)

plt.tight_layout()
save_fig("07_rule_variation_model.png")
plt.close()

# --- 08: Position Patterns ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

ax = axes[0]
palace_names = [f"y={y}" for y in LEVEL_ORDER]
level_sums_list = [sum(LEVELS[y]) for y in LEVEL_ORDER]
level_counts = [len(LEVELS[y]) for y in LEVEL_ORDER]
x = np.arange(len(LEVEL_ORDER))
width = 0.35
ax.bar(x - width / 2, level_sums_list, width, label="Level Sum", color="#CC4444", edgecolor="black")
ax2 = ax.twinx()
ax2.bar(x + width / 2, level_counts, width, label="Node Count", color="#4488CC", edgecolor="black", alpha=0.7)
ax.set_xticks(x)
ax.set_xticklabels(palace_names, rotation=15, ha="right")
ax.set_ylabel("Sum", fontsize=10)
ax2.set_ylabel("Node Count", fontsize=10)
ax.set_title("Horizontal Level Sums and Node Counts", fontsize=13, fontweight="bold")

ax = axes[1]
reg_names = ["Left (x < -0.5)", "Center (-0.5 ≤ x ≤ 0.5)", "Right (x > 0.5)"]
reg_values = [86, 93, 86]
ax.bar(reg_names, reg_values, color=["#4488CC", "#CC4444", "#4488CC"], edgecolor="black", linewidth=1.5)
ax.set_title("Left-Center-Right Region Sums (Symmetry 86=86)", fontsize=13, fontweight="bold")
for bar, val in zip(ax.patches, reg_values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        str(val),
        ha="center",
        fontsize=12,
        fontweight="bold",
    )
ax.set_ylabel("Sum", fontsize=10)

plt.tight_layout()
save_fig("08_position_patterns.png")
plt.close()

print("\n" + "=" * 60)
print("All images generated successfully!")
print("Note: This visualization model is a Rule Variation Model created for mathematical study, not the raw historical original facsimile.")
print(f"Output directory: {OUTPUT_DIR}/")
print("=" * 60)
