#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
象上用九圖 (중상용구도) — 현대 그래프·조합론적 심층 분석

《구수략(九數略)》계열 도상 중 중상용구도(象上用九圖)를 현대 수학 언어로 재해석.
분석 대상: 1부터 33까지의 수를 중심 9를 관통하는 4개 축(각 9자, 합 147)과
4겹의 동심 팔각형 고리(각 합 138)에 배치한 별형(스파이더) 구조.
"""

import math
import os
from collections import Counter
from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.lines import Line2D

# ============================================================
# 0. 폰트 및 출력 설정
# ============================================================

os.chdir(Path(__file__).parent)

try:
    fm.fontManager.addfont("/usr/share/fonts/naver-nanum-gothic-fonts/NanumGothic.ttf")
except Exception:
    pass

PREFERRED_FONTS = [
    "NanumGothic",
    "Noto Sans CJK KR",
    "Noto Sans CJK JP",
    "Malgun Gothic",
    "AppleGothic",
]
_available_fonts = {f.name for f in fm.fontManager.ttflist}
_selected_fonts = [name for name in PREFERRED_FONTS if name in _available_fonts]
if not _selected_fonts:
    for f in fm.fontManager.ttflist:
        if any(k in f.name for k in ("CJK", "Nanum", "Malgun", "AppleGothic")):
            _selected_fonts.append(f.name)
            break

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = _selected_fonts + ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUTPUT_DIR = Path(".")
SAVED_FIGURES: list[str] = []


def save_fig(name: str) -> None:
    path = OUTPUT_DIR / name
    plt.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    SAVED_FIGURES.append(name)
    print(f"[저장] {path}")


# ============================================================
# 1. 원본 데이터 구조화
# ============================================================

# 좌표는 이 디렉토리의 visualize.py와 동일한 기하학을 사용한다.
COORDS = {
    27: (-4, 4), 20: (0, 4), 33: (4, 4),
    15: (-2, 3), 16: (0, 3), 1: (2, 3),
    3: (-1.5, 2), 23: (0, 2), 13: (1.5, 2),
    24: (-1, 1), 10: (0, 1), 22: (1, 1),
    28: (-4, 0), 5: (-3, 0), 11: (-2, 0), 25: (-1, 0), 9: (0, 0),
    7: (1, 0), 19: (2, 0), 31: (3, 0), 12: (4, 0),
    18: (-1, -1), 2: (0, -1), 30: (1, -1),
    26: (-1.5, -2), 29: (0, -2), 14: (1.5, -2),
    17: (-2, -3), 32: (0, -3), 21: (2, -3),
    8: (-4, -4), 6: (0, -4), 4: (4, -4),
}

CENTER = 9

# 4개 대칭축: 한쪽 끝에서 중심을 지나 반대쪽 끝까지 이어지는 9자 열.
AXES = {
    "vertical": [20, 16, 23, 10, 9, 2, 29, 32, 6],
    "horizontal": [28, 5, 11, 25, 9, 7, 19, 31, 12],
    "diagonal1": [27, 15, 3, 24, 9, 30, 14, 21, 4],
    "diagonal2": [33, 1, 13, 22, 9, 18, 26, 17, 8],
}

AXIS_TARGET = 147   # 각 축의 목표 합
RING_TARGET = 138   # 각 고리의 목표 합
RAY_TARGET = 69     # 각 광선의 목표 합
TOTAL_TARGET = 561  # 1..33의 전체 합

RESIDUE_STYLE = {
    1: {"face": "#E5E5E5", "edge": "#444444", "name": "Water", "ko": "수"},
    2: {"face": "#F6D0D0", "edge": "#B54141", "name": "Fire", "ko": "화"},
    3: {"face": "#D5E3FA", "edge": "#3D6DB3", "name": "Wood", "ko": "목"},
    4: {"face": "#D7D7D7", "edge": "#1F1F1F", "name": "Metal", "ko": "금"},
    0: {"face": "#F7E3A0", "edge": "#B58A00", "name": "Earth", "ko": "토"},
}

DISPLAY_LABELS = {
    "vertical": "세로축",
    "horizontal": "가로축",
    "diagonal1": "대각축1",
    "diagonal2": "대각축2",
    "Water": "수",
    "Fire": "화",
    "Wood": "목",
    "Metal": "금",
    "Earth": "토",
    "generation": "상생",
    "overcoming": "상극",
    "same_phase": "동질",
    "neutral": "중성",
}

PHASE_COLOR = {
    "Water": "#4488CC",
    "Fire": "#CC4444",
    "Wood": "#44AA44",
    "Metal": "#888888",
    "Earth": "#CC9944",
}

AXIS_COLORS = {
    "vertical": "#CC4444",
    "horizontal": "#4488CC",
    "diagonal1": "#44AA44",
    "diagonal2": "#CC9944",
}

# 오행 관계 (상생: 목→화→토→금→수→목, 상극: 목→토→수→화→금→목)
GENERATION_PAIRS = {
    frozenset(p)
    for p in [
        ("Wood", "Fire"), ("Fire", "Earth"), ("Earth", "Metal"),
        ("Metal", "Water"), ("Water", "Wood"),
    ]
}
OVERCOMING_PAIRS = {
    frozenset(p)
    for p in [
        ("Wood", "Earth"), ("Earth", "Water"), ("Water", "Fire"),
        ("Fire", "Metal"), ("Metal", "Wood"),
    ]
}

DIRECTION_KO = {
    90: "북", 45: "북동", 0: "동", -45: "남동",
    -90: "남", -135: "남서", 180: "서", 135: "북서",
}


def phase_of(n: int) -> str:
    return RESIDUE_STYLE[n % 5]["name"]


def residue_1based(n: int) -> int:
    r = n % 5
    return 5 if r == 0 else r


def compass_of(value: int) -> int:
    """중심 원점 기준 value의 방위각을 가장 가까운 45° 방위로 환산."""
    x, y = COORDS[value]
    ang = math.degrees(math.atan2(y, x))
    return int(round(ang / 45.0) * 45) if abs(ang) <= 180 else 0


def clockwise_from_top(values: list[int]) -> list[int]:
    """12시 방향에서 시작해 시계방향이 되도록 각도 정렬."""
    return sorted(
        values,
        key=lambda v: math.atan2(COORDS[v][0], COORDS[v][1]) % (2 * math.pi),
    )


# ============================================================
# 2. 그래프 구성 (스파이더 트리: 중심 + 8개 광선)
# ============================================================

EDGES: list[tuple[int, int]] = []
for axis in AXES.values():
    for a, b in zip(axis, axis[1:]):
        EDGES.append(tuple(sorted((a, b))))
EDGES = sorted(set(EDGES))

G = nx.Graph()
G.add_nodes_from(range(1, 34))
G.add_edges_from(EDGES)
for n in G.nodes():
    G.nodes[n]["phase"] = phase_of(n)

# 동심 고리: 중심 9로부터의 그래프 거리(BFS)가 같은 노드들의 집합.
DIST = nx.single_source_shortest_path_length(G, CENTER)
RINGS: dict[str, list[int]] = {}
for d in range(1, 5):
    RINGS[f"d{d}"] = sorted([n for n, dist in DIST.items() if dist == d])

# 광선: 각 축에서 중심을 제외한 한쪽 방향의 4자 열 (중심에서 바깥 순서).
RAYS: dict[str, list[int]] = {}
for axis in AXES.values():
    i = axis.index(CENTER)
    for side in (axis[:i][::-1], axis[i + 1:]):
        direction = DIRECTION_KO[compass_of(side[-1])]
        RAYS[direction] = list(side)

RAY_COLORS = {
    "북": "#E41A1C", "북동": "#FF7F00", "동": "#B8860B", "남동": "#4DAF4A",
    "남": "#377EB8", "남서": "#984EA3", "서": "#A65628", "북서": "#F781BF",
}

RING_COLORS = {"d1": "#555555", "d2": "#777777", "d3": "#999999", "d4": "#BBBBBB"}


# ============================================================
# 3. 조합론·그래프 이론 분석
# ============================================================

def validate() -> None:
    """원본 데이터의 모든 핵심 성질을 검산. 하나라도 어긋나면 즉시 중단."""
    values = sorted(COORDS)
    if values != list(range(1, 34)):
        raise ValueError("수 집합이 1..33 각 1회가 아님")
    total = sum(values)
    if total != TOTAL_TARGET:
        raise ValueError(f"전체 합이 {TOTAL_TARGET}이 아님: {total}")

    for name, axis in AXES.items():
        label = DISPLAY_LABELS[name]
        if len(axis) != 9:
            raise ValueError(f"{label}이 9자가 아님")
        if len(set(axis)) != 9:
            raise ValueError(f"{label}에 중복 값이 있음")
        if sum(axis) != AXIS_TARGET:
            raise ValueError(f"{label} 합이 {AXIS_TARGET}이 아님: {sum(axis)}")
        if axis.count(CENTER) != 1 or axis[4] != CENTER:
            raise ValueError(f"{label}의 중앙 칸이 {CENTER}가 아님")

    # 겹침 검산: 임의의 두 축은 오직 중심 9에서만 만나야 한다.
    names = list(AXES)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            inter = set(AXES[names[i]]) & set(AXES[names[j]])
            if inter != {CENTER}:
                raise ValueError(f"{names[i]}와 {names[j]}의 교집합이 중심뿐이 아님: {inter}")
    k_times_s = len(AXES) * AXIS_TARGET
    duplication = (len(AXES) - 1) * CENTER  # 중심이 4회 계수 → 3회 중복
    if k_times_s != total + duplication:
        raise ValueError("중복 보정 등식 k·S = T + D 불성립")

    # 고리 검산: 4개 동심 고리 각각 8자, 합 138.
    for d, ring in RINGS.items():
        if len(ring) != 8:
            raise ValueError(f"{d} 고리가 8자가 아님")
        if sum(ring) != RING_TARGET:
            raise ValueError(f"{d} 고리 합이 {RING_TARGET}이 아님: {sum(ring)}")

    # 광선 검산: 8개 광선 각각 4자, 합 69.
    if len(RAYS) != 8:
        raise ValueError("광선이 8개가 아님")
    for direction, ray in RAYS.items():
        if len(ray) != 4:
            raise ValueError(f"{direction} 광선이 4자가 아님")
        if sum(ray) != RAY_TARGET:
            raise ValueError(f"{direction} 광선 합이 {RAY_TARGET}이 아님: {sum(ray)}")

    # 검산 통과 — 검증된 합 등식 출력
    print("[검산 통과] 검증된 합 등식:")
    for name, axis in AXES.items():
        print(f"  {DISPLAY_LABELS[name]}: {'+'.join(map(str, axis))} = {sum(axis)}")
    print(f"  전체 합: 1+...+33 = {total}")
    print(f"  중복 보정: 4×{AXIS_TARGET} = {k_times_s} = {total} + 3×{CENTER} (만든 수 33자, 쓰임 36자)")
    for d, ring in RINGS.items():
        print(f"  {d} 고리: {'+'.join(map(str, ring))} = {sum(ring)}")
    print(f"  고리 보정: 4×{RING_TARGET} = {4 * RING_TARGET} = {total} − {CENTER}")
    for direction, ray in RAYS.items():
        print(f"  {direction} 광선: {'+'.join(map(str, ray))} = {sum(ray)}")


validate()

print()
print("=" * 60)
print("象上用九圖 (중상용구도) 현대 그래프·조합론 분석")
print("=" * 60)
print(f"노드 수: {G.number_of_nodes()}")
print(f"엣지 수: {G.number_of_edges()}")
print(f"연결 성분: {nx.number_connected_components(G)}")
print(f"트리 여부: {nx.is_tree(G)}")
print(f"지름(diameter): {nx.diameter(G)}")

deg_seq = sorted([d for _, d in G.degree()], reverse=True)
deg_counter = Counter(d for _, d in G.degree())
print(f"차수 시퀀스: {deg_seq}")
print(f"차수 분포: {dict(sorted(deg_counter.items(), reverse=True))}")

print("\n오행별 수 합:")
WUXING_SUMS: dict[str, int] = {}
for r in [1, 2, 3, 4, 5]:
    nodes = [n for n in range(1, 34) if residue_1based(n) == r]
    wx = RESIDUE_STYLE[r % 5]["name"]
    WUXING_SUMS[wx] = sum(nodes)
    print(f"  {DISPLAY_LABELS[wx]}({wx}, {r}): {len(nodes)}개, 합={sum(nodes)}, 수들={nodes}")

print("\n축별 오행 분포:")
for name, axis in AXES.items():
    counts = Counter(phase_of(v) for v in axis)
    counts_ko = {DISPLAY_LABELS[k]: v for k, v in sorted(counts.items())}
    print(f"  {DISPLAY_LABELS[name]}: {counts_ko}")

print("\n고리별 오행 분포:")
for d, ring in RINGS.items():
    counts = Counter(phase_of(v) for v in ring)
    counts_ko = {DISPLAY_LABELS[k]: v for k, v in sorted(counts.items())}
    print(f"  {d}: {counts_ko}")

betw = nx.betweenness_centrality(G)
print("\n매개 중심성 (Top 10):")
for n, v in sorted(betw.items(), key=lambda x: (-x[1], x[0]))[:10]:
    print(f"  {n}({DISPLAY_LABELS[phase_of(n)]}, 거리 {DIST[n]}): {v:.3f}")

cycle_basis = nx.cycle_basis(G)
print(f"\n사이클 기반 크기: {len(cycle_basis)} (트리 — 사이클 없음)")

# 오행 엣지 분류
wx_edge_counts: dict[str, int] = {}
for u, v in G.edges():
    pair = frozenset((phase_of(u), phase_of(v)))
    if phase_of(u) == phase_of(v):
        key = "same_phase"
    elif pair in GENERATION_PAIRS:
        key = "generation"
    elif pair in OVERCOMING_PAIRS:
        key = "overcoming"
    else:
        key = "neutral"
    wx_edge_counts[key] = wx_edge_counts.get(key, 0) + 1

print("\n오행 엣지 분포:")
total_edges = G.number_of_edges()
for key in ["generation", "overcoming", "same_phase", "neutral"]:
    cnt = wx_edge_counts.get(key, 0)
    print(f"  {DISPLAY_LABELS[key]}: {cnt} ({100.0 * cnt / total_edges:.1f}%)")

# 스펙트럼 분석
RESIDUE_ORDER = {1: 0, 2: 1, 3: 2, 4: 3, 0: 4}
nodelist = sorted(G.nodes(), key=lambda n: (RESIDUE_ORDER[n % 5], n))
adj = nx.to_numpy_array(G, nodelist=nodelist)
eigenvalues = np.linalg.eigvalsh(adj)
lambda_max = float(max(eigenvalues))
lambda_min = float(min(eigenvalues))
print(f"\n인접 행렬 스펙트럼: λ_max = {lambda_max:.4f}, λ_min = {lambda_min:.4f}")

# ============================================================
# 4. 위치 기반 분석 (고리 / 광선 / 축)
# ============================================================

RING_SUMS = {d: sum(ring) for d, ring in RINGS.items()}
RAY_SUMS = {direction: sum(ray) for direction, ray in RAYS.items()}
AXIS_SUMS = {name: sum(axis) for name, axis in AXES.items()}

print("\n고리별 합:")
for d, ring in RINGS.items():
    print(f"  {d} (거리 {d[1]}): {ring} → 합 {RING_SUMS[d]}")

print("\n광선별 합 (중심→바깥):")
for direction, ray in RAYS.items():
    print(f"  {direction}: {ray} → 합 {RAY_SUMS[direction]}")

print("\n축 분해 (광선+중심+광선):")
for name, axis in AXES.items():
    i = axis.index(CENTER)
    left, right = axis[:i], axis[i + 1:]
    print(
        f"  {DISPLAY_LABELS[name]}: {sum(left)} + {CENTER} + {sum(right)} = {AXIS_SUMS[name]}"
    )

# ============================================================
# 5. 일반화 가족 (별형 가족: 축 a개, 축당 L자)
# ============================================================

def family_params(a: int, L: int) -> tuple[int, int, int, int, int]:
    """축 a개, 축당 L자(중심 공유), 중심값 c=L일 때의 구조 매개변수."""
    N = a * (L - 1) + 1
    T = N * (N + 1) // 2
    c = L
    S = (T + (a - 1) * c) // a
    R = 2 * (T - c) // (L - 1)
    return N, T, c, S, R


FAMILY = [
    ("범수용오도(範數用五圖)", 2, 5),
    ("장책용칠도(章策用七圖)", 3, 7),
    ("중상용구도(象上用九圖)", 4, 9),
]

print("\n일반화 가족 (축 a개, 축당 L자, 중심 c=L, N=a(L−1)+1):")
for label, a, L in FAMILY:
    N, T, c, S, R = family_params(a, L)
    print(f"  {label}: a={a}, L={L} → N={N}, T={T}, c={c}, 축 합 S={S}, 고리 합 R={R}")

# ============================================================
# 6. 시각화
# ============================================================

def draw_ring_polygons(ax, labeled: bool = True, colorful: bool = False) -> None:
    for d, ring in RINGS.items():
        order = clockwise_from_top(ring)
        xs = [COORDS[v][0] for v in order] + [COORDS[order[0]][0]]
        ys = [COORDS[v][1] for v in order] + [COORDS[order[0]][1]]
        color = PHASE_COLOR[["Water", "Fire", "Wood", "Metal"][int(d[1]) - 1]] if colorful else RING_COLORS[d]
        ax.plot(xs, ys, color=color, linewidth=1.5, linestyle=(0, (4, 4)), alpha=0.9, zorder=0)
        if labeled:
            top = max(ring, key=lambda v: COORDS[v][1])
            tx, ty = COORDS[top]
            ax.text(
                tx + 0.15, ty + 0.35,
                f"{d} 고리 Σ={RING_SUMS[d]}",
                ha="left", va="bottom", fontsize=9, color="#333333",
            )


def draw_nodes(ax, values=None, radius=0.34, fontsize=10) -> None:
    for value, (x, y) in COORDS.items():
        if values is not None and value not in values:
            continue
        style = RESIDUE_STYLE[value % 5]
        face, edge, lw, rad = style["face"], style["edge"], 2.0, radius
        if value == CENTER:
            edge, lw, rad = "#000000", 3.5, radius + 0.08
        ax.add_patch(
            plt.Circle((x, y), rad, facecolor=face, edgecolor=edge, linewidth=lw, zorder=2)
        )
        ax.text(x, y, str(value), ha="center", va="center",
                fontsize=fontsize, fontweight="bold", zorder=3)


def draw_axis_edges(ax, alpha=0.6, linewidth=2.5) -> None:
    for name, axis in AXES.items():
        for a, b in zip(axis, axis[1:]):
            x1, y1 = COORDS[a]
            x2, y2 = COORDS[b]
            ax.plot([x1, x2], [y1, y2], color=AXIS_COLORS[name],
                    linewidth=linewidth, alpha=alpha, zorder=1)


# --- 01: 원본 그래프 ---
fig, ax = plt.subplots(figsize=(12, 12))
draw_ring_polygons(ax)
draw_axis_edges(ax)
draw_nodes(ax)
ax.set_title(
    "象上用九圖 (중상용구도) — 원본 별형 구조\n"
    "4축 · 9자 · 축 합 147 · 4겹 고리 합 138 · 전체 합 561",
    fontsize=16, fontweight="bold",
)
ax.set_xlim(-5.4, 5.4)
ax.set_ylim(-5.4, 5.9)
ax.set_aspect("equal")
ax.axis("off")
wuxing_handles = [
    mpatches.Patch(facecolor=PHASE_COLOR[wx], edgecolor="black",
                   label=f"{DISPLAY_LABELS[wx]}({wx})")
    for wx in ["Water", "Fire", "Wood", "Metal", "Earth"]
]
leg1 = ax.legend(handles=wuxing_handles, loc="lower right", fontsize=10, framealpha=0.9)
ax.add_artist(leg1)
axis_handles = [
    Line2D([0], [0], color=AXIS_COLORS[name], lw=2.5, label=DISPLAY_LABELS[name])
    for name in AXES
]
ax.legend(handles=axis_handles, loc="upper left", fontsize=10, framealpha=0.9)
save_fig("01_original_graph.png")
plt.close()

# --- 02: 오행별 서브그래프 분해 ---
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()
ax = axes[0]
draw_ring_polygons(ax, labeled=False)
draw_axis_edges(ax, alpha=0.3, linewidth=1.5)
draw_nodes(ax, radius=0.3, fontsize=9)
ax.set_title("전체 그래프", fontsize=13, fontweight="bold")
ax.set_xlim(-5.2, 5.2)
ax.set_ylim(-5.2, 5.2)
ax.set_aspect("equal")
ax.axis("off")

for idx, wx in enumerate(["Water", "Fire", "Wood", "Metal", "Earth"]):
    ax = axes[idx + 1]
    wx_nodes = [n for n in range(1, 34) if phase_of(n) == wx]
    for a, b in EDGES:
        x1, y1 = COORDS[a]
        x2, y2 = COORDS[b]
        ax.plot([x1, x2], [y1, y2], color="#EEEEEE", linewidth=1, alpha=0.5, zorder=0)
    for n in range(1, 34):
        if n in wx_nodes:
            continue
        x, y = COORDS[n]
        ax.add_patch(plt.Circle((x, y), 0.24, facecolor="#F0F0F0",
                                edgecolor="#CCCCCC", linewidth=1, zorder=1))
        ax.text(x, y, str(n), ha="center", va="center", fontsize=8, color="#AAAAAA", zorder=2)
    for n in wx_nodes:
        x, y = COORDS[n]
        ax.add_patch(plt.Circle((x, y), 0.36, facecolor=PHASE_COLOR[wx],
                                edgecolor="black", linewidth=2.5, zorder=2))
        ax.text(x, y, str(n), ha="center", va="center", fontsize=10,
                fontweight="bold",
                color="white" if wx in ["Water", "Wood"] else "black", zorder=3)
    ax.set_title(
        f"{DISPLAY_LABELS[wx]}({wx}) · {len(wx_nodes)}개 · 합 {WUXING_SUMS[wx]}",
        fontsize=12, fontweight="bold", color=PHASE_COLOR[wx],
    )
    ax.set_xlim(-5.2, 5.2)
    ax.set_ylim(-5.2, 5.2)
    ax.set_aspect("equal")
    ax.axis("off")

plt.suptitle("오행(五行)별 서브그래프 분해", fontsize=16, fontweight="bold", y=1.0)
plt.tight_layout()
save_fig("02_wuxing_decomposition.png")
plt.close()

# --- 03: 인접 행렬 + 스펙트럼 ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
im = ax.imshow(adj, cmap="YlOrRd", interpolation="nearest")
ax.set_xticks(range(33))
ax.set_yticks(range(33))
ax.set_xticklabels(nodelist, fontsize=6)
ax.set_yticklabels(nodelist, fontsize=6)
wx_sorted = [phase_of(n) for n in nodelist]
boundaries = [i - 0.5 for i in range(1, 33) if wx_sorted[i] != wx_sorted[i - 1]]
for b in boundaries:
    ax.axhline(y=b, color="blue", linewidth=1.5, alpha=0.7)
    ax.axvline(x=b, color="blue", linewidth=1.5, alpha=0.7)
plt.colorbar(im, ax=ax, shrink=0.8)
ax.set_title("인접 행렬 (오행 블록 순서)", fontsize=13, fontweight="bold")

ax = axes[1]
ax.bar(range(len(eigenvalues)), sorted(eigenvalues, reverse=True),
       color="#4488CC", edgecolor="black", alpha=0.8)
ax.axhline(y=0, color="red", linestyle="--", linewidth=1)
ax.set_xlabel("지표", fontsize=11)
ax.set_ylabel("고유값", fontsize=11)
ax.set_title(
    f"그래프 스펙트럼\nλ_max={lambda_max:.2f}, λ_min={lambda_min:.2f}",
    fontsize=13, fontweight="bold",
)
ax.grid(True, alpha=0.3)
plt.tight_layout()
save_fig("03_adjacency_spectrum.png")
plt.close()

# --- 04: 사이클 분석 (트리 → 광선/고리 구조로 대체) ---
fig, axes = plt.subplots(2, 2, figsize=(16, 14))

ax = axes[0, 0]
# 광선별 색상: 엣지를 광선에 귀속시켜 색칠
edge_ray: dict[tuple[int, int], str] = {}
for direction, ray in RAYS.items():
    chain = [CENTER] + ray
    for a, b in zip(chain, chain[1:]):
        edge_ray[tuple(sorted((a, b)))] = direction
for (a, b), direction in edge_ray.items():
    x1, y1 = COORDS[a]
    x2, y2 = COORDS[b]
    ax.plot([x1, x2], [y1, y2], color=RAY_COLORS[direction], linewidth=3, alpha=0.75, zorder=1)
draw_nodes(ax)
ax.set_title("8방향 광선(ray) 구조 — 스파이더 트리", fontsize=13, fontweight="bold")
ax.set_xlim(-5.2, 5.2)
ax.set_ylim(-5.2, 5.2)
ax.set_aspect("equal")
ax.axis("off")

ax = axes[0, 1]
for a, b in EDGES:
    x1, y1 = COORDS[a]
    x2, y2 = COORDS[b]
    ax.plot([x1, x2], [y1, y2], color="#DDDDDD", linewidth=1.2, alpha=0.6, zorder=0)
draw_ring_polygons(ax, colorful=True)
draw_nodes(ax, radius=0.28, fontsize=9)
ax.set_title("동심 고리 수준 (중심으로부터 그래프 거리 d1–d4)", fontsize=13, fontweight="bold")
ax.set_xlim(-5.2, 5.2)
ax.set_ylim(-5.2, 5.9)
ax.set_aspect("equal")
ax.axis("off")

ax = axes[1, 0]
ray_names = list(RAYS)
ray_vals = [RAY_SUMS[direction] for direction in ray_names]
ax.bar(ray_names, ray_vals, color=[RAY_COLORS[d] for d in ray_names],
       edgecolor="black", linewidth=1.5)
ax.axhline(y=RAY_TARGET, color="red", linestyle="--", linewidth=2)
for bar, val in zip(ax.patches, ray_vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, str(val),
            ha="center", fontsize=12, fontweight="bold")
ax.set_ylim(0, 82)
ax.set_title("광선별 4자 합 — 모두 69", fontsize=13, fontweight="bold")
ax.set_ylabel("합", fontsize=10)

ax = axes[1, 1]
ax.text(
    0.5, 0.5,
    "트리 그래프 (사이클 없음)\n\n"
    f"노드 N = 33, 엣지 E = 32 = N - 1\n"
    f"연결 성분: 1 · 사이클 기반 크기: {len(cycle_basis)}\n"
    f"지름: {nx.diameter(G)} (잎→중심→잎)\n"
    "이분 그래프 ⇒ 스펙트럼이 원점 대칭",
    ha="center", va="center", fontsize=13, fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.6", facecolor="lightyellow", edgecolor="black"),
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
degrees = dict(G.degree())
nodes_sorted = sorted(G.nodes(), key=lambda n: (-degrees[n], n))
ax.bar(range(33), [degrees[n] for n in nodes_sorted],
       color=[PHASE_COLOR[phase_of(n)] for n in nodes_sorted], edgecolor="black")
ax.set_xticks(range(33))
ax.set_xticklabels([str(n) for n in nodes_sorted], fontsize=7)
ax.set_title("차수 (중심 8 · 중간 24개 차수 2 · 잎 8개 차수 1)", fontsize=12, fontweight="bold")
ax.set_ylabel("차수", fontsize=10)

ax = axes[0, 1]
betw_sorted = sorted(G.nodes(), key=lambda n: (-betw[n], n))
ax.bar(range(33), [betw[n] for n in betw_sorted],
       color=[PHASE_COLOR[phase_of(n)] for n in betw_sorted], edgecolor="black")
ax.set_xticks(range(33))
ax.set_xticklabels([str(n) for n in betw_sorted], fontsize=7)
ax.set_title("매개 중심성 (고리 수준별로 동일)", fontsize=12, fontweight="bold")
ax.set_ylabel("중심성", fontsize=10)

ax = axes[1, 0]
wx_names = ["Water", "Fire", "Wood", "Metal", "Earth"]
wx_vals = [WUXING_SUMS[w] for w in wx_names]
ax.bar([DISPLAY_LABELS[w] for w in wx_names], wx_vals,
       color=[PHASE_COLOR[w] for w in wx_names], edgecolor="black", linewidth=1.5)
for bar, val in zip(ax.patches, wx_vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2, str(val),
            ha="center", fontsize=12, fontweight="bold")
ax.set_title("오행별 수 합 (수112 · 화119 · 목126 · 금99 · 토105)", fontsize=12, fontweight="bold")
ax.set_ylabel("합", fontsize=10)

ax = axes[1, 1]
axis_names = list(AXES)
axis_vals = [AXIS_SUMS[n] for n in axis_names]
ax.bar([DISPLAY_LABELS[n] for n in axis_names], axis_vals,
       color=[AXIS_COLORS[n] for n in axis_names], edgecolor="black", linewidth=1.5)
ax.axhline(y=AXIS_TARGET, color="red", linestyle="--", linewidth=2)
for bar, val in zip(ax.patches, axis_vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2, str(val),
            ha="center", fontsize=12, fontweight="bold")
ax.set_ylim(0, 175)
ax.set_title("축별 9자 합 — 모두 147", fontsize=12, fontweight="bold")
ax.set_ylabel("합", fontsize=10)

plt.tight_layout()
save_fig("05_centrality_invariants.png")
plt.close()

# --- 06: 오행 상생상극 ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
phase_graph = nx.DiGraph()
phase_relations = [
    ("Water", "Wood", "generation"),
    ("Wood", "Fire", "generation"),
    ("Fire", "Earth", "generation"),
    ("Earth", "Metal", "generation"),
    ("Metal", "Water", "generation"),
    ("Water", "Fire", "overcoming"),
    ("Fire", "Metal", "overcoming"),
    ("Metal", "Wood", "overcoming"),
    ("Wood", "Earth", "overcoming"),
    ("Earth", "Water", "overcoming"),
]
for u, v, r in phase_relations:
    phase_graph.add_edge(u, v, relation=r)
wx_pos = {"Water": (0, 2), "Wood": (2, 1), "Fire": (1, -1), "Earth": (-1, -1), "Metal": (-2, 1)}
sheng_edges = [(u, v) for u, v, r in phase_relations if r == "generation"]
ke_edges = [(u, v) for u, v, r in phase_relations if r == "overcoming"]
nx.draw_networkx_edges(phase_graph, wx_pos, edgelist=sheng_edges,
                       edge_color="#44AA44", width=3, alpha=0.8, arrows=True,
                       arrowsize=20, connectionstyle="arc3,rad=0.15", ax=ax)
nx.draw_networkx_edges(phase_graph, wx_pos, edgelist=ke_edges,
                       edge_color="#CC4444", width=2, alpha=0.6, style="--",
                       arrows=True, arrowsize=15, connectionstyle="arc3,rad=-0.15", ax=ax)
nx.draw_networkx_nodes(phase_graph, wx_pos,
                       node_color=[PHASE_COLOR[w] for w in phase_graph.nodes()],
                       node_size=3000, edgecolors="black", linewidths=2.5, ax=ax)
nx.draw_networkx_labels(phase_graph, wx_pos,
                        labels={n: DISPLAY_LABELS[n] for n in phase_graph.nodes()},
                        font_size=14, ax=ax)
ax.legend(handles=[
    Line2D([0], [0], color="#44AA44", lw=3, label="상생"),
    Line2D([0], [0], color="#CC4444", lw=2, linestyle="--", label="상극"),
], loc="upper right", fontsize=11)
ax.set_title("오행 상생상극 관계도", fontsize=13, fontweight="bold")
ax.set_xlim(-3, 3.5)
ax.set_ylim(-2.5, 3)
ax.axis("off")

ax = axes[1]
pie_keys = [k for k in ["generation", "overcoming", "same_phase", "neutral"]
            if wx_edge_counts.get(k, 0) > 0]
pie_colors = {"generation": "#44AA44", "overcoming": "#CC4444",
              "same_phase": "#CC9944", "neutral": "#4488CC"}
ax.pie(
    [wx_edge_counts[k] for k in pie_keys],
    labels=[f"{DISPLAY_LABELS[k]}\n{wx_edge_counts[k]}개" for k in pie_keys],
    autopct="%1.1f%%",
    colors=[pie_colors[k] for k in pie_keys],
    explode=[0.05] * len(pie_keys),
    textprops={"fontsize": 12, "fontweight": "bold"},
)
ax.set_title(f"오행 엣지 분포 (N={total_edges})", fontsize=13, fontweight="bold")
plt.tight_layout()
save_fig("06_wuxing_relations.png")
plt.close()

# --- 07: 확장 및 일반화 ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

ax = axes[0]
fam_labels = []
fam_S = []
fam_R = []
for label, a, L in FAMILY:
    N, T, c, S, R = family_params(a, L)
    fam_labels.append(f"{label.split('(')[0]}\na={a} · L={L}")
    fam_S.append(S)
    fam_R.append(R)
x = np.arange(len(FAMILY))
width = 0.35
bars1 = ax.bar(x - width / 2, fam_S, width, label="축 합 S", color="#4488CC", edgecolor="black")
bars2 = ax.bar(x + width / 2, fam_R, width, label="고리 합 R", color="#CC9944", edgecolor="black")
for bars in (bars1, bars2):
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                str(int(bar.get_height())), ha="center", fontsize=11, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(fam_labels, fontsize=10)
ax.set_title("별형 일반화 가족: 축 a개 · 축당 L자 · 중심 c=L", fontsize=13, fontweight="bold")
ax.legend(fontsize=11)
ax.set_ylabel("합", fontsize=10)

ax = axes[1]
for k in range(4):
    ang = math.radians(90 + k * 45)
    dx, dy = math.cos(ang), math.sin(ang)
    ax.plot([-4.6 * dx, 4.6 * dx], [-4.6 * dy, 4.6 * dy],
            color="#999999", linewidth=1.5, linestyle=(0, (4, 4)), zorder=0)
for r in [1.3, 2.3, 3.3, 4.3]:
    ax.add_patch(plt.Circle((0, 0), r, fill=False, color="#4488CC",
                            linewidth=1.2, linestyle=":", alpha=0.8))
ax.add_patch(plt.Circle((0, 0), 0.42, facecolor="#F7E3A0", edgecolor="black", linewidth=2, zorder=2))
ax.text(0, 0, "c", ha="center", va="center", fontsize=12, fontweight="bold", zorder=3)
ax.text(
    0, -5.6,
    "N = a(L-1)+1 · T = N(N+1)/2 · S = (T+(a-1)c)/a · R = 2(T-c)/(L-1)\n"
    "다음 후보: a=5, L=11 → N=51, S=274, R=263 (가설, 미검증)",
    ha="center", va="center", fontsize=11,
    bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", edgecolor="black"),
)
ax.set_xlim(-5.6, 5.6)
ax.set_ylim(-6.4, 5.4)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("별형 구조의 일반 스키마 (a축 · L자 · 동심 고리)", fontsize=13, fontweight="bold")

plt.tight_layout()
save_fig("07_local_extensions.png")
plt.close()

# --- 08: 위치 패턴 (고리 / 광선 / 축 분해) ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

ax = axes[0]
ring_names = list(RINGS)
ring_vals = [RING_SUMS[d] for d in ring_names]
ax.bar(ring_names, ring_vals,
       color=[RING_COLORS[d] for d in ring_names], edgecolor="black", linewidth=1.5)
ax.axhline(y=RING_TARGET, color="red", linestyle="--", linewidth=2)
for bar, val in zip(ax.patches, ring_vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2, str(val),
            ha="center", fontsize=12, fontweight="bold")
ax.set_ylim(0, 165)
ax.set_title("고리별 8자 합 — 모두 138 = (561-9)/4", fontsize=13, fontweight="bold")
ax.set_ylabel("합", fontsize=10)

ax = axes[1]
stack_names = [DISPLAY_LABELS[n] for n in AXES]
left_sums = []
right_sums = []
for name, axis in AXES.items():
    i = axis.index(CENTER)
    left_sums.append(sum(axis[:i]))
    right_sums.append(sum(axis[i + 1:]))
x = np.arange(len(AXES))
b1 = ax.bar(x, left_sums, 0.5, label="광선 A (69)", color="#4488CC", edgecolor="black")
b2 = ax.bar(x, [CENTER] * 4, 0.5, bottom=left_sums, label=f"중심 ({CENTER})",
            color="#CC9944", edgecolor="black")
b3 = ax.bar(x, right_sums, 0.5,
            bottom=[l + CENTER for l in left_sums], label="광선 B (69)",
            color="#44AA44", edgecolor="black")
for bars in (b1, b2, b3):
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + h / 2, str(int(h)),
                ha="center", va="center", fontsize=11, fontweight="bold", color="white")
ax.axhline(y=AXIS_TARGET, color="red", linestyle="--", linewidth=2)
ax.set_xticks(x)
ax.set_xticklabels(stack_names, fontsize=11)
ax.set_ylim(0, 175)
ax.set_title("축 분해: 광선 69 + 중심 9 + 광선 69 = 147", fontsize=13, fontweight="bold")
ax.legend(fontsize=11, loc="lower right")
ax.set_ylabel("합", fontsize=10)

plt.tight_layout()
save_fig("08_position_patterns.png")
plt.close()

# ============================================================
# 7. 요약
# ============================================================

print()
print("=" * 60)
print("검증된 핵심 성질 요약")
print("=" * 60)
print("  1. 수 집합: 1..33 각 1회, 전체 합 561")
print(f"  2. 4개 축 각각 합 147; 4×147 = 588 = 561 + 3×9 (중심 4회 계수)")
print(f"  3. 그래프: 트리 (노드 {G.number_of_nodes()}, 엣지 {G.number_of_edges()}), "
      f"중심 차수 8, 잎 8개, 지름 {nx.diameter(G)}")
print("  4. 8개 광선 각각 합 69; 축 = 69+9+69 = 147")
print("  5. 4개 동심 고리 각각 합 138 = (561−9)/4; 중심 포함 시 147")
print(f"  6. 오행 합: 수{WUXING_SUMS['Water']} 화{WUXING_SUMS['Fire']} "
      f"목{WUXING_SUMS['Wood']} 금{WUXING_SUMS['Metal']} 토{WUXING_SUMS['Earth']}")
print(f"  7. 엣지 관계: 상생 {wx_edge_counts.get('generation', 0)}, "
      f"상극 {wx_edge_counts.get('overcoming', 0)}, "
      f"동질 {wx_edge_counts.get('same_phase', 0)}, 중성 {wx_edge_counts.get('neutral', 0)}")
print(f"  8. 스펙트럼: λ_max ≈ {lambda_max:.3f}, λ_min ≈ {lambda_min:.3f}")

print("\n생성된 파일:")
for name in SAVED_FIGURES:
    print(f"  {name}")
print("=" * 60)
