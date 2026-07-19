import matplotlib.pyplot as plt
import numpy as np


groups = [
    {"center": 4, "surround": [31, 43, 22, 60, 27, 37], "source": ["ocr", "ocr", "rule", "ocr", "ocr", "ocr"], "pos": (1, 3)},
    {"center": 9, "surround": [15, 45, 36, 55, 10, 54], "source": ["ocr", "ocr", "rule", "ocr", "ocr", "ocr"], "pos": (2, 3)},
    {"center": 2, "surround": [28, 29, 39, 62, 17, 47], "source": ["ocr", "ocr", "ocr", "ocr", "ocr", "ocr"], "pos": (3, 3)},
    {"center": 3, "surround": [30, 40, 26, 61, 16, 48], "source": ["ocr", "ocr", "rule", "ocr", "ocr", "ocr"], "pos": (1, 2)},
    {"center": 5, "surround": [32, 41, 23, 59, 14, 50], "source": ["ocr", "ocr", "ocr", "ocr", "ocr", "ocr"], "pos": (2, 2)},
    {"center": 7, "surround": [34, 38, 24, 57, 20, 44], "source": ["ocr", "rule", "ocr", "ocr", "ocr", "ocr"], "pos": (3, 2)},
    {"center": 8, "surround": [35, 49, 12, 56, 11, 53], "source": ["ocr", "ocr", "ocr", "rule", "ocr", "ocr"], "pos": (1, 1)},
    {"center": 1, "surround": [52, 25, 19, 63, 18, 46], "source": ["ocr", "ocr", "ocr", "ocr", "rule", "rule"], "pos": (2, 1)},
    {"center": 6, "surround": [33, 42, 21, 58, 13, 51], "source": ["ocr", "ocr", "ocr", "ocr", "ocr", "rule"], "pos": (3, 1)},
]


def draw_pattern():
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_aspect("equal")
    ax.axis("off")

    group_spacing_x = 5.0
    group_spacing_y = 5.0

    for group in groups:
        cx = group["pos"][0] * group_spacing_x
        cy = group["pos"][1] * group_spacing_y

        outer_boundary = plt.Circle((cx, cy), 2.2, color="#F5F5F5", fill=True, zorder=1)
        ax.add_patch(outer_boundary)

        center_circle = plt.Circle((cx, cy), 0.5, color="#FFFFFF", ec="#333333", lw=1.5, zorder=3)
        ax.add_patch(center_circle)
        ax.text(cx, cy, str(group["center"]), fontsize=12, fontweight="bold", ha="center", va="center", zorder=4)

        for i, (value, source) in enumerate(zip(group["surround"], group["source"])):
            angle = np.deg2rad(90 - (60 * i))
            px = cx + 1.3 * np.cos(angle)
            py = cy + 1.3 * np.sin(angle)
            face = "#D9D9D9" if source == "rule" else "#FFFFFF"
            edge = "#666666" if source == "rule" else "#444444"
            circle = plt.Circle((px, py), 0.45, color=face, ec=edge, lw=1.2, zorder=3)
            ax.add_patch(circle)
            ax.text(px, py, str(value), fontsize=11, ha="center", va="center", zorder=4)

        ax.text(cx, cy - 2.5, f"sum {group['center'] + sum(group['surround'])}",
                fontsize=9, ha="center", va="center", color="#333333", zorder=4)

    ax.set_xlim(2, 18)
    ax.set_ylim(1.2, 18)
    ax.text(
        10, 1.35,
        "Gray cells are rule-reconstructed values: each palace sums to 224, and 1..63 is used exactly once.",
        fontsize=10,
        ha="center",
        va="center",
        color="#333333",
    )

    plt.tight_layout()
    plt.savefig("pattern_corrected.png", dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    draw_pattern()
