from __future__ import annotations

"""
Gujagakdeuk basic visualization

This file is a basic visualization script showing the original cross structure
of Gujagakdeuk with mod 5 colors.

For modern graph and combinatorial deep analysis, see analyze_gujagakdeuk.py,
analysis_report.md, and blog.md.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Circle, FancyBboxPatch


# A five-palace layout that faithfully transcribes the 45 numbers written in
# the hand drawing.
PALACES = {
    "Top": [
        [12, 44, 9],
        [19, 21, 29],
        [37, 2, 34],
    ],
    "Left": [
        [13, 43, 8],
        [18, 25, 26],
        [38, 3, 33],
    ],
    "Center": [
        [15, 41, 6],
        [16, 23, 30],
        [40, 5, 31],
    ],
    "Right": [
        [14, 42, 7],
        [17, 24, 28],
        [39, 4, 32],
    ],
    "Bottom": [
        [11, 45, 10],
        [20, 22, 27],
        [36, 1, 35],
    ],
}

# Coordinates normalizing the cross-shaped layout of the hand drawing.
PALACE_ORIGINS = {
    "Top": (3, 6),
    "Left": (0, 3),
    "Center": (3, 3),
    "Right": (6, 3),
    "Bottom": (3, 0),
}

# Preserves the residue class color classification from the notes.
RESIDUE_STYLE = {
    1: {
        "name": "mod 5 ≡ 1",
        "face": "#E5E5E5",
        "edge": "#444444",
        "text": "#202020",
    },
    2: {
        "name": "mod 5 ≡ 2",
        "face": "#F6D0D0",
        "edge": "#B54141",
        "text": "#7A2020",
    },
    3: {
        "name": "mod 5 ≡ 3",
        "face": "#D5E3FA",
        "edge": "#3D6DB3",
        "text": "#234A82",
    },
    4: {
        "name": "mod 5 ≡ 4",
        "face": "#D7D7D7",
        "edge": "#1F1F1F",
        "text": "#111111",
    },
    0: {
        "name": "mod 5 ≡ 0",
        "face": "#F7E3A0",
        "edge": "#B58A00",
        "text": "#7B5B00",
    },
}

# Sums by residue class written in the notes.
RESIDUE_SUMS = {
    1: 189,
    2: 198,
    3: 207,
    4: 216,
    0: 225,
}


def find_cjk_font() -> FontProperties:
    candidates = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
        "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf",
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/truetype/unfonts-core/UnDotum.ttf",
        "/usr/share/fonts/truetype/baekmuk/dotum.ttf",
    ]

    for candidate in candidates:
        if Path(candidate).exists():
            return FontProperties(fname=candidate)

    raise RuntimeError(
        "CJK font not found. Install Noto Sans CJK KR or NanumGothic."
    )


def values_for_residue(residue: int) -> list[int]:
    start = residue if residue != 0 else 5
    return list(range(start, 46, 5))


def validate() -> None:
    all_values = [
        value
        for grid in PALACES.values()
        for row in grid
        for value in row
    ]

    if sorted(all_values) != list(range(1, 46)):
        raise ValueError("The numbers 1 through 45 must appear exactly once.")

    if sum(all_values) != 1035:
        raise ValueError("The total sum of 1 through 45 must be 1035.")

    for palace_name, grid in PALACES.items():
        values = [value for row in grid for value in row]
        palace_sum = sum(values)

        if len(values) != 9:
            raise ValueError(f"{palace_name} must contain exactly 9 numbers.")

        if palace_sum != 207:
            raise ValueError(
                f"{palace_name} sum is {palace_sum}, which is not 207."
            )

    for residue, expected_sum in RESIDUE_SUMS.items():
        actual_sum = sum(values_for_residue(residue))

        if actual_sum != expected_sum:
            raise ValueError(
                f"Sum of residue {residue} is {actual_sum}, "
                f"which differs from the recorded value {expected_sum}."
            )


def build_positions() -> dict[int, tuple[float, float]]:
    positions: dict[int, tuple[float, float]] = {}

    for palace_name, grid in PALACES.items():
        origin_x, origin_y = PALACE_ORIGINS[palace_name]

        for row_index, row in enumerate(grid):
            for column_index, value in enumerate(row):
                x = origin_x + column_index
                y = origin_y + (2 - row_index)
                positions[value] = (x, y)

    return positions


def draw_palace_box(
    ax: plt.Axes,
    palace_name: str,
    origin: tuple[float, float],
    font: FontProperties,
) -> None:
    origin_x, origin_y = origin

    box = FancyBboxPatch(
        (origin_x - 0.52, origin_y - 0.52),
        3.04,
        3.04,
        boxstyle="round,pad=0.04,rounding_size=0.14",
        facecolor="#FAFAFA",
        edgecolor="#888888",
        linewidth=1.1,
        linestyle=(0, (4, 4)),
        zorder=0,
    )
    ax.add_patch(box)

    ax.text(
        origin_x + 1.0,
        origin_y + 2.64,
        f"{palace_name} · 9 numbers · sum 207",
        ha="center",
        va="bottom",
        fontproperties=font,
        fontsize=10.5,
        color="#333333",
    )


def draw_legend(
    ax: plt.Axes,
    font: FontProperties,
) -> None:
    ax.axis("off")

    ax.text(
        0.0,
        0.98,
        "Gujagakdeuk layer analysis",
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=17,
        weight="bold",
    )

    y = 0.91
    summary = [
        "Numbers used: 1–45, once each",
        "Total sum: 1035",
        "Number of palaces: 5",
        "Each palace: 3×3, 9 total",
        "Each palace sum (nine_sum): 207",
        "5 × 207 = 1035",
    ]

    for line in summary:
        ax.text(
            0.0,
            y,
            f"• {line}",
            ha="left",
            va="top",
            fontproperties=font,
            fontsize=11.2,
        )
        y -= 0.052

    y -= 0.015
    ax.text(
        0.0,
        y,
        "mod 5 residue groups",
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=14,
        weight="bold",
    )
    y -= 0.07

    residue_order = [1, 2, 3, 4, 0]

    for residue in residue_order:
        style = RESIDUE_STYLE[residue]
        values = values_for_residue(residue)
        value_text = ", ".join(str(value) for value in values)

        ax.add_patch(
            Circle(
                (0.035, y + 0.012),
                0.022,
                transform=ax.transAxes,
                facecolor=style["face"],
                edgecolor=style["edge"],
                linewidth=1.5,
            )
        )

        ax.text(
            0.08,
            y + 0.012,
            style["name"],
            ha="left",
            va="center",
            transform=ax.transAxes,
            fontproperties=font,
            fontsize=10.7,
            weight="bold",
            color=style["text"],
        )

        ax.text(
            0.08,
            y - 0.018,
            value_text,
            ha="left",
            va="top",
            transform=ax.transAxes,
            fontproperties=font,
            fontsize=9.3,
            color="#333333",
        )

        y -= 0.085

    y -= 0.005
    ax.text(
        0.0,
        y,
        "Residue class sums",
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=14,
        weight="bold",
    )
    y -= 0.066

    sum_lines = [
        "n0 = 1 → SUM = 189",
        "n0 = 2 → SUM = 198",
        "n0 = 3 → SUM = 207",
        "n0 = 4 → SUM = 216",
        "n0 = 5 → SUM = 225",
    ]

    for line in sum_lines:
        ax.text(
            0.02,
            y,
            line,
            ha="left",
            va="top",
            fontproperties=font,
            fontsize=11.0,
        )
        y -= 0.046

    ax.text(
        0.02,
        y - 0.005,
        "Common difference: +9",
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=11.5,
        weight="bold",
    )

    y -= 0.07
    ax.text(
        0.0,
        y,
        "Relations in the notes",
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=14,
        weight="bold",
    )

    ax.text(
        0.02,
        y - 0.06,
        "nine_sum = 207",
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=11.2,
    )

    ax.text(
        0.02,
        y - 0.11,
        "nine_sum = three_n_3_sum",
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=11.2,
    )


def draw_diagram(
    png_output: str | Path = "nine_each_from_notes.png",
    svg_output: str | Path = "nine_each_from_notes.svg",
) -> None:
    validate()

    font = find_cjk_font()
    positions = build_positions()

    fig = plt.figure(figsize=(13.5, 9.5), dpi=220)
    diagram_ax = fig.add_axes([0.04, 0.06, 0.68, 0.88])
    legend_ax = fig.add_axes([0.75, 0.08, 0.22, 0.84])

    diagram_ax.set_aspect("equal")
    diagram_ax.set_xlim(-0.75, 8.75)
    diagram_ax.set_ylim(-0.75, 8.75)
    diagram_ax.axis("off")

    for palace_name, origin in PALACE_ORIGINS.items():
        draw_palace_box(diagram_ax, palace_name, origin, font)

    radius = 0.32

    for number, (x, y) in positions.items():
        residue = number % 5
        style = RESIDUE_STYLE[residue]

        diagram_ax.add_patch(
            Circle(
                (x, y),
                radius,
                facecolor=style["face"],
                edgecolor=style["edge"],
                linewidth=2.0,
                zorder=2,
            )
        )

        diagram_ax.text(
            x,
            y,
            str(number),
            ha="center",
            va="center",
            fontproperties=font,
            fontsize=13.0,
            color=style["text"],
            zorder=3,
        )

    diagram_ax.set_title(
        "Gujagakdeuk — Hand-drawing transcription and mod 5 layer separation",
        fontproperties=font,
        fontsize=18,
        pad=18,
    )

    draw_legend(legend_ax, font)

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
