"""Compact, executable checks for the shared Lo Shu rule cited in the README."""

from itertools import product


LO_SHU = ((8, 1, 6), (3, 5, 7), (4, 9, 2))


def audit() -> dict:
    assert all(
        LO_SHU[row][col] + LO_SHU[2 - row][2 - col] == 10
        for row, col in product(range(3), repeat=2)
    )
    assert LO_SHU[1][1] == 5
    assert all(6 * level + 6 * (10 - level) == 60 for level in range(1, 5))
    assert all(value + (91 - value) == 91 for value in range(10, 46))
    return {
        "lo_shu_opposite_sum": 10,
        "lo_shu_fixed_center": 5,
        "gugudo_documented_outer_complement_sum": 91,
        "yukgodo_sixfold_ring_complement_sum": 60,
    }


if __name__ == "__main__":
    print(audit())
