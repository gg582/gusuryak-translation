#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MILP reconstruction for Nakseo Gugudo (낙서구구도).

Hard constraints:
- the nine palace centers stay fixed at the loshu values
  (4 9 2 / 3 5 7 / 8 1 6 in the source reading order)
- each cluster (center + 8 ring values) sums to 369
- ring positions use each integer 10..81 exactly once

Objective:
- the original diagram has every value inscribed correctly; the errors were
  introduced while transcribing it (four cells), so preserve the transcription
  wherever it stays consistent with the constraints
- each ring slot keeps its transcribed value at cost 0; any change costs 1

Solved with scipy.optimize.milp (HiGHS).
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix

TARGET_SUM = 369

# Palace order follows the user's reading (loshu text order).
# Each entry: (label, center, [ring reads clockwise from the upper-left],
#              [slot indices that were read, 1-based; empty = free slot])
PALACES = [
    ("四", 4, [15, 80, 61, 23, 28, 72, 39], [1, 2, 3, 4, 5, 6, 7]),
    ("九", 9, [49, 57, 17, 73, 41, 25, 65, 33], [1, 2, 3, 4, 5, 6, 7, 8]),
    ("二", 2, [54, 43, 67, 10, 59, 21, 78, 35], [1, 2, 3, 4, 5, 6, 7, 8]),
    ("三", 3, [11, 76, 60, 36, 71, 68, 52, 44], [1, 2, 3, 4, 5, 6, 7, 8]),
    ("五", 5, [29, 24, 62, 37, 70, 81, 48, 13], [1, 2, 3, 4, 5, 6, 7, 8]),
    ("七", 7, [74, 26, 55, 3, 42, 50, 66, 18], [1, 2, 3, 4, 5, 6, 7, 8]),
    ("八", 8, [16, 51, 56, 27, 64, 32, 40, 75], [1, 2, 3, 4, 5, 6, 7, 8]),
    ("一", 1, [69, 34, 77, 12, 53, 58, 45, 20], [1, 2, 3, 4, 5, 6, 7, 8]),
    ("六", 6, [38, 79, 14, 63, 46, 22, 71, 38], [1, 2, 3, 4, 5, 6, 7, 8]),
]

VALUES = list(range(10, 82))
N_SLOTS = 9 * 8
N_VARS = N_SLOTS * len(VALUES)

# slots: palace-major, slot 1..8
def slot_index(palace_idx: int, ring_slot: int) -> int:
    return palace_idx * 8 + (ring_slot - 1)


def solve() -> dict[tuple[int, int], int]:
    costs = np.ones(N_VARS)
    for pi, (_, _, reads, slots) in enumerate(PALACES):
        for value, s in zip(reads, slots):
            if value in VALUES:
                costs[slot_index(pi, s) * len(VALUES) + (value - 10)] = 0.0

    rows = []
    lb = []
    ub = []

    def add_row(entries: list[tuple[int, int, float]], lo: float, hi: float) -> None:
        row = lil_matrix((1, N_VARS))
        for si, vi, coef in entries:
            row[0, si * len(VALUES) + vi] = coef
        rows.append(row)
        lb.append(lo)
        ub.append(hi)

    for si in range(N_SLOTS):
        add_row([(si, vi, 1.0) for vi in range(len(VALUES))], 1.0, 1.0)

    for vi in range(len(VALUES)):
        add_row([(si, vi, 1.0) for si in range(N_SLOTS)], 1.0, 1.0)

    for pi, (_, center, _, _) in enumerate(PALACES):
        entries = [
            (slot_index(pi, s), vi, float(vi + 10))
            for s in range(1, 9)
            for vi in range(len(VALUES))
        ]
        add_row(entries, float(TARGET_SUM - center), float(TARGET_SUM - center))

    A = lil_matrix(np.vstack([m.toarray() for m in rows]))
    result = milp(
        c=costs,
        constraints=LinearConstraint(A.tocsr(), np.array(lb), np.array(ub)),
        bounds=Bounds(np.zeros(N_VARS), np.ones(N_VARS)),
        integrality=np.ones(N_VARS),
        options={"time_limit": 600, "mip_rel_gap": 0.0},
    )
    if result.x is None:
        raise RuntimeError(f"No feasible reconstruction found: {result.message}")

    solution: dict[tuple[int, int], int] = {}
    for pi in range(9):
        for s in range(1, 9):
            si = slot_index(pi, s)
            chosen = np.where(result.x[si * len(VALUES) : (si + 1) * len(VALUES)] > 0.5)[0]
            if len(chosen) != 1:
                raise RuntimeError(f"palace {pi} slot {s} has {len(chosen)} values")
            solution[(pi, s)] = chosen[0] + 10
    return solution


def verify(solution: dict[tuple[int, int], int]) -> None:
    ring = sorted(solution[(pi, s)] for pi in range(9) for s in range(1, 9))
    assert ring == VALUES, "ring must use 10..81 exactly once"
    for pi, (label, center, _, _) in enumerate(PALACES):
        total = center + sum(solution[(pi, s)] for s in range(1, 9))
        assert total == TARGET_SUM, f"palace {label} sums to {total}"


def main() -> None:
    solution = solve()
    verify(solution)

    changed = []
    for pi, (label, center, reads, slots) in enumerate(PALACES):
        ring = [solution[(pi, s)] for s in range(1, 9)]
        print(f"palace {label} (center {center}): {ring} sum={center + sum(ring)}")
        for value, s in zip(reads, slots):
            if value not in VALUES:
                changed.append((label, s, value, solution[(pi, s)], "misread"))
            elif solution[(pi, s)] != value:
                changed.append((label, s, value, solution[(pi, s)], ""))
        for s in range(1, 9):
            if s not in slots:
                changed.append((label, s, "—", solution[(pi, s)], "dropped in transcription"))
    print(f"\ncorrections: {len(changed)}")
    for label, s, old, new, note in changed:
        print(f"  palace {label} slot {s}: {old} -> {new} {note}")


if __name__ == "__main__":
    main()
