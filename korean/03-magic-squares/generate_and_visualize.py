#!/usr/bin/env python3
"""
정상 마방진 교정본 생성 및 시각화 스크립트

- 육육도: 이미 정상 마방진. associated는 n≡2 (mod 4)일 때 불가능하므로 교정본 없음.
- 구수도: 이미 정상 마방진.
- 10×10 방진들: magic_square 패키지로 정상 10×10 마방진 교정본 생성.
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 한글 폰트 설정
font_path = "/usr/share/fonts/truetype/nanum/NanumSquare_acR.ttf"
font_manager.fontManager.addfont(font_path)
rc('font', family=font_manager.FontProperties(fname=font_path).get_name())
plt.rcParams['axes.unicode_minus'] = False

# virtual environment의 magic_square 사용
import magic_square as ms

OUT_DIR = "/home/yjlee/gusuryak-translation/korean/03-magic-squares"
FIG_DIR = os.path.join(OUT_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# ---------- 원본 데이터 ----------

ORIGINALS = {
    "육육도_예시1": np.array([
        [13, 22, 18, 27, 11, 20],
        [31, 4, 36, 9, 29, 2],
        [12, 21, 14, 23, 16, 25],
        [30, 3, 5, 32, 34, 7],
        [17, 26, 10, 19, 15, 24],
        [8, 35, 28, 1, 6, 33],
    ]),
    "육육도_예시2": np.array([
        [4, 13, 36, 27, 29, 2],
        [22, 31, 18, 9, 11, 20],
        [3, 21, 23, 32, 25, 7],
        [30, 12, 5, 14, 16, 34],
        [17, 26, 19, 28, 6, 15],
        [35, 8, 10, 1, 24, 33],
    ]),
    "구수도_예시1": np.array([
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
    "구수도_예시2": np.array([
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
    lines.append(f"- 차수: {n}×{n}")
    lines.append(f"- 마방진 상수: {mc}")
    lines.append(f"- 정상 수 집합(1~{n*n}): {'예' if is_normal_set(m) else '아니오'}")
    lines.append(f"- Magic square: {'예' if ms.ismagic(m) else '아니오'}")
    lines.append(f"- Associated: {'예' if is_associated(m) else '아니오'}")
    lines.append("")
    return "\n".join(lines)


def generate_corrected_10x10():
    """서로 다른 4개의 10×10 정상 마방진 교정본 생성."""
    base = ms.magic(10)
    corrected = {
        "백자자수음양착종도_교정본": base.copy(),
        "백자생성순수도_교정본": np.rot90(base, 1).copy(),
        "백자생성교수도_교정본": np.fliplr(base).copy(),
        "백자음양자모착종도_교정본": np.flipud(base).copy(),
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

    # 검증
    for name, m in corrected.items():
        assert is_normal_set(m), f"{name}: not normal set"
        assert ms.ismagic(m), f"{name}: not magic"
        print(f"{name}: normal={is_normal_set(m)}, magic={ms.ismagic(m)}, associated={is_associated(m)}")

    # 교정본 corrected.md 저장
    folder_map = {
        "백자자수음양착종도_교정본": "03-baekjajasuyin-yang-chakjong",
        "백자생성순수도_교정본": "04-baekjasaengseong-sunsu",
        "백자생성교수도_교정본": "05-baekjasaengseong-gyosu",
        "백자음양자모착종도_교정본": "06-baekjayin-yang-jamo-chakjong",
    }

    for name, folder in folder_map.items():
        m = corrected[name]
        md = matrix_to_markdown(m, name.replace("_", " "))
        path = os.path.join(OUT_DIR, folder, "corrected.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# 정상 마방진 교정본\n\n")
            f.write(md)

    # 시각화
    # 육육도: 원본만 (정상 마방진, associated는 불가능)
    for name, m in ORIGINALS.items():
        if name.startswith("육육도"):
            visualize(m, f"원본: {name}", os.path.join(FIG_DIR, f"{name}.png"))

    # 구수도: 원본만
    for name, m in ORIGINALS.items():
        if name.startswith("구수도"):
            visualize(m, f"원본: {name}", os.path.join(FIG_DIR, f"{name}.png"))

    # 10×10: 교정본만
    for name, m in corrected.items():
        visualize(m, name.replace("_", " "), os.path.join(FIG_DIR, f"{name}.png"))

    print("교정본 생성 및 시각화 완료.")
    print(f"이미지 저장 위치: {FIG_DIR}")


if __name__ == "__main__":
    main()
