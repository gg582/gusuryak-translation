#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
九子各得 (구자각득) — 현대 그래프·조합론적 심층 분석

《구수력(九數略)》계열 도상 중 구자각득(九子各得)을 현대 수학 언어로 재해석.
분석 대상: 1부터 45까지의 수를 5개 궁(宮)에 9자씩 배치한 교차 구조.
"""

import os
from collections import Counter

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
        [12, 44, 9],
        [19, 21, 29],
        [37, 2, 34],
    ],
    "좌궁": [
        [13, 43, 8],
        [18, 25, 26],
        [38, 3, 33],
    ],
    "중궁": [
        [15, 41, 6],
        [16, 23, 30],
        [40, 5, 31],
    ],
    "우궁": [
        [14, 42, 7],
        [17, 24, 28],
        [39, 4, 32],
    ],
    "하궁": [
        [11, 45, 10],
        [20, 22, 27],
        [36, 1, 35],
    ],
}

PALACE_ORIGINS = {
    "상궁": (3, 6),
    "좌궁": (0, 3),
    "중궁": (3, 3),
    "우궁": (6, 3),
    "하궁": (3, 0),
}

RESIDUE_STYLE = {
    1: {"face": "#E5E5E5", "edge": "#444444", "name": "수", "en": "Water"},
    2: {"face": "#F6D0D0", "edge": "#B54141", "name": "화", "en": "Fire"},
    3: {"face": "#D5E3FA", "edge": "#3D6DB3", "name": "목", "en": "Wood"},
    4: {"face": "#D7D7D7", "edge": "#1F1F1F", "name": "금", "en": "Metal"},
    0: {"face": "#F7E3A0", "edge": "#B58A00", "name": "토", "en": "Earth"},
}

WUXING_COLOR = {
    "수": "#4488CC",
    "화": "#CC4444",
    "목": "#44AA44",
    "금": "#888888",
    "토": "#CC9944",
}


def wuxing_of(n: int) -> str:
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
                x = origin_x + col_index
                y = origin_y + (2 - row_index)
                positions[value] = (x, y)
    return positions


POSITIONS = build_positions()


def palace_values(palace_name: str) -> list[int]:
    return [v for row in PALACES[palace_name] for v in row]


def palace_cells(palace_name: str) -> list[tuple[int, int, int]]:
    """궁 내 (값, 행, 열) 목록."""
    cells = []
    for r, row in enumerate(PALACES[palace_name]):
        for c, value in enumerate(row):
            cells.append((value, r, c))
    return cells


def cell_role(row: int, col: int) -> str:
    if (row, col) == (1, 1):
        return "center"
    if (row, col) in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        return "corner"
    return "edge"


# ============================================================
# 2. 그래프 구성
# ============================================================

INTRA_EDGES: list[tuple[int, int]] = []
FULL_EDGES: list[tuple[int, int]] = []

# 같은 궁 내부 인접 엣지 (3×3 격자).
for palace_name, grid in PALACES.items():
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if c + 1 < 3:
                right = grid[r][c + 1]
                INTRA_EDGES.append(tuple(sorted((value, right))))
            if r + 1 < 3:
                down = grid[r + 1][c]
                INTRA_EDGES.append(tuple(sorted((value, down))))

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
for n in range(1, 46):
    G_intra.add_node(n)
    G_intra.nodes[n]["wuxing"] = wuxing_of(n)

G_full = nx.Graph()
G_full.add_edges_from(FULL_EDGES)
for n in range(1, 46):
    G_full.add_node(n)
    G_full.nodes[n]["wuxing"] = wuxing_of(n)


def value_to_palace(value: int) -> str:
    for palace_name, grid in PALACES.items():
        for row in grid:
            if value in row:
                return palace_name
    raise ValueError(value)


# ============================================================
# 3. 조합론·그래프 이론 분석
# ============================================================

def validate():
    all_values = [v for grid in PALACES.values() for row in grid for v in row]
    assert sorted(all_values) == list(range(1, 46)), "1~45가 각각 한 번씩이어야 함"
    assert sum(all_values) == 1035, "전체 합은 1035"
    for palace_name, grid in PALACES.items():
        vals = [v for row in grid for v in row]
        assert len(vals) == 9, f"{palace_name}은 9자"
        assert sum(vals) == 207, f"{palace_name} 합은 207"


validate()

print("=" * 60)
print("九子各得 (구자각득) 현대 그래프·조합론 분석")
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

print("\n오행별 수 합:")
for r in [1, 2, 3, 4, 5]:
    nodes = [n for n in range(1, 46) if residue_1based(n) == r]
    wx = RESIDUE_STYLE[r % 5]["name"]
    print(f"  {wx}({r}): 합={sum(nodes)}, 수들={nodes}")

print("\n궁별 오행 분포:")
for palace_name in PALACES:
    vals = palace_values(palace_name)
    counts = Counter(wuxing_of(v) for v in vals)
    print(f"  {palace_name}: {dict(counts)}")

print("\n궁별 중심값:")
for palace_name in PALACES:
    center = [v for v, r, c in palace_cells(palace_name) if cell_role(r, c) == "center"][0]
    print(f"  {palace_name}: 중심={center}({wuxing_of(center)})")

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
# 4. 위치 기반 분석 (모서리 / 변의 중점 / 중심)
# ============================================================

CORNER_SUMS: dict[str, int] = {}
EDGE_SUMS: dict[str, int] = {}
CENTER_VALUES: dict[str, int] = {}
for palace_name in PALACES:
    corner_vals = []
    edge_vals = []
    center_val = None
    for value, r, c in palace_cells(palace_name):
        role = cell_role(r, c)
        if role == "corner":
            corner_vals.append(value)
        elif role == "edge":
            edge_vals.append(value)
        else:
            center_val = value
    CORNER_SUMS[palace_name] = sum(corner_vals)
    EDGE_SUMS[palace_name] = sum(edge_vals)
    CENTER_VALUES[palace_name] = center_val  # type: ignore[assignment]

print("\n궁별 위치별 합:")
for palace_name in PALACES:
    print(
        f"  {palace_name}: 모서리={CORNER_SUMS[palace_name]}, "
        f"변의 중점={EDGE_SUMS[palace_name]}, 중심={CENTER_VALUES[palace_name]}"
    )

# ============================================================
# 5. 일반화 가족
# ============================================================

FAMILY = [(m0, 189 + (m0 - 1) * 9) for m0 in range(1, 6)]
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
            f"{palace_name} · Σ=207",
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
draw_nodes(ax)
ax.set_title(
    "九子各得 (구자각득) - 원본 교차 구조\n5궁 · 9자 · 각 궁 합 207 · 전체 합 1035",
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
    wx_nodes = [n for n in range(1, 46) if wuxing_of(n) == wx]
    other_nodes = [n for n in range(1, 46) if n not in wx_nodes]

    for u, v in FULL_EDGES:
        x1, y1 = POSITIONS[u]
        x2, y2 = POSITIONS[v]
        ax.plot([x1, x2], [y1, y2], color="#EEEEEE", linewidth=1, alpha=0.4, zorder=0)

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
ax.set_xticks(range(45))
ax.set_yticks(range(45))
ax.set_xticklabels(sorted(G_full.nodes()), fontsize=6)
ax.set_yticklabels(sorted(G_full.nodes()), fontsize=6)
wx_sorted = [wuxing_of(n) for n in sorted(G_full.nodes())]
boundaries = [i - 0.5 for i in range(1, 45) if wx_sorted[i] != wx_sorted[i - 1]]
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
ax.set_title("5개 궁의 3×3 Grid 그래프", fontsize=13, fontweight="bold")
ax.set_xlim(-0.8, 8.8)
ax.set_ylim(-0.8, 8.8)
ax.set_aspect("equal")
ax.axis("off")

ax = axes[0, 1]
# 4-Cycle 예시 강조: 중궁 하변 + 하궁 상변
cycle4 = [40, 5, 1, 36]
cycle4_edges = [(cycle4[i], cycle4[(i + 1) % 4]) for i in range(4)]
for u, v in FULL_EDGES:
    x1, y1 = POSITIONS[u]
    x2, y2 = POSITIONS[v]
    if (u, v) in cycle4_edges or (v, u) in cycle4_edges:
        ax.plot([x1, x2], [y1, y2], color="red", linewidth=3.5, alpha=0.9, zorder=2)
    else:
        ax.plot([x1, x2], [y1, y2], color="#DDDDDD", linewidth=1, alpha=0.4, zorder=0)
for n in cycle4:
    x, y = POSITIONS[n]
    ax.add_patch(
        plt.Circle(
            (x, y),
            0.36,
            facecolor="#FFCCCC",
            edgecolor="red",
            linewidth=3,
            zorder=2,
        )
    )
    ax.text(x, y, str(n), ha="center", va="center", fontsize=10, fontweight="bold", zorder=3)
for n in range(1, 46):
    if n in cycle4:
        continue
    x, y = POSITIONS[n]
    ax.add_patch(
        plt.Circle(
            (x, y),
            0.26,
            facecolor="white",
            edgecolor="#999999",
            linewidth=1.2,
            zorder=1,
        )
    )
    ax.text(x, y, str(n), ha="center", va="center", fontsize=8, zorder=2)
ax.set_title(f"최소 사이클 예시: 40-5-1-36-40 (합={sum(cycle4)})", fontsize=13, fontweight="bold")
ax.set_xlim(-0.8, 8.8)
ax.set_ylim(-0.8, 8.8)
ax.set_aspect("equal")
ax.axis("off")

ax = axes[1, 0]
palace_names = list(PALACES.keys())
palace_sums = [sum(palace_values(p)) for p in palace_names]
palace_bar_colors = [PALACE_COLORS[p] for p in palace_names]
ax.bar(palace_names, palace_sums, color=palace_bar_colors, edgecolor="black", linewidth=1.5)
ax.axhline(y=207, color="red", linestyle="--", linewidth=2)
ax.set_title("각 궁의 9자 합", fontsize=13, fontweight="bold")
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
# 중궁 3×3 grid의 사이클 기반 분해
cycles = nx.cycle_basis(G_intra.subgraph(palace_values("중궁")))
ax.text(
    0.5,
    0.5,
    f"중궁 3×3 Grid\n사이클 수: {len(cycles)}\n최소 사이클 길이: {min(len(c) for c in cycles)}",
    ha="center",
    va="center",
    fontsize=14,
    fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", edgecolor="black"),
)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

plt.tight_layout()
save_fig("04_cycle_analysis.png")
plt.close()

# --- 05: 중심성 + 합 불변량 ---
fig, axes = plt.subplots(2, 2, figsize=(16, 14))

ax = axes[0, 0]
degrees = dict(G_full.degree())
nodes_sorted = sorted(G_full.nodes(), key=lambda n: degrees[n], reverse=True)
colors_sorted = [WUXING_COLOR[wuxing_of(n)] for n in nodes_sorted]
ax.bar(range(45), [degrees[n] for n in nodes_sorted], color=colors_sorted, edgecolor="black")
ax.set_xticks(range(45))
ax.set_xticklabels([str(n) for n in nodes_sorted], fontsize=7)
ax.set_title("Degree (전체 격자)", fontsize=12, fontweight="bold")
ax.set_ylabel("Degree", fontsize=10)

ax = axes[0, 1]
betw_sorted = sorted(G_full.nodes(), key=lambda n: betw_full[n], reverse=True)
colors_b = [WUXING_COLOR[wuxing_of(n)] for n in betw_sorted]
ax.bar(range(45), [betw_full[n] for n in betw_sorted], color=colors_b, edgecolor="black")
ax.set_xticks(range(45))
ax.set_xticklabels([str(n) for n in betw_sorted], fontsize=7)
ax.set_title("Betweenness Centrality", fontsize=12, fontweight="bold")
ax.set_ylabel("Centrality", fontsize=10)

ax = axes[1, 0]
wx_sums = {wx: sum([n for n in range(1, 46) if wuxing_of(n) == wx]) for wx in ["수", "화", "목", "금", "토"]}
wx_names = list(wx_sums.keys())
wx_vals = list(wx_sums.values())
wx_colors_bar = [WUXING_COLOR[w] for w in wx_names]
ax.bar(wx_names, wx_vals, color=wx_colors_bar, edgecolor="black", linewidth=1.5)
ax.set_title("오행별 수 합 (189, 198, 207, 216, 225)", fontsize=12, fontweight="bold")
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
    "전체": sum(range(1, 46)),
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
m0_labels = [f"M0={m0}" for m0, _ in FAMILY]
m0_values = [total for _, total in FAMILY]
m0_colors = [WUXING_COLOR[RESIDUE_STYLE[m0 % 5]["name"]] for m0, _ in FAMILY]
ax.bar(m0_labels, m0_values, color=m0_colors, edgecolor="black", linewidth=1.5)
ax.set_title("일반화 가족: 궁 합의 등차수열\nM(n+1) = M(n) + 9", fontsize=13, fontweight="bold")
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

ax = axes[1]
n_layers = 3
theta = np.linspace(0, 2 * np.pi, n_layers + 1)[:-1]
for i, t in enumerate(theta):
    r = 2.5 + i * 1.5
    circle = plt.Circle((0, 0), r, fill=False, color=["#CC4444", "#4488CC", "#44AA44"][i], linewidth=2, linestyle="--")
    ax.add_patch(circle)
    ax.text(r * np.cos(np.pi / 4), r * np.sin(np.pi / 4), f"{45 * (i + 1)}자", fontsize=10, fontweight="bold")
ax.add_patch(plt.Circle((0, 0), 0.5, facecolor="#CC9944", edgecolor="black", linewidth=2))
ax.text(0, 0, "CORE\n45", ha="center", va="center", fontsize=10, fontweight="bold")
ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("동심원 확장: 45k자 구조", fontsize=13, fontweight="bold")

plt.tight_layout()
save_fig("07_local_extensions.png")
plt.close()

# --- 08: 위치 패턴 (모서리 / 변의 중점 / 중심) ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

ax = axes[0]
palace_names = list(PALACES.keys())
corner_vals_list = [CORNER_SUMS[p] for p in palace_names]
edge_vals_list = [EDGE_SUMS[p] for p in palace_names]
center_vals_list = [CENTER_VALUES[p] for p in palace_names]
x = np.arange(len(palace_names))
width = 0.25
ax.bar(x - width, corner_vals_list, width, label="모서리 4개 숫자", color="#CC4444", edgecolor="black")
ax.bar(x, edge_vals_list, width, label="변의 중점 4개 숫자", color="#4488CC", edgecolor="black")
ax.bar(x + width, center_vals_list, width, label="중심 1자", color="#44AA44", edgecolor="black")
ax.set_xticks(x)
ax.set_xticklabels(palace_names)
ax.set_title("궁별 위치별 합", fontsize=13, fontweight="bold")
ax.legend()
ax.set_ylabel("Sum", fontsize=10)

ax = axes[1]
# 중심값 분포
ax.bar(palace_names, center_vals_list, color=[PALACE_COLORS[p] for p in palace_names], edgecolor="black")
ax.set_title(f"각 궁의 중심값: {sorted(center_vals_list)}", fontsize=13, fontweight="bold")
for bar, val in zip(ax.patches, center_vals_list):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.3,
        str(val),
        ha="center",
        fontsize=12,
        fontweight="bold",
    )
ax.set_ylabel("Center Value", fontsize=10)

plt.tight_layout()
save_fig("08_position_patterns.png")
plt.close()

print("\n" + "=" * 60)
print("모든 이미지 생성 완료!")
print(f"출력 디렉토리: {OUTPUT_DIR}/")
print("=" * 60)
