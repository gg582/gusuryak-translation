#!/usr/bin/env python3
"""Visualize the corrected Huchaek-yong-gudo working arrangement."""

from __future__ import annotations

import matplotlib.pyplot as plt

from huchaek_data import CORRECTED_FORMATIONS
from visualize import formation


def main() -> None:
    fig, ax = plt.subplots(figsize=(12, 12))

    spacing_x = 5.4
    spacing_y = 5.6

    for row in range(3):
        for col in range(3):
            item = CORRECTED_FORMATIONS[row * 3 + col]
            formation(
                ax,
                col * spacing_x,
                -row * spacing_y,
                top=item["top"],
                left=item["left"],
                right=item["right"],
                bottom=item["bottom"],
                top_sum=item["sums"][0],
                left_sum=item["sums"][1],
                right_sum=item["sums"][2],
                bottom_sum=item["sums"][3],
            )

    ax.set_aspect("equal")
    ax.set_xlim(-2.5, spacing_x * 2 + 2.5)
    ax.set_ylim(-spacing_y * 2 - 3, 3)
    ax.axis("off")

    plt.tight_layout()
    plt.savefig("Huchaek-yong-gudo_corrected.png", dpi=300, facecolor="white")
    plt.savefig("Huchaek-yong-gudo_corrected.svg", facecolor="white")
    plt.show()


if __name__ == "__main__":
    main()
