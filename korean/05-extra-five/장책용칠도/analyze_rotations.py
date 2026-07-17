#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
장책용칠도 (章策用七圖) 회전 분석.

중심 7을 기준으로 한 세 개의 동심 고리(그래프 거리 d1, d2, d3)를 6-cycle로
분석한다. 각 고리는 12시 방향에 가장 가까운 위치에서 시작해 시계방향으로 읽는다.
세 축(각 7칸)은 환형이 아닌 선형이므로 참고용 나열로 함께 기록한다.
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

# visualize.py와 동일한 좌표 계산
AXES = {
    "수직축 90": [5, 18, 9, 7, 12, 2, 15],
    "대각축 150": [4, 10, 19, 7, 1, 14, 13],
    "대각축 30": [8, 6, 17, 7, 3, 11, 16],
}
AXIS_ANGLE = {"수직축 90": 90.0, "대각축 150": 150.0, "대각축 30": 30.0}

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
    """12시(90°)에 가장 가까운 위치부터 시계방향(각도 감소)으로 정렬."""
    return sorted(values, key=lambda v: (90.0 - _angle_of(v)) % 360.0)


# 중심으로부터의 거리에 따른 동심 고리
RINGS: dict[int, list[int]] = {1: [], 2: [], 3: []}
for node, (x, y) in POSITIONS.items():
    if node == CENTER:
        continue
    d = round(math.hypot(x, y) / SPACING)
    RINGS[d].append(node)

RING_NAMES = {1: "내륜 d1", 2: "중륜 d2", 3: "외륜 d3"}

OUTPUT_DIR = Path(".")


def main() -> None:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["NanumGothic", "Noto Sans CJK KR", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    analyses = []

    # 세 고리를 6-cycle로 분석 (순서는 실제 좌표의 방위각에서 계산)
    for d in [1, 2, 3]:
        cycle = clockwise_from_top(RINGS[d])
        analysis = analyze_cycle(cycle, modulo=5, name=RING_NAMES[d])
        analysis.notes.append(
            f"중심 7 기준 거리 {d}단계 고리; 반대편 쌍은 같은 축의 중심대칭 쌍"
        )
        analyses.append(analysis)

    # 세 축은 환형이 아닌 선형이므로 참고용 나열로 기록
    for axis_name, nodes in AXES.items():
        idx = nodes.index(CENTER)
        first, last = nodes[0], nodes[-1]
        # 12시에 가까운 끝에서 시작하도록 방향 확인
        if abs(_angle_of(first) - 90.0) > abs(_angle_of(last) - 90.0):
            nodes = list(reversed(nodes))
        analysis = analyze_cycle(nodes, modulo=5, name=axis_name)
        analysis.notes.append(
            "선형(비환형) 축: 12시에 가까운 끝에서 중심을 지나 반대 끝까지의 나열이며, "
            "환형이 아니므로 회전 불변 지표는 적용되지 않음"
        )
        analysis.notes.append(f"중심 칸 = {CENTER} (인덱스 {idx})")
        analyses.append(analysis)

    # 클러스터 중심(무게중심) 계산: 모든 고리와 축이 원점을 공유하는 동심 구조
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
        # 모든 무게중심이 원점에 일치하므로 전역 회전 대칭 판정이 퇴화한다.
        global_syms = {}
        note = (
            "동심(同心) 구조: 모든 클러스터 무게중심이 원점 (0,0)에 일치하여 "
            "전역 회전 대칭 판정이 퇴화하므로 생략함. 위치 배치 자체는 "
            "60° 회전 기하 대칭이나 수 배열은 회전 불변이 아님"
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
        global_title="장책용칠도 — 동심 고리(d1·d2·d3) 및 3축 회전 분석",
        save_path=str(OUTPUT_DIR / "rotation_overview.png"),
        ncols=3,
        modulo=5,
    )

    write_report(
        puzzle_name="장책용칠도 (章策用七圖)",
        analyses=analyses,
        global_symmetries=global_syms,
        save_path=str(OUTPUT_DIR / "rotation_report.txt"),
    )


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
