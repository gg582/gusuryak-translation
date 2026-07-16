#!/usr/bin/env python3

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Circle


NODE_RADIUS = 0.30


def get_cjk_font():
    """Return a FontProperties that can render CJK (Korean/Chinese) glyphs."""
    candidates = [
        "Noto Serif CJK KR",
        "Noto Sans CJK KR",
        "NanumMyeongjo",
        "NanumGothic",
        "Noto Serif CJK SC",
        "Noto Sans CJK SC",
    ]
    available = {f.name for f in matplotlib.font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            return FontProperties(family=name)
    return FontProperties(family=["serif"])


def draw_node(ax, x, y, value):
    circle = Circle(
        (x, y),
        radius=NODE_RADIUS,
        facecolor="white",
        edgecolor="black",
        linewidth=1.5,
        zorder=3,
    )
    ax.add_patch(circle)

    ax.text(
        x,
        y,
        str(value),
        ha="center",
        va="center",
        fontsize=11,
        zorder=4,
    )


def draw_edge(ax, start, end):
    ax.plot(
        [start[0], end[0]],
        [start[1], end[1]],
        linewidth=1.4,
        color="black",
        zorder=1,
    )


def draw_vertical_formation(ax, x, y, rows):
    """
    Draw a formation composed mainly of vertical columns.

    Each row contains one or more tuples:
        (x_offset, value)

    Nodes in the same x-offset column are connected vertically in row order.
    """
    positions = {}
    columns = {}

    for row_index, row in enumerate(rows):
        node_y = y - row_index * 1.0

        for x_offset, value in row:
            node_x = x + x_offset
            positions[value] = (node_x, node_y)
            columns.setdefault(x_offset, []).append((node_x, node_y))

    for column_points in columns.values():
        for start, end in zip(column_points, column_points[1:]):
            draw_edge(ax, start, end)

    for value, point in positions.items():
        draw_node(ax, point[0], point[1], value)


def draw_horizontal_formation(ax, x, y, rows):
    """
    Draw four horizontal pairs.

    Each row is:
        (left_value, right_value, half_width)
    """
    for row_index, (left_value, right_value, half_width) in enumerate(rows):
        node_y = y - row_index * 1.0
        left = (x - half_width, node_y)
        right = (x + half_width, node_y)

        draw_edge(ax, left, right)
        draw_node(ax, left[0], left[1], left_value)
        draw_node(ax, right[0], right[1], right_value)


def main():
    fig, ax = plt.subplots(figsize=(11, 12))

    draw_vertical_formation(
        ax,
        x=-5.2,
        y=6.0,
        rows=[
            [(-0.6, 40), (0.6, 14)],
            [(-1.2, 57), (0.6, 9)],
            [(-1.2, 8), (0.6, 56)],
            [(-0.6, 25), (0.6, 41)],
        ],
    )

    draw_horizontal_formation(
        ax,
        x=0.0,
        y=6.0,
        rows=[
            (14, 51, 0.8),
            (19, 46, 1.8),
            (33, 30, 1.8),
            (62, 3, 0.8),
        ],
    )

    draw_vertical_formation(
        ax,
        x=5.2,
        y=6.0,
        rows=[
            [(-0.6, 45), (0.6, 24)],
            [(-1.2, 52), (1.2, 4)],
            [(-1.2, 13), (1.2, 61)],
            [(-0.6, 22), (0.6, 36)],
        ],
    )

    draw_vertical_formation(
        ax,
        x=-5.2,
        y=1.0,
        rows=[
            [(-0.6, 48), (0.6, 32)],
            [(-1.2, 49), (1.2, 1)],
            [(-1.2, 16), (1.2, 64)],
            [(-0.6, 17), (0.6, 35)],
        ],
    )

    ax.text(
        0.0,
        0.0,
        "八\n陣\n圖",
        ha="center",
        va="center",
        fontsize=26,
        linespacing=1.0,
        fontproperties=get_cjk_font(),
    )

    draw_vertical_formation(
        ax,
        x=5.2,
        y=1.0,
        rows=[
            [(-0.6, 37), (0.6, 21)],
            [(-1.2, 60), (1.2, 12)],
            [(-1.2, 5), (1.2, 53)],
            [(-0.6, 28), (0.6, 44)],
        ],
    )

    draw_vertical_formation(
        ax,
        x=-5.2,
        y=-4.0,
        rows=[
            [(-0.6, 38), (0.6, 22)],
            [(-1.2, 59), (1.2, 11)],
            [(-1.2, 6), (1.2, 54)],
            [(-0.6, 27), (0.6, 43)],
        ],
    )

    draw_horizontal_formation(
        ax,
        x=0.0,
        y=-4.0,
        rows=[
            (7, 58, 0.8),
            (26, 39, 1.8),
            (42, 23, 1.8),
            (55, 10, 0.8),
        ],
    )

    draw_vertical_formation(
        ax,
        x=5.2,
        y=-4.0,
        rows=[
            [(-0.6, 47), (0.6, 31)],
            [(-1.2, 50), (1.2, 2)],
            [(-1.2, 15), (1.2, 63)],
            [(-0.6, 18), (0.6, 34)],
        ],
    )

    ax.set_aspect("equal")
    ax.set_xlim(-8.0, 8.0)
    ax.set_ylim(-8.5, 7.5)
    ax.axis("off")

    plt.tight_layout()

    plt.savefig(
        "eight_formation_diagram_wrong_origin.png",
        dpi=300,
        bbox_inches="tight",
        facecolor="white",
    )

    plt.savefig(
        "eight_formation_diagram_wrong_origin.svg",
        bbox_inches="tight",
        facecolor="white",
    )

    plt.show()


if __name__ == "__main__":
    main()
