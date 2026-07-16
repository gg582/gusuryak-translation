#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
팔자각득 궁별 회전 분석.

각 궁은 3×3 격자에서 중심이 비어 있고 8개의 수가 중심 주변을 이룬다.
위쪽 가울짓칸부터 시계방향으로 8-cycle을 읽어 맞은편 합, mod 5 잉여 패턴,
궁 내 회전 불변성, 전체 십자 배치의 회전 대칭성을 분석한다.
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
        [39, 7, 34],
        [12, None, 19],
        [24, 2, 27],
    ],
    "left_palace": [
        [33, 18, 28],
        [8, None, 3],
        [38, 13, 23],
    ],
    "center_palace": [
        [30, 5, 21],
        [16, None, 15],
        [31, 10, 36],
    ],
    "right_palace": [
        [22, 14, 37],
        [4, None, 9],
        [29, 17, 32],
    ],
    "lower_palace": [
        [26, 1, 25],
        [20, None, 11],
        [35, 6, 40],
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
        analysis = analyze_cycle(cycle, modulo=5, name=DISPLAY_LABELS[name])
        analyses.append(analysis)

    centers = {
        name: (origin[0] + 1.0, origin[1] + 1.0)
        for name, origin in PALACE_ORIGINS.items()
    }
    global_syms = find_global_rotation_symmetries(centers, candidates=[90, 180, 270])

    draw_individual_clusters(analyses, str(OUTPUT_DIR / "rotation_cluster"))
    draw_overview(
        analyses,
        global_title="팔자각득 — 5개 궁 회전 분석 (8-cycle)",
        save_path=str(OUTPUT_DIR / "rotation_overview.png"),
        ncols=3,
        modulo=5,
    )

    write_report(
        puzzle_name="팔자각득 (八子各得)",
        analyses=analyses,
        global_symmetries=global_syms,
        save_path=str(OUTPUT_DIR / "rotation_report.txt"),
    )


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
