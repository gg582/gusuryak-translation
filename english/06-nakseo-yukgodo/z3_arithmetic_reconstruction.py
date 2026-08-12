import math

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


def build_arithmetic_solver():
    """
    Reconstruct the numerical structure described by the manuscript.

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

    虛一:
        271 - 1 = 270
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
    solver.add(
        luoshu_sum
        == Sum(list(range(1, LUOSHU_ORDER + 1)))
    )

    # 逓加洛書數六倍
    solver.add(
        occupied_count
        == Sum(
            [ring_sizes[k] for k in range(1, LUOSHU_ORDER + 1)]
        )
    )

    solver.add(
        occupied_count
        == RING_STEP * luoshu_sum
    )

    # 虛一
    solver.add(void_count == 1)

    solver.add(
        geometric_total
        == occupied_count + void_count
    )

    # 來積法: 外周添六
    solver.add(
        side_total == outer_count + 6
    )

    # 六歸之得一十
    solver.add(
        side_total == 6 * side_count
    )

    # 倍之得二十，減一為十九，為中觚數
    solver.add(
        middle_span == 2 * side_count - 1
    )

    # 去中觚 leaves the adjacent maximum span.
    solver.add(
        adjacent_span == middle_span - 1
    )

    # The nine steps agree with the outer count.
    solver.add(
        outer_count == 6 * ring_count
    )

    # Reconstructed field-style area relation.
    solver.add(
        non_middle_count
        == (side_count + adjacent_span) * ring_count
    )

    # Restore 中觚.
    solver.add(
        geometric_total
        == non_middle_count + middle_span
    )

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
    """
    Return one complete hexagonal ring in cyclic order.

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
    """
    Reconstructed value-range hypothesis.

    Ring k receives the next 6k consecutive values.

    Ring 1:   1..6
    Ring 2:   7..18
    ...
    Ring 9: 217..270
    """

    previous_total = 3 * (ring - 1) * ring
    current_total = 3 * ring * (ring + 1)

    return previous_total + 1, current_total


def build_value_solver(arithmetic):
    """
    Fill all noncentral cells.

    Manuscript-derived constraints:
        - center is void
        - ring k contains 6k positions
        - total occupied positions = 270

    Reconstruction hypothesis used to recover individual values:
        - values are 1..270
        - ring k receives its corresponding consecutive range
        - values progress consecutively around each ring

    The cyclic start direction is a normalization of rotational symmetry,
    not a historical claim.
    """

    radius = arithmetic["ring_count"]

    all_cells = build_hex_grid(radius)
    center = (0, 0)

    occupied_cells = [
        cell
        for cell in all_cells
        if cell != center
    ]

    solver = Solver()

    values = {
        cell: Int(f"value_{cell[0]}_{cell[1]}")
        for cell in occupied_cells
    }

    for variable in values.values():
        solver.add(variable >= 1)
        solver.add(variable <= arithmetic["occupied_count"])

    solver.add(
        Distinct(list(values.values()))
    )

    for ring in range(1, radius + 1):
        cells = ring_cells(ring)

        first_value, last_value = ring_value_range(ring)

        assert last_value - first_value + 1 == 6 * ring

        # Each ring receives exactly its consecutive numerical interval.
        for cell in cells:
            solver.add(values[cell] >= first_value)
            solver.add(values[cell] <= last_value)

        # Strong reconstruction hypothesis:
        # values proceed consecutively around the ring.
        for index, cell in enumerate(cells):
            solver.add(
                values[cell] == first_value + index
            )

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

        actual_values = sorted(
            values[cell]
            for cell in cells
        )

        first_value, last_value = ring_value_range(ring)

        expected_values = list(
            range(first_value, last_value + 1)
        )

        assert actual_values == expected_values


def axial_to_xy(cell):
    q, r = cell

    x = math.sqrt(3) * (q + r / 2)
    y = 1.5 * r

    return x, y


def print_arithmetic(arithmetic):
    print("Manuscript reconstruction")
    print("=========================")
    print()

    print("逓加")
    print("----")

    for ring in range(1, arithmetic["ring_count"] + 1):
        first_value, last_value = ring_value_range(ring)

        print(
            f"Ring {ring}: "
            f"{arithmetic['ring_sizes'][ring]:2d} cells, "
            f"reconstructed values {first_value}..{last_value}"
        )

    print()

    ring_expression = " + ".join(
        str(arithmetic["ring_sizes"][ring])
        for ring in range(1, arithmetic["ring_count"] + 1)
    )

    print(
        f"{ring_expression} "
        f"= {arithmetic['occupied_count']}"
    )

    print(
        f"6 * (1 + 2 + ... + 9) "
        f"= 6 * {arithmetic['luoshu_sum']} "
        f"= {arithmetic['occupied_count']}"
    )

    print()
    print("來積法")
    print("------")

    print(
        f"{arithmetic['outer_count']} + 6 "
        f"= {arithmetic['side_total']}"
    )

    print(
        f"{arithmetic['side_total']} / 6 "
        f"= {arithmetic['side_count']}"
    )

    print(
        f"2 * {arithmetic['side_count']} - 1 "
        f"= {arithmetic['middle_span']}"
    )

    print(
        f"{arithmetic['middle_span']} - 1 "
        f"= {arithmetic['adjacent_span']}"
    )

    print(
        f"({arithmetic['side_count']} "
        f"+ {arithmetic['adjacent_span']}) "
        f"* {arithmetic['ring_count']} "
        f"= {arithmetic['non_middle_count']}"
    )

    print(
        f"{arithmetic['non_middle_count']} "
        f"+ {arithmetic['middle_span']} "
        f"= {arithmetic['geometric_total']}"
    )

    print()

    print(
        f"{arithmetic['geometric_total']} "
        f"- {arithmetic['void_count']} "
        f"= {arithmetic['occupied_count']}"
    )


def draw_reconstruction(arithmetic, values, all_cells):
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
            ax.text(
                x,
                y,
                "VOID",
                ha="center",
                va="center",
                fontsize=7,
            )
        else:
            ax.text(
                x,
                y,
                str(values[cell]),
                ha="center",
                va="center",
                fontsize=5,
            )

    ax.set_aspect("equal")
    ax.autoscale_view()
    ax.axis("off")

    ax.set_title(
        (
            "Reconstructed Hexagonal Arrangement\n"
            "逓加: 6, 12, ..., 54 | "
            "270 occupied cells | "
            "1 central void"
        ),
        fontsize=14,
    )

    plt.tight_layout()
    fig.savefig("reconstruction_1.png", dpi=150)
    plt.show()


def main():
    arithmetic = solve_arithmetic()

    values, all_cells = solve_values(arithmetic)

    verify_reconstruction(
        arithmetic,
        values,
        all_cells,
    )

    print_arithmetic(arithmetic)

    draw_reconstruction(
        arithmetic,
        values,
        all_cells,
    )


if __name__ == "__main__":
    main()
