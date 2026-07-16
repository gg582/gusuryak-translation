"""최적해의 성질 분석 및 리포트 생성.

측정 결과를 JSON/Markdown으로 정리하며, 각 수치를 주석 OCR 구절 및
《漢書·律曆志》 六觚 기록과 대조한다.
"""

from __future__ import annotations

import json

from .hexgrid import PAIR_SUM, TOTAL_SUM, HexGrid
from .properties import PropertyReport, ring_target

# OCR 구절 ↔ 검증 수치 대조표
OCR_ANCHORS = [
    ("共積二百七十", "채워진 칸 270개", "270칸 (虛一로 중심 제외)"),
    ("虛一則二百七十數", "중심을 비우면 270수", "중심 칸 미사용"),
    ("校計周五十四數", "외주를 세면 54", "가장 바깥 고리 54칸"),
    ("通加洛書數六倍", "낙서수(1+..+9=45)의 6배 = 270", "총 칸 수 = 6×45"),
    ("十九爲中觔數也", "중앙 가로줄 19", "중觔(중심을 지나는 행) 19칸"),
    ("置外周添六", "바깥 고리에서 6씩 더해 감", "고리 k가 6k칸 (6,12,...,54)"),
    ("之數見甲編數器章", "수의 출전 표기", "값 1..270 (籌數略 체계)"),
]


def build_analysis(values: dict, grid: HexGrid, report: PropertyReport,
                   penalty_floor: float) -> dict:
    """분석 결과 전체를 JSON 직렬화 가능한 dict로 만든다."""
    corners = grid.corners()
    corner_vals = report.corner_values
    perimeter = [(c, values[c]) for c in grid.perimeter_walk()]
    ring_walk_values = {
        k: [values[c] for c in grid.ring_walk[k]]
        for k in range(1, grid.radius + 1)
    }
    pairs = sorted(
        (min(values[a], values[b]), max(values[a], values[b]))
        for a, b in grid.slots
    )
    mid_rows = {}
    for a in range(3):
        rows = grid.rows(a)
        mid_rows[a] = {
            "cells": len(rows[0]),
            "sum": sum(values.get(c, 0) for c in rows[0]),
        }
    return {
        "meta": {
            "filled_cells": len(values),
            "pair_sum": PAIR_SUM,
            "total_sum": sum(values.values()),
            "total_sum_target": TOTAL_SUM,
            "penalty": report.penalty,
            "penalty_floor": penalty_floor,
            "penalty_parts": report.parts,
        },
        "rings": {
            str(k): {"cells": 6 * k, "sum": report.ring_sums[k],
                     "target": ring_target(k)}
            for k in range(1, grid.radius + 1)
        },
        "sides": {"sums": report.side_sums, "target": 5 * PAIR_SUM},
        "wedges": {"sums": report.wedge_sums, "target": 45 * PAIR_SUM / 2},
        "rays": {"sums": report.ray_sums, "target": 9 * PAIR_SUM / 2},
        "axes": {"sums": report.axis_sums, "target": 9 * PAIR_SUM},
        "middle_rows_中觔": mid_rows,
        "corners": {
            "values": corner_vals,
            "mod9": [v % 9 for v in corner_vals],
            "mod6": [v % 6 for v in corner_vals],
            "note": "洛書 대조용: 꼭짓점 값의 9법·6법 잔여",
        },
        "pair_check": {
            "all_pairs_sum_271": all(a + b == PAIR_SUM for a, b in pairs),
            "n_pairs": len(pairs),
        },
        "perimeter_sequence": [v for _, v in perimeter],
        "ring_walk_sequences": {str(k): v for k, v in ring_walk_values.items()},
    }


def write_markdown(analysis: dict, report: PropertyReport,
                   path: str, solver_meta: dict) -> None:
    """성질 분석 리포트를 Markdown으로 저장한다."""
    m = analysis["meta"]
    lines: list[str] = []
    lines.append("# 落書六觚圖 복원 최적해 — 성질 분석\n")
    lines.append("## 1. 탐색 결과 요약\n")
    lines.append(f"- 시드: {solver_meta.get('seed')}, 재시작: {solver_meta.get('restarts')}회, "
                 f"재시작당 반복: {solver_meta.get('iterations'):,}회")
    lines.append(f"- 재시작별 페널티: {solver_meta.get('restart_penalties')}")
    lines.append(f"- 최종 페널티: **{m['penalty']}** (이론적 하한 {m['penalty_floor']})")
    lines.append(f"- 페널티 구성: {m['penalty_parts']}")
    lines.append("")
    lines.append("## 2. 주석 OCR 대조\n")
    lines.append("| 주석 구절 | 의미 | 복원 도안에서의 확인 |")
    lines.append("|---|---|---|")
    for phrase, meaning, check in OCR_ANCHORS:
        lines.append(f"| {phrase} | {meaning} | {check} |")
    lines.append("")
    lines.append("## 3. 기본 검증\n")
    lines.append(f"- 채워진 칸: {m['filled_cells']} (목표 270)")
    lines.append(f"- 전체 합: {m['total_sum']} (목표 {m['total_sum_target']})")
    lines.append(f"- 대점쌍(합 271) 전부 성립: {analysis['pair_check']['all_pairs_sum_271']} "
                 f"({analysis['pair_check']['n_pairs']}쌍)")
    lines.append("")
    lines.append("## 4. 구조별 합\n")
    lines.append("### 고리 (通加洛書數六倍)\n")
    lines.append("| 고리 k | 칸 수 6k | 합 | 목표 813k | 달성 |")
    lines.append("|---|---|---|---|---|")
    for k in range(1, 10):
        r = analysis["rings"][str(k)]
        ok = "✓" if r["sum"] == r["target"] else "✗"
        lines.append(f"| {k} | {r['cells']} | {r['sum']} | {r['target']} | {ok} |")
    lines.append("")
    s = analysis["sides"]
    lines.append(f"### 외주 6변 (목표 각 {s['target']})\n")
    lines.append(f"- 실측: {s['sums']}")
    lines.append("")
    w = analysis["wedges"]
    lines.append(f"### 6觚 섹터 (목표 각 {w['target']}, 이상적 분포 6097/6098)\n")
    lines.append(f"- 실측: {w['sums']}")
    lines.append("")
    ry = analysis["rays"]
    lines.append(f"### 6 광선 (목표 각 {ry['target']}, 이상적 분포 1219/1220)\n")
    lines.append(f"- 실측: {ry['sums']}")
    lines.append("")
    ax = analysis["axes"]
    lines.append(f"### 3축/中觔 (목표 각 {ax['target']})\n")
    lines.append(f"- 축 합 실측: {ax['sums']}")
    for a, mr in analysis["middle_rows_中觔"].items():
        lines.append(f"- 중觔(방향 {a}) {mr['cells']}칸, 합 {mr['sum']}")
    lines.append("")
    c = analysis["corners"]
    lines.append("## 5. 꼭짓점 값 (洛書 대조용)\n")
    lines.append(f"- 값: {c['values']}")
    lines.append(f"- mod 9: {c['mod9']}")
    lines.append(f"- mod 6: {c['mod6']}")
    lines.append("")
    lines.append("## 6. 외주 순회 수열 (알고리즘 패턴 검토용)\n")
    seq = analysis["perimeter_sequence"]
    lines.append(f"- 54수: {seq}")
    diffs = [(seq[(i + 1) % 54] - seq[i]) % 270 for i in range(54)]
    lines.append(f"- 인접 차분(시계, mod 270): {diffs}")
    lines.append("")
    lines.append("## 7. 해석 노트\n")
    lines.append("- 이 배치는 虛一·대점 보수쌍(합 271) 가설을 전제로 한 **탐색 최적해**이며,")
    lines.append("  주석의 승적법 절차를 그대로 따라한 것이 아니라 주석의 수치 조건을")
    lines.append("  만족하는 배치를 역산한 것이다.")
    lines.append("- 고리 합 813k, 축 합 2439, 대점쌍 271은 가설의 구조적 귀결이라 탐색 없이도 성립한다.")
    lines.append("- 변 1355, 섹터 6097/6098, 광선 1219/1220 균형은 탐색으로만 얻는 목표다.")
    lines.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def write_json(analysis: dict, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
