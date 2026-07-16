import matplotlib.pyplot as plt
import numpy as np

# 1. Define the arrangement on a 7x7 grid (row, col indices are 0..6).
#    Empty cells are represented by None. The missing numbers (11, 15, 29)
#    are filled into symmetric positions.
grid_data = [
    # Row 1 (index 0)
    [5, 11, 30, 25, 4, 32, 9],
    # Row 2 (index 1)
    [36, None, 17, None, 33, None, 28],
    # Row 3 (index 2)
    [1, 40, 24, 18, 12, None, 13],
    # Row 4 (index 3)
    [27, None, 23, None, 19, None, 16],
    # Row 5 (index 4)
    [8, 26, 15, 22, 31, 10, 35],
    # Row 6 (index 5)
    [37, None, 38, None, 20, None, 2],  # Existing typo '28' corrected to '38'
    # Row 7 (index 6)
    [7, 34, 3, 14, 21, 39, 6]
]

# Fill the empty cell that most likely holds 29 according to the grid shape
# (position may be adjusted if necessary).
grid_data[2][5] = 29

def get_color_properties(val):
    """Classify border color and background color by n mod 5."""
    rem = val % 5
    if rem == 1:   # Black
        return '#333333', '#F9F9F9'
    elif rem == 2: # Red
        return '#E05A6D', '#FFF5F5'
    elif rem == 3: # Blue
        return '#4D88E5', '#F0F5FF'
    elif rem == 0: # Yellow
        return '#E5C14D', '#FFFFF0'
    else:          # Grey (rem == 4)
        return '#888888', '#FAFAFA'

def draw_ojungto():
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.axis('off')

    # Draw 7x7 grid lines (well-field pattern emphasis)
    for i in range(8):
        ax.plot([0, 7], [i, i], color='#CCCCCC', lw=1, zorder=1)
        ax.plot([i, i], [0, 7], color='#CCCCCC', lw=1, zorder=1)

    for r in range(7):
        for c in range(7):
            val = grid_data[r][c]
            if val is not None:
                # matplotlib y-axis runs bottom to top, so invert the row
                cx = c + 0.5
                cy = 7 - (r + 0.5)

                edge_color, face_color = get_color_properties(val)

                # Draw a numbered circle
                circle = plt.Circle((cx, cy), 0.38, facecolor=face_color,
                                    edgecolor=edge_color, lw=2.5, zorder=3)
                ax.add_patch(circle)

                # Render the number
                ax.text(cx, cy, str(val), fontsize=13, fontweight='bold',
                        ha='center', va='center', color='#222222', zorder=4)

    # Add title
    plt.title("O-pal-jeong-jeon-do (五八井田圖) Restoration Design",
              fontsize=16, fontweight='bold', pad=20)

    ax.set_xlim(0, 7)
    ax.set_ylim(0, 7)
    plt.tight_layout()
    plt.savefig('ojungto_pattern.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    draw_ojungto()
