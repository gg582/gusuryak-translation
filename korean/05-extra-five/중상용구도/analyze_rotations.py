#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
중상용구도 고리·축 회전 분석.

중심 9를 공유하는 4개 축 위에서, 중심으로부터의 그래프 거리가 같은 8개 노드가
동심 팔각형 고리(d1–d4)를 이룬다. 각 고리를 12시 방향부터 시계방향으로 읽은
8-cycle로 분석한다. 4개 직선 축은 비순환 선형 클러스터로, 참조용 열과 함께 기록한다.
모든 클러스터의 무게중심이 원점에 겹치는 동심 구조이므로 전체 회전 대칭 검사는
퇴화(degenerate)하여 생략하고 그 이유를 보고서에 남긴다.
"""

import math
import os
import sys
from pathlib import Path

import matplotlib.font_manager as fm
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

# 좌표는 이 디렉토리의 visualize.py 및 analyze_jungsang_yonggudo.py와 동일하다.
COORDS = {
    27: (-4, 4), 20: (0, 4), 33: (4, 4),
    15: (-2, 3), 16: (0, 3), 1: (2, 3),
    3: (-1.5, 2), 23: (0, 2), 13: (1.5, 2),
    24: (-1, 1), 10: (0, 1), 22: (1, 1),
    28: (-4, 0), 5: (-3, 0), 11: (-2, 0), 25: (-1, 0), 9: (0, 0),
    7: (1, 0), 19: (2, 0), 31: (3, 0), 12: (4, 0),
    18: (-1, -1), 2: (0, -1), 30: (1, -1),
    26: (-1.5, -2), 29: (0, -2), 14: (1.5, -2),
    17: (-2, -3), 32: (0, -3), 21: (2, -3),
    8: (-4, -4), 6: (0, -4), 4: (4, -4),
}

CENTER = 9

AXES = {
    "vertical": [20, 16, 23, 10, 9, 2, 29, 32, 6],
    "horizontal": [28, 5, 11, 25, 9, 7, 19, 31, 12],
    "diagonal1": [27, 15, 3, 24, 9, 30, 14, 21, 4],
    "diagonal2": [33, 1, 13, 22, 9, 18, 26, 17, 8],
}

DISPLAY_LABELS = {
    "vertical": "세로축",
    "horizontal": "가로축",
    "diagonal1": "대각축1",
    "diagonal2": "대각축2",
}

OUTPUT_DIR = Path(".")

DEGENERATE_NOTE = """전체 회전 대칭 (참고: 동심 구조로 인한 퇴화)
--------------------------------------------------
모든 클러스터(4개 고리 + 4개 축)의 무게중심이 원점 (0, 0)에 정확히 겹치는
동심(concentric) 배치다. 원점에 대한 임의의 회전이 모든 클러스터 중심을 제자리에
두므로, 클러스터 간 치환으로 정의되는 전체 회전 대칭은 퇴화(degenerate)한다.
따라서 find_global_rotation_symmetries 검사는 생략하고 이 사실만 기록한다.
(고리 자체의 회전 성질은 위의 각 8-cycle 분석을 참조.)
"""


def _setup_fonts() -> None:
    try:
        fm.fontManager.addfont("/usr/share/fonts/naver-nanum-gothic-fonts/NanumGothic.ttf")
    except Exception:
        pass
    preferred = ["NanumGothic", "Noto Sans CJK KR", "Noto Sans CJK JP", "Malgun Gothic"]
    available = {f.name for f in fm.fontManager.ttflist}
    selected = [name for name in preferred if name in available]
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = selected + ["DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False


def clockwise_from_top(values: list[int]) -> list[int]:
    """좌표의 방위각으로 정렬해 12시 방향 시작·시계방향 순환열을 만든다."""
    return sorted(
        values,
        key=lambda v: math.atan2(COORDS[v][0], COORDS[v][1]) % (2 * math.pi),
    )


def build_rings() -> dict[str, list[int]]:
    """중심으로부터의 축상 거리(= 그래프 거리)가 같은 노드끼리 고리를 구성."""
    rings: dict[str, list[int]] = {f"d{d}": [] for d in range(1, 5)}
    for axis in AXES.values():
        center_idx = axis.index(CENTER)
        for i, value in enumerate(axis):
            if value == CENTER:
                continue
            rings[f"d{abs(i - center_idx)}"].append(value)
    return rings


def centroid(members: list[int]) -> tuple[float, float]:
    xs = [COORDS[v][0] for v in members]
    ys = [COORDS[v][1] for v in members]
    return (sum(xs) / len(xs), sum(ys) / len(ys))


def main() -> None:
    _setup_fonts()

    rings = build_rings()
    analyses = []

    # 4개 동심 팔각형 고리: 8-cycle (12시 시작, 시계방향).
    for d in range(1, 5):
        name = f"d{d}고리"
        cycle = clockwise_from_top(rings[f"d{d}"])
        analysis = analyze_cycle(cycle, modulo=5, name=name)
        analysis.notes.append(f"중심 {CENTER}로부터 그래프 거리 {d}의 동심 팔각형 고리")
        analysis.notes.append(
            f"고리 합 138 = (561-9)/4; 중심 {CENTER}를 더하면 147 "
            "(원문 '주위사중 각득 147'와 정합)"
        )
        analyses.append(analysis)

    # 4개 직선 축: 비순환 선형 클러스터 (참조용 열).
    for key, axis in AXES.items():
        analysis = analyze_cycle(axis, modulo=5, name=DISPLAY_LABELS[key])
        analysis.notes.append("비순환 선형 클러스터(직선 축) — 회전 주기 해석은 고리에만 해당")
        analysis.notes.append("홀수 길이(9)이므로 대향 합은 생략됨")
        analysis.notes.append(f"합 147 = 69+{CENTER}+69 (광선+중심+광선)")
        analyses.append(analysis)

    # 전체 회전 대칭: 모든 무게중심이 원점에 겹치는 동심 구조인지 확인.
    members = {f"d{d}고리": rings[f"d{d}"] for d in range(1, 5)}
    members.update({DISPLAY_LABELS[k]: v for k, v in AXES.items()})
    centers = {name: centroid(vals) for name, vals in members.items()}
    max_radius = max(math.hypot(x, y) for x, y in centers.values())
    if max_radius < 1e-9:
        # 퇴화: 전체 회전 대칭 검사 생략, 보고서에 사유 기록.
        global_syms: dict[float, dict] = {}
        degenerate = True
    else:
        global_syms = find_global_rotation_symmetries(centers, candidates=[45, 90, 135, 180, 225, 270, 315])
        degenerate = False

    draw_individual_clusters(analyses, str(OUTPUT_DIR / "rotation_cluster"))
    draw_overview(
        analyses,
        global_title="중상용구도 — 4개 동심 고리(8-cycle) + 4개 축 회전 분석",
        save_path=str(OUTPUT_DIR / "rotation_overview.png"),
        ncols=3,
        modulo=5,
    )

    report_path = OUTPUT_DIR / "rotation_report.txt"
    write_report(
        puzzle_name="중상용구도 (象上用九圖)",
        analyses=analyses,
        global_symmetries=global_syms,
        save_path=str(report_path),
    )
    if degenerate:
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("\n" + DEGENERATE_NOTE)
        print(DEGENERATE_NOTE)


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
