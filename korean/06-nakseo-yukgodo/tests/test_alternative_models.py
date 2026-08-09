#!/usr/bin/env python3
"""대척 대안 조건의 기본 불변량 회귀 검사."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from yukgodo.alternative_models import (  # noqa: E402
    _groups, global_nonantipodal_pairs, ring_adjacent_pairs, rotation_orbits, rotate60,
)
from yukgodo.hexgrid import HexGrid, antipode  # noqa: E402


def main() -> None:
    grid = HexGrid()
    assert all(rotate60(rotate60(rotate60(c))) == antipode(c) for c in grid.filled)
    orbits = rotation_orbits(grid)
    assert len(orbits) == 45 and all(len(orbit) == 6 for orbit in orbits)
    assert set(c for orbit in orbits for c in orbit) == set(grid.filled)
    groups = _groups()
    assert len(groups) == 45 and all(sum(group) == 813 for group in groups)
    assert sorted(v for group in groups for v in group) == list(range(1, 271))
    for slots in (ring_adjacent_pairs(grid), global_nonantipodal_pairs(grid)):
        assert len(slots) == 135
        assert len({c for pair in slots for c in pair}) == 270
        assert all(antipode(a) != b for a, b in slots)
    print("대척 대안 모델 불변량 테스트 통과")


if __name__ == "__main__":
    main()
