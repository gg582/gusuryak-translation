#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""기책용팔도 팔각형별 회전 분석.

4개의 정팔각형(상·하·좌·우)이 각각 8-cycle을 이룬다. 각 사이클은
12시 방향에 가장 가까운 꼭짓점부터 시계방향으로 읽는 정준 순서를 쓴다.
인접 팔각형은 한 변(꼭짓점 2개)을 공유한다.
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
    canonicalize_by_angle,
    draw_individual_clusters,
    draw_overview,
    find_global_rotation_symmetries,
    write_report,
)

# 반시계 방향 꼭짓점 순서 (visualize.py / analyze_gichaek_yongpaldo.py 와 동일)
GROUPS = {
    "상": [4, 9, 14, 23, 5, 8, 19, 18],
    "좌": [8, 5, 15, 22, 3, 10, 20, 17],
    "우": [1, 12, 18, 19, 6, 7, 13, 24],
    "하": [7, 6, 17, 20, 2, 11, 16, 21],
}

SHARED = {
    "상": [("좌", (5, 8)), ("우", (18, 19))],
    "좌": [("상", (5, 8)), ("하", (17, 20))],
    "우": [("상", (18, 19)), ("하", (6, 7))],
    "하": [("좌", (17, 20)), ("우", (6, 7))],
}

OCTAGON_RADIUS = 2.3
ROTATION = math.pi / 8.0

OUTPUT_DIR = Path(".")


def build_positions():
    apothem = OCTAGON_RADIUS * math.cos(math.pi / 8.0)
    offset = math.sqrt(2.0) * apothem
    centers = {"상": (0.0, offset), "좌": (-offset, 0.0),
               "우": (offset, 0.0), "하": (0.0, -offset)}
    positions = {}
    for name, (cx, cy) in centers.items():
        for i, value in enumerate(GROUPS[name]):
            point = (
                cx + OCTAGON_RADIUS * math.cos(ROTATION + i * math.pi / 4.0),
                cy + OCTAGON_RADIUS * math.sin(ROTATION + i * math.pi / 4.0),
            )
            positions.setdefault(value, point)
    return centers, positions


def main() -> None:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Noto Sans CJK KR", "NanumGothic", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    centers, positions = build_positions()

    analyses = []
    for name, values in GROUPS.items():
        cycle = canonicalize_by_angle(values, positions, clockwise=True)
        analysis = analyze_cycle(cycle, modulo=5, name=f"{name} 팔각형")
        shared_note = ", ".join(f"{other}와 공유 변 {pair}" for other, pair in SHARED[name])
        analysis.notes.append(f"합 = {sum(values)} (목표 100)")
        analysis.notes.append(shared_note)
        analyses.append(analysis)

    # 중앙 정사각형 4-cycle (각 팔각형의 안쪽 변을 이은 최소 사이클)
    central = canonicalize_by_angle([8, 19, 6, 17], positions, clockwise=True)
    central_analysis = analyze_cycle(central, modulo=5, name="중앙 정사각형")
    central_analysis.notes.append("합 = 50 = S/2, girth 4 의 최소 사이클")
    central_analysis.notes.append("꼭짓점 전부가 공유 꼭짓점(차수 3)")
    analyses.append(central_analysis)

    all_centers = dict(centers)
    all_centers["중앙"] = (0.0, 0.0)
    global_syms = find_global_rotation_symmetries(all_centers, candidates=[90, 180, 270])

    draw_individual_clusters(analyses, str(OUTPUT_DIR / "rotation_cluster"))
    draw_overview(
        analyses,
        global_title="기책용팔도 — 4개 팔각형 회전 분석 (8-cycles)",
        save_path=str(OUTPUT_DIR / "rotation_overview.png"),
        ncols=2,
        modulo=5,
    )

    write_report(
        puzzle_name="기책용팔도 (奇策用八圖)",
        analyses=analyses,
        global_symmetries=global_syms,
        save_path=str(OUTPUT_DIR / "rotation_report.txt"),
    )


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
