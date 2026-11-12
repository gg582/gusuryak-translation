#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MILP reconstruction for Nakseo Palgudo (오팔정전도 五八井田圖).

Hard constraints:
- the 7x7 well-field keeps its 9 empty centers fixed
- each of the nine 3x3 wells (center hole + 8 surrounding cells) sums to 164
- the diagram uses each integer 1..40 exactly once

Objective:
- keep the observed placements from visualize.py when possible
- minimize the number of cells whose value has to move

Solved with scipy.optimize.milp (HiGHS).
"""

from __future__ import annotations

import json

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix

TARGET_SUM = 164
N = 7
CENTERS = [(r, c) for r in (1, 3, 5) for c in (1, 3, 5)]

# Observed placement copied from visualize.py (guessed cells included).
OBSERVED = [
    [5, 11, 30, 25, 4, 32, 9],
    [36, None, 17, None, 33, None, 28],
    [1, 40, 24, 18, 12, 29, 13],
    [27, None, 23, None, 19, None, 16],
    [8, 26, 15, 22, 31, 10, 35],
    [37, None, 38, None, 20, None, 2],
    [7, 34, 3, 14, 21, 39, 6],
]

CELLS = [(r, c) for r in range(N) for c in range(N) if OBSERVED[r][c] is not None]
VALUES = list(range(1, 41))
N_CELLS = len(CELLS)
N_VARS = N_CELLS * len(VALUES)


def well_cells(center: tuple[int, int]) -> list[tuple[int, int]]:
    cr, cc = center
    return [
        (cr + dr, cc + dc)
        for dr in (-1, 0, 1)
        for dc in (-1, 0, 1)
        if (dr, dc) != (0, 0)
    ]


def solve() -> np.ndarray:
    # x[cell_index * 40 + (value - 1)] = 1 iff the cell holds that value.
    costs = np.ones(N_VARS)
    for ci, (r, c) in enumerate(CELLS):
        costs[ci * 40 + (OBSERVED[r][c] - 1)] = 0.0

    rows = []
    lb = []
    ub = []

    def add_row(entries: list[tuple[int, int, float]], lo: float, hi: float) -> None:
        row = lil_matrix((1, N_VARS))
        for ci, vi, coef in entries:
            row[0, ci * 40 + vi] = coef
        rows.append(row)
        lb.append(lo)
        ub.append(hi)

    for ci in range(N_CELLS):
        add_row([(ci, vi, 1.0) for vi in range(40)], 1.0, 1.0)

    for vi in range(40):
        add_row([(ci, vi, 1.0) for ci in range(N_CELLS)], 1.0, 1.0)

    for center in CENTERS:
        entries = [
            (CELLS.index((r, c)), vi, float(vi + 1))
            for (r, c) in well_cells(center)
            for vi in range(40)
        ]
        add_row(entries, float(TARGET_SUM), float(TARGET_SUM))

    A = lil_matrix(np.vstack([m.toarray() for m in rows]))
    result = milp(
        c=costs,
        constraints=LinearConstraint(A.tocsr(), np.array(lb), np.array(ub)),
        bounds=Bounds(np.zeros(N_VARS), np.ones(N_VARS)),
        integrality=np.ones(N_VARS),
        options={"time_limit": 300, "mip_rel_gap": 0.0},
    )
    if result.x is None or result.status not in (0, 1):
        raise RuntimeError(f"No feasible reconstruction found: {result.message}")

    solution = np.zeros(N_CELLS, dtype=int)
    for ci in range(N_CELLS):
        chosen = np.where(result.x[ci * 40 : (ci + 1) * 40] > 0.5)[0]
        if len(chosen) != 1:
            raise RuntimeError(f"Cell {CELLS[ci]} has {len(chosen)} assigned values")
        solution[ci] = chosen[0] + 1
    return solution


def build_grid(solution: np.ndarray) -> list[list[int | None]]:
    grid: list[list[int | None]] = [[None] * N for _ in range(N)]
    for ci, (r, c) in enumerate(CELLS):
        grid[r][c] = int(solution[ci])
    return grid


def verify(grid: list[list[int | None]]) -> None:
    flat = sorted(v for row in grid for v in row if v is not None)
    assert flat == VALUES, "values 1..40 must each appear exactly once"
    for center in CENTERS:
        total = sum(grid[r][c] for r, c in well_cells(center))
        assert total == TARGET_SUM, f"well {center} sums to {total}, expected {TARGET_SUM}"


def main() -> None:
    solution = solve()
    grid = build_grid(solution)
    verify(grid)

    print("corrected grid_data:")
    print(json.dumps(grid, ensure_ascii=False))

    changed = [
        (r, c, OBSERVED[r][c], grid[r][c])
        for r, c in CELLS
        if OBSERVED[r][c] != grid[r][c]
    ]
    print(f"\nchanged cells: {len(changed)} / {N_CELLS}")
    for r, c, old, new in changed:
        print(f"  ({r},{c}): {old} -> {new}")

    for center in CENTERS:
        cells = well_cells(center)
        total = sum(grid[r][c] for r, c in cells)
        print(f"well {center}: sum={total}  cells={[grid[r][c] for r, c in cells]}")


if __name__ == "__main__":
    main()
