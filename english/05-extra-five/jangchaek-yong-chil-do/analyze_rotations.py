#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Per-cluster rotation analysis for Jangchaek-yong-chil-do (章策用七圖).

The three concentric rings (graph distances d1, d2, d3 from the center 7) are
analyzed as 6-cycles, each read clockwise starting from the position nearest
12 o'clock.  The three axes (7 cells each) are linear, not cyclic, so they are
recorded as reference sequences with a note.
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

CENTER = 7
SPACING = 1.2

# Same coordinate geometry as visualize.py
AXES = {
    "Vertical axis 90": [5, 18, 9, 7, 12, 2, 15],
    "Diagonal axis 150": [4, 10, 19, 7, 1, 14, 13],
    "Diagonal axis 30": [8, 6, 17, 7, 3, 11, 16],
}
AXIS_ANGLE = {"Vertical axis 90": 90.0, "Diagonal axis 150": 150.0, "Diagonal axis 30": 30.0}

POSITIONS = {CENTER: (0.0, 0.0)}
for axis_name, nodes in AXES.items():
    angle = math.radians(AXIS_ANGLE[axis_name])
    for i, node in enumerate(nodes):
        if node == CENTER:
            continue
        dist = 3 - i
        POSITIONS[node] = (
            dist * math.cos(angle) * SPACING,
            dist * math.sin(angle) * SPACING,
        )


def _angle_of(v: int) -> float:
    x, y = POSITIONS[v]
    return math.degrees(math.atan2(y, x))


def clockwise_from_top(values: list[int]) -> list[int]:
    """Order clockwise (decreasing angle) starting nearest to 12 o'clock (90°)."""
    return sorted(values, key=lambda v: (90.0 - _angle_of(v)) % 360.0)


# Concentric rings by distance from the center
RINGS: dict[int, list[int]] = {1: [], 2: [], 3: []}
for node, (x, y) in POSITIONS.items():
    if node == CENTER:
        continue
    d = round(math.hypot(x, y) / SPACING)
    RINGS[d].append(node)

RING_NAMES = {1: "Ring d1", 2: "Ring d2", 3: "Ring d3"}

OUTPUT_DIR = Path(".")


def main() -> None:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False

    analyses = []

    # Analyze the three rings as 6-cycles (order computed from actual azimuth angles)
    for d in [1, 2, 3]:
        cycle = clockwise_from_top(RINGS[d])
        analysis = analyze_cycle(cycle, modulo=5, name=RING_NAMES[d])
        analysis.notes.append(
            f"Ring at distance {d} from center 7; opposite pairs are the "
            f"center-symmetric pairs of the same axis"
        )
        analyses.append(analysis)

    # The three axes are linear (not cyclic), recorded as reference sequences
    for axis_name, nodes in AXES.items():
        idx = nodes.index(CENTER)
        first, last = nodes[0], nodes[-1]
        # Ensure the sequence starts at the end nearest 12 o'clock
        if abs(_angle_of(first) - 90.0) > abs(_angle_of(last) - 90.0):
            nodes = list(reversed(nodes))
        analysis = analyze_cycle(nodes, modulo=5, name=axis_name)
        analysis.notes.append(
            "Linear (non-cyclic) axis: sequence from the end nearest 12 o'clock "
            "through the center to the opposite end; rotation-invariance "
            "metrics do not apply since it is not a cycle"
        )
        analysis.notes.append(f"center cell = {CENTER} (index {idx})")
        analyses.append(analysis)

    # Cluster centroids: every ring and axis shares the origin (concentric layout)
    centers = {}
    for analysis in analyses:
        xs = [POSITIONS[v][0] for v in analysis.values]
        ys = [POSITIONS[v][1] for v in analysis.values]
        centers[analysis.name] = (sum(xs) / len(xs), sum(ys) / len(ys))

    origin = (0.0, 0.0)
    concentric = all(
        math.hypot(cx - origin[0], cy - origin[1]) < 1e-9
        for cx, cy in centers.values()
    )
    if concentric:
        # All centroids coincide at the origin, so the global rotation test degenerates.
        global_syms = {}
        note = (
            "Concentric layout: all cluster centroids coincide at the origin "
            "(0,0), so the global rotational symmetry test is degenerate and "
            "was skipped. The geometry itself has 60-degree rotational "
            "symmetry of positions, but the value arrangement is not "
            "rotationally invariant"
        )
        for analysis in analyses:
            analysis.notes.append(note)
    else:
        global_syms = find_global_rotation_symmetries(
            centers, candidates=[60, 120, 180, 240, 300]
        )

    draw_individual_clusters(analyses, str(OUTPUT_DIR / "rotation_cluster"))
    draw_overview(
        analyses,
        global_title="Jangchaek-yong-chil-do — concentric rings (d1/d2/d3) and 3 axes rotation analysis",
        save_path=str(OUTPUT_DIR / "rotation_overview.png"),
        ncols=3,
        modulo=5,
    )

    write_report(
        puzzle_name="Jangchaek-yong-chil-do (章策用七圖)",
        analyses=analyses,
        global_symmetries=global_syms,
        save_path=str(OUTPUT_DIR / "rotation_report.txt"),
    )


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
