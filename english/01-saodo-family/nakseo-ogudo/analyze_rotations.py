#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Per-cluster rotation analysis for Nakseo-ogudo (洛書五九圖).

Each of the nine palaces is a plus shape: a center cell plus four orthogonal
neighbors.  We read the four neighbors as a 4-cycle clockwise from the top
(N -> E -> S -> W) and report opposite-pair sums, mod-5 residue patterns, and
cluster invariants.  We also report the 90° rotation mapping of the 3×3
palace-center grid.
"""

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

PALACES = {
    "upper_left": ((1, 2), (0, 2), (2, 2), (1, 3), (1, 1.5)),
    "upper_center": ((3, 2), (2, 2), (4, 2), (3, 3), (3, 1.5)),
    "upper_right": ((5, 2), (4, 2), (6, 2), (5, 3), (5, 1.5)),
    "middle_left": ((1, 1), (0, 1), (2, 1), (1, 1.5), (1, 0.5)),
    "center": ((3, 1), (2, 1), (4, 1), (3, 1.5), (3, 0.5)),
    "middle_right": ((5, 1), (4, 1), (6, 1), (5, 1.5), (5, 0.5)),
    "lower_left": ((1, 0), (0, 0), (2, 0), (1, 0.5), (1, -1)),
    "lower_center": ((3, 0), (2, 0), (4, 0), (3, 0.5), (3, -1)),
    "lower_right": ((5, 0), (4, 0), (6, 0), (5, 0.5), (5, -1)),
}

VALUES = {
    (1, 3): 23,
    (3, 3): 28,
    (5, 3): 21,
    (0, 2): 20,
    (1, 2): 4,
    (2, 2): 16,
    (3, 2): 9,
    (4, 2): 14,
    (5, 2): 2,
    (6, 2): 33,
    (1, 1.5): 22,
    (3, 1.5): 18,
    (5, 1.5): 15,
    (0, 1): 31,
    (1, 1): 3,
    (2, 1): 19,
    (3, 1): 5,
    (4, 1): 26,
    (5, 1): 7,
    (6, 1): 25,
    (1, 0.5): 10,
    (3, 0.5): 17,
    (5, 0.5): 12,
    (0, 0): 29,
    (1, 0): 8,
    (2, 0): 11,
    (3, 0): 1,
    (4, 0): 24,
    (5, 0): 6,
    (6, 0): 30,
    (1, -1): 27,
    (3, -1): 32,
    (5, -1): 13,
}

# Order in PALACES tuple: center, west, east, north, south.
# We want clockwise 4-cycle of neighbors: north -> east -> south -> west.
NEIGHBOR_ORDER = [3, 2, 4, 1]

OUTPUT_DIR = Path(".")


def main() -> None:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False

    analyses = []
    palace_centers = {}
    for name, coords in PALACES.items():
        center_coord = coords[0]
        cycle = [VALUES[coords[i]] for i in NEIGHBOR_ORDER]
        analysis = analyze_cycle(cycle, modulo=5, name=name)
        analysis.notes.append(f"center value = {VALUES[center_coord]}")
        analyses.append(analysis)
        palace_centers[name] = center_coord

    global_syms = find_global_rotation_symmetries(palace_centers, candidates=[90, 180, 270])

    draw_individual_clusters(analyses, str(OUTPUT_DIR / "rotation_cluster"))
    draw_overview(
        analyses,
        global_title="Nakseo-ogudo — 9 palace neighbor rotations (N→E→S→W)",
        save_path=str(OUTPUT_DIR / "rotation_overview.png"),
        ncols=3,
        modulo=5,
    )

    write_report(
        puzzle_name="Nakseo-ogudo (洛書五九圖)",
        analyses=analyses,
        global_symmetries=global_syms,
        save_path=str(OUTPUT_DIR / "rotation_report.txt"),
    )


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
