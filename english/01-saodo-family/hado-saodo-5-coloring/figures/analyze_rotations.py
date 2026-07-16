#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rotation analysis for the Hado / Saodo 5-coloring puzzle.

The 20 numbered nodes are colored by mod-5 residue (five wuxing groups).
Each residue class is treated as a cyclic cluster by arranging its members
clockwise from the top around the center of the cross.  We also record the
uniform -30° numeral orientation noted in the existing symmetry analysis.
"""

import math
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt

def _find_project_root() -> Path:
    p = Path(__file__).resolve()
    while p.parent != p:
        if (p / "rotation_analysis.py").exists():
            return p
        p = p.parent
    raise RuntimeError("Could not find project root containing rotation_analysis.py")


ROOT = _find_project_root()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from rotation_analysis import (
    analyze_cycle,
    draw_individual_clusters,
    draw_overview,
    find_global_rotation_symmetries,
    write_report,
)

NODES = [
    {"pos": (-1, 3), "label": 19},
    {"pos": (0, 3),  "label": 2},
    {"pos": (-1, 2), "label": 7},
    {"pos": (0, 2),  "label": 14},
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
    {"pos": (-1, -1), "label": 15},
    {"pos": (0, -1),  "label": 1},
    {"pos": (-1, -2), "label": 6},
    {"pos": (0, -2),  "label": 20},
]

GROUP_NAMES = {
    1: "Water",
    2: "Fire",
    3: "Wood",
    4: "Metal",
    5: "Earth",
}

OUTPUT_DIR = Path(".")


def group_of(n: int) -> int:
    g = n % 5
    return 5 if g == 0 else g


def main() -> None:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False

    # Group by mod-5 residue
    groups: dict[int, list[tuple[int, tuple[int, int]]]] = {r: [] for r in range(1, 6)}
    for node in NODES:
        groups[group_of(node["label"])].append((node["label"], node["pos"]))

    # Arrange each group clockwise from top around the origin.
    analyses = []
    for r in range(1, 6):
        members = groups[r]

        def angle(item):
            _, (x, y) = item
            return math.degrees(math.atan2(y, x))

        # clockwise from top means decreasing angle from 90°
        sorted_members = sorted(members, key=angle, reverse=True)
        start_idx = min(range(len(sorted_members)),
                        key=lambda i: abs(angle(sorted_members[i]) - 90.0))
        ordered = [sorted_members[(start_idx + i) % len(sorted_members)][0]
                   for i in range(len(sorted_members))]

        analysis = analyze_cycle(ordered, modulo=5, name=GROUP_NAMES[r])
        analysis.notes.append(f"{len(ordered)} nodes arranged by angle around cross center")
        analyses.append(analysis)

    # Global rotational symmetry of node positions
    centers = {node["label"]: node["pos"] for node in NODES}
    global_syms = find_global_rotation_symmetries(centers, candidates=[90, 180, 270])

    draw_individual_clusters(analyses, str(OUTPUT_DIR / "rotation_cluster"))
    draw_overview(
        analyses,
        global_title="Hado/Saodo 5-coloring — five wuxing group rotations",
        save_path=str(OUTPUT_DIR / "rotation_overview.png"),
        ncols=3,
        modulo=5,
    )

    # Append orientation note to report manually
    write_report(
        puzzle_name="Hado / Saodo 5-coloring",
        analyses=analyses,
        global_symmetries=global_syms,
        save_path=str(OUTPUT_DIR / "rotation_report.txt"),
    )

    # Append the -30° orientation note to the saved report
    with open(OUTPUT_DIR / "rotation_report.txt", "a", encoding="utf-8") as f:
        f.write("\nNumeral orientation note:\n")
        f.write("  All numerals share approximately θ = -30° (clockwise from horizontal).\n")
        f.write("  This uniform skew is preserved under any rotation of the whole diagram,\n")
        f.write("  but the label placement itself has no nontrivial rotational symmetry.\n")


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
