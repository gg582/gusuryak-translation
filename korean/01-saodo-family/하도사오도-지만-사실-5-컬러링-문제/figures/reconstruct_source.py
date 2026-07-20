#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conservative reconstruction script for the Sa-o-do (A puzzle of Four and Five) 5-coloring puzzle.

This script visualizes the source data as faithfully as possible,
following the Reconstruction Policy in the Problem Constraints.

Preserved:
    - slot positions (fixed symmetric cross-shaped layout)
    - circular marks
    - numeral values
    - numeral orientations
    - symmetric cross-shaped layout
    - residue-group partition (five mod-5 groups of four)
    - checksum note (共積210)

Not introduced:
    - artificial graph edges
    - nearest-neighbor assumptions
    - rewrite systems
    - finite-state machines
    - traversal rules
    - algebraic semantics

Usage:
    python3 figures/reconstruct_source.py
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np


def _find_cjk_font():
    """Auto-detect a system font that supports CJK (Korean/Chinese) characters."""
    candidates = [
        "Noto Sans CJK KR",
        "Noto Sans CJK SC",
        "Noto Sans CJK TC",
        "NanumGothic",
        "NanumSquare",
        "NanumBarunGothic",
        "Baekmuk Batang",
        "UnDotum",
        "Malgun Gothic",
        "AppleGothic",
    ]
    available = {f.name for f in fm.fontManager.ttflist}
    for name in candidates:
        if name in available:
            return name
    return None


_CJK_FONT = _find_cjk_font()
if _CJK_FONT:
    plt.rcParams['font.family'] = [_CJK_FONT, 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False

# --------------------------------------------------
# 1. Source data
# --------------------------------------------------

# Slot coordinates, labels, and slant angles (theta, in degrees).
# Geometry: top arm 2x2, central body 2x6, bottom arm 2x2.
SLOTS = [
    # Top arm (y=3,2 ; x=-1,0) — adjacent to the central body to form a cross
    {"pos": (-1, 3), "label": 19, "theta": -30},
    {"pos": (0, 3),  "label": 2,  "theta": -30},
    {"pos": (-1, 2), "label": 7,  "theta": -30},
    {"pos": (0, 2),  "label": 14, "theta": -30},

    # Central body (y=1,0 ; x=-3,-2,-1,0,1,2)
    {"pos": (-3, 1), "label": 13, "theta": -30},
    {"pos": (-2, 1), "label": 8,  "theta": -30},
    {"pos": (-1, 1), "label": 5,  "theta": -30},
    {"pos": (0, 1),  "label": 16, "theta": -30},
    {"pos": (1, 1),  "label": 4,  "theta": -30},
    {"pos": (2, 1),  "label": 17, "theta": -30},

    {"pos": (-3, 0), "label": 18, "theta": -30},
    {"pos": (-2, 0), "label": 3,  "theta": -30},
    {"pos": (-1, 0), "label": 11, "theta": -30},
    {"pos": (0, 0),  "label": 10, "theta": -30},
    {"pos": (1, 0),  "label": 12, "theta": -30},
    {"pos": (2, 0),  "label": 9,  "theta": -30},

    # Bottom arm (y=-1,-2 ; x=-1,0)
    {"pos": (-1, -1), "label": 15, "theta": -30},
    {"pos": (0, -1),  "label": 1,  "theta": -30},
    {"pos": (-1, -2), "label": 6,  "theta": -30},
    {"pos": (0, -2),  "label": 20, "theta": -30},
]

# Residue-group partition (1-based mod 5).
RESIDUE_GROUPS = {
    1: {"name": "Water",  "labels": [1, 6, 11, 16]},
    2: {"name": "Fire",   "labels": [2, 7, 12, 17]},
    3: {"name": "Wood",   "labels": [3, 8, 13, 18]},
    4: {"name": "Metal",  "labels": [4, 9, 14, 19]},
    5: {"name": "Earth",  "labels": [5, 10, 15, 20]},
}

# Group border colors. Colors are used only to preserve the residue-group
# partition visually; circle fills remain white.
GROUP_COLORS = {
    1: "#4A90E2",  # Water - blue
    2: "#E94B3C",  # Fire - red
    3: "#6AB04C",  # Wood - green
    4: "#BDC3C7",  # Metal - silver-gray
    5: "#D4A017",  # Earth - ochre
}

# Text colors when circles are filled by group color.
GROUP_TEXT_COLORS = {
    1: "white",
    2: "white",
    3: "white",
    4: "#2C3E50",
    5: "#2C3E50",
}


def group_of(label):
    """group(n) = ((n - 1) mod 5) + 1"""
    return ((label - 1) % 5) + 1


def checksum(labels):
    """sum(1..20) = 210"""
    return sum(labels)


# --------------------------------------------------
# 2. Visualization
# --------------------------------------------------

def draw_reconstruction(save_path="figures/puzzle_reconstruction.png"):
    fig, ax = plt.subplots(figsize=(12, 13))
    ax.set_aspect('equal')
    ax.axis('off')

    # Background
    ax.set_facecolor('#FDFBF7')
    fig.patch.set_facecolor('#FDFBF7')

    # Title and subtitle
    ax.text(0, 5.8, "Sa-o-do (A puzzle of Four and Five): Conservative Reconstruction", fontsize=20,
            ha='center', va='center', fontweight='bold', color='#2C3E50')
    ax.text(0, 5.45, "Preserve positions, circles, labels, orientations, layout, groups, checksum",
            fontsize=11, ha='center', va='center', color='#7F8C8D', style='italic')

    # --- Circular slots and numeral labels ---
    for slot in SLOTS:
        x, y = slot["pos"]
        label = slot["label"]
        theta = slot["theta"]
        g = group_of(label)
        color = GROUP_COLORS[g]

        # Circular mark
        circle = plt.Circle((x, y), 0.42, color='white', ec=color, linewidth=3, zorder=2)
        ax.add_patch(circle)

        # Numeral label (preserve orientation)
        ax.text(x, y, str(label), fontsize=18, ha='center', va='center',
                color='#2C3E50', fontweight='bold', zorder=3,
                rotation=theta, rotation_mode='anchor')

    # --- Checksum 共積210 ---
    total = checksum(slot["label"] for slot in SLOTS)
    ax.text(0, -3.3, f"Checksum = {total}", fontsize=15, ha='center', va='center',
            color='#2C3E50', fontweight='bold')
    ax.text(0, -3.75, "sum(1..20) = 210", fontsize=11, ha='center', va='center',
            color='#7F8C8D')

    # --- Layout outline (dashed: single box around the whole symmetric cross) ---
    # The dashed box is only a visual aid; it is not a graph edge or adjacency relation.
    outline = plt.Rectangle((-3.55, -2.55), 7.1, 6.2, fill=False,
                            edgecolor='#BDC3C7', linewidth=1.5, linestyle='--', zorder=1)
    ax.add_patch(outline)

    # --- Group legend ---
    legend_x = -4.8
    legend_y = 4.6
    ax.text(legend_x, legend_y + 0.5, "Residue groups\n(mod 5)", fontsize=11,
            fontweight='bold', color='#2C3E50', va='bottom')
    for i, g in enumerate([1, 2, 3, 4, 5], start=0):
        yy = legend_y - i * 0.55
        circ = plt.Circle((legend_x, yy), 0.14, color='white', ec=GROUP_COLORS[g], linewidth=2.5)
        ax.add_patch(circ)
        info = RESIDUE_GROUPS[g]
        ax.text(legend_x + 0.35, yy,
                f"G{g} ({info['name']}): {info['labels']}",
                fontsize=9, va='center', color='#2C3E50')

    # --- Reconstruction policy note ---
    policy_text = (
        "Reconstruction policy preserved:\n"
        "  • 20 slot positions  • circular marks  • numeral values/orientations\n"
        "  • symmetric cross layout  • mod-5 잉여류 그룹  • checksum = 210\n"
        "Not introduced: graph edges, adjacency, rewrite rules, FSMs, algebraic semantics."
    )
    ax.text(0, -4.5, policy_text, fontsize=9, ha='center', va='top',
            color='#5D6D7E', linespacing=1.4,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#F8F9F9', edgecolor='#D5DBDB'))

    ax.set_xlim(-6, 6)
    ax.set_ylim(-5.2, 6.5)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {save_path}")


def draw_filled_groups(save_path="figures/puzzle_filled_groups.png"):
    """Visualization with each group filled by the same color.

    This image is an additional visual emphasis of the residue-group partition:
    the circular marks are filled by their group color.
    """
    fig, ax = plt.subplots(figsize=(12, 13))
    ax.set_aspect('equal')
    ax.axis('off')

    ax.set_facecolor('#FDFBF7')
    fig.patch.set_facecolor('#FDFBF7')

    ax.text(0, 5.8, "Sa-o-do (A puzzle of Four and Five): 5-Coloring by Residue Group", fontsize=20,
            ha='center', va='center', fontweight='bold', color='#2C3E50')
    ax.text(0, 5.45, "Same group, same fill color",
            fontsize=11, ha='center', va='center', color='#7F8C8D', style='italic')

    for slot in SLOTS:
        x, y = slot["pos"]
        label = slot["label"]
        theta = slot["theta"]
        g = group_of(label)
        color = GROUP_COLORS[g]
        text_color = GROUP_TEXT_COLORS[g]

        # Circle filled with group color
        circle = plt.Circle((x, y), 0.42, color=color, ec='#2C3E50', linewidth=2, zorder=2)
        ax.add_patch(circle)

        # Numeral label
        ax.text(x, y, str(label), fontsize=18, ha='center', va='center',
                color=text_color, fontweight='bold', zorder=3,
                rotation=theta, rotation_mode='anchor')

    total = checksum(slot["label"] for slot in SLOTS)
    ax.text(0, -3.3, f"Checksum = {total}", fontsize=15, ha='center', va='center',
            color='#2C3E50', fontweight='bold')

    # Single dashed bounding box around the whole symmetric cross.
    # The cross spans x in [-3.55, 3.55] and y in [-2.55, 3.65].
    outline = plt.Rectangle((-3.55, -2.55), 7.1, 6.2, fill=False,
                            edgecolor='#BDC3C7', linewidth=1.5, linestyle='--', zorder=1)
    ax.add_patch(outline)

    # Legend
    legend_x = -4.8
    legend_y = 4.6
    ax.text(legend_x, legend_y + 0.5, "Residue groups\n(mod 5)", fontsize=11,
            fontweight='bold', color='#2C3E50', va='bottom')
    for i, g in enumerate([1, 2, 3, 4, 5], start=0):
        yy = legend_y - i * 0.55
        circ = plt.Circle((legend_x, yy), 0.14, color=GROUP_COLORS[g], ec='#2C3E50', linewidth=1.5)
        ax.add_patch(circ)
        info = RESIDUE_GROUPS[g]
        ax.text(legend_x + 0.35, yy,
                f"G{g} ({info['name']}): {info['labels']}",
                fontsize=9, va='center', color='#2C3E50')

    ax.set_xlim(-6, 6)
    ax.set_ylim(-4.2, 6.5)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {save_path}")


if __name__ == "__main__":
    # Data consistency checks
    labels = [slot["label"] for slot in SLOTS]
    assert len(labels) == 20, "Expected 20 slots"
    assert sorted(labels) == list(range(1, 21)), "Labels must be {1,...,20} exactly once"
    assert checksum(labels) == 210, "Checksum must be 210"
    for g, info in RESIDUE_GROUPS.items():
        assert sorted(info["labels"]) == sorted([l for l in labels if group_of(l) == g]), \
            f"Residue group {g} mismatch"
    print("Data consistency checks passed.")

    draw_reconstruction()
    draw_filled_groups("figures/puzzle_filled_groups.png")
    # Also update the copy used by the first blog post.
    draw_filled_groups("../../first-post/assets/puzzle_filled_groups.png")
