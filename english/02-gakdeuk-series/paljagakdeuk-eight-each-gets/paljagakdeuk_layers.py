from __future__ import annotations

"""
Paljagakdeuk (八子各得) — Basic visualization

This script displays the original cross structure of Paljagakdeuk
using Hanja labels and mod 5 colors.

For modern graph and combinatorial deep analysis, see
analyze_paljagakdeuk.py, analysis_report.md, and blog.md.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Circle, FancyBboxPatch


PALACES = {
    "Upper Palace": [
        [39, 7, 34],
        [12, None, 19],
        [24, 2, 27],
    ],
    "Left Palace": [
        [33, 18, 28],
        [8, None, 3],
        [38, 13, 23],
    ],
    "Center Palace": [
        [30, 5, 21],
        [16, None, 15],
        [31, 10, 36],
    ],
    "Right Palace": [
        [22, 14, 37],
        [4, None, 9],
        [29, 17, 32],
    ],
    "Lower Palace": [
        [26, 1, 25],
        [20, None, 11],
        [35, 6, 40],
    ],
}

# Each 3×3 palace is positioned as one arm of the cross.
PALACE_ORIGINS = {
    "Upper Palace": (3, 6),
    "Left Palace": (0, 3),
    "Center Palace": (3, 3),
    "Right Palace": (6, 3),
    "Lower Palace": (3, 0),
}

# These colors reproduce the five residue classes marked in the notebook.
RESIDUE_STYLE = {
    1: {"face": "#D9D9D9", "edge": "#555555", "name": "mod 5 = 1"},
    2: {"face": "#F3C2C2", "edge": "#A33A3A", "name": "mod 5 = 2"},
    3: {"face": "#C7D8F5", "edge": "#315C9A", "name": "mod 5 = 3"},
    4: {"face": "#BFBFBF", "edge": "#222222", "name": "mod 5 = 4"},
    0: {"face": "#F3D58A", "edge": "#A67C00", "name": "mod 5 = 0"},
}

HANJA_DIGITS = {
    0: "零",
    1: "一",
    2: "二",
    3: "三",
    4: "四",
    5: "五",
    6: "六",
    7: "七",
    8: "八",
    9: "九",
    10: "十",
}


def to_hanja(number: int) -> str:
    if number <= 10:
        return HANJA_DIGITS[number]

    tens, ones = divmod(number, 10)
    prefix = "十" if tens == 1 else HANJA_DIGITS[tens] + "十"
    return prefix if ones == 0 else prefix + HANJA_DIGITS[ones]


def get_font() -> FontProperties:
    candidates = [
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/arphic/uming.ttc",
    ]

    for candidate in candidates:
        if Path(candidate).exists():
            return FontProperties(fname=candidate)

    return FontProperties()


def build_positions() -> dict[int, tuple[float, float]]:
    positions: dict[int, tuple[float, float]] = {}

    for palace_name, grid in PALACES.items():
        origin_x, origin_y = PALACE_ORIGINS[palace_name]

        for row_index, row in enumerate(grid):
            for column_index, value in enumerate(row):
                if value is None:
                    continue

                x = origin_x + column_index
                y = origin_y + (2 - row_index)
                positions[value] = (x, y)

    return positions


def palace_values(grid: list[list[int | None]]) -> list[int]:
    return [
        value
        for row in grid
        for value in row
        if value is not None
    ]


def validate() -> None:
    all_values = [
        value
        for grid in PALACES.values()
        for value in palace_values(grid)
    ]

    if sorted(all_values) != list(range(1, 41)):
        raise ValueError("The diagram must contain every integer from 1 to 40 exactly once.")

    if sum(all_values) != 820:
        raise ValueError("The total of 1 through 40 must be 820.")

    for palace_name, grid in PALACES.items():
        values = palace_values(grid)

        if len(values) != 8:
            raise ValueError(f"{palace_name} must contain exactly eight numbers.")

        if sum(values) != 164:
            raise ValueError(
                f"{palace_name} sums to {sum(values)}, not 164."
            )


def draw_palace_boundary(
    ax: plt.Axes,
    palace_name: str,
    origin: tuple[float, float],
    font: FontProperties,
) -> None:
    origin_x, origin_y = origin

    boundary = FancyBboxPatch(
        (origin_x - 0.52, origin_y - 0.52),
        3.04,
        3.04,
        boxstyle="round,pad=0.04,rounding_size=0.18",
        facecolor="none",
        edgecolor="#777777",
        linewidth=1.1,
        linestyle=(0, (4, 4)),
        zorder=0,
    )
    ax.add_patch(boundary)

    ax.text(
        origin_x + 1.0,
        origin_y + 2.67,
        f"{palace_name} · 8 numbers · sum 164",
        ha="center",
        va="bottom",
        fontproperties=font,
        fontsize=10.5,
    )


def draw_diagram(
    png_output: str | Path = "paljagakdeuk_layers.png",
    svg_output: str | Path = "paljagakdeuk_layers.svg",
    label_style: str = "arabic",
) -> None:
    validate()

    if label_style not in {"hanja", "arabic"}:
        raise ValueError("label_style must be either 'hanja' or 'arabic'.")

    font = get_font()
    positions = build_positions()

    fig = plt.figure(figsize=(13, 9), dpi=240)
    ax = fig.add_axes([0.04, 0.06, 0.67, 0.88])
    info = fig.add_axes([0.74, 0.08, 0.23, 0.84])

    ax.set_aspect("equal")
    ax.set_xlim(-0.8, 8.8)
    ax.set_ylim(-0.8, 8.8)
    ax.axis("off")

    for palace_name, origin in PALACE_ORIGINS.items():
        draw_palace_boundary(ax, palace_name, origin, font)

    radius = 0.31

    for number, (x, y) in positions.items():
        residue = number % 5
        style = RESIDUE_STYLE[residue]

        ax.add_patch(
            Circle(
                (x, y),
                radius,
                facecolor=style["face"],
                edgecolor=style["edge"],
                linewidth=1.9,
                zorder=2,
            )
        )

        label = to_hanja(number) if label_style == "hanja" else str(number)

        ax.text(
            x,
            y,
            label,
            ha="center",
            va="center",
            fontproperties=font,
            fontsize=13.5 if number < 10 else 11.5,
            zorder=3,
        )

    ax.set_title(
        "Paljagakdeuk (八子各得) — 1 to 40, five palaces, 8 numbers each, palace sum 164",
        fontproperties=font,
        fontsize=17,
        pad=18,
    )

    info.axis("off")
    info.text(
        0.0,
        0.98,
        "Structure and Verification",
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=16,
        weight="bold",
    )

    summary_lines = [
        "• Numbers used: 1–40, each once",
        "• Total sum: 820",
        "• Number of palaces: 5",
        "• Each palace: 8 numbers in a 3×3 grid with empty center",
        "• Sum per palace: 164",
        "• 5 × 164 = 820",
    ]

    y = 0.91
    for line in summary_lines:
        info.text(
            0.0,
            y,
            line,
            ha="left",
            va="top",
            fontproperties=font,
            fontsize=11.5,
        )
        y -= 0.055

    info.text(
        0.0,
        y - 0.01,
        "mod 5 Layers",
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=14,
        weight="bold",
    )
    y -= 0.08

    for residue in [1, 2, 3, 4, 0]:
        style = RESIDUE_STYLE[residue]
        info.add_patch(
            Circle(
                (0.055, y + 0.012),
                0.024,
                transform=info.transAxes,
                facecolor=style["face"],
                edgecolor=style["edge"],
                linewidth=1.4,
            )
        )
        sequence = list(range(residue if residue != 0 else 5, 41, 5))
        sequence_text = ", ".join(str(value) for value in sequence)

        info.text(
            0.11,
            y + 0.012,
            f"{style['name']}: {sequence_text}",
            ha="left",
            va="center",
            transform=info.transAxes,
            fontproperties=font,
            fontsize=10.2,
        )
        y -= 0.062

    y -= 0.015
    info.text(
        0.0,
        y,
        "Generalization from the Notebook",
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=14,
        weight="bold",
    )
    y -= 0.065

    # The notebook records a family whose palace total increases by eight.
    family = [
        ("M0 = 1", 148),
        ("M0 = 2", 156),
        ("M0 = 3", 164),
        ("M0 = 4", 172),
        ("M0 = 5", 180),
    ]

    for label, total in family:
        info.text(
            0.02,
            y,
            f"{label}  →  SUM = {total}",
            ha="left",
            va="top",
            fontproperties=font,
            fontsize=11,
        )
        y -= 0.047

    info.text(
        0.02,
        y - 0.005,
        "Therefore  M(n+1) = M(n) + 8",
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=11.5,
        weight="bold",
    )

    fig.savefig(
        png_output,
        dpi=300,
        bbox_inches="tight",
        pad_inches=0.12,
        facecolor="white",
    )
    fig.savefig(
        svg_output,
        bbox_inches="tight",
        pad_inches=0.12,
        facecolor="white",
    )
    plt.close(fig)


if __name__ == "__main__":
    draw_diagram()
