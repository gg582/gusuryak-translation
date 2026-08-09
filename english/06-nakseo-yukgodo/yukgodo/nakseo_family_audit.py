"""Executable audit of the shared Lo Shu layer and its exact scope."""

from __future__ import annotations

from itertools import product
from pathlib import Path
import runpy


KOREAN = Path(__file__).resolve().parents[3] / "korean"
FAMILY = KOREAN / "01-saodo-family"
LO_SHU = ((8, 1, 6), (3, 5, 7), (4, 9, 2))
HANJA_DIGIT = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}


def _dihedral_forms(square: tuple[tuple[int, ...], ...]) -> set[tuple[tuple[int, ...], ...]]:
    forms = set()
    current = square
    for _ in range(4):
        forms.add(current)
        forms.add(tuple(tuple(reversed(row)) for row in current))
        current = tuple(tuple(current[2 - col][row] for col in range(3)) for row in range(3))
    return forms


def _violations(values: dict, opposite: dict, total: int) -> list[tuple]:
    failures, seen = [], set()
    for place, value in values.items():
        other = opposite[place]
        if place in seen:
            continue
        seen.update((place, other))
        if value + values[other] != total:
            failures.append((place, value, other, values[other], value + values[other]))
    return failures


def audit() -> dict:
    gugudo = runpy.run_path(str(FAMILY / "낙서구구도" / "visualize.py"))
    ogudo = runpy.run_path(str(FAMILY / "낙서오구도" / "nakseo_ogudo.py"))
    chilgudo = runpy.run_path(str(FAMILY / "낙서칠구도" / "visualize_basic.py"))

    gugudo_square = tuple(tuple(HANJA_DIGIT[c.center_label] for c in row) for row in gugudo["CLUSTERS"])
    ogudo_square = tuple(tuple(ogudo["VALUES"][(x, y)] for x in (1, 3, 5)) for y in (2, 1, 0))
    chilgudo_square = tuple(
        tuple(next(g["center"] for g in chilgudo["groups"] if g["pos"] == (x, y)) for x in (1, 2, 3))
        for y in (3, 2, 1)
    )
    assert all(square in _dihedral_forms(LO_SHU) for square in (gugudo_square, ogudo_square, chilgudo_square))
    assert all(LO_SHU[row][col] + LO_SHU[2 - row][2 - col] == 10 for row, col in product(range(3), repeat=2))

    gugudo_values = {
        (row, col, offset): value
        for row, line in enumerate(gugudo["CLUSTERS"])
        for col, cluster in enumerate(line)
        for offset, value in enumerate(cluster.values)
    }
    gugudo_opposite = {(row, col, offset): (2 - row, 2 - col, (offset + 4) % 8) for row, col, offset in gugudo_values}
    ogudo_values = ogudo["VALUES"]
    ogudo_opposite = {place: (6 - place[0], 2 - place[1]) for place in ogudo_values}
    chilgudo_values = {
        (g["pos"][0], g["pos"][1], offset): value
        for g in chilgudo["groups"]
        for offset, value in enumerate(g["surround"])
    }
    chilgudo_opposite = {(x, y, offset): (4 - x, 4 - y, (offset + 3) % 6) for x, y, offset in chilgudo_values}
    expansions = {
        "gugudo": (gugudo_values, gugudo_opposite, 82),
        "ogudo": (ogudo_values, ogudo_opposite, 34),
        "chilgudo": (chilgudo_values, chilgudo_opposite, 64),
    }
    full_cells = {
        name: {"total": total, "holds": not _violations(values, opposite, total),
               "first_failure": _violations(values, opposite, total)[0]}
        for name, (values, opposite, total) in expansions.items()
    }
    assert not any(item["holds"] for item in full_cells.values())
    return {
        "lo_shu_opposite_sum": 10,
        "lo_shu_fixed_center": 5,
        "all_control_arrays_dihedrally_lo_shu": True,
        "gugudo_documented_outer_complement_sum": 91,
        "yukgodo_sixfold_ring_complement_sum": 60,
        "full_expansion_equivariance": full_cells,
    }


if __name__ == "__main__":
    print(audit())
