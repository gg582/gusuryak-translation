#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ojagakdeuk (五子各得 / Cheonsu-yong-odo) — petal (cross-palace) point-symmetry visualization

Both layouts split into one center cell and four surrounding palaces (petals) of five numbers.
- Layout 1 (21 of 1–24): center 5, every petal sums to 65 (4 × 65 + 5 = 265)
- Layout 2 (1–21): center 15, every petal sums to 54 (4 × 54 + 15 = 231)
  Source: 去中宮十五 外合得二百一十六 應乾之策 每宮各得五十四 爲六九之數
Equal petal sums make opposite petals point-symmetric (180°) and the petal pattern
invariant under 90° rotation. Layout 2 also has finer point-symmetric partial sums
in the upper/lower petals: 12 + 5 = 16 + 1 = 17 and 17 + 18 + 2 = 21 + 10 + 6 = 37.
Left-right mirror balance (L 86 = R 86) holds only in Layout 1 (Layout 2: 81 vs 93).

Outputs: 09_flower_point_symmetry_2.png, 10_symmetry_comparison.png

---- (Korean original docstring follows) ----
五子各得 (오자각득 / 천수용오도) — 꽃잎(십자 궁) 점대칭 시각화

두 배치 모두 중심 1칸과, 그 둘레의 상·좌·우·하 네 궁(꽃잎, 각 5수)으로 나뉜다.

- 배치 1 (1~24 중 21수): 중심 5, 네 꽃잎의 합이 모두 65  (4 × 65 + 5 = 265)
- 배치 2 (1~21):        중심 15, 네 꽃잎의 합이 모두 54 (4 × 54 + 15 = 231)
  원문 「去中宮十五 外合得二百一十六 應乾之策 每宮各得五十四 爲六九之數」

네 꽃잎의 부분합이 모두 같으므로, 중심을 기준으로 마주 보는 꽃잎(상↔하, 좌↔우)의
부분합이 점대칭(180° 회전)으로 일치하고, 나아가 90° 회전에도 부분합이 불변인 4엽 꽃
구조가 된다. 배치 2는 여기에 더해 상·하 꽃잎 안에서도
  꼭짓점+중간점: 12 + 5 = 16 + 1 = 17,  양 날개+안쪽: 17 + 18 + 2 = 21 + 10 + 6 = 37
의 세부 점대칭 부분합이 성립한다.

반면 좌우 거울대칭(좌 86 = 우 86)은 배치 1에만 있다(배치 2는 좌 81 ≠ 우 93).

생성 파일:
- 09_flower_point_symmetry_2.png : 배치 2의 꽃잎 점대칭 + 부분합 로즈
- 10_symmetry_comparison.png     : 배치 1(거울대칭) vs 배치 2(점대칭 꽃) 대칭성 비교
"""

import math

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon

LANG = "en"

fm._load_fontmanager(try_read_cache=False)
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Noto Sans CJK KR", "Noto Sans CJK JP", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# ============================================================
# 1. 데이터
# ============================================================

# 기하 슬롯(두 배치 공통): 중심 C와 네 꽃잎. 꽃잎 슬롯 순서는
# [꼭짓점, 날개1, 날개2, 중간점, 안쪽점] 이며, 상↔하·좌↔우의 같은 순서 슬롯이
# 중심에 대해 (근사) 점대칭 위치에 놓인다.
CENTER_XY = (0.0, 2.0)
SLOTS = {
    "up":    [(0.0, 6.0), (-1.5, 5.0), (1.5, 5.0), (0.0, 4.2), (0.0, 3.3)],
    "down":  [(0.0, -1.7), (1.8, -0.4), (-1.8, -0.4), (0.0, -0.4), (0.0, 0.8)],
    "left":  [(-4.2, 2.0), (-2.8, 3.3), (-2.8, 0.8), (-2.8, 2.0), (-1.4, 2.0)],
    "right": [(4.2, 2.0), (2.8, 0.8), (2.8, 3.3), (2.8, 2.0), (1.4, 2.0)],
}

LAYOUTS = {
    1: {
        "center": 5,
        "up": [19, 12, 8, 6, 20],
        "down": [2, 13, 9, 17, 24],
        "left": [21, 4, 16, 23, 1],
        "right": [18, 11, 7, 14, 15],
        "total": 265,
    },
    2: {
        "center": 15,
        "up": [12, 17, 18, 5, 2],
        "down": [16, 21, 10, 1, 6],
        "left": [7, 13, 11, 3, 20],
        "right": [8, 14, 19, 4, 9],
        "total": 231,
    },
}

TXT = {
    "ko": {
        "petal": {"up": "상궁", "down": "하궁", "left": "좌궁", "right": "우궁"},
        "center": "중궁",
        "fig09_title": "五子各得 (천수용오도) 배치 2 — 15를 중심으로 한 꽃잎 점대칭",
        "fig09_left": "네 꽃잎(궁)의 부분합 = 54, 마주 보는 꽃잎끼리 점대칭",
        "fig09_right": "부분합 로즈: 90°마다 같은 꽃잎",
        "sub": "상·하 꽃잎 안의 세부 점대칭 부분합\n"
               "꼭짓점+중간점:  12 + 5 = 16 + 1 = 17\n"
               "날개+안쪽:  17 + 18 + 2 = 21 + 10 + 6 = 37",
        "check2": "4 × 54 + 15 = 231\n去中宮十五 外合得二百一十六 (乾之策 216)\n每宮各得五十四 (六九 = 54)",
        "fig10_title": "천수용오도 대칭성 비교 — 배치 1 vs 배치 2",
        "l1": "배치 1 (1~24 중 21수, 중심 5)",
        "l2": "배치 2 (1~21, 중심 15)",
        "mirror_ok": "좌우 거울대칭  좌 {L} = 우 {R}  ✓",
        "mirror_ng": "좌우 거울대칭  좌 {L} ≠ 우 {R}",
        "flower": "꽃잎 점대칭  4 × {S} + {C} = {T}  ✓",
        "pair": "{a} ↔ {b}\n{s} = {s}",
        "legend_pair_ud": "상↔하 점대칭 쌍",
        "legend_pair_lr": "좌↔우 점대칭 쌍",
        "rose_c": "중궁\n{C}",
    },
    "en": {
        "petal": {"up": "Upper", "down": "Lower", "left": "Left", "right": "Right"},
        "center": "Center",
        "fig09_title": "Ojagakdeuk (Cheonsu-yong-odo) Layout 2 — petal point symmetry about 15",
        "fig09_left": "Each of the four petals (palaces) sums to 54; opposite petals are point-symmetric",
        "fig09_right": "Partial-sum rose: identical petal every 90°",
        "sub": "Finer point-symmetric partial sums inside the upper/lower petals\n"
               "tip + middle:  12 + 5 = 16 + 1 = 17\n"
               "wings + inner:  17 + 18 + 2 = 21 + 10 + 6 = 37",
        "check2": "4 × 54 + 15 = 231\n去中宮十五 外合得二百一十六 (Qian tally 216)\n每宮各得五十四 (six-nine = 54)",
        "fig10_title": "Cheonsu-yong-odo symmetry comparison — Layout 1 vs Layout 2",
        "l1": "Layout 1 (21 of 1–24, center 5)",
        "l2": "Layout 2 (1–21, center 15)",
        "mirror_ok": "Left-right mirror  L {L} = R {R}  ✓",
        "mirror_ng": "Left-right mirror  L {L} ≠ R {R}",
        "flower": "Petal point symmetry  4 × {S} + {C} = {T}  ✓",
        "pair": "{a} ↔ {b}\n{s} = {s}",
        "legend_pair_ud": "upper↔lower point pair",
        "legend_pair_lr": "left↔right point pair",
        "rose_c": "Center\n{C}",
    },
}[LANG]

RESIDUE_STYLE = {
    1: ("#CFE2F5", "#4488CC"),  # 수
    2: ("#F4D0D0", "#CC4444"),  # 화
    3: ("#D4ECD4", "#44AA44"),  # 목
    4: ("#E8E8E8", "#888888"),  # 금
    0: ("#F6E5A3", "#CC9944"),  # 토
}
PAIR_COLOR = {"up": "#5B8DEF", "down": "#5B8DEF", "left": "#E8893B", "right": "#E8893B"}
OPPOSITE = {"up": "down", "down": "up", "left": "right", "right": "left"}


def positions(n: int) -> dict[int, tuple[float, float]]:
    lay = LAYOUTS[n]
    pos = {lay["center"]: CENTER_XY}
    for k, slots in SLOTS.items():
        for v, xy in zip(lay[k], slots):
            pos[v] = xy
    return pos


def validate() -> None:
    for n, lay in LAYOUTS.items():
        vals = [lay["center"]] + [v for k in SLOTS for v in lay[k]]
        assert len(set(vals)) == 21 and sum(vals) == lay["total"], n
        sums = {k: sum(lay[k]) for k in SLOTS}
        assert len(set(sums.values())) == 1, (n, sums)
    l2 = LAYOUTS[2]
    assert l2["up"][0] + l2["up"][3] == l2["down"][0] + l2["down"][3] == 17
    assert sum(l2["up"][i] for i in (1, 2, 4)) == sum(l2["down"][i] for i in (1, 2, 4)) == 37
    assert set(range(1, 22)) == set(positions(2))
    assert set(range(1, 25)) - {3, 10, 22} == set(positions(1))


def lr_sums(n: int) -> tuple[int, int]:
    pos = positions(n)
    left = sum(v for v, (x, _) in pos.items() if x < -0.5)
    right = sum(v for v, (x, _) in pos.items() if x > 0.5)
    return left, right


# ============================================================
# 2. 그리기 도구
# ============================================================


def petal_polygon(slots, pad=0.55, width_pad=0.42, n=80):
    """중심에서 바깥으로 뻗은 꽃잎(잎새) 모양 다각형."""
    cx, cy = CENTER_XY
    pts = np.array(slots)
    centroid = pts.mean(axis=0)
    u = centroid - np.array([cx, cy])
    u = u / np.linalg.norm(u)
    v = np.array([-u[1], u[0]])
    rel = pts - np.array([cx, cy])
    pu, pv = rel @ u, rel @ v
    u0, u1 = pu.min() - pad, pu.max() + pad
    w = np.abs(pv).max() + width_pad
    s = np.linspace(0, 1, n)
    half = w * np.sin(np.pi * s ** 0.6) ** 0.8
    along = u0 + (u1 - u0) * s
    upper = [(cx + a * u[0] + h * v[0], cy + a * u[1] + h * v[1]) for a, h in zip(along, half)]
    lower = [(cx + a * u[0] - h * v[0], cy + a * u[1] - h * v[1]) for a, h in zip(along[::-1], half[::-1])]
    tip = (cx + (u1 + 0.35) * u[0], cy + (u1 + 0.35) * u[1])
    return upper + lower, tip, centroid


def draw_nodes(ax, n, radius=0.32, fs=10):
    pos = positions(n)
    center = LAYOUTS[n]["center"]
    for v, (x, y) in pos.items():
        face, edge = RESIDUE_STYLE[v % 5]
        r = radius * (1.35 if v == center else 1.0)
        ax.add_patch(Circle((x, y), r, facecolor=face, edgecolor=edge, linewidth=2.4, zorder=4))
        ax.text(x, y, str(v), ha="center", va="center", fontsize=fs + (2 if v == center else 0),
                fontweight="bold", zorder=5)


def draw_flower(ax, n, show_pairs=True, label_size=11):
    lay = LAYOUTS[n]
    centroids = {}
    for k, slots in SLOTS.items():
        poly, tip, cen = petal_polygon(slots)
        centroids[k] = cen
        col = PAIR_COLOR[k]
        ax.add_patch(Polygon(poly, closed=True, facecolor=col, alpha=0.16, edgecolor=col, linewidth=2.0, zorder=1))
        ha = {"up": "center", "down": "center", "left": "right", "right": "left"}[k]
        va = {"up": "bottom", "down": "top", "left": "center", "right": "center"}[k]
        ax.text(tip[0], tip[1], f"{TXT['petal'][k]}  Σ = {sum(lay[k])}", ha=ha, va=va,
                fontsize=label_size, fontweight="bold", color=col, zorder=6,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor=col, alpha=0.9))
    if show_pairs:
        cx, cy = CENTER_XY
        for a, b, key in (("up", "down", "legend_pair_ud"), ("left", "right", "legend_pair_lr")):
            pa, pb = centroids[a], centroids[b]
            ax.plot([pa[0], pb[0]], [pa[1], pb[1]], ls=(0, (5, 4)), lw=1.6, color=PAIR_COLOR[a],
                    alpha=0.85, zorder=2, label=TXT[key])
        # 180° 회전 표시
        arc = np.linspace(math.radians(20), math.radians(200), 60)
        ax.plot(cx + 0.66 * np.cos(arc), cy + 0.66 * np.sin(arc), color="#444444", lw=1.2, zorder=3)
        ax.annotate("", xy=(cx + 0.66 * math.cos(arc[-1]), cy + 0.66 * math.sin(arc[-1])),
                    xytext=(cx + 0.66 * math.cos(arc[-4]), cy + 0.66 * math.sin(arc[-4])),
                    arrowprops=dict(arrowstyle="-|>", color="#444444", lw=1.2), zorder=3)
        ax.text(cx + 0.5, cy + 0.62, "180°", fontsize=9, color="#444444", zorder=6)
    return centroids


def frame(ax, ymin=-3.0):
    ax.set_xlim(-6.2, 6.2)
    ax.set_ylim(ymin, 7.4)
    ax.set_aspect("equal")
    ax.axis("off")


def save(fig, name):
    fig.savefig(name, dpi=200, bbox_inches="tight", facecolor="white")
    print(f"[saved] {name}")


# ============================================================
# 3. 그림 09 — 배치 2 꽃잎 점대칭 + 부분합 로즈
# ============================================================


def figure_09():
    lay = LAYOUTS[2]
    fig = plt.figure(figsize=(19, 9.5))
    ax = fig.add_axes([0.0, 0.0, 0.58, 0.9])
    draw_flower(ax, 2)
    draw_nodes(ax, 2)
    # 상·하 꽃잎 세부 점대칭: 꼭짓점+중간점 쌍을 실선으로 표시
    pos = positions(2)
    for a, b in ((12, 16), (5, 1)):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        ax.plot([x1 + 0.05, x2 + 0.05], [y1, y2], color="#7A4FD0", lw=1.0, alpha=0.6, zorder=2)
    ax.text(-6.1, -3.95, TXT["sub"], fontsize=10.5, va="bottom", ha="left", color="#4A2F8F",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#F4EFFF", edgecolor="#7A4FD0"))
    ax.legend(loc="upper left", fontsize=10, framealpha=0.9)
    frame(ax, ymin=-4.0)
    ax.set_title(TXT["fig09_left"], fontsize=13)

    # 부분합 로즈
    axr = fig.add_axes([0.6, 0.12, 0.38, 0.72], projection="polar")
    order = ["right", "up", "left", "down"]
    theta = np.radians([0, 90, 180, 270])
    vals = [sum(lay[k]) for k in order]
    axr.bar(theta, vals, width=np.radians(62), bottom=lay["center"],
            color=[PAIR_COLOR[k] for k in order], alpha=0.55, edgecolor="white", linewidth=2)
    for t, k, v in zip(theta, order, vals):
        axr.text(t, lay["center"] + v * 0.62, f"{TXT['petal'][k]}\n{v}", ha="center", va="center",
                 fontsize=12, fontweight="bold", color="white")
    axr.bar([0], [lay["center"]], width=2 * np.pi, bottom=0, color="#F6E5A3", edgecolor="none")
    axr.text(0, 0, TXT["rose_c"].format(C=lay["center"]), ha="center", va="center", fontsize=11, fontweight="bold")
    axr.set_ylim(0, lay["center"] + 60)
    axr.set_yticks([])
    axr.set_xticks(theta)
    axr.set_xticklabels(["0°", "90°", "180°", "270°"], fontsize=9, color="#666666")
    axr.spines["polar"].set_visible(False)
    axr.grid(False)
    axr.set_title(TXT["fig09_right"], fontsize=13, pad=14)
    fig.text(0.79, 0.04, TXT["check2"], ha="center", va="bottom", fontsize=11,
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFF8E1", edgecolor="#CC9944"))
    fig.suptitle(TXT["fig09_title"], fontsize=17, fontweight="bold", y=0.99)
    save(fig, "09_flower_point_symmetry_2.png")
    plt.close(fig)


# ============================================================
# 4. 그림 10 — 배치 1 vs 배치 2 대칭성 비교
# ============================================================


def figure_10():
    fig, axes = plt.subplots(1, 2, figsize=(20, 10))
    for ax, n, title in ((axes[0], 1, TXT["l1"]), (axes[1], 2, TXT["l2"])):
        lay = LAYOUTS[n]
        draw_flower(ax, n, show_pairs=True, label_size=10)
        draw_nodes(ax, n, fs=9)
        L, R = lr_sums(n)
        ok = L == R
        ax.axvline(0, ymin=0.13, ymax=0.97, color="#2E7D32" if ok else "#C62828", lw=1.4, ls=":", zorder=0)
        mirror = (TXT["mirror_ok"] if ok else TXT["mirror_ng"]).format(L=L, R=R)
        flower = TXT["flower"].format(S=sum(lay["up"]), C=lay["center"], T=lay["total"])
        ax.text(0, -4.15, mirror, ha="center", va="bottom", fontsize=12, fontweight="bold",
                color="#2E7D32" if ok else "#C62828")
        ax.text(0, -3.55, flower, ha="center", va="bottom", fontsize=12, fontweight="bold", color="#1F4E9E")
        frame(ax, ymin=-4.3)
        ax.set_title(title, fontsize=14, fontweight="bold")
    axes[0].legend(loc="upper left", fontsize=10, framealpha=0.9)
    fig.suptitle(TXT["fig10_title"], fontsize=18, fontweight="bold", y=0.98)
    save(fig, "10_symmetry_comparison.png")
    plt.close(fig)


if __name__ == "__main__":
    validate()
    for n in (1, 2):
        lay = LAYOUTS[n]
        print(f"layout {n}: center {lay['center']}, petals",
              {k: sum(lay[k]) for k in SLOTS}, "L/R", lr_sums(n))
    figure_09()
    figure_10()
