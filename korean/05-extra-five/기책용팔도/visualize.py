#!/usr/bin/env python3

import math
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Circle, Polygon

# Use a Korean-capable font so Hangul labels (e.g. the title) do not render
# as placeholder boxes.  NanumGothic is widely available on Linux systems.
font_manager.fontManager.addfont(
    "/usr/share/fonts/naver-nanum-gothic-fonts/NanumGothic.ttf"
)
matplotlib.rcParams["font.family"] = "NanumGothic"
matplotlib.rcParams["axes.unicode_minus"] = False


OUTPUT_DIR = Path(".")
PNG_PATH = OUTPUT_DIR / "four_magic_octagons.png"
SVG_PATH = OUTPUT_DIR / "four_magic_octagons.svg"
PDF_PATH = OUTPUT_DIR / "four_magic_octagons.pdf"

TARGET_SUM = 100
OCTAGON_RADIUS = 2.3
NODE_RADIUS = 0.28
ROTATION = math.pi / 8.0


GROUPS = {
    "Top": [4, 9, 14, 23, 5, 8, 19, 18],
    "Left": [8, 5, 15, 22, 3, 10, 20, 17],
    "Right": [1, 12, 18, 19, 6, 7, 13, 24],
    "Bottom": [7, 6, 17, 20, 2, 11, 16, 21],
}


def regular_octagon_vertices(
    center: tuple[float, float],
    radius: float,
    rotation: float,
) -> list[tuple[float, float]]:
    """Return eight counterclockwise vertices of a regular octagon."""
    cx, cy = center

    return [
        (
            cx + radius * math.cos(rotation + index * math.pi / 4.0),
            cy + radius * math.sin(rotation + index * math.pi / 4.0),
        )
        for index in range(8)
    ]


def rounded_coordinate(
    point: tuple[float, float],
    digits: int = 8,
) -> tuple[float, float]:
    """Create a stable key for geometrically identical shared vertices."""
    return round(point[0], digits), round(point[1], digits)


def validate_groups(groups: dict[str, list[int]]) -> None:
    """Reject malformed groups before drawing the figure."""
    for name, values in groups.items():
        if len(values) != 8:
            raise ValueError(
                f"{name} must contain exactly eight values, "
                f"but contains {len(values)}."
            )

        group_sum = sum(values)

        if group_sum != TARGET_SUM:
            raise ValueError(
                f"{name} has sum {group_sum}, not {TARGET_SUM}: {values}"
            )

    all_values = sorted({value for values in groups.values() for value in values})

    expected_values = list(range(1, 25))

    if all_values != expected_values:
        raise ValueError(
            "The diagram must use every integer from 1 through 24 exactly "
            "as a distinct vertex label.\n"
            f"Observed values: {all_values}"
        )


def build_geometry():
    """
    Build four regular octagons arranged around a central square.

    Adjacent octagons share one complete edge:
    Top-Left, Top-Right, Left-Bottom, and Right-Bottom.
    """
    apothem = OCTAGON_RADIUS * math.cos(math.pi / 8.0)

    # The diagonal distance between adjacent centers must equal twice
    # the apothem for the octagons to share an entire edge.
    center_offset = math.sqrt(2.0) * apothem

    centers = {
        "Top": (0.0, center_offset),
        "Left": (-center_offset, 0.0),
        "Right": (center_offset, 0.0),
        "Bottom": (0.0, -center_offset),
    }

    vertices = {
        name: regular_octagon_vertices(
            center=center,
            radius=OCTAGON_RADIUS,
            rotation=ROTATION,
        )
        for name, center in centers.items()
    }

    return centers, vertices


def collect_number_positions(
    polygon_vertices: dict[str, list[tuple[float, float]]],
    groups: dict[str, list[int]],
) -> dict[int, tuple[float, float]]:
    """
    Assign each number to a geometric vertex.

    Repeated labels in adjacent groups must resolve to the same coordinate,
    because those labels represent shared vertices.
    """
    positions: dict[int, tuple[float, float]] = {}

    for group_name, numbers in groups.items():
        vertices = polygon_vertices[group_name]

        for number, point in zip(numbers, vertices):
            if number in positions:
                old_key = rounded_coordinate(positions[number])
                new_key = rounded_coordinate(point)

                if old_key != new_key:
                    raise ValueError(
                        f"Number {number} was assigned to two different "
                        f"coordinates: {positions[number]} and {point}"
                    )
            else:
                positions[number] = point

    return positions


def format_sum_expression(values: list[int]) -> str:
    """Format a visible partial-sum equation."""
    return " + ".join(str(value) for value in values) + f" = {sum(values)}"


def draw_diagram() -> None:
    validate_groups(GROUPS)

    centers, polygon_vertices = build_geometry()
    number_positions = collect_number_positions(polygon_vertices, GROUPS)

    fig, ax = plt.subplots(figsize=(11, 11))

    polygon_styles = {
        "Top": {
            "facecolor": "#9ecae1",
            "edgecolor": "#2171b5",
        },
        "Left": {
            "facecolor": "#a1d99b",
            "edgecolor": "#238b45",
        },
        "Right": {
            "facecolor": "#fdae6b",
            "edgecolor": "#d94801",
        },
        "Bottom": {
            "facecolor": "#bcbddc",
            "edgecolor": "#6a51a3",
        },
    }

    draw_order = ["Top", "Left", "Right", "Bottom"]

    for group_name in draw_order:
        style = polygon_styles[group_name]

        polygon = Polygon(
            polygon_vertices[group_name],
            closed=True,
            facecolor=style["facecolor"],
            edgecolor=style["edgecolor"],
            linewidth=2.4,
            alpha=0.24,
            joinstyle="round",
            zorder=1,
        )

        ax.add_patch(polygon)

    for number, point in sorted(number_positions.items()):
        x, y = point

        node = Circle(
            (x, y),
            radius=NODE_RADIUS,
            facecolor="white",
            edgecolor="#202020",
            linewidth=1.7,
            zorder=5,
        )

        ax.add_patch(node)

        ax.text(
            x,
            y,
            str(number),
            ha="center",
            va="center",
            fontsize=12,
            fontweight="bold",
            zorder=6,
        )

    equation_positions = {
        "Top": (0.0, centers["Top"][1] + 0.65),
        "Left": (centers["Left"][0] - 0.15, 0.0),
        "Right": (centers["Right"][0] + 0.15, 0.0),
        "Bottom": (0.0, centers["Bottom"][1] - 0.65),
    }

    equation_alignments = {
        "Top": ("center", "center"),
        "Left": ("center", "center"),
        "Right": ("center", "center"),
        "Bottom": ("center", "center"),
    }

    for group_name, values in GROUPS.items():
        x, y = equation_positions[group_name]
        horizontal_alignment, vertical_alignment = equation_alignments[group_name]

        ax.text(
            x,
            y,
            f"{group_name} octagon\n"
            f"$\\Sigma = {sum(values)}$",
            ha=horizontal_alignment,
            va=vertical_alignment,
            fontsize=12,
            fontweight="bold",
            zorder=4,
        )

    detailed_equations = {
        "Top": (0.0, 6.65),
        "Left": (-6.9, 0.0),
        "Right": (6.9, 0.0),
        "Bottom": (0.0, -6.65),
    }

    detailed_alignment = {
        "Top": ("center", "bottom"),
        "Left": ("right", "center"),
        "Right": ("left", "center"),
        "Bottom": ("center", "top"),
    }

    for group_name, values in GROUPS.items():
        x, y = detailed_equations[group_name]
        horizontal_alignment, vertical_alignment = detailed_alignment[group_name]

        if group_name in {"Left", "Right"}:
            first_half = " + ".join(str(value) for value in values[:4])
            second_half = " + ".join(str(value) for value in values[4:])

            expression = (
                f"{first_half}\n"
                f"+ {second_half}\n"
                f"= {sum(values)}"
            )
        else:
            expression = format_sum_expression(values)

        ax.text(
            x,
            y,
            expression,
            ha=horizontal_alignment,
            va=vertical_alignment,
            fontsize=10.5,
            bbox={
                "boxstyle": "round,pad=0.45",
                "facecolor": "white",
                "edgecolor": polygon_styles[group_name]["edgecolor"],
                "linewidth": 1.4,
                "alpha": 0.95,
            },
            zorder=10,
        )

    shared_pairs = {
        "Top ∩ Left": {5, 8},
        "Top ∩ Right": {18, 19},
        "Left ∩ Bottom": {17, 20},
        "Right ∩ Bottom": {6, 7},
    }

    for pair_name, expected_shared_values in shared_pairs.items():
        first_name, second_name = pair_name.split(" ∩ ")

        actual_shared_values = set(GROUPS[first_name]) & set(GROUPS[second_name])

        if actual_shared_values != expected_shared_values:
            raise ValueError(
                f"Incorrect shared edge for {pair_name}: "
                f"expected {sorted(expected_shared_values)}, "
                f"observed {sorted(actual_shared_values)}"
            )

    ax.set_title(
        "기책용팔도(氣策用八圖)\n"
        "Each octagon has vertex sum 100",
        fontsize=17,
        pad=24,
    )

    ax.text(
        0.0,
        0.0,
        "central\nsquare",
        ha="center",
        va="center",
        fontsize=9,
        color="#555555",
        zorder=3,
    )

    coordinate_limit = 8.7

    ax.set_xlim(-coordinate_limit, coordinate_limit)
    ax.set_ylim(-coordinate_limit, coordinate_limit)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")

    plt.tight_layout()

    fig.savefig(
        PNG_PATH,
        dpi=300,
        bbox_inches="tight",
        facecolor="white",
    )

    fig.savefig(
        SVG_PATH,
        bbox_inches="tight",
        facecolor="white",
    )

    fig.savefig(
        PDF_PATH,
        bbox_inches="tight",
        facecolor="white",
    )

    print("Validated partial sums:")

    for name, values in GROUPS.items():
        print(f"  {name:6s}: {format_sum_expression(values)}")

    print()
    print(f"Saved PNG: {PNG_PATH.resolve()}")
    print(f"Saved SVG: {SVG_PATH.resolve()}")
    print(f"Saved PDF: {PDF_PATH.resolve()}")

    plt.show()


if __name__ == "__main__":
    draw_diagram()
