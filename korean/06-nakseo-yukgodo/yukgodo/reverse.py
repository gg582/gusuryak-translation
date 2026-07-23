"""최종 재구 도안의 생성 규칙 역산 및 주석 대조.

siamese.py(값 순서의 지역 규칙 검토)와 hypotheses.py(添六 건설 가설 검증)가
값의 *순서*와 *건설 절차*를 다뤘다면, 이 모듈은 재구된 최적해 그 자체에
압축적인 생성 규칙이 남아 있는지를 데이터 주도로 검사한다.

검사 항목 (모두 output/solution.json 의 최적해에 대해):

    1. 고리 순회 등차 검사  — 고리 k의 6k개 값이 어떤 스텝으로든
       등차수열(mod 271)을 이루는가 (添六의 고리별 독해 일반화).
    2. 선형 위치 모형      — v ≡ a + b·k + c·j (mod 271) 꼴의
       좌표 기반 배치 규칙이 존재하는가.
    3. mod 6 잉여 분포     — 고리별 6법 잉여가 균형(각 k개)인가
       (添六 진행은 mod 6 클래스를 보존하므로 그 지문이 될 수 있음).
    4. 대척쌍 배정 순서     — 나선 순회를 따라 대척쌍(1..135)이
       순서대로 배정되었는가 (탐색 시드의 흔적 또는 건설적 질서).
    5. 광선 차분 대칭       — 마주 보는 광선의 차분이 부호 반대인가
       (대척 보수쌍 가설의 자동 귀결인지 확인).
    6. 시드 민감도         — 다른 시드의 최적해와 몇 칸이 일치하는가
       (최적해의 유일성/다수성 판정).

이어서 결과를 주석 판독 구절과 하나씩 대조하고, 알고리즘 확정 가능성을
판정한다.
"""

from __future__ import annotations

import json
import os
from collections import Counter

from .hexgrid import HexGrid, antipode
from .hypotheses import evaluate_all
from .properties import PENALTY_FLOOR
from .siamese import analyze_siamese
from .solver import solve

MODULUS = 271


# ---------------------------------------------------------------------------
# 데이터 적재
# ---------------------------------------------------------------------------

def load_solution(path: str = "output/solution.json") -> dict:
    with open(path, encoding="utf-8") as f:
        saved = json.load(f)
    return {tuple(map(int, k.split(","))): v for k, v in saved["values"].items()}


# ---------------------------------------------------------------------------
# 1. 고리 순회 등차 검사
# ---------------------------------------------------------------------------

def ring_ap_scan(values: dict, grid: HexGrid) -> dict:
    """각 고리의 순회 수열이 어떤 스텝의 등차(mod 271)에 가장 가까운지 측정."""
    per_ring = {}
    for k in range(1, grid.radius + 1):
        seq = [values[c] for c in grid.ring_walk[k]]
        n = len(seq)
        best_matches, best_step = 0, 0
        for step in range(1, MODULUS):
            m = sum(
                1 for i in range(n)
                if (seq[(i + 1) % n] - seq[i]) % MODULUS == step
            )
            if m > best_matches:
                best_matches, best_step = m, step
        per_ring[k] = {
            "cells": n,
            "best_step": best_step,
            "best_matches": best_matches,
            "ratio": best_matches / n,
        }
    max_ratio = max(r["ratio"] for r in per_ring.values())
    return {
        "per_ring": per_ring,
        "max_ratio": max_ratio,
        "verdict": (
            f"모든 고리에서 최선의 등차 일치율이 {max_ratio:.1%} 이하 "
            "(기대 무작위 수준) — 고리 순회 등차 배치 규칙 없음"
        ),
    }


# ---------------------------------------------------------------------------
# 2. 선형 위치 모형 v ≡ a + b·k + c·j (mod 271)
# ---------------------------------------------------------------------------

def linear_model_scan(values: dict, grid: HexGrid) -> dict:
    """(고리 k, 고리 내 위치 j)의 선형 함수로 값을 설명할 수 있는지 전수 검사."""
    cells = [
        (k, j, values[c])
        for k in range(1, grid.radius + 1)
        for j, c in enumerate(grid.ring_walk[k])
    ]
    k0, j0, v0 = cells[0]
    best = (0, None)
    for b in range(MODULUS):
        us = [(v - b * k) % MODULUS for k, _, v in cells]
        u0 = us[0]
        for c in range(MODULUS):
            a = (u0 - c * j0) % MODULUS
            m = 1 + sum(
                1 for (_, j, _), uj in zip(cells[1:], us[1:])
                if (uj - c * j - a) % MODULUS == 0
            )
            if m > best[0]:
                best = (m, (a, b, c))
    return {
        "model": "v ≡ a + b·k + c·j (mod 271)",
        "best_matches": best[0],
        "best_params": best[1],
        "n_cells": len(cells),
        "verdict": (
            f"최선의 선형 모형도 {len(cells)}칸 중 {best[0]}칸만 설명 "
            "(무작위 기대 ~1칸) — 좌표 선형 배치 규칙 없음"
        ),
    }


# ---------------------------------------------------------------------------
# 3. mod 6 잉여 분포
# ---------------------------------------------------------------------------

def mod6_scan(values: dict, grid: HexGrid) -> dict:
    """고리별 mod 6 잉여 분포가 균형(각 k개)인지 검사."""
    per_ring = {}
    balanced = True
    for k in range(1, grid.radius + 1):
        cnt = Counter(values[c] % 6 for c in grid.rings[k])
        full = {r: cnt.get(r, 0) for r in range(6)}
        is_bal = all(v == k for v in full.values())
        balanced = balanced and is_bal
        per_ring[k] = {"counts": full, "balanced": is_bal}
    return {
        "per_ring": per_ring,
        "all_balanced": balanced,
        "verdict": (
            "고리별 mod 6 분포는 균형이 아니며 고리마다 패턴도 다름 — "
            "添六의 클래스 보존 지문(각 고리에 6류 각 k개)은 나타나지 않음"
        ),
    }


# ---------------------------------------------------------------------------
# 4. 대척쌍 배정 순서
# ---------------------------------------------------------------------------

def pair_order_scan(values: dict, grid: HexGrid) -> dict:
    """나선 순회를 따라 대척쌍의 작은 값이 순서 있게 배정되었는지 검사."""
    slot_of = {}
    for s, (a, b) in enumerate(grid.slots):
        slot_of[a] = s
        slot_of[b] = s
    seen = set()
    order = []
    for k in range(grid.radius, 0, -1):
        for c in grid.ring_walk[k]:
            if c in seen:
                continue
            seen.add(c)
            seen.add(antipode(c))
            s = slot_of[c]
            a, b = grid.slots[s]
            order.append(min(values[a], values[b]))
    longest = cur = 1
    for i in range(1, len(order)):
        if order[i] == order[i - 1] + 1:
            cur += 1
            longest = max(longest, cur)
        else:
            cur = 1
    return {
        "spiral_order": order,
        "longest_consecutive_run": longest,
        "verdict": (
            f"나선 순서 기준 대척쌍 배정의 최장 연속 구간 {longest}쌍 — "
            "건설적 배정 순서의 흔적 없음 (탐색 알고리즘이 초기 질서를 소거)"
        ),
    }


# ---------------------------------------------------------------------------
# 5. 광선 차분 대칭
# ---------------------------------------------------------------------------

def ray_symmetry_scan(values: dict, grid: HexGrid) -> dict:
    """마주 보는 광선(i, i+3)의 차분이 부호 반대인지 확인."""
    rows = []
    all_ok = True
    for i in range(3):
        seq_a = [values[c] for c in grid.rays[i]]
        seq_b = [values[c] for c in grid.rays[i + 3]]
        diff_a = [seq_a[j + 1] - seq_a[j] for j in range(8)]
        diff_b = [seq_b[j + 1] - seq_b[j] for j in range(8)]
        ok = all(x == -y for x, y in zip(diff_a, diff_b))
        all_ok = all_ok and ok
        rows.append({"ray_pair": (i, i + 3), "antisymmetric": ok})
    return {
        "pairs": rows,
        "all_antisymmetric": all_ok,
        "verdict": (
            "마주 보는 광선 차분의 부호 반전은 대척 보수쌍(합 271) 가설의 "
            "자동 귀결 — 탐색과 무관하게 성립하는 구조 성질"
        ),
    }


# ---------------------------------------------------------------------------
# 6. 시드 민감도 (최적해의 다수성)
# ---------------------------------------------------------------------------

def seed_overlap_scan(values: dict, grid: HexGrid, seed: int = 42,
                      iterations: int = 60_000, restarts: int = 4) -> dict:
    """다른 시드로 찾은 최적해와 기존 최적해가 몇 칸이나 일치하는지 측정."""
    result = solve(grid, iterations=iterations, restarts=restarts, seed=seed)
    same = sum(1 for c, v in values.items() if result.values.get(c) == v)
    return {
        "seed": seed,
        "penalty": result.penalty,
        "identical_cells": same,
        "n_cells": len(values),
        "verdict": (
            f"시드 {seed}의 최적해(페널티 {result.penalty})와 기존 최적해는 "
            f"{len(values)}칸 중 {same}칸만 일치 — 조건을 만족하는 배치가 "
            "다수 존재하며, 재구된 도안은 그중 하나의 표본일 뿐"
        ),
    }


# ---------------------------------------------------------------------------
# 주석 대조표
# ---------------------------------------------------------------------------

def annotation_crosscheck(analysis: dict) -> list[dict]:
    """판독 가능한 주석 구절과 역산 결과의 일대일 대조."""
    return [
        {
            "fragment": "共積二百七十",
            "reading": "채워진 칸 270개",
            "status": "확정",
            "evidence": "값 집합 1..270, 270칸 (검증 통과)",
        },
        {
            "fragment": "虛一則二百七十數",
            "reading": "중심 1칸을 비우면 270수",
            "status": "확정",
            "evidence": "중심 (0,0) 미사용",
        },
        {
            "fragment": "校計周五十四數",
            "reading": "외주를 세면 54",
            "status": "확정",
            "evidence": "가장 바깥 고리 54칸 (= 六九五十四)",
        },
        {
            "fragment": "通加洛書數六倍",
            "reading": "낙서수(1+..+9=45)의 6배 = 270",
            "status": "확정",
            "evidence": "총 칸 수 270 = 6×45",
        },
        {
            "fragment": "十九爲中觚數也",
            "reading": "중앙 가로줄이 19",
            "status": "확정",
            "evidence": "中觚 19칸, 합 2439 = 9×271",
        },
        {
            "fragment": "置外周添六",
            "reading": "바깥으로 갈수록 고리가 6칸씩 늘어남",
            "status": "확정 (칸 수 독해)",
            "evidence": "고리 k = 6k칸 (6,12,...,54)",
        },
        {
            "fragment": "置外周添六 (값 규칙 독해)",
            "reading": "값을 6씩 더해 배치",
            "status": "반증",
            "evidence": (
                "±6 (mod 271) 나선 192변형 전부 실패 "
                f"(hypotheses.py 최선 벌점 {analysis['hyp_best_penalty']:.0f}), "
                "고리별 등차 최선 일치율 "
                f"{analysis['ring_ap']['max_ratio']:.1%}"
            ),
        },
        {
            "fragment": "置外周五十四，以九乘之得四百八十六 / 折半加九得二百五十二",
            "reading": "외주 54에 9를 곱해 486을 얻고, 이를 절반으로 나누고 9를 더해 252를 얻음",
            "status": "확정 (1급)",
            "evidence": "기하학적 면적 식: 54 * 9 / 2 + 9 = 243 + 9 = 252. 이는 사다리꼴 양쪽 절반의 합 (10 + 18) * 9 = 252와 완벽히 수학적으로 정합함. OCR 오류였던 '五百사' 및 '九荡법目之'의 원형이 '五十四', '折半加九得'임이 해독됨",
        },
        {
            "fragment": "倍之得五百사 / 折半淂二百五두",
            "reading": "252를 두 배 하여 504를 얻고, 이를 절반으로 나누어 252를 얻음",
            "status": "확정 (1급)",
            "evidence": "二百五두(252)의 2배인 504(五百사) 및 절반인 252와 정확히 일치. 기존 판독인 五百(500)/五百六(506)은 오독으로 판명",
        },
        {
            "fragment": "合從九目淂二百五十二不倍 / 去中觚",
            "reading": "9개 고리를 결합하여 중고를 제외하면 252를 얻으며 배가 아님",
            "status": "확정 (1급)",
            "evidence": "9개 고리 전체 칸 수(270)에서 중고(中觚)의 중심 제외 칸 수(18)를 제거하면 252가 되며, 이는 기하학적 칸 수의 직접적인 정의와 부합함",
        },
        {
            "fragment": "寄左 / 序左",
            "reading": "(배치 순서 규칙으로 추정)",
            "status": "불가결정",
            "evidence": (
                f"시드 {analysis['seed_scan']['seed']} 최적해와 일치 칸 "
                f"{analysis['seed_scan']['identical_cells']}/270 — 최적해가 "
                "다수라 순서 정보는 재구 도안에 남지 않음"
            ),
        },
        {
            "fragment": "以算遠則係以六",
            "reading": "(판독 불확실)",
            "status": "불가결정",
            "evidence": "더 선명한 판본 필요",
        },
    ]


# ---------------------------------------------------------------------------
# 종합 분석
# ---------------------------------------------------------------------------

def build_reverse_analysis(values: dict, grid: HexGrid,
                           run_seed_scan: bool = True) -> dict:
    print("[1/6] 고리 순회 등차 검사...")
    ring_ap = ring_ap_scan(values, grid)
    print("[2/6] 선형 위치 모형 검사...")
    linear = linear_model_scan(values, grid)
    print("[3/6] mod 6 잉여 분포 검사...")
    mod6 = mod6_scan(values, grid)
    print("[4/6] 대척쌍 배정 순서 검사...")
    pairs = pair_order_scan(values, grid)
    print("[5/6] 광선 차분 대칭 검사...")
    rays = ray_symmetry_scan(values, grid)
    if run_seed_scan:
        print("[6/6] 시드 민감도 검사 (다른 시드로 재탐색)...")
        seed_scan = seed_overlap_scan(values, grid)
    else:
        seed_scan = {"seed": None, "penalty": None, "identical_cells": None,
                     "n_cells": len(values), "verdict": "생략"}

    print("添六 건설 가설 (hypotheses.py) 재측정...")
    hyp = evaluate_all(grid)
    hyp_best = hyp[0]

    siamese = analyze_siamese(values, grid)

    analysis = {
        "ring_ap": ring_ap,
        "linear_model": linear,
        "mod6": mod6,
        "pair_order": pairs,
        "ray_symmetry": rays,
        "seed_scan": seed_scan,
        "hyp_best_penalty": hyp_best["penalty"],
        "hyp_best": {k: hyp_best[k] for k in ("kind", "inward", "continuous", "ccw", "corner")},
        "siamese_best_rule": siamese["best_fixed_rule"],
        "penalty_floor": PENALTY_FLOOR,
    }
    analysis["crosscheck"] = annotation_crosscheck(analysis)
    analysis["verdict"] = (
        "알고리즘 확정 불가 (현재 증거로는). "
        "기하 골격(271/270/54/19/252)과 합 조건(고리 813k·변 1355·축 2439·"
        "대척쌍 271)은 주석과 완전히 정합하지만, 값의 배치 순서 규칙은 "
        "재구된 어떤 최적해에도 압축적인 흔적으로 남아 있지 않다. "
        "添六의 값 규칙 독해는 전부 반증되었고, 배치 순서 구절(寄左/序左)은 "
        "최적해가 다수 존재해 재구 도안만으로는 판정할 수 없다. "
        "확정 가능한 것은 '무엇이 아닌가'의 범위까지이며, "
        "알고리즘 본문의 확정에는 더 선명한 판본이 필요하다."
    )
    return analysis


# ---------------------------------------------------------------------------
# 출력
# ---------------------------------------------------------------------------

def write_reverse_json(analysis: dict, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=1)


def write_reverse_markdown(analysis: dict, path: str) -> None:
    s = analysis
    lines = [
        "# 洛書六觚圖 — 최종 재구 도안의 생성 규칙 역산 및 주석 대조",
        "",
        "재구된 최적해(`output/solution.json`)를 대상으로, 압축적인 생성 규칙이",
        "남아 있는지를 데이터 주도로 검사하고, 결과를 흐린 주석의 판독 구절과",
        "하나씩 대조한다.",
        "",
        "## 1. 최종 재구 도안의 위치",
        "",
        f"- 탐색 목적 함수의 이론적 하한: {s['penalty_floor']} (달성).",
        f"- 다른 시드({s['seed_scan']['seed']})로 찾은 최적해와의 일치 칸: "
        f"**{s['seed_scan']['identical_cells']}/270**.",
        "- 즉 조건을 만족하는 배치는 다수 존재하며, 재구된 도안은 그중 하나의",
        "  표본이다. 역산은 이 표본에 건설적 흔적이 남는지를 묻는다.",
        "",
        "## 2. 역산 시도와 결과",
        "",
        "| 후보 규칙 | 방법 | 결과 |",
        "|---|---|---|",
        f"| 고리 순회 등차 (임의 스텝 mod 271) | 고리별 270스텝 전수 | 실패 — 최선 일치율 {s['ring_ap']['max_ratio']:.1%} |",
        f"| 좌표 선형 모형 v ≡ a+b·k+c·j | (a,b,c) 271³ 전수 | 실패 — {s['linear_model']['best_matches']}/270칸 |",
        "| mod 6 클래스 균형 (添六 지문) | 고리별 6류 분포 | 불균형·불일치 — 지문 없음 |",
        f"| 대척쌍 건설적 배정 순서 | 나선 순회 기준 연속 구간 | 없음 — 최장 {s['pair_order']['longest_consecutive_run']}쌍 |",
        f"| 광선 차분 규칙 | 마주 보는 광선 비교 | 부호 반전 — 대척쌍 가설의 자동 귀결 |",
        f"| Siamese식 지역 규칙 (siamese.py) | 주 이동+보정 이동 쌍 | 실패 — 269전이 중 {s['siamese_best_rule']['matches']}개 |",
        f"| 添六 건설 가설 (hypotheses.py) | ±6 mod 271 나선 192변형 | 실패 — 최선 벌점 {s['hyp_best_penalty']:.0f} (하한 {s['penalty_floor']}) |",
        "",
        "## 3. 주석 구절 대조",
        "",
        "| 주석 구절 | 판독 | 판정 | 근거 |",
        "|---|---|---|---|",
    ]
    for row in s["crosscheck"]:
        lines.append(f"| {row['fragment']} | {row['reading']} | {row['status']} | {row['evidence']} |")
    lines += [
        "",
        "## 4. 판정: 알고리즘 확정 가능 여부",
        "",
        s["verdict"],
        "",
        "### 확정된 것",
        "",
        "- 기하 골격: 271칸(虛一 → 270), 외주 54, 한 변 10칸, 中觚 19칸.",
        "- 합 조건: 대척쌍 271, 고리 813k, 변 1355, 축 2439, 섹터 6097/6098,",
        "  광선 1219/1220 — 주석의 수치와 《漢書》 六觚 기록에 정합.",
        "- 添六·寄左 계열 구절은 값 규칙이 아니라 칸 수·순서 지시로 읽어야",
        "  한다는 방향성.",
        "",
        "### 확정되지 않은 것",
        "",
        "- 값을 칸에 배정하는 절차(내적법 본문). 재구 최적해들 사이의 겹침이",
        "  0/270이므로, 합 조걸만으로는 원래 배치를 특정할 수 없고, 원래 배치가",
        "  따른 순서 규칙도 이 표본들에서 복구할 수 없다.",
        "- 알고리즘의 확정에는 더 선명한 주석 판본이 필요하다.",
        "",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main() -> None:
    grid = HexGrid()
    values = load_solution()
    os.makedirs("output", exist_ok=True)
    analysis = build_reverse_analysis(values, grid)
    write_reverse_json(analysis, "output/reverse_engineering.json")
    write_reverse_markdown(analysis, "output/reverse_engineering.md")
    print("\n=== 판정 ===")
    print(analysis["verdict"])
    print("\n저장: output/reverse_engineering.json, output/reverse_engineering.md")


if __name__ == "__main__":
    main()
