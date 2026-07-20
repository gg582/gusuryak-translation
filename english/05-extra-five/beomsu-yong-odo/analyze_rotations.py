#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rotation analysis of the Beomsu-yongodo (範數用五圖) rings and axes.

The two concentric 4-cycles (inner/outer ring) are read clockwise from
12 o'clock; the two axes (horizontal/vertical) are included as linear
5-cell sequences with notes, since they are not cycles.
Every cluster's centroid coincides with the origin (concentric layout), so
the global-rotation check is degenerate and skipped with a recorded reason.
"""

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
    draw_individual_clusters,
    draw_overview,
    find_global_rotation_symmetries,
    write_report,
)

# Coordinates from visualize.py.
POSITIONS = {
    3: (-2, 0), 7: (-1, 0), 5: (0, 0), 4: (1, 0), 6: (2, 0),
    2: (0, 2), 8: (0, 1), 1: (0, -1), 9: (0, -2),
}

# Cycles read clockwise from the top.
INNER_RING = [8, 4, 1, 7]   # inner ring (midpoints) 4-cycle
OUTER_RING = [2, 6, 9, 3]   # outer ring (endpoints) 4-cycle

# Linear axes (geometric reading order only; not cycles).
HORIZONTAL = [3, 7, 5, 4, 6]  # left -> right
VERTICAL = [2, 8, 5, 1, 9]    # top -> bottom

OUTPUT_DIR = Path(".")


def centroid(values: list[int]) -> tuple[float, float]:
    xs = [POSITIONS[v][0] for v in values]
    ys = [POSITIONS[v][1] for v in values]
    return (sum(xs) / len(xs), sum(ys) / len(ys))


def main() -> None:
    configure_matplotlib_fonts()

    analyses = []

    inner = analyze_cycle(INNER_RING, modulo=5, name="inner ring 4-cycle")
    inner.notes.append("center 5 is not part of the ring (separate single cell)")
    inner.notes.append("antipodal pair sums split 9 and 11 — the two pairs total 20 = ring sum")
    inner.notes.append("residues cover Water/Fire/Wood/Metal (1,2,3,4) exactly once")
    analyses.append(inner)

    outer = analyze_cycle(OUTER_RING, modulo=5, name="outer ring 4-cycle")
    outer.notes.append("antipodal pair sums 11 and 9 — crossed against the inner ring "
                       "(horizontal: outer 9 / inner 11, vertical: outer 11 / inner 9)")
    outer.notes.append("residues cover Water/Fire/Wood/Metal (1,2,3,4) exactly once")
    analyses.append(outer)

    horiz = analyze_cycle(HORIZONTAL, modulo=5, name="horizontal axis 5-sequence")
    horiz.notes.append("linear axis, not a cycle — read left to right")
    horiz.notes.append("odd length 5, so opposite-pair sums are undefined")
    horiz.notes.append("residue sequence 3-2-5-4-1 = generation cycle "
                       "Wood->Fire->Earth->Metal->Water (every neighbor pair generates)")
    analyses.append(horiz)

    vert = analyze_cycle(VERTICAL, modulo=5, name="vertical axis 5-sequence")
    vert.notes.append("linear axis, not a cycle — read top to bottom")
    vert.notes.append("odd length 5, so opposite-pair sums are undefined")
    vert.notes.append("the two edges adjacent to the center (8-5, 5-1) are overcoming pairs")
    analyses.append(vert)

    # Global rotation symmetry: check whether all cluster centroids coincide.
    centers = {
        "inner_ring": centroid(INNER_RING),
        "outer_ring": centroid(OUTER_RING),
        "horizontal_axis": centroid(HORIZONTAL),
        "vertical_axis": centroid(VERTICAL),
    }
    distinct = set(centers.values())
    global_syms: dict = {}
    degenerate_note = None
    if len(distinct) == 1:
        only = next(iter(distinct))
        degenerate_note = (
            f"All cluster centroids coincide at the single point {only} (concentric layout).\n"
            "A global rotation mapping cluster centers onto other cluster centers is undefined "
            "(degenerate), so the check is skipped.\n"
            "Geometrically a 90-degree rotation preserves the cross shape, but not the value labels."
        )
    else:
        global_syms = find_global_rotation_symmetries(centers, candidates=[90, 180, 270])

    draw_individual_clusters(analyses, str(OUTPUT_DIR / "rotation_cluster"))
    draw_overview(
        analyses,
        global_title="Beomsu-yongodo — inner/outer ring + two axes rotation analysis (mod 5)",
        save_path=str(OUTPUT_DIR / "rotation_overview.png"),
        ncols=2,
        modulo=5,
    )

    report_path = str(OUTPUT_DIR / "rotation_report.txt")
    write_report(
        puzzle_name="Beomsu-yongodo (範數用五圖)",
        analyses=analyses,
        global_symmetries=global_syms,
        save_path=report_path,
    )
    if degenerate_note:
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("\nNOTE (concentric layout):\n" + degenerate_note + "\n")
        print("NOTE (concentric layout):")
        print(degenerate_note)


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
