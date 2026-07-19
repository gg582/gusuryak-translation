#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
중의용육도(重儀用六圖) 회전 분석.

분석 대상 순환 구조:
  · 외곽 12환: 좌상단 7에서 시작해 시계방향으로 도는 외곽 12개 값
  · 내측 4환: 내측 직사각형의 4개 값 (좌상단 11에서 시작, 시계방향)
  · 4개의 합-51 그룹: 도상에 환(環)으로 그려진 것은 아니지만,
    각 그룹의 6개 셀이 기하학적으로 볼록 다각형을 이루므로
    시계방향 기하 순서로 나열하여 분석에 포함한다 (메모 참조).
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

# visualize.py와 동일한 좌표
POSITIONS = {
    7: (-2.5, 3), 16: (-1, 3.2), 1: (1, 3.2), 6: (2.5, 3),
    13: (-3, 1.5), 11: (-1, 1), 10: (1, 1), 4: (3, 1.5),
    3: (-3, -1.5), 9: (-1, -1), 12: (1, -1), 14: (3, -1.5),
    8: (-2.5, -3), 2: (-1, -3.2), 15: (1, -3.2), 5: (2.5, -3),
}

# 합 51을 이루는 4개의 6자 그룹
GROUPS = {
    "상단 그룹": [7, 16, 1, 6, 11, 10],
    "좌측 그룹": [7, 13, 11, 3, 9, 8],
    "하단 그룹": [8, 2, 9, 12, 15, 5],
    "우측 그룹": [6, 10, 4, 12, 14, 5],
}

# 외곽 12환: 좌상단 7에서 시작, 시계방향
PERIMETER = [7, 16, 1, 6, 4, 14, 5, 15, 2, 8, 3, 13]

# 내측 4환: 좌상단 11에서 시작, 시계방향
INNER = [11, 10, 12, 9]

# 각 그룹의 6개 셀을 시계방향 기하 순서로 나열 (각 그룹의 좌상단 셀에서 시작)
GROUP_SEQ = {
    "상단 그룹": [16, 1, 6, 10, 11, 7],
    "좌측 그룹": [7, 11, 9, 8, 3, 13],
    "하단 그룹": [9, 12, 5, 15, 2, 8],
    "우측 그룹": [6, 4, 14, 5, 12, 10],
}

OUTPUT_DIR = Path(".")


def assert_clockwise(seq: list[int], name: str) -> None:
    """연속 세 점의 외적이 모두 0 이하인지 확인하여 시계방향(볼록) 순열임을 검증."""
    pts = [POSITIONS[v] for v in seq]
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        x3, y3 = pts[(i + 2) % n]
        cross = (x2 - x1) * (y3 - y2) - (y2 - y1) * (x3 - x2)
        if cross > 0:
            raise ValueError(f"{name}: 시계방향이 아닌 꼭짓점 발견 (index {i})")


def main() -> None:
    try:
        import matplotlib.font_manager as font_manager
        font_manager.fontManager.addfont(
            "/usr/share/fonts/naver-nanum-gothic-fonts/NanumGothic.ttf"
        )
    except Exception:
        pass
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = [
        "NanumGothic", "Noto Sans CJK KR", "Noto Sans CJK JP", "DejaVu Sans",
    ]
    plt.rcParams["axes.unicode_minus"] = False

    # 기하 순서 검증
    assert_clockwise(PERIMETER, "외곽 12환")
    assert_clockwise(INNER, "내측 4환")
    for name, seq in GROUP_SEQ.items():
        if sorted(seq) != sorted(GROUPS[name]):
            raise ValueError(f"{name} 나열이 그룹 구성과 다름: {seq}")
        assert_clockwise(seq, name)

    analyses = []

    perimeter_analysis = analyze_cycle(PERIMETER, modulo=5, name="외곽 12환")
    perimeter_analysis.notes.append("좌상단 7에서 시작해 시계방향. 대척합은 180° 회전 대응 쌍의 합.")
    analyses.append(perimeter_analysis)

    inner_analysis = analyze_cycle(INNER, modulo=5, name="내측 4환")
    inner_analysis.notes.append("내측 직사각형 (11,10,12,9), 좌상단 11에서 시작해 시계방향.")
    analyses.append(inner_analysis)

    for name, seq in GROUP_SEQ.items():
        analysis = analyze_cycle(seq, modulo=5, name=name)
        analysis.notes.append(
            "도상에 환으로 그려진 구조가 아니라, 6개 셀을 시계방향 기하 순서로 나열한 것 "
            f"(그룹 합 {sum(seq)} 검산용)."
        )
        analyses.append(analysis)

    # 전역 회전 대칭: 그룹 중심 = 멤버 좌표의 무게중심
    centers = {}
    for name, members in GROUPS.items():
        cx = sum(POSITIONS[v][0] for v in members) / len(members)
        cy = sum(POSITIONS[v][1] for v in members) / len(members)
        centers[name] = (round(cx, 6), round(cy, 6))
    global_syms = find_global_rotation_symmetries(centers, candidates=[180])

    draw_individual_clusters(analyses, str(OUTPUT_DIR / "rotation_cluster"))
    draw_overview(
        analyses,
        global_title="중의용육도 — 외곽 12환 · 내측 4환 · 4개 그룹 회전 분석",
        save_path=str(OUTPUT_DIR / "rotation_overview.png"),
        ncols=3,
        modulo=5,
    )

    write_report(
        puzzle_name="중의용육도 (重儀用六圖)",
        analyses=analyses,
        global_symmetries=global_syms,
        save_path=str(OUTPUT_DIR / "rotation_report.txt"),
    )


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
