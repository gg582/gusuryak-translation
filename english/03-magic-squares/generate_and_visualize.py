#!/usr/bin/env python3
"""
Valid magic square correction generator and visualization script
(with mathematical symmetry and internal rules recovery model).
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# Korean font setting (kept for proper rendering of any CJK text)
font_path = "/usr/share/fonts/truetype/nanum/NanumSquare_acR.ttf"
if os.path.exists(font_path):
    font_manager.fontManager.addfont(font_path)
    rc('font', family=font_manager.FontProperties(fname=font_path).get_name())
plt.rcParams['axes.unicode_minus'] = False

OUT_DIR = "/home/yjlee/gusuryak-translation/english/03-magic-squares"
FIG_DIR = os.path.join(OUT_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# ---------- Raw Data ----------

ORIGINALS = {
    "yukyukdo_example_1": np.array([
        [13, 22, 18, 27, 11, 20],
        [31,  4, 36,  9, 29,  2],
        [12, 21, 14, 23, 16, 25],
        [30,  3,  5, 32, 34,  7],
        [17, 26, 10, 19, 15, 24],
        [ 8, 35, 28,  1,  6, 33],
    ]),
    "yukyukdo_example_2": np.array([
        [ 4, 13, 36, 27, 29,  2],
        [22, 31, 18,  9, 11, 20],
        [ 3, 21, 23, 32, 25,  7],
        [30, 12,  5, 14, 16, 34],
        [17, 26, 19, 28,  6, 15],
        [35,  8, 10,  1, 24, 33],
    ]),
    "gusudo_example_1": np.array([
        [31, 76, 13, 36, 81, 18, 29, 74, 11],
        [22, 40, 58, 27, 45, 63, 20, 38, 56],
        [67,  4, 49, 72,  9, 54, 65,  2, 47],
        [30, 75, 12, 32, 77, 14, 34, 79, 16],
        [21, 39, 57, 23, 41, 59, 25, 43, 61],
        [66,  3, 48, 68,  5, 50, 70,  7, 52],
        [35, 80, 17, 28, 73, 10, 33, 78, 15],
        [26, 44, 62, 19, 37, 55, 24, 42, 60],
        [71,  8, 53, 64,  1, 46, 69,  6, 51],
    ]),
    "gusudo_example_2": np.array([
        [50, 18, 55, 70,  5, 48,  3, 76, 44],
        [66, 31, 26, 29, 81, 13, 52, 11, 60],
        [ 7, 74, 42, 24, 37, 62, 68, 36, 19],
        [54, 67,  2, 65, 25, 33, 28, 23, 72],
        [59, 21, 43,  9, 41, 73, 15, 61, 47],
        [10, 35, 78, 49, 57, 17, 80, 39,  4],
        [79,  6, 38, 20, 69, 34, 32, 64, 27],
        [30, 71, 22, 45,  1, 77, 16, 51, 56],
        [14, 46, 63, 58, 53, 12, 75,  8, 40],
    ]),
    "baekjasaengseong_sunsu_original": np.array([
        [90, 89, 78, 67, 56, 45, 34, 23, 12,  1],
        [86, 70, 69, 58, 97,  4, 43, 32, 21, 15],
        [77, 66, 50, 99, 88, 13,  2, 41, 35, 24],
        [68, 57, 96, 80, 79, 22, 11,  5, 44, 33],
        [59, 98, 87, 76, 60, 31, 25, 14,  3, 42],
        [42,  3, 14, 25, 31, 60, 76, 87, 98, 59],
        [33, 44,  5, 11, 22, 79, 80, 96, 57, 68],
        [24, 35, 41,  2, 13, 88, 99, 50, 66, 77],
        [15, 21, 32, 43,  4, 97, 58, 69, 70, 86],
        [ 1, 12, 23, 34, 45, 56, 67, 78, 89, 90]
    ]),
    "baekjasaengseong_gyosu_original": np.array([
        [10, 19, 28, 37, 46, 55, 64, 73, 82, 91],
        [16, 20, 39, 48,  7, 94, 53, 62, 71, 85],
        [27, 36, 40,  9, 18, 83, 92, 51, 65, 74],
        [38, 47,  6, 10, 29, 72, 81, 95, 54, 63],
        [59,  8, 17, 26, 30, 61, 75, 84, 93, 52],
        [42, 93, 84, 75, 61, 30, 26, 17,  8, 49],
        [63, 54, 95, 81, 72, 29, 10,  6, 47, 38],
        [74, 65, 51, 92, 83, 18,  9, 40, 36, 27],
        [85, 71, 62, 53, 94,  7, 48, 39, 20, 16],
        [91, 82, 73, 64, 55, 46, 37, 28, 19, 10]
    ]),
    "baekjayin_yang_jamo_chakjong_original": np.array([
        [100, 89, 78, 67, 56, 45, 34, 23, 12,  1],
        [ 29, 28, 47, 36, 10, 91, 65, 54, 73, 72],
        [ 48, 17, 26, 40, 39, 62, 61, 75, 84, 53],
        [ 27, 46, 50,  9, 88, 13, 92, 51, 55, 74],
        [ 76, 80, 59, 98, 87, 14,  3, 32, 21, 25],
        [ 15, 31, 42, 43,  4, 97, 58, 69, 70, 86],
        [ 24, 35, 41,  2, 83, 18, 99, 60, 66, 77],
        [ 93, 94, 85, 71, 52, 49, 30, 16,  7,  8],
        [ 82, 63, 64, 95, 81, 20,  6, 37, 38, 19],
        [ 11, 22, 33, 44,  5, 96, 57, 68, 79, 90]
    ]),
    "baekjado_original": np.array([
        [ 1, 20, 21, 40, 41, 60, 61, 80, 81, 100],
        [99, 82, 79, 62, 59, 42, 39, 22, 19,  2],
        [ 3, 18, 23, 38, 43, 58, 63, 78, 83, 98],
        [97, 84, 77, 64, 57, 44, 37, 24, 17,  4],
        [ 5, 86, 75, 66, 55, 46, 35, 26, 15, 96],
        [95, 16, 25, 36, 45, 56, 65, 76, 85,  6],
        [14,  7, 34, 27, 54, 47, 74, 67, 94, 87],
        [88, 93, 68, 73, 48, 53, 28, 33,  8, 13],
        [12,  9, 32, 29, 52, 49, 72, 69, 92, 89],
        [91, 90, 71, 70, 51, 50, 31, 30, 11, 10]
    ])
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
    row_sums = m.sum(axis=1)
    col_sums = m.sum(axis=0)
    diag_sum1 = np.trace(m)
    diag_sum2 = np.trace(np.fliplr(m))
    
    is_semi = np.all(row_sums == row_sums[0]) and np.all(col_sums == col_sums[0])
    is_magic = is_semi and (diag_sum1 == row_sums[0]) and (diag_sum2 == row_sums[0])
    
    lines.append(f"- Order: {n}×{n}")
    lines.append(f"- Row sums: {row_sums.tolist()}")
    lines.append(f"- Column sums: {col_sums.tolist()}")
    lines.append(f"- Diagonal sums: {[diag_sum1, diag_sum2]}")
    lines.append(f"- Normal set (1~{n*n}): {'Yes' if is_normal_set(m) else 'No'}")
    lines.append(f"- Semi-magic: {'Yes' if is_semi else 'No'}")
    lines.append(f"- Magic square: {'Yes' if is_magic else 'No'}")
    lines.append("")
    return "\n".join(lines)

def generate_corrected_10x10():
    """Generate corrected versions based on the original grid's point symmetry and combinatorial rules."""
    # 1. Baekjasaengseong-sunsu
    m04 = ORIGINALS["baekjasaengseong_sunsu_original"].copy()
    
    # 3. Baekjayin-yang-jamo-chakjong correction: Restore semi-magic structure and 1-100 permutation with minimal correction (5 cells corrected)
    m06 = ORIGINALS["baekjayin_yang_jamo_chakjong_original"].copy()
    m06[1, 2] = 54
    m06[1, 7] = 47
    m06[4, 2] = 42
    m06[4, 7] = 59
    m06[5, 2] = 32
    
    # 4. Baekjado correction: Correct errors in the 8 corner cells to restore semi-magic structure and tens-place symmetry
    m07 = ORIGINALS["baekjado_original"].copy()
    m07[4, 0] = 96
    m07[4, 9] = 5
    m07[5, 0] = 6
    m07[5, 9] = 95
    m07[6, 0] = 87
    m07[6, 9] = 14
    m07[7, 0] = 13
    m07[7, 9] = 88
    
    corrected = {
        "baekjasaengseong_sunsu": m04,
        "baekjayin_yang_jamo_chakjong_correction": m06,
        "baekjado_correction": m07,
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

    # Save corrected.md files in their respective folders
    folder_map = {
        "baekjasaengseong_sunsu": "04-baekjasaengseong-sunsu",
        "baekjayin_yang_jamo_chakjong_correction": "06-baekjayin-yang-jamo-chakjong",
        "baekjado_correction": "10-baekjado",
    }

    for name, folder in folder_map.items():
        m = corrected[name]
        md = matrix_to_markdown(m, name.replace("_", " "))
        path = os.path.join(OUT_DIR, folder, "corrected.md")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# Valid Magic Square Correction\n\n")
            f.write(md)

    # Visualize original and corrected magic squares
    for name, m in ORIGINALS.items():
        if name.startswith("yukyukdo") or name.startswith("gusudo"):
            visualize(m, f"Original: {name}", os.path.join(FIG_DIR, f"{name}.png"))

    for name, m in corrected.items():
        visualize(m, name.replace("_", " "), os.path.join(FIG_DIR, f"{name}.png"))

    print("Correction generation and visualization complete.")
    print(f"Images saved at: {FIG_DIR}")

if __name__ == "__main__":
    main()
