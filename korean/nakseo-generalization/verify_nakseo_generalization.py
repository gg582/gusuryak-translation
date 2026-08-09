#!/usr/bin/env python3
"""낙서 보수 대합의 공통분모와 육고도 적용을 유한 집합으로 검증한다."""

from __future__ import annotations

from itertools import product


LO_SHU = ((4, 9, 2), (3, 5, 7), (8, 1, 6))


def complement(value: int, total: int) -> int:
    return total - value


def verify_lo_shu() -> None:
    for row, col in product(range(3), repeat=2):
        assert LO_SHU[row][col] + LO_SHU[2 - row][2 - col] == 10
    assert LO_SHU[1][1] == 5


def verify_yukgodo_orbits() -> None:
    # 중심을 지운 반지름 9 axial hexagon
    cells = [
        (q, r)
        for q in range(-9, 10)
        for r in range(-9, 10)
        if max(abs(q), abs(r), abs(q + r)) <= 9 and (q, r) != (0, 0)
    ]
    assert len(cells) == 270
    unseen = set(cells)
    pairs = []
    while unseen:
        cell = unseen.pop()
        opposite = (-cell[0], -cell[1])
        assert opposite in unseen
        unseen.remove(opposite)
        pairs.append((cell, opposite))
    assert len(pairs) == 135

    value_pairs = {(value, complement(value, 271)) for value in range(1, 136)}
    assert len(value_pairs) == 135
    assert all(left + right == 271 for left, right in value_pairs)

    # 대척 위치쌍과 값 보수쌍의 등변 배정은 항상 존재한다.
    assignment = {}
    for (left_cell, right_cell), (left_value, right_value) in zip(pairs, sorted(value_pairs)):
        assignment[left_cell] = left_value
        assignment[right_cell] = right_value
    assert all(assignment[cell] + assignment[(-cell[0], -cell[1])] == 271 for cell in cells)


def verify_sixfold_lift() -> None:
    assert all(6 * level + 6 * (10 - level) == 60 for level in range(1, 5))


def main() -> None:
    verify_lo_shu()
    verify_sixfold_lift()
    verify_yukgodo_orbits()
    print("통과: 3×3 낙서 대합, 6배 고리 상승, 135 위치쌍·135 값쌍 등변 배정")


if __name__ == "__main__":
    main()
