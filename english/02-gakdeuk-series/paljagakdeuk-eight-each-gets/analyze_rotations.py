#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Per-cluster rotation analysis for Paljagakdeuk (Eight-Each-Gets).

Each palace is a 3×3 grid with the center cell blank; the 8 numbered cells form
an 8-cycle around the blank center.  We read each palace clockwise from the
top edge and report opposite-pair sums, mod-5 residue patterns, cluster
invariants, and global rotational symmetries of the cross layout.
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
    "Upper Palace": [
        [39, 7, 34],
        [12, None, 19],
        [24, 2, 27],
    ],
    "Left Palace": [
        [33, 18, 28],
        [8, None, 3],
        [38, 13, 23],
    ],
    "Center Palace": [
        [30, 5, 21],
        [16, None, 15],
        [31, 10, 36],
    ],
    "Right Palace": [
        [22, 14, 37],
        [4, None, 9],
        [29, 17, 32],
    ],
    "Lower Palace": [
        [26, 1, 25],
        [20, None, 11],
        [35, 6, 40],
    ],
}

PALACE_ORIGINS = {
    "Upper Palace": (3, 6),
    "Left Palace": (0, 3),
    "Center Palace": (3, 3),
    "Right Palace": (6, 3),
    "Lower Palace": (3, 0),
}

# Clockwise from top-mid: top-mid, top-right, mid-right, bottom-right,
# bottom-mid, bottom-left, mid-left, top-left.
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
        analysis = analyze_cycle(cycle, modulo=5, name=name)
        analyses.append(analysis)

    centers = {
        name: (origin[0] + 1.0, origin[1] + 1.0)
        for name, origin in PALACE_ORIGINS.items()
    }
    global_syms = find_global_rotation_symmetries(centers, candidates=[90, 180, 270])

    draw_individual_clusters(analyses, str(OUTPUT_DIR / "rotation_cluster"))
    draw_overview(
        analyses,
        global_title="Paljagakdeuk — 5 palace rotations (8-cycles)",
        save_path=str(OUTPUT_DIR / "rotation_overview.png"),
        ncols=3,
        modulo=5,
    )

    write_report(
        puzzle_name="Paljagakdeuk (Eight-Each-Gets)",
        analyses=analyses,
        global_symmetries=global_syms,
        save_path=str(OUTPUT_DIR / "rotation_report.txt"),
    )


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
