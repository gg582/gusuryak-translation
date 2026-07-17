#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
범수용오도 고리·축 회전 분석.

두 개의 동심 4-cycle(내륜·외륜)을 12시 방향부터 시계방향으로 읽고,
두 축(가로·세로)은 순환이 아닌 선형 5자 수열로서 메모와 함께 포함한다.
모든 클러스터의 무게중심이 원점으로 일치하는 동심(concentric) 구조이므로
전역 회전 대칭 검사는 퇴화(degenerate)하여 생략하고 그 사유를 기록한다.
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

# visualize.py의 정방향 좌표.
POSITIONS = {
    3: (-2, 0), 7: (-1, 0), 5: (0, 0), 4: (1, 0), 6: (2, 0),
    2: (0, 2), 8: (0, 1), 1: (0, -1), 9: (0, -2),
}

# 12시 방향에서 시작하여 시계방향으로 읽은 순환 열.
INNER_RING = [8, 4, 1, 7]   # 내륜(중간점) 4-cycle
OUTER_RING = [2, 6, 9, 3]   # 외륜(끝점) 4-cycle

# 순환이 아닌 선형 축 (기하학적 읽기 순서만 사용).
HORIZONTAL = [3, 7, 5, 4, 6]  # 왼쪽 → 오른쪽
VERTICAL = [2, 8, 5, 1, 9]    # 위 → 아래

OUTPUT_DIR = Path(".")


def centroid(values: list[int]) -> tuple[float, float]:
    xs = [POSITIONS[v][0] for v in values]
    ys = [POSITIONS[v][1] for v in values]
    return (sum(xs) / len(xs), sum(ys) / len(ys))


def main() -> None:
    # 한글 폰트 부트스트랩
    try:
        import matplotlib.font_manager as fm
        fm.fontManager.addfont("/usr/share/fonts/naver-nanum-gothic-fonts/NanumGothic.ttf")
    except Exception:
        pass
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = [
        "NanumGothic", "Noto Sans CJK KR", "Noto Sans CJK JP",
        "Malgun Gothic", "DejaVu Sans",
    ]
    plt.rcParams["axes.unicode_minus"] = False

    analyses = []

    inner = analyze_cycle(INNER_RING, modulo=5, name="내륜 4-cycle")
    inner.notes.append("중심 5는 고리에 포함되지 않음 (별도 1자)")
    inner.notes.append("대향 쌍 합이 9와 11로 갈라짐 — 두 쌍의 합 20 = 고리 전체 합")
    inner.notes.append("잔여 패턴이 수·화·목·금(1,2,3,4)을 정확히 한 번씩 포함")
    analyses.append(inner)

    outer = analyze_cycle(OUTER_RING, modulo=5, name="외륜 4-cycle")
    outer.notes.append("대향 쌍 합이 11과 9 — 내륜과 교차 (가로: 외륜 9·내륜 11, 세로: 외륜 11·내륜 9)")
    outer.notes.append("잔여 패턴이 수·화·목·금(1,2,3,4)을 정확히 한 번씩 포함")
    analyses.append(outer)

    horiz = analyze_cycle(HORIZONTAL, modulo=5, name="가로축 5자 수열")
    horiz.notes.append("순환 고리가 아닌 선형 축 — 왼쪽→오른쪽 읽기 순서")
    horiz.notes.append("홀수 길이 5이므로 대향 쌍 합은 정의되지 않음")
    horiz.notes.append("잔여열 3-2-5-4-1 = 상생 순환 목→화→토→금→수 (모든 이웃 관계가 상생)")
    analyses.append(horiz)

    vert = analyze_cycle(VERTICAL, modulo=5, name="세로축 5자 수열")
    vert.notes.append("순환 고리가 아닌 선형 축 — 위→아래 읽기 순서")
    vert.notes.append("홀수 길이 5이므로 대향 쌍 합은 정의되지 않음")
    vert.notes.append("중심에 인접한 두 엣지(8-5, 5-1)가 상극 관계")
    analyses.append(vert)

    # 전역 회전 대칭: 클러스터 중심(무게중심)이 모두 원점으로 일치하는지 확인.
    centers = {
        "inner_ring": centroid(INNER_RING),
        "outer_ring": centroid(OUTER_RING),
        "horizontal_axis": centroid(HORIZONTAL),
        "vertical_axis": centroid(VERTICAL),
    }
    distinct = set(centers.values())
    global_syms: dict = {}
    degenerate_note = None
    if len(distinct) == 1:
        only = next(iter(distinct))
        degenerate_note = (
            f"모든 클러스터의 무게중심이 {only} 한 점으로 일치하는 동심(concentric) 구조입니다.\n"
            "클러스터 중심을 서로 옮기는 전역 회전 대칭은 정의되지 않으므로(퇴화) 검사를 생략합니다.\n"
            "기하학적으로는 90° 회전이 십자 도형 자체를 보존하지만, 수 배치(레이블)는 보존하지 않습니다."
        )
    else:
        global_syms = find_global_rotation_symmetries(centers, candidates=[90, 180, 270])

    draw_individual_clusters(analyses, str(OUTPUT_DIR / "rotation_cluster"))
    draw_overview(
        analyses,
        global_title="범수용오도 — 내륜·외륜·두 축 회전 분석 (mod 5)",
        save_path=str(OUTPUT_DIR / "rotation_overview.png"),
        ncols=2,
        modulo=5,
    )

    report_path = str(OUTPUT_DIR / "rotation_report.txt")
    write_report(
        puzzle_name="범수용오도 (範數用五圖)",
        analyses=analyses,
        global_symmetries=global_syms,
        save_path=report_path,
    )
    if degenerate_note:
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("\nNOTE (concentric layout):\n" + degenerate_note + "\n")
        print("NOTE (concentric layout):")
        print(degenerate_note)


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
