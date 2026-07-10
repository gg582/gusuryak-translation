#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visualizations for the Sa-o-do (A puzzle of Four and Five) 5-coloring puzzle.

Faithful to the source:
- symmetric cross-shaped layout
- circular marks
- rotated Arabic numeral labels
- five mod-5 group colors
- checksum 共積210
- implicit direction-mark hint
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# --------------------------------------------------
# 1. Data definition
# --------------------------------------------------

# Coordinates (x, y) and labels
# top arm 2x2
# central body 2x6
# bottom arm 2x2
nodes = [
    # Top arm (y=3,2 ; x=-1,0) — adjacent to the central body to form a cross
    {"pos": (-1, 3), "label": 19},
    {"pos": (0, 3),  "label": 2},
    {"pos": (-1, 2), "label": 7},
    {"pos": (0, 2),  "label": 14},

    # Central body (y=1,0 ; x=-3,-2,-1,0,1,2)
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

    # Bottom arm (y=-1,-2 ; x=-1,0)
    {"pos": (-1, -1), "label": 15},
    {"pos": (0, -1),  "label": 1},
    {"pos": (-1, -2), "label": 6},
    {"pos": (0, -2),  "label": 20},
]

# mod-5 group colors (1-based)
GROUP_COLORS = {
    1: "#4A90E2",  # Water - blue
    2: "#E94B3C",  # Fire - red
    3: "#6AB04C",  # Wood - green
    4: "#BDC3C7",  # Metal - silver-gray
    5: "#D4A017",  # Earth - ochre
}

GROUP_NAMES = {
    1: "Water",
    2: "Fire",
    3: "Wood",
    4: "Metal",
    5: "Earth",
}

# Numeral rotation angle (approximately -30° as observed in the source)
THETA_DEG = -30


# --------------------------------------------------
# 2. Group assignment
# --------------------------------------------------

def group_of(label):
    """1-based mod 5"""
    g = label % 5
    return 5 if g == 0 else g


# --------------------------------------------------
# 3. Base puzzle visualization
# --------------------------------------------------

def draw_base_puzzle(save_path="figures/puzzle_base.png"):
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.set_aspect('equal')
    ax.axis('off')

    # Background
    ax.set_facecolor('#FDFBF7')
    fig.patch.set_facecolor('#FDFBF7')

    # Title
    ax.text(0, 5.6, "Sa-o-do (A puzzle of Four and Five)", fontsize=22, ha='center', va='center',
            fontweight='bold', color='#2C3E50')
    ax.text(0, 5.25, "Symmetric Cross-Shaped Point Configuration", fontsize=11,
            ha='center', va='center', color='#7F8C8D', style='italic')

    # Circular slots and numerals
    for node in nodes:
        x, y = node["pos"]
        label = node["label"]
        g = group_of(label)
        color = GROUP_COLORS[g]

        # Circular mark
        circle = plt.Circle((x, y), 0.42, color='white', ec=color, linewidth=3, zorder=2)
        ax.add_patch(circle)

        # Rotated numeral label
        ax.text(x, y, str(label), fontsize=18, ha='center', va='center',
                color='#2C3E50', fontweight='bold', zorder=3,
                rotation=THETA_DEG,
                rotation_mode='anchor')

    # Checksum 共積210 text
    total = sum(n["label"] for n in nodes)
    ax.text(0, -3.2, f"Checksum = {total}", fontsize=14, ha='center', va='center',
            color='#2C3E50', fontweight='bold')

    # Legend
    legend_x = -4.5
    legend_y = 4.8
    ax.text(legend_x, legend_y + 0.5, "mod 5 groups", fontsize=12, fontweight='bold', color='#2C3E50')
    for i, g in enumerate([1, 2, 3, 4, 5], start=0):
        yy = legend_y - i * 0.45
        circ = plt.Circle((legend_x, yy), 0.12, color=GROUP_COLORS[g], ec='#2C3E50', linewidth=1)
        ax.add_patch(circ)
        ax.text(legend_x + 0.35, yy, f"{g}: {GROUP_NAMES[g]}", fontsize=10, va='center', color='#2C3E50')

    ax.set_xlim(-5.5, 5.5)
    ax.set_ylim(-4, 6.5)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {save_path}")


# --------------------------------------------------
# 4. Opposition / complement relation visualization
# --------------------------------------------------

def draw_relations(save_path="figures/puzzle_relations.png"):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor('#FDFBF7')
    fig.patch.set_facecolor('#FDFBF7')

    # Place the five groups at regular pentagon vertices
    angles = np.linspace(90, 90 - 360, 6)[:-1] * np.pi / 180
    radius = 2.5
    positions = {}
    for i, g in enumerate([1, 2, 3, 4, 5]):
        x = radius * np.cos(angles[i])
        y = radius * np.sin(angles[i])
        positions[g] = (x, y)
        color = GROUP_COLORS[g]
        circle = plt.Circle((x, y), 0.55, color='white', ec=color, linewidth=4, zorder=2)
        ax.add_patch(circle)
        ax.text(x, y, GROUP_NAMES[g], fontsize=14, ha='center', va='center',
                fontweight='bold', color='#2C3E50', zorder=3)

    # Opposition: Water(1) ↔ Earth(5) - red solid line
    ax.plot([positions[1][0], positions[5][0]],
            [positions[1][1], positions[5][1]],
            'r-', linewidth=3, alpha=0.7, label='Opposition σ')

    # Complement: Fire(2) ↔ Metal(4) - blue dashed line
    ax.plot([positions[2][0], positions[4][0]],
            [positions[2][1], positions[4][1]],
            'b--', linewidth=3, alpha=0.7, label='Complement τ')

    # Wood(3) is a fixed point
    ax.text(positions[3][0], positions[3][1] - 0.9, "Fixed point", fontsize=10,
            ha='center', va='center', color='#6AB04C')

    ax.text(0, 3.5, "Five-Phase Relation Diagram", fontsize=18, ha='center', va='center',
            fontweight='bold', color='#2C3E50')
    ax.text(0, -3.5, "σ = (1 5) : Water ↔ Earth    τ = (2 4) : Fire ↔ Metal", fontsize=12,
            ha='center', va='center', color='#2C3E50')

    ax.set_xlim(-4, 4)
    ax.set_ylim(-4.5, 4.5)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {save_path}")


# --------------------------------------------------
# 5. 5×5 / 6×5 block-design hypothesis visualization
# --------------------------------------------------

def draw_block_design(save_path="figures/puzzle_block_design.png"):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor('#FDFBF7')

    V = list(range(1, 21))

    # 5x5 hypothesis: 5 blocks of 4 elements (the five-phase groups themselves)
    B_H = [
        [1, 6, 11, 16],
        [2, 7, 12, 17],
        [3, 8, 13, 18],
        [4, 9, 14, 19],
        [5, 10, 15, 20],
    ]

    # 6x5 hypothesis reinterpreted from the original text:
    # 河圖五五卽上天數圖，六五卽上地數圖
    # H = {1,3,5,7,9}, sum = 25 = 5*5  (Heaven numbers)
    # E = {2,4,6,8,10}, sum = 30 = 5*6 (Earth numbers)
    # Extended to 1..20 by adding +10 to each base number.
    B_E = [
        [1, 11],
        [3, 13],
        [5, 15],
        [7, 17],
        [9, 19],
    ]

    titles = ["B_H: Five-Phase blocks (5 blocks, 4 each)",
              "B_E: Heaven-number blocks (5 blocks, sum 25 in base cycle)"]
    block_families = [B_H, B_E]

    for ax, title, blocks in zip(axes, titles, block_families):
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_facecolor('#FDFBF7')
        ax.set_title(title, fontsize=13, fontweight='bold', color='#2C3E50', pad=10)

        # Polygon arrangement
        n_blocks = len(blocks)
        angles = np.linspace(90, 90 - 360, n_blocks + 1)[:-1] * np.pi / 180
        radius = 2.2
        block_positions = [(radius * np.cos(a), radius * np.sin(a)) for a in angles]

        for idx, block in enumerate(blocks):
            bx, by = block_positions[idx]
            # Block circle
            circ = plt.Circle((bx, by), 0.7, color='white', ec='#7F8C8D', linewidth=2, zorder=1)
            ax.add_patch(circ)
            ax.text(bx, by + 0.05, f"B{idx+1}", fontsize=9, ha='center', va='center',
                    fontweight='bold', color='#2C3E50')
            ax.text(bx, by - 0.25, str(block), fontsize=7, ha='center', va='center',
                    color='#7F8C8D')

        ax.set_xlim(-3.5, 3.5)
        ax.set_ylim(-3.5, 3.5)

    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {save_path}")


# --------------------------------------------------
# 6. Heaven/Earth numbers visualization
# --------------------------------------------------

def draw_heaven_earth(save_path="figures/puzzle_heaven_earth.png"):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor('#FDFBF7')

    # Left panel: base cycle 1..10
    ax = axes[0]
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor('#FDFBF7')
    ax.set_title("Heaven/Earth numbers in 1..10\n(5+5 = 55, the Great Expansion number)",
                 fontsize=13, fontweight='bold', color='#2C3E50', pad=10)

    heaven = {1, 3, 5, 7, 9}
    earth = {2, 4, 6, 8, 10}
    radius = 2.5
    angles = np.linspace(90, 90 - 360, 11)[:-1] * np.pi / 180
    for i, n in enumerate(range(1, 11)):
        x = radius * np.cos(angles[i])
        y = radius * np.sin(angles[i])
        color = '#4A90E2' if n in heaven else '#D4A017'
        circ = plt.Circle((x, y), 0.38, color='white', ec=color, linewidth=3, zorder=2)
        ax.add_patch(circ)
        ax.text(x, y, str(n), fontsize=14, ha='center', va='center',
                fontweight='bold', color='#2C3E50', zorder=3)

    ax.text(0, 0, "ΣH=25=5²\nΣE=30=5·6", fontsize=12, ha='center', va='center',
            color='#2C3E50', fontweight='bold')

    # Legend
    ax.add_patch(plt.Circle((-3.2, 2.8), 0.15, color='white', ec='#4A90E2', linewidth=2))
    ax.text(-2.85, 2.8, "Heaven H", fontsize=10, va='center', color='#2C3E50')
    ax.add_patch(plt.Circle((-3.2, 2.35), 0.15, color='white', ec='#D4A017', linewidth=2))
    ax.text(-2.85, 2.35, "Earth E", fontsize=10, va='center', color='#2C3E50')

    ax.set_xlim(-4, 4)
    ax.set_ylim(-3.5, 3.5)

    # Right panel: extended 1..20 with two cycles
    ax = axes[1]
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor('#FDFBF7')
    ax.set_title("Extended to 1..20 (2-cycle repetition)\nΣH'=100, ΣE'=110",
                 fontsize=13, fontweight='bold', color='#2C3E50', pad=10)

    # Inner ring: 1..10, outer ring: 11..20
    inner_r, outer_r = 1.8, 3.2
    for cycle, r in [(range(1, 11), inner_r), (range(11, 21), outer_r)]:
        angles = np.linspace(90, 90 - 360, 11)[:-1] * np.pi / 180
        for i, n in enumerate(cycle):
            x = r * np.cos(angles[i])
            y = r * np.sin(angles[i])
            color = '#4A90E2' if n % 2 == 1 else '#D4A017'
            circ = plt.Circle((x, y), 0.32, color='white', ec=color, linewidth=2, zorder=2)
            ax.add_patch(circ)
            ax.text(x, y, str(n), fontsize=10, ha='center', va='center',
                    fontweight='bold', color='#2C3E50', zorder=3)

    # Radial lines connecting cycles for heaven/earth pairs
    for i, n in enumerate(range(1, 11)):
        angle = np.linspace(90, 90 - 360, 11)[:-1][i] * np.pi / 180
        color = '#4A90E2' if n % 2 == 1 else '#D4A017'
        ax.plot([inner_r * np.cos(angle), outer_r * np.cos(angle)],
                [inner_r * np.sin(angle), outer_r * np.sin(angle)],
                color=color, linewidth=1.5, alpha=0.5, zorder=1)

    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)

    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {save_path}")


# --------------------------------------------------
# 7. Run
# --------------------------------------------------

if __name__ == "__main__":
    draw_base_puzzle()
    draw_relations()
    draw_block_design()
    draw_heaven_earth()
    print("All visualizations generated.")
