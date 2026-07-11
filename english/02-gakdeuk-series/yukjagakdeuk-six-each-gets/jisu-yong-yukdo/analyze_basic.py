from __future__ import annotations

from pathlib import Path
from typing import Final

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Circle, Polygon


TITLE: Final = "Jisu-yong-yukdo"
HANJA_TITLE: Final = "Earth-Number Six-Use Diagram"
SUBTITLE: Final = "Six-Each-Gets, Sixty-Three"
TARGET_SUM: Final = 63

# The hand-drawn structure is normalized onto a straight honeycomb lattice.
# The five hexagons share some vertices and edges with adjacent hexagons.
POSITIONS: Final = {
    # Outer vertices of the upper-left hexagon
    5:  (-2.0,  4.5),
    18: (-3.0,  3.6),
    16: (-3.0,  2.5),
    3:  (-2.0,  1.7),
    8:  (-1.0,  2.5),
    13: (-1.0,  3.6),

    # Outer vertices of the upper-right hexagon
    1:  ( 0.0,  4.5),
    7:  ( 1.0,  3.6),
    20: ( 1.0,  2.5),
    14: ( 0.0,  1.7),

    # Lower vertices of the center hexagon
    12: (-2.0,  0.3),
    11: (-1.0, -0.5),
    15: ( 0.0,  0.3),

    # Outer vertices of the lower-left hexagon
    9:  (-3.0, -0.5),
    19: (-3.0, -1.7),
    2:  (-2.0, -2.5),
    10: (-1.0, -1.7),

    # Outer vertices of the lower-right hexagon
    4:  ( 1.0, -0.5),
    17: ( 1.0, -1.7),
    6:  ( 0.0, -2.5),
}

# Each hexagon is defined by its six vertices in clockwise order.
HEXAGONS: Final = {
    "upper-left": (5, 18, 16, 3, 8, 13),
    "upper-right": (1, 13, 8, 14, 20, 7),
    "center": (3, 8, 14, 15, 11, 12),
    "lower-left": (12, 11, 10, 2, 19, 9),
    "lower-right": (15, 4, 17, 6, 10, 11),
}

# The mod 5 color scheme from the notes is preserved.
RESIDUE_STYLE: Final = {
    1: {
        "label": "n mod 5 ≡ 1",
        "face": "#3F3F3F",
        "edge": "#161616",
        "text": "#FFFFFF",
    },
    2: {
        "label": "n mod 5 ≡ 2",
        "face": "#F1CDCD",
        "edge": "#B63E3E",
        "text": "#782020",
    },
    3: {
        "label": "n mod 5 ≡ 3",
        "face": "#D4E3F7",
        "edge": "#3E70AF",
        "text": "#244C7B",
    },
    4: {
        "label": "n mod 5 ≡ 4",
        "face": "#E1E1E1",
        "edge": "#666666",
        "text": "#222222",
    },
    0: {
        "label": "n mod 5 ≡ 0",
        "face": "#F5E1A2",
        "edge": "#B98D00",
        "text": "#725500",
    },
}

RESIDUE_GROUPS: Final = {
    1: (1, 6, 11, 16),
    2: (2, 7, 12, 17),
    3: (3, 8, 13, 18),
    4: (4, 9, 14, 19),
    0: (5, 10, 15, 20),
}


def find_cjk_font() -> FontProperties:
    candidates = (
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf",
        "/usr/share/fonts/truetype/unfonts-core/UnDotum.ttf",
        "/usr/share/fonts/truetype/baekmuk/dotum.ttf",
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "C:/Windows/Fonts/malgun.ttf",
        "C:/Windows/Fonts/gulim.ttc",
    )

    for candidate in candidates:
        if Path(candidate).exists():
            return FontProperties(fname=candidate)

    return FontProperties()


def validate() -> None:
    numbers = sorted(POSITIONS)

    if numbers != list(range(1, 21)):
        raise ValueError("The numbers 1 through 20 must appear exactly once.")

    grouped = sorted(
        number
        for group in RESIDUE_GROUPS.values()
        for number in group
    )

    if grouped != list(range(1, 21)):
        raise ValueError("Residue groups must partition 1 through 20 exactly.")

    for residue, group in RESIDUE_GROUPS.items():
        for number in group:
            if number % 5 != residue:
                raise ValueError(
                    f"{number} is placed in the wrong residue group."
                )

    for name, vertices in HEXAGONS.items():
        value_sum = sum(vertices)

        if value_sum != TARGET_SUM:
            raise ValueError(
                f"The {name} hexagon has sum {value_sum}, "
                f"but it must be {TARGET_SUM}."
            )


def unique_edges() -> list[tuple[int, int]]:
    edges: set[tuple[int, int]] = set()

    for vertices in HEXAGONS.values():
        for start, end in zip(vertices, vertices[1:] + vertices[:1]):
            edge = tuple(sorted((start, end)))
            edges.add(edge)

    return sorted(edges)


def draw_hexagon_regions(ax: Axes) -> None:
    # Instead of large circles, lightly emphasize the hexagons themselves.
    fills = (
        "#F8F8F8",
        "#FBFBFB",
        "#F6F6F6",
        "#FAFAFA",
        "#F7F7F7",
    )

    for (name, vertices), fill in zip(HEXAGONS.items(), fills):
        polygon_points = [POSITIONS[number] for number in vertices]

        ax.add_patch(
            Polygon(
                polygon_points,
                closed=True,
                facecolor=fill,
                edgecolor="#A8A8A8",
                linewidth=1.1,
                linestyle=(0, (4, 4)),
                zorder=0,
            )
        )

        center_x = sum(point[0] for point in polygon_points) / 6
        center_y = sum(point[1] for point in polygon_points) / 6

        ax.text(
            center_x,
            center_y,
            "sum 63",
            ha="center",
            va="center",
            fontsize=9.5,
            color="#9A9A9A",
            zorder=1,
        )


def draw_edges(ax: Axes) -> None:
    for start, end in unique_edges():
        x1, y1 = POSITIONS[start]
        x2, y2 = POSITIONS[end]

        ax.plot(
            [x1, x2],
            [y1, y2],
            color="#303030",
            linewidth=2.0,
            solid_capstyle="round",
            zorder=2,
        )


def draw_nodes(ax: Axes, font: FontProperties) -> None:
    radius = 0.28

    for number, (x, y) in POSITIONS.items():
        residue = number % 5
        style = RESIDUE_STYLE[residue]

        ax.add_patch(
            Circle(
                (x, y),
                radius,
                facecolor=style["face"],
                edgecolor=style["edge"],
                linewidth=2.0,
                zorder=3,
            )
        )

        ax.text(
            x,
            y,
            str(number),
            ha="center",
            va="center",
            fontproperties=font,
            fontsize=12,
            color=style["text"],
            zorder=4,
        )


def draw_legend(ax: Axes, font: FontProperties) -> None:
    ax.axis("off")

    ax.text(
        0.0,
        0.98,
        f"{TITLE} ({HANJA_TITLE})",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=17,
        weight="bold",
    )

    ax.text(
        0.0,
        0.92,
        SUBTITLE,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=13,
    )

    y = 0.84

    summary = (
        "Vertices: 1–20, each once",
        "Hexagons: 5",
        "Each hexagon: 6 vertices",
        "Each hexagon sum: 63",
        "Total vertex usages across hexagons: 30",
    )

    for line in summary:
        ax.text(
            0.0,
            y,
            f"• {line}",
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontproperties=font,
            fontsize=11,
        )
        y -= 0.053

    y -= 0.02

    ax.text(
        0.0,
        y,
        "mod 5 residue groups",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=14,
        weight="bold",
    )

    y -= 0.08

    for residue in (1, 2, 3, 4, 0):
        style = RESIDUE_STYLE[residue]
        group = RESIDUE_GROUPS[residue]

        ax.add_patch(
            Circle(
                (0.04, y + 0.012),
                0.023,
                transform=ax.transAxes,
                facecolor=style["face"],
                edgecolor=style["edge"],
                linewidth=1.5,
            )
        )

        ax.text(
            0.09,
            y + 0.012,
            f"{style['label']} · 4",
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontproperties=font,
            fontsize=10.8,
            weight="bold",
            color=style["text"],
        )

        ax.text(
            0.09,
            y - 0.026,
            "{ " + ", ".join(str(number) for number in group) + " }",
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontproperties=font,
            fontsize=10,
            color="#333333",
        )

        y -= 0.10

    y -= 0.005

    ax.text(
        0.0,
        y,
        "Verification by hexagon",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=14,
        weight="bold",
    )

    y -= 0.065

    for name, vertices in HEXAGONS.items():
        expression = " + ".join(str(number) for number in vertices)

        ax.text(
            0.0,
            y,
            f"{name}: {expression} = 63",
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontproperties=font,
            fontsize=9.7,
        )
        y -= 0.052


def draw(
    png_output: str | Path = "jisu_yong_yukdo.png",
    svg_output: str | Path = "jisu_yong_yukdo.svg",
) -> None:
    validate()
    font = find_cjk_font()

    fig = plt.figure(figsize=(12.5, 9.0), dpi=220)
    graph_ax = fig.add_axes([0.04, 0.07, 0.63, 0.86])
    legend_ax = fig.add_axes([0.71, 0.08, 0.26, 0.84])

    graph_ax.set_aspect("equal")
    graph_ax.set_xlim(-3.7, 1.7)
    graph_ax.set_ylim(-3.2, 5.2)
    graph_ax.axis("off")

    draw_hexagon_regions(graph_ax)
    draw_edges(graph_ax)
    draw_nodes(graph_ax, font)
    draw_legend(legend_ax, font)

    graph_ax.set_title(
        f"{TITLE} ({HANJA_TITLE})",
        fontproperties=font,
        fontsize=18,
        pad=18,
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
    draw()
