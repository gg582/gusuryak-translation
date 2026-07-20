from __future__ import annotations

from pathlib import Path
from typing import Final

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Circle, Polygon


TITLE: Final = "지수용육도"
HANJA_TITLE: Final = "地數用六圖"
SUBTITLE: Final = "六子各得六十三數"
TARGET_SUM: Final = 63

# 손그림의 구조를 반듯한 벌집형 격자로 정규화했다.
# 다섯 육각형은 인접 육각형과 일부 정점·간선을 공유한다.
POSITIONS: Final = {
    # 상단 왼쪽 육각형의 외곽
    5:  (-2.0,  4.5),
    18: (-3.0,  3.6),
    16: (-3.0,  2.5),
    3:  (-2.0,  1.7),
    8:  (-1.0,  2.5),
    13: (-1.0,  3.6),

    # 상단 오른쪽 육각형의 외곽
    1:  ( 0.0,  4.5),
    7:  ( 1.0,  3.6),
    20: ( 1.0,  2.5),
    14: ( 0.0,  1.7),

    # 중앙 육각형의 하단
    12: (-2.0,  0.3),
    11: (-1.0, -0.5),
    15: ( 0.0,  0.3),

    # 하단 왼쪽 육각형의 외곽
    9:  (-3.0, -0.5),
    19: (-3.0, -1.7),
    2:  (-2.0, -2.5),
    10: (-1.0, -1.7),

    # 하단 오른쪽 육각형의 외곽
    4:  ( 1.0, -0.5),
    17: ( 1.0, -1.7),
    6:  ( 0.0, -2.5),
}

# 각 육각형은 시계 방향의 6개 정점으로 정의한다.
HEXAGONS: Final = {
    "upper_left": (5, 18, 16, 3, 8, 13),
    "upper_right": (1, 13, 8, 14, 20, 7),
    "center": (3, 8, 14, 15, 11, 12),
    "lower_left": (12, 11, 10, 2, 19, 9),
    "lower_right": (15, 4, 17, 6, 10, 11),
}

DISPLAY_LABELS: Final = {
    "upper_left": "상좌",
    "upper_right": "상우",
    "center": "중앙",
    "lower_left": "하좌",
    "lower_right": "하우",
}

# 노트에 표시된 mod 5 색 구분을 유지한다.
RESIDUE_STYLE: Final = {
    1: {
        "label": "n mod 5 ≡ 1",
        "face": "#3F3F3F",
        "edge": "#161616",
        "text": "#FFFFFF",
        "legend_text": "#222222",
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
        raise ValueError("1부터 20까지의 수가 정확히 한 번씩 있어야 합니다.")

    grouped = sorted(
        number
        for group in RESIDUE_GROUPS.values()
        for number in group
    )

    if grouped != list(range(1, 21)):
        raise ValueError("잉여류 그룹이 1부터 20까지를 정확히 분할해야 합니다.")

    for residue, group in RESIDUE_GROUPS.items():
        for number in group:
            if number % 5 != residue:
                raise ValueError(
                    f"{number}가 잘못된 잉여류 그룹에 들어 있습니다."
                )

    for name, vertices in HEXAGONS.items():
        value_sum = sum(vertices)

        if value_sum != TARGET_SUM:
            raise ValueError(
                f"{name} 육각형의 합은 {value_sum}이며, "
                f"{TARGET_SUM}이어야 합니다."
            )


def unique_edges() -> list[tuple[int, int]]:
    edges: set[tuple[int, int]] = set()

    for vertices in HEXAGONS.values():
        for start, end in zip(vertices, vertices[1:] + vertices[:1]):
            edge = tuple(sorted((start, end)))
            edges.add(edge)

    return sorted(edges)


def draw_hexagon_regions(ax: Axes, font: FontProperties) -> None:
    # 큰 연필 원 대신 육각형 자체를 아주 옅게 강조한다.
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
            f"합 {TARGET_SUM}",
            ha="center",
            va="center",
            fontproperties=font,
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
        "정점: 1–20, 각 1회",
        "육각형: 5개",
        "각 육각형: 6개 정점",
        "각 육각형의 합: 63",
        "육각형별 정점 사용 횟수 합: 30",
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
        "mod 5 잉여 클래스",
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
            f"{style['label']} · 4개",
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontproperties=font,
            fontsize=10.8,
            weight="bold",
            color=style.get("legend_text", style["text"]),
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
        "육각형별 검산",
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
            f"{DISPLAY_LABELS[name]}: {expression} = 63",
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

    draw_hexagon_regions(graph_ax, font)
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
