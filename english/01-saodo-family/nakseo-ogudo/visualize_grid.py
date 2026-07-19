import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.font_manager import FontProperties
from pathlib import Path

# Square-lattice coordinates and values for the 33 nodes of Nakseo Ogudo
VALUES = {
    (1, 5): 23, (3, 5): 28, (5, 5): 21,
    (0, 4): 20, (1, 4): 4, (2, 4): 16, (3, 4): 9, (4, 4): 14, (5, 4): 2, (6, 4): 33,
    (1, 3): 22, (3, 3): 18, (5, 3): 15,
    (0, 2): 31, (1, 2): 3, (2, 2): 19, (3, 2): 5, (4, 2): 26, (5, 2): 7, (6, 2): 25,
    (1, 1): 10, (3, 1): 17, (5, 1): 12,
    (0, 0): 29, (1, 0): 8, (2, 0): 11, (3, 0): 1, (4, 0): 24, (5, 0): 6, (6, 0): 30,
    (1, -1): 27, (3, -1): 32, (5, -1): 13,
}

PALACE_CENTERS = {
    "upper_left": (1, 4), "upper_center": (3, 4), "upper_right": (5, 4),
    "middle_left": (1, 2), "center": (3, 2), "middle_right": (5, 2),
    "lower_left": (1, 0), "lower_center": (3, 0), "lower_right": (5, 0),
}

DISPLAY_LABELS = {
    "upper_left": "Upper Left", "upper_center": "Upper Center", "upper_right": "Upper Right",
    "middle_left": "Middle Left", "center": "Center", "middle_right": "Middle Right",
    "lower_left": "Lower Left", "lower_center": "Lower Center", "lower_right": "Lower Right",
}

RESIDUE_STYLE = {
    1: {"face": "#444444", "edge": "#111111", "text": "#FFFFFF"},
    2: {"face": "#F3CCCC", "edge": "#B53A3A", "text": "#702020"},
    3: {"face": "#CFE0F5", "edge": "#3B6FAE", "text": "#244C7A"},
    4: {"face": "#D8D8D8", "edge": "#555555", "text": "#222222"},
    0: {"face": "#F4DFA0", "edge": "#B18400", "text": "#6A5000"},
}

def find_font() -> FontProperties:
    candidates = (
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "C:/Windows/Fonts/malgun.ttf",
    )
    for candidate in candidates:
        if Path(candidate).exists():
            return FontProperties(fname=candidate)
    return FontProperties(family="sans-serif")

def draw_grid_overview():
    font = find_font()
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    ax.set_aspect("equal")
    ax.set_xlim(-1.2, 7.2)
    ax.set_ylim(-1.8, 5.8)
    ax.axis("off")

    # Palace boundary guides (dashed circles)
    boundary_radius = 1.15
    for palace_name, (x, y) in PALACE_CENTERS.items():
        ax.add_patch(Circle((x, y), boundary_radius, facecolor="none", edgecolor="#CCCCCC", linewidth=1.0, linestyle=(0, (4, 4)), zorder=0))
        label_y = y + 1.25 if y >= 1 else y - 1.25
        ax.text(x, label_y, f"{DISPLAY_LABELS[palace_name]} (Sum 85)", ha="center", va="center", fontproperties=font, fontsize=9, color="#666666", zorder=1)

    # Horizontal grid lines
    horizontal_rows = (
        ((0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4)),
        ((0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2)),
        ((0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)),
    )
    for row in horizontal_rows:
        for left, right in zip(row, row[1:]):
            ax.plot([left[0], right[0]], [left[1], right[1]], color="#555555", linewidth=1.8, solid_capstyle="round", zorder=1)

    # Vertical grid lines
    vertical_columns = (
        ((1, 5), (1, 4), (1, 3), (1, 2), (1, 1), (1, 0), (1, -1)),
        ((3, 5), (3, 4), (3, 3), (3, 2), (3, 1), (3, 0), (3, -1)),
        ((5, 5), (5, 4), (5, 3), (5, 2), (5, 1), (5, 0), (5, -1)),
    )
    for col in vertical_columns:
        for upper, lower in zip(col, col[1:]):
            ax.plot([upper[0], lower[0]], [upper[1], lower[1]], color="#555555", linewidth=1.8, solid_capstyle="round", zorder=1)

    # Draw nodes
    node_radius = 0.22
    for coordinate, number in VALUES.items():
        x, y = coordinate
        style = RESIDUE_STYLE[number % 5]
        ax.add_patch(Circle((x, y), node_radius, facecolor=style["face"], edgecolor=style["edge"], linewidth=1.5, zorder=2))
        ax.text(x, y, str(number), ha="center", va="center", fontproperties=font, fontsize=10.5, color=style["text"], zorder=3)

    plt.title("Nakseo Ogudo (Five-Each-Gets) Global Grid Network Visualization", fontproperties=font, fontsize=14, pad=15)
    plt.tight_layout()
    plt.savefig("overview.png", dpi=300, bbox_inches="tight")
    plt.savefig("overview.svg", bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    draw_grid_overview()
