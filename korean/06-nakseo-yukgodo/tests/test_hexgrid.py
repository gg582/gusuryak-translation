#!/usr/bin/env python3
"""격자 기하 불변량 테스트. pytest 없이 직접 실행 가능:

    python3 tests/test_hexgrid.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from yukgodo.hexgrid import HexGrid, antipode, ring_of  # noqa: E402


def main() -> None:
    g = HexGrid()

    # 전체 칸 수: 271 (六觚一握)
    assert len(g.cells) == 271, len(g.cells)
    assert len(g.filled) == 270

    # 고리 크기: 1, 6, 12, ..., 54 (通加洛書數六倍 = 6×45)
    sizes = [len(r) for r in g.rings]
    assert sizes == [1, 6, 12, 18, 24, 30, 36, 42, 48, 54], sizes

    # 고리 순회 길이와 중복 없음
    for k in range(1, 10):
        walk = g.ring_walk[k]
        assert len(walk) == 6 * k
        assert len(set(walk)) == 6 * k
        assert all(ring_of(c) == k for c in walk)

    # 외주 54칸 (校計周五十四數), 변 10칸
    assert len(g.perimeter_walk()) == 54
    for side in g.sides:
        assert len(side) == 10
        assert all(ring_of(c) == 9 for c in side)
    # 6변의 합집합 = 외주, 꼭짓점만 두 변에 속함
    side_cells = [c for s in g.sides for c in s]
    assert len(set(side_cells)) == 54
    corners = set(g.corners())
    for c in set(side_cells):
        expect = 2 if c in corners else 1
        assert len(g.sides_of[c]) == expect, (c, g.sides_of[c])

    # 섹터: 45칸씩 270칸 분할
    assert all(len(w) == 45 for w in g.wedges)
    all_wedge = [c for w in g.wedges for c in w]
    assert len(set(all_wedge)) == 270
    assert set(all_wedge) == set(g.filled)
    # 대척점은 반대편 섹터로
    for i, w in enumerate(g.wedges):
        for c in w:
            assert g.wedge_of[antipode(c)] == (i + 3) % 6

    # 광선: 9칸씩, 섹터 i 안에 광선 i 포함
    assert all(len(r) == 9 for r in g.rays)
    for i, ray in enumerate(g.rays):
        for c in ray:
            assert g.wedge_of[c] == i

    # 축: 19칸 (十九爲中觚數也), 중심 포함
    for axis in g.axes:
        assert len(axis) == 19
        assert (0, 0) in axis
    # 中觚: 각 방향의 중앙 행 19칸
    for a in range(3):
        rows = g.rows(a)
        assert len(rows[0]) == 19
        assert all(len(rows[m]) == 19 - abs(m) for m in range(-9, 10))

    # 대척 슬롯: 135쌍, 전체 filled 분할
    assert len(g.slots) == 135
    slot_cells = [c for pair in g.slots for c in pair]
    assert len(set(slot_cells)) == 270
    for a, b in g.slots:
        assert antipode(a) == b and a != b

    print("모든 기하 불변량 테스트 통과")


if __name__ == "__main__":
    main()
