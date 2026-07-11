#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
五子各得 (오자각득 / 천수용오도) — 현대 조합론·위치 분석

《구수략(九數略)》계열 도상 중 오자각득(五子各得) 혹은 천수용오도(天水用五圖)의
수 배치를 현대 수학 언어로 재해석.
분석 대상: 1~24 중 21개 수를 천수용오도 형태로 배치한 도상.

본 스크립트는 원본에 간선이 없음을 전제로, 위치·오행·조합론적 불변량만 분석한다.
"""

import os
from collections import Counter

import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

# ============================================================
# 0. 폰트 및 출력 설정
# ============================================================

fm._load_fontmanager(try_read_cache=False)
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK KR",
    "Noto Sans CJK JP",
    "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False

OUTPUT_DIR = "."
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_fig(name):
    path = f"{OUTPUT_DIR}/{name}"
    plt.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    print(f"[저장] {path}")


# ============================================================
# 1. 원본 데이터 구조화
# ============================================================

POSITIONS: dict[int, tuple[float, float]] = {
    19: (0.0, 6.0),
    12: (-1.5, 5.0),
    8:  (1.5, 5.0),
    6:  (0.0, 4.2),
    4:  (-2.8, 3.3),
    20: (0.0, 3.3),
    7:  (2.8, 3.3),
    21: (-4.2, 2.0),
    23: (-2.8, 2.0),
    1:  (-1.4, 2.0),
    5:  (0.0, 2.0),
    15: (1.4, 2.0),
    14: (2.8, 2.0),
    18: (4.2, 2.0),
    16: (-2.8, 0.8),
    24: (0.0, 0.8),
    11: (2.8, 0.8),
    9:  (-1.8, -0.4),
    17: (0.0, -0.4),
    13: (1.8, -0.4),
    2:  (0.0, -1.7),
}

GROUPS: dict[int, list[int]] = {
    1: [1, 6, 11, 16, 21],
    2: [2, 7, 12, 17],
    3: [8, 13, 18, 23],
    4: [4, 9, 14, 19, 24],
    0: [5, 15, 20],
}

RESIDUE_STYLE: dict[int, dict[str, str]] = {
    1: {"face": "#E0E0E0", "edge": "#333333", "name": "수", "en": "Water"},
    2: {"face": "#F4D0D0", "edge": "#B33B3B", "name": "화", "en": "Fire"},
    3: {"face": "#D4E4F8", "edge": "#3A6FAE", "name": "목", "en": "Wood"},
    4: {"face": "#E5E5E5", "edge": "#666666", "name": "금", "en": "Metal"},
    0: {"face": "#F6E5A3", "edge": "#C39A00", "name": "토", "en": "Earth"},
}

WUXING_COLOR = {
    "수": "#4488CC",
    "화": "#CC4444",
    "목": "#44AA44",
    "금": "#888888",
    "토": "#CC9944",
}


def wuxing_of(n: int) -> str:
    return RESIDUE_STYLE[n % 5]["name"]


def residue_1based(n: int) -> int:
    r = n % 5
    return 5 if r == 0 else r


# ============================================================
# 2. 조합론·위치 분석
# ============================================================


def validate() -> None:
    all_values = sorted(POSITIONS.keys())
    assert all_values == sorted(set(POSITIONS)), "중복 없는 21개 수"
    assert set(all_values) == set(range(1, 25)) - {3, 10, 22}, "1~24 중 3, 10, 22 제외"
    assert sum(all_values) == 265, "전체 합은 265"
    grouped = [n for nums in GROUPS.values() for n in nums]
    assert sorted(grouped) == all_values, "GROUPS가 전체 수를 정확히 분할"


validate()

print("=" * 60)
print("五子各得 (오자각득 / 천수용오도) 현대 조합론·위치 분석")
print("=" * 60)
print(f"노드 수: {len(POSITIONS)}")
print("원본에 간선이 없으므로 그래프 이론 지표(차수·betweenness·사이클·스펙트럼)는 분석하지 않음.")

print("\n오행별 수 합:")
for r in [1, 2, 3, 4, 5]:
    nodes = [n for n in POSITIONS if residue_1based(n) == r]
    wx = RESIDUE_STYLE[r % 5]["name"]
    print(f"  {wx}({r}): 합={sum(nodes)}, 수들={sorted(nodes)}")

print("\n오행별 위치 분포:")
for r in [1, 2, 3, 4, 0]:
    nums = GROUPS[r]
    wx = RESIDUE_STYLE[r]["name"]
    print(f"  {wx}: {len(nums)}개 - {sorted(nums)}")

# 수평 단(y좌표)별 집계
LEVELS: dict[float, list[int]] = {}
for n, (x, y) in POSITIONS.items():
    LEVELS.setdefault(round(y, 1), []).append(n)
LEVEL_ORDER = sorted(LEVELS.keys(), reverse=True)

# 좌/중/우 분할
LEFT_VALUES = [n for n, (x, _) in POSITIONS.items() if x < -0.5]
MID_VALUES = [n for n, (x, _) in POSITIONS.items() if -0.5 <= x <= 0.5]
RIGHT_VALUES = [n for n, (x, _) in POSITIONS.items() if x > 0.5]

print("\n수평 단별 합:")
for y in LEVEL_ORDER:
    nums = LEVELS[y]
    print(f"  y={y}: {sorted(nums)} 합={sum(nums)}")

print(f"\n좌/중/우 분할:")
print(f"  좌: {sorted(LEFT_VALUES)} 합={sum(LEFT_VALUES)}")
print(f"  중: {sorted(MID_VALUES)} 합={sum(MID_VALUES)}")
print(f"  우: {sorted(RIGHT_VALUES)} 합={sum(RIGHT_VALUES)}")

# ============================================================
# 3. 시각화
# ============================================================


def draw_nodes(ax, highlight_values=None, alpha_other=1.0, radius=0.32):
    """기본 노드 드로잉."""
    for value, (x, y) in POSITIONS.items():
        r = value % 5
        style = RESIDUE_STYLE[r]
        color = style["face"]
        edge = style["edge"]
        lw = 2.5
        if highlight_values is not None and value not in highlight_values:
            color = "#F0F0F0"
            edge = "#CCCCCC"
            lw = 1.2
        ax.add_patch(
            plt.Circle(
                (x, y),
                radius,
                facecolor=color,
                edgecolor=edge,
                linewidth=lw,
                zorder=2,
            )
        )
        text_color = "black"
        if highlight_values is not None and value not in highlight_values:
            text_color = "#AAAAAA"
        ax.text(
            x,
            y,
            str(value),
            ha="center",
            va="center",
            fontsize=10,
            fontweight="bold",
            color=text_color,
            zorder=3,
        )


# --- 01: 원본 구조 (간선 없음) ---
fig, ax = plt.subplots(figsize=(12, 12))
draw_nodes(ax)
ax.set_title(
    "五子各得 (오자각득 / 천수용오도) - 원본 배치\n"
    "21수 · mod 5 오행 분류 · 천수용오도 기하 구조",
    fontsize=16,
    fontweight="bold",
)
ax.set_xlim(-5.0, 5.0)
ax.set_ylim(-2.4, 6.8)
ax.set_aspect("equal")
ax.axis("off")
legend_elements = [
    mpatches.Patch(facecolor=WUXING_COLOR[wx], edgecolor="black", label=f"{wx}")
    for wx in ["수", "화", "목", "금", "토"]
]
ax.legend(handles=legend_elements, loc="lower right", fontsize=10, framealpha=0.9)
save_fig("01_original_graph.png")
plt.close()

# --- 02: 오행별 서브그룹 분해 (간선 없음) ---
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()

ax = axes[0]
draw_nodes(ax)
ax.set_title("전체 배치", fontsize=13, fontweight="bold")
ax.set_xlim(-5.0, 5.0)
ax.set_ylim(-2.4, 6.8)
ax.set_aspect("equal")
ax.axis("off")

for idx, wx in enumerate(["수", "화", "목", "금", "토"]):
    ax = axes[idx + 1]
    wx_nodes = [n for n in POSITIONS if wuxing_of(n) == wx]
    other_nodes = [n for n in POSITIONS if n not in wx_nodes]

    for n in other_nodes:
        x, y = POSITIONS[n]
        ax.add_patch(
            plt.Circle(
                (x, y),
                0.22,
                facecolor="#F0F0F0",
                edgecolor="#CCCCCC",
                linewidth=1,
                zorder=1,
            )
        )
        ax.text(x, y, str(n), ha="center", va="center", fontsize=8, color="#AAAAAA", zorder=2)

    for n in wx_nodes:
        x, y = POSITIONS[n]
        ax.add_patch(
            plt.Circle(
                (x, y),
                0.34,
                facecolor=WUXING_COLOR[wx],
                edgecolor="black",
                linewidth=2.5,
                zorder=2,
            )
        )
        ax.text(
            x,
            y,
            str(n),
            ha="center",
            va="center",
            fontsize=10,
            fontweight="bold",
            color="white" if wx in ["수", "목"] else "black",
            zorder=3,
        )

    ax.set_title(
        f"{wx} · 합 {sum(wx_nodes)}",
        fontsize=12,
        fontweight="bold",
        color=WUXING_COLOR[wx],
    )
    ax.set_xlim(-5.0, 5.0)
    ax.set_ylim(-2.4, 6.8)
    ax.set_aspect("equal")
    ax.axis("off")

plt.suptitle("오행(五行)별 서브그룹 분해", fontsize=16, fontweight="bold", y=1.02)
plt.tight_layout()
save_fig("02_wuxing_decomposition.png")
plt.close()

# --- 03: mod 5 잉여의 공간 분포 (히트맵) ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

ax = axes[0]
# x축: 좌표 열(반올림), y축: 수평 단
xs = sorted(set(round(x, 1) for x, _ in POSITIONS.values()))
ys = LEVEL_ORDER
# 잉여값을 격자에 매핑
grid = np.full((len(ys), len(xs)), np.nan)
for n, (x, y) in POSITIONS.items():
    r = residue_1based(n)
    i = ys.index(round(y, 1))
    j = xs.index(round(x, 1))
    grid[i, j] = r

im = ax.imshow(grid, cmap="tab10", vmin=1, vmax=5, aspect="auto")
ax.set_xticks(range(len(xs)))
ax.set_yticks(range(len(ys)))
ax.set_xticklabels([str(x) for x in xs], fontsize=9)
ax.set_yticklabels([f"y={y}" for y in ys], fontsize=9)
ax.set_title("mod 5 잉여 공간 분포", fontsize=13, fontweight="bold")
ax.set_xlabel("x좌표", fontsize=11)
ax.set_ylabel("y좌표", fontsize=11)

# 셀에 숫자 표시
for n, (x, y) in POSITIONS.items():
    i = ys.index(round(y, 1))
    j = xs.index(round(x, 1))
    ax.text(j, i, str(n), ha="center", va="center", fontsize=9, fontweight="bold",
            color="white" if n % 5 in [3, 0] else "black")

# 컬러바
from matplotlib.colors import BoundaryNorm
sm = plt.cm.ScalarMappable(cmap="tab10", norm=BoundaryNorm([0.5, 1.5, 2.5, 3.5, 4.5, 5.5], 5))
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, ticks=[1, 2, 3, 4, 5], shrink=0.8)
cbar.ax.set_yticklabels(["수", "화", "목", "금", "토"])

ax = axes[1]
# 각 오행의 x좌표 분포
for wx in ["수", "화", "목", "금", "토"]:
    nodes = [n for n in POSITIONS if wuxing_of(n) == wx]
    xvals = [POSITIONS[n][0] for n in nodes]
    yvals = [POSITIONS[n][1] for n in nodes]
    ax.scatter(xvals, yvals, c=WUXING_COLOR[wx], s=200, edgecolors="black", linewidths=1.5, label=wx, zorder=2)
    for n in nodes:
        ax.text(POSITIONS[n][0], POSITIONS[n][1], str(n), ha="center", va="center",
                fontsize=8, fontweight="bold", zorder=3)
ax.set_xlim(-5.0, 5.0)
ax.set_ylim(-2.4, 6.8)
ax.set_aspect("equal")
ax.axvline(x=0, color="gray", linestyle="--", linewidth=1, alpha=0.5)
ax.axhline(y=0, color="gray", linestyle="--", linewidth=1, alpha=0.5)
ax.set_title("오행별 좌표 분포", fontsize=13, fontweight="bold")
ax.legend(loc="lower right", fontsize=10)
ax.axis("off")

plt.tight_layout()
save_fig("03_spatial_distribution.png")
plt.close()

# --- 04: 대칭 분석 ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

ax = axes[0]
# 좌우 대칭: x 부호별 노드 표시
for n, (x, y) in POSITIONS.items():
    if x < -0.5:
        color = "#4488CC"
        label = "좌"
    elif x > 0.5:
        color = "#CC4444"
        label = "우"
    else:
        color = "#44AA44"
        label = "중"
    ax.add_patch(
        plt.Circle(
            (x, y),
            0.32,
            facecolor=color,
            edgecolor="black",
            linewidth=2,
            zorder=2,
        )
    )
    ax.text(x, y, str(n), ha="center", va="center", fontsize=9, fontweight="bold", zorder=3)

# 범례
legend_elements = [
    mpatches.Patch(facecolor="#4488CC", edgecolor="black", label=f"좌 (합 {sum(LEFT_VALUES)})"),
    mpatches.Patch(facecolor="#44AA44", edgecolor="black", label=f"중 (합 {sum(MID_VALUES)})"),
    mpatches.Patch(facecolor="#CC4444", edgecolor="black", label=f"우 (합 {sum(RIGHT_VALUES)})"),
]
ax.legend(handles=legend_elements, loc="lower right", fontsize=10)
ax.set_xlim(-5.0, 5.0)
ax.set_ylim(-2.4, 6.8)
ax.set_aspect("equal")
ax.axvline(x=0, color="gray", linestyle="--", linewidth=1.5, alpha=0.5)
ax.set_title("좌·중·우 대칭 분포", fontsize=13, fontweight="bold")
ax.axis("off")

ax = axes[1]
# 수평 단별 합
level_sums = [sum(LEVELS[y]) for y in LEVEL_ORDER]
level_names = [f"y={y}" for y in LEVEL_ORDER]
colors_level = ["#CC4444", "#4488CC", "#44AA44", "#CC9944", "#888888", "#AA44AA", "#44AAAA", "#CC8844"]
ax.barh(level_names, level_sums, color=colors_level[:len(level_names)], edgecolor="black", linewidth=1.5)
ax.set_title("수평 단별 합", fontsize=13, fontweight="bold")
ax.set_xlabel("Sum", fontsize=11)
for i, val in enumerate(level_sums):
    ax.text(val + 1, i, str(val), va="center", fontsize=11, fontweight="bold")

plt.tight_layout()
save_fig("04_symmetry_analysis.png")
plt.close()

# --- 05: 합 불변량 ---
fig, axes = plt.subplots(2, 2, figsize=(16, 14))

ax = axes[0, 0]
wx_sums = {wx: sum([n for n in POSITIONS if wuxing_of(n) == wx]) for wx in ["수", "화", "목", "금", "토"]}
wx_names = list(wx_sums.keys())
wx_vals = list(wx_sums.values())
wx_colors_bar = [WUXING_COLOR[w] for w in wx_names]
ax.bar(wx_names, wx_vals, color=wx_colors_bar, edgecolor="black", linewidth=1.5)
ax.set_title("오행별 수 합 (55, 38, 62, 70, 40)", fontsize=12, fontweight="bold")
for bar, val in zip(ax.patches, wx_vals):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        str(val),
        ha="center",
        fontsize=12,
        fontweight="bold",
    )

ax = axes[0, 1]
components = {
    "좌": sum(LEFT_VALUES),
    "중": sum(MID_VALUES),
    "우": sum(RIGHT_VALUES),
    "전체": sum(POSITIONS),
}
ax.bar(
    list(components.keys()),
    list(components.values()),
    color=["#4488CC", "#44AA44", "#CC4444", "#333333"],
    edgecolor="black",
    linewidth=1.5,
)
ax.set_title("좌·중·우 대칭 합 (좌=우=86)", fontsize=12, fontweight="bold")
ax.set_ylabel("Sum", fontsize=10)
for bar, val in zip(ax.patches, components.values()):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 2,
        str(val),
        ha="center",
        fontsize=12,
        fontweight="bold",
    )

ax = axes[1, 0]
# 수평 단별 합 (세로 막대)
level_sums_v = [sum(LEVELS[y]) for y in LEVEL_ORDER]
ax.bar(level_names, level_sums_v, color="#CC4444", edgecolor="black", linewidth=1.5)
ax.set_title("수평 단별 합", fontsize=12, fontweight="bold")
ax.set_ylabel("Sum", fontsize=10)
plt.setp(ax.xaxis.get_majorticklabels(), rotation=15, ha="right")
for bar, val in zip(ax.patches, level_sums_v):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        str(val),
        ha="center",
        fontsize=10,
        fontweight="bold",
    )

ax = axes[1, 1]
# 누락 수 복원 시 오행별 개수
extended_counts = []
for r in [1, 2, 3, 4, 0]:
    base = GROUPS[r]
    missing_same = [n for n in range(1, 26) if n % 5 == r and n not in base]
    extended = base + missing_same[: 5 - len(base)]
    extended_counts.append((RESIDUE_STYLE[r]["name"], len(extended)))
labels = [f"{wx}\n({cnt}개)" for wx, cnt in extended_counts]
counts = [cnt for _, cnt in extended_counts]
colors_cnt = [WUXING_COLOR[wx] for wx, _ in extended_counts]
ax.bar(labels, counts, color=colors_cnt, edgecolor="black", linewidth=1.5)
ax.set_title("완전 5×5 확장 시 오행별 개수", fontsize=12, fontweight="bold")
for bar, val in zip(ax.patches, counts):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.05,
        str(val),
        ha="center",
        fontsize=12,
        fontweight="bold",
    )

plt.tight_layout()
save_fig("05_invariants.png")
plt.close()

# --- 06: 오행 상생상극 관계도 ---
fig, ax = plt.subplots(figsize=(10, 8))
wuxing_graph_relations = [
    ("수", "목", "생"),
    ("목", "화", "생"),
    ("화", "토", "생"),
    ("토", "금", "생"),
    ("금", "수", "생"),
    ("수", "화", "극"),
    ("화", "금", "극"),
    ("금", "목", "극"),
    ("목", "토", "극"),
    ("토", "수", "극"),
]
# 수동으로 화살표 그리기
wx_pos = {"수": (0, 2), "목": (2, 1), "화": (1, -1), "토": (-1, -1), "금": (-2, 1)}
for u, v, r in wuxing_graph_relations:
    x1, y1 = wx_pos[u]
    x2, y2 = wx_pos[v]
    color = "#44AA44" if r == "생" else "#CC4444"
    style = "-" if r == "생" else "--"
    rad = 0.15 if r == "생" else -0.15
    # 화살표
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(arrowstyle="->", color=color, lw=2.5 if r == "생" else 2,
                        connectionstyle=f"arc3,rad={rad}"),
    )

for wx, (x, y) in wx_pos.items():
    ax.add_patch(
        plt.Circle(
            (x, y),
            0.35,
            facecolor=WUXING_COLOR[wx],
            edgecolor="black",
            linewidth=2.5,
            zorder=2,
        )
    )
    ax.text(x, y, wx, ha="center", va="center", fontsize=14, fontweight="bold", zorder=3)

legend_elements = [
    Line2D([0], [0], color="#44AA44", lw=3, label="상생"),
    Line2D([0], [0], color="#CC4444", lw=2, linestyle="--", label="상극"),
]
ax.legend(handles=legend_elements, loc="upper right", fontsize=11)
ax.set_title("오행 상생상극 관계도", fontsize=14, fontweight="bold")
ax.set_xlim(-3, 3.5)
ax.set_ylim(-2.5, 3)
ax.set_aspect("equal")
ax.axis("off")
plt.tight_layout()
save_fig("06_wuxing_relations.png")
plt.close()

# --- 07: 확장 및 층별 분포 ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

ax = axes[0]
extended_totals = []
for r in [1, 2, 3, 4, 0]:
    base = GROUPS[r]
    missing_same_residue = [n for n in range(1, 26) if n % 5 == r and n not in base]
    extended = base + missing_same_residue[: 5 - len(base)]
    extended_totals.append((RESIDUE_STYLE[r]["name"], sum(extended), len(extended)))

labels = [f"{wx}\n({cnt}개)" for wx, _, cnt in extended_totals]
values = [t for _, t, _ in extended_totals]
colors_ext = [WUXING_COLOR[wx] for wx, _, _ in extended_totals]
ax.bar(labels, values, color=colors_ext, edgecolor="black", linewidth=1.5)
ax.set_title("완전 5×5 오행 확장 (가상 25수)", fontsize=13, fontweight="bold")
for bar, val in zip(ax.patches, values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        str(val),
        ha="center",
        fontsize=12,
        fontweight="bold",
    )
ax.set_ylabel("Sum", fontsize=10)

ax = axes[1]
layer_names = ["상단 정점\n(y=6.0)", "상부 연결대\n(y=5.0~4.2)", "중앙 수평대\n(y=3.3~2.0)", "하부 연결대\n(y=0.8~-0.4)", "하단 정점\n(y=-1.7)"]
layer_values = [
    sum(LEVELS[6.0]),
    sum(LEVELS[5.0]) + sum(LEVELS[4.2]),
    sum(LEVELS[3.3]) + sum(LEVELS[2.0]),
    sum(LEVELS[0.8]) + sum(LEVELS[-0.4]),
    sum(LEVELS[-1.7]),
]
layer_colors = ["#CC4444", "#4488CC", "#44AA44", "#CC9944", "#888888"]
ax.barh(layer_names, layer_values, color=layer_colors, edgecolor="black", linewidth=1.5)
ax.set_title("수직 층별 합 분포", fontsize=13, fontweight="bold")
for bar, val in zip(ax.patches, layer_values):
    ax.text(
        bar.get_width() + 1,
        bar.get_y() + bar.get_height() / 2,
        str(val),
        ha="left",
        va="center",
        fontsize=11,
        fontweight="bold",
    )
ax.set_xlabel("Sum", fontsize=10)

plt.tight_layout()
save_fig("07_local_extensions.png")
plt.close()

# --- 08: 위치 패턴 (수평 단 / 좌중우) ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

ax = axes[0]
palace_names = [f"y={y}" for y in LEVEL_ORDER]
level_sums_list = [sum(LEVELS[y]) for y in LEVEL_ORDER]
level_counts = [len(LEVELS[y]) for y in LEVEL_ORDER]
x = np.arange(len(LEVEL_ORDER))
width = 0.35
ax.bar(x - width / 2, level_sums_list, width, label="단별 합", color="#CC4444", edgecolor="black")
ax2 = ax.twinx()
ax2.bar(x + width / 2, level_counts, width, label="노드 수", color="#4488CC", edgecolor="black", alpha=0.7)
ax.set_xticks(x)
ax.set_xticklabels(palace_names, rotation=15, ha="right")
ax.set_title("수평 단별 합 및 노드 수", fontsize=13, fontweight="bold")
ax.set_ylabel("Sum", fontsize=10)
ax2.set_ylabel("Count", fontsize=10)
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

ax = axes[1]
components = {
    "좌": sum(LEFT_VALUES),
    "중": sum(MID_VALUES),
    "우": sum(RIGHT_VALUES),
}
ax.bar(
    list(components.keys()),
    list(components.values()),
    color=["#4488CC", "#44AA44", "#CC4444"],
    edgecolor="black",
    linewidth=1.5,
)
ax.set_title("좌·중·우 대칭 합", fontsize=13, fontweight="bold")
ax.set_ylabel("Sum", fontsize=10)
for bar, val in zip(ax.patches, components.values()):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        str(val),
        ha="center",
        fontsize=12,
        fontweight="bold",
    )
ax.axhline(y=sum(LEFT_VALUES), color="red", linestyle="--", linewidth=1.5, alpha=0.5)

plt.tight_layout()
save_fig("08_position_patterns.png")
plt.close()

print("\n" + "=" * 60)
print("모든 이미지 생성 완료!")
print(f"출력 디렉토리: {OUTPUT_DIR}/")
print("=" * 60)
