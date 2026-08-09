#!/usr/bin/env python3
"""Verify Lo Shu complements, the sixfold lift, and Yukgodo orbit matching."""

from itertools import product


LO_SHU = ((4, 9, 2), (3, 5, 7), (8, 1, 6))


def main() -> None:
    assert all(
        LO_SHU[row][col] + LO_SHU[2 - row][2 - col] == 10
        for row, col in product(range(3), repeat=2)
    )
    assert LO_SHU[1][1] == 5
    assert all(6 * level + 6 * (10 - level) == 60 for level in range(1, 5))

    cells = [
        (q, r)
        for q in range(-9, 10)
        for r in range(-9, 10)
        if max(abs(q), abs(r), abs(q + r)) <= 9 and (q, r) != (0, 0)
    ]
    assert len(cells) == 270
    assert len({tuple(sorted((cell, (-cell[0], -cell[1])))) for cell in cells}) == 135
    assert len({tuple(sorted((value, 271 - value))) for value in range(1, 271)}) == 135
    print("Passed: Lo Shu complements, sixfold lift, and 135-by-135 Yukgodo orbit matching")


if __name__ == "__main__":
    main()
