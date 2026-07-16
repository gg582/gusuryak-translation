#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Per-cluster rotation analysis for Gujagakdeuk (Nine-Each-Gets).

Each palace is a full 3×3 grid.  The eight outer cells (corners + edge
midpoints) form an 8-cycle around the central cell, read clockwise from the
top edge.  The central cell is recorded as a note.  We report opposite-pair
sums, mod-5 residue patterns, cluster invariants, and global rotational
symmetries of the cross layout.
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
    "Top": [
        [12, 44, 9],
        [19, 21, 29],
        [37, 2, 34],
    ],
    "Left": [
        [13, 43, 8],
        [18, 25, 26],
        [38, 3, 33],
    ],
    "Center": [
        [15, 41, 6],
        [16, 23, 30],
        [40, 5, 31],
    ],
    "Right": [
        [14, 42, 7],
        [17, 24, 28],
        [39, 4, 32],
    ],
    "Bottom": [
        [11, 45, 10],
        [20, 22, 27],
        [36, 1, 35],
    ],
}

PALACE_ORIGINS = {
    "Top": (3, 6),
    "Left": (0, 3),
    "Center": (3, 3),
    "Right": (6, 3),
    "Bottom": (3, 0),
}

# Clockwise 8-cycle around the center cell (1,1).
CLOCKWISE_CELLS = [
    (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0), (0, 0)
]

OUTPUT_DIR = Path(".")


def main() -> None:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False

    analyses = []
    for name, grid in PALACES.items():
        cycle = [grid[r][c] for r, c in CLOCKWISE_CELLS]
        center = grid[1][1]
        analysis = analyze_cycle(cycle, modulo=5, name=name)
        analysis.notes.append(f"center cell = {center}")
        analyses.append(analysis)

    centers = {
        name: (origin[0] + 1.0, origin[1] + 1.0)
        for name, origin in PALACE_ORIGINS.items()
    }
    global_syms = find_global_rotation_symmetries(centers, candidates=[90, 180, 270])

    draw_individual_clusters(analyses, str(OUTPUT_DIR / "rotation_cluster"))
    draw_overview(
        analyses,
        global_title="Gujagakdeuk — 5 palace rotations (outer 8-cycles)",
        save_path=str(OUTPUT_DIR / "rotation_overview.png"),
        ncols=3,
        modulo=5,
    )

    write_report(
        puzzle_name="Gujagakdeuk (Nine-Each-Gets)",
        analyses=analyses,
        global_symmetries=global_syms,
        save_path=str(OUTPUT_DIR / "rotation_report.txt"),
    )


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
