"""중심 공백 7칸 도형과 육고도의 대척보수 구조를 비교한다."""

from __future__ import annotations

from .hexgrid import HexGrid, antipode


def report() -> dict[str, int | bool]:
    """반지름 1과 9에서 중심 공백 뒤 남는 대척 궤도를 검산한다."""
    small = HexGrid(radius=1)
    full = HexGrid(radius=9)
    assert len(small.cells) == 7
    assert len(small.filled) == 6
    assert len(small.slots) == 3
    assert all(antipode(a) == b for a, b in small.slots)

    assert len(full.cells) == 271
    assert len(full.filled) == 270
    assert len(full.slots) == 135

    return {
        "small_cells": len(small.cells),
        "small_center_removed": len(small.filled) == 6,
        "small_antipodal_pairs": len(small.slots),
        "full_cells": len(full.cells),
        "full_center_removed": len(full.filled) == 270,
        "full_antipodal_pairs": len(full.slots),
        "small_value_complement_sum": 7,
        "full_value_complement_sum": 271,
    }


def main() -> None:
    for key, value in report().items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
