#!/usr/bin/env python3
"""Deterministic Spiral-Wedge Equalizer Solver.

Principle:
When placing antipodal complement pairs (v, 271-v) into 135 slots,
balance across 6 sides (target: 1355), 6 sectors (target: 6097/6098),
and 6 rays (target: 1219/1220) is achieved without randomness, via a
pure 'Deterministic Rotation & Flip Rule', generating a candidate optimal solution.
"""

from __future__ import annotations

import argparse
import json
import math
import os

from yukgodo.hexgrid import HexGrid, PAIR_SUM, Cell, antipode
from yukgodo.properties import PENALTY_FLOOR, measure, validate


def solve_deterministic_equalizer(grid: HexGrid) -> tuple[dict[Cell, int], float]:
    """Construct a solution using only pure deterministic symmetry/rotation alternation rules, without any random seed."""
    values: dict[Cell, int] = {}
    
    # 1. Deterministically sort 135 slots by (ring number k, CCW phase θ)
    slots = grid.slots
    slot_info = []
    for s, (ca, cb) in enumerate(slots):
        ring = max(abs(ca[0]), abs(ca[1]), abs(ca[0] + ca[1]))
        wedge = grid.wedge_of[ca]
        # Axial angle order
        angle = math.atan2(ca[1], ca[0])
        slot_info.append((ring, wedge, angle, s, ca, cb))
        
    # Deterministic primary sort (external order within ring, sector alternation)
    slot_info.sort(key=lambda x: (x[0], x[1], x[2]))
    
    # 2. Deterministic value assignment with directional flip rotation rule
    # Assign 1..135 pairs to slot positions by ring and sector, alternating CCW
    for rank, (ring, wedge, _, s, ca, cb) in enumerate(slot_info, start=1):
        val_small = rank
        val_large = PAIR_SUM - rank
        
        # Deterministic flip rule: direction determined by parity of (wedge + ring + rank)
        flip = ((wedge * 2 + ring + rank) % 2 == 0)
        
        va, vb = (val_large, val_small) if flip else (val_small, val_large)
        values[ca] = va
        values[cb] = vb
        
    rep = measure(values, grid)
    return values, rep.penalty


def main():
    grid = HexGrid()
    vals, pen = solve_deterministic_equalizer(grid)
    print(f"=== Deterministic Equalizer Solver ===")
    print(f"  - Random seed used: 0% (fully deterministic)")
    print(f"  - Measured penalty: {pen:.1f}")
    
    errs = validate(vals, grid)
    print(f"  - Grid validation: {'Pass (Valid)' if not errs else errs}")
    
if __name__ == "__main__":
    main()
