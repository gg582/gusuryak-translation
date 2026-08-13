#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
오자각득(천수용오도) 배치 2 회전 분석.

원본 배치(analyze_rotations.py)와 모양은 동일하되 수 배치가 다른 변형(1~21).
원본 도상에는 명시적인 간선이나 궁 사이클이 없으므로, mod 5 잉여 클래스를
하나의 군으로 보고 각 수의 각도를 이용해 12시 방향부터 시계방향으로 배열해
회전 분석을 수행한다. 전역 회전 대칭성도 함께 검사한다.
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

POSITIONS = {
    12: (0.0, 6.0),
    17: (-1.5, 5.0),
    18: (1.5, 5.0),
    5:  (0.0, 4.2),
    13: (-2.8, 3.3),
    2:  (0.0, 3.3),
    19: (2.8, 3.3),
    7:  (-4.2, 2.0),
    3:  (-2.8, 2.0),
    20: (-1.4, 2.0),
    15: (0.0, 2.0),
    9:  (1.4, 2.0),
    4:  (2.8, 2.0),
    8:  (4.2, 2.0),
    11: (-2.8, 0.8),
    6:  (0.0, 0.8),
    14: (2.8, 0.8),
    10: (-1.8, -0.4),
    1:  (0.0, -0.4),
    21: (1.8, -0.4),
    16: (0.0, -1.7),
}

GROUPS = {
    1: [1, 6, 11, 16, 21],
    2: [2, 7, 12, 17],
    3: [3, 8, 13, 18],
    4: [4, 9, 14, 19],
    0: [5, 10, 15, 20],
}

RESIDUE_KEYS = {
    1: "Water",
    2: "Fire",
    3: "Wood",
    4: "Metal",
    0: "Earth",
}

DISPLAY_LABELS = {
    "Water": "수 (r=1)",
    "Fire": "화 (r=2)",
    "Wood": "목 (r=3)",
    "Metal": "금 (r=4)",
    "Earth": "토 (r=5)",
}

OUTPUT_DIR = Path(".")


def main() -> None:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Noto Sans CJK KR", "Noto Sans CJK JP", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    cx, cy = 0.0, 2.0

    def angle_of(v: int) -> float:
        x, y = POSITIONS[v]
        return math.degrees(math.atan2(y - cy, x - cx))

    analyses = []
    for r in [1, 2, 3, 4, 0]:
        members = sorted(GROUPS[r], key=lambda v: angle_of(v), reverse=True)
        start_idx = min(range(len(members)), key=lambda i: abs(angle_of(members[i]) - 90.0))
        ordered = [members[(start_idx + i) % len(members)] for i in range(len(members))]
        analysis = analyze_cycle(ordered, modulo=5, name=DISPLAY_LABELS[RESIDUE_KEYS[r]])
        analysis.notes.append("잉여 클래스를 각도 순서로 배열; 원본에 고유 사이클은 없음.")
        analyses.append(analysis)

    centers = {v: (x, y) for v, (x, y) in POSITIONS.items()}
    global_syms = find_global_rotation_symmetries(centers, candidates=[180], tolerance=1e-5)

    # 클러스터별 이미지: 임시 접두사로 생성 후 _2 접미사로 변경
    tmp_prefix = str(OUTPUT_DIR / "rotation_cluster_tmp2")
    draw_individual_clusters(analyses, tmp_prefix)
    for tmp_path in sorted(OUTPUT_DIR.glob("rotation_cluster_tmp2_*.png")):
        final_name = tmp_path.name.replace("rotation_cluster_tmp2_", "rotation_cluster_", 1)
        final_name = final_name[:-4] + "_2.png"
        tmp_path.rename(OUTPUT_DIR / final_name)
        print(f"Renamed cluster: {final_name}")

    draw_overview(
        analyses,
        global_title="오자각득 배치 2 — 잉여 클래스 회전 분석 (원본 궁 사이클 없음)",
        save_path=str(OUTPUT_DIR / "rotation_overview_2.png"),
        ncols=3,
        modulo=5,
    )

    write_report(
        puzzle_name="오자각득 배치 2 (五子各得 / 천수용오도, 1~21)",
        analyses=analyses,
        global_symmetries=global_syms,
        save_path=str(OUTPUT_DIR / "rotation_report_2.txt"),
    )


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
