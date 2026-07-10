#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract and visualize modern combinatorial problems from the Sa-o-do (A puzzle of Four and Five) 5-coloring puzzle.
Each figure corresponds to one problem in figures/math_problems.md.
"""

import matplotlib.pyplot as plt
import numpy as np

# --------------------------------------------------
# Shared data
# --------------------------------------------------

labels = [
    [19, 2],
    [7, 14],
    [13, 8, 5, 16, 4, 17],
    [18, 3, 11, 10, 12, 9],
    [15, 1],
    [6, 20],
]

GROUP_COLORS = {
    1: "#4A90E2",  # Water
    2: "#E94B3C",  # Fire
    3: "#6AB04C",  # Wood
    4: "#BDC3C7",  # Metal
    5: "#D4A017",  # Earth
}


def group_of(n):
    g = n % 5
    return 5 if g == 0 else g


def setup_axis(ax, title):
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor('#FDFBF7')
    ax.set_title(title, fontsize=13, fontweight='bold', color='#2C3E50', pad=10)


# --------------------------------------------------
# Problem 1: 5-coloring consistency
# --------------------------------------------------

def draw_coloring_problem(save_path="figures/problem_01_coloring.png"):
    fig, ax = plt.subplots(figsize=(10, 10))
    setup_axis(ax, "Problem 1: Proper 5-coloring on symmetric cross")

    positions = []
    for row_idx, row in enumerate(labels):
        y = 5 - row_idx * 1.2
        n = len(row)
        start_x = -(n - 1) * 0.6 / 2
        for col_idx, label in enumerate(row):
            x = start_x + col_idx * 0.6
            positions.append((x, y, label))

    for x, y, label in positions:
        g = group_of(label)
        color = GROUP_COLORS[g]
        circ = plt.Circle((x, y), 0.22, color='white', ec=color, linewidth=2.5, zorder=2)
        ax.add_patch(circ)
        ax.text(x, y, str(label), fontsize=9, ha='center', va='center',
                fontweight='bold', color='#2C3E50', zorder=3)

    # Color-class counts
    counts = {g: 0 for g in range(1, 6)}
    for _, _, label in positions:
        counts[group_of(label)] += 1

    ax.text(0, -2.0, "Color class sizes: " + str(counts), fontsize=11,
            ha='center', va='center', color='#2C3E50', fontweight='bold')

    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-3, 7)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {save_path}")


# --------------------------------------------------
# Problem 2: Heaven/Earth partition
# --------------------------------------------------

def draw_heaven_earth_problem(save_path="figures/problem_02_heaven_earth.png"):
    fig, ax = plt.subplots(figsize=(10, 6))
    setup_axis(ax, "Problem 2: Heaven/Earth partition of 1..20")

    heaven = [n for n in range(1, 21) if n % 2 == 1]
    earth = [n for n in range(1, 21) if n % 2 == 0]

    # Heaven row
    for i, n in enumerate(heaven):
        x = i * 0.7 - 3.15
        circ = plt.Circle((x, 1), 0.25, color='white', ec='#4A90E2', linewidth=2)
        ax.add_patch(circ)
        ax.text(x, 1, str(n), fontsize=9, ha='center', va='center', fontweight='bold')

    # Earth row
    for i, n in enumerate(earth):
        x = i * 0.7 - 3.15
        circ = plt.Circle((x, -1), 0.25, color='white', ec='#D4A017', linewidth=2)
        ax.add_patch(circ)
        ax.text(x, -1, str(n), fontsize=9, ha='center', va='center', fontweight='bold')

    ax.text(-4.2, 1, "H'", fontsize=14, ha='center', va='center',
            fontweight='bold', color='#4A90E2')
    ax.text(-4.2, -1, "E'", fontsize=14, ha='center', va='center',
            fontweight='bold', color='#D4A017')

    ax.text(0, -2.5, f"ΣH' = {sum(heaven)} = 100,  ΣE' = {sum(earth)} = 110",
            fontsize=12, ha='center', va='center', color='#2C3E50', fontweight='bold')

    ax.set_xlim(-5, 5)
    ax.set_ylim(-3.5, 2.5)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {save_path}")


# --------------------------------------------------
# Problem 3: Involution structure
# --------------------------------------------------

def draw_involution_problem(save_path="figures/problem_03_involution.png"):
    fig, ax = plt.subplots(figsize=(8, 8))
    setup_axis(ax, "Problem 3: Involutions σ and τ on five phases")

    names = ["Water", "Fire", "Wood", "Metal", "Earth"]
    angles = np.linspace(90, 90 - 360, 6)[:-1] * np.pi / 180
    radius = 2.2
    pos = {}
    for i, name in enumerate(names):
        x = radius * np.cos(angles[i])
        y = radius * np.sin(angles[i])
        pos[name] = (x, y)
        color = GROUP_COLORS[i + 1]
        circ = plt.Circle((x, y), 0.5, color='white', ec=color, linewidth=3, zorder=2)
        ax.add_patch(circ)
        ax.text(x, y, name, fontsize=10, ha='center', va='center',
                fontweight='bold', color='#2C3E50', zorder=3)

    # σ: Water ↔ Earth
    ax.annotate('', xy=pos["Earth"], xytext=pos["Water"],
                arrowprops=dict(arrowstyle='<->', color='#E94B3C', lw=2.5))
    # τ: Fire ↔ Metal
    ax.annotate('', xy=pos["Metal"], xytext=pos["Fire"],
                arrowprops=dict(arrowstyle='<->', color='#4A90E2', lw=2.5, ls='--'))

    ax.text(0, 0, "σ² = τ² = Id\nWood is fixed", fontsize=11,
            ha='center', va='center', color='#2C3E50', fontweight='bold')
    ax.text(0, -3.2, "σ = (Water Earth),  τ = (Fire Metal)", fontsize=11,
            ha='center', va='center', color='#2C3E50')

    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-4, 3.5)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {save_path}")


# --------------------------------------------------
# Problem 4: Block design intersection matrix
# --------------------------------------------------

def draw_block_intersection(save_path="figures/problem_04_intersection.png"):
    B_H = [
        {1, 6, 11, 16},
        {2, 7, 12, 17},
        {3, 8, 13, 18},
        {4, 9, 14, 19},
        {5, 10, 15, 20},
    ]
    B_E = [
        {1, 11},
        {3, 13},
        {5, 15},
        {7, 17},
        {9, 19},
    ]

    M = np.array([[len(h & e) for e in B_E] for h in B_H])

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.set_facecolor('#FDFBF7')
    fig.patch.set_facecolor('#FDFBF7')
    ax.set_title("Problem 4: Intersection matrix M[i,j] = |B_H[i] ∩ B_E[j]|",
                 fontsize=12, fontweight='bold', color='#2C3E50', pad=10)

    im = ax.imshow(M, cmap='Blues', aspect='auto')
    for i in range(5):
        for j in range(5):
            ax.text(j, i, str(M[i, j]), ha='center', va='center',
                    color='white' if M[i, j] > 0 else '#2C3E50', fontsize=14, fontweight='bold')

    ax.set_xticks(range(5))
    ax.set_yticks(range(5))
    ax.set_xticklabels([f"E{j+1}" for j in range(5)])
    ax.set_yticklabels([f"H{i+1}" for i in range(5)])
    ax.set_xlabel("Earth blocks B_E", fontsize=11)
    ax.set_ylabel("Five-phase blocks B_H", fontsize=11)

    plt.colorbar(im, ax=ax, label='Intersection size')
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {save_path}")


# --------------------------------------------------
# Problem 5: Term rewriting rules
# --------------------------------------------------

def draw_rewriting_problem(save_path="figures/problem_05_rewriting.png"):
    fig, ax = plt.subplots(figsize=(10, 5))
    setup_axis(ax, "Problem 5: Term rewriting rules")

    # Wood + Wood -> Fire
    y1 = 1.5
    for i, name in enumerate(["Wood", "Wood"]):
        x = -2 + i * 1.0
        color = GROUP_COLORS[3]
        circ = plt.Circle((x, y1), 0.35, color='white', ec=color, linewidth=2)
        ax.add_patch(circ)
        ax.text(x, y1, name, fontsize=9, ha='center', va='center', fontweight='bold')

    ax.annotate('', xy=(1.2, y1), xytext=(-0.6, y1),
                arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=2))
    color = GROUP_COLORS[2]
    circ = plt.Circle((2.0, y1), 0.35, color='white', ec=color, linewidth=2)
    ax.add_patch(circ)
    ax.text(2.0, y1, "Fire", fontsize=9, ha='center', va='center', fontweight='bold')

    # Metal + Fire -> empty
    y2 = -0.5
    for i, name in enumerate(["Metal", "Fire"]):
        x = -2 + i * 1.0
        color = GROUP_COLORS[4 if name == "Metal" else 2]
        circ = plt.Circle((x, y2), 0.35, color='white', ec=color, linewidth=2)
        ax.add_patch(circ)
        ax.text(x, y2, name, fontsize=9, ha='center', va='center', fontweight='bold')

    ax.annotate('', xy=(1.2, y2), xytext=(-0.6, y2),
                arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=2))
    ax.text(2.0, y2, "∅", fontsize=16, ha='center', va='center', fontweight='bold', color='#2C3E50')

    ax.set_xlim(-3, 3.5)
    ax.set_ylim(-2, 3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {save_path}")


# --------------------------------------------------
# Problem 6: Checksum invariant
# --------------------------------------------------

def draw_checksum_problem(save_path="figures/problem_06_checksum.png"):
    fig, ax = plt.subplots(figsize=(8, 5))
    setup_axis(ax, "Problem 6: Checksum invariant Σ = 210")

    total = sum(range(1, 21))
    ax.text(0, 1, "1 + 2 + … + 20", fontsize=16, ha='center', va='center',
            fontweight='bold', color='#2C3E50')
    ax.text(0, 0, f"= {total}", fontsize=22, ha='center', va='center',
            fontweight='bold', color='#E94B3C')
    ax.text(0, -1, "Question: what invariant survives under rewriting?",
            fontsize=11, ha='center', va='center', color='#7F8C8D', style='italic')

    ax.set_xlim(-3, 3)
    ax.set_ylim(-2, 2.5)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {save_path}")


# --------------------------------------------------
# Run all
# --------------------------------------------------

if __name__ == "__main__":
    draw_coloring_problem()
    draw_heaven_earth_problem()
    draw_involution_problem()
    draw_block_intersection()
    draw_rewriting_problem()
    draw_checksum_problem()
    print("All problem visualizations generated.")
