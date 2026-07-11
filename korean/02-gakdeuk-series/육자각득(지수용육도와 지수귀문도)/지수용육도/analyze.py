#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
地數用六圖 (지수용육도) / 六子各得 — 현대 그래프·조합론적 심층 분석

《구수력(九數略)》계열 도상 중 지수용육도를 현대 수학 언어로 재해석.
분석 대상: 1부터 20까지의 수를 5개 육각형에 6자씩 배치한 벌집 교차 구조.
"""

from __future__ import annotations

import os
import sys
from collections import Counter
from pathlib import Path
from typing import Final

import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.axes import Axes
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Polygon

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

TITLE: Final = "지수용육도"
HANJA_TITLE: Final = "地數用六圖"
SUBTITLE: Final = "六子各得六十三數"
TARGET_SUM: Final = 63


def find_cjk_font() -> FontProperties:
    candidates = (
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf",
        "/usr/share/fonts/truetype/unfonts-core/UnDotum.ttf",
        "/usr/share/fonts/truetype/baekmuk/dotum.ttf",
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "C:/Windows/Fonts/malgun.ttf",
        "C:/Windows/Fonts/gulim.ttc",
    )
    for candidate in candidates:
        if Path(candidate).exists():
            return FontProperties(fname=candidate)
    return FontProperties()


def save_fig(name: str) -> None:
    path = f"{OUTPUT_DIR}/{name}"
    plt.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    print(f"[저장] {path}")


# ============================================================
# 1. 원본 데이터 구조화
# ============================================================

# 손그림의 구조를 반듯한 벌집형 격자로 정규화했다.
# 다섯 육각형은 인접 육각형과 일부 정점·간선을 공유한다.
POSITIONS: Final = {
    # 상단 왼쪽 육각형의 외곽
    5: (-2.0, 4.5),
    18: (-3.0, 3.6),
    16: (-3.0, 2.5),
    3: (-2.0, 1.7),
    8: (-1.0, 2.5),
    13: (-1.0, 3.6),

    # 상단 오른쪽 육각형의 외곽
    1: (0.0, 4.5),
    7: (1.0, 3.6),
    20: (1.0, 2.5),
    14: (0.0, 1.7),

    # 중앙 육각형의 하단
    12: (-2.0, 0.3),
    11: (-1.0, -0.5),
    15: (0.0, 0.3),

    # 하단 왼쪽 육각형의 외곽
    9: (-3.0, -0.5),
    19: (-3.0, -1.7),
    2: (-2.0, -2.5),
    10: (-1.0, -1.7),

    # 하단 오른쪽 육각형의 외곽
    4: (1.0, -0.5),
    17: (1.0, -1.7),
    6: (0.0, -2.5),
}

# 각 육각형은 시계 방향의 6개 정점으로 정의한다.
HEXAGONS: Final = {
    "상좌": (5, 18, 16, 3, 8, 13),
    "상우": (1, 13, 8, 14, 20, 7),
    "중앙": (3, 8, 14, 15, 11, 12),
    "하좌": (12, 11, 10, 2, 19, 9),
    "하우": (15, 4, 17, 6, 10, 11),
}

RESIDUE_STYLE: Final = {
    1: {"label": "n mod 5 ≡ 1", "face": "#3F3F3F", "edge": "#161616", "text": "#FFFFFF", "name": "수", "en": "Water"},
    2: {"label": "n mod 5 ≡ 2", "face": "#F1CDCD", "edge": "#B63E3E", "text": "#782020", "name": "화", "en": "Fire"},
    3: {"label": "n mod 5 ≡ 3", "face": "#D4E3F7", "edge": "#3E70AF", "text": "#244C7B", "name": "목", "en": "Wood"},
    4: {"label": "n mod 5 ≡ 4", "face": "#E1E1E1", "edge": "#666666", "text": "#222222", "name": "금", "en": "Metal"},
    0: {"label": "n mod 5 ≡ 0", "face": "#F5E1A2", "edge": "#B98D00", "text": "#725500", "name": "토", "en": "Earth"},
}

WUXING_COLOR: Final = {
    "수": "#4488CC",
    "화": "#CC4444",
    "목": "#44AA44",
    "금": "#888888",
    "토": "#CC9944",
}

HEXAGON_COLORS: Final = {
    "상좌": "#CC4444",
    "상우": "#4488CC",
    "중앙": "#44AA44",
    "하좌": "#CC9944",
    "하우": "#888888",
}


def wuxing_of(n: int) -> str:
    r = n % 5
    return RESIDUE_STYLE[r]["name"]


def residue_1based(n: int) -> int:
    r = n % 5
    return 5 if r == 0 else r


# ============================================================
# 2. 그래프 구성
# ============================================================

FULL_EDGES: list[tuple[int, int]] = []
seen_edges: set[tuple[int, int]] = set()
for vertices in HEXAGONS.values():
    for start, end in zip(vertices, vertices[1:] + vertices[:1]):
        edge = tuple(sorted((start, end)))
        if edge not in seen_edges:
            seen_edges.add(edge)
            FULL_EDGES.append(edge)

G_full = nx.Graph()
G_full.add_edges_from(FULL_EDGES)
for n in range(1, 21):
    G_full.add_node(n)
    G_full.nodes[n]["wuxing"] = wuxing_of(n)


# 정점이 속한 육각형 목록
VERTEX_TO_HEXAGONS: dict[int, list[str]] = {n: [] for n in range(1, 21)}
for hex_name, vertices in HEXAGONS.items():
    for v in vertices:
        VERTEX_TO_HEXAGONS[v].append(hex_name)


def shared_count(v: int) -> int:
    return len(VERTEX_TO_HEXAGONS[v])


# ============================================================
# 3. 조합론·그래프 이론 분석
# ============================================================


def validate() -> None:
    numbers = sorted(POSITIONS)
    if numbers != list(range(1, 21)):
        raise ValueError("1부터 20까지의 수가 정확히 한 번씩 있어야 합니다.")

    for hex_name, vertices in HEXAGONS.items():
        value_sum = sum(vertices)
        if value_sum != TARGET_SUM:
            raise ValueError(
                f"{hex_name} 육각형의 합은 {value_sum}이며, {TARGET_SUM}이어야 합니다."
            )

    # 중복 계수 합 검증: 5개 육각형 × 6정점 = 30, 공유 정점이 여러 번 셈.
    repeated_total = sum(sum(vertices) for vertices in HEXAGONS.values())
    if repeated_total != TARGET_SUM * len(HEXAGONS):
        raise ValueError(f"중복 계수 합이 {repeated_total}입니다.")


validate()

print("=" * 60)
print(f"{HANJA_TITLE} ({TITLE}) 현대 그래프·조합론 분석")
print("=" * 60)
print(f"노드 수: {G_full.number_of_nodes()}")
print(f"엣지 수: {G_full.number_of_edges()}")
print(f"연결 성분: {nx.number_connected_components(G_full)}")

deg_seq_full = sorted([d for _, d in G_full.degree()], reverse=True)
print(f"차수 시퀀스: {deg_seq_full}")

print("\n육각형별 6자 합:")
for hex_name, vertices in HEXAGONS.items():
    print(f"  {hex_name}: {' + '.join(map(str, vertices))} = {sum(vertices)}")

print("\n오행별 수 합:")
for r in [1, 2, 3, 4, 5]:
    nodes = [n for n in range(1, 21) if residue_1based(n) == r]
    wx = RESIDUE_STYLE[r % 5]["name"]
    print(f"  {wx}({r}): 합={sum(nodes)}, 수들={nodes}")

print("\n육각형별 오행 분포:")
for hex_name in HEXAGONS:
    vals = list(HEXAGONS[hex_name])
    counts = Counter(wuxing_of(v) for v in vals)
    print(f"  {hex_name}: {dict(counts)}")

print("\n정점별 공유 육각형 수:")
for v in range(1, 21):
    print(f"  {v}({wuxing_of(v)}): {shared_count(v)}개 {VERTEX_TO_HEXAGONS[v]}")

betw_full = nx.betweenness_centrality(G_full)
print("\nBetweenness Centrality (Top 10):")
for n, v in sorted(betw_full.items(), key=lambda x: -x[1])[:10]:
    print(f"  {n}({wuxing_of(n)}): {v:.3f}")

# 오행 엣지 분류
wx_edge_counts: dict[str, int] = {}
for u, v in G_full.edges():
    wu, wv = wuxing_of(u), wuxing_of(v)
    if wu == wv:
        key = "동질"
    elif (wu, wv) in [
        ("수", "목"),
        ("목", "화"),
        ("화", "토"),
        ("토", "금"),
        ("금", "수"),
    ] or (wv, wu) in [
        ("수", "목"),
        ("목", "화"),
        ("화", "토"),
        ("토", "금"),
        ("금", "수"),
    ]:
        key = "상생"
    elif (wu, wv) in [
        ("수", "화"),
        ("화", "금"),
        ("금", "목"),
        ("목", "토"),
        ("토", "수"),
    ] or (wv, wu) in [
        ("수", "화"),
        ("화", "금"),
        ("금", "목"),
        ("목", "토"),
        ("토", "수"),
    ]:
        key = "상극"
    else:
        key = "중성"
    wx_edge_counts[key] = wx_edge_counts.get(key, 0) + 1

print("\n오행 엣지 분포:")
for key, cnt in wx_edge_counts.items():
    print(f"  {key}: {cnt}")

# 사이클 기반
hex_cycles = {
    hex_name: list(vertices) for hex_name, vertices in HEXAGONS.items()
}
print("\n각 육각형의 6-Cycle:")
for hex_name, cycle in hex_cycles.items():
    print(f"  {hex_name}: {' → '.join(map(str, cycle + [cycle[0]]))}")

# ============================================================
# 4. 위치 기반 분석 (공유 정점 vs 고유 정점)
# ============================================================

SHARED_VALUES = [v for v in range(1, 21) if shared_count(v) > 1]
UNIQUE_VALUES = [v for v in range(1, 21) if shared_count(v) == 1]

print("\n공유 정점:", sorted(SHARED_VALUES))
print("고유 정점:", sorted(UNIQUE_VALUES))

# ============================================================
# 5. 일반화 가족
# ============================================================

# mod 5 잉여 클래스 합: 34, 38, 42, 46, 50 (등차 4)
FAMILY_RESIDUE = [(m0, 34 + (m0 - 1) * 4) for m0 in range(1, 6)]
print("\nmod 5 잉여 클래스 합의 일반화:")
for m0, total in FAMILY_RESIDUE:
    wx = RESIDUE_STYLE[m0 % 5]["name"]
    print(f"  M0={m0}({wx}): 클래스 합={total}")

# ============================================================
# 6. 시각화 헬퍼
# ============================================================


def draw_hexagon_boundaries(ax: Axes, labels: bool = True) -> None:
    fills = ("#F8F8F8", "#FBFBFB", "#F6F6F6", "#FAFAFA", "#F7F7F7")
    for (hex_name, vertices), fill in zip(HEXAGONS.items(), fills):
        polygon_points = [POSITIONS[number] for number in vertices]
        ax.add_patch(
            Polygon(
                polygon_points,
                closed=True,
                facecolor=fill,
                edgecolor="#777777",
                linewidth=1.5,
                linestyle=(0, (4, 4)),
                zorder=0,
            )
        )
        if labels:
            center_x = sum(point[0] for point in polygon_points) / 6
            center_y = sum(point[1] for point in polygon_points) / 6
            ax.text(
                center_x,
                center_y,
                f"{hex_name}\nΣ={TARGET_SUM}",
                ha="center",
                va="center",
                fontsize=9,
                color="#555555",
                zorder=1,
            )


def draw_edges(ax: Axes, color: str = "#303030", alpha: float = 1.0, lw: float = 2.0) -> None:
    for start, end in FULL_EDGES:
        x1, y1 = POSITIONS[start]
        x2, y2 = POSITIONS[end]
        ax.plot(
            [x1, x2],
            [y1, y2],
            color=color,
            linewidth=lw,
            alpha=alpha,
            solid_capstyle="round",
            zorder=1,
        )


def draw_nodes(
    ax: Axes,
    highlight_values: set[int] | None = None,
    dim_others: bool = False,
    node_radius: float = 0.28,
) -> None:
    for value, (x, y) in POSITIONS.items():
        r = value % 5
        style = RESIDUE_STYLE[r]
        color = style["face"]
        edge = style["edge"]
        lw = 2.0
        text_color = style["text"]
        z_node = 2
        z_text = 3
        fs = 10

        if highlight_values is not None:
            if value in highlight_values:
                z_node = 4
                z_text = 5
                fs = 11
                lw = 3.0
            else:
                if dim_others:
                    color = "#F0F0F0"
                    edge = "#CCCCCC"
                    text_color = "#AAAAAA"
                    lw = 1.0
                    fs = 8
                    z_node = 1
                    z_text = 2

        ax.add_patch(
            Circle(
                (x, y),
                node_radius,
                facecolor=color,
                edgecolor=edge,
                linewidth=lw,
                zorder=z_node,
            )
        )
        ax.text(
            x,
            y,
            str(value),
            ha="center",
            va="center",
            fontsize=fs,
            fontweight="bold" if highlight_values and value in highlight_values else "normal",
            color=text_color,
            zorder=z_text,
        )


def set_ax_lims(ax: Axes) -> None:
    ax.set_xlim(-3.7, 1.7)
    ax.set_ylim(-3.2, 5.2)
    ax.set_aspect("equal")
    ax.axis("off")


# ============================================================
# 7. 시각화
# ============================================================

# --- 01: 원본 그래프 ---
fig, ax = plt.subplots(figsize=(12, 11))
draw_hexagon_boundaries(ax)
for start, end in FULL_EDGES:
    x1, y1 = POSITIONS[start]
    x2, y2 = POSITIONS[end]
    hex_start = VERTEX_TO_HEXAGONS[start][0]
    hex_end = VERTEX_TO_HEXAGONS[end][0]
    if hex_start == hex_end:
        ax.plot([x1, x2], [y1, y2], color=HEXAGON_COLORS[hex_start], linewidth=2.5, alpha=0.7, zorder=1)
    else:
        ax.plot([x1, x2], [y1, y2], color="#333333", linewidth=1.8, alpha=0.5, zorder=1)
draw_nodes(ax)
ax.set_title(
    f"{HANJA_TITLE} ({TITLE}) - 원본 벌집 교차 구조\n"
    "5육각형 · 6자 · 각 육각형 합 63 · 전체 합 210",
    fontsize=16,
    fontweight="bold",
)
set_ax_lims(ax)
legend_elements = [
    mpatches.Patch(facecolor=WUXING_COLOR[wx], edgecolor="black", label=f"{wx}")
    for wx in ["수", "화", "목", "금", "토"]
]
ax.legend(handles=legend_elements, loc="lower right", fontsize=10, framealpha=0.9)
save_fig("01_original_graph.png")
plt.close()

# --- 02: 오행별 서브그래프 분해 ---
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()
ax = axes[0]
draw_hexagon_boundaries(ax, labels=False)
draw_edges(ax, color="#CCCCCC", alpha=0.5, lw=1)
draw_nodes(ax)
ax.set_title("전체 그래프", fontsize=13, fontweight="bold")
set_ax_lims(ax)

for idx, wx in enumerate(["수", "화", "목", "금", "토"]):
    ax = axes[idx + 1]
    draw_hexagon_boundaries(ax, labels=False)
    wx_nodes = [n for n in range(1, 21) if wuxing_of(n) == wx]
    other_nodes = [n for n in range(1, 21) if n not in wx_nodes]

    draw_edges(ax, color="#EEEEEE", alpha=0.4, lw=1)

    for n in other_nodes:
        x, y = POSITIONS[n]
        ax.add_patch(
            Circle(
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
            Circle(
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
    set_ax_lims(ax)

plt.suptitle("오행(五行)별 서브그래프 분해", fontsize=16, fontweight="bold", y=1.02)
plt.tight_layout()
save_fig("02_wuxing_decomposition.png")
plt.close()

# --- 03: 인접 행렬 + 스펙트럼 ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
adj = nx.adjacency_matrix(G_full, nodelist=sorted(G_full.nodes())).todense()
im = ax.imshow(adj, cmap="YlOrRd", interpolation="nearest")
ax.set_xticks(range(20))
ax.set_yticks(range(20))
ax.set_xticklabels(sorted(G_full.nodes()), fontsize=8)
ax.set_yticklabels(sorted(G_full.nodes()), fontsize=8)
wx_sorted = [wuxing_of(n) for n in sorted(G_full.nodes())]
boundaries = [i - 0.5 for i in range(1, 20) if wx_sorted[i] != wx_sorted[i - 1]]
for b in boundaries:
    ax.axhline(y=b, color="blue", linewidth=1.5, alpha=0.7)
    ax.axvline(x=b, color="blue", linewidth=1.5, alpha=0.7)
plt.colorbar(im, ax=ax, shrink=0.8)
ax.set_title("Adjacency Matrix (육각형 그래프)", fontsize=13, fontweight="bold")

ax = axes[1]
eigenvalues = np.linalg.eigvalsh(adj)
ax.bar(
    range(len(eigenvalues)),
    sorted(eigenvalues, reverse=True),
    color="#4488CC",
    edgecolor="black",
    alpha=0.8,
)
ax.axhline(y=0, color="red", linestyle="--", linewidth=1)
ax.set_xlabel("Index", fontsize=11)
ax.set_ylabel("Eigenvalue", fontsize=11)
ax.set_title(
    f"Graph Spectrum\nλ_max={max(eigenvalues):.2f}, λ_min={min(eigenvalues):.2f}",
    fontsize=13,
    fontweight="bold",
)
ax.grid(True, alpha=0.3)
plt.tight_layout()
save_fig("03_adjacency_spectrum.png")
plt.close()

# --- 04: 사이클 분석 ---
fig, axes = plt.subplots(2, 2, figsize=(16, 14))

ax = axes[0, 0]
draw_hexagon_boundaries(ax, labels=False)
for start, end in FULL_EDGES:
    x1, y1 = POSITIONS[start]
    x2, y2 = POSITIONS[end]
    hex_start = VERTEX_TO_HEXAGONS[start][0]
    ax.plot([x1, x2], [y1, y2], color=HEXAGON_COLORS[hex_start], linewidth=3, alpha=0.8, zorder=1)
draw_nodes(ax)
ax.set_title("5개 육각형의 6-Cycle", fontsize=13, fontweight="bold")
set_ax_lims(ax)

ax = axes[0, 1]
# 중앙 육각형 강조
central_cycle = list(HEXAGONS["중앙"])
central_edges = [(central_cycle[i], central_cycle[(i + 1) % 6]) for i in range(6)]
draw_hexagon_boundaries(ax, labels=False)
for start, end in FULL_EDGES:
    x1, y1 = POSITIONS[start]
    x2, y2 = POSITIONS[end]
    if (start, end) in central_edges or (end, start) in central_edges:
        ax.plot([x1, x2], [y1, y2], color="red", linewidth=3.5, alpha=0.9, zorder=2)
    else:
        ax.plot([x1, x2], [y1, y2], color="#DDDDDD", linewidth=1, alpha=0.4, zorder=0)
for n in central_cycle:
    x, y = POSITIONS[n]
    ax.add_patch(
        Circle(
            (x, y),
            0.34,
            facecolor="#FFCCCC",
            edgecolor="red",
            linewidth=3,
            zorder=2,
        )
    )
    ax.text(x, y, str(n), ha="center", va="center", fontsize=10, fontweight="bold", zorder=3)
for n in range(1, 21):
    if n in central_cycle:
        continue
    x, y = POSITIONS[n]
    ax.add_patch(
        Circle(
            (x, y),
            0.26,
            facecolor="white",
            edgecolor="#999999",
            linewidth=1.2,
            zorder=1,
        )
    )
    ax.text(x, y, str(n), ha="center", va="center", fontsize=8, zorder=2)
ax.set_title(f"중앙 육각형 6-Cycle: {' → '.join(map(str, central_cycle + [central_cycle[0]]))}", fontsize=13, fontweight="bold")
set_ax_lims(ax)

ax = axes[1, 0]
hex_names = list(HEXAGONS.keys())
hex_sums = [sum(HEXAGONS[h]) for h in hex_names]
hex_bar_colors = [HEXAGON_COLORS[h] for h in hex_names]
ax.bar(hex_names, hex_sums, color=hex_bar_colors, edgecolor="black", linewidth=1.5)
ax.axhline(y=TARGET_SUM, color="red", linestyle="--", linewidth=2)
ax.set_title("각 육각형의 6자 합", fontsize=13, fontweight="bold")
for bar, val in zip(ax.patches, hex_sums):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.3,
        str(val),
        ha="center",
        fontsize=12,
        fontweight="bold",
    )

ax = axes[1, 1]
# 사이클 길이 분포
cycle_lengths = [len(c) for c in nx.cycle_basis(G_full)]
hist, bins = np.histogram(cycle_lengths, bins=[5.5, 6.5, 7.5, 8.5, 9.5, 10.5])
ax.bar(["6", "7", "8", "9", "10"], hist, color="#44AA44", edgecolor="black")
ax.set_title(f"Cycle basis 길이 분포\n총 {len(cycle_lengths)}개 기저 사이클", fontsize=13, fontweight="bold")
ax.set_xlabel("Cycle length", fontsize=10)
ax.set_ylabel("Count", fontsize=10)

plt.tight_layout()
save_fig("04_cycle_analysis.png")
plt.close()

# --- 05: 중심성 + 합 불변량 ---
fig, axes = plt.subplots(2, 2, figsize=(16, 14))

ax = axes[0, 0]
degrees = dict(G_full.degree())
nodes_sorted = sorted(G_full.nodes(), key=lambda n: degrees[n], reverse=True)
colors_sorted = [WUXING_COLOR[wuxing_of(n)] for n in nodes_sorted]
ax.bar(range(20), [degrees[n] for n in nodes_sorted], color=colors_sorted, edgecolor="black")
ax.set_xticks(range(20))
ax.set_xticklabels([str(n) for n in nodes_sorted], fontsize=8)
ax.set_title("Degree (육각형 그래프)", fontsize=12, fontweight="bold")
ax.set_ylabel("Degree", fontsize=10)

ax = axes[0, 1]
betw_sorted = sorted(G_full.nodes(), key=lambda n: betw_full[n], reverse=True)
colors_b = [WUXING_COLOR[wuxing_of(n)] for n in betw_sorted]
ax.bar(range(20), [betw_full[n] for n in betw_sorted], color=colors_b, edgecolor="black")
ax.set_xticks(range(20))
ax.set_xticklabels([str(n) for n in betw_sorted], fontsize=8)
ax.set_title("Betweenness Centrality", fontsize=12, fontweight="bold")
ax.set_ylabel("Centrality", fontsize=10)

ax = axes[1, 0]
wx_sums = {wx: sum([n for n in range(1, 21) if wuxing_of(n) == wx]) for wx in ["수", "화", "목", "금", "토"]}
wx_names = list(wx_sums.keys())
wx_vals = list(wx_sums.values())
wx_colors_bar = [WUXING_COLOR[w] for w in wx_names]
ax.bar(wx_names, wx_vals, color=wx_colors_bar, edgecolor="black", linewidth=1.5)
ax.set_title("오행별 수 합 (34, 38, 42, 46, 50)", fontsize=12, fontweight="bold")
for bar, val in zip(ax.patches, wx_vals):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        str(val),
        ha="center",
        fontsize=12,
        fontweight="bold",
    )
ax.plot(range(5), wx_vals, "o--", color="black", alpha=0.5, linewidth=2)

ax = axes[1, 1]
components = {
    "상좌": sum(HEXAGONS["상좌"]),
    "상우": sum(HEXAGONS["상우"]),
    "중앙": sum(HEXAGONS["중앙"]),
    "하좌": sum(HEXAGONS["하좌"]),
    "하우": sum(HEXAGONS["하우"]),
    "전체": sum(range(1, 21)),
}
ax.bar(
    list(components.keys()),
    list(components.values()),
    color=[HEXAGON_COLORS[k] for k in list(components.keys())[:-1]] + ["#333333"],
    edgecolor="black",
    linewidth=1.5,
)
ax.set_title("구조적 부분집합 합", fontsize=12, fontweight="bold")
ax.set_ylabel("Sum", fontsize=10)
plt.setp(ax.xaxis.get_majorticklabels(), rotation=15, ha="right")

plt.tight_layout()
save_fig("05_centrality_invariants.png")
plt.close()

# --- 06: 오행 상생상극 ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
wuxing_graph = nx.DiGraph()
wuxing_relations = [
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
for u, v, r in wuxing_relations:
    wuxing_graph.add_edge(u, v, relation=r)
wx_pos = {"수": (0, 2), "목": (2, 1), "화": (1, -1), "토": (-1, -1), "금": (-2, 1)}
sheng_edges = [(u, v) for u, v, r in wuxing_relations if r == "생"]
ke_edges = [(u, v) for u, v, r in wuxing_relations if r == "극"]
nx.draw_networkx_edges(
    wuxing_graph,
    wx_pos,
    edgelist=sheng_edges,
    edge_color="#44AA44",
    width=3,
    alpha=0.8,
    arrows=True,
    arrowsize=20,
    connectionstyle="arc3,rad=0.15",
    ax=ax,
)
nx.draw_networkx_edges(
    wuxing_graph,
    wx_pos,
    edgelist=ke_edges,
    edge_color="#CC4444",
    width=2,
    alpha=0.6,
    style="--",
    arrows=True,
    arrowsize=15,
    connectionstyle="arc3,rad=-0.15",
    ax=ax,
)
wx_node_colors = [WUXING_COLOR[w] for w in wuxing_graph.nodes()]
nx.draw_networkx_nodes(
    wuxing_graph,
    wx_pos,
    node_color=wx_node_colors,
    node_size=3000,
    edgecolors="black",
    linewidths=2.5,
    ax=ax,
)
nx.draw_networkx_labels(wuxing_graph, wx_pos, font_size=14, font_weight="normal", ax=ax)
legend_elements = [
    Line2D([0], [0], color="#44AA44", lw=3, label="상생"),
    Line2D([0], [0], color="#CC4444", lw=2, linestyle="--", label="상극"),
]
ax.legend(handles=legend_elements, loc="upper right", fontsize=11)
ax.set_title("오행 상생상극 관계도", fontsize=13, fontweight="bold")
ax.set_xlim(-3, 3.5)
ax.set_ylim(-2.5, 3)
ax.axis("off")

ax = axes[1]
colors_pie = ["#44AA44", "#CC4444", "#CC9944", "#4488CC"]
ax.pie(
    list(wx_edge_counts.values()),
    labels=list(wx_edge_counts.keys()),
    autopct="%1.0f%%",
    colors=colors_pie[: len(wx_edge_counts)],
    explode=[0.05] * len(wx_edge_counts),
    textprops={"fontsize": 12, "fontweight": "bold"},
)
ax.set_title(f"오행 엣지 분포 (N={G_full.number_of_edges()})", fontsize=13, fontweight="bold")
plt.tight_layout()
save_fig("06_wuxing_relations.png")
plt.close()

# --- 07: 확장 및 일반화 ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

ax = axes[0]
m0_labels = [f"M0={m0}" for m0, _ in FAMILY_RESIDUE]
m0_values = [total for _, total in FAMILY_RESIDUE]
m0_colors = [WUXING_COLOR[RESIDUE_STYLE[m0 % 5]["name"]] for m0, _ in FAMILY_RESIDUE]
ax.bar(m0_labels, m0_values, color=m0_colors, edgecolor="black", linewidth=1.5)
ax.set_title("mod 5 잉여 클래스 합의 등차수열\nM(n+1) = M(n) + 4", fontsize=13, fontweight="bold")
for bar, val in zip(ax.patches, m0_values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        str(val),
        ha="center",
        fontsize=12,
        fontweight="bold",
    )
ax.plot(range(5), m0_values, "o--", color="black", alpha=0.5, linewidth=2)
ax.set_ylabel("Residue-class Sum", fontsize=10)

ax = axes[1]
n_layers = 3
theta = np.linspace(0, 2 * np.pi, n_layers + 1)[:-1]
for i, t in enumerate(theta):
    r = 2.5 + i * 1.5
    circle = plt.Circle((0, 0), r, fill=False, color=["#CC4444", "#4488CC", "#44AA44"][i], linewidth=2, linestyle="--")
    ax.add_patch(circle)
    ax.text(r * np.cos(np.pi / 4), r * np.sin(np.pi / 4), f"{20 * (i + 1)}자", fontsize=10, fontweight="bold")
ax.add_patch(plt.Circle((0, 0), 0.5, facecolor="#CC9944", edgecolor="black", linewidth=2))
ax.text(0, 0, "CORE\n20", ha="center", va="center", fontsize=10, fontweight="bold")
ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("동심원 확장: 20k자 구조", fontsize=13, fontweight="bold")

plt.tight_layout()
save_fig("07_local_extensions.png")
plt.close()

# --- 08: 위치 패턴 (공유 정점 vs 고유 정점) ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

ax = axes[0]
draw_hexagon_boundaries(ax, labels=False)
for n in SHARED_VALUES:
    x, y = POSITIONS[n]
    ax.add_patch(
        Circle(
            (x, y),
            0.34,
            facecolor="#FFCCCC",
            edgecolor="red",
            linewidth=3,
            zorder=2,
        )
    )
    ax.text(x, y, str(n), ha="center", va="center", fontsize=10, fontweight="bold", zorder=3)
for n in UNIQUE_VALUES:
    x, y = POSITIONS[n]
    ax.add_patch(
        Circle(
            (x, y),
            0.28,
            facecolor="#E8F4FF",
            edgecolor="#4488CC",
            linewidth=2,
            zorder=1,
        )
    )
    ax.text(x, y, str(n), ha="center", va="center", fontsize=9, zorder=2)
draw_edges(ax, color="#303030", alpha=0.3, lw=1.5)
ax.set_title("공유 정점(빨강) vs 고유 정점(파랑)", fontsize=13, fontweight="bold")
set_ax_lims(ax)

ax = axes[1]
share_counts = [shared_count(v) for v in range(1, 21)]
colors_sc = [WUXING_COLOR[wuxing_of(v)] for v in range(1, 21)]
ax.bar(range(1, 21), share_counts, color=colors_sc, edgecolor="black")
ax.set_xticks(range(1, 21))
ax.set_xticklabels([str(n) for n in range(1, 21)], fontsize=8)
ax.set_title("정점별 공유 육각형 수", fontsize=13, fontweight="bold")
ax.set_ylabel("Shared hexagons", fontsize=10)
ax.set_xlabel("Value", fontsize=10)

plt.tight_layout()
save_fig("08_position_patterns.png")
plt.close()

# ============================================================
# 8. 기본 시각화 (기존 analyze.py와 동일)
# ============================================================


def draw_basic(
    png_output: str | Path = "jisu_yong_yukdo.png",
    svg_output: str | Path = "jisu_yong_yukdo.svg",
) -> None:
    font = find_cjk_font()

    fig = plt.figure(figsize=(12.5, 9.0), dpi=220)
    graph_ax = fig.add_axes([0.04, 0.07, 0.63, 0.86])
    legend_ax = fig.add_axes([0.71, 0.08, 0.26, 0.84])

    graph_ax.set_aspect("equal")
    graph_ax.set_xlim(-3.7, 1.7)
    graph_ax.set_ylim(-3.2, 5.2)
    graph_ax.axis("off")

    # 육각형 영역
    fills = ("#F8F8F8", "#FBFBFB", "#F6F6F6", "#FAFAFA", "#F7F7F7")
    for (name, vertices), fill in zip(HEXAGONS.items(), fills):
        polygon_points = [POSITIONS[number] for number in vertices]
        graph_ax.add_patch(
            Polygon(
                polygon_points,
                closed=True,
                facecolor=fill,
                edgecolor="#A8A8A8",
                linewidth=1.1,
                linestyle=(0, (4, 4)),
                zorder=0,
            )
        )
        center_x = sum(point[0] for point in polygon_points) / 6
        center_y = sum(point[1] for point in polygon_points) / 6
        graph_ax.text(
            center_x,
            center_y,
            "sum 63",
            ha="center",
            va="center",
            fontsize=9.5,
            color="#9A9A9A",
            zorder=1,
        )

    # 엣지
    for start, end in FULL_EDGES:
        x1, y1 = POSITIONS[start]
        x2, y2 = POSITIONS[end]
        graph_ax.plot(
            [x1, x2],
            [y1, y2],
            color="#303030",
            linewidth=2.0,
            solid_capstyle="round",
            zorder=2,
        )

    # 노드
    radius = 0.28
    for number, (x, y) in POSITIONS.items():
        residue = number % 5
        style = RESIDUE_STYLE[residue]
        graph_ax.add_patch(
            Circle(
                (x, y),
                radius,
                facecolor=style["face"],
                edgecolor=style["edge"],
                linewidth=2.0,
                zorder=3,
            )
        )
        graph_ax.text(
            x,
            y,
            str(number),
            ha="center",
            va="center",
            fontproperties=font,
            fontsize=12,
            color=style["text"],
            zorder=4,
        )

    # 범례
    legend_ax.axis("off")
    legend_ax.text(
        0.0,
        0.98,
        f"{TITLE} ({HANJA_TITLE})",
        transform=legend_ax.transAxes,
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=17,
        weight="bold",
    )
    legend_ax.text(
        0.0,
        0.92,
        SUBTITLE,
        transform=legend_ax.transAxes,
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=13,
    )

    y = 0.84
    summary = (
        "정점: 1–20, 각 1회",
        "육각형: 5개",
        "각 육각형: 6개 정점",
        "각 육각형의 합: 63",
        "육각형별 정점 사용 횟수 합: 30",
    )
    for line in summary:
        legend_ax.text(
            0.0,
            y,
            f"• {line}",
            transform=legend_ax.transAxes,
            ha="left",
            va="top",
            fontproperties=font,
            fontsize=11,
        )
        y -= 0.053

    y -= 0.02
    legend_ax.text(
        0.0,
        y,
        "mod 5 residue groups",
        transform=legend_ax.transAxes,
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=14,
        weight="bold",
    )
    y -= 0.08
    for residue in (1, 2, 3, 4, 0):
        style = RESIDUE_STYLE[residue]
        group = [n for n in range(1, 21) if n % 5 == residue]
        legend_ax.add_patch(
            Circle(
                (0.04, y + 0.012),
                0.023,
                transform=legend_ax.transAxes,
                facecolor=style["face"],
                edgecolor=style["edge"],
                linewidth=1.5,
            )
        )
        legend_ax.text(
            0.09,
            y + 0.012,
            f"{style['label']} · 4개",
            transform=legend_ax.transAxes,
            ha="left",
            va="center",
            fontproperties=font,
            fontsize=10.8,
            weight="bold",
            color=style["text"],
        )
        legend_ax.text(
            0.09,
            y - 0.026,
            "{ " + ", ".join(str(number) for number in group) + " }",
            transform=legend_ax.transAxes,
            ha="left",
            va="top",
            fontproperties=font,
            fontsize=10,
            color="#333333",
        )
        y -= 0.10

    y -= 0.005
    legend_ax.text(
        0.0,
        y,
        "육각형별 검산",
        transform=legend_ax.transAxes,
        ha="left",
        va="top",
        fontproperties=font,
        fontsize=14,
        weight="bold",
    )
    y -= 0.065
    for name, vertices in HEXAGONS.items():
        expression = " + ".join(str(number) for number in vertices)
        legend_ax.text(
            0.0,
            y,
            f"{name}: {expression} = 63",
            transform=legend_ax.transAxes,
            ha="left",
            va="top",
            fontproperties=font,
            fontsize=9.7,
        )
        y -= 0.052

    graph_ax.set_title(
        f"{TITLE} ({HANJA_TITLE})",
        fontproperties=font,
        fontsize=18,
        pad=18,
    )

    fig.savefig(
        png_output,
        dpi=300,
        bbox_inches="tight",
        pad_inches=0.12,
        facecolor="white",
    )
    fig.savefig(
        svg_output,
        bbox_inches="tight",
        pad_inches=0.12,
        facecolor="white",
    )
    plt.close(fig)
    print(f"[저장] {png_output}")
    print(f"[저장] {svg_output}")


draw_basic()

# ============================================================
# 9. 보고서 작성
# ============================================================

degrees = dict(G_full.degree())
betw_full = nx.betweenness_centrality(G_full)
adj = nx.adjacency_matrix(G_full, nodelist=sorted(G_full.nodes())).todense()
eigenvalues = np.linalg.eigvalsh(adj)

report_md = f"""# 심층 분석 보고서: 지수용육도 (地數用六圖 / 六子各得)

## 1. 개요

지수용육도는 1부터 20까지의 자연수를 5개 육각형에 6자씩 배치한 도식입니다.
인접 육각형은 정점과 간선을 공유하며, 모든 육각형의 6자 합이 63로 일정합니다.

- **정점 수**: 20 (1–20, 각 1회)
- **육각형 수**: 5
- **엣지 수**: {G_full.number_of_edges()}
- **연결 성분**: {nx.number_connected_components(G_full)}
- **각 육각형 합**: {TARGET_SUM}
- **전체 합**: {sum(range(1, 21))}
- **중복 계수 합 (5×63)**: {TARGET_SUM * len(HEXAGONS)}

## 2. 육각형 데이터

| 육각형 | 6개 정점 | 합 |
|---|---|---|
| 상좌 | {' + '.join(map(str, HEXAGONS['상좌']))} | {sum(HEXAGONS['상좌'])} |
| 상우 | {' + '.join(map(str, HEXAGONS['상우']))} | {sum(HEXAGONS['상우'])} |
| 중앙 | {' + '.join(map(str, HEXAGONS['중앙']))} | {sum(HEXAGONS['중앙'])} |
| 하좌 | {' + '.join(map(str, HEXAGONS['하좌']))} | {sum(HEXAGONS['하좌'])} |
| 하우 | {' + '.join(map(str, HEXAGONS['하우']))} | {sum(HEXAGONS['하우'])} |

## 3. 오행(五行) 분석

`n mod 5`에 따른 분류 (0은 5로 처리):

| 오행 | 잉여 | 수들 | 합 |
|---|---|---|---|
| 수 | 1 | {', '.join(map(str, [n for n in range(1, 21) if n % 5 == 1]))} | {sum([n for n in range(1, 21) if n % 5 == 1])} |
| 화 | 2 | {', '.join(map(str, [n for n in range(1, 21) if n % 5 == 2]))} | {sum([n for n in range(1, 21) if n % 5 == 2])} |
| 목 | 3 | {', '.join(map(str, [n for n in range(1, 21) if n % 5 == 3]))} | {sum([n for n in range(1, 21) if n % 5 == 3])} |
| 금 | 4 | {', '.join(map(str, [n for n in range(1, 21) if n % 5 == 4]))} | {sum([n for n in range(1, 21) if n % 5 == 4])} |
| 토 | 0 | {', '.join(map(str, [n for n in range(1, 21) if n % 5 == 0]))} | {sum([n for n in range(1, 21) if n % 5 == 0])} |

오행별 합은 34, 38, 42, 46, 50로 등차 4를 이룹니다.

## 4. 그래프 이론적 지표

- **차수 시퀀스**: {deg_seq_full}
- **최대 차수**: {max(deg_seq_full)}
- **최소 차수**: {min(deg_seq_full)}
- **Betweenness Centrality 상위 5개**:
{chr(10).join(f"  - {n}({wuxing_of(n)}): {v:.3f}" for n, v in sorted(betw_full.items(), key=lambda x: -x[1])[:5])}

## 5. 스펙트럼

- λ_max = {max(eigenvalues):.4f}
- λ_min = {min(eigenvalues):.4f}
- 고유값 범위 = {max(eigenvalues) - min(eigenvalues):.4f}

## 6. 사이클 구조

각 육각형은 6-Cycle을 형성합니다.

{chr(10).join(f"- **{name}**: {' → '.join(map(str, cycle + [cycle[0]]))}" for name, cycle in hex_cycles.items())}

## 7. 위치 패턴

- **공유 정점** (2개 이상의 육각형에 속함): {sorted(SHARED_VALUES)}
- **고유 정점** (한 육각형에만 속함): {sorted(UNIQUE_VALUES)}

공유 정점은 육각형 간의 결합부 역할을 하며, 그래프의 연결성과 중심성에 큰 영향을 줍니다.

## 8. 오행 엣지 분포

| 분류 | 개수 |
|---|---|
{chr(10).join(f"| {key} | {cnt} |" for key, cnt in wx_edge_counts.items())}

## 9. 일반화

mod 5 잉여 클래스 합의 등차수열:

| M0 | 오행 | 클래스 합 |
|---|---|---|
{chr(10).join(f"| {m0} | {RESIDUE_STYLE[m0 % 5]['name']} | {total} |" for m0, total in FAMILY_RESIDUE)}

## 10. 생성된 산출물

- `01_original_graph.png`
- `02_wuxing_decomposition.png`
- `03_adjacency_spectrum.png`
- `04_cycle_analysis.png`
- `05_centrality_invariants.png`
- `06_wuxing_relations.png`
- `07_local_extensions.png`
- `08_position_patterns.png`
- `jisu_yong_yukdo.png` / `jisu_yong_yukdo.svg`
- `analysis_report.md`
- `blog.md`
"""

force = "--force" in sys.argv

report_path = Path(f"{OUTPUT_DIR}/analysis_report.md")
if force or not report_path.exists():
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_md)
    print("[저장] analysis_report.md")
else:
    print("[SKIP] analysis_report.md already exists (use --force to regenerate)")

blog_md = f"""# 지수용육도(地數用六圖) 심층 해부

지수용육도는 《구수력》 계열의 전통 수학 퍼즐로, 1부터 20까지의 수를 5개 육각형에 배치하여 각 육각형의 합이 63이 되도록 한 도식입니다.

## 핵심 구조

- 5개 육각형: 상좌, 상우, 중앙, 하좌, 하우
- 각 육각형 6정점, 합 63
- 전체 정점 20개, 간선 {G_full.number_of_edges()}개
- 인접 육각형은 정점·간선을 공유

## 오행 분류

`n mod 5`로 수·화·목·금·토 5개 클래스로 나누면 각 클래스에 정확히 4개씩 들어갑니다.
오행별 합 34, 38, 42, 46, 50은 등차 4의 수열을 이룹니다.

## 그래프로 보기

육각형의 변을 그래프의 엣지로 보면 지수용육도는 20개 노드, {G_full.number_of_edges()}개 엣지의 평면 그래프가 됩니다.
각 육각형은 6-Cycle이며, 공유 정점을 통해 5개의 사이클이 서로 얽여 있습니다.

## 합 불변량

모든 육각형의 합이 63으로 동일하다는 것은 이 퍼즐의 핵심 규칙입니다.
5개 육각형을 중복 계수까지 합치면 `63 × 5 = 315`가 되며, 이는 1–20의 총합 210보다 105만큼 큽니다.
이 105는 공유 정점들이 중복으로 더해진 결과입니다.

## 시각화

동일 디렉토리의 8개 이미지(`01_original_graph.png` ~ `08_position_patterns.png`)를 통해
원본 구조부터 오행 분해, 스펙트럼, 사이클, 중심성, 상생상극, 확장, 위치 패턴까지
현대 수학적 관점에서 심층적으로 살펴볼 수 있습니다.
"""

blog_path = Path(f"{OUTPUT_DIR}/blog.md")
if force or not blog_path.exists():
    with open(blog_path, "w", encoding="utf-8") as f:
        f.write(blog_md)
    print("[저장] blog.md")
else:
    print("[SKIP] blog.md already exists (use --force to regenerate)")

print("\n" + "=" * 60)
print("모든 이미지 및 보고서 생성 완료!")
print(f"출력 디렉토리: {OUTPUT_DIR}/")
print("=" * 60)
