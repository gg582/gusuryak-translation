from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.font_manager import FontProperties


POSITIONS = {
    19: (-2,  3),
    2:  (-3,  2),
    14: (-2,  1),
    5:  (-1,  0),
    16: ( 0,  1),
    7:  (-1,  2),

    17: ( 2,  3),
    4:  ( 1,  2),
    9:  ( 3,  2),
    12: ( 2,  1),
    10: ( 1,  0),

    18: (-2, -1),
    3:  (-3, -2),
    13: (-2, -3),
    8:  (-1, -2),
    11: ( 0, -1),

    6:  ( 2, -1),
    1:  ( 3, -2),
    20: ( 2, -3),
    15: ( 1, -2),
}

EDGES = [
    (19, 2), (2, 14), (14, 5), (5, 16), (16, 7), (7, 19),
    (17, 4), (4, 16), (16, 10), (10, 12), (12, 9), (9, 17),
    (5, 18), (18, 3), (3, 13), (13, 8), (8, 11), (11, 5),
    (10, 6), (6, 1), (1, 20), (20, 15), (15, 11), (11, 10),
]

LABELS = {i: str(i) for i in range(1, 21)}


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


def draw_graph(
    png_output: str | Path = "sanhak_graph.png",
    svg_output: str | Path = "sanhak_graph.svg",
) -> None:
    font = get_font()

    fig, ax = plt.subplots(figsize=(8, 8), dpi=240)
    ax.set_aspect("equal")
    ax.set_xlim(-3.65, 3.65)
    ax.set_ylim(-3.65, 3.65)
    ax.axis("off")

    for start, end in EDGES:
        x1, y1 = POSITIONS[start]
        x2, y2 = POSITIONS[end]

        ax.plot(
            [x1, x2],
            [y1, y2],
            color="black",
            linewidth=2.0,
            solid_capstyle="round",
            zorder=1,
        )

    radius = 0.29

    for number, (x, y) in POSITIONS.items():
        ax.add_patch(
            Circle(
                (x, y),
                radius,
                facecolor="white",
                edgecolor="black",
                linewidth=2.0,
                zorder=2,
            )
        )

        ax.text(
            x,
            y,
            LABELS[number],
            ha="center",
            va="center",
            fontproperties=font,
            fontsize=15 if number < 10 else 12.5,
            zorder=3,
        )

    fig.savefig(
        png_output,
        dpi=300,
        bbox_inches="tight",
        pad_inches=0.08,
        facecolor="white",
    )
    fig.savefig(
        svg_output,
        bbox_inches="tight",
        pad_inches=0.08,
        facecolor="white",
    )
    plt.close(fig)


if __name__ == "__main__":
    draw_graph()
