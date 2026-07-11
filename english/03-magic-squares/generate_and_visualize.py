#!/usr/bin/env python3
"""
Valid magic square correction generator and visualization script.

- Yukyukdo (Six-Six Board): already a valid magic square. Associated is impossible when n≡2 (mod 4), so no correction is generated.
- Gusudo (Nine Palace): already a valid magic square.
- 10×10 squares: generate valid 10×10 magic square corrections using the magic_square package.
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# Korean font setting (kept so generated visualizations can still render any Korean labels if needed)
font_path = "/usr/share/fonts/truetype/nanum/NanumSquare_acR.ttf"
font_manager.fontManager.addfont(font_path)
rc('font', family=font_manager.FontProperties(fname=font_path).get_name())
plt.rcParams['axes.unicode_minus'] = False

# Use magic_square from the virtual environment
import magic_square as ms

OUT_DIR = "/home/yjlee/gusuryak-translation/english/03-magic-squares"
FIG_DIR = os.path.join(OUT_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# ---------- Original data ----------

ORIGINALS = {
    "yukyukdo_example_1": np.array([
        [13, 22, 18, 27, 11, 20],
        [31, 4, 36, 9, 29, 2],
        [12, 21, 14, 23, 16, 25],
        [30, 3, 5, 32, 34, 7],
        [17, 26, 10, 19, 15, 24],
        [8, 35, 28, 1, 6, 33],
    ]),
    "yukyukdo_example_2": np.array([
        [4, 13, 36, 27, 29, 2],
        [22, 31, 18, 9, 11, 20],
        [3, 21, 23, 32, 25, 7],
        [30, 12, 5, 14, 16, 34],
        [17, 26, 19, 28, 6, 15],
        [35, 8, 10, 1, 24, 33],
    ]),
    "gusudo_example_1": np.array([
        [31, 76, 13, 36, 81, 18, 29, 74, 11],
        [22, 40, 58, 27, 45, 63, 20, 38, 56],
        [67, 4, 49, 72, 9, 54, 65, 2, 47],
        [30, 75, 12, 32, 77, 14, 34, 79, 16],
        [21, 39, 57, 23, 41, 59, 25, 43, 61],
        [66, 3, 48, 68, 5, 50, 70, 7, 52],
        [35, 80, 17, 28, 73, 10, 33, 78, 15],
        [26, 44, 62, 19, 37, 55, 24, 42, 60],
        [71, 8, 53, 64, 1, 46, 69, 6, 51],
    ]),
    "gusudo_example_2": np.array([
        [50, 18, 55, 70, 5, 48, 3, 76, 44],
        [66, 31, 26, 29, 81, 13, 52, 11, 60],
        [7, 74, 42, 24, 37, 62, 68, 36, 19],
        [54, 67, 2, 65, 25, 33, 28, 23, 72],
        [59, 21, 43, 9, 41, 73, 15, 61, 47],
        [10, 35, 78, 49, 57, 17, 80, 39, 4],
        [79, 6, 38, 20, 69, 34, 32, 64, 27],
        [30, 71, 22, 45, 1, 77, 16, 51, 56],
        [14, 46, 63, 58, 53, 12, 75, 8, 40],
    ]),
}


def is_normal_set(m):
    n = m.shape[0]
    return set(m.flatten()) == set(range(1, n * n + 1))


def is_associated(m):
    n = m.shape[0]
    comp = m + np.rot90(m, 2)
    return np.all(comp == n * n + 1)


def matrix_to_markdown(m, title):
    lines = [f"## {title}", ""]
    lines.append("```")
    for row in m:
        lines.append(" ".join(f"{x:3d}" for x in row))
    lines.append("```")
    lines.append("")
    n = m.shape[0]
    mc = n * (n * n + 1) // 2
    lines.append(f"- Order: {n}×{n}")
    lines.append(f"- Magic constant: {mc}")
    lines.append(f"- Normal set (1~{n*n}): {'Yes' if is_normal_set(m) else 'No'}")
    lines.append(f"- Magic square: {'Yes' if ms.ismagic(m) else 'No'}")
    lines.append(f"- Associated: {'Yes' if is_associated(m) else 'No'}")
    lines.append("")
    return "\n".join(lines)


def generate_corrected_10x10():
    """Generate four distinct valid 10×10 magic square corrections."""
    base = ms.magic(10)
    corrected = {
        "baekjajasuyin_yang_chakjong_correction": base.copy(),
        "baekjasaengseong_sunsu_correction": np.rot90(base, 1).copy(),
        "baekjasaengseong_gyosu_correction": np.fliplr(base).copy(),
        "baekjayin_yang_jamo_chakjong_correction": np.flipud(base).copy(),
    }
    return corrected


def visualize(m, title, path):
    n = m.shape[0]
    fig, ax = plt.subplots(figsize=(max(6, n * 0.75), max(6, n * 0.75)))
    cmap = plt.cm.viridis
    im = ax.imshow(m, cmap=cmap)

    for i in range(n):
        for j in range(n):
            color = "white" if m[i, j] > (n * n) / 2 else "black"
            ax.text(j, i, str(m[i, j]), ha="center", va="center",
                    color=color, fontsize=max(7, 14 - n))

    ax.set_title(title, fontsize=14)
    ax.set_xticks([])
    ax.set_yticks([])
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)


def main():
    corrected = generate_corrected_10x10()

    # Validation
    for name, m in corrected.items():
        assert is_normal_set(m), f"{name}: not normal set"
        assert ms.ismagic(m), f"{name}: not magic"
        print(f"{name}: normal={is_normal_set(m)}, magic={ms.ismagic(m)}, associated={is_associated(m)}")

    # Save corrections to corrected.md
    folder_map = {
        "baekjajasuyin_yang_chakjong_correction": "03-baekjajasuyin-yang-chakjong",
        "baekjasaengseong_sunsu_correction": "04-baekjasaengseong-sunsu",
        "baekjasaengseong_gyosu_correction": "05-baekjasaengseong-gyosu",
        "baekjayin_yang_jamo_chakjong_correction": "06-baekjayin-yang-jamo-chakjong",
    }

    for name, folder in folder_map.items():
        m = corrected[name]
        md = matrix_to_markdown(m, name.replace("_", " "))
        path = os.path.join(OUT_DIR, folder, "corrected.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# Valid Magic Square Correction\n\n")
            f.write(md)

    # Visualizations
    # Yukyukdo: originals only (valid magic square, associated impossible)
    for name, m in ORIGINALS.items():
        if name.startswith("yukyukdo"):
            visualize(m, f"Original: {name}", os.path.join(FIG_DIR, f"{name}.png"))

    # Gusudo: originals only
    for name, m in ORIGINALS.items():
        if name.startswith("gusudo"):
            visualize(m, f"Original: {name}", os.path.join(FIG_DIR, f"{name}.png"))

    # 10×10: corrections only
    for name, m in corrected.items():
        visualize(m, name.replace("_", " "), os.path.join(FIG_DIR, f"{name}.png"))

    print("Correction generation and visualization complete.")
    print(f"Image save location: {FIG_DIR}")


if __name__ == "__main__":
    main()
