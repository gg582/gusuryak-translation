from __future__ import annotations

from pathlib import Path
from typing import Final

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Circle


TITLE: Final = "낙서오구도"
TARGET_SUM: Final = 85
TOTAL_SUM: Final = 765

# Nine palace centers. Each palace is a plus-shaped set of five nodes.
PALACE_CENTERS: Final = {
    "상좌궁": (1, 2),
    "상중궁": (3, 2),
    "상우궁": (5, 2),
    "중좌궁": (1, 1),
    "중궁":   (3, 1),
    "중우궁": (5, 1),
    "하좌궁": (1, 0),
    "하중궁": (3, 0),
    "하우궁": (5, 0),
}

# The handwritten diagram transcribed onto a regular lattice.
#
# Horizontal lattice positions use integer x coordinates from 0 to 6.
# Vertical levels use y coordinates from -1 to 3.
VALUES: Final = {
    # Top row
    (1, 3): 23,
    (3, 3): 28,
    (5, 3): 21,

    (0, 2): 20,
    (1, 2): 4,
    (2, 2): 16,
    (3, 2): 9,
    (4, 2): 14,
    (5, 2): 2,
    (6, 2): 33,

    (1, 1.5): 22,
    (3, 1.5): 18,
    (5, 1.5): 15,

    # Middle row
    (0, 1): 31,
    (1, 1): 3,
    (2, 1): 19,
    (3, 1): 5,
    (4, 1): 26,
    (5, 1): 7,
    (6, 1): 25,

    (1, 0.5): 10,
    (3, 0.5): 17,
    (5, 0.5): 12,

    # Bottom row
    (0, 0): 29,
    (1, 0): 8,
    (2, 0): 11,
    (3, 0): 1,
    (4, 0): 24,
    (5, 0): 6,
    (6, 0): 30,

    (1, -1): 27,
    (3, -1): 32,
    (5, -1): 13,
}

# Each palace is defined by its center and four orthogonal neighbors.
PALACES: Final = {
    "상좌궁": ((1, 2), (0, 2), (2, 2), (1, 3), (1, 1.5)),
    "상중궁": ((3, 2), (2, 2), (4, 2), (3, 3), (3, 1.5)),
    "상우궁": ((5, 2), (4, 2), (6, 2), (5, 3), (5, 1.5)),

    "중좌궁": ((1, 1), (0, 1), (2, 1), (1, 1.5), (1, 0.5)),
    "중궁":   ((3, 1), (2, 1), (4, 1), (3, 1.5), (3, 0.5)),
    "중우궁": ((5, 1), (4, 1), (6, 1), (5, 1.5), (5, 0.5)),

    "하좌궁": ((1, 0), (0, 0), (2, 0), (1, 0.5), (1, -1)),
    "하중궁": ((3, 0), (2, 0), (4, 0), (3, 0.5), (3, -1)),
    "하우궁": ((5, 0), (4, 0), (6, 0), (5, 0.5), (5, -1)),
}

RESIDUE_STYLE: Final = {
    1: {
        "label": "n mod 5 ≡ 1",
        "face": "#444444",
        "edge": "#111111",
        "text": "#FFFFFF",
    },
    2: {
        "label": "n mod 5 ≡ 2",
        "face": "#F3CCCC",
        "edge": "#B53A3A",
        "text": "#702020",
    },
    3: {
        "label": "n mod 5 ≡ 3",
        "face": "#CFE0F5",
        "edge": "#3B6FAE",
        "text": "#244C7A",
    },
    4: {
        "label": "n mod 5 ≡ 4",
        "face": "#D8D8D8",
        "edge": "#555555",
        "text": "#222222",
    },
    0: {
        "label": "n mod 5 ≡ 0",
        "face": "#F4DFA0",
        "edge": "#B18400",
        "text": "#6A5000",
    },
}

RESIDUE_COUNTS: Final = {
    1: 7,
    2: 7,
    3: 7,
    4: 6,
    0: 6,
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

    raise RuntimeError(
        "한글·한자 글꼴을 찾지 못했습니다. "
        "Noto Sans CJK KR 또는 나눔고딕을 설치하십시오."
    )


def residue_group(number: int) -> int:
    return number % 5


def validate() -> None:
    numbers = list(VALUES.values())

    if sorted(numbers) != list(range(1, 34)):
        raise ValueError("1부터 33까지의 수가 정확히 한 번씩 있어야 합니다.")

    if sum(numbers) != 561:
        raise ValueError("1부터 33까지의 합은 561이어야 합니다.")

    for palace_name, coordinates in PALACES.items():
        palace_sum = sum(VALUES[coordinate] for coordinate in coordinates)

        if palace_sum != TARGET_SUM:
            raise ValueError(
                f"{palace_name}의 합은 {palace_sum}입니다. "
                f"{TARGET_SUM}이어야 합니다."
            )

    actual_counts = {
        residue: sum(
            1 for number in numbers if residue_group(number) == residue
        )
        for residue in (1, 2, 3, 4, 0)
    }

    if actual_counts != RESIDUE_COUNTS:
        raise ValueError(
            f"residue group 개수가 노트와 다릅니다: {actual_counts}"
        )

    # Each of the nine palace sums is 85, so repeated palace-total accounting is 765.
    repeated_total = sum(
        sum(VALUES[coordinate] for coordinate in coordinates)
        for coordinates in PALACES.values()
    )

    if repeated_total != TOTAL_SUM:
        raise ValueError(
            f"9궁의 중복 계수 합이 {repeated_total}입니다. "
            f"{TOTAL_SUM}이어야 합니다."
        )


def draw_edges(ax: Axes) -> None:
    # Three horizontal rows.
    horizontal_rows = (
        ((0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2)),
        ((0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)),
        ((0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)),
    )

    for row in horizontal_rows:
        for left, right in zip(row, row[1:]):
            ax.plot(
                [left[0], right[0]],
                [left[1], right[1]],
                color="#303030",
                linewidth=2.0,
                solid_capstyle="round",
                zorder=1,
            )

    # Vertical arms of the nine plus-shaped palaces.
    vertical_columns = {
        1: ((1, 3), (1, 2), (1, 1.5), (1, 1), (1, 0.5), (1, 0), (1, -1)),
        3: ((3, 3), (3, 2), (3, 1.5), (3, 1), (3, 0.5), (3, 0), (3, -1)),
        5: ((5, 3), (5, 2), (5, 1.5), (5, 1), (5, 0.5), (5, 0), (5, -1)),
    }

    for column in vertical_columns.values():
        for upper, lower in zip(column, column[1:]):
            ax.plot(
                [upper[0], lower[0]],
                [upper[1], lower[1]],
                color="#303030",
                linewidth=2.0,
                solid_capstyle="round",
                zorder=1,
            )


def draw_palace_boundaries(ax: Axes, font: FontProperties) -> None:
    # The handwritten notebook marks each palace with a large circular boundary.
    boundary_radius = 1.15

    for palace_name, (x, y) in PALACE_CENTERS.items():
        ax.add_patch(
            Circle(
                (x, y),
                boundary_radius,
                facecolor="none",
                edgecolor="#888888",
                linewidth=1.0,
                linestyle=(0, (4, 4)),
                alpha=0.55,
                zorder=0,
            )
        )

        label_y = y + 1.30 if y >= 1 else y - 1.32

        ax.text(
            x,
            label_y,
            f"{palace_name}  합 85",
            ha="center",
            va="center",
            fontproperties=font,
            fontsize=9.5,
            color="#555555",
            zorder=4,
        )


def draw_nodes(ax: Axes, font: FontProperties) -> None:
    node_radius = 0.23

    for coordinate, number in VALUES.items():
        x, y = coordinate
        residue = residue_group(number)
        style = RESIDUE_STYLE[residue]

        ax.add_patch(
            Circle(
                (x, y),
                node_radius,
                facecolor=style["face"],
                edgecolor=style["edge"],
                linewidth=1.8,
                zorder=2,
            )
        )

        ax.text(
            x,
            y,
            str(number),
            ha="center",
            va="center",
            fontproperties=font,
            fontsize=11.5,
            color=style["text"],
            zorder=3,
        )


def draw_legend(ax: Axes, font: FontProperties) -> None:
    ax.axis("off")

    ax.text(
        0.0,
        0.98,
        "낙서오구도",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=18,
        weight="bold",
    )

    y = 0.91

    summary = (
        "정점: 1–33, 각 1회",
        "궁: 9개",
        "각 궁: 십자형 5정점",
        "각 궁의 합: 85",
        "9궁 중복 계수 합: 85 × 9 = 765",
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
            fontsize=11.2,
        )
        y -= 0.055

    y -= 0.015

    ax.text(
        0.0,
        y,
        "residue groups",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=14,
        weight="bold",
    )
    y -= 0.075

    for residue in (1, 2, 3, 4, 0):
        style = RESIDUE_STYLE[residue]
        values = sorted(
            number
            for number in VALUES.values()
            if residue_group(number) == residue
        )

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
            f"{style['label']} — {len(values)}개",
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontproperties=font,
            fontsize=10.6,
            weight="bold",
            color=style["text"],
        )

        ax.text(
            0.08,
            y - 0.022,
            ", ".join(str(value) for value in values),
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontproperties=font,
            fontsize=9.2,
            color="#333333",
        )

        y -= 0.09

    y -= 0.01

    ax.text(
        0.0,
        y,
        "원문 메모",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=14,
        weight="bold",
    )

    notes = (
        "五子各得 八十五數",
        "九宮共得 七百六十五數",
        "33자 1회 사용",
        "85 × 9 = 765",
    )

    y -= 0.065

    for note in notes:
        ax.text(
            0.02,
            y,
            note,
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontproperties=font,
            fontsize=11.0,
        )
        y -= 0.052


def draw(
    png_output: str | Path = "nakseo_ogudo.png",
    svg_output: str | Path = "nakseo_ogudo.svg",
) -> None:
    validate()
    font = find_cjk_font()

    fig = plt.figure(figsize=(13.5, 8.8), dpi=220)
    graph_ax = fig.add_axes([0.035, 0.07, 0.70, 0.86])
    legend_ax = fig.add_axes([0.765, 0.09, 0.21, 0.82])

    graph_ax.set_aspect("equal")
    graph_ax.set_xlim(-1.4, 7.4)
    graph_ax.set_ylim(-2.1, 4.1)
    graph_ax.axis("off")

    draw_palace_boundaries(graph_ax, font)
    draw_edges(graph_ax)
    draw_nodes(graph_ax, font)
    draw_legend(legend_ax, font)

    graph_ax.set_title(
        "낙서오구도 — 9궁·5자·각 합 85",
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
