#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
구자각득 궁별 회전 분석.

각 궁은 3×3 격자 전체가 채워져 있다. 중심 칸(1,1)을 제외한 8개 칸이
중심 주변의 8-cycle을 이루며, 위쪽 변 중앙부터 시계방향으로 읽는다.
중심값은 별도 메모로 기록한다.
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
    "upper_palace": [
        [12, 44, 9],
        [19, 21, 29],
        [37, 2, 34],
    ],
    "left_palace": [
        [13, 43, 8],
        [18, 25, 26],
        [38, 3, 33],
    ],
    "center_palace": [
        [15, 41, 6],
        [16, 23, 30],
        [40, 5, 31],
    ],
    "right_palace": [
        [14, 42, 7],
        [17, 24, 28],
        [39, 4, 32],
    ],
    "lower_palace": [
        [11, 45, 10],
        [20, 22, 27],
        [36, 1, 35],
    ],
}

PALACE_ORIGINS = {
    "upper_palace": (3, 6),
    "left_palace": (0, 3),
    "center_palace": (3, 3),
    "right_palace": (6, 3),
    "lower_palace": (3, 0),
}

DISPLAY_LABELS = {
    "upper_palace": "상궁",
    "left_palace": "좌궁",
    "center_palace": "중궁",
    "right_palace": "우궁",
    "lower_palace": "하궁",
}

CLOCKWISE_CELLS = [
    (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0), (0, 0)
]

OUTPUT_DIR = Path(".")


def main() -> None:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Noto Sans CJK KR", "Noto Sans CJK JP", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    analyses = []
    for name, grid in PALACES.items():
        cycle = [grid[r][c] for r, c in CLOCKWISE_CELLS]
        center = grid[1][1]
        analysis = analyze_cycle(cycle, modulo=5, name=DISPLAY_LABELS[name])
        analysis.notes.append(f"중심 칸 = {center}")
        analyses.append(analysis)

    centers = {
        name: (origin[0] + 1.0, origin[1] + 1.0)
        for name, origin in PALACE_ORIGINS.items()
    }
    global_syms = find_global_rotation_symmetries(centers, candidates=[90, 180, 270])

    draw_individual_clusters(analyses, str(OUTPUT_DIR / "rotation_cluster"))
    draw_overview(
        analyses,
        global_title="구자각득 — 5개 궁 회전 분석 (외곽 8-cycle)",
        save_path=str(OUTPUT_DIR / "rotation_overview.png"),
        ncols=3,
        modulo=5,
    )

    write_report(
        puzzle_name="구자각득 (九子各得)",
        analyses=analyses,
        global_symmetries=global_syms,
        save_path=str(OUTPUT_DIR / "rotation_report.txt"),
    )


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
