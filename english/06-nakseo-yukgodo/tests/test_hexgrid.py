#!/usr/bin/env python3
"""Lattice geometry invariant tests. Runnable directly without pytest:

    python3 tests/test_hexgrid.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from yukgodo.hexgrid import HexGrid, antipode, ring_of  # noqa: E402


def main() -> None:
    g = HexGrid()

    # total cells: 271 (六觚一握)
    assert len(g.cells) == 271, len(g.cells)
    assert len(g.filled) == 270

    # ring sizes: 1, 6, 12, ..., 54 (通加洛書數六倍 = 6×45)
    sizes = [len(r) for r in g.rings]
    assert sizes == [1, 6, 12, 18, 24, 30, 36, 42, 48, 54], sizes

    # ring walk lengths and no duplicates
    for k in range(1, 10):
        walk = g.ring_walk[k]
        assert len(walk) == 6 * k
        assert len(set(walk)) == 6 * k
        assert all(ring_of(c) == k for c in walk)

    # perimeter 54 cells (校計周五十四數), sides of 10 cells
    assert len(g.perimeter_walk()) == 54
    for side in g.sides:
        assert len(side) == 10
        assert all(ring_of(c) == 9 for c in side)
    # union of the 6 sides = perimeter; only corners belong to two sides
    side_cells = [c for s in g.sides for c in s]
    assert len(set(side_cells)) == 54
    corners = set(g.corners())
    for c in set(side_cells):
        expect = 2 if c in corners else 1
        assert len(g.sides_of[c]) == expect, (c, g.sides_of[c])

    # sectors: 45 cells each, partitioning the 270 cells
    assert all(len(w) == 45 for w in g.wedges)
    all_wedge = [c for w in g.wedges for c in w]
    assert len(set(all_wedge)) == 270
    assert set(all_wedge) == set(g.filled)
    # antipodes map to the opposite sector
    for i, w in enumerate(g.wedges):
        for c in w:
            assert g.wedge_of[antipode(c)] == (i + 3) % 6

    # rays: 9 cells each; ray i lies inside sector i
    assert all(len(r) == 9 for r in g.rays)
    for i, ray in enumerate(g.rays):
        for c in ray:
            assert g.wedge_of[c] == i

    # axes: 19 cells (十九爲中觚數也), including the center
    for axis in g.axes:
        assert len(axis) == 19
        assert (0, 0) in axis
    # 中觚: the middle row of each direction has 19 cells
    for a in range(3):
        rows = g.rows(a)
        assert len(rows[0]) == 19
        assert all(len(rows[m]) == 19 - abs(m) for m in range(-9, 10))

    # antipodal slots: 135 pairs partitioning all filled cells
    assert len(g.slots) == 135
    slot_cells = [c for pair in g.slots for c in pair]
    assert len(set(slot_cells)) == 270
    for a, b in g.slots:
        assert antipode(a) == b and a != b

    print("all geometry invariant tests passed")


if __name__ == "__main__":
    main()
