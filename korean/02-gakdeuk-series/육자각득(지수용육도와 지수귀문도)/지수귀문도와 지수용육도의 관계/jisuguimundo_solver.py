#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
지수귀문도(Jisuguimundo) / 지수용육도 일반화 Solver

- 노드 수 M이 주어지면 위키백과에 기록된 대표적 지수귀문도 토폴로지 중
  해당하는 구조를 선택해 MILP(PuLP)으로 수 배치를 탐색합니다.
- 지수용육도(5hex, M=20, S=63)를 핵심 코어로 보고, 이를 확장한
  3/4/6/7/9/10-hex 구조를 함께 다룹니다.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from typing import Any

import pulp


# ============================================================
# 0. 사전 정의된 지수귀문도 토폴로지
# ============================================================

# 지수용육도 (5hex): 20개 노드, 각 육각형 합 63
# 출처: analyze.py 의 HEXAGONS (1-based 값을 0-based 인덱스로 변환)
YUKDO_HEXAGONS: list[list[int]] = [
    [4, 17, 15, 2, 7, 12],    # 상좌
    [0, 12, 7, 13, 19, 6],    # 상우
    [2, 7, 13, 14, 10, 11],   # 중앙
    [11, 10, 9, 1, 18, 8],    # 하좌
    [14, 3, 16, 5, 9, 10],    # 하우
]

# 3hex 삼각형 (M=13): 중앙 1노드가 3개 육각형 공유, 변 공유 3노드, 고유 9노드
HEX3_HEXAGONS: list[list[int]] = [
    [0, 1, 2, 3, 4, 5],
    [0, 1, 6, 7, 8, 9],
    [0, 9, 10, 11, 12, 2],
]

# 4hex 마름모 (M=16): 2x2 배치, 인접 쌍마다 2노드 공유
HEX4_HEXAGONS: list[list[int]] = [
    [0, 1, 2, 3, 4, 5],    # TL
    [0, 1, 6, 7, 8, 9],    # TR
    [2, 3, 10, 11, 12, 13],# BL
    [6, 7, 10, 11, 14, 15],# BR
]

# 7hex 정육각형 (M=24): 중앙 1개 + 주변 6개
# 중앙 정점 6개, 중앙-주변 공유 6쌍(12 소속), 주변-주변 공유 6개, 주변 고유 12개
HEX7_HEXAGONS: list[list[int]] = [
    [0, 1, 2, 3, 4, 5],          # 중앙
    [0, 1, 6, 7, 8, 23],         # 주변 0 (s5=23 과 s0=6 공유)
    [1, 2, 6, 9, 10, 11],        # 주변 1
    [2, 3, 11, 12, 13, 14],      # 주변 2
    [3, 4, 14, 15, 16, 17],      # 주변 3
    [4, 5, 17, 18, 19, 20],      # 주변 4
    [5, 0, 20, 21, 22, 23],      # 주변 5
]

# 9hex 거북등 (M=30), 10hex 삼각형(M=33), 19hex 정육각형(M=54) 등은
# 토폴로지가 복잡하여 본 스크립트에서는 아직 자동 생성하지 않습니다.
# 위키백과의 S 범위만 기록해 둡니다.

# M -> (hexagon 수 H, 토폴로지, 위키 S 범위)
STRUCTURES: dict[int, dict[str, Any]] = {
    13: {"name": "3hex 삼각형", "hexagons": HEX3_HEXAGONS, "s_range": (34, 50)},
    16: {"name": "4hex 마름모", "hexagons": HEX4_HEXAGONS, "s_range": (40, 62)},
    20: {"name": "지수용육도(5hex)", "hexagons": YUKDO_HEXAGONS, "s_range": (63, 63)},
    22: {"name": "6hex 삼각형", "hexagons": None, "s_range": (57, 71)},
    24: {"name": "7hex 정육각형", "hexagons": HEX7_HEXAGONS, "s_range": (65, 85)},
    30: {"name": "9hex 거북등", "hexagons": None, "s_range": (77, 109)},
    33: {"name": "10hex 삼각형", "hexagons": None, "s_range": (83, 121)},
    54: {"name": "19hex 정육각형", "hexagons": None, "s_range": (140, 190)},
}


def compute_multiplicities(hexagons: list[list[int]], m: int) -> list[int]:
    mult = [0] * m
    for h in hexagons:
        for v in h:
            mult[v] += 1
    return mult


def magic_sum_bounds(m: int, hexagons: list[list[int]]) -> tuple[int, int]:
    """
    H*S = T + D, where D = sum_{v} (mult(v)-1) * value(v).
    Crude bounds on D by assigning smallest/largest numbers to shared vertices.
    """
    h = len(hexagons)
    t = m * (m + 1) // 2
    mult = compute_multiplicities(hexagons, m)
    shared = [(mult[v] - 1, v) for v in range(m) if mult[v] > 1]
    # Min D: largest excess paired with smallest values
    shared.sort(key=lambda x: x[0], reverse=True)
    weights = [w for w, _ in shared]
    k = len(shared)
    # assign 1..k to shared vertices, highest weight gets smallest value
    d_min = sum(w * (i + 1) for i, w in enumerate(weights))
    d_max = sum(w * (m - i) for i, w in enumerate(weights))
    s_min = math.ceil((t + d_min) / h)
    s_max = math.floor((t + d_max) / h)
    return s_min, s_max


def solve_jisuguimundo(
    m: int,
    hexagons: list[list[int]],
    target_s: int | None = None,
    max_solutions: int = 1,
    time_limit: int | None = None,
    verbose: bool = False,
) -> list[dict[str, Any]]:
    """
    MILP solver for a Jisuguimundo instance.
    Returns list of solutions, each is dict with 'assignment' (node->value) and 'S'.
    """
    h = len(hexagons)
    # Determine target S
    if target_s is None:
        s_min, s_max = magic_sum_bounds(m, hexagons)
        # Try the natural center first, then widen
        candidates = []
        center = (s_min + s_max) // 2
        candidates.append(center)
        for delta in range(1, max(s_max - s_min + 1, 1)):
            if center - delta >= s_min:
                candidates.append(center - delta)
            if center + delta <= s_max:
                candidates.append(center + delta)
    else:
        candidates = [target_s]

    solutions: list[dict[str, Any]] = []
    for s in candidates:
        if len(solutions) >= max_solutions:
            break
        prob = pulp.LpProblem("Jisuguimundo", pulp.LpStatusOptimal)
        # x[v][n] = 1 if node v gets number n
        x = pulp.LpVariable.dicts(
            "x", (range(m), range(1, m + 1)), lowBound=0, upBound=1, cat=pulp.LpBinary
        )
        # Each node gets exactly one number
        for v in range(m):
            prob += pulp.lpSum(x[v][n] for n in range(1, m + 1)) == 1
        # Each number used exactly once
        for n in range(1, m + 1):
            prob += pulp.lpSum(x[v][n] for v in range(m)) == 1
        # Each hexagon sums to S
        for idx, hx in enumerate(hexagons):
            prob += (
                pulp.lpSum(n * x[v][n] for v in hx for n in range(1, m + 1)) == s
            ), f"hex_sum_{idx}"
        # Optional time limit
        if time_limit:
            prob.solve(pulp.PULP_CBC_CMD(msg=verbose, timeLimit=time_limit))
        else:
            prob.solve(pulp.PULP_CBC_CMD(msg=verbose))
        if pulp.LpStatus[prob.status] == "Optimal":
            assignment: dict[int, int] = {}
            for v in range(m):
                for n in range(1, m + 1):
                    if pulp.value(x[v][n]) > 0.5:
                        assignment[v] = n
                        break
            # Validate
            valid = True
            for hx in hexagons:
                if sum(assignment[v] for v in hx) != s:
                    valid = False
                    break
            if valid:
                solutions.append({"S": s, "assignment": assignment})
                if verbose:
                    print(f"  Found solution with S={s}")
            # For enumerating multiple solutions for same S, add no-good cuts
            if max_solutions > len(solutions):
                # This is handled by outer loop; for same S enumeration we'd need more.
                pass
        else:
            if verbose:
                print(f"  No solution for S={s}")
    return solutions


def solve_all_for_s(
    m: int,
    hexagons: list[list[int]],
    target_s: int,
    max_solutions: int | None = None,
    time_limit: int | None = None,
    verbose: bool = False,
) -> list[dict[str, Any]]:
    """Enumerate all solutions for a fixed S using no-good cuts."""
    solutions: list[dict[str, Any]] = []
    prob = pulp.LpProblem("Jisuguimundo_Enum", pulp.LpStatusOptimal)
    x = pulp.LpVariable.dicts(
        "x", (range(m), range(1, m + 1)), lowBound=0, upBound=1, cat=pulp.LpBinary
    )
    for v in range(m):
        prob += pulp.lpSum(x[v][n] for n in range(1, m + 1)) == 1
    for n in range(1, m + 1):
        prob += pulp.lpSum(x[v][n] for v in range(m)) == 1
    for idx, hx in enumerate(hexagons):
        prob += (
            pulp.lpSum(n * x[v][n] for v in hx for n in range(1, m + 1)) == target_s
        ), f"hex_sum_{idx}"

    count = 0
    while max_solutions is None or count < max_solutions:
        if time_limit:
            prob.solve(pulp.PULP_CBC_CMD(msg=verbose, timeLimit=time_limit))
        else:
            prob.solve(pulp.PULP_CBC_CMD(msg=verbose))
        if pulp.LpStatus[prob.status] != "Optimal":
            break
        assignment: dict[int, int] = {}
        for v in range(m):
            for n in range(1, m + 1):
                if pulp.value(x[v][n]) > 0.5:
                    assignment[v] = n
                    break
        solutions.append({"S": target_s, "assignment": assignment})
        count += 1
        # No-good cut
        prob += (
            pulp.lpSum(x[v][assignment[v]] for v in range(m)) <= m - 1
        ), f"nogood_{count}"
    return solutions


def pretty_print_solution(m: int, hexagons: list[list[int]], sol: dict[str, Any]) -> None:
    assignment = sol["assignment"]
    s = sol["S"]
    print(f"M={m}, H={len(hexagons)}, S={s}")
    mult = compute_multiplicities(hexagons, m)
    shared = [v for v in range(m) if mult[v] > 1]
    print(f"공유 정점: {sorted(shared)}")
    for idx, hx in enumerate(hexagons):
        vals = [assignment[v] for v in hx]
        print(f"  H{idx}: {vals} = {sum(vals)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="지수귀문도 / 지수용육도 Solver")
    parser.add_argument("--m", type=int, required=True, help="노드 수 M")
    parser.add_argument("--S", type=int, default=None, help="목표 육각형 합")
    parser.add_argument("--max-solutions", type=int, default=1, help="찾을 최대 해 수")
    parser.add_argument("--enumerate", action="store_true", help="주어진 S에 대해 모든 해 열거")
    parser.add_argument("--time-limit", type=int, default=60, help="S 후보당 시간 제한(초)")
    parser.add_argument("--output", type=str, default=None, help="JSON 저장 경로")
    parser.add_argument("--verbose", action="store_true", help="자세한 출력")
    args = parser.parse_args()

    if args.m not in STRUCTURES:
        print(f"지원하지 않는 M={args.m}. 지원: {sorted(STRUCTURES.keys())}")
        sys.exit(1)
    info = STRUCTURES[args.m]
    hexagons = info["hexagons"]
    if hexagons is None:
        print(f"M={args.m} ({info['name']})는 아직 토폴로지가 구현되지 않았습니다.")
        sys.exit(1)

    s_min, s_max = magic_sum_bounds(args.m, hexagons)
    print(f"[{info['name']}] M={args.m}, H={len(hexagons)}")
    print(f"  이론적 S 범위(추정): {s_min} ~ {s_max}")
    if info["s_range"]:
        print(f"  위키백과 S 범위: {info['s_range'][0]} ~ {info['s_range'][1]}")

    target_s = args.S
    if target_s is None:
        target_s = (info["s_range"][0] + info["s_range"][1]) // 2
        print(f"  목표 S: {target_s} (위키 범위 중앙)")
    else:
        print(f"  목표 S: {target_s}")

    if args.enumerate:
        print(f"  S={target_s}에서 모든 해를 열거합니다...")
        solutions = solve_all_for_s(
            args.m,
            hexagons,
            target_s,
            max_solutions=args.max_solutions if args.max_solutions > 0 else None,
            time_limit=args.time_limit,
            verbose=args.verbose,
        )
    else:
        solutions = solve_jisuguimundo(
            args.m,
            hexagons,
            target_s=target_s,
            max_solutions=args.max_solutions,
            time_limit=args.time_limit,
            verbose=args.verbose,
        )

    print(f"\n총 {len(solutions)}개 해 찾음")
    for i, sol in enumerate(solutions[:5], 1):
        print(f"\n[해 {i}]")
        pretty_print_solution(args.m, hexagons, sol)

    if args.output:
        out = {
            "M": args.m,
            "name": info["name"],
            "H": len(hexagons),
            "target_S": target_s,
            "solutions": [
                {"S": s["S"], "assignment": [s["assignment"][v] for v in range(args.m)]}
                for s in solutions
            ],
        }
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print(f"\n[JSON 저장] {args.output}")


if __name__ == "__main__":
    main()
