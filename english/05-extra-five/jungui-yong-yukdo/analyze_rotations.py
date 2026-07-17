#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rotation analysis of Jungui-yongyukdo (重儀用六圖).

Cyclic structures analyzed:
  · Perimeter 12-cycle: the 12 outer values, clockwise from top-left 7
  · Inner 4-cycle: the 4 values of the inner rectangle, clockwise from
    top-left 11
  · The four sum-51 groups: not drawn as rings in the source diagram, but
    each group's 6 cells form a convex polygon geometrically, so they are
    listed in clockwise geometric order and included (see notes).
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

# Same coordinates as visualize.py
POSITIONS = {
    7: (-2.5, 3), 16: (-1, 3.2), 1: (1, 3.2), 6: (2.5, 3),
    13: (-3, 1.5), 11: (-1, 1), 10: (1, 1), 4: (3, 1.5),
    3: (-3, -1.5), 9: (-1, -1), 12: (1, -1), 14: (3, -1.5),
    8: (-2.5, -3), 2: (-1, -3.2), 15: (1, -3.2), 5: (2.5, -3),
}

# The four 6-value groups, each summing to 51
GROUPS = {
    "top group": [7, 16, 1, 6, 11, 10],
    "left group": [7, 13, 11, 3, 9, 8],
    "bottom group": [8, 2, 9, 12, 15, 5],
    "right group": [6, 10, 4, 12, 14, 5],
}

# Perimeter 12-cycle: starts at top-left 7, clockwise
PERIMETER = [7, 16, 1, 6, 4, 14, 5, 15, 2, 8, 3, 13]

# Inner 4-cycle: starts at top-left 11, clockwise
INNER = [11, 10, 12, 9]

# The 6 cells of each group in clockwise geometric order (from its top-left cell)
GROUP_SEQ = {
    "top group": [16, 1, 6, 10, 11, 7],
    "left group": [7, 11, 9, 8, 3, 13],
    "bottom group": [9, 12, 5, 15, 2, 8],
    "right group": [6, 4, 14, 5, 12, 10],
}

OUTPUT_DIR = Path(".")


def assert_clockwise(seq: list[int], name: str) -> None:
    """Verify clockwise (convex) order: every consecutive triple must have
    a non-positive cross product."""
    pts = [POSITIONS[v] for v in seq]
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        x3, y3 = pts[(i + 2) % n]
        cross = (x2 - x1) * (y3 - y2) - (y2 - y1) * (x3 - x2)
        if cross > 0:
            raise ValueError(f"{name}: non-clockwise vertex found (index {i})")


def main() -> None:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False

    # Verify the geometric orders
    assert_clockwise(PERIMETER, "perimeter 12-cycle")
    assert_clockwise(INNER, "inner 4-cycle")
    for name, seq in GROUP_SEQ.items():
        if sorted(seq) != sorted(GROUPS[name]):
            raise ValueError(f"{name} order does not match group members: {seq}")
        assert_clockwise(seq, name)

    analyses = []

    perimeter_analysis = analyze_cycle(PERIMETER, modulo=5, name="perimeter 12-cycle")
    perimeter_analysis.notes.append(
        "Clockwise from top-left 7. Opposite sums are pairs under 180-degree rotation."
    )
    analyses.append(perimeter_analysis)

    inner_analysis = analyze_cycle(INNER, modulo=5, name="inner 4-cycle")
    inner_analysis.notes.append(
        "Inner rectangle (11,10,12,9), clockwise from top-left 11."
    )
    analyses.append(inner_analysis)

    for name, seq in GROUP_SEQ.items():
        analysis = analyze_cycle(seq, modulo=5, name=name)
        analysis.notes.append(
            "Not a ring in the source diagram; the 6 cells are listed in clockwise "
            f"geometric order (group sum {sum(seq)} for verification)."
        )
        analyses.append(analysis)

    # Global rotation symmetry: group centers = centroids of member coordinates
    centers = {}
    for name, members in GROUPS.items():
        cx = sum(POSITIONS[v][0] for v in members) / len(members)
        cy = sum(POSITIONS[v][1] for v in members) / len(members)
        centers[name] = (round(cx, 6), round(cy, 6))
    global_syms = find_global_rotation_symmetries(centers, candidates=[180])

    draw_individual_clusters(analyses, str(OUTPUT_DIR / "rotation_cluster"))
    draw_overview(
        analyses,
        global_title="Jungui-yongyukdo — perimeter 12-cycle, inner 4-cycle, and 4 groups",
        save_path=str(OUTPUT_DIR / "rotation_overview.png"),
        ncols=3,
        modulo=5,
    )

    write_report(
        puzzle_name="Jungui-yongyukdo (重儀用六圖)",
        analyses=analyses,
        global_symmetries=global_syms,
        save_path=str(OUTPUT_DIR / "rotation_report.txt"),
    )


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
