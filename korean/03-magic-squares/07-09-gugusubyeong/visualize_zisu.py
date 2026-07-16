#!/usr/bin/env python3
"""09 구구자수변궁양도/음도 시각화: 값 히트맵 + 낙서⊗낙서 구조도."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from analyze_zisu import yang, yin, L

YA = np.array(yang)
YI = np.array(yin)

fig, axes = plt.subplots(1, 2, figsize=(14, 6.6))
for ax, M, title, note in zip(
    axes, (YA, YI),
    ("Yang (09): a×b = L(palace) × L(cell-in-palace)",
     "Yin (09): anti-diagonal symmetric"),
    ("all rows/cols/diagonals = 225; block constants 15×Lo Shu",
     "all rows/cols = 225; diagonals 165 / 285; anti-diagonal = 1²..9²"),
):
    im = ax.imshow(M, cmap="viridis", vmin=1, vmax=81)
    for i in range(9):
        for j in range(9):
            ax.text(j, i, M[i, j], ha="center", va="center", fontsize=8,
                    color="white" if M[i, j] < 45 else "black")
    for k in (2.5, 5.5):
        ax.axhline(k, color="red", lw=2); ax.axvline(k, color="red", lw=2)
    bs = [int(M[br:br+3, bc:bc+3].sum()) for br in (0, 3, 6) for bc in (0, 3, 6)]
    ax.set_title(title, fontsize=11)
    ax.set_xlabel(f"{note}\nblock sums={bs}", fontsize=8)
    ax.set_xticks(range(9)); ax.set_yticks(range(9))
fig.colorbar(im, ax=axes, shrink=0.8)
fig.savefig("zisu-yang-yin.png", dpi=150, bbox_inches="tight")
print("saved zisu-yang-yin.png")

# --- 낙서⊗낙서 구조도: 양도 각 칸을 (궁 낙서값, 궁내 낙서값) 쌍으로 표기 ---
fig, ax = plt.subplots(figsize=(13, 13))
ax.set_xlim(0, 9); ax.set_ylim(0, 9)
for r in range(9):
    for c in range(9):
        a, b = L[r // 3][c // 3], L[r % 3][c % 3]
        ax.text(c + 0.5, 8 - r + 0.62, f"({a},{b})", ha="center", va="center",
                fontsize=11, color="navy", fontweight="bold")
        ax.text(c + 0.5, 8 - r + 0.28, f"{a*b}", ha="center", va="center",
                fontsize=11, color="darkred")
for k in range(10):
    lw = 2.5 if k % 3 == 0 else 0.5
    ax.axhline(k, color="black", lw=lw); ax.axvline(k, color="black", lw=lw)
ax.set_xticks([]); ax.set_yticks([])
ax.set_title("Yang (09) = Lo Shu ⊗ Lo Shu: pair (palace value, cell value) in navy, product in dark red\n"
             "each 3×3 palace is k×Lo Shu (k = palace value); palace constants form 15×Lo Shu",
             fontsize=12)
fig.savefig("zisu-yang-kronecker.png", dpi=150, bbox_inches="tight")
print("saved zisu-yang-kronecker.png")
