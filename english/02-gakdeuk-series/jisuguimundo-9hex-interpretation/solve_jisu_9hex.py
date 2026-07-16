#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MILP solver for the representative 30-vertex 9-hex Jisuguimundo.

A solved assignment with magic constant S=93 is already stored in
jisu_9hex_solution.json.  Running this script reproduces (or re-finds)
that solution and writes it to disk.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pulp


ROOT = Path(__file__).resolve().parent


def load_topology(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def solve(
    hexagons: list[list[int]],
    magic_constant: int,
    time_limit: int = 300,
) -> dict[str, Any]:
    node_count = max(max(hx) for hx in hexagons)
    hexagons_0based = [[v - 1 for v in hx] for hx in hexagons]

    prob = pulp.LpProblem("jisuguimundo_9hex", pulp.LpStatusOptimal)
    x = pulp.LpVariable.dicts(
        "x", (range(node_count), range(1, node_count + 1)),
        lowBound=0, upBound=1, cat=pulp.LpBinary,
    )

    for v in range(node_count):
        prob += pulp.lpSum(x[v][n] for n in range(1, node_count + 1)) == 1
    for n in range(1, node_count + 1):
        prob += pulp.lpSum(x[v][n] for v in range(node_count)) == 1
    for idx, hx in enumerate(hexagons_0based):
        prob += (
            pulp.lpSum(n * x[v][n] for v in hx for n in range(1, node_count + 1))
            == magic_constant
        ), f"hex_sum_{idx}"

    prob.solve(pulp.PULP_CBC_CMD(msg=True, timeLimit=time_limit))

    status = pulp.LpStatus[prob.status]
    if status != "Optimal":
        raise RuntimeError(f"No optimal solution found; status={status}")

    assignment: list[int] = [0] * node_count
    for v in range(node_count):
        for n in range(1, node_count + 1):
            if pulp.value(x[v][n]) > 0.5:
                assignment[v] = n
                break

    return {"S": magic_constant, "assignment": assignment}


def main() -> None:
    topology = load_topology(ROOT / "jisu_9hex_topology.json")
    magic_constant = topology["magic_constant"]
    hexagons = topology["hexagons"]

    solution = solve(hexagons, magic_constant)
    solution["hexagon_values"] = [
        [solution["assignment"][v - 1] for v in hx] for hx in hexagons
    ]

    out_path = ROOT / "jisu_9hex_solution.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(solution, f, ensure_ascii=False, indent=2)
    print(f"Saved solution: {out_path}")

    for idx, vals in enumerate(solution["hexagon_values"], start=1):
        print(f"Hex{idx}: {vals} = {sum(vals)}")


if __name__ == "__main__":
    main()
