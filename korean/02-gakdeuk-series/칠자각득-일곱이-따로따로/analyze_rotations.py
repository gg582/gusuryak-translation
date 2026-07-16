#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
칠자각득(일곱이 따로따로) 군별 회전 분석.

5개 군(cluster) 각각은 중심값 + 6개 주변 슬롯으로 구성되며, 슬롯은
12시 방향부터 시계방향(SLOT_ANGLES)으로 배엸다. 각 군을 7-cycle로 보고
맞은편 합, mod 5 잉여 패턴, 군 내 회전 불변성, 전체 십자 배치의
회전 대칭성을 분석한다.
"""

import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

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

CLUSTER_SPACING = 3.3

CLUSTERS = [
    {"id": "C1", "dir": "상",  "pos": (0.0, CLUSTER_SPACING),  "center": 2,  "slots": [29, 1, 24, 34, 11, 19]},
    {"id": "C2", "dir": "좌",  "pos": (-CLUSTER_SPACING, 0.0), "center": 3,  "slots": [6, 33, 23, 13, 34, 8]},
    {"id": "C3", "dir": "중",  "pos": (0.0, 0.0),              "center": 5,  "slots": [22, 7, 20, 30, 26, 10]},
    {"id": "C4", "dir": "우",  "pos": (CLUSTER_SPACING, 0.0),  "center": 4,  "slots": [15, 28, 9, 18, 32, 14]},
    {"id": "C5", "dir": "하",  "pos": (0.0, -CLUSTER_SPACING), "center": 1,  "slots": [35, 16, 21, 24, 6, 17]},
]

OUTPUT_DIR = Path("figures")
OUTPUT_DIR.mkdir(exist_ok=True)


def main() -> None:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Noto Sans CJK KR", "Noto Sans CJK JP", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    analyses = []
    for cluster in CLUSTERS:
        cycle_values = [cluster["center"]] + cluster["slots"]
        analysis = analyze_cycle(cycle_values, modulo=5, name=cluster["id"])
        analysis.notes.append(f"중심={cluster['center']}, 방향={cluster['dir']}")
        analyses.append(analysis)

    centers = {c["id"]: c["pos"] for c in CLUSTERS}
    global_syms = find_global_rotation_symmetries(centers, candidates=[90, 180, 270])

    draw_individual_clusters(analyses, str(OUTPUT_DIR / "rotation_cluster"))
    draw_overview(
        analyses,
        global_title="칠자각득 — 5개 군의 회전 분석 (중심 + 6 슬롯)",
        save_path=str(OUTPUT_DIR / "rotation_overview.png"),
        ncols=3,
        modulo=5,
    )

    write_report(
        puzzle_name="칠자각득 (일곱이 따로따로)",
        analyses=analyses,
        global_symmetries=global_syms,
        save_path=str(OUTPUT_DIR / "rotation_report.txt"),
    )


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
