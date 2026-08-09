"""Find a non-antipodal countermodel while retaining the documented aggregates."""

from __future__ import annotations

import json
from pathlib import Path

from .hexgrid import HexGrid, ring_of
from .properties import measure, validate


def _profile(cell, grid):
    axes = tuple(i for i, axis in enumerate(grid.axes) if cell in axis)
    return ring_of(cell), axes, tuple(grid.sides_of.get(cell, ()))


def load_witness(path: Path, grid: HexGrid) -> dict:
    raw = json.loads(path.read_text(encoding="utf-8"))["values"]
    values = {tuple(map(int, key.split(","))): value for key, value in raw.items()}
    if validate(values, grid):
        raise ValueError("saved witness is not a 1..270 placement")
    return values


def find_countermodel(values: dict, grid: HexGrid):
    before = measure(values, grid)
    for i, left in enumerate(grid.filled):
        for right in grid.filled[i + 1:]:
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
    raise RuntimeError("no suitable countermodel found")


def audit(path: Path = Path("output/solution.json")) -> dict:
    grid = HexGrid()
    values = load_witness(path, grid)
    candidate, left, right = find_countermodel(values, grid)
    after = measure(candidate, grid)
    return {
        "verdict": "not_derived_without_equivariance",
        "swap": [left, right, values[left], values[right]],
        "pairs_still_summing_271": sum(dev == 0 for dev in after.pair_devs),
        "pair_count": len(after.pair_devs),
    }


if __name__ == "__main__":
    print(audit())
