#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rotation analysis for Ojagakdeuk (Five-Each-Gets / Heaven-Water Five-Use Diagram) Layout 2.

A variant with the same shape as the original placement (analyze_rotations.py)
but a different number placement (1–21).  The original diagram has no explicit
edges and no natural palace cycles.  We therefore treat each mod-5 residue
class as a cyclic cluster, ordering its members clockwise from the top around
the vertical axis of the figure.  We report opposite-pair sums where
applicable, mod-5 residue patterns (trivially constant within a class), and
the global rotational symmetry of the placement.
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

POSITIONS = {
    12: (0.0, 6.0),
    17: (-1.5, 5.0),
    18: (1.5, 5.0),
    5:  (0.0, 4.2),
    13: (-2.8, 3.3),
    2:  (0.0, 3.3),
    19: (2.8, 3.3),
    7:  (-4.2, 2.0),
    3:  (-2.8, 2.0),
    20: (-1.4, 2.0),
    15: (0.0, 2.0),
    9:  (1.4, 2.0),
    4:  (2.8, 2.0),
    8:  (4.2, 2.0),
    11: (-2.8, 0.8),
    6:  (0.0, 0.8),
    14: (2.8, 0.8),
    10: (-1.8, -0.4),
    1:  (0.0, -0.4),
    21: (1.8, -0.4),
    16: (0.0, -1.7),
}

GROUPS = {
    1: [1, 6, 11, 16, 21],
    2: [2, 7, 12, 17],
    3: [3, 8, 13, 18],
    4: [4, 9, 14, 19],
    0: [5, 10, 15, 20],
}

RESIDUE_NAMES = {
    1: "Water (r=1)",
    2: "Fire (r=2)",
    3: "Wood (r=3)",
    4: "Metal (r=4)",
    0: "Earth (r=5)",
}

OUTPUT_DIR = Path(".")


def main() -> None:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False

    # Order each residue class clockwise from the top around the vertical axis.
    cx, cy = 0.0, 2.0

    def angle_of(v: int) -> float:
        x, y = POSITIONS[v]
        return math.degrees(math.atan2(y - cy, x - cx))

    analyses = []
    for r in [1, 2, 3, 4, 0]:
        members = sorted(GROUPS[r], key=lambda v: angle_of(v), reverse=True)
        # Start at the value closest to the top (angle 90°).
        start_idx = min(range(len(members)), key=lambda i: abs(angle_of(members[i]) - 90.0))
        ordered = [members[(start_idx + i) % len(members)] for i in range(len(members))]
        analysis = analyze_cycle(ordered, modulo=5, name=RESIDUE_NAMES[r])
        analysis.notes.append("Residue class arranged by angular position; no intrinsic cycle in original text.")
        analyses.append(analysis)

    # Global rotational symmetry: only 180° is plausible for the vertical diamond.
    centers = {v: (x, y) for v, (x, y) in POSITIONS.items()}
    global_syms = find_global_rotation_symmetries(centers, candidates=[180], tolerance=1e-5)

    # Per-cluster images: generate with a temporary prefix, then rename with the _2 suffix
    tmp_prefix = str(OUTPUT_DIR / "rotation_cluster_tmp2")
    draw_individual_clusters(analyses, tmp_prefix)
    for tmp_path in sorted(OUTPUT_DIR.glob("rotation_cluster_tmp2_*.png")):
        final_name = tmp_path.name.replace("rotation_cluster_tmp2_", "rotation_cluster_", 1)
        final_name = final_name[:-4] + "_2.png"
        tmp_path.rename(OUTPUT_DIR / final_name)
        print(f"Renamed cluster: {final_name}")

    draw_overview(
        analyses,
        global_title="Ojagakdeuk Layout 2 — residue-class rotations (no intrinsic palace cycles)",
        save_path=str(OUTPUT_DIR / "rotation_overview_2.png"),
        ncols=3,
        modulo=5,
    )

    write_report(
        puzzle_name="Ojagakdeuk Layout 2 (Five-Each-Gets / Heaven-Water Five-Use Diagram, 1–21)",
        analyses=analyses,
        global_symmetries=global_syms,
        save_path=str(OUTPUT_DIR / "rotation_report_2.txt"),
    )


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
