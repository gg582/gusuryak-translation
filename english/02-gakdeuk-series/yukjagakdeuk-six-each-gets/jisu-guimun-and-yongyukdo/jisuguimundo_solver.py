#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jisu-guimun-do / Jisu-yong-yukdo generalized solver

- Given the number of nodes M, selects the corresponding representative
  Jisu-guimun-do topology and searches for a number placement using MILP (PuLP).
- Treats Jisu-yong-yukdo (5 hexagons, M=20, S=63) as the core, and also handles
  the extended 3/4/6/7/9/10-hex structures.
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
# 0. Predefined Jisu-guimun-do topologies
# ============================================================

# Jisu-yong-yukdo (5 hexagons): 20 nodes, each hexagon sums to 63
# Source: HEXAGONS from analyze.py, converted from 1-based values to 0-based indices
YUKDO_HEXAGONS: list[list[int]] = [
    [4, 17, 15, 2, 7, 12],    # upper-left
    [0, 12, 7, 13, 19, 6],    # upper-right
    [2, 7, 13, 14, 10, 11],   # center
    [11, 10, 9, 1, 18, 8],    # lower-left
    [14, 3, 16, 5, 9, 10],    # lower-right
]

# 3-hex triangle (M=13): 1 central node shared by 3 hexagons,
# 3 edge-shared nodes, and 9 unique nodes
HEX3_HEXAGONS: list[list[int]] = [
    [0, 1, 2, 3, 4, 5],
    [0, 1, 6, 7, 8, 9],
    [0, 9, 10, 11, 12, 2],
]

# 4-hex rhombus (M=16): 2x2 arrangement, each adjacent pair shares 2 nodes
HEX4_HEXAGONS: list[list[int]] = [
    [0, 1, 2, 3, 4, 5],    # top-left
    [0, 1, 6, 7, 8, 9],    # top-right
    [2, 3, 10, 11, 12, 13],# bottom-left
    [6, 7, 10, 11, 14, 15],# bottom-right
]

# 7-hex regular hexagon (M=24): 1 central hexagon + 6 surrounding hexagons
# Central vertices (6), central-surround shared pairs (12 membership-counts),
# surround-surround shared vertices (6), and surround-unique vertices (12)
HEX7_HEXAGONS: list[list[int]] = [
    [0, 1, 2, 3, 4, 5],          # center
    [0, 1, 6, 7, 8, 23],         # surround 0 (shares s5=23 and s0=6)
    [1, 2, 6, 9, 10, 11],        # surround 1
    [2, 3, 11, 12, 13, 14],      # surround 2
    [3, 4, 14, 15, 16, 17],      # surround 3
    [4, 5, 17, 18, 19, 20],      # surround 4
    [5, 0, 20, 21, 22, 23],      # surround 5
]

# 9-hex turtle shell (M=30), 10-hex triangle (M=33), 19-hex regular hexagon (M=54), etc.,
# have complex topologies and are not yet auto-generated in this script.
# We record only the Wikipedia S ranges for them.

# M -> (number of hexagons H, topology, Wikipedia S range)
STRUCTURES: dict[int, dict[str, Any]] = {
    13: {"name": "3-hex triangle", "hexagons": HEX3_HEXAGONS, "s_range": (34, 50)},
    16: {"name": "4-hex rhombus", "hexagons": HEX4_HEXAGONS, "s_range": (40, 62)},
    20: {"name": "Jisu-yong-yukdo (5-hex)", "hexagons": YUKDO_HEXAGONS, "s_range": (63, 63)},
    22: {"name": "6-hex triangle", "hexagons": None, "s_range": (57, 71)},
    24: {"name": "7-hex regular hexagon", "hexagons": HEX7_HEXAGONS, "s_range": (65, 85)},
    30: {"name": "9-hex turtle shell", "hexagons": None, "s_range": (77, 109)},
    33: {"name": "10-hex triangle", "hexagons": None, "s_range": (83, 121)},
    54: {"name": "19-hex regular hexagon", "hexagons": None, "s_range": (140, 190)},
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
    MILP solver for a Jisu-guimun-do instance.
    Returns a list of solutions, each a dict with 'assignment' (node->value) and 'S'.
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
                # This is handled by outer loop; for same-S enumeration more would be needed.
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
    print(f"Shared vertices: {sorted(shared)}")
    for idx, hx in enumerate(hexagons):
        vals = [assignment[v] for v in hx]
        print(f"  H{idx}: {vals} = {sum(vals)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Jisu-guimun-do / Jisu-yong-yukdo solver")
    parser.add_argument("--m", type=int, required=True, help="Number of nodes M")
    parser.add_argument("--S", type=int, default=None, help="Target hexagon sum")
    parser.add_argument("--max-solutions", type=int, default=1, help="Maximum number of solutions to find")
    parser.add_argument("--enumerate", action="store_true", help="Enumerate all solutions for the given S")
    parser.add_argument("--time-limit", type=int, default=60, help="Time limit per S candidate (seconds)")
    parser.add_argument("--output", type=str, default=None, help="JSON output path")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    if args.m not in STRUCTURES:
        print(f"Unsupported M={args.m}. Supported values: {sorted(STRUCTURES.keys())}")
        sys.exit(1)
    info = STRUCTURES[args.m]
    hexagons = info["hexagons"]
    if hexagons is None:
        print(f"M={args.m} ({info['name']}) topology is not implemented yet.")
        sys.exit(1)

    s_min, s_max = magic_sum_bounds(args.m, hexagons)
    print(f"[{info['name']}] M={args.m}, H={len(hexagons)}")
    print(f"  Theoretical S range (estimate): {s_min} ~ {s_max}")
    if info["s_range"]:
        print(f"  Wikipedia S range: {info['s_range'][0]} ~ {info['s_range'][1]}")

    target_s = args.S
    if target_s is None:
        target_s = (info["s_range"][0] + info["s_range"][1]) // 2
        print(f"  Target S: {target_s} (center of Wikipedia range)")
    else:
        print(f"  Target S: {target_s}")

    if args.enumerate:
        print(f"  Enumerating all solutions for S={target_s}...")
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

    print(f"\nTotal solutions found: {len(solutions)}")
    for i, sol in enumerate(solutions[:5], 1):
        print(f"\n[Solution {i}]")
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
        print(f"\n[JSON saved] {args.output}")


if __name__ == "__main__":
    main()
