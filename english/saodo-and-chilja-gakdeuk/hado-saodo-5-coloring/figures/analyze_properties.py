#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Detailed property analysis of the Sa-o-do (A puzzle of Four and Five) 5-coloring puzzle.
Generates figures for symmetry, row/column sums, group distribution,
Heto correspondence, adjacency hypothesis, and orientation.
"""

import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# --------------------------------------------------
# Data: corrected layout
# --------------------------------------------------

nodes = [
    # top arm (y=3,2; x=-1,0) — adjacent to the central body to form a cross
    {"pos": (-1, 3), "label": 19},
    {"pos": (0, 3),  "label": 2},
    {"pos": (-1, 2), "label": 7},
    {"pos": (0, 2),  "label": 14},

    # central body (y=1,0; x=-3,-2,-1,0,1,2)
    {"pos": (-3, 1), "label": 13},
    {"pos": (-2, 1), "label": 8},
    {"pos": (-1, 1), "label": 5},
    {"pos": (0, 1),  "label": 16},
    {"pos": (1, 1),  "label": 4},
    {"pos": (2, 1),  "label": 17},

    {"pos": (-3, 0), "label": 18},
    {"pos": (-2, 0), "label": 3},
    {"pos": (-1, 0), "label": 11},
    {"pos": (0, 0),  "label": 10},
    {"pos": (1, 0),  "label": 12},
    {"pos": (2, 0),  "label": 9},

    # bottom arm (y=-1,-2; x=-1,0)
    {"pos": (-1, -1), "label": 15},
    {"pos": (0, -1),  "label": 1},
    {"pos": (-1, -2), "label": 6},
    {"pos": (0, -2),  "label": 20},
]

GROUP_COLORS = {
    1: "#4A90E2",  # Water
    2: "#E94B3C",  # Fire
    3: "#6AB04C",  # Wood
    4: "#BDC3C7",  # Metal
    5: "#D4A017",  # Earth
}

GROUP_NAMES = {
    1: "Water",
    2: "Fire",
    3: "Wood",
    4: "Metal",
    5: "Earth",
}


def group_of(n):
    g = n % 5
    return 5 if g == 0 else g


def setup_axis(ax, title):
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor('#FDFBF7')
    ax.set_title(title, fontsize=12, fontweight='bold', color='#2C3E50', pad=10)


# --------------------------------------------------
# 1. Symmetry analysis
# --------------------------------------------------

def draw_symmetry_analysis(save_path="figures/analysis_01_symmetry.png"):
    fig, axes = plt.subplots(1, 3, figsize=(16, 6))
    fig.patch.set_facecolor('#FDFBF7')

    titles = ["Original layout", "180° rotation test", "Reflection test (x=0)"]
    for ax, title in zip(axes, titles):
        setup_axis(ax, title)

    # Original
    ax = axes[0]
    for node in nodes:
        x, y = node["pos"]
        label = node["label"]
        g = group_of(label)
        circ = plt.Circle((x, y), 0.35, color='white', ec=GROUP_COLORS[g], linewidth=2, zorder=2)
        ax.add_patch(circ)
        ax.text(x, y, str(label), fontsize=8, ha='center', va='center',
                fontweight='bold', color='#2C3E50', zorder=3)
    ax.set_xlim(-4, 4)
    ax.set_ylim(-3, 6)

    # 180 rotation: (x,y) -> (-x,-y)
    ax = axes[1]
    label_map = {n["label"]: n["pos"] for n in nodes}
    for node in nodes:
        x, y = node["pos"]
        rx, ry = -x, -y
        label = node["label"]
        g = group_of(label)
        # draw original slot faintly
        circ = plt.Circle((x, y), 0.35, color='#FDFBF7', ec='#BDC3C7', linewidth=1, alpha=0.3)
        ax.add_patch(circ)
        # draw rotated position
        circ2 = plt.Circle((rx, ry), 0.35, color='white', ec=GROUP_COLORS[g], linewidth=2, zorder=2)
        ax.add_patch(circ2)
        ax.text(rx, ry, str(label), fontsize=8, ha='center', va='center',
                fontweight='bold', color='#2C3E50', zorder=3)
    ax.text(0, -2.5, "Slots do not coincide:\nshape is symmetric, labeling is not",
            fontsize=10, ha='center', va='center', color='#E94B3C', fontweight='bold')
    ax.set_xlim(-4, 4)
    ax.set_ylim(-3, 6)

    # Reflection x=0
    ax = axes[2]
    for node in nodes:
        x, y = node["pos"]
        rx, ry = -x, y
        label = node["label"]
        g = group_of(label)
        circ = plt.Circle((x, y), 0.35, color='#FDFBF7', ec='#BDC3C7', linewidth=1, alpha=0.3)
        ax.add_patch(circ)
        circ2 = plt.Circle((rx, ry), 0.35, color='white', ec=GROUP_COLORS[g], linewidth=2, zorder=2)
        ax.add_patch(circ2)
        ax.text(rx, ry, str(label), fontsize=8, ha='center', va='center',
                fontweight='bold', color='#2C3E50', zorder=3)
    ax.text(0, -2.5, "Reflection also fails:\nleft/right labels differ",
            fontsize=10, ha='center', va='center', color='#E94B3C', fontweight='bold')
    ax.set_xlim(-4, 4)
    ax.set_ylim(-3, 6)

    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {save_path}")


# --------------------------------------------------
# 2. Row/column sums
# --------------------------------------------------

def draw_row_column_sums(save_path="figures/analysis_02_rowcol.png"):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor('#FDFBF7')

    # Row sums by y-coordinate
    row_sums = defaultdict(int)
    for node in nodes:
        row_sums[node["pos"][1]] += node["label"]

    ax = axes[0]
    ax.set_facecolor('#FDFBF7')
    ax.set_title("Row sums (by y-coordinate)", fontsize=13, fontweight='bold', color='#2C3E50')
    ys = sorted(row_sums.keys(), reverse=True)
    vals = [row_sums[y] for y in ys]
    bars = ax.barh([str(y) for y in ys], vals, color=['#4A90E2', '#4A90E2', '#6AB04C',
                                                     '#6AB04C', '#D4A017', '#D4A017'])
    for i, (y, v) in enumerate(zip(ys, vals)):
        ax.text(v + 1, i, str(v), va='center', color='#2C3E50', fontweight='bold')
    ax.set_xlabel("Sum")
    ax.set_ylabel("y-coordinate")
    ax.invert_yaxis()
    ax.set_xlim(0, max(vals) + 10)

    # Column sums by x-coordinate
    col_sums = defaultdict(int)
    for node in nodes:
        col_sums[node["pos"][0]] += node["label"]

    ax = axes[1]
    ax.set_facecolor('#FDFBF7')
    ax.set_title("Column sums (by x-coordinate)", fontsize=13, fontweight='bold', color='#2C3E50')
    xs = sorted(col_sums.keys())
    vals = [col_sums[x] for x in xs]
    bars = ax.bar([str(x) for x in xs], vals, color=['#E94B3C', '#E94B3C', '#4A90E2',
                                                     '#4A90E2', '#E94B3C', '#E94B3C'])
    for i, (x, v) in enumerate(zip(xs, vals)):
        ax.text(i, v + 1, str(v), ha='center', color='#2C3E50', fontweight='bold')
    ax.set_ylabel("Sum")
    ax.set_xlabel("x-coordinate")
    ax.set_ylim(0, max(vals) + 10)

    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {save_path}")


# --------------------------------------------------
# 3. Group distribution heatmap
# --------------------------------------------------

def draw_group_distribution(save_path="figures/analysis_03_distribution.png"):
    fig, ax = plt.subplots(figsize=(10, 8))
    setup_axis(ax, "Group distribution on the layout")

    # Build a grid map
    grid = {}
    for node in nodes:
        grid[node["pos"]] = node["label"]

    all_x = sorted({p[0] for p in grid})
    all_y = sorted({p[1] for p in grid}, reverse=True)

    for y in all_y:
        for x in all_x:
            if (x, y) in grid:
                label = grid[(x, y)]
                g = group_of(label)
                color = GROUP_COLORS[g]
                circ = plt.Circle((x, y), 0.4, color='white', ec=color, linewidth=3, zorder=2)
                ax.add_patch(circ)
                ax.text(x, y, str(label), fontsize=12, ha='center', va='center',
                        fontweight='bold', color='#2C3E50', zorder=3)

    # Legend
    for i, g in enumerate([1, 2, 3, 4, 5]):
        y_leg = 5.2 - i * 0.5
        circ = plt.Circle((3.2, y_leg), 0.15, color=GROUP_COLORS[g], ec='#2C3E50', linewidth=1)
        ax.add_patch(circ)
        ax.text(3.55, y_leg, GROUP_NAMES[g], fontsize=10, va='center', color='#2C3E50')

    # Region annotations
    ax.text(-3.6, 0.5, "Wood\nzone", fontsize=10, ha='center', va='center',
            color='#6AB04C', fontweight='bold')
    ax.text(1.4, -1.5, "Water/Earth\ninterleaved", fontsize=10, ha='center', va='center',
            color='#2C3E50', fontweight='bold')
    ax.text(0, 3.7, "Fire/Metal\nmixed", fontsize=10, ha='center', va='center',
            color='#2C3E50', fontweight='bold')

    ax.set_xlim(-4, 4.5)
    ax.set_ylim(-3, 6.5)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {save_path}")


# --------------------------------------------------
# 4. Heto correspondence
# --------------------------------------------------

def draw_heto_correspondence(save_path="figures/analysis_04_heto.png"):
    fig, ax = plt.subplots(figsize=(10, 10))
    setup_axis(ax, "Classical Heto direction-phase correspondence")

    # Draw cross layout with phase zones
    zones = {
        "North\n(Water/Earth)": (0, -2.5, 2.2),
        "South\n(Fire/Metal)": (0, 3.2, 2.2),
        "East\n(Wood)": (-3.5, 0.5, 2.2),
        "West\n(Fire/Metal)": (3.5, 0.5, 2.2),
        "Center\n(Water/Earth)": (0, 0.5, 2.5),
    }

    for name, (x, y, r) in zones.items():
        circ = plt.Circle((x, y), r, color='white', ec='#BDC3C7', linewidth=1.5, linestyle='--', alpha=0.5)
        ax.add_patch(circ)
        ax.text(x, y, name, fontsize=9, ha='center', va='center', color='#7F8C8D')

    for node in nodes:
        x, y = node["pos"]
        label = node["label"]
        g = group_of(label)
        circ = plt.Circle((x, y), 0.32, color='white', ec=GROUP_COLORS[g], linewidth=2, zorder=2)
        ax.add_patch(circ)
        ax.text(x, y, str(label), fontsize=8, ha='center', va='center',
                fontweight='bold', color='#2C3E50', zorder=3)

    ax.text(0, -3.5, "Classical Heto: N=Water(1,6), S=Fire(2,7), E=Wood(3,8), W=Metal(4,9), C=Earth(5,10)",
            fontsize=9, ha='center', va='center', color='#2C3E50')

    ax.set_xlim(-5, 5)
    ax.set_ylim(-4.5, 6.5)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {save_path}")


# --------------------------------------------------
# 5. Adjacency hypothesis (k-nearest)
# --------------------------------------------------

def draw_adjacency_hypothesis(save_path="figures/analysis_05_adjacency.png"):
    fig, ax = plt.subplots(figsize=(10, 10))
    setup_axis(ax, "Adjacency hypothesis: nearest-neighbor graph")

    positions = np.array([n["pos"] for n in nodes])
    labels = [n["label"] for n in nodes]

    # Draw edges to 2 nearest neighbors (excluding self)
    for i, (x, y) in enumerate(positions):
        dists = np.linalg.norm(positions - np.array([x, y]), axis=1)
        nearest = np.argsort(dists)[1:3]
        for j in nearest:
            x2, y2 = positions[j]
            ax.plot([x, x2], [y, y2], 'k-', alpha=0.2, linewidth=1, zorder=1)

    for node in nodes:
        x, y = node["pos"]
        label = node["label"]
        g = group_of(label)
        circ = plt.Circle((x, y), 0.32, color='white', ec=GROUP_COLORS[g], linewidth=2, zorder=2)
        ax.add_patch(circ)
        ax.text(x, y, str(label), fontsize=8, ha='center', va='center',
                fontweight='bold', color='#2C3E50', zorder=3)

    ax.text(0, -3.0, "Hypothetical edges: 2-nearest Euclidean neighbors\n(no edges are explicitly given in the original text)",
            fontsize=10, ha='center', va='center', color='#2C3E50')

    ax.set_xlim(-4, 4)
    ax.set_ylim(-3.5, 6)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {save_path}")


# --------------------------------------------------
# 6. Orientation analysis
# --------------------------------------------------

def draw_orientation_analysis(save_path="figures/analysis_06_orientation.png"):
    fig, ax = plt.subplots(figsize=(10, 8))
    setup_axis(ax, "Numeral orientation analysis")

    theta_deg = -30
    for node in nodes:
        x, y = node["pos"]
        label = node["label"]
        g = group_of(label)
        circ = plt.Circle((x, y), 0.35, color='white', ec=GROUP_COLORS[g], linewidth=2, zorder=2)
        ax.add_patch(circ)
        ax.text(x, y, str(label), fontsize=9, ha='center', va='center',
                fontweight='bold', color='#2C3E50', zorder=3,
                rotation=theta_deg, rotation_mode='anchor')
        # small arrow showing orientation
        rad = np.radians(theta_deg)
        ax.annotate('', xy=(x + 0.5*np.cos(rad), y + 0.5*np.sin(rad)),
                    xytext=(x, y),
                    arrowprops=dict(arrowstyle='->', color='#95A5A6', lw=1))

    ax.text(0, -3.0, f"All numerals share approximately θ = {theta_deg}°\nmeaning remains unknown",
            fontsize=11, ha='center', va='center', color='#2C3E50', fontweight='bold')

    ax.set_xlim(-4, 4)
    ax.set_ylim(-3.5, 6)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {save_path}")


# --------------------------------------------------
# Run
# --------------------------------------------------

if __name__ == "__main__":
    draw_symmetry_analysis()
    draw_row_column_sums()
    draw_group_distribution()
    draw_heto_correspondence()
    draw_adjacency_hypothesis()
    draw_orientation_analysis()
    print("All detailed analysis figures generated.")
