#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modern visualization of the Chiljagakdeuk (Seven-Each-Gets) puzzle.
All labels and annotations are in English to avoid pseudo-classical naming.
"""

import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

# --------------------------------------------------
# Data
# --------------------------------------------------

# Distance between adjacent cluster centers.  The cluster boundary radius is
# 1.35, so a value of 3.3 leaves a clean 0.6-unit gap between large circles.
CLUSTER_SPACING = 3.3

CLUSTERS = [
    {"id": "C1", "dir": "top",    "pos": (0.0, CLUSTER_SPACING),  "center": 2,  "slots": [29, 1, 24, 34, 11, 19]},
    {"id": "C2", "dir": "left",   "pos": (-CLUSTER_SPACING, 0.0), "center": 3,  "slots": [6, 33, 23, 13, 34, 8]},
    {"id": "C3", "dir": "center", "pos": (0.0, 0.0),              "center": 5,  "slots": [22, 7, 20, 30, 26, 10]},
    {"id": "C4", "dir": "right",  "pos": (CLUSTER_SPACING, 0.0),  "center": 4,  "slots": [15, 28, 9, 18, 32, 14]},
    {"id": "C5", "dir": "bottom", "pos": (0.0, -CLUSTER_SPACING), "center": 1,  "slots": [35, 16, 21, 24, 6, 17]},
]

SLOT_ANGLES = np.linspace(90, 90 - 360, 7)[:-1] * np.pi / 180
SLOT_RADIUS = 1.0

GROUP_COLORS = {
    1: "#4A90E2",  # residue 1
    2: "#E94B3C",  # residue 2
    3: "#6AB04C",  # residue 3
    4: "#BDC3C7",  # residue 4
    5: "#D4A017",  # residue 5
}


def residue(n):
    """1-based mod-5 residue."""
    g = n % 5
    return 5 if g == 0 else g


def cluster_sum(cluster):
    return cluster["center"] + sum(cluster["slots"])


# --------------------------------------------------
# 1. Base layout
# --------------------------------------------------

def draw_base_layout(save_path="figures/base_layout.png"):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor('#FDFBF7')
    fig.patch.set_facecolor('#FDFBF7')
    ax.set_title("Seven-Each-Gets Puzzle: Base Layout\n5 clusters, sum 120 each",
                 fontsize=15, fontweight='bold', color='#2C3E50', pad=10)

    for cluster in CLUSTERS:
        cx, cy = cluster["pos"]

        # cluster boundary
        circ = plt.Circle((cx, cy), 1.35, fill=False, ec='#2C3E50', linewidth=2, zorder=1)
        ax.add_patch(circ)

        # center
        center_color = GROUP_COLORS[residue(cluster["center"])]
        circ = plt.Circle((cx, cy), 0.22, color='white', ec=center_color, linewidth=3, zorder=3)
        ax.add_patch(circ)
        ax.text(cx, cy, str(cluster["center"]), fontsize=12, ha='center', va='center',
                fontweight='bold', color='#2C3E50', zorder=4)

        # peripheral slots
        for i, value in enumerate(cluster["slots"]):
            angle = SLOT_ANGLES[i]
            x = cx + SLOT_RADIUS * np.cos(angle)
            y = cy + SLOT_RADIUS * np.sin(angle)
            color = GROUP_COLORS[residue(value)]

            # radial edge
            ax.plot([cx, x], [cy, y], color='#95A5A6', linewidth=1.2, zorder=1)

            circ = plt.Circle((x, y), 0.22, color='white', ec=color, linewidth=2, zorder=3)
            ax.add_patch(circ)
            ax.text(x, y, str(value), fontsize=9, ha='center', va='center',
                    fontweight='bold', color='#2C3E50', zorder=4)

        # sum label
        ax.text(cx, cy - 1.6, f"sum = {cluster_sum(cluster)}",
                fontsize=10, ha='center', va='center', color='#2C3E50', fontweight='bold')

    # legend (top-left, away from the clusters)
    legend_x = -(CLUSTER_SPACING + 1.7)
    legend_y = CLUSTER_SPACING + 1.1
    ax.text(legend_x, legend_y, "mod 5 residue", fontsize=11, fontweight='bold', color='#2C3E50')
    for i, g in enumerate([1, 2, 3, 4, 5], start=0):
        yy = legend_y - 0.45 - i * 0.4
        circ = plt.Circle((legend_x + 0.15, yy), 0.12, color=GROUP_COLORS[g], ec='#2C3E50', linewidth=1)
        ax.add_patch(circ)
        ax.text(legend_x + 0.45, yy, f"r = {g}", fontsize=9, va='center', color='#2C3E50')

    margin = CLUSTER_SPACING + 2.2
    ax.set_xlim(-margin, margin)
    ax.set_ylim(-margin, margin)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {save_path}")


# --------------------------------------------------
# 2. Residue distribution
# --------------------------------------------------

def draw_residue_distribution(save_path="figures/residue_distribution.png"):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_facecolor('#FDFBF7')
    fig.patch.set_facecolor('#FDFBF7')
    ax.set_title("Residue distribution per cluster (center + peripheral slots)",
                 fontsize=13, fontweight='bold', color='#2C3E50', pad=10)

    clusters = [c["id"] for c in CLUSTERS]
    bottom = np.zeros(5)
    bar_positions = np.arange(5)

    for r in range(1, 6):
        counts = []
        for cluster in CLUSTERS:
            total = [cluster["center"]] + cluster["slots"]
            counts.append(sum(1 for v in total if residue(v) == r))
        ax.bar(bar_positions, counts, bottom=bottom, label=f"r = {r}", color=GROUP_COLORS[r])
        bottom += np.array(counts)

    ax.set_xticks(bar_positions)
    ax.set_xticklabels(clusters)
    ax.set_ylabel("Count")
    ax.set_xlabel("Cluster")
    ax.legend(title="mod 5 residue")
    ax.set_ylim(0, 8)

    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {save_path}")


# --------------------------------------------------
# 3. Center-periphery structure (single cluster detail)
# --------------------------------------------------

def draw_cluster_structure(save_path="figures/cluster_structure.png"):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor('#FDFBF7')
    fig.patch.set_facecolor('#FDFBF7')
    ax.set_title("Cluster template: center + 6 peripheral slots",
                 fontsize=14, fontweight='bold', color='#2C3E50', pad=10)

    cx, cy = 0, 0
    circ = plt.Circle((cx, cy), 1.35, fill=False, ec='#2C3E50', linewidth=2)
    ax.add_patch(circ)

    # center
    circ = plt.Circle((cx, cy), 0.25, color='white', ec='#E94B3C', linewidth=3)
    ax.add_patch(circ)
    ax.text(cx, cy, "center\n(1)", fontsize=10, ha='center', va='center', fontweight='bold')

    # 6 slots
    for i in range(6):
        angle = SLOT_ANGLES[i]
        x = cx + SLOT_RADIUS * np.cos(angle)
        y = cy + SLOT_RADIUS * np.sin(angle)
        ax.plot([cx, x], [cy, y], color='#95A5A6', linewidth=1.5)
        circ = plt.Circle((x, y), 0.22, color='white', ec='#4A90E2', linewidth=2)
        ax.add_patch(circ)
        ax.text(x, y, f"s{i+1}", fontsize=10, ha='center', va='center', fontweight='bold')

    ax.text(0, -2.0, "Σ(center + s1+...+s6) = 120", fontsize=12,
            ha='center', va='center', color='#2C3E50', fontweight='bold')

    ax.set_xlim(-2, 2)
    ax.set_ylim(-2.5, 2.5)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {save_path}")


# --------------------------------------------------
# 4. Duplication analysis
# --------------------------------------------------

def draw_duplication_graph(save_path="figures/duplication_graph.png"):
    fig, ax = plt.subplots(figsize=(9, 9))
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor('#FDFBF7')
    fig.patch.set_facecolor('#FDFBF7')
    ax.set_title("Duplication graph: values appearing in two clusters",
                 fontsize=14, fontweight='bold', color='#2C3E50', pad=10)

    # positions
    pos = {c["id"]: c["pos"] for c in CLUSTERS}

    # draw clusters
    for cluster in CLUSTERS:
        cx, cy = cluster["pos"]
        circ = plt.Circle((cx, cy), 0.35, fill=False, ec='#2C3E50', linewidth=2)
        ax.add_patch(circ)
        ax.text(cx, cy, cluster["id"], fontsize=14, ha='center', va='center', fontweight='bold')

    # find duplicates
    value_to_clusters = {}
    for cluster in CLUSTERS:
        all_vals = [cluster["center"]] + cluster["slots"]
        for v in all_vals:
            value_to_clusters.setdefault(v, []).append(cluster["id"])

    duplicates = {v: ids for v, ids in value_to_clusters.items() if len(ids) == 2}

    # draw edges for duplicates
    drawn = set()
    for v, ids in duplicates.items():
        a, b = ids
        if (a, b) in drawn or (b, a) in drawn:
            continue
        drawn.add((a, b))
        x1, y1 = pos[a]
        x2, y2 = pos[b]
        ax.plot([x1, x2], [y1, y2], 'r-', linewidth=2.5, alpha=0.6, zorder=1)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my, str(v), fontsize=10, ha='center', va='center',
                color='#E94B3C', fontweight='bold',
                bbox=dict(boxstyle='circle,pad=0.2', facecolor='white', edgecolor='#E94B3C'))

    # list duplicates
    dup_text = "Duplicated values: " + ", ".join(str(v) for v in sorted(duplicates.keys()))
    ax.text(0, -3.8, dup_text, fontsize=11, ha='center', va='center',
            color='#2C3E50', fontweight='bold')

    margin = CLUSTER_SPACING + 1.2
    ax.set_xlim(-margin, margin)
    ax.set_ylim(-margin - 0.5, margin + 0.5)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {save_path}")


# --------------------------------------------------
# 5. Direction graph (spatial adjacency)
# --------------------------------------------------

def draw_direction_graph(save_path="figures/direction_graph.png"):
    fig, ax = plt.subplots(figsize=(9, 9))
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor('#FDFBF7')
    fig.patch.set_facecolor('#FDFBF7')
    ax.set_title("Cross-shaped direction graph of 5 clusters",
                 fontsize=14, fontweight='bold', color='#2C3E50', pad=10)

    pos = {c["id"]: c["pos"] for c in CLUSTERS}
    edges = [("C1","C3"), ("C2","C3"), ("C3","C4"), ("C3","C5")]

    for a, b in edges:
        x1, y1 = pos[a]
        x2, y2 = pos[b]
        ax.plot([x1, x2], [y1, y2], 'k-', linewidth=2, alpha=0.4, zorder=1)

    for cluster in CLUSTERS:
        cx, cy = cluster["pos"]
        color = GROUP_COLORS[residue(cluster["center"])]
        circ = plt.Circle((cx, cy), 0.4, color='white', ec=color, linewidth=3, zorder=2)
        ax.add_patch(circ)
        ax.text(cx, cy, f"{cluster['id']}\n({cluster['center']})",
                fontsize=11, ha='center', va='center', fontweight='bold', color='#2C3E50', zorder=3)

    ax.text(0, -3.8, "5-direction cross: top-left-center-right-bottom",
            fontsize=11, ha='center', va='center', color='#2C3E50', fontweight='bold')

    margin = CLUSTER_SPACING + 1.2
    ax.set_xlim(-margin, margin)
    ax.set_ylim(-margin - 0.5, margin + 0.5)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {save_path}")


# --------------------------------------------------
# Run
# --------------------------------------------------

if __name__ == "__main__":
    draw_base_layout("figures/base_layout.png")
    draw_residue_distribution()
    draw_cluster_structure()
    draw_duplication_graph()
    draw_direction_graph()
    print("All visualizations generated.")
