"""yukgodo2 — property comparison of the two reconstruction hypotheses.

Measures the parent project's antipodal-complement witness
(../output/solution.json) and this repo's consecutive ring-value solution
(output/solution.json) with the same geometric indicators, and writes
output/comparison.{json,md}.

Indicator targets (per the parent README):
    ring k sum 813k, wedge 6097/6098, ray 1219/1220, side 1355,
    axis 2439 (18 cells excluding the center), corner sum 813 (=3×271),
    antipodal pair sum 271.
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from yukgodo.hexgrid import HexGrid

RADIUS = 9
TARGETS = {
    "ring_sums": [813 * k for k in range(1, RADIUS + 1)],
    "wedge_sums": [6097.5] * 6,
    "ray_sums": [1219.5] * 6,
    "side_sums": [1355] * 6,
    "axis_sums": [2439] * 3,
    "corner_sum": 813,
}


def load_values(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        tuple(map(int, key.split(","))): value
        for key, value in data["values"].items()
    }


def metrics(grid, values):
    def total(cells):
        return sum(values[c] for c in cells if c in values)

    pair_sums = [values[a] + values[b] for a, b in grid.slots]

    return {
        "ring_sums": [total(grid.rings[k]) for k in range(1, RADIUS + 1)],
        "wedge_sums": [total(w) for w in grid.wedges],
        "ray_sums": [total(r) for r in grid.rays],
        "side_sums": [total(s) for s in grid.sides],
        "axis_sums": [total(a) for a in grid.axes],
        "corner_sum": total(grid.corners()),
        "antipodal_pair_sum_min": min(pair_sums),
        "antipodal_pair_sum_max": max(pair_sums),
        "antipodal_pairs_eq_271": sum(1 for s in pair_sums if s == 271),
    }


def max_deviation(series, target):
    return max(abs(s - target) for s in series)


def main():
    grid = HexGrid()

    antipodal = metrics(
        grid, load_values(HERE.parent / "output" / "solution.json")
    )
    consecutive = metrics(grid, load_values(HERE / "output" / "solution.json"))

    result = {"antipodal": antipodal, "consecutive": consecutive}
    (HERE / "output" / "comparison.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    lines = []
    lines.append("# Geometric indicators of the two reconstruction hypotheses")
    lines.append("")
    lines.append(
        "The antipodal-complement witness (parent `output/solution.json`, "
        "seed 1715) and the consecutive ring-value solution "
        "(`yukgodo2/output/solution.json`) measured with the same grid "
        "indicators."
    )
    lines.append("")

    lines.append("## Ring sums (target 813k)")
    lines.append("")
    lines.append("| ring k | target 813k | antipodal | consecutive (18k³+3k) |")
    lines.append("| ---: | ---: | ---: | ---: |")
    for k in range(1, RADIUS + 1):
        lines.append(
            f"| {k} | {813 * k} | {antipodal['ring_sums'][k - 1]} "
            f"| {consecutive['ring_sums'][k - 1]} |"
        )
    lines.append("")

    def simple_section(title, key, target):
        lines.append(f"## {title} (target {target})")
        lines.append("")
        lines.append("| indicator | antipodal | consecutive |")
        lines.append("| --- | --- | --- |")
        lines.append(
            f"| values | {antipodal[key]} | {consecutive[key]} |"
        )
        lines.append(
            f"| max deviation | {max_deviation(antipodal[key], target)} "
            f"| {max_deviation(consecutive[key], target)} |"
        )
        lines.append("")

    simple_section("Wedge (觚) sums", "wedge_sums", 6097.5)
    simple_section("Ray sums", "ray_sums", 1219.5)
    simple_section("Outer side sums", "side_sums", 1355)
    simple_section("Axis (中觚 family) sums", "axis_sums", 2439)

    lines.append("## Antipodal pairs and corners")
    lines.append("")
    lines.append("| indicator | antipodal | consecutive |")
    lines.append("| --- | ---: | ---: |")
    lines.append(
        f"| pairs summing to 271 (of 135) "
        f"| {antipodal['antipodal_pairs_eq_271']} "
        f"| {consecutive['antipodal_pairs_eq_271']} |"
    )
    lines.append(
        f"| pair-sum min–max "
        f"| {antipodal['antipodal_pair_sum_min']}–{antipodal['antipodal_pair_sum_max']} "
        f"| {consecutive['antipodal_pair_sum_min']}–{consecutive['antipodal_pair_sum_max']} |"
    )
    lines.append(
        f"| corner sum (structural target 813) "
        f"| {antipodal['corner_sum']} | {consecutive['corner_sum']} |"
    )
    lines.append("")
    lines.append(
        "The consecutive solution's indicators are fixed only up to "
        "rotation by the chosen normalization of start point and "
        "direction (rotating permutes the wedge/ray/side values). "
        "Neither arrangement is a directly transcribed placement."
    )
    lines.append("")

    (HERE / "output" / "comparison.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )

    print(f"comparison written -> {HERE / 'output'}")
    print(f"  antipodal   : rings all 813k = "
          f"{all(s == 813 * (i + 1) for i, s in enumerate(antipodal['ring_sums']))}, "
          f"pairs=271: {antipodal['antipodal_pairs_eq_271']}/135")
    print(f"  consecutive : pairs=271: {consecutive['antipodal_pairs_eq_271']}/135, "
          f"corner sum {consecutive['corner_sum']}")


if __name__ == "__main__":
    main()
