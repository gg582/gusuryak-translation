#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
낙서칠구도(洛書七九圖) 군별 회전 분석.

visualize_basic.py에 정의된 손상된 데이터와 chiljagakdeuk.md의 교정된
분할 두 가지를 모두 분석한다. 각 궁은 중심값 + 12시 방향부터 시계방향의
6개 주변값으로 구성된 7-cycle로 본다.
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
)

# 손상된 원본 데이터 (visualize_basic.py)
CORRUPTED_GROUPS = [
    {"center": 4, "surround": [31, 43, 22, 60, 27, 37], "pos": (1, 3)},
    {"center": 9, "surround": [15, 43, 38, 55, 10, 54], "pos": (2, 3)},
    {"center": 2, "surround": [28, 29, 39, 62, 17, 47], "pos": (3, 3)},
    {"center": 3, "surround": [30, 40, 26, 61, 16, 48], "pos": (1, 2)},
    {"center": 5, "surround": [32, 41, 23, 59, 14, 50], "pos": (2, 2)},
    {"center": 7, "surround": [34, 38, 24, 57, 20, 44], "pos": (3, 2)},
    {"center": 8, "surround": [35, 49, 12, 56, 11, 53], "pos": (1, 1)},
    {"center": 1, "surround": [52, 25, 19, 63, 18, 46], "pos": (2, 1)},
    {"center": 6, "surround": [33, 42, 21, 36, 13, 23], "pos": (3, 1)},
]

# chiljagakdeuk.md 의 교정된 9개 궁 (center: 7개 수)
CORRECTED_PALACES = {
    "upper_left": [4, 22, 27, 31, 37, 43, 60],
    "upper_center": [9, 10, 15, 36, 45, 54, 55],
    "upper_right": [2, 17, 28, 29, 39, 47, 62],
    "middle_left": [3, 16, 26, 30, 40, 48, 61],
    "center": [5, 14, 23, 32, 41, 50, 59],
    "middle_right": [7, 20, 24, 34, 38, 44, 57],
    "lower_left": [8, 11, 12, 35, 49, 53, 56],
    "lower_center": [1, 18, 19, 25, 46, 52, 63],
    "lower_right": [6, 13, 21, 33, 42, 51, 58],
}

PALACE_CENTERS_CORRECTED = {
    "upper_left": (1, 3),
    "upper_center": (2, 3),
    "upper_right": (3, 3),
    "middle_left": (1, 2),
    "center": (2, 2),
    "middle_right": (3, 2),
    "lower_left": (1, 1),
    "lower_center": (2, 1),
    "lower_right": (3, 1),
}

DISPLAY_LABELS = {
    "upper_left": "상좌(4)",
    "upper_center": "상중(9)",
    "upper_right": "상우(2)",
    "middle_left": "중좌(3)",
    "center": "중궁(5)",
    "middle_right": "중우(7)",
    "lower_left": "하좌(8)",
    "lower_center": "하중(1)",
    "lower_right": "하우(6)",
}

OUTPUT_DIR = Path(".")


CENTER_LABELS = {
    4: "상좌(4)", 9: "상중(9)", 2: "상우(2)",
    3: "중좌(3)", 5: "중궁(5)", 7: "중우(7)",
    8: "하좌(8)", 1: "하중(1)", 6: "하우(6)",
}


def analyze_dataset(groups_or_dict, title_prefix, out_prefix, centers):
    analyses = []
    if isinstance(groups_or_dict, list):
        for g in groups_or_dict:
            cycle = [g["center"]] + g["surround"]
            name = CENTER_LABELS[g["center"]]
            analysis = analyze_cycle(cycle, modulo=5, name=name)
            analysis.notes.append(f"sum = {sum(cycle)}; center mod 9 = {g['center'] % 9 or 9}")
            analyses.append(analysis)
    else:
        for name, cycle in groups_or_dict.items():
            analysis = analyze_cycle(cycle, modulo=5, name=DISPLAY_LABELS[name])
            analysis.notes.append(f"sum = {sum(cycle)}; center mod 9 = {cycle[0] % 9 or 9}")
            analyses.append(analysis)

    global_syms = find_global_rotation_symmetries(centers, candidates=[90, 180, 270])

    draw_individual_clusters(analyses, str(OUTPUT_DIR / f"{out_prefix}_cluster"))
    draw_overview(
        analyses,
        global_title=f"{title_prefix} — 9 palace rotations (center + 6 slots)",
        save_path=str(OUTPUT_DIR / f"{out_prefix}_overview.png"),
        ncols=3,
        modulo=5,
    )
    return analyses, global_syms


def format_section(puzzle_name, analyses, global_syms):
    lines = [
        "=" * 60,
        f"Per-cluster rotation analysis: {puzzle_name}",
        "=" * 60,
        "",
    ]
    for a in analyses:
        lines.append(f"Cluster: {a.name}")
        lines.append(f"  Cyclic order ({len(a.values)} elements): "
                     f"{' -> '.join(map(str, a.values))}")
        lines.append(f"  Sum: {a.sum_total}")
        lines.append(f"  Residue pattern (mod {a.modulo}): "
                     f"{'-'.join(str(r) for r in a.residue_pattern)}")
        if a.opposite_sums is not None:
            lines.append(f"  Opposite-pair sums: {a.opposite_sums}")
            if len(set(a.opposite_sums)) == 1:
                lines.append(f"    -> All opposite pairs sum to {a.opposite_sums[0]}")
        inv = a.rotation_invariants
        if len(inv) > 1:
            lines.append(f"  Invariant under nontrivial rotations by shifts: {inv[1:]}")
        else:
            lines.append("  No nontrivial rotational invariance.")
        for note in a.notes:
            lines.append(f"  Note: {note}")
        lines.append("")
    lines.append(f"Global rotational symmetry for {puzzle_name}")
    lines.append("-" * 50)
    if not global_syms:
        lines.append("No nontrivial global rotation maps clusters to clusters.")
    else:
        for angle in sorted(global_syms):
            mapping = global_syms[angle]
            lines.append(f"  {angle}° rotation:")
            for src, dst in mapping.items():
                marker = " (fixed)" if src == dst else ""
                lines.append(f"    {src} -> {dst}{marker}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Noto Sans CJK KR", "Noto Sans CJK JP", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    centers_corrupted = {f"center {g['center']}": g["pos"] for g in CORRUPTED_GROUPS}
    analyses_corr, syms_corr = analyze_dataset(
        CORRUPTED_GROUPS,
        "Nakseo Chilgudo (corrupted data)",
        "rotation_corrupted",
        centers_corrupted,
    )

    analyses_fix, syms_fix = analyze_dataset(
        CORRECTED_PALACES,
        "Nakseo Chilgudo (corrected partition)",
        "rotation_corrected",
        PALACE_CENTERS_CORRECTED,
    )

    report = (
        format_section("Nakseo Chilgudo — corrupted data", analyses_corr, syms_corr)
        + "\n"
        + format_section("Nakseo Chilgudo — corrected partition", analyses_fix, syms_fix)
    )

    report_path = OUTPUT_DIR / "rotation_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(report)


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
