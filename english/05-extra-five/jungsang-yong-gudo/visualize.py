# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

def plot_magic_star():
    # 1. Define 33 node coordinates respecting the diagram's geometric symmetry
    coords = {
        27: (-4, 4),  20: (0, 4),   33: (4, 4),
        15: (-2, 3),  16: (0, 3),   1: (2, 3),
        3: (-1.5, 2), 23: (0, 2),   13: (1.5, 2),
        24: (-1, 1),  10: (0, 1),   22: (1, 1),
        28: (-4, 0),  5: (-3, 0),   11: (-2, 0), 25: (-1, 0), 9: (0, 0), 7: (1, 0), 19: (2, 0), 31: (3, 0), 12: (4, 0),
        18: (-1, -1), 2: (0, -1),   30: (1, -1),
        26: (-1.5, -2), 29: (0, -2), 14: (1.5, -2),
        17: (-2, -3), 32: (0, -3),  21: (2, -3),
        8: (-4, -4),  6: (0, -4),   4: (4, -4)
    }

    # 2. Canvas and layout setup
    plt.figure(figsize=(10, 10))
    plt.title("Gusu-ryak: Heavy Hexagonal Star (Jungsang-yong-gudo)",
              fontsize=16, fontweight='bold', pad=20)

    # 3. Draw representative symmetry axes that satisfy the constant 147
    # Vertical center axis (sum: 147)
    vertical_axis = [20, 16, 23, 10, 9, 2, 29, 32, 6]
    x_v = [coords[n][0] for n in vertical_axis]
    y_v = [coords[n][1] for n in vertical_axis]
    plt.plot(x_v, y_v, color='red', linestyle='--', alpha=0.5, label='Vertical Axis (Sum=147)')

    # Horizontal center axis (sum: 147)
    horizontal_axis = [28, 5, 11, 25, 9, 7, 19, 31, 12]
    x_h = [coords[n][0] for n in horizontal_axis]
    y_h = [coords[n][1] for n in horizontal_axis]
    plt.plot(x_h, y_h, color='blue', linestyle='--', alpha=0.5, label='Horizontal Axis (Sum=147)')

    # Diagonal axes (auxiliary lines)
    diagonal1 = [27, 15, 3, 24, 9, 30, 14, 21, 4]
    x_d1 = [coords[n][0] for n in diagonal1]
    y_d1 = [coords[n][1] for n in diagonal1]
    plt.plot(x_d1, y_d1, color='green', linestyle=':', alpha=0.4)

    diagonal2 = [33, 1, 13, 22, 9, 18, 26, 17, 8]
    x_d2 = [coords[n][0] for n in diagonal2]
    y_d2 = [coords[n][1] for n in diagonal2]
    plt.plot(x_d2, y_d2, color='green', linestyle=':', alpha=0.4)

    # 4. Render nodes (distinguishing outer boundary nodes from inner nodes)
    for num, pos in coords.items():
        is_outer = num in [27, 20, 33, 28, 12, 8, 6, 4]
        color = '#E6F2FF' if is_outer else '#FFF0F5'
        edgecolor = '#1E90FF' if is_outer else '#FF1493'

        plt.scatter(pos[0], pos[1], s=1000, color=color, edgecolor=edgecolor, linewidth=2, zorder=3)
        plt.text(pos[0], pos[1], str(num), fontsize=12, fontweight='bold',
                 ha='center', va='center', zorder=4)

    plt.axis('equal')
    plt.axis('off')
    plt.legend(loc='upper right')
    plt.tight_layout()

    # Save and display the image
    plt.savefig('gusu_ryak_star.png', dpi=300)
    plt.show()

if __name__ == '__main__':
    plot_magic_star()
