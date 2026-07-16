#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
낙서사구도(洛書四九圖) 군별 회전 분석.

4개 육각형 면, 외곽 20-cycle, 주석 기반 9개 4자 궁을 각각 회전 객체로
분석한다. 각 cycle은 정점 위치를 이용해 12시 방향부터 시계방향으로
정규화하고, 맞은편 합·mod 5 잉여 패턴·군 내 회전 불변성·전역 회전
대칭성을 보고한다.
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
    19: (-2, 3),
    2: (-3, 2),
    14: (-2, 1),
    5: (-1, 0),
    16: (0, 1),
    7: (-1, 2),
    17: (2, 3),
    4: (1, 2),
    9: (3, 2),
    12: (2, 1),
    10: (1, 0),
    18: (-2, -1),
    3: (-3, -2),
    13: (-2, -3),
    8: (-1, -2),
    11: (0, -1),
    6: (2, -1),
    1: (3, -2),
    20: (2, -3),
    15: (1, -2),
}

HEXAGONS = {
    "NW": [19, 2, 14, 5, 16, 7],
    "NE": [17, 4, 16, 10, 12, 9],
    "SW": [5, 18, 3, 13, 8, 11],
    "SE": [10, 6, 1, 20, 15, 11],
}

HEXAGON_LABELS = {
    "NW": "NW 면",
    "NE": "NE 면",
    "SW": "SW 면",
    "SE": "SE 면",
}

PERIMETER_20 = [19, 2, 14, 5, 18, 3, 13, 8, 11, 15, 20, 1, 6, 10, 12, 9, 17, 4, 16, 7]

NINE_PALACES = {
    "NW": [19, 2, 14, 7],
    "N": [19, 17, 2, 4],
    "NE": [17, 4, 12, 9],
    "W": [14, 7, 18, 3],
    "C": [5, 16, 10, 11],
    "E": [9, 12, 6, 15],
    "SW": [18, 3, 13, 8],
    "S": [13, 8, 20, 1],
    "SE": [6, 1, 20, 15],
}

PALACE_LABELS = {
    "NW": "NW 궁",
    "N": "N 궁",
    "NE": "NE 궁",
    "W": "W 궁",
    "C": "C 궁",
    "E": "E 궁",
    "SW": "SW 궁",
    "S": "S 궁",
    "SE": "SE 궁",
}

OUTPUT_DIR = Path(".")


def main() -> None:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Noto Sans CJK KR", "Noto Sans CJK JP", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    analyses = []

    for name, cycle in HEXAGONS.items():
        canonical = canonicalize_by_angle(list(cycle), POSITIONS, clockwise=True)
        analyses.append(analyze_cycle(canonical, modulo=5, name=HEXAGON_LABELS[name]))

    boundary = canonicalize_by_angle(list(PERIMETER_20), POSITIONS, clockwise=True)
    analyses.append(analyze_cycle(boundary, modulo=5, name="외곽 20-cycle"))

    for name, members in NINE_PALACES.items():
        canonical = canonicalize_by_angle(members, POSITIONS, clockwise=True)
        analyses.append(analyze_cycle(canonical, modulo=5, name=PALACE_LABELS[name]))

    hex_centers = {
        name: (
            sum(POSITIONS[v][0] for v in cycle) / len(cycle),
            sum(POSITIONS[v][1] for v in cycle) / len(cycle),
        )
        for name, cycle in HEXAGONS.items()
    }
    palace_centers = {
        name: (
            sum(POSITIONS[v][0] for v in members) / len(members),
            sum(POSITIONS[v][1] for v in members) / len(members),
        )
        for name, members in NINE_PALACES.items()
    }
    global_syms_hex = find_global_rotation_symmetries(hex_centers, candidates=[90, 180, 270])
    global_syms_pal = find_global_rotation_symmetries(palace_centers, candidates=[90, 180, 270])

    global_syms = global_syms_hex
    if global_syms_pal:
        for angle, mapping in global_syms_pal.items():
            if angle not in global_syms:
                global_syms[angle] = mapping

    draw_individual_clusters(analyses, str(OUTPUT_DIR / "rotation_cluster"))
    draw_overview(
        analyses,
        global_title="낙서사구도 — 육각형, 외곽 20-cycle, 9개 4자 궁의 회전 분석",
        save_path=str(OUTPUT_DIR / "rotation_overview.png"),
        ncols=4,
        modulo=5,
    )

    write_report(
        puzzle_name="낙서사구도 (洛書四九圖)",
        analyses=analyses,
        global_symmetries=global_syms,
        save_path=str(OUTPUT_DIR / "rotation_report.txt"),
    )


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
