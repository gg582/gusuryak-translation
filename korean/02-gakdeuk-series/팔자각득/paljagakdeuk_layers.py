from __future__ import annotations

"""
八子各得 (팔자각득) 기초 시각화

이 파일은 팔자각득의 원본 교차 구조를 한자 라벨과 mod 5 색상으로
보여주는 기초 시각화 스크립트이다.

현대 그래프·조합론적 심층 분석은 analyze_paljagakdeuk.py,
analysis_report.md, blog.md 를 참조한다.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Circle, FancyBboxPatch


PALACES = {
    "upper_palace": [
        [39, 7, 34],
        [12, None, 19],
        [24, 2, 27],
    ],
    "left_palace": [
        [33, 18, 28],
        [8, None, 3],
        [38, 13, 23],
    ],
    "center_palace": [
        [30, 5, 21],
        [16, None, 15],
        [31, 10, 36],
    ],
    "right_palace": [
        [22, 14, 37],
        [4, None, 9],
        [29, 17, 32],
    ],
    "lower_palace": [
        [26, 1, 25],
        [20, None, 11],
        [35, 6, 40],
    ],
}

# Each 3×3 palace is positioned as one arm of the cross.
PALACE_ORIGINS = {
    "upper_palace": (3, 6),
    "left_palace": (0, 3),
    "center_palace": (3, 3),
    "right_palace": (6, 3),
    "lower_palace": (3, 0),
}

DISPLAY_LABELS = {
    "upper_palace": "상궁",
    "left_palace": "좌궁",
    "center_palace": "중궁",
    "right_palace": "우궁",
    "lower_palace": "하궁",
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
        raise ValueError("도상은 1부터 40까지의 수를 정확히 한 번씩 포함해야 합니다.")

    if sum(all_values) != 820:
        raise ValueError("1부터 40까지의 합은 820이어야 합니다.")

    for palace_name, grid in PALACES.items():
        values = palace_values(grid)

        if len(values) != 8:
            raise ValueError(f"{DISPLAY_LABELS[palace_name]}은 정확히 8개의 수를 포함해야 합니다.")

        if sum(values) != 164:
            raise ValueError(
                f"{DISPLAY_LABELS[palace_name]}의 합은 {sum(values)}로, 164가 아닙니다."
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
        f"{DISPLAY_LABELS[palace_name]} · 8자 · 합 164",
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
        "八子各得 — 1부터 40까지, 오궁마다 8자·합 164",
        fontproperties=font,
        fontsize=17,
        pad=18,
    )

    info.axis("off")
    info.text(
        0.0,
        0.98,
        "구조와 검산",
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=16,
        weight="bold",
    )

    summary_lines = [
        "• 사용 수: 1–40, 각 1회",
        "• 전체 합: 820",
        "• 궁의 수: 5",
        "• 각 궁: 3×3에서 중심을 비운 8자",
        "• 각 궁의 합: 164",
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
        "mod 5 계층",
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
        "노트의 일반화",
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
        "따라서  M(n+1) = M(n) + 8",
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
