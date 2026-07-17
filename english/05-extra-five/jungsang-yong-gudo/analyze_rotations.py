#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Per-cluster rotation analysis for Jungsang-yonggudo.

On the four axes sharing the center 9, the eight nodes at equal graph distance
from the center form concentric octagonal rings (d1-d4).  Each ring is analyzed
as an 8-cycle read clockwise from the 12 o'clock position.  The four straight
axes are recorded as non-cyclic line clusters for reference.  All cluster
centroids coincide at the origin (concentric layout), so the global rotation
symmetry check is degenerate; the reason is noted in the report.
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

# Coordinates are identical to visualize.py and analyze_jungsang_yonggudo.py
# in this directory.
COORDS = {
    27: (-4, 4), 20: (0, 4), 33: (4, 4),
    15: (-2, 3), 16: (0, 3), 1: (2, 3),
    3: (-1.5, 2), 23: (0, 2), 13: (1.5, 2),
    24: (-1, 1), 10: (0, 1), 22: (1, 1),
    28: (-4, 0), 5: (-3, 0), 11: (-2, 0), 25: (-1, 0), 9: (0, 0),
    7: (1, 0), 19: (2, 0), 31: (3, 0), 12: (4, 0),
    18: (-1, -1), 2: (0, -1), 30: (1, -1),
    26: (-1.5, -2), 29: (0, -2), 14: (1.5, -2),
    17: (-2, -3), 32: (0, -3), 21: (2, -3),
    8: (-4, -4), 6: (0, -4), 4: (4, -4),
}

CENTER = 9

AXES = {
    "vertical": [20, 16, 23, 10, 9, 2, 29, 32, 6],
    "horizontal": [28, 5, 11, 25, 9, 7, 19, 31, 12],
    "diagonal1": [27, 15, 3, 24, 9, 30, 14, 21, 4],
    "diagonal2": [33, 1, 13, 22, 9, 18, 26, 17, 8],
}

AXIS_LABELS = {
    "vertical": "Vertical axis",
    "horizontal": "Horizontal axis",
    "diagonal1": "Diagonal axis 1",
    "diagonal2": "Diagonal axis 2",
}

OUTPUT_DIR = Path(".")

DEGENERATE_NOTE = """Global rotational symmetry (note: degenerate due to concentric layout)
--------------------------------------------------
The centroid of every cluster (4 rings + 4 axes) coincides exactly with the
origin (0, 0): the layout is concentric.  Any rotation about the origin leaves
every cluster center fixed, so the global rotation symmetry defined as a
permutation of clusters is degenerate.  The find_global_rotation_symmetries
check is therefore skipped and only this fact is recorded.
(For the rotational properties of the rings themselves, see each 8-cycle
analysis above.)
"""


def clockwise_from_top(values: list[int]) -> list[int]:
    """Sort by bearing so the list starts at 12 o'clock and runs clockwise."""
    return sorted(
        values,
        key=lambda v: math.atan2(COORDS[v][0], COORDS[v][1]) % (2 * math.pi),
    )


def build_rings() -> dict[str, list[int]]:
    """Group nodes whose axial distance (= graph distance) from the center is equal."""
    rings: dict[str, list[int]] = {f"d{d}": [] for d in range(1, 5)}
    for axis in AXES.values():
        center_idx = axis.index(CENTER)
        for i, value in enumerate(axis):
            if value == CENTER:
                continue
            rings[f"d{abs(i - center_idx)}"].append(value)
    return rings


def centroid(members: list[int]) -> tuple[float, float]:
    xs = [COORDS[v][0] for v in members]
    ys = [COORDS[v][1] for v in members]
    return (sum(xs) / len(xs), sum(ys) / len(ys))


def main() -> None:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False

    rings = build_rings()
    analyses = []

    # The 4 concentric octagonal rings: 8-cycles (start at top, clockwise).
    for d in range(1, 5):
        name = f"Ring d{d}"
        cycle = clockwise_from_top(rings[f"d{d}"])
        analysis = analyze_cycle(cycle, modulo=5, name=name)
        analysis.notes.append(f"Concentric octagonal ring at graph distance {d} from center {CENTER}")
        analysis.notes.append(
            f"Ring sum 138 = (561-9)/4; adjoining the center {CENTER} gives 147 "
            "(matches the source text 'four surrounding rings each obtain 147')"
        )
        analyses.append(analysis)

    # The 4 straight axes: non-cyclic line clusters (for reference).
    for key, axis in AXES.items():
        analysis = analyze_cycle(axis, modulo=5, name=AXIS_LABELS[key])
        analysis.notes.append("Non-cyclic line cluster (straight axis) -- rotational period analysis applies to the rings only")
        analysis.notes.append("Odd length (9), so opposite-pair sums are skipped")
        analysis.notes.append(f"Sum 147 = 69+{CENTER}+69 (ray + center + ray)")
        analyses.append(analysis)

    # Global rotation symmetry: check whether all centroids coincide at the origin.
    members = {f"Ring d{d}": rings[f"d{d}"] for d in range(1, 5)}
    members.update({AXIS_LABELS[k]: v for k, v in AXES.items()})
    centers = {name: centroid(vals) for name, vals in members.items()}
    max_radius = max(math.hypot(x, y) for x, y in centers.values())
    if max_radius < 1e-9:
        # Degenerate: skip the global symmetry check and record the reason.
        global_syms: dict[float, dict] = {}
        degenerate = True
    else:
        global_syms = find_global_rotation_symmetries(centers, candidates=[45, 90, 135, 180, 225, 270, 315])
        degenerate = False

    draw_individual_clusters(analyses, str(OUTPUT_DIR / "rotation_cluster"))
    draw_overview(
        analyses,
        global_title="Jungsang-yonggudo -- 4 concentric rings (8-cycles) + 4 axes rotation analysis",
        save_path=str(OUTPUT_DIR / "rotation_overview.png"),
        ncols=3,
        modulo=5,
    )

    report_path = OUTPUT_DIR / "rotation_report.txt"
    write_report(
        puzzle_name="Jungsang-yonggudo",
        analyses=analyses,
        global_symmetries=global_syms,
        save_path=str(report_path),
    )
    if degenerate:
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("\n" + DEGENERATE_NOTE)
        print(DEGENERATE_NOTE)


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
