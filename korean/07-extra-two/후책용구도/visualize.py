import matplotlib.pyplot as plt
from matplotlib.patches import Circle

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


formations = [

    # Row 1
    dict(
        top=(5, 68),
        left=(33, 45),
        right=(41, 31),
        bottom=(67, 6),
        sums=(73, 74, 72, 73),
    ),

    dict(
        top=(3, 70),
        left=(34, 40),
        right=(39, 33),
        bottom=(64, 4),
        sums=(73, 74, 72, 73),
    ),

    dict(
        top=(73, 1),
        left=(36, 38),
        right=(37, 35),
        bottom=(71, 2),
        sums=(74, 74, 72, 73),
    ),

    # Row 2
    dict(
        top=(18, 55),
        left=(19, 56),
        right=(54, 20),
        bottom=(11, 62),
        sums=(73, 74, 74, 73),
    ),

    dict(
        top=(16, 57),
        left=(21, 51),
        right=(52, 22),
        bottom=(58, 15),
        sums=(73, 72, 74, 73),
    ),

    dict(
        top=(14, 59),
        left=(23, 49),
        right=(50, 24),
        bottom=(60, 13),
        sums=(73, 72, 74, 73),
    ),

    # Row 3
    dict(
        top=(11, 62),
        left=(26, 48),
        right=(42, 25),
        bottom=(61, 12),
        sums=(73, 74, 72, 73),
    ),

    dict(
        top=(9, 64),
        left=(28, 46),
        right=(45, 27),
        bottom=(63, 10),
        sums=(73, 74, 72, 73),
    ),

    dict(
        top=(7, 66),
        left=(30, 44),
        right=(43, 29),
        bottom=(65, 8),
        sums=(73, 74, 72, 73),
    ),
]

fig, ax = plt.subplots(figsize=(12, 12))

spacing_x = 5.4
spacing_y = 5.6

for r in range(3):
    for c in range(3):
        f = formations[r * 3 + c]

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
plt.savefig("후책용구도(侯策用九圖).png", dpi=300)
plt.savefig("후책용구도(侯策用九圖).svg")
plt.show()
