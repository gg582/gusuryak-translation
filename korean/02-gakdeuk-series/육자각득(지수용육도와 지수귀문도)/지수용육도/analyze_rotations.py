#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
지수용육도(육자각득) 육각형별 회전 분석.

5개 육각형을 6-cycle로 보고, 각 정점의 위치를 이용해 12시 방향부터
시계방향으로 정규화한 뒤 맞은편 합, mod 5 잉여 패턴, 군 내 회전 불변성,
벌집 배치의 전역 회전 대칭성을 분석한다.
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
    "upper_left": (5, 18, 16, 3, 8, 13),
    "upper_right": (1, 13, 8, 14, 20, 7),
    "center": (3, 8, 14, 15, 11, 12),
    "lower_left": (12, 11, 10, 2, 19, 9),
    "lower_right": (15, 4, 17, 6, 10, 11),
}

DISPLAY_LABELS = {
    "upper_left": "상좌",
    "upper_right": "상우",
    "center": "중앙",
    "lower_left": "하좌",
    "lower_right": "하우",
}

OUTPUT_DIR = Path(".")


def main() -> None:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Noto Sans CJK KR", "Noto Sans CJK JP", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    analyses = []
    for name, cycle in HEXAGONS.items():
        canonical = canonicalize_by_angle(list(cycle), POSITIONS, clockwise=True)
        analysis = analyze_cycle(canonical, modulo=5, name=DISPLAY_LABELS[name])
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
        global_title="지수용육도 — 5개 육각형 회전 분석 (6-cycle)",
        save_path=str(OUTPUT_DIR / "rotation_overview.png"),
        ncols=3,
        modulo=5,
    )

    write_report(
        puzzle_name="지수용육도 (육자각득)",
        analyses=analyses,
        global_symmetries=global_syms,
        save_path=str(OUTPUT_DIR / "rotation_report.txt"),
    )


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
