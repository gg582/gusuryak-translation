"""대척보수 가설의 논리적 지위를 감사한다.

기존 ``solver.py``는 처음부터 각 대척 슬롯에 ``(i, 271-i)``를 넣는다.
그러므로 그 솔버의 해는 대척보수를 *검증*할 수는 있어도, 원문 기하나 집계합에서
그 조건이 *도출된다*는 증거는 될 수 없다.

이 모듈은 저장된 조건부 증인해에서 같은 고리·같은 축 소속·같은 변 소속인 두 셀을
맞바꾼다. 이 교환은 다음을 보존한다.

* 값 집합 1..270 및 총합,
* 각 고리합,
* 세 中觚 축합,
* 여섯 외변합.

그러나 일반적으로 해당 두 대척 슬롯의 합은 271이 아니게 된다. 따라서 이 집계들은
대척보수의 결과와 양립할 수는 있어도, 그 위치-값 대응을 논리적으로 강제하지는 못한다.
"""

from __future__ import annotations

import json
from pathlib import Path

from .hexgrid import Cell, HexGrid, ring_of
from .properties import measure, validate


def _axis_membership(cell: Cell, grid: HexGrid) -> tuple[int, ...]:
    return tuple(i for i, axis in enumerate(grid.axes) if cell in axis)


def _profile(cell: Cell, grid: HexGrid) -> tuple[int, tuple[int, ...], tuple[int, ...]]:
    """교환 뒤에도 고리·축·변 합이 같은 셀의 소속 프로필."""
    return (
        ring_of(cell),
        _axis_membership(cell, grid),
        tuple(grid.sides_of.get(cell, ())),
    )


def load_witness(path: Path, grid: HexGrid) -> dict[Cell, int]:
    raw = json.loads(path.read_text(encoding="utf-8"))["values"]
    values = {tuple(map(int, key.split(","))): value for key, value in raw.items()}
    errors = validate(values, grid)
    if errors:
        raise ValueError(f"조건부 증인해가 기본 값 조건을 만족하지 않음: {errors}")
    return values


def find_countermodel(values: dict[Cell, int], grid: HexGrid) -> tuple[dict[Cell, int], Cell, Cell]:
    """지정한 집계를 보존하지만 대척합을 깨는 한 번의 교환을 찾는다."""
    before = measure(values, grid)
    cells = grid.filled
    for i, left in enumerate(cells):
        for right in cells[i + 1:]:
            if _profile(left, grid) != _profile(right, grid):
                continue
            candidate = values.copy()
            candidate[left], candidate[right] = candidate[right], candidate[left]
            after = measure(candidate, grid)
            if (
                after.ring_sums == before.ring_sums
                and after.axis_sums == before.axis_sums
                and after.side_sums == before.side_sums
                and all(6097 <= value <= 6098 for value in after.wedge_sums)
                and all(1219 <= value <= 1220 for value in after.ray_sums)
                and after.parts["pairs"] > 0
            ):
                return candidate, left, right
    raise RuntimeError("집계를 보존하는 대척-비보수 교환을 찾지 못함")


def audit(witness_path: Path = Path("output/solution.json")) -> dict[str, object]:
    grid = HexGrid()
    values = load_witness(witness_path, grid)
    before = measure(values, grid)
    candidate, left, right = find_countermodel(values, grid)
    after = measure(candidate, grid)

    assert not validate(candidate, grid)
    assert after.ring_sums == before.ring_sums
    assert after.axis_sums == before.axis_sums
    assert after.side_sums == before.side_sums
    assert all(6097 <= value <= 6098 for value in after.wedge_sums)
    assert all(1219 <= value <= 1220 for value in after.ray_sums)
    assert after.parts["pairs"] > 0

    return {
        "verdict": "not_derived",
        "method": "same-profile value transposition",
        "preserved": {
            "value_set_1_to_270": True,
            "total": after.total,
            "ring_sums": after.ring_sums[1:],
            "axis_sums": after.axis_sums,
            "side_sums": after.side_sums,
        },
        "swap": {
            "cells": [list(left), list(right)],
            "values_before": [values[left], values[right]],
            "profile": {
                "ring": ring_of(left),
                "axes": list(_axis_membership(left, grid)),
                "sides": list(grid.sides_of.get(left, ())),
            },
        },
        "antipodal": {
            "before_all_pairs_sum_271": before.parts["pairs"] == 0,
            "after_pair_absolute_deviation": after.parts["pairs"],
            "after_pairs_summing_271": sum(dev == 0 for dev in after.pair_devs),
            "number_of_pairs": len(after.pair_devs),
        },
        "also_satisfies_solver_balance_ranges": {
            "wedge_sums": after.wedge_sums,
            "ray_sums": after.ray_sums,
        },
        "scope": (
            "이 반례는 원문 기하 및 보존된 집계가 대척보수를 논리적으로 함의하지 "
            "않음을 보인다. 대척보수가 역사적으로 유력한 복원 원리인지의 평가는 "
            "별도의 문헌·도상 증거 문제다."
        ),
    }


def main() -> None:
    report = audit()
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
