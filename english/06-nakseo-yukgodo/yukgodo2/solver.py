"""yukgodo2 — consecutive ring-value reconstruction solver (六包一/逓加 family).

Encodes the arithmetic structure directly supported by the manuscript
(逓加 ring sizes 6k, the 來積法 chain, 虛一) as Z3 constraints, then places
values 1..270 under the consecutive ring-value hypothesis.

- ring k receives the consecutive interval 3k(k−1)+1 … 3k(k+1)
- within each ring, values proceed consecutively around the circumference
- the starting point and direction of each ring are a normalization of
  rotational symmetry, not a manuscript claim

Results are written to output/ (solution.json, report.md, reconstruction.png).
"""

import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from z3 import Distinct, Int, Solver, Sum, sat

plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK JP",
    "DejaVu Sans",
    "Droid Sans Fallback",
]
plt.rcParams["font.family"] = "sans-serif"

RING_STEP = 6
LUOSHU_ORDER = 9
OUTPUT_DIR = Path(__file__).resolve().parent / "output"

# Report language: this repo is English
LANG = "en"


def build_arithmetic_solver():
    """Reconstruct the manuscript's numerical structure as Z3 constraints.

    逓加 path:
        6, 12, 18, ..., 54
        6 * (1 + 2 + ... + 9) = 270

    六包一 series (Gyowusa edition, Kun volume, p. 11):
        1 + (6 + 12 + ... + 54) = 271  (one center wrapped by rings of 6k)
        after 虛一: 270 occupied cells

    來積法 path:
        54 + 6 = 60
        60 / 6 = 10
        2 * 10 - 1 = 19
        19 - 1 = 18
        54 / 6 = 9
        (10 + 18) * 9 = 252
        252 + 19 = 271
    """

    solver = Solver()

    ring_count = Int("ring_count")
    outer_count = Int("outer_count")
    side_total = Int("side_total")
    side_count = Int("side_count")
    middle_span = Int("middle_span")
    adjacent_span = Int("adjacent_span")

    non_middle_count = Int("non_middle_count")
    geometric_total = Int("geometric_total")

    luoshu_sum = Int("luoshu_sum")
    occupied_count = Int("occupied_count")
    void_count = Int("void_count")

    ring_sizes = {
        k: Int(f"ring_size_{k}")
        for k in range(1, LUOSHU_ORDER + 1)
    }

    solver.add(ring_count > 0)

    # 枚外周五十四數
    solver.add(outer_count == 54)

    # 以筭法則係以六，逓加
    for k in range(1, LUOSHU_ORDER + 1):
        solver.add(ring_sizes[k] == RING_STEP * k)

    solver.add(ring_count == LUOSHU_ORDER)
    solver.add(ring_sizes[LUOSHU_ORDER] == outer_count)

    # 洛書數 = 1 + 2 + ... + 9
    solver.add(luoshu_sum == Sum(list(range(1, LUOSHU_ORDER + 1))))

    # 逓加洛書數六倍
    solver.add(
        occupied_count
        == Sum([ring_sizes[k] for k in range(1, LUOSHU_ORDER + 1)])
    )
    solver.add(occupied_count == RING_STEP * luoshu_sum)

    # 虛一
    solver.add(void_count == 1)
    solver.add(geometric_total == occupied_count + void_count)

    # 來積法: 外周添六
    solver.add(side_total == outer_count + 6)

    # 六歸之得一十
    solver.add(side_total == 6 * side_count)

    # 倍之得二十，減一為十九，為中觚數
    solver.add(middle_span == 2 * side_count - 1)

    # after removing the 中觚, the adjacent maximum span remains
    solver.add(adjacent_span == middle_span - 1)

    # the nine steps agree with the outer count
    solver.add(outer_count == 6 * ring_count)

    # reconstructed field-style area relation
    solver.add(
        non_middle_count == (side_count + adjacent_span) * ring_count
    )

    # restore the 中觚
    solver.add(geometric_total == non_middle_count + middle_span)

    variables = {
        "ring_count": ring_count,
        "outer_count": outer_count,
        "side_total": side_total,
        "side_count": side_count,
        "middle_span": middle_span,
        "adjacent_span": adjacent_span,
        "non_middle_count": non_middle_count,
        "geometric_total": geometric_total,
        "luoshu_sum": luoshu_sum,
        "occupied_count": occupied_count,
        "void_count": void_count,
        "ring_sizes": ring_sizes,
    }

    return solver, variables


def solve_arithmetic():
    solver, variables = build_arithmetic_solver()

    if solver.check() != sat:
        raise RuntimeError("The manuscript arithmetic is inconsistent.")

    model = solver.model()

    result = {
        name: model.evaluate(variable).as_long()
        for name, variable in variables.items()
        if name != "ring_sizes"
    }
    result["ring_sizes"] = {
        k: model.evaluate(variable).as_long()
        for k, variable in variables["ring_sizes"].items()
    }

    return result


def hex_distance(cell):
    q, r = cell
    return max(abs(q), abs(r), abs(q + r))


def build_hex_grid(radius):
    cells = []
    for q in range(-radius, radius + 1):
        for r in range(-radius, radius + 1):
            if hex_distance((q, r)) <= radius:
                cells.append((q, r))
    return cells


def ring_cells(radius):
    """Return one complete hexagonal ring in cyclic order.

    The chosen start point and direction are coordinate conventions.
    They are not claimed to be specified by the manuscript.
    """

    if radius == 0:
        return [(0, 0)]

    directions = [
        (1, 0),
        (0, 1),
        (-1, 1),
        (-1, 0),
        (0, -1),
        (1, -1),
    ]

    q, r = 0, -radius
    result = []

    for dq, dr in directions:
        for _ in range(radius):
            result.append((q, r))
            q += dq
            r += dr

    assert len(result) == 6 * radius
    assert all(hex_distance(cell) == radius for cell in result)

    return result


def ring_value_range(ring):
    """Consecutive ring-value hypothesis: ring k takes the next 6k values.

    Ring 1: 1..6, ring 2: 7..18, …, ring 9: 217..270
    """

    previous_total = 3 * (ring - 1) * ring
    current_total = 3 * ring * (ring + 1)
    return previous_total + 1, current_total


def ring_sum(ring):
    """Ring k sum under this hypothesis = 18k³ + 3k (not the 813k of the
    antipodal-complement hypothesis)."""

    first, last = ring_value_range(ring)
    return 6 * ring * (first + last) // 2


def build_value_solver(arithmetic):
    """Fill all noncentral cells.

    Manuscript-derived constraints:
        - center is void
        - ring k contains 6k positions
        - total occupied positions = 270

    Reconstruction hypothesis used to recover individual values:
        - values are 1..270
        - ring k receives its corresponding consecutive range
        - values progress consecutively around each ring
    """

    radius = arithmetic["ring_count"]
    all_cells = build_hex_grid(radius)
    center = (0, 0)
    occupied_cells = [cell for cell in all_cells if cell != center]

    solver = Solver()
    values = {
        cell: Int(f"value_{cell[0]}_{cell[1]}") for cell in occupied_cells
    }

    for variable in values.values():
        solver.add(variable >= 1)
        solver.add(variable <= arithmetic["occupied_count"])

    solver.add(Distinct(list(values.values())))

    for ring in range(1, radius + 1):
        cells = ring_cells(ring)
        first_value, last_value = ring_value_range(ring)

        assert last_value - first_value + 1 == 6 * ring

        for cell in cells:
            solver.add(values[cell] >= first_value)
            solver.add(values[cell] <= last_value)

        # strong reconstruction hypothesis: values proceed consecutively
        # around the ring
        for index, cell in enumerate(cells):
            solver.add(values[cell] == first_value + index)

    return solver, values, all_cells


def solve_values(arithmetic):
    solver, variables, all_cells = build_value_solver(arithmetic)

    if solver.check() != sat:
        raise RuntimeError("The value reconstruction is inconsistent.")

    model = solver.model()
    values = {
        cell: model.evaluate(variable).as_long()
        for cell, variable in variables.items()
    }

    return values, all_cells


def verify_reconstruction(arithmetic, values, all_cells):
    radius = arithmetic["ring_count"]

    assert len(all_cells) == arithmetic["geometric_total"]
    assert len(values) == arithmetic["occupied_count"]
    assert (0, 0) not in values
    assert sorted(values.values()) == list(
        range(1, arithmetic["occupied_count"] + 1)
    )

    for ring in range(1, radius + 1):
        cells = ring_cells(ring)
        assert len(cells) == arithmetic["ring_sizes"][ring]

        actual_values = sorted(values[cell] for cell in cells)
        first_value, last_value = ring_value_range(ring)
        assert actual_values == list(range(first_value, last_value + 1))

        actual_sum = sum(values[cell] for cell in cells)
        assert actual_sum == ring_sum(ring)


def axial_to_xy(cell):
    q, r = cell
    x = math.sqrt(3) * (q + r / 2)
    y = 1.5 * r
    return x, y


def draw_reconstruction(arithmetic, values, all_cells, path):
    radius = arithmetic["ring_count"]

    fig, ax = plt.subplots(figsize=(16, 16))

    for cell in all_cells:
        x, y = axial_to_xy(cell)
        distance = hex_distance(cell)
        is_center = cell == (0, 0)
        is_outer = distance == radius

        patch = RegularPolygon(
            (x, y),
            numVertices=6,
            radius=0.98,
            orientation=0,
            facecolor="none",
            edgecolor="black",
            linewidth=1.6 if is_outer else 0.6,
        )
        ax.add_patch(patch)

        if is_center:
            ax.text(x, y, "虛", ha="center", va="center", fontsize=10)
        else:
            ax.text(
                x, y, str(values[cell]),
                ha="center", va="center", fontsize=5,
            )

    ax.set_aspect("equal")
    ax.autoscale_view()
    ax.axis("off")
    ax.set_title(
        "yukgodo2 — consecutive ring-value reconstruction\n"
        "六包一: 1+(6+12+…+54) = 271 | 270 occupied after 虛一",
        fontsize=14,
    )

    plt.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def write_solution(arithmetic, values, path):
    data = {
        "hypothesis": "consecutive ring values (六包一/逓加 series)",
        "arithmetic": {
            name: (value if name != "ring_sizes" else
                   {str(k): v for k, v in value.items()})
            for name, value in arithmetic.items()
        },
        "ring_value_ranges": {
            str(k): list(ring_value_range(k))
            for k in range(1, arithmetic["ring_count"] + 1)
        },
        "ring_sums": {
            str(k): ring_sum(k)
            for k in range(1, arithmetic["ring_count"] + 1)
        },
        "values": {
            f"{q},{r}": value for (q, r), value in sorted(values.items())
        },
    }
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def write_report(arithmetic, path):
    lines = []
    a = arithmetic

    lines.append("# yukgodo2 — consecutive ring-value reconstruction results")
    lines.append("")
    lines.append("## Arithmetic chain (text-supported part, Z3-verified)")
    lines.append("")
    lines.append("```")
    lines.append(
        f"逓加: 6 + 12 + … + 54 = {a['occupied_count']} "
        f"= 6 × {a['luoshu_sum']}"
    )
    lines.append(
        f"六包一 series: 1 + (6 + 12 + … + 54) = {a['geometric_total']}"
    )
    lines.append(
        f"來積法: {a['outer_count']} + 6 = {a['side_total']}, "
        f"{a['side_total']} ÷ 6 = {a['side_count']}, "
        f"2 × {a['side_count']} − 1 = {a['middle_span']}"
    )
    lines.append(
        f"        ({a['side_count']} + {a['adjacent_span']}) "
        f"× {a['ring_count']} = {a['non_middle_count']}, "
        f"{a['non_middle_count']} + {a['middle_span']} "
        f"= {a['geometric_total']}"
    )
    lines.append(
        f"虛一: {a['geometric_total']} − {a['void_count']} "
        f"= {a['occupied_count']}"
    )
    lines.append("```")
    lines.append("")
    lines.append("## Placement by ring (reconstruction hypothesis)")
    lines.append("")
    lines.append("| ring k | cells 6k | value range | ring sum 18k³+3k |")
    lines.append("| ---: | ---: | --- | ---: |")
    for k in range(1, a["ring_count"] + 1):
        first, last = ring_value_range(k)
        lines.append(
            f"| {k} | {a['ring_sizes'][k]} | {first}..{last} "
            f"| {ring_sum(k)} |"
        )
    lines.append("")
    lines.append("## Verification")
    lines.append("")
    lines.append(
        f"- grid cells = {a['geometric_total']} (central void 1 + occupied "
        f"{a['occupied_count']})"
    )
    lines.append("- values 1..270 are each placed exactly once")
    lines.append(
        "- every ring's value set matches its consecutive interval exactly"
    )
    lines.append("- every ring sum matches 18k³+3k exactly")
    lines.append("")
    lines.append("## Interpretive boundary")
    lines.append("")
    lines.append(
        "This arrangement is a separate candidate from the "
        "antipodal-complement hypothesis (ring sums 813k). The starting "
        "point and direction of each ring are a normalization of "
        "rotational symmetry; there is no evidence that the text directly "
        "prescribes this value placement. The alignment with the 六包一 "
        "series only strengthens the cell-count arithmetic."
    )
    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    arithmetic = solve_arithmetic()
    values, all_cells = solve_values(arithmetic)
    verify_reconstruction(arithmetic, values, all_cells)

    write_solution(arithmetic, values, OUTPUT_DIR / "solution.json")
    write_report(arithmetic, OUTPUT_DIR / "report.md")
    draw_reconstruction(
        arithmetic, values, all_cells, OUTPUT_DIR / "reconstruction.png"
    )

    print(f"yukgodo2: solved and verified -> {OUTPUT_DIR}")
    print(
        f"  cells={arithmetic['geometric_total']} "
        f"(void {arithmetic['void_count']} + "
        f"occupied {arithmetic['occupied_count']})"
    )
    for k in range(1, arithmetic["ring_count"] + 1):
        first, last = ring_value_range(k)
        print(
            f"  ring {k}: {arithmetic['ring_sizes'][k]:2d} cells, "
            f"values {first}..{last}, sum {ring_sum(k)}"
        )


if __name__ == "__main__":
    main()
