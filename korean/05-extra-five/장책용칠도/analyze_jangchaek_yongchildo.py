#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
장책용칠도 (章策用七圖) — 현대 그래프·조합론적 심층 분석

《구수략(九數略)》계열 도상 중 장책용칠도(章策用七圖)를 현대 수학 언어로 재해석.
분석 대상: 1부터 19까지의 수를 중심 7을 공유하는 3개 축(각 7칸)에 배치한 별형 구조.
각 축의 합은 68, 중심 7은 세 축이 공유한다.
"""

import math
import os
from collections import Counter
from pathlib import Path

import matplotlib.font_manager as font_manager
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.lines import Line2D

# ============================================================
# 0. 폰트 및 출력 설정
# ============================================================

os.chdir(Path(__file__).parent)

# 나눔고딕 직접 등록 시도 후, 실패하면 설치된 CJK 폰트를 탐색
try:
    font_manager.fontManager.addfont("/usr/share/fonts/naver-nanum-gothic-fonts/NanumGothic.ttf")
except Exception:
    pass

preferred_fonts = [
    "NanumGothic",
    "NanumBarunGothic",
    "Noto Sans CJK KR",
    "Noto Sans CJK JP",
    "Malgun Gothic",
    "AppleGothic",
]
available_fonts = {f.name for f in font_manager.fontManager.ttflist}
selected_fonts = [name for name in preferred_fonts if name in available_fonts]
if not selected_fonts:
    for f in font_manager.fontManager.ttflist:
        if any(k in f.name for k in ("Nanum", "Noto Sans CJK", "Malgun", "AppleGothic")):
            selected_fonts.append(f.name)
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = selected_fonts + ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUTPUT_DIR = Path(".")


def save_fig(name):
    path = OUTPUT_DIR / name
    plt.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    print(f"[저장] {path}")


# ============================================================
# 1. 원본 데이터 구조화 (visualize.py와 동일한 좌표 계산)
# ============================================================

CENTER = 7
SPACING = 1.2

# 세 축: 중심 7을 사이에 두고 한쪽 끝에서 반대쪽 끝까지 나열
AXES = {
    "axis_vertical": [5, 18, 9, 7, 12, 2, 15],   # 수직축 (90°), 위 -> 아래
    "axis_150": [4, 10, 19, 7, 1, 14, 13],       # 150° 축, 좌상 -> 우하
    "axis_30": [8, 6, 17, 7, 3, 11, 16],         # 30° 축, 우상 -> 좌하
}
AXIS_ANGLE = {"axis_vertical": 90.0, "axis_150": 150.0, "axis_30": 30.0}

RESIDUE_STYLE = {
    1: {"face": "#E5E5E5", "edge": "#444444", "name": "Water", "ko": "수"},
    2: {"face": "#F6D0D0", "edge": "#B54141", "name": "Fire", "ko": "화"},
    3: {"face": "#D5E3FA", "edge": "#3D6DB3", "name": "Wood", "ko": "목"},
    4: {"face": "#D7D7D7", "edge": "#1F1F1F", "name": "Metal", "ko": "금"},
    0: {"face": "#F7E3A0", "edge": "#B58A00", "name": "Earth", "ko": "토"},
}

DISPLAY_LABELS = {
    "axis_vertical": "수직축(90°)",
    "axis_150": "대각축(150°)",
    "axis_30": "대각축(30°)",
    "Water": "수",
    "Fire": "화",
    "Wood": "목",
    "Metal": "금",
    "Earth": "토",
    "generation": "상생",
    "overcoming": "상극",
    "same_phase": "동질",
    "neutral": "중립",
}

PHASE_COLOR = {
    "Water": "#4488CC",
    "Fire": "#CC4444",
    "Wood": "#44AA44",
    "Metal": "#888888",
    "Earth": "#CC9944",
}

PHASES = ["Water", "Fire", "Wood", "Metal", "Earth"]


def phase_of(n: int) -> str:
    return RESIDUE_STYLE[n % 5]["name"]


def residue_1based(n: int) -> int:
    r = n % 5
    return 5 if r == 0 else r


def build_positions() -> dict[int, tuple[float, float]]:
    """visualize.py와 동일한 기하 좌표: 중심 7 = (0,0), 세 축 방향으로 등간격 배치."""
    positions: dict[int, tuple[float, float]] = {CENTER: (0.0, 0.0)}
    for axis_name, nodes in AXES.items():
        angle = math.radians(AXIS_ANGLE[axis_name])
        for i, node in enumerate(nodes):
            if node == CENTER:
                continue
            dist = 3 - i
            positions[node] = (
                dist * math.cos(angle) * SPACING,
                dist * math.sin(angle) * SPACING,
            )
    return positions


POSITIONS = build_positions()

# 그래프 거리(중심으로부터의 단계)에 따른 동심 고리 d1, d2, d3
RINGS: dict[int, list[int]] = {1: [], 2: [], 3: []}
for node, (x, y) in POSITIONS.items():
    if node == CENTER:
        continue
    d = round(math.hypot(x, y) / SPACING)
    RINGS[d].append(node)
for d in RINGS:
    RINGS[d].sort()

RING_LABELS = {1: "내륜(d1)", 2: "중륜(d2)", 3: "외륜(d3)"}


def spokes_of(axis_nodes: list[int]) -> tuple[list[int], list[int]]:
    """축을 중심 기준 양쪽 반직선(스포크)으로 분할."""
    idx = axis_nodes.index(CENTER)
    return axis_nodes[:idx], axis_nodes[idx + 1:]


def antipodal_pairs(axis_nodes: list[int]) -> list[tuple[int, int, int]]:
    """축의 중심 대칭 쌍 (레벨 k, 왼쪽값, 오른쪽값)."""
    idx = axis_nodes.index(CENTER)
    return [(k, axis_nodes[idx - k], axis_nodes[idx + k]) for k in range(1, idx + 1)]


# ============================================================
# 2. 그래프 구성
# ============================================================

EDGES: list[tuple[int, int]] = []
for nodes in AXES.values():
    for i in range(len(nodes) - 1):
        EDGES.append((nodes[i], nodes[i + 1]))

G = nx.Graph()
G.add_nodes_from(range(1, 20))
G.add_edges_from(EDGES)
for n in G.nodes():
    G.nodes[n]["phase"] = phase_of(n)


def role_of(n: int) -> str:
    if n == CENTER:
        return "중심"
    x, y = POSITIONS[n]
    d = round(math.hypot(x, y) / SPACING)
    return f"d{d}"


# ============================================================
# 3. 조합론·그래프 이론 분석
# ============================================================

def validate():
    """원본 데이터의 기본 불변량을 검산. 하나라도 어긋나면 즉시 실패."""
    all_values = [v for nodes in AXES.values() for v in nodes if v != CENTER] + [CENTER]
    if sorted(all_values) != list(range(1, 20)):
        raise ValueError("1~19가 각각 한 번씩 사용되어야 함")
    total = sum(all_values)
    if total != 190:
        raise ValueError(f"전체 합은 190이어야 함: {total}")
    for axis_name, nodes in AXES.items():
        if len(nodes) != 7:
            raise ValueError(f"{DISPLAY_LABELS[axis_name]}은 7칸이어야 함")
        if sum(nodes) != 68:
            raise ValueError(f"{DISPLAY_LABELS[axis_name]} 합은 68이어야 함: {sum(nodes)}")
        if nodes.count(CENTER) != 1:
            raise ValueError(f"{DISPLAY_LABELS[axis_name]}은 중심 7을 정확히 한 번 포함해야 함")
    # 중복 계수 검산: 3축 합계 = 전체 합 + 중심 중복분
    k_times_s = 3 * 68
    duplication = 2 * CENTER
    if k_times_s != total + duplication:
        raise ValueError(f"3 × 68 = {k_times_s} ≠ 190 + {duplication}")
    # 고리 합 불변량
    ring_target = (total - CENTER) // 3
    for d, members in RINGS.items():
        if sum(members) != ring_target:
            raise ValueError(f"{RING_LABELS[d]} 합은 {ring_target}이어야 함: {sum(members)}")

    # 검산식 출력
    print("검산식:")
    for axis_name, nodes in AXES.items():
        expr = "+".join(map(str, nodes))
        print(f"  {DISPLAY_LABELS[axis_name]}: {expr} = {sum(nodes)}")
    print(f"  전체 합: 1+2+...+19 = {total}")
    print(f"  3 × 68 = {k_times_s} = {total} + {duplication}  (중심 7이 3회 사용: 19수, 21칸)")
    for d, members in RINGS.items():
        expr = "+".join(map(str, members))
        print(f"  {RING_LABELS[d]}: {expr} = {sum(members)}  (R = (190-7)/3 = {ring_target})")


validate()

print("=" * 60)
print("장책용칠도 (章策用七圖) 현대 그래프·조합론 분석")
print("=" * 60)
print(f"노드 수: {G.number_of_nodes()}")
print(f"엣지 수: {G.number_of_edges()}")
print(f"연결 성분: {nx.number_connected_components(G)}")
print(f"트리 여부: {nx.is_tree(G)}")

deg_seq = sorted([d for _, d in G.degree()], reverse=True)
deg_counter = Counter(d for _, d in G.degree())
print(f"차수 시퀀스: {deg_seq}")
print(f"차수 분포: {dict(sorted(deg_counter.items(), reverse=True))}")

cycle_basis = nx.cycle_basis(G)
print(f"사이클 기반 크기: {len(cycle_basis)} (트리이므로 girth는 정의되지 않음)")

betw = nx.betweenness_centrality(G)
print("\n매개 중심성 (Top 10):")
for n, v in sorted(betw.items(), key=lambda x: -x[1])[:10]:
    print(f"  {n}({DISPLAY_LABELS[phase_of(n)]}, {role_of(n)}): {v:.3f}")

print("\n오행별 수 합:")
WX_SUMS = {}
for r in [1, 2, 3, 4, 5]:
    nodes = [n for n in range(1, 20) if residue_1based(n) == r]
    wx = RESIDUE_STYLE[r % 5]["name"]
    WX_SUMS[wx] = sum(nodes)
    print(f"  {DISPLAY_LABELS[wx]}({wx}): 합={sum(nodes)}, 수들={nodes}")

print("\n축별 오행 분포:")
for axis_name, nodes in AXES.items():
    counts = Counter(phase_of(v) for v in nodes)
    counts_ko = {DISPLAY_LABELS[k]: v for k, v in counts.items()}
    print(f"  {DISPLAY_LABELS[axis_name]}: {counts_ko}")

# 오행 엣지 분류 (상생 / 상극 / 동질)
GENERATION = [
    ("Water", "Wood"), ("Wood", "Fire"), ("Fire", "Earth"),
    ("Earth", "Metal"), ("Metal", "Water"),
]
OVERCOMING = [
    ("Water", "Fire"), ("Fire", "Metal"), ("Metal", "Wood"),
    ("Wood", "Earth"), ("Earth", "Water"),
]


def classify_edge(u: int, v: int) -> str:
    wu, wv = phase_of(u), phase_of(v)
    if wu == wv:
        return "same_phase"
    if (wu, wv) in GENERATION or (wv, wu) in GENERATION:
        return "generation"
    if (wu, wv) in OVERCOMING or (wv, wu) in OVERCOMING:
        return "overcoming"
    return "neutral"


wx_edge_counts: dict[str, int] = {}
for u, v in G.edges():
    key = classify_edge(u, v)
    wx_edge_counts[key] = wx_edge_counts.get(key, 0) + 1

print("\n오행 엣지 분포:")
for key, cnt in wx_edge_counts.items():
    print(f"  {DISPLAY_LABELS[key]}: {cnt} ({cnt / G.number_of_edges() * 100:.1f}%)")


# ============================================================
# 4. 위치 기반 분석 (고리 / 스포크 / 반대편 쌍)
# ============================================================

print("\n고리별 합:")
RING_SUMS = {d: sum(members) for d, members in RINGS.items()}
for d, s in RING_SUMS.items():
    print(f"  {RING_LABELS[d]}: {s}")

print("\n스포크(반직선)별 합:")
SPOKES: dict[str, list[int]] = {}
SPOKE_LABELS = {
    ("axis_vertical", 0): "수직 상", ("axis_vertical", 1): "수직 하",
    ("axis_150", 0): "150° 좌상", ("axis_150", 1): "150° 우하",
    ("axis_30", 0): "30° 우상", ("axis_30", 1): "30° 좌하",
}
for axis_name, nodes in AXES.items():
    for side, spoke in enumerate(spokes_of(nodes)):
        label = SPOKE_LABELS[(axis_name, side)]
        SPOKES[label] = spoke
        print(f"  {label}: {spoke} 합={sum(spoke)}")
spoke_sums_sorted = sorted(sum(s) for s in SPOKES.values())
print(f"  스포크 합 정렬: {spoke_sums_sorted} (연속 6정수: {spoke_sums_sorted == list(range(28, 34))})")

print("\n축별 반대편 쌍 합 (레벨 d1, d2, d3):")
PAIR_SUM_MATRIX: dict[str, list[int]] = {}
for axis_name, nodes in AXES.items():
    pair_sums = []
    for k, a, b in antipodal_pairs(nodes):
        pair_sums.append(a + b)
        print(f"  {DISPLAY_LABELS[axis_name]} d{k}: {a}+{b} = {a + b}")
    PAIR_SUM_MATRIX[axis_name] = pair_sums
    print(f"  {DISPLAY_LABELS[axis_name]} 쌍 합계: {sum(pair_sums)} (+중심 7 = {sum(pair_sums) + CENTER})")
col_sums = [sum(PAIR_SUM_MATRIX[a][i] for a in AXES) for i in range(3)]
print(f"  레벨별(열) 합: {col_sums}  → 행 합 = 열 합 = 61")


# ============================================================
# 5. 일반화 가족 (a축 × L칸 별형)
# ============================================================

# 같은 별형 가족: 범수용오도(a=2, L=5), 장책용칠도(a=3, L=7), 중상용구도(a=4, L=9)
FAMILY = [
    ("범수용오도(範數用五圖)", 2, 5),
    ("장책용칠도(章策用七圖)", 3, 7),
    ("중상용구도(中上用九圖)", 4, 9),
]
print("\n일반화 가족 (a축 × L칸, 중심 L, N = a(L-1)+1):")
FAMILY_ROWS = []
for name, a, L in FAMILY:
    N = a * (L - 1) + 1
    T = N * (N + 1) // 2
    S = (T + (a - 1) * L) // a
    R = (T - L) // a
    FAMILY_ROWS.append((name, a, L, N, T, S, R))
    print(f"  {name}: a={a}, L={L}, N={N}, T={T}, 축합 S={S}, 고리합 R={R}")
    if a == 3:
        assert (N, T, S, R) == (19, 190, 68, 61), "장책용칠도 매개변수 불일치"


# ============================================================
# 6. 그래프 스펙트럼 분석
# ============================================================

nodelist = sorted(G.nodes())
adj = nx.to_numpy_array(G, nodelist=nodelist)
eigenvalues = np.linalg.eigvalsh(adj)
lambda_max = float(max(eigenvalues))
lambda_min = float(min(eigenvalues))
print(f"\n인접 행렬 고유값: λ_max = {lambda_max:.4f}, λ_min = {lambda_min:.4f}")
print(f"  이분그래프(트리) 대칭성: λ_min = -λ_max → {abs(lambda_min + lambda_max) < 1e-9}")


# ============================================================
# 7. 시각화
# ============================================================

AXIS_COLORS = {"axis_vertical": "#CC4444", "axis_150": "#4488CC", "axis_30": "#44AA44"}


def draw_axis_lines(ax, linewidth=2.5, alpha=0.7):
    for axis_name, nodes in AXES.items():
        for i in range(len(nodes) - 1):
            x1, y1 = POSITIONS[nodes[i]]
            x2, y2 = POSITIONS[nodes[i + 1]]
            ax.plot(
                [x1, x2], [y1, y2],
                color=AXIS_COLORS[axis_name], linewidth=linewidth, alpha=alpha, zorder=1,
            )


def draw_nodes(ax, highlight_values=None, node_radius=0.30, fontsize=10):
    for value, (x, y) in POSITIONS.items():
        style = RESIDUE_STYLE[value % 5]
        edge = style["edge"]
        lw = 2.0
        if value == CENTER:
            edge = "#AA0000"
            lw = 3.5
        if highlight_values and value in highlight_values:
            edge = "red"
            lw = 3.5
        ax.add_patch(
            plt.Circle((x, y), node_radius, facecolor=style["face"],
                       edgecolor=edge, linewidth=lw, zorder=2)
        )
        ax.text(x, y, str(value), ha="center", va="center",
                fontsize=fontsize, fontweight="bold", zorder=3)


def draw_ring_guides(ax):
    for d, label in RING_LABELS.items():
        r = d * SPACING
        ax.add_patch(
            plt.Circle((0, 0), r, fill=False, edgecolor="#999999",
                       linewidth=1.2, linestyle=(0, (4, 4)), zorder=0)
        )
        ax.text(r * math.cos(math.radians(45)), r * math.sin(math.radians(45)) + 0.10,
                f"{label} Σ=61", fontsize=9, color="#666666")


def wuxing_legend(ax, loc="lower right"):
    legend_elements = [
        mpatches.Patch(facecolor=PHASE_COLOR[wx], edgecolor="black",
                       label=f"{DISPLAY_LABELS[wx]}({wx[0] if wx != 'Wood' else 'Wd'})")
        for wx in PHASES
    ]
    ax.legend(handles=legend_elements, loc=loc, fontsize=10, framealpha=0.9)


# --- 01: 원본 그래프 ---
fig, ax = plt.subplots(figsize=(10, 10))
draw_ring_guides(ax)
draw_axis_lines(ax)
draw_nodes(ax)
for axis_name, nodes in AXES.items():
    end = nodes[0]
    x, y = POSITIONS[end]
    ax.text(x * 1.16, y * 1.16, f"{DISPLAY_LABELS[axis_name]}\nΣ=68",
            ha="center", va="center", fontsize=10, color=AXIS_COLORS[axis_name],
            fontweight="bold")
ax.set_title(
    "장책용칠도(章策用七圖) — 원본 3축 구조\n3축 · 7칸 · 축 합 68 · 전체 합 190 · 중심 7 공유",
    fontsize=15, fontweight="bold",
)
ax.set_xlim(-4.6, 4.6)
ax.set_ylim(-4.6, 4.6)
ax.set_aspect("equal")
ax.axis("off")
wuxing_legend(ax)
save_fig("01_original_graph.png")
plt.close()

# --- 02: 오행별 서브그래프 분해 ---
fig, axes = plt.subplots(2, 3, figsize=(16, 11))
axes = axes.flatten()
ax = axes[0]
draw_axis_lines(ax, linewidth=1.5, alpha=0.5)
draw_nodes(ax)
ax.set_title("전체 그래프", fontsize=13, fontweight="bold")
ax.set_xlim(-4.6, 4.6)
ax.set_ylim(-4.6, 4.6)
ax.set_aspect("equal")
ax.axis("off")

for idx, wx in enumerate(PHASES):
    ax = axes[idx + 1]
    draw_axis_lines(ax, linewidth=1.0, alpha=0.25)
    wx_nodes = [n for n in range(1, 20) if phase_of(n) == wx]
    for n in range(1, 20):
        x, y = POSITIONS[n]
        if n in wx_nodes:
            ax.add_patch(
                plt.Circle((x, y), 0.32, facecolor=PHASE_COLOR[wx],
                           edgecolor="black", linewidth=2.5, zorder=2)
            )
            ax.text(x, y, str(n), ha="center", va="center", fontsize=10,
                    fontweight="bold",
                    color="white" if wx in ["Water", "Wood"] else "black", zorder=3)
        else:
            ax.add_patch(
                plt.Circle((x, y), 0.20, facecolor="#F0F0F0",
                           edgecolor="#CCCCCC", linewidth=1, zorder=1)
            )
            ax.text(x, y, str(n), ha="center", va="center", fontsize=7,
                    color="#AAAAAA", zorder=2)
    ax.set_title(f"{DISPLAY_LABELS[wx]} · {len(wx_nodes)}개 · 합 {WX_SUMS[wx]}",
                 fontsize=12, fontweight="bold", color=PHASE_COLOR[wx])
    ax.set_xlim(-4.6, 4.6)
    ax.set_ylim(-4.6, 4.6)
    ax.set_aspect("equal")
    ax.axis("off")

plt.suptitle("오행(五行)별 서브그래프 분해 — 토·수·화·목·금 순 합 30, 34, 38, 42, 46",
             fontsize=15, fontweight="bold")
plt.tight_layout()
save_fig("02_wuxing_decomposition.png")
plt.close()

# --- 03: 인접 행렬 + 스펙트럼 ---
fig, axes = plt.subplots(1, 2, figsize=(15, 6.5))
ax = axes[0]
im = ax.imshow(adj, cmap="YlOrRd", interpolation="nearest")
ax.set_xticks(range(19))
ax.set_yticks(range(19))
ax.set_xticklabels(nodelist, fontsize=7)
ax.set_yticklabels(nodelist, fontsize=7)
plt.colorbar(im, ax=ax, shrink=0.8)
ax.set_title("인접 행렬 (19×19)", fontsize=13, fontweight="bold")

ax = axes[1]
ax.bar(range(len(eigenvalues)), sorted(eigenvalues, reverse=True),
       color="#4488CC", edgecolor="black", alpha=0.8)
ax.axhline(y=0, color="red", linestyle="--", linewidth=1)
ax.set_xlabel("지표", fontsize=11)
ax.set_ylabel("고유값", fontsize=11)
ax.set_title(f"그래프 스펙트럼\nλ_max={lambda_max:.2f}, λ_min={lambda_min:.2f} (트리: 원점 대칭)",
             fontsize=13, fontweight="bold")
ax.grid(True, alpha=0.3)
plt.tight_layout()
save_fig("03_adjacency_spectrum.png")
plt.close()

# --- 04: 사이클 분석 (트리이므로 스포크/고리 구조로 대체) ---
fig, axes = plt.subplots(2, 2, figsize=(15, 13))

ax = axes[0, 0]
for axis_name, nodes in AXES.items():
    for i in range(len(nodes) - 1):
        x1, y1 = POSITIONS[nodes[i]]
        x2, y2 = POSITIONS[nodes[i + 1]]
        ax.plot([x1, x2], [y1, y2], color=AXIS_COLORS[axis_name],
                linewidth=3, alpha=0.8, zorder=1)
draw_nodes(ax)
ax.set_title("6개 스포크(길이 3)의 거미형 트리", fontsize=13, fontweight="bold")
ax.set_xlim(-4.6, 4.6)
ax.set_ylim(-4.6, 4.6)
ax.set_aspect("equal")
ax.axis("off")

ax = axes[0, 1]
draw_ring_guides(ax)
draw_axis_lines(ax, linewidth=1.5, alpha=0.4)
ring_colors = {1: "#44AA44", 2: "#CC9944", 3: "#4488CC"}
for d, members in RINGS.items():
    for n in members:
        x, y = POSITIONS[n]
        ax.add_patch(
            plt.Circle((x, y), 0.32, facecolor=ring_colors[d],
                       edgecolor="black", linewidth=2, zorder=2)
        )
        ax.text(x, y, str(n), ha="center", va="center", fontsize=10,
                fontweight="bold", color="white", zorder=3)
cx, cy = POSITIONS[CENTER]
ax.add_patch(plt.Circle((cx, cy), 0.32, facecolor="#FFCCCC",
                        edgecolor="#AA0000", linewidth=3, zorder=2))
ax.text(cx, cy, str(CENTER), ha="center", va="center", fontsize=10,
        fontweight="bold", zorder=3)
ax.set_title("중심 기준 동심 고리 d1·d2·d3 (각 합 61)", fontsize=13, fontweight="bold")
ax.set_xlim(-4.6, 4.6)
ax.set_ylim(-4.6, 4.6)
ax.set_aspect("equal")
ax.axis("off")

ax = axes[1, 0]
ax.text(
    0.5, 0.5,
    "트리(나무) 그래프 — 사이클 없음\n\n"
    f"노드 {G.number_of_nodes()} · 엣지 {G.number_of_edges()} · 연결 성분 1\n"
    "사이클 기반(cycle basis) = 공집합\n"
    "girth(최소 사이클 길이)는 정의되지 않음\n\n"
    "대신 6개 반지름(스포크)과\n3개 동심 고리(d1, d2, d3)가 구조를 이룬다",
    ha="center", va="center", fontsize=12,
    bbox=dict(boxstyle="round,pad=0.6", facecolor="lightyellow", edgecolor="black"),
)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

ax = axes[1, 1]
levels = ["중심(d0)", "내륜(d1)", "중륜(d2)", "외륜(d3)"]
level_sums = [CENTER] + [RING_SUMS[d] for d in [1, 2, 3]]
bars = ax.bar(levels, level_sums,
              color=["#FFCCCC", ring_colors[1], ring_colors[2], ring_colors[3]],
              edgecolor="black", linewidth=1.5)
ax.axhline(y=61, color="red", linestyle="--", linewidth=2)
ax.text(2.5, 62.5, "61 = (190-7)/3", color="red", fontsize=11, ha="center")
for bar, val in zip(bars, level_sums):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, str(val),
            ha="center", fontsize=12, fontweight="bold")
ax.set_title("거리 레벨별 합", fontsize=13, fontweight="bold")
ax.set_ylabel("합", fontsize=10)
ax.set_ylim(0, 75)

plt.tight_layout()
save_fig("04_cycle_analysis.png")
plt.close()

# --- 05: 중심성 + 합 불변량 ---
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

ax = axes[0, 0]
degrees = dict(G.degree())
nodes_sorted = sorted(G.nodes(), key=lambda n: (degrees[n], n), reverse=True)
colors_sorted = [PHASE_COLOR[phase_of(n)] for n in nodes_sorted]
ax.bar(range(19), [degrees[n] for n in nodes_sorted], color=colors_sorted, edgecolor="black")
ax.set_xticks(range(19))
ax.set_xticklabels([str(n) for n in nodes_sorted], fontsize=7)
ax.set_title("차수 (중심 6 · d1·d2 각 2 · 끝점 1)", fontsize=12, fontweight="bold")
ax.set_ylabel("차수", fontsize=10)

ax = axes[0, 1]
betw_sorted = sorted(G.nodes(), key=lambda n: (betw[n], n), reverse=True)
colors_b = [PHASE_COLOR[phase_of(n)] for n in betw_sorted]
ax.bar(range(19), [betw[n] for n in betw_sorted], color=colors_b, edgecolor="black")
ax.set_xticks(range(19))
ax.set_xticklabels([str(n) for n in betw_sorted], fontsize=7)
ax.set_title("매개 중심성 (중심 7이 압도적)", fontsize=12, fontweight="bold")
ax.set_ylabel("중심성", fontsize=10)

ax = axes[1, 0]
wx_names = PHASES
wx_vals = [WX_SUMS[w] for w in wx_names]
wx_colors_bar = [PHASE_COLOR[w] for w in wx_names]
bars = ax.bar([DISPLAY_LABELS[w] for w in wx_names], wx_vals,
              color=wx_colors_bar, edgecolor="black", linewidth=1.5)
for bar, val in zip(bars, wx_vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, str(val),
            ha="center", fontsize=12, fontweight="bold")
ax.plot(range(5), [30, 34, 38, 42, 46], "o--", color="black", alpha=0.4, linewidth=1.5)
ax.set_title("오행별 수 합 (토·수·화·목·금 순 공차 4의 등차)", fontsize=12, fontweight="bold")
ax.set_ylabel("합", fontsize=10)

ax = axes[1, 1]
axis_names = list(AXES.keys())
axis_sums = [sum(AXES[a]) for a in axis_names]
bars = ax.bar([DISPLAY_LABELS[a] for a in axis_names], axis_sums,
              color=[AXIS_COLORS[a] for a in axis_names], edgecolor="black", linewidth=1.5)
ax.axhline(y=68, color="red", linestyle="--", linewidth=2)
for bar, val in zip(bars, axis_sums):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, str(val),
            ha="center", fontsize=12, fontweight="bold")
ax.set_title("축별 7칸 합 (3 × 68 = 204 = 190 + 2×7)", fontsize=12, fontweight="bold")
ax.set_ylabel("합", fontsize=10)
ax.set_ylim(0, 80)

plt.tight_layout()
save_fig("05_centrality_invariants.png")
plt.close()

# --- 06: 오행 상생상극 ---
fig, axes = plt.subplots(1, 2, figsize=(15, 6.5))
ax = axes[0]
phase_graph = nx.DiGraph()
phase_relations = [(u, v, "generation") for u, v in GENERATION] + \
                  [(u, v, "overcoming") for u, v in OVERCOMING]
for u, v, r in phase_relations:
    phase_graph.add_edge(u, v, relation=r)
wx_pos = {"Water": (0, 2), "Wood": (2, 1), "Fire": (1, -1), "Earth": (-1, -1), "Metal": (-2, 1)}
sheng_edges = [(u, v) for u, v, r in phase_relations if r == "generation"]
ke_edges = [(u, v) for u, v, r in phase_relations if r == "overcoming"]
nx.draw_networkx_edges(phase_graph, wx_pos, edgelist=sheng_edges, edge_color="#44AA44",
                       width=3, alpha=0.8, arrows=True, arrowsize=20,
                       connectionstyle="arc3,rad=0.15", ax=ax)
nx.draw_networkx_edges(phase_graph, wx_pos, edgelist=ke_edges, edge_color="#CC4444",
                       width=2, alpha=0.6, style="--", arrows=True, arrowsize=15,
                       connectionstyle="arc3,rad=-0.15", ax=ax)
wx_node_colors = [PHASE_COLOR[w] for w in phase_graph.nodes()]
nx.draw_networkx_nodes(phase_graph, wx_pos, node_color=wx_node_colors, node_size=3000,
                       edgecolors="black", linewidths=2.5, ax=ax)
nx.draw_networkx_labels(phase_graph, wx_pos,
                        labels={n: DISPLAY_LABELS[n] for n in phase_graph.nodes()},
                        font_size=14, ax=ax)
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
pie_order = ["generation", "overcoming", "same_phase"]
pie_counts = [wx_edge_counts.get(k, 0) for k in pie_order]
colors_pie = ["#44AA44", "#CC4444", "#CC9944"]
ax.pie(pie_counts, labels=[DISPLAY_LABELS[k] for k in pie_order], autopct="%1.1f%%",
       colors=colors_pie, explode=[0.05] * 3,
       textprops={"fontsize": 12, "fontweight": "bold"})
ax.set_title(f"오행 엣지 분포 (N={G.number_of_edges()})", fontsize=13, fontweight="bold")
plt.tight_layout()
save_fig("06_wuxing_relations.png")
plt.close()

# --- 07: 확장 및 일반화 ---
fig, axes = plt.subplots(1, 2, figsize=(15, 6.5))

ax = axes[0]
fam_names = [row[0].split("(")[0] for row in FAMILY_ROWS]
x = np.arange(len(FAMILY_ROWS))
width = 0.35
bars1 = ax.bar(x - width / 2, [row[5] for row in FAMILY_ROWS], width,
               label="축 합 S", color="#4488CC", edgecolor="black")
bars2 = ax.bar(x + width / 2, [row[6] for row in FAMILY_ROWS], width,
               label="고리 합 R", color="#CC9944", edgecolor="black")
for bar in list(bars1) + list(bars2):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
            str(int(bar.get_height())), ha="center", fontsize=11, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels([f"{n}\na={r[1]}, L={r[2]}, N={r[3]}" for n, r in zip(fam_names, FAMILY_ROWS)],
                   fontsize=10)
ax.set_title("별형 가족: N = a(L-1)+1, S = (T+(a-1)L)/a, R = (T-L)/a",
             fontsize=12, fontweight="bold")
ax.legend(fontsize=10)
ax.set_ylabel("합", fontsize=10)

ax = axes[1]
# 세 가족 구성원의 골격(중심 + a축 × (L-1)/2단계) 모식도
offsets = {"범수용오도": (-2.6, 0), "장책용칠도": (0, 0), "중상용구도": (2.8, 0)}
scales = {"범수용오도": 0.5, "장책용칠도": 0.38, "중상용구도": 0.30}
for (name, a, L), (ox, oy) in zip(FAMILY, offsets.values()):
    short = name.split("(")[0]
    sc = scales[short]
    levels_per_spoke = (L - 1) // 2
    for i in range(a):
        ang = math.radians(90 + i * 360 / a)
        for sign in [1, -1]:
            prev = (ox, oy)
            for lev in range(1, levels_per_spoke + 1):
                px = ox + sign * lev * sc * math.cos(ang)
                py = oy + sign * lev * sc * math.sin(ang)
                ax.plot([prev[0], px], [prev[1], py], color="#888888", linewidth=1.2, zorder=1)
                ax.add_patch(plt.Circle((px, py), 0.09, facecolor="white",
                                        edgecolor="#333333", linewidth=1.2, zorder=2))
                prev = (px, py)
    ax.add_patch(plt.Circle((ox, oy), 0.16, facecolor="#FFCCCC",
                            edgecolor="#AA0000", linewidth=2, zorder=3))
    ax.text(ox, oy, str(L), ha="center", va="center", fontsize=8,
            fontweight="bold", zorder=4)
    ax.text(ox, oy - 1.6, f"{short}\na={a}, L={L}, N={a * (L - 1) + 1}",
            ha="center", va="top", fontsize=10, fontweight="bold")
ax.set_xlim(-4.3, 4.3)
ax.set_ylim(-2.6, 1.6)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("별형 골격: 중심 L + a축 × (L-1)/2단계", fontsize=12, fontweight="bold")

plt.tight_layout()
save_fig("07_local_extensions.png")
plt.close()

# --- 08: 위치 패턴 (고리 / 스포크 / 반대편 쌍) ---
fig, axes = plt.subplots(1, 2, figsize=(15, 6.5))

ax = axes[0]
ring_items = [(RING_LABELS[d], RING_SUMS[d]) for d in [1, 2, 3]]
spoke_items = sorted(SPOKES.items(), key=lambda kv: sum(kv[1]))
labels_bar = [k for k, _ in ring_items] + [k for k, _ in spoke_items]
vals_bar = [v for _, v in ring_items] + [sum(s) for _, s in spoke_items]
colors_bar = ["#44AA44"] * 3 + ["#4488CC"] * 6
bars = ax.bar(range(len(vals_bar)), vals_bar, color=colors_bar, edgecolor="black", linewidth=1.2)
ax.axhline(y=61, color="red", linestyle="--", linewidth=2)
ax.text(len(vals_bar) - 1, 62.5, "61", color="red", fontsize=11, ha="right", fontweight="bold")
for bar, val in zip(bars, vals_bar):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, str(val),
            ha="center", fontsize=10, fontweight="bold")
ax.set_xticks(range(len(labels_bar)))
ax.set_xticklabels(labels_bar, fontsize=8, rotation=30, ha="right")
ax.set_title("고리 합(61×3)과 스포크 합(28~33 연속 6정수)", fontsize=12, fontweight="bold")
ax.set_ylabel("합", fontsize=10)
ax.set_ylim(0, 72)

ax = axes[1]
matrix = np.array([PAIR_SUM_MATRIX[a] for a in AXES], dtype=float)
im = ax.imshow(matrix, cmap="YlOrRd", interpolation="nearest", vmin=15, vmax=26)
ax.set_xticks(range(3))
ax.set_yticks(range(3))
ax.set_xticklabels(["d1 쌍", "d2 쌍", "d3 쌍"], fontsize=10)
ax.set_yticklabels([DISPLAY_LABELS[a] for a in AXES], fontsize=10)
for i in range(3):
    for j in range(3):
        ax.text(j, i, int(matrix[i, j]), ha="center", va="center",
                fontsize=13, fontweight="bold")
ax.set_title("반대편 쌍 합 행렬 — 행 합 = 열 합 = 61\n(값은 17·20·21·24뿐, 20 = 2×평균(1..19))",
             fontsize=12, fontweight="bold")
plt.colorbar(im, ax=ax, shrink=0.8)

plt.tight_layout()
save_fig("08_position_patterns.png")
plt.close()

print("\n" + "=" * 60)
print("검증된 핵심 성질 요약")
print("=" * 60)
print(f"  - 사용 수: 1~19 각 1회, 전체 합 190")
print(f"  - 3축 × 7칸, 축 합 68, 중심 7 공유: 3×68 = 204 = 190 + 2×7 (19수, 21칸)")
print(f"  - 그래프: 트리, 19노드 18엣지, 차수 분포 {dict(sorted(deg_counter.items(), reverse=True))}")
print(f"  - 고리 합: d1 = d2 = d3 = 61 = (190-7)/3")
print(f"  - 스포크 합: {spoke_sums_sorted} (28~33 연속), 반대 스포크 쌍 합 61")
print(f"  - 반대편 쌍 합 행렬: 행 합 = 열 합 = 61 (값 17·20·21·24)")
print(f"  - 오행 합: 토30 · 수34 · 화38 · 목42 · 금46 (공차 4 등차)")
print(f"  - 오행 엣지: " + ", ".join(
    f"{DISPLAY_LABELS[k]} {wx_edge_counts.get(k, 0)}" for k in ["generation", "overcoming", "same_phase"]))
print(f"  - 스펙트럼: λ_max = {lambda_max:.4f}, λ_min = {lambda_min:.4f}")
print("\n모든 이미지 생성 완료!")
print(f"출력 디렉토리: {OUTPUT_DIR.resolve()}/")
print("=" * 60)
