#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八子各得 (팔자각득) — 현대 그래프·조합론적 심층 분석

《구수력(九數略)》계열 도상 중 팔자각득(八子各得)을 현대 수학 언어로 재해석.
분석 대상: 1부터 40까지의 수를 5개 궁(宮)에 8자씩 배치한 교차 구조.
"""

import os
from collections import Counter
from itertools import combinations

import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx
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

PALACES = {
    "상궁": [
        [39, 7, 34],
        [12, None, 19],
        [24, 2, 27],
    ],
    "좌궁": [
        [33, 18, 28],
        [8, None, 3],
        [38, 13, 23],
    ],
    "중궁": [
        [30, 5, 21],
        [16, None, 15],
        [31, 10, 36],
    ],
    "우궁": [
        [22, 14, 37],
        [4, None, 9],
        [29, 17, 32],
    ],
    "하궁": [
        [26, 1, 25],
        [20, None, 11],
        [35, 6, 40],
    ],
}

# 십자 배치에서 각 궁의 원점(좌하단 기준).
PALACE_ORIGINS = {
    "상궁": (3, 6),
    "좌궁": (0, 3),
    "중궁": (3, 3),
    "우궁": (6, 3),
    "하궁": (3, 0),
}

# 노트에 기록된 mod 5 잉여 클래스 색상.
RESIDUE_STYLE = {
    1: {"face": "#D9D9D9", "edge": "#555555", "name": "수", "en": "Water"},
    2: {"face": "#F3C2C2", "edge": "#A33A3A", "name": "화", "en": "Fire"},
    3: {"face": "#C7D8F5", "edge": "#315C9A", "name": "목", "en": "Wood"},
    4: {"face": "#BFBFBF", "edge": "#222222", "name": "금", "en": "Metal"},
    0: {"face": "#F3D58A", "edge": "#A67C00", "name": "토", "en": "Earth"},
}

# 간결한 오행 색상 (서브그래프 분해 등에 사용).
WUXING_COLOR = {
    "수": "#4488CC",
    "화": "#CC4444",
    "목": "#44AA44",
    "금": "#888888",
    "토": "#CC9944",
}


def wuxing_of(n: int) -> str:
    """1 기반 mod 5 잉여에 따른 오행."""
    r = n % 5
    return RESIDUE_STYLE[r]["name"]


def residue_1based(n: int) -> int:
    r = n % 5
    return 5 if r == 0 else r


def build_positions() -> dict[int, tuple[float, float]]:
    positions: dict[int, tuple[float, float]] = {}
    for palace_name, grid in PALACES.items():
        origin_x, origin_y = PALACE_ORIGINS[palace_name]
        for row_index, row in enumerate(grid):
            for col_index, value in enumerate(row):
                if value is None:
                    continue
                x = origin_x + col_index
                y = origin_y + (2 - row_index)
                positions[value] = (x, y)
    return positions


POSITIONS = build_positions()


def palace_cells(palace_name: str) -> list[tuple[int, int, int]]:
    """궁 내 (값, 행, 열) 목록. 행/열은 0 기준."""
    cells = []
    grid = PALACES[palace_name]
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value is not None:
                cells.append((value, r, c))
    return cells


def cell_role(palace_name: str, row: int, col: int) -> str:
    """3×3 격자에서 중심을 제외한 8자의 위치 역할."""
    if (row, col) in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        return "corner"
    return "edge"


# ============================================================
# 2. 그래프 구성
# ============================================================

INTRA_EDGES: list[tuple[int, int]] = []
FULL_EDGES: list[tuple[int, int]] = []

# 같은 궁 내부 인접 엣지.
for palace_name, grid in PALACES.items():
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value is None:
                continue
            # 우측 이웃
            if c + 1 < 3:
                right = grid[r][c + 1]
                if right is not None:
                    INTRA_EDGES.append(tuple(sorted((value, right))))  # type: ignore[arg-type]
            # 하측 이웃
            if r + 1 < 3:
                down = grid[r + 1][c]
                if down is not None:
                    INTRA_EDGES.append(tuple(sorted((value, down))))  # type: ignore[arg-type]

# 전체 격자 인접 엣지 (궁 경계를 넘어섬).
pos_to_value = {pos: value for value, pos in POSITIONS.items()}
for value, (x, y) in POSITIONS.items():
    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        neighbor_pos = (x + dx, y + dy)
        if neighbor_pos in pos_to_value:
            neighbor = pos_to_value[neighbor_pos]
            if neighbor > value:
                FULL_EDGES.append((value, neighbor))

G_intra = nx.Graph()
G_intra.add_edges_from(INTRA_EDGES)
for n in range(1, 41):
    G_intra.add_node(n)
    G_intra.nodes[n]["wuxing"] = wuxing_of(n)

G_full = nx.Graph()
G_full.add_edges_from(FULL_EDGES)
for n in range(1, 41):
    G_full.add_node(n)
    G_full.nodes[n]["wuxing"] = wuxing_of(n)

# ============================================================
# 3. 조합론·그래프 이론 분석
# ============================================================


def palace_values(palace_name: str) -> list[int]:
    return [v for v, _, _ in palace_cells(palace_name)]


def palace_values_from_grid(grid: list[list[int | None]]) -> list[int]:
    return [v for row in grid for v in row if v is not None]


# 각 궁의 8-사이클 순서(시계/반시계 무관).
PALACE_CYCLES: dict[str, list[int]] = {}
for palace_name in PALACES:
    cycle = list(nx.cycle_basis(G_intra.subgraph(palace_values(palace_name)))[0])
    PALACE_CYCLES[palace_name] = cycle


def validate():
    all_values = [v for vals in PALACES.values() for v in palace_values_from_grid(vals)]
    assert sorted(all_values) == list(range(1, 41)), "1~40이 각각 한 번씩이어야 함"
    assert sum(all_values) == 820, "전체 합은 820"
    for palace_name, grid in PALACES.items():
        vals = palace_values_from_grid(grid)
        assert len(vals) == 8, f"{palace_name}은 8자"
        assert sum(vals) == 164, f"{palace_name} 합은 164"


validate()

print("=" * 60)
print("八子各得 (팔자각득) 현대 그래프·조합론 분석")
print("=" * 60)
print(f"노드 수: {G_full.number_of_nodes()}")
print(f"엣지 수(궁 내부만): {G_intra.number_of_edges()}")
print(f"엣지 수(전체 격자): {G_full.number_of_edges()}")
print(f"연결 성분(궁 내부만): {nx.number_connected_components(G_intra)}")
print(f"연결 성분(전체 격자): {nx.number_connected_components(G_full)}")

deg_seq_intra = sorted([d for _, d in G_intra.degree()], reverse=True)
deg_seq_full = sorted([d for _, d in G_full.degree()], reverse=True)
print(f"차수 시퀀스(궁 내부만): {deg_seq_intra}")
print(f"차수 시퀀스(전체 격자): {deg_seq_full}")

print("\n각 궁의 8-사이클 및 합:")
for palace_name, cycle in PALACE_CYCLES.items():
    print(f"  {palace_name}: {' → '.join(map(str, cycle))} (합={sum(cycle)})")

print("\n오행별 수 합:")
for r in [1, 2, 3, 4, 5]:
    nodes = [n for n in range(1, 41) if residue_1based(n) == r]
    wx = RESIDUE_STYLE[r % 5]["name"]
    print(f"  {wx}({r}): 합={sum(nodes)}, 수들={nodes}")

print("\n궁별 오행 분포:")
for palace_name in PALACES:
    vals = palace_values(palace_name)
    counts = Counter(wuxing_of(v) for v in vals)
    print(f"  {palace_name}: {dict(counts)}")

betw_full = nx.betweenness_centrality(G_full)
print("\nBetweenness Centrality (Top 10):")
for n, v in sorted(betw_full.items(), key=lambda x: -x[1])[:10]:
    print(f"  {n}({wuxing_of(n)}): {v:.3f}")

try:
    girth = min(len(c) for c in nx.cycle_basis(G_full))
    print(f"\nGirth (최소 사이클 길이): {girth}")
except Exception:
    girth = None

# 오행 엣지 분류 출력
wx_edge_counts = {}
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

# ============================================================
# 4. 위치 기반 분석 (모서리 vs 변의 중점)
# ============================================================

CORNER_SUMS: dict[str, int] = {}
EDGE_SUMS: dict[str, int] = {}
for palace_name in PALACES:
    corner_vals = []
    edge_vals = []
    for value, r, c in palace_cells(palace_name):
        if cell_role(palace_name, r, c) == "corner":
            corner_vals.append(value)
        else:
            edge_vals.append(value)
    CORNER_SUMS[palace_name] = sum(corner_vals)
    EDGE_SUMS[palace_name] = sum(edge_vals)

print("\n궁별 모서리/변의 중점 합:")
for palace_name in PALACES:
    print(
        f"  {palace_name}: 모서리={CORNER_SUMS[palace_name]}, "
        f"변의 중점={EDGE_SUMS[palace_name]}"
    )

# ============================================================
# 5. 일반화 가족
# ============================================================

FAMILY = [(m0, 148 + (m0 - 1) * 8) for m0 in range(1, 6)]
print("\nM0 일반화 가족:")
for m0, total in FAMILY:
    wx = RESIDUE_STYLE[m0 % 5]["name"]
    print(f"  M0={m0}({wx}): 궁 합={total}")

# ============================================================
# 6. 시각화
# ============================================================

PALACE_COLORS = {
    "상궁": "#CC4444",
    "좌궁": "#4488CC",
    "중궁": "#44AA44",
    "우궁": "#CC9944",
    "하궁": "#888888",
}


def draw_palace_boundaries(ax):
    for palace_name, origin in PALACE_ORIGINS.items():
        ox, oy = origin
        rect = plt.Rectangle(
            (ox - 0.52, oy - 0.52),
            3.04,
            3.04,
            fill=False,
            edgecolor="#777777",
            linewidth=1.5,
            linestyle=(0, (4, 4)),
            zorder=0,
        )
        ax.add_patch(rect)
        ax.text(
            ox + 1.0,
            oy + 2.7,
            f"{palace_name} · Σ=164",
            ha="center",
            va="bottom",
            fontsize=10,
            color="#333333",
        )


def draw_nodes(ax, highlight_palace=None, highlight_values=None, node_size=1000):
    for value, (x, y) in POSITIONS.items():
        palace = value_to_palace(value)
        if highlight_palace and palace != highlight_palace:
            continue
        r = value % 5
        style = RESIDUE_STYLE[r]
        color = style["face"]
        edge = style["edge"]
        lw = 2.5
        if highlight_values and value in highlight_values:
            edge = "red"
            lw = 3.5
        ax.add_patch(
            plt.Circle(
                (x, y),
                0.32,
                facecolor=color,
                edgecolor=edge,
                linewidth=lw,
                zorder=2,
            )
        )
        ax.text(
            x,
            y,
            str(value),
            ha="center",
            va="center",
            fontsize=10,
            fontweight="bold",
            zorder=3,
        )


def value_to_palace(value: int) -> str:
    for palace_name, grid in PALACES.items():
        for row in grid:
            if value in row:
                return palace_name
    raise ValueError(value)


# --- 01: 원본 그래프 ---
fig, ax = plt.subplots(figsize=(12, 12))
draw_palace_boundaries(ax)
for u, v in FULL_EDGES:
    x1, y1 = POSITIONS[u]
    x2, y2 = POSITIONS[v]
    palace_u = value_to_palace(u)
    palace_v = value_to_palace(v)
    if palace_u == palace_v:
        ax.plot([x1, x2], [y1, y2], color=PALACE_COLORS[palace_u], linewidth=2.5, alpha=0.7, zorder=1)
    else:
        ax.plot([x1, x2], [y1, y2], color="#333333", linewidth=1.8, alpha=0.5, zorder=1)

# 중심 공백 표시
for palace_name, origin in PALACE_ORIGINS.items():
    ox, oy = origin
    ax.add_patch(
        plt.Circle(
            (ox + 1, oy + 1),
            0.18,
            facecolor="white",
            edgecolor="#999999",
            linewidth=1.5,
            linestyle="--",
            zorder=1,
        )
    )

draw_nodes(ax)
ax.set_title(
    "八子各得 (팔자각득) - 원본 교차 구조\n5궁 · 8자 · 각 궁 합 164 · 전체 합 820",
    fontsize=16,
    fontweight="bold",
)
ax.set_xlim(-0.8, 8.8)
ax.set_ylim(-0.8, 8.8)
ax.set_aspect("equal")
ax.axis("off")
legend_elements = [
    mpatches.Patch(facecolor=WUXING_COLOR[wx], edgecolor="black", label=f"{wx}")
    for wx in ["수", "화", "목", "금", "토"]
]
legend_elements.append(
    Line2D(
        [0],
        [0],
        marker="o",
        color="w",
        markeredgecolor="#999999",
        markerfacecolor="white",
        markersize=8,
        label="중심 공백",
    )
)
ax.legend(handles=legend_elements, loc="lower right", fontsize=10, framealpha=0.9)
save_fig("01_original_graph.png")
plt.close()

# --- 02: 오행별 서브그래프 분해 ---
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()
ax = axes[0]
draw_palace_boundaries(ax)
for u, v in FULL_EDGES:
    x1, y1 = POSITIONS[u]
    x2, y2 = POSITIONS[v]
    ax.plot([x1, x2], [y1, y2], color="#CCCCCC", linewidth=1, alpha=0.5, zorder=0)
draw_nodes(ax)
ax.set_title("전체 그래프", fontsize=13, fontweight="bold")
ax.set_xlim(-0.8, 8.8)
ax.set_ylim(-0.8, 8.8)
ax.set_aspect("equal")
ax.axis("off")

for idx, wx in enumerate(["수", "화", "목", "금", "토"]):
    ax = axes[idx + 1]
    draw_palace_boundaries(ax)
    wx_nodes = [n for n in range(1, 41) if wuxing_of(n) == wx]
    other_nodes = [n for n in range(1, 41) if n not in wx_nodes]

    # 배경 엣지
    for u, v in FULL_EDGES:
        x1, y1 = POSITIONS[u]
        x2, y2 = POSITIONS[v]
        ax.plot([x1, x2], [y1, y2], color="#EEEEEE", linewidth=1, alpha=0.4, zorder=0)

    # 비오행 노드는 흐리게
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

    # 오행 노드 강조
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
    ax.set_xlim(-0.8, 8.8)
    ax.set_ylim(-0.8, 8.8)
    ax.set_aspect("equal")
    ax.axis("off")

plt.suptitle("오행(五行)별 서브그래프 분해", fontsize=16, fontweight="bold", y=1.02)
plt.tight_layout()
save_fig("02_wuxing_decomposition.png")
plt.close()

# --- 03: 인접 행렬 + 스펙트럼 ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
adj = nx.adjacency_matrix(G_full, nodelist=sorted(G_full.nodes())).todense()
im = ax.imshow(adj, cmap="YlOrRd", interpolation="nearest")
ax.set_xticks(range(40))
ax.set_yticks(range(40))
ax.set_xticklabels(sorted(G_full.nodes()), fontsize=7)
ax.set_yticklabels(sorted(G_full.nodes()), fontsize=7)
# 오행별 경계선
wx_sorted = [wuxing_of(n) for n in sorted(G_full.nodes())]
boundaries = [i - 0.5 for i in range(1, 40) if wx_sorted[i] != wx_sorted[i - 1]]
for b in boundaries:
    ax.axhline(y=b, color="blue", linewidth=1.5, alpha=0.7)
    ax.axvline(x=b, color="blue", linewidth=1.5, alpha=0.7)
plt.colorbar(im, ax=ax, shrink=0.8)
ax.set_title("Adjacency Matrix (전체 격자)", fontsize=13, fontweight="bold")

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
draw_palace_boundaries(ax)
for u, v in FULL_EDGES:
    x1, y1 = POSITIONS[u]
    x2, y2 = POSITIONS[v]
    palace_u = value_to_palace(u)
    palace_v = value_to_palace(v)
    if palace_u == palace_v:
        ax.plot([x1, x2], [y1, y2], color=PALACE_COLORS[palace_u], linewidth=3, alpha=0.8, zorder=1)
draw_nodes(ax)
ax.set_title("5개 궁의 내부 8-Cycle", fontsize=13, fontweight="bold")
ax.set_xlim(-0.8, 8.8)
ax.set_ylim(-0.8, 8.8)
ax.set_aspect("equal")
ax.axis("off")

ax = axes[0, 1]
# 궁 간 연결 엣지만 강조
for u, v in FULL_EDGES:
    x1, y1 = POSITIONS[u]
    x2, y2 = POSITIONS[v]
    palace_u = value_to_palace(u)
    palace_v = value_to_palace(v)
    if palace_u != palace_v:
        ax.plot([x1, x2], [y1, y2], color="#333333", linewidth=2.5, alpha=0.9, zorder=1)
    else:
        ax.plot([x1, x2], [y1, y2], color="#DDDDDD", linewidth=1, alpha=0.5, zorder=0)
# 중궁 노드 강조
for n in palace_values("중궁"):
    x, y = POSITIONS[n]
    ax.add_patch(
        plt.Circle(
            (x, y),
            0.34,
            facecolor="#44AA44",
            edgecolor="red",
            linewidth=2.5,
            zorder=2,
        )
    )
    ax.text(x, y, str(n), ha="center", va="center", fontsize=10, fontweight="bold", zorder=3)
# 다른 노드
for n in range(1, 41):
    if n in palace_values("중궁"):
        continue
    x, y = POSITIONS[n]
    ax.add_patch(
        plt.Circle(
            (x, y),
            0.28,
            facecolor="white",
            edgecolor="#999999",
            linewidth=1.5,
            zorder=1,
        )
    )
    ax.text(x, y, str(n), ha="center", va="center", fontsize=9, zorder=2)
ax.set_title("중궁을 중심으로 한 4방향 연결\n(궁 간 경계 엣지 12개)", fontsize=13, fontweight="bold")
ax.set_xlim(-0.8, 8.8)
ax.set_ylim(-0.8, 8.8)
ax.set_aspect("equal")
ax.axis("off")

ax = axes[1, 0]
palace_names = list(PALACES.keys())
palace_sums = [sum(palace_values(p)) for p in palace_names]
palace_bar_colors = [PALACE_COLORS[p] for p in palace_names]
ax.bar(palace_names, palace_sums, color=palace_bar_colors, edgecolor="black", linewidth=1.5)
ax.axhline(y=164, color="red", linestyle="--", linewidth=2)
ax.set_title("각 궁의 8자 합", fontsize=13, fontweight="bold")
for bar, val in zip(ax.patches, palace_sums):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        str(val),
        ha="center",
        fontsize=12,
        fontweight="bold",
    )

ax = axes[1, 1]
# 각 궁의 8-cycle 누적 합 시각화
palace_name = "중궁"
cycle = PALACE_CYCLES[palace_name]
cumsum = np.cumsum([n for n in cycle])
ax.plot(range(8), cumsum, "o-", color=PALACE_COLORS[palace_name], linewidth=2.5, markersize=8, markeredgecolor="black")
ax.fill_between(range(8), cumsum, alpha=0.2, color=PALACE_COLORS[palace_name])
ax.set_xticks(range(8))
ax.set_xticklabels([str(n) for n in cycle], fontsize=9)
ax.set_title(f"중궁 8-Cycle 누적 합 (Total={sum(cycle)})", fontsize=13, fontweight="bold")
ax.grid(True, alpha=0.3)
ax.axhline(y=sum(cycle) / 2, color="blue", linestyle="--", alpha=0.5)

plt.tight_layout()
save_fig("04_cycle_analysis.png")
plt.close()

# --- 05: 중심성 + 합 불변량 ---
fig, axes = plt.subplots(2, 2, figsize=(16, 14))

ax = axes[0, 0]
degrees = dict(G_full.degree())
nodes_sorted = sorted(G_full.nodes(), key=lambda n: degrees[n], reverse=True)
colors_sorted = [WUXING_COLOR[wuxing_of(n)] for n in nodes_sorted]
ax.bar(range(40), [degrees[n] for n in nodes_sorted], color=colors_sorted, edgecolor="black")
ax.set_xticks(range(40))
ax.set_xticklabels([str(n) for n in nodes_sorted], fontsize=8)
ax.set_title("Degree (전체 격자)", fontsize=12, fontweight="bold")
ax.set_ylabel("Degree", fontsize=10)

ax = axes[0, 1]
betw_sorted = sorted(G_full.nodes(), key=lambda n: betw_full[n], reverse=True)
colors_b = [WUXING_COLOR[wuxing_of(n)] for n in betw_sorted]
ax.bar(range(40), [betw_full[n] for n in betw_sorted], color=colors_b, edgecolor="black")
ax.set_xticks(range(40))
ax.set_xticklabels([str(n) for n in betw_sorted], fontsize=8)
ax.set_title("Betweenness Centrality", fontsize=12, fontweight="bold")
ax.set_ylabel("Centrality", fontsize=10)

ax = axes[1, 0]
wx_sums = {wx: sum([n for n in range(1, 41) if wuxing_of(n) == wx]) for wx in ["수", "화", "목", "금", "토"]}
wx_names = list(wx_sums.keys())
wx_vals = list(wx_sums.values())
wx_colors_bar = [WUXING_COLOR[w] for w in wx_names]
ax.bar(wx_names, wx_vals, color=wx_colors_bar, edgecolor="black", linewidth=1.5)
ax.set_title("오행별 수 합 (148, 156, 164, 172, 180)", fontsize=12, fontweight="bold")
for bar, val in zip(ax.patches, wx_vals):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 2,
        str(val),
        ha="center",
        fontsize=12,
        fontweight="bold",
    )
ax.plot(range(5), wx_vals, "o--", color="black", alpha=0.5, linewidth=2)

ax = axes[1, 1]
components = {
    "상궁": sum(palace_values("상궁")),
    "좌궁": sum(palace_values("좌궁")),
    "중궁": sum(palace_values("중궁")),
    "우궁": sum(palace_values("우궁")),
    "하궁": sum(palace_values("하궁")),
    "전체": sum(range(1, 41)),
}
ax.bar(
    list(components.keys()),
    list(components.values()),
    color=[PALACE_COLORS[k] for k in list(components.keys())[:-1]] + ["#333333"],
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
wx_edge_counts = {}
for u, v in G_full.edges():
    wu, wv = wuxing_of(u), wuxing_of(v)
    if wu == wv:
        key = f"{wu}동질"
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

# 왼쪽: M0 가족
ax = axes[0]
m0_labels = [f"M0={m0}" for m0, _ in FAMILY]
m0_values = [total for _, total in FAMILY]
m0_colors = [WUXING_COLOR[RESIDUE_STYLE[m0 % 5]["name"]] for m0, _ in FAMILY]
ax.bar(m0_labels, m0_values, color=m0_colors, edgecolor="black", linewidth=1.5)
ax.set_title("일반화 가족: 궁 합의 등차수열\nM(n+1) = M(n) + 8", fontsize=13, fontweight="bold")
for bar, val in zip(ax.patches, m0_values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 2,
        str(val),
        ha="center",
        fontsize=12,
        fontweight="bold",
    )
ax.plot(range(5), m0_values, "o--", color="black", alpha=0.5, linewidth=2)
ax.set_ylabel("Palace Sum", fontsize=10)

# 오른쪽: 40→80→120... 배수 확장
ax = axes[1]
n_layers = 3
theta = np.linspace(0, 2 * np.pi, n_layers + 1)[:-1]
for i, t in enumerate(theta):
    r = 2.5 + i * 1.5
    circle = plt.Circle((0, 0), r, fill=False, color=["#CC4444", "#4488CC", "#44AA44"][i], linewidth=2, linestyle="--")
    ax.add_patch(circle)
    ax.text(r * np.cos(np.pi / 4), r * np.sin(np.pi / 4), f"{40 * (i + 1)}자", fontsize=10, fontweight="bold")
ax.add_patch(plt.Circle((0, 0), 0.5, facecolor="#CC9944", edgecolor="black", linewidth=2))
ax.text(0, 0, "CORE\n40", ha="center", va="center", fontsize=10, fontweight="bold")
ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("동심원 확장: 40k자 구조", fontsize=13, fontweight="bold")

plt.tight_layout()
save_fig("07_local_extensions.png")
plt.close()

# --- 08: 위치 패턴 (모서리 vs 변의 중점) ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

ax = axes[0]
palace_names = list(PALACES.keys())
corner_vals_list = [CORNER_SUMS[p] for p in palace_names]
edge_vals_list = [EDGE_SUMS[p] for p in palace_names]
x = np.arange(len(palace_names))
width = 0.35
ax.bar(x - width / 2, corner_vals_list, width, label="모서리 4자", color="#CC4444", edgecolor="black")
ax.bar(x + width / 2, edge_vals_list, width, label="변의 중점 4자", color="#4488CC", edgecolor="black")
ax.set_xticks(x)
ax.set_xticklabels(palace_names)
ax.set_title("궁별 모서리/변의 중점 합", fontsize=13, fontweight="bold")
ax.legend()
ax.set_ylabel("Sum", fontsize=10)

ax = axes[1]
# 궁별 평균 위치와 합의 관계
palace_centers = {
    "상궁": (4, 7),
    "좌궁": (1, 4),
    "중궁": (4, 4),
    "우궁": (7, 4),
    "하궁": (4, 1),
}
for palace_name in PALACES:
    cx, cy = palace_centers[palace_name]
    total = sum(palace_values(palace_name))
    ax.scatter(cx, cy, s=total * 3, c=PALACE_COLORS[palace_name], edgecolors="black", linewidths=2, alpha=0.7)
    ax.text(cx, cy, f"{palace_name}\n{total}", ha="center", va="center", fontsize=10, fontweight="bold")
# 십자 연결
for a, b in [("상궁", "중궁"), ("좌궁", "중궁"), ("중궁", "우궁"), ("중궁", "하궁")]:
    x1, y1 = palace_centers[a]
    x2, y2 = palace_centers[b]
    ax.plot([x1, x2], [y1, y2], "k-", linewidth=2, alpha=0.3)
ax.set_xlim(-1, 9)
ax.set_ylim(-1, 9)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("십자 배치에서의 합 불변량", fontsize=13, fontweight="bold")

plt.tight_layout()
save_fig("08_position_patterns.png")
plt.close()

print("\n" + "=" * 60)
print("모든 이미지 생성 완료!")
print(f"출력 디렉토리: {OUTPUT_DIR}/")
print("=" * 60)
