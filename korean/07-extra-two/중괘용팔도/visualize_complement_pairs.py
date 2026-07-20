#!/usr/bin/env python3
"""
Visualize the complement-pair reading of the eight-formation diagram.

The visual emphasis follows the method described for Nakseo Gugudo on
LibreWiki: establish a baseline complement sum, then inspect how local groups
use or redistribute those complement pairs.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Circle, FancyArrowPatch

from analyze_complement_structure import (
    COMPLEMENT_SUM,
    FORMATIONS,
    Formation,
    internal_pairs,
    split_pairs,
    unpaired_values,
)


NODE_RADIUS = 0.30
PAIR_COLORS = ["#1b9e77", "#d95f02", "#7570b3", "#e7298a"]


FORMATION_COORDS = {
    "TL": (-5.2, 6.0),
    "T": (0.0, 6.0),
    "TR": (5.2, 6.0),
    "L": (-5.2, 1.0),
    "R": (5.2, 1.0),
    "BL": (-5.2, -4.0),
    "B": (0.0, -4.0),
    "BR": (5.2, -4.0),
}

VERTICAL_LAYOUTS = {
    "TL": [
        [(-0.6, 40), (0.6, 20)],
        [(-1.2, 57), (1.2, 9)],
        [(-1.2, 8), (1.2, 56)],
        [(-0.6, 29), (0.6, 41)],
    ],
    "TR": [
        [(-0.6, 45), (0.6, 24)],
        [(-1.2, 52), (1.2, 4)],
        [(-1.2, 13), (1.2, 61)],
        [(-0.6, 25), (0.6, 36)],
    ],
    "L": [
        [(-0.6, 48), (0.6, 32)],
        [(-1.2, 49), (1.2, 1)],
        [(-1.2, 16), (1.2, 64)],
        [(-0.6, 17), (0.6, 33)],
    ],
    "R": [
        [(-0.6, 37), (0.6, 21)],
        [(-1.2, 60), (1.2, 12)],
        [(-1.2, 5), (1.2, 53)],
        [(-0.6, 28), (0.6, 44)],
    ],
    "BL": [
        [(-0.6, 38), (0.6, 22)],
        [(-1.2, 59), (1.2, 11)],
        [(-1.2, 6), (1.2, 54)],
        [(-0.6, 27), (0.6, 43)],
    ],
    "BR": [
        [(-0.6, 47), (0.6, 31)],
        [(-1.2, 50), (1.2, 2)],
        [(-1.2, 15), (1.2, 63)],
        [(-0.6, 18), (0.6, 34)],
    ],
}

HORIZONTAL_LAYOUTS = {
    "T": [
        (14, 51, 0.8),
        (19, 46, 1.8),
        (35, 30, 1.8),
        (62, 3, 0.8),
    ],
    "B": [
        (7, 58, 0.8),
        (26, 39, 1.8),
        (42, 23, 1.8),
        (55, 10, 0.8),
    ],
}


def get_cjk_font() -> FontProperties:
    font_paths = [
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]
    for path in font_paths:
        if Path(path).exists():
            return FontProperties(fname=path)

    candidates = [
        "Noto Serif CJK KR",
        "Noto Sans CJK KR",
        "NanumMyeongjo",
        "NanumGothic",
    ]
    available = {font.name for font in matplotlib.font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            return FontProperties(family=name)
    return FontProperties(family=["serif"])


def build_positions() -> dict[int, tuple[float, float]]:
    positions: dict[int, tuple[float, float]] = {}

    for key, rows in VERTICAL_LAYOUTS.items():
        x, y = FORMATION_COORDS[key]
        for row_index, row in enumerate(rows):
            node_y = y - row_index
            for x_offset, value in row:
                positions[value] = (x + x_offset, node_y)

    for key, rows in HORIZONTAL_LAYOUTS.items():
        x, y = FORMATION_COORDS[key]
        for row_index, (left_value, right_value, half_width) in enumerate(rows):
            node_y = y - row_index
            positions[left_value] = (x - half_width, node_y)
            positions[right_value] = (x + half_width, node_y)

    return positions


def draw_base_shape(ax, positions: dict[int, tuple[float, float]]) -> None:
    for rows in VERTICAL_LAYOUTS.values():
        columns: dict[float, list[int]] = {}
        for row in rows:
            for x_offset, value in row:
                columns.setdefault(x_offset, []).append(value)
        for column in columns.values():
            for start, end in zip(column, column[1:]):
                draw_line(ax, positions[start], positions[end], "#c8c8c8", 1.2, 1)

    for rows in HORIZONTAL_LAYOUTS.values():
        for left_value, right_value, _half_width in rows:
            draw_line(ax, positions[left_value], positions[right_value], "#c8c8c8", 1.2, 1)


def draw_line(
    ax,
    start: tuple[float, float],
    end: tuple[float, float],
    color: str,
    linewidth: float,
    zorder: int,
    linestyle: str = "-",
) -> None:
    ax.plot(
        [start[0], end[0]],
        [start[1], end[1]],
        color=color,
        linewidth=linewidth,
        linestyle=linestyle,
        zorder=zorder,
    )


def draw_curve(
    ax,
    start: tuple[float, float],
    end: tuple[float, float],
    color: str,
    rad: float,
) -> None:
    patch = FancyArrowPatch(
        start,
        end,
        arrowstyle="-",
        connectionstyle=f"arc3,rad={rad}",
        color=color,
        linewidth=1.8,
        linestyle=(0, (4, 3)),
        zorder=2,
    )
    ax.add_patch(patch)


def draw_nodes(
    ax,
    positions: dict[int, tuple[float, float]],
    split_values: set[int],
) -> None:
    for value, (x, y) in positions.items():
        is_split = value in split_values
        circle = Circle(
            (x, y),
            radius=NODE_RADIUS,
            facecolor="#fff7d6" if is_split else "white",
            edgecolor="#9a6b00" if is_split else "black",
            linewidth=1.7 if is_split else 1.3,
            zorder=4,
        )
        ax.add_patch(circle)
        ax.text(x, y, str(value), ha="center", va="center", fontsize=11, zorder=5)


def draw_internal_complements(
    ax,
    positions: dict[int, tuple[float, float]],
    formations: list[Formation],
) -> None:
    for formation in formations:
        for pair_index, pair in enumerate(internal_pairs(formation)):
            color = PAIR_COLORS[pair_index % len(PAIR_COLORS)]
            draw_line(ax, positions[pair[0]], positions[pair[1]], color, 2.4, 2)


def draw_split_complements(ax, positions: dict[int, tuple[float, float]]) -> set[int]:
    top_left = FORMATIONS[0]
    top_right = FORMATIONS[2]
    pairs = split_pairs(top_left, top_right)
    split_values = {value for pair in pairs for value in pair}

    for index, (left_value, right_value) in enumerate(pairs):
        draw_curve(
            ax,
            positions[left_value],
            positions[right_value],
            "#5b5b5b",
            rad=0.18 + index * 0.05,
        )

    return split_values


def draw_labels(ax) -> None:
    cjk_font = get_cjk_font()
    ax.text(
        0.0,
        0.1,
        "八\n陣\n圖",
        ha="center",
        va="center",
        fontsize=25,
        linespacing=1.0,
        fontproperties=cjk_font,
        zorder=1,
    )
    ax.text(
        0.0,
        7.0,
        f"baseline complement sum = {COMPLEMENT_SUM}; four pairs = {COMPLEMENT_SUM * 4}",
        ha="center",
        va="center",
        fontsize=12,
        color="#333333",
    )
    ax.text(
        -7.6,
        -7.85,
        "dashed links: split complement pairs shared by the upper corner formations",
        ha="left",
        va="center",
        fontsize=10,
        color="#5b5b5b",
    )
    ax.text(
        -7.6,
        -8.25,
        "colored links: complement pairs closed inside each formation",
        ha="left",
        va="center",
        fontsize=10,
        color="#333333",
    )


def main() -> None:
    fig, ax = plt.subplots(figsize=(12, 12))
    positions = build_positions()

    draw_base_shape(ax, positions)
    draw_internal_complements(ax, positions, FORMATIONS)
    split_values = draw_split_complements(ax, positions)
    draw_nodes(ax, positions, split_values)
    draw_labels(ax)

    ax.set_aspect("equal")
    ax.set_xlim(-8.0, 8.0)
    ax.set_ylim(-8.5, 7.5)
    ax.axis("off")
    plt.tight_layout()

    plt.savefig(
        "eight_formation_complement_pairs.png",
        dpi=300,
        bbox_inches="tight",
        facecolor="white",
    )
    plt.savefig(
        "eight_formation_complement_pairs.svg",
        bbox_inches="tight",
        facecolor="white",
    )
    plt.show()


if __name__ == "__main__":
    main()
