#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Per-cluster rotation analysis for Chiljagakdeuk (Seven-Each-Gets).

Each of the 5 clusters has a center value + 6 peripheral slots arranged
clockwise from 12 o'clock (SLOT_ANGLES).  We treat each cluster as a 7-cycle
(center, then slots 0..5) and report opposite-pair sums, mod-5 residue patterns,
cluster invariants, and global rotational symmetries of the cross layout.
"""

import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Make the shared helper importable from any subdirectory.
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

# Re-use the data from visualize.py
CLUSTER_SPACING = 3.3

CLUSTERS = [
    {"id": "C1", "dir": "top",    "pos": (0.0, CLUSTER_SPACING),  "center": 2,  "slots": [29, 1, 24, 34, 11, 19]},
    {"id": "C2", "dir": "left",   "pos": (-CLUSTER_SPACING, 0.0), "center": 3,  "slots": [6, 33, 23, 13, 34, 8]},
    {"id": "C3", "dir": "center", "pos": (0.0, 0.0),              "center": 5,  "slots": [22, 7, 20, 30, 26, 10]},
    {"id": "C4", "dir": "right",  "pos": (CLUSTER_SPACING, 0.0),  "center": 4,  "slots": [15, 28, 9, 18, 32, 14]},
    {"id": "C5", "dir": "bottom", "pos": (0.0, -CLUSTER_SPACING), "center": 1,  "slots": [35, 16, 21, 24, 6, 17]},
]

OUTPUT_DIR = Path("figures")
OUTPUT_DIR.mkdir(exist_ok=True)


def main() -> None:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False

    analyses = []
    for cluster in CLUSTERS:
        # 7-cycle: center first, then the six peripheral slots in their
        # existing clockwise-from-12 order.
        cycle_values = [cluster["center"]] + cluster["slots"]
        analysis = analyze_cycle(cycle_values, modulo=5, name=cluster["id"])
        analysis.notes.append(f"center={cluster['center']}, direction={cluster['dir']}")
        analyses.append(analysis)

    # Global rotational symmetry of the cross layout
    centers = {c["id"]: c["pos"] for c in CLUSTERS}
    # Only 180° is a candidate for the cross; 90° is not because top/bottom
    # and left/right would have to swap compatibly.
    global_syms = find_global_rotation_symmetries(centers, candidates=[90, 180, 270])

    # Figures
    draw_individual_clusters(analyses, str(OUTPUT_DIR / "rotation_cluster"))
    draw_overview(
        analyses,
        global_title="Chiljagakdeuk — 5 cluster rotations (center + 6 slots)",
        save_path=str(OUTPUT_DIR / "rotation_overview.png"),
        ncols=3,
        modulo=5,
    )

    # Report
    write_report(
        puzzle_name="Chiljagakdeuk (Seven-Each-Gets)",
        analyses=analyses,
        global_symmetries=global_syms,
        save_path=str(OUTPUT_DIR / "rotation_report.txt"),
    )


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
