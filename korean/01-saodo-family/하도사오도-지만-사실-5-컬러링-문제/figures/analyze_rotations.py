#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
하도/사오도 5-컬러링 문제의 회전 분석.

20개 수를 mod 5 잉여(오행)별 5개 군으로 나누고, 십자 중심 주변에서
12시 방향부터 시계방향으로 각 군을 배열해 회전 분석한다. 기존
symmetry 분석에서 언급된 모든 숫자의 -30° 방향도 메모로 남긴다.
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

NODES = [
    {"pos": (-1, 3), "label": 19},
    {"pos": (0, 3),  "label": 2},
    {"pos": (-1, 2), "label": 7},
    {"pos": (0, 2),  "label": 14},
    {"pos": (-3, 1), "label": 13},
    {"pos": (-2, 1), "label": 8},
    {"pos": (-1, 1), "label": 5},
    {"pos": (0, 1),  "label": 16},
    {"pos": (1, 1),  "label": 4},
    {"pos": (2, 1),  "label": 17},
    {"pos": (-3, 0), "label": 18},
    {"pos": (-2, 0), "label": 3},
    {"pos": (-1, 0), "label": 11},
    {"pos": (0, 0),  "label": 10},
    {"pos": (1, 0),  "label": 12},
    {"pos": (2, 0),  "label": 9},
    {"pos": (-1, -1), "label": 15},
    {"pos": (0, -1),  "label": 1},
    {"pos": (-1, -2), "label": 6},
    {"pos": (0, -2),  "label": 20},
]

GROUP_KEYS = {
    1: "Water",
    2: "Fire",
    3: "Wood",
    4: "Metal",
    5: "Earth",
}

DISPLAY_LABELS = {
    "Water": "수",
    "Fire": "화",
    "Wood": "목",
    "Metal": "금",
    "Earth": "토",
}

OUTPUT_DIR = Path(".")


def group_of(n: int) -> int:
    g = n % 5
    return 5 if g == 0 else g


def main() -> None:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Noto Sans CJK KR", "Noto Sans CJK JP", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    groups: dict[int, list[tuple[int, tuple[int, int]]]] = {r: [] for r in range(1, 6)}
    for node in NODES:
        groups[group_of(node["label"])].append((node["label"], node["pos"]))

    analyses = []
    for r in range(1, 6):
        members = groups[r]

        def angle(item):
            _, (x, y) = item
            return math.degrees(math.atan2(y, x))

        sorted_members = sorted(members, key=angle, reverse=True)
        start_idx = min(range(len(sorted_members)),
                        key=lambda i: abs(angle(sorted_members[i]) - 90.0))
        ordered = [sorted_members[(start_idx + i) % len(sorted_members)][0]
                   for i in range(len(sorted_members))]

        analysis = analyze_cycle(ordered, modulo=5, name=DISPLAY_LABELS[GROUP_KEYS[r]])
        analysis.notes.append(f"십자 중심 주변 각도 순서로 {len(ordered)}개 노드 배열")
        analyses.append(analysis)

    centers = {node["label"]: node["pos"] for node in NODES}
    global_syms = find_global_rotation_symmetries(centers, candidates=[90, 180, 270])

    draw_individual_clusters(analyses, str(OUTPUT_DIR / "rotation_cluster"))
    draw_overview(
        analyses,
        global_title="하도/사오도 5-컬러링 — 오행 5군 회전 분석",
        save_path=str(OUTPUT_DIR / "rotation_overview.png"),
        ncols=3,
        modulo=5,
    )

    write_report(
        puzzle_name="하도/사오도 5-컬러링",
        analyses=analyses,
        global_symmetries=global_syms,
        save_path=str(OUTPUT_DIR / "rotation_report.txt"),
    )

    with open(OUTPUT_DIR / "rotation_report.txt", "a", encoding="utf-8") as f:
        f.write("\n숫자 방향 메모:\n")
        f.write("  모든 숫자는 약 θ = -30°(수평선에서 시계방향)로 기울어져 있다.\n")
        f.write("  이 균일한 기울기는 전체 도상 회전 하에 보존되지만,\n")
        f.write("  수 배치 자체는 비자명한 회전 대칭을 갖지 않는다.\n")


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
