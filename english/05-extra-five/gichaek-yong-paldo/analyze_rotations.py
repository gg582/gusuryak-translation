#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Per-octagon rotation analysis of Gichaek-yongpaldo (奇策用八圖).

Each of the four regular octagons forms an 8-cycle.  Cycles are read in the
canonical order: starting at the vertex nearest 12 o'clock, then clockwise.
Adjacent octagons share one edge (two vertices).  The central square
(8-19-6-17) is included as a fifth 4-cycle cluster.
"""

import math
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt

from cjk_font_config import configure_matplotlib_fonts


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

# Counterclockwise vertex order (same as visualize.py / analyze_gichaek_yongpaldo.py)
GROUPS = {
    "Top": [4, 9, 14, 23, 5, 8, 19, 18],
    "Left": [8, 5, 15, 22, 3, 10, 20, 17],
    "Right": [1, 12, 18, 19, 6, 7, 13, 24],
    "Bottom": [7, 6, 17, 20, 2, 11, 16, 21],
}

SHARED = {
    "Top": [("Left", (5, 8)), ("Right", (18, 19))],
    "Left": [("Top", (5, 8)), ("Bottom", (17, 20))],
    "Right": [("Top", (18, 19)), ("Bottom", (6, 7))],
    "Bottom": [("Left", (17, 20)), ("Right", (6, 7))],
}

OCTAGON_RADIUS = 2.3
ROTATION = math.pi / 8.0

OUTPUT_DIR = Path(".")


def build_positions():
    apothem = OCTAGON_RADIUS * math.cos(math.pi / 8.0)
    offset = math.sqrt(2.0) * apothem
    centers = {"Top": (0.0, offset), "Left": (-offset, 0.0),
               "Right": (offset, 0.0), "Bottom": (0.0, -offset)}
    positions = {}
    for name, (cx, cy) in centers.items():
        for i, value in enumerate(GROUPS[name]):
            point = (
                cx + OCTAGON_RADIUS * math.cos(ROTATION + i * math.pi / 4.0),
                cy + OCTAGON_RADIUS * math.sin(ROTATION + i * math.pi / 4.0),
            )
            positions.setdefault(value, point)
    return centers, positions


def main() -> None:
    configure_matplotlib_fonts()

    centers, positions = build_positions()

    analyses = []
    for name, values in GROUPS.items():
        cycle = canonicalize_by_angle(values, positions, clockwise=True)
        analysis = analyze_cycle(cycle, modulo=5, name=f"{name} octagon")
        shared_note = ", ".join(f"shared edge with {other} {pair}"
                                for other, pair in SHARED[name])
        analysis.notes.append(f"sum = {sum(values)} (target 100)")
        analysis.notes.append(shared_note)
        analyses.append(analysis)

    # Central square 4-cycle (minimum cycle formed by the inner edges)
    central = canonicalize_by_angle([8, 19, 6, 17], positions, clockwise=True)
    central_analysis = analyze_cycle(central, modulo=5, name="central square")
    central_analysis.notes.append("sum = 50 = S/2, minimum cycle (girth 4)")
    central_analysis.notes.append("all vertices are shared vertices (degree 3)")
    analyses.append(central_analysis)

    all_centers = dict(centers)
    all_centers["Center"] = (0.0, 0.0)
    global_syms = find_global_rotation_symmetries(all_centers, candidates=[90, 180, 270])

    draw_individual_clusters(analyses, str(OUTPUT_DIR / "rotation_cluster"))
    draw_overview(
        analyses,
        global_title="Gichaek-yongpaldo — per-octagon rotation analysis (8-cycles)",
        save_path=str(OUTPUT_DIR / "rotation_overview.png"),
        ncols=3,
        modulo=5,
    )

    write_report(
        puzzle_name="Gichaek-yongpaldo (奇策用八圖)",
        analyses=analyses,
        global_symmetries=global_syms,
        save_path=str(OUTPUT_DIR / "rotation_report.txt"),
    )


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
