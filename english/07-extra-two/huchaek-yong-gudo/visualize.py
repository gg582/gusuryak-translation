import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from huchaek_data import FORMATIONS

R = 0.28


def node(ax, x, y, text):
    ax.add_patch(Circle((x, y), R, facecolor="white",
                        edgecolor="black", linewidth=1.5))
    ax.text(x, y, str(text),
            ha="center", va="center",
            fontsize=11)


def line(ax, p1, p2):
    ax.plot([p1[0], p2[0]],
            [p1[1], p2[1]],
            color="black",
            linewidth=1.5)


def formation(ax, cx, cy,
              top,
              left,
              right,
              bottom,
              top_sum,
              left_sum,
              right_sum,
              bottom_sum):
    """
    One Huchaek-yong-gudo formation.

          a---b

      c       e
      d       f

          g---h
    """

    x = 1.15
    y = 0.95

    pos = {
        "a": (cx - 0.45, cy + 1.5 * y),
        "b": (cx + 0.45, cy + 1.5 * y),

        "c": (cx - x, cy + 0.5 * y),
        "d": (cx - x, cy - 0.5 * y),

        "e": (cx + x, cy + 0.5 * y),
        "f": (cx + x, cy - 0.5 * y),

        "g": (cx - 0.45, cy - 1.5 * y),
        "h": (cx + 0.45, cy - 1.5 * y),
    }

    line(ax, pos["a"], pos["b"])
    line(ax, pos["c"], pos["d"])
    line(ax, pos["e"], pos["f"])
    line(ax, pos["g"], pos["h"])

    vals = {
        "a": top[0],
        "b": top[1],
        "c": left[0],
        "d": left[1],
        "e": right[0],
        "f": right[1],
        "g": bottom[0],
        "h": bottom[1],
    }

    for k in vals:
        node(ax, *pos[k], vals[k])

    ax.text(cx, cy + 2.05, str(top_sum),
            ha="center", fontsize=13)

    ax.text(cx - 1.65, cy, str(left_sum),
            ha="center", fontsize=13, color="blue")

    ax.text(cx + 1.65, cy, str(right_sum),
            ha="center", fontsize=13, color="red")

    ax.text(cx, cy - 2.05, str(bottom_sum),
            ha="center", fontsize=13)


def main():
    fig, ax = plt.subplots(figsize=(12, 12))

    spacing_x = 5.4
    spacing_y = 5.6

    for r in range(3):
        for c in range(3):
            f = FORMATIONS[r * 3 + c]

            formation(
                ax,
                c * spacing_x,
                -r * spacing_y,
                top=f["top"],
                left=f["left"],
                right=f["right"],
                bottom=f["bottom"],
                top_sum=f["sums"][0],
                left_sum=f["sums"][1],
                right_sum=f["sums"][2],
                bottom_sum=f["sums"][3],
            )

    ax.set_aspect("equal")
    ax.set_xlim(-2.5, spacing_x * 2 + 2.5)
    ax.set_ylim(-spacing_y * 2 - 3, 3)
    ax.axis("off")

    plt.tight_layout()
    plt.savefig("Huchaek-yong-gudo(侯策用九圖).png", dpi=300)
    plt.savefig("Huchaek-yong-gudo(侯策用九圖).svg")
    plt.show()


if __name__ == "__main__":
    main()
