from __future__ import annotations

from pathlib import Path
from typing import Final

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Circle


# The handwritten diagram is normalized onto a clean coordinate system.
# The original relative structure is preserved, but all rows and columns are straightened.
POSITIONS: Final = {
    19: (0.0, 6.0),

    12: (-1.5, 5.0),
    8:  (1.5, 5.0),

    6:  (0.0, 4.2),

    4:  (-2.8, 3.3),
    20: (0.0, 3.3),
    7:  (2.8, 3.3),

    21: (-4.2, 2.0),
    23: (-2.8, 2.0),
    1:  (-1.4, 2.0),
    5:  (0.0, 2.0),
    15: (1.4, 2.0),
    14: (2.8, 2.0),
    18: (4.2, 2.0),

    16: (-2.8, 0.8),
    24: (0.0, 0.8),
    11: (2.8, 0.8),

    9:  (-1.8, -0.4),
    17: (0.0, -0.4),
    13: (1.8, -0.4),

    2:  (0.0, -1.7),
}

GROUPS: Final = {
    1: [1, 6, 11, 16, 21],
    2: [2, 7, 12, 17],
    3: [8, 13, 18, 23],
    4: [4, 9, 14, 19, 24],
    0: [5, 15, 20],
}

STYLE: Final = {
    1: {
        "name": "G1 · n mod 5 ≡ 1",
        "face": "#E0E0E0",
        "edge": "#333333",
        "text": "#111111",
    },
    2: {
        "name": "G2 · n mod 5 ≡ 2",
        "face": "#F4D0D0",
        "edge": "#B33B3B",
        "text": "#7A2020",
    },
    3: {
        "name": "G3 · n mod 5 ≡ 3",
        "face": "#D4E4F8",
        "edge": "#3A6FAE",
        "text": "#244E80",
    },
    4: {
        "name": "G4 · n mod 5 ≡ 4",
        "face": "#E5E5E5",
        "edge": "#666666",
        "text": "#222222",
    },
    0: {
        "name": "G5 · n mod 5 ≡ 0",
        "face": "#F6E5A3",
        "edge": "#C39A00",
        "text": "#735700",
    },
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


def residue_of(number: int) -> int:
    return number % 5


def validate() -> None:
    grouped_numbers = [
        number
        for numbers in GROUPS.values()
        for number in numbers
    ]

    if sorted(grouped_numbers) != sorted(POSITIONS):
        raise ValueError(
            "GROUPS와 POSITIONS는 정확히 같은 수를 각각 한 번씩 포함해야 합니다."
        )

    for number in POSITIONS:
        expected = residue_of(number)
        if number not in GROUPS[expected]:
            raise ValueError(
                f"{number}가 올바른 잉여 클래스에 배치되지 않았습니다."
            )


def draw(
    png_output: str | Path = "mod5_residue_diagram.png",
    svg_output: str | Path = "mod5_residue_diagram.svg",
) -> None:
    validate()
    font = find_cjk_font()

    fig = plt.figure(figsize=(12, 8), dpi=220)
    diagram_ax = fig.add_axes([0.04, 0.06, 0.68, 0.88])
    legend_ax = fig.add_axes([0.75, 0.10, 0.22, 0.80])

    diagram_ax.set_aspect("equal")
    diagram_ax.set_xlim(-5.0, 5.0)
    diagram_ax.set_ylim(-2.4, 6.8)
    diagram_ax.axis("off")

    node_radius = 0.38

    for number, (x, y) in POSITIONS.items():
        residue = residue_of(number)
        style = STYLE[residue]

        diagram_ax.add_patch(
            Circle(
                (x, y),
                node_radius,
                facecolor=style["face"],
                edgecolor=style["edge"],
                linewidth=2.1,
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
            fontsize=15,
            color=style["text"],
            zorder=3,
        )

    diagram_ax.set_title(
        "오자각득 mod 5 잉여 클래스 도식",
        fontproperties=font,
        fontsize=18,
        pad=16,
    )

    legend_ax.axis("off")

    legend_ax.text(
        0.0,
        0.98,
        "잉여 클래스",
        transform=legend_ax.transAxes,
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=17,
        weight="bold",
    )

    y = 0.88

    for residue in (1, 2, 3, 4, 0):
        style = STYLE[residue]
        numbers = GROUPS[residue]

        legend_ax.add_patch(
            Circle(
                (0.045, y),
                0.025,
                transform=legend_ax.transAxes,
                facecolor=style["face"],
                edgecolor=style["edge"],
                linewidth=1.6,
            )
        )

        legend_ax.text(
            0.10,
            y + 0.012,
            style["name"],
            transform=legend_ax.transAxes,
            ha="left",
            va="center",
            fontproperties=font,
            fontsize=11.5,
            weight="bold",
            color=style["text"],
        )

        legend_ax.text(
            0.10,
            y - 0.025,
            "{ " + ", ".join(str(number) for number in numbers) + " }",
            transform=legend_ax.transAxes,
            ha="left",
            va="top",
            fontproperties=font,
            fontsize=10.5,
            color="#333333",
        )

        y -= 0.15

    legend_ax.text(
        0.0,
        0.08,
        f"보이는 노드: {len(POSITIONS)}개",
        transform=legend_ax.transAxes,
        ha="left",
        va="bottom",
        fontproperties=font,
        fontsize=11,
    )

    fig.savefig(
        png_output,
        dpi=300,
        bbox_inches="tight",
        pad_inches=0.10,
        facecolor="white",
    )
    fig.savefig(
        svg_output,
        bbox_inches="tight",
        pad_inches=0.10,
        facecolor="white",
    )
    plt.close(fig)


if __name__ == "__main__":
    draw()
