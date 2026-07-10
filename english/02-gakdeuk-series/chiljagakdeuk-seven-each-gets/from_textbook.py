from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib import font_manager


TITLE = "Chiljagakdeuk (Seven-Each-Gets)\nSeven groups, each on its own"
OUTPUT_STEM = "chiljagakdeuk_example"

EXAMPLE_GROUPS = [
    [29, 1, 24, 34, 11, 19, 2],
    [6, 33, 23, 13, 34, 8, 3],
    [22, 7, 20, 30, 26, 10, 5],
    [15, 28, 9, 18, 32, 14, 4],
    [35, 16, 21, 24, 6, 17, 1],
]

GROUP_POSITIONS = [
    (0.0, 2.4),
    (-2.4, 0.0),
    (0.0, 0.0),
    (2.4, 0.0),
    (0.0, -2.4),
]

SLOT_OFFSETS = [
    (-0.75, 0.45),
    (0.0, 0.75),
    (0.75, 0.45),
    (0.65, -0.45),
    (0.0, -0.75),
    (-0.65, -0.45),
    (0.0, 0.0),
]


def setup_font():
    font_candidates = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/truetype/unifont/unifont.ttf",
    ]

    for font_path in font_candidates:
        path = Path(font_path)
        if path.exists():
            font_manager.fontManager.addfont(str(path))
            plt.rcParams["font.family"] = font_manager.FontProperties(fname=str(path)).get_name()
            break

    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42


def draw_group(ax, values, center):
    cx, cy = center
    ax.add_patch(plt.Circle((cx, cy), 1.1, fill=False, linewidth=1.8))

    for value, (dx, dy) in zip(values, SLOT_OFFSETS):
        x = cx + dx
        y = cy + dy

        if dx != 0.0 or dy != 0.0:
            ax.plot([cx, x], [cy, y], linewidth=0.8)

        ax.text(
            x,
            y,
            str(value),
            ha="center",
            va="center",
            fontsize=13,
            bbox={
                "boxstyle": "circle,pad=0.25",
                "facecolor": "white",
                "edgecolor": "black",
            },
        )

    ax.text(cx, cy - 1.35, f"sum = {sum(values)}", ha="center", fontsize=11)


def main():
    setup_font()

    fig, ax = plt.subplots(figsize=(8, 8))

    for values, center in zip(EXAMPLE_GROUPS, GROUP_POSITIONS):
        draw_group(ax, values, center)

    ax.set_aspect("equal")
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.axis("off")
    ax.set_title(TITLE, fontsize=16)

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_STEM}.png", dpi=200)
    plt.savefig(f"{OUTPUT_STEM}.pdf")
    plt.show()


if __name__ == "__main__":
    main()
