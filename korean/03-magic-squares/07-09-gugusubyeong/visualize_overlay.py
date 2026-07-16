#!/usr/bin/env python3
"""양도/음도 성분 격자의 라틴·궁 성질 추가 검증 + 겹침 시각화."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from analyze_overlay import yang, yin

def comp_grids(g):
    A = np.array([[p[0] for p in row] for row in g])
    B = np.array([[p[1] for p in row] for row in g])
    return A, B

YA, YB = comp_grids(yang)
NA, NB = comp_grids(yin)

def is_perm(v): return sorted(v) == list(range(1, 10))

print("== yang components: row/col Latin, block ==")
for name, G in (("YA", YA), ("YB", YB)):
    print(name, "rows all perm:", all(is_perm(r) for r in G),
          "cols all perm:", all(is_perm(G[:, c]) for c in range(9)),
          "blocks all perm:", all(is_perm(G[br:br+3, bc:bc+3].ravel()) for br in (0,3,6) for bc in (0,3,6)))
print("== yin components ==")
for name, G in (("NA", NA), ("NB", NB)):
    print(name, "rows all perm:", all(is_perm(r) for r in G),
          "cols all perm:", all(is_perm(G[:, c]) for c in range(9)),
          "blocks all perm:", all(is_perm(G[br:br+3, bc:bc+3].ravel()) for br in (0,3,6) for bc in (0,3,6)))

# --- 시각화 1: 셀 합 히트맵 (양도 vs 음도), 3x3 궁 구분선 ---
YS = YA + YB
NS = NA + NB
fig, axes = plt.subplots(1, 2, figsize=(13, 6.2))
for ax, M, title in zip(axes, (YS, NS), ("Yang (07): cell sums a+b", "Yin (08): cell sums c+d")):
    im = ax.imshow(M, cmap="viridis", vmin=2, vmax=18)
    for i in range(9):
        for j in range(9):
            ax.text(j, i, M[i, j], ha="center", va="center", fontsize=9,
                    color="white" if M[i, j] < 11 else "black")
    for k in (2.5, 5.5):
        ax.axhline(k, color="red", lw=2); ax.axvline(k, color="red", lw=2)
    bs = [int(M[br:br+3, bc:bc+3].sum()) for br in (0,3,6) for bc in (0,3,6)]
    ax.set_title(title, fontsize=12); ax.set_xlabel(f"rows/cols=90, block sums={bs}", fontsize=9)
    ax.set_xticks(range(9)); ax.set_yticks(range(9))
fig.colorbar(im, ax=axes, shrink=0.8)
fig.savefig("yang-yin-sums.png", dpi=150, bbox_inches="tight")
print("saved yang-yin-sums.png")

# --- 시각화 2: 겹침표 — 각 칸에 양도쌍/음도쌍 병기 ---
fig, ax = plt.subplots(figsize=(15, 15))
ax.set_xlim(0, 9); ax.set_ylim(0, 9)
for r in range(9):
    for c in range(9):
        a, b = yang[r][c]; d, e = yin[r][c]
        ax.text(c + 0.5, 8 - r + 0.62, f"({a},{b})", ha="center", va="center",
                fontsize=11, color="navy", fontweight="bold")
        ax.text(c + 0.5, 8 - r + 0.30, f"({d},{e})", ha="center", va="center",
                fontsize=11, color="darkred")
for k in range(10):
    lw = 2.5 if k % 3 == 0 else 0.5
    ax.axhline(k, color="black", lw=lw); ax.axvline(k, color="black", lw=lw)
ax.set_xticks([]); ax.set_yticks([])
ax.set_title("Overlay: yang pair (navy) vs yin pair (dark red) per cell\n"
             "fixed point (5,5) at center; permutation cycles on 81 pairs: 1,2,6,8,8,8,8,9,10,21",
             fontsize=12)
fig.savefig("yang-yin-overlay.png", dpi=150, bbox_inches="tight")
print("saved yang-yin-overlay.png")
