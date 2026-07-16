#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Per-cluster rotation analysis for Jisu-yong-yukdo (Six-Each-Gets).

The 5 hexagons are treated as 6-cycles.  Each cycle is canonicalized so it
starts at the top (12 o'clock) vertex and proceeds clockwise.  We report
opposite-pair sums, mod-5 residue patterns, cluster invariants, and global
rotational symmetries of the honeycomb layout.
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
    canonicalize_by_angle,
    draw_individual_clusters,
    draw_overview,
    find_global_rotation_symmetries,
    write_report,
)

POSITIONS = {
    5: (-2.0, 4.5),
    18: (-3.0, 3.6),
    16: (-3.0, 2.5),
    3: (-2.0, 1.7),
    8: (-1.0, 2.5),
    13: (-1.0, 3.6),
    1: (0.0, 4.5),
    7: (1.0, 3.6),
    20: (1.0, 2.5),
    14: (0.0, 1.7),
    12: (-2.0, 0.3),
    11: (-1.0, -0.5),
    15: (0.0, 0.3),
    9: (-3.0, -0.5),
    19: (-3.0, -1.7),
    2: (-2.0, -2.5),
    10: (-1.0, -1.7),
    4: (1.0, -0.5),
    17: (1.0, -1.7),
    6: (0.0, -2.5),
}

HEXAGONS = {
    "upper-left": (5, 18, 16, 3, 8, 13),
    "upper-right": (1, 13, 8, 14, 20, 7),
    "center": (3, 8, 14, 15, 11, 12),
    "lower-left": (12, 11, 10, 2, 19, 9),
    "lower-right": (15, 4, 17, 6, 10, 11),
}

OUTPUT_DIR = Path(".")


def main() -> None:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False

    analyses = []
    for name, cycle in HEXAGONS.items():
        canonical = canonicalize_by_angle(list(cycle), POSITIONS, clockwise=True)
        analysis = analyze_cycle(canonical, modulo=5, name=name)
        analyses.append(analysis)

    centers = {
        name: (
            sum(POSITIONS[v][0] for v in cycle) / 6,
            sum(POSITIONS[v][1] for v in cycle) / 6,
        )
        for name, cycle in HEXAGONS.items()
    }
    global_syms = find_global_rotation_symmetries(centers, candidates=[60, 120, 180, 240, 300])

    draw_individual_clusters(analyses, str(OUTPUT_DIR / "rotation_cluster"))
    draw_overview(
        analyses,
        global_title="Jisu-yong-yukdo — 5 hexagon rotations (6-cycles)",
        save_path=str(OUTPUT_DIR / "rotation_overview.png"),
        ncols=3,
        modulo=5,
    )

    write_report(
        puzzle_name="Jisu-yong-yukdo (Six-Each-Gets)",
        analyses=analyses,
        global_symmetries=global_syms,
        save_path=str(OUTPUT_DIR / "rotation_report.txt"),
    )


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
