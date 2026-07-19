#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MILP reconstruction for Nakseo Chilgudo.

Hard constraints:
- each of the 9 palaces has 7 numbers summing to 224
- the reconstructed diagram uses each integer 1..63 exactly once

Objective:
- keep OCR readings when possible
- otherwise choose the lowest-cost OCR correction candidate
"""

from __future__ import annotations

from dataclasses import dataclass

import pulp


TARGET_SUM = 224
VALUES = range(1, 64)


@dataclass(frozen=True)
class Slot:
    palace: str
    index: int
    observed: int | None
    candidates: dict[int, int]


PALACES = [
    ("상좌궁", 4, [31, 43, 12, 60, 27, 37]),
    ("상중궁", 9, [15, 45, None, 55, 10, 54]),
    ("상우궁", 2, [28, 29, 39, 62, 17, 47]),
    ("중좌궁", 3, [30, 40, 36, 61, 16, 48]),
    ("중중궁", 5, [32, 41, 23, 59, 14, 50]),
    ("중우궁", 7, [34, None, 24, 57, 20, 44]),
    ("하좌궁", 8, [35, 49, 12, None, 11, 53]),
    ("하중궁", 1, [52, 25, 19, 63, 68, 48]),
    ("하우궁", 6, [33, 42, 21, 58, 13, 23]),
]


def candidate_costs(observed: int | None) -> dict[int, int]:
    if observed is None:
        return {v: 5 for v in VALUES}

    costs = {v: 20 for v in VALUES}
    if observed in VALUES:
        costs[observed] = 0

    # Low-cost OCR confusions needed by the source constraints.
    corrections = {
        12: [22],
        46: [36],
        36: [26],
        68: [18],
        48: [46],
        23: [51],
    }
    for v in corrections.get(observed, []):
        costs[v] = min(costs[v], 1)
    return costs


def build_slots() -> tuple[list[Slot], dict[str, list[Slot]]]:
    slots: list[Slot] = []
    by_palace: dict[str, list[Slot]] = {}

    for palace, center, surround in PALACES:
        palace_slots = [Slot(palace, 0, center, {center: 0})]
        for i, observed in enumerate(surround, start=1):
            palace_slots.append(Slot(palace, i, observed, candidate_costs(observed)))
        slots.extend(palace_slots)
        by_palace[palace] = palace_slots

    return slots, by_palace


def solve() -> dict[tuple[str, int], int]:
    slots, by_palace = build_slots()
    problem = pulp.LpProblem("nakseo_chilgudo_reconstruction", pulp.LpMinimize)

    x = {}
    for slot in slots:
        for value in slot.candidates:
            x[(slot.palace, slot.index, value)] = pulp.LpVariable(
                f"x_{slot.palace}_{slot.index}_{value}",
                lowBound=0,
                upBound=1,
                cat="Binary",
            )

    for slot in slots:
        problem += (
            pulp.lpSum(x[(slot.palace, slot.index, value)] for value in slot.candidates) == 1
        )

    for value in VALUES:
        problem += (
            pulp.lpSum(
                x[(slot.palace, slot.index, value)]
                for slot in slots
                if value in slot.candidates
            )
            == 1
        )

    for palace, palace_slots in by_palace.items():
        problem += (
            pulp.lpSum(
                value * x[(slot.palace, slot.index, value)]
                for slot in palace_slots
                for value in slot.candidates
            )
            == TARGET_SUM
        ), f"sum_{palace}"

    problem += pulp.lpSum(
        cost * x[(slot.palace, slot.index, value)]
        for slot in slots
        for value, cost in slot.candidates.items()
    )

    status = problem.solve(pulp.PULP_CBC_CMD(msg=False))
    if pulp.LpStatus[status] != "Optimal":
        raise RuntimeError(f"No optimal reconstruction found: {pulp.LpStatus[status]}")

    solution: dict[tuple[str, int], int] = {}
    for slot in slots:
        chosen = [
            value
            for value in slot.candidates
            if pulp.value(x[(slot.palace, slot.index, value)]) > 0.5
        ]
        solution[(slot.palace, slot.index)] = chosen[0]
    return solution


def main() -> None:
    solution = solve()
    for palace, center, surround in PALACES:
        values = [solution[(palace, i)] for i in range(7)]
        observed = [center] + surround
        changed = [
            f"{i}:{obs}->{val}"
            for i, (obs, val) in enumerate(zip(observed, values))
            if obs != val
        ]
        print(f"{palace}: {values} sum={sum(values)}")
        if changed:
            print(f"  reconstructed: {', '.join(changed)}")


if __name__ == "__main__":
    main()
