#!/usr/bin/env python3
"""Visualize pair-sum classes in the Huchaek-yong-gudo working diagram."""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from huchaek_data import CORRECTED_FORMATIONS, FORMATIONS


RADIUS = 0.28
SPACING_X = 5.4
SPACING_Y = 5.6

COLORS = {
    73: "#1b9e77",
    74: "#1f78b4",
    72: "#d95f02",
}
FALLBACK_COLOR = "#b22222"


def formation_positions(cx: float, cy: float) -> dict[str, tuple[float, float]]:
    x = 1.15
    y = 0.95
    return {
        "a": (cx - 0.45, cy + 1.5 * y),
        "b": (cx + 0.45, cy + 1.5 * y),
        "c": (cx - x, cy + 0.5 * y),
        "d": (cx - x, cy - 0.5 * y),
        "e": (cx + x, cy + 0.5 * y),
        "f": (cx + x, cy - 0.5 * y),
        "g": (cx - 0.45, cy - 1.5 * y),
        "h": (cx + 0.45, cy - 1.5 * y),
    }


def draw_line(ax, p1, p2, total: int) -> None:
    color = COLORS.get(total, FALLBACK_COLOR)
    linestyle = "-" if total in COLORS else (0, (4, 2))
    ax.plot(
        [p1[0], p2[0]],
        [p1[1], p2[1]],
        color=color,
        linewidth=2.4,
        linestyle=linestyle,
        zorder=1,
    )


def draw_node(ax, x: float, y: float, value: int) -> None:
    ax.add_patch(
        Circle((x, y), RADIUS, facecolor="white", edgecolor="black", linewidth=1.4, zorder=2)
    )
    ax.text(x, y, str(value), ha="center", va="center", fontsize=11, zorder=3)


def draw_formation(ax, formation: dict, cx: float, cy: float) -> None:
    pos = formation_positions(cx, cy)
    values = {
        "a": formation["top"][0],
        "b": formation["top"][1],
        "c": formation["left"][0],
        "d": formation["left"][1],
        "e": formation["right"][0],
        "f": formation["right"][1],
        "g": formation["bottom"][0],
        "h": formation["bottom"][1],
    }
    sides = [
        ("top", "a", "b"),
        ("left", "c", "d"),
        ("right", "e", "f"),
        ("bottom", "g", "h"),
    ]

    for side, start_key, end_key in sides:
        total = sum(formation[side])
        draw_line(ax, pos[start_key], pos[end_key], total)
        midpoint = (
            (pos[start_key][0] + pos[end_key][0]) / 2,
            (pos[start_key][1] + pos[end_key][1]) / 2,
        )
        ax.text(
            midpoint[0],
            midpoint[1],
            str(total),
            ha="center",
            va="center",
            fontsize=10,
            color=COLORS.get(total, FALLBACK_COLOR),
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.6},
            zorder=4,
        )

    for key, value in values.items():
        draw_node(ax, *pos[key], value)

    total = sum(sum(formation[side]) for side in ("top", "left", "right", "bottom"))
    ax.text(cx, cy, str(total), ha="center", va="center", fontsize=13, color="#333333")


def draw_legend(ax) -> None:
    items = [
        ("73 pair: octagon complement edge", COLORS[73]),
        ("74 pair: square high edge", COLORS[74]),
        ("72 pair: square low edge", COLORS[72]),
        ("other: outside current rule", FALLBACK_COLOR),
    ]
    x0 = -2.2
    y0 = -SPACING_Y * 2 - 2.65
    for index, (label, color) in enumerate(items):
        y = y0 - index * 0.35
        ax.plot([x0, x0 + 0.5], [y, y], color=color, linewidth=2.4)
        ax.text(x0 + 0.65, y, label, ha="left", va="center", fontsize=10)


def draw(formations: list[dict], filename_prefix: str, title_suffix: str) -> None:
    fig, ax = plt.subplots(figsize=(12, 12))

    for row in range(3):
        for col in range(3):
            draw_formation(
                ax,
                formations[row * 3 + col],
                col * SPACING_X,
                -row * SPACING_Y,
            )

    ax.text(
        SPACING_X,
        2.65,
        f"Huchaek-yong-gudo pair-sum classes: 73 / 74 / 72{title_suffix}",
        ha="center",
        va="center",
        fontsize=14,
    )
    draw_legend(ax)

    ax.set_aspect("equal")
    ax.set_xlim(-2.5, SPACING_X * 2 + 2.5)
    ax.set_ylim(-SPACING_Y * 2 - 4.1, 3.0)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(f"{filename_prefix}.png", dpi=300, facecolor="white")
    plt.savefig(f"{filename_prefix}.svg", facecolor="white")
    plt.show()


def main() -> None:
    draw(FORMATIONS, "huchaek_rule_pairs", "")


if __name__ == "__main__":
    main()
