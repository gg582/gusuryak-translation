#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
範數用五圖 (범수용오도) — 현대 그래프·조합론적 심층 분석

《구수략(九數略)》계열 도상 중 범수용오도(範數用五圖)를 현대 수학 언어로 재해석.
분석 대상: 1부터 9까지의 수를 십자(十) 형태의 두 축(가로 5자, 세로 5자)에 배치한
구조. 중심 5는 두 축이 공유한다 (作 9자, 用 10자).
"""

import os
from collections import Counter
from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch

# ============================================================
# 0. 폰트 및 출력 설정
# ============================================================

# CJK 폰트 부트스트랩: NanumGothic을 명시적으로 등록하고, 실패하면
# 시스템에 설치된 Nanum/Noto CJK/Malgun 계열 폰트를 탐색한다.
try:
    fm.fontManager.addfont("/usr/share/fonts/naver-nanum-gothic-fonts/NanumGothic.ttf")
except Exception:
    pass

_preferred = ["NanumGothic", "Noto Sans CJK KR", "Noto Sans CJK JP", "Malgun Gothic"]
_available = {f.name for f in fm.fontManager.ttflist}
_selected = [name for name in _preferred if name in _available]
if not _selected:
    for f in fm.fontManager.ttflist:
        if any(k in f.name for k in ("Nanum", "Noto Sans CJK", "Malgun")):
            _selected.append(f.name)
            break
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = _selected + ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

os.chdir(Path(__file__).parent)
OUTPUT_DIR = Path(".")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_fig(name):
    path = OUTPUT_DIR / name
    plt.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    print(f"[저장] {path}")


# ============================================================
# 1. 원본 데이터 구조화
# ============================================================

# visualize.py의 정방향 좌표를 그대로 사용한다.
POSITIONS = {
    3: (-2, 0), 7: (-1, 0), 5: (0, 0), 4: (1, 0), 6: (2, 0),  # 가로축
    2: (0, 2), 8: (0, 1), 1: (0, -1), 9: (0, -2),             # 세로축
}

AXES = {
    "horizontal": [3, 7, 5, 4, 6],  # 가로축 (왼쪽 → 오른쪽)
    "vertical": [2, 8, 5, 1, 9],    # 세로축 (위 → 아래)
}
AXIS_SUM = 25
CENTER = 5

# 위치 역할: 중심 / 내륜(중간점) / 외륜(끝점), 고리는 12시 방향부터 시계방향.
INNER_RING = [8, 4, 1, 7]
OUTER_RING = [2, 6, 9, 3]
ARMS = {  # 방사선(팔): 같은 방향의 (외곽, 내곽) 쌍
    "top": [2, 8],
    "right": [6, 4],
    "bottom": [9, 1],
    "left": [3, 7],
}
ANTIPODAL = {  # 대향 쌍 (고리 내 정반대 위치)
    "outer_horizontal": (3, 6),
    "outer_vertical": (2, 9),
    "inner_horizontal": (7, 4),
    "inner_vertical": (8, 1),
}

RESIDUE_STYLE = {
    1: {"face": "#E5E5E5", "edge": "#444444", "name": "Water", "ko": "수"},
    2: {"face": "#F6D0D0", "edge": "#B54141", "name": "Fire", "ko": "화"},
    3: {"face": "#D5E3FA", "edge": "#3D6DB3", "name": "Wood", "ko": "목"},
    4: {"face": "#D7D7D7", "edge": "#1F1F1F", "name": "Metal", "ko": "금"},
    0: {"face": "#F7E3A0", "edge": "#B58A00", "name": "Earth", "ko": "토"},
}

DISPLAY_LABELS = {
    "horizontal": "가로축",
    "vertical": "세로축",
    "top": "상(上)",
    "bottom": "하(下)",
    "left": "좌(左)",
    "right": "우(右)",
    "Water": "수",
    "Fire": "화",
    "Wood": "목",
    "Metal": "금",
    "Earth": "토",
    "generation": "상생",
    "overcoming": "상극",
    "same_phase": "동질",
    "neutral": "중립",
    "center": "중심",
    "inner": "내륜(중간점)",
    "outer": "외륜(끝점)",
}

PHASE_COLOR = {
    "Water": "#4488CC",
    "Fire": "#CC4444",
    "Wood": "#44AA44",
    "Metal": "#888888",
    "Earth": "#CC9944",
}

AXIS_COLOR = {"horizontal": "#CC4444", "vertical": "#4488CC"}
ROLE_COLOR = {"center": "#F7E3A0", "inner": "#D5E3FA", "outer": "#F6D0D0"}


def phase_of(n: int) -> str:
    return RESIDUE_STYLE[n % 5]["name"]


def residue_1based(n: int) -> int:
    r = n % 5
    return 5 if r == 0 else r


def role_of(n: int) -> str:
    if n == CENTER:
        return "center"
    if n in INNER_RING:
        return "inner"
    return "outer"


# ============================================================
# 2. 그래프 구성
# ============================================================

# 축 상에서 인접한 셀을 연결한다 (중심 5는 두 축의 공유 노드).
EDGES: list[tuple[int, int]] = []
for line in AXES.values():
    for i in range(len(line) - 1):
        EDGES.append((line[i], line[i + 1]))

# 각 엣지가 어느 축에 속하는지 기록 (중심 연결 엣지는 양쪽 모두 가능하나
# 여기서는 비중심 단말이 속한 축으로 분류한다).
def axis_of_edge(u: int, v: int) -> str:
    if u in AXES["horizontal"] and v in AXES["horizontal"]:
        return "horizontal"
    return "vertical"


G = nx.Graph()
G.add_nodes_from(range(1, 10))
G.add_edges_from(EDGES)
for n in G.nodes():
    G.nodes[n]["phase"] = phase_of(n)
    G.nodes[n]["role"] = role_of(n)


# ============================================================
# 3. 조합론·그래프 이론 분석
# ============================================================

def validate():
    """원본 데이터의 기본 불변량을 검산한다. 하나라도 어긋나면 중단."""
    all_values = list(POSITIONS.keys())
    if sorted(all_values) != list(range(1, 10)):
        raise ValueError("값 집합은 1부터 9까지 각 1회여야 함")
    total = sum(all_values)
    if total != 45:
        raise ValueError(f"전체 합은 45여야 함 (실제: {total})")
    for name, line in AXES.items():
        s = sum(line)
        if s != AXIS_SUM:
            raise ValueError(f"{DISPLAY_LABELS[name]} 합은 {AXIS_SUM}이어야 함 (실제: {s})")
    overlap = set(AXES["horizontal"]) & set(AXES["vertical"])
    if overlap != {CENTER}:
        raise ValueError(f"두 축의 공유 셀은 중심 {CENTER} 하나여야 함 (실제: {overlap})")
    if 2 * AXIS_SUM != total + CENTER:
        raise ValueError("중복 계수 방정식 2·S = T + D 불성립")

    print("검산 통과:")
    for name, line in AXES.items():
        eq = " + ".join(map(str, line))
        print(f"  {DISPLAY_LABELS[name]}: {eq} = {sum(line)}")
    print(f"  중복 계수 방정식: 2 × {AXIS_SUM} = {2 * AXIS_SUM} = {total} + {CENTER}"
          f"  (作 9자, 用 10자 — 중심 {CENTER} 두 번 사용)")


print("=" * 60)
print("範數用五圖 (범수용오도) 현대 그래프·조합론 분석")
print("=" * 60)
validate()

print(f"\n노드 수: {G.number_of_nodes()}")
print(f"엣지 수: {G.number_of_edges()}")
print(f"연결 성분: {nx.number_connected_components(G)}")
print(f"트리 여부: {nx.is_tree(G)}")
print(f"사이클 기반(cycle basis): {nx.cycle_basis(G)}  (트리이므로 공집합)")
print(f"지름(diameter): {nx.diameter(G)}, 반경(radius): {nx.radius(G)},"
      f" 그래프 중심: {nx.center(G)}")

deg_seq = sorted([d for _, d in G.degree()], reverse=True)
deg_counter = Counter(d for _, d in G.degree())
print(f"차수 시퀀스: {deg_seq}")
print("차수 분포: " + ", ".join(f"차수 {d}: {c}개" for d, c in sorted(deg_counter.items(), reverse=True)))
for role, members in [("center", [CENTER]), ("inner", INNER_RING), ("outer", OUTER_RING)]:
    degs = [G.degree(n) for n in members]
    print(f"  {DISPLAY_LABELS[role]} {members}: 차수 {degs}")

betw = nx.betweenness_centrality(G)
print("\n매개 중심성 (Top 10):")
for n, v in sorted(betw.items(), key=lambda x: -x[1])[:10]:
    print(f"  {n}({DISPLAY_LABELS[phase_of(n)]}, {DISPLAY_LABELS[role_of(n)]}): {v:.3f}")

print("\n오행별 수 합:")
for r in [1, 2, 3, 4, 5]:
    nodes = [n for n in range(1, 10) if residue_1based(n) == r]
    wx = RESIDUE_STYLE[r % 5]["name"]
    print(f"  {DISPLAY_LABELS[wx]}({r}): 합={sum(nodes)}, 수들={nodes}")

print("\n축별 오행 분포:")
for name, line in AXES.items():
    counts = Counter(phase_of(v) for v in line)
    counts_ko = {DISPLAY_LABELS[k]: v for k, v in counts.items()}
    seq_ko = "→".join(DISPLAY_LABELS[phase_of(v)] for v in line)
    print(f"  {DISPLAY_LABELS[name]}: {counts_ko}  (배열 순서: {seq_ko})")

# 오행 엣지 분류: 상생(목→화→토→금→수→목) / 상극(목→토→수→화→금→목) / 동질.
GENERATION_PAIRS = [(3, 2), (2, 0), (0, 4), (4, 1), (1, 3)]   # mod-5 잉여 쌍
OVERCOMING_PAIRS = [(3, 0), (0, 1), (1, 2), (2, 4), (4, 3)]


def classify_edge(u: int, v: int) -> str:
    ru, rv = u % 5, v % 5
    if ru == rv:
        return "same_phase"
    if (ru, rv) in GENERATION_PAIRS or (rv, ru) in GENERATION_PAIRS:
        return "generation"
    if (ru, rv) in OVERCOMING_PAIRS or (rv, ru) in OVERCOMING_PAIRS:
        return "overcoming"
    return "neutral"


wx_edge_counts: dict[str, int] = {}
print("\n엣지별 오행 관계:")
for u, v in G.edges():
    key = classify_edge(u, v)
    wx_edge_counts[key] = wx_edge_counts.get(key, 0) + 1
    print(f"  ({u},{v}) [{DISPLAY_LABELS[phase_of(u)]}-{DISPLAY_LABELS[phase_of(v)]},"
          f" {DISPLAY_LABELS[axis_of_edge(u, v)]}]: {DISPLAY_LABELS[key]}")
total_edges = G.number_of_edges()
print("오행 엣지 분포:")
for key in ["generation", "overcoming", "same_phase"]:
    cnt = wx_edge_counts.get(key, 0)
    print(f"  {DISPLAY_LABELS[key]}: {cnt} ({100 * cnt / total_edges:.1f}%)")

# 가로축의 상생 사슬 검증: 왼쪽→오른쪽 잉여열이 목→화→토→금→수인지.
h_residues = [v % 5 for v in AXES["horizontal"]]
h_all_generation = all(
    (h_residues[i], h_residues[i + 1]) in GENERATION_PAIRS for i in range(4)
)
print(f"\n가로축 잉여열(왼쪽→오른쪽): {h_residues}  → 모든 이웃 관계가 상생: {h_all_generation}")

# ============================================================
# 4. 위치 기반 분석 (중심 / 내륜 / 외륜 / 팔 / 대향 쌍)
# ============================================================

inner_sum = sum(INNER_RING)
outer_sum = sum(OUTER_RING)
arm_sums = {name: sum(pair) for name, pair in ARMS.items()}
antipodal_sums = {name: a + b for name, (a, b) in ANTIPODAL.items()}
ring_formula = (45 - CENTER) // 2

print("\n위치 기반 합:")
print(f"  중심: {CENTER}")
print(f"  내륜(중간점) {INNER_RING}: 합 = {inner_sum}")
print(f"  외륜(끝점) {OUTER_RING}: 합 = {outer_sum}")
print(f"  등륜 공식 R = (T − 중심)/2 = (45 − {CENTER})/2 = {ring_formula}")
print("  팔(방사 쌍) 합: " + ", ".join(f"{DISPLAY_LABELS[k]} {ARMS[k]}={s}" for k, s in arm_sums.items()))
print("  대향 쌍 합: " + ", ".join(f"{k}={s}" for k, s in antipodal_sums.items()))
print(f"  대향 쌍 두 개의 합: 9 + 11 = {9 + 11} (= 고리 합)")

# ============================================================
# 5. 일반화 가족 (등축·등륜 별 가족)
# ============================================================

# 범수용오도 값은 본 스크립트에서 직접 검증하고, 나머지 두 도상의 값은
# 각 도상의 원전 주석·스펙에 기록된 주장값으로서 공식과의 일치성만 확인한다.
FAMILY = [
    {"name": "범수용오도", "hanja": "範數用五圖", "axes": 2, "cells": 5,
     "N": 9, "center": 5, "S": 25, "R": 20, "self": True},
    {"name": "장책용칠도", "hanja": "章策用七圖", "axes": 3, "cells": 7,
     "N": 19, "center": 7, "S": 68, "R": 61, "self": False},
    {"name": "중상용구도", "hanja": "象上用九圖", "axes": 4, "cells": 9,
     "N": 33, "center": 9, "S": 147, "R": 138, "self": False},
]

print("\n등축·등륜 별 가족 (N = a(L−1)+1, S = (T+(a−1)L)/a, R = (T−L)/a):")
for m in FAMILY:
    a, L = m["axes"], m["cells"]
    N_pred = a * (L - 1) + 1
    T = m["N"] * (m["N"] + 1) // 2
    S_pred = (T + (a - 1) * L) / a
    R_pred = (T - L) / a
    ok_N = N_pred == m["N"]
    ok_S = S_pred == m["S"]
    ok_R = R_pred == m["R"]
    tag = "본 도상(직접 검증)" if m["self"] else "주장값(공식 일치성만 확인)"
    print(f"  {m['name']}({m['hanja']}): 축 {a} × {L}자, N={m['N']}, 중심={m['center']},"
          f" T={T}, S={m['S']}, R={m['R']}  "
          f"[N 공식 {'일치' if ok_N else '불일치'}, S {'일치' if ok_S else '불일치'},"
          f" R {'일치' if ok_R else '불일치'} — {tag}]")

# ============================================================
# 6. 그래프 스펙트럼
# ============================================================

node_order = sorted(G.nodes(), key=lambda n: (residue_1based(n), n))
adj = nx.to_numpy_array(G, nodelist=node_order)
eigenvalues = np.linalg.eigvalsh(adj)
lam_max = float(max(eigenvalues))
lam_min = float(min(eigenvalues))
print("\n스펙트럼:")
print(f"  노드 순서(오행별): {node_order}")
print(f"  고유값: {np.round(np.sort(eigenvalues)[::-1], 4)}")
print(f"  λ_max = {lam_max:.4f} (√5 = {np.sqrt(5):.4f}), λ_min = {lam_min:.4f}")

# ============================================================
# 7. 시각화
# ============================================================


def draw_axis_bands(ax):
    band_h = FancyBboxPatch(
        (-2.55, -0.52), 5.1, 1.04, boxstyle="round,pad=0.06",
        facecolor=AXIS_COLOR["horizontal"], alpha=0.10,
        edgecolor=AXIS_COLOR["horizontal"], linestyle=(0, (4, 4)), linewidth=1.5, zorder=0,
    )
    band_v = FancyBboxPatch(
        (-0.52, -2.55), 1.04, 5.1, boxstyle="round,pad=0.06",
        facecolor=AXIS_COLOR["vertical"], alpha=0.10,
        edgecolor=AXIS_COLOR["vertical"], linestyle=(0, (4, 4)), linewidth=1.5, zorder=0,
    )
    ax.add_patch(band_h)
    ax.add_patch(band_v)
    ax.text(2.85, 0, f"{DISPLAY_LABELS['horizontal']}\nΣ=25", ha="left", va="center",
            fontsize=11, fontweight="bold", color=AXIS_COLOR["horizontal"])
    ax.text(0, 2.85, f"{DISPLAY_LABELS['vertical']} · Σ=25", ha="center", va="bottom",
            fontsize=11, fontweight="bold", color=AXIS_COLOR["vertical"])


def draw_edges(ax, gray=False, lw=3.2, zorder=1):
    for u, v in EDGES:
        x1, y1 = POSITIONS[u]
        x2, y2 = POSITIONS[v]
        if gray:
            ax.plot([x1, x2], [y1, y2], color="#DDDDDD", linewidth=1.2, zorder=0)
        else:
            ax.plot([x1, x2], [y1, y2], color=AXIS_COLOR[axis_of_edge(u, v)],
                    linewidth=lw, alpha=0.75, zorder=zorder)


def draw_nodes(ax, highlight_values=None, dim_values=None, role_colors=False,
               node_radius=0.30, fontsize=11):
    for value, (x, y) in POSITIONS.items():
        style = RESIDUE_STYLE[value % 5]
        face, edge, lw = style["face"], style["edge"], 2.2
        text_color = "black"
        if role_colors:
            face = ROLE_COLOR[role_of(value)]
            edge = "#333333"
        if dim_values is not None and value in dim_values:
            face, edge, lw = "#F2F2F2", "#CCCCCC", 1.0
            text_color = "#AAAAAA"
        if highlight_values and value in highlight_values:
            edge, lw = "red", 3.2
        ax.add_patch(plt.Circle((x, y), node_radius, facecolor=face, edgecolor=edge,
                                linewidth=lw, zorder=2))
        ax.text(x, y, str(value), ha="center", va="center", fontsize=fontsize,
                fontweight="bold", color=text_color, zorder=3)


def wuxing_legend(ax, loc="lower right"):
    legend_elements = [
        mpatches.Patch(facecolor=PHASE_COLOR[wx], edgecolor="black",
                       label=f"{DISPLAY_LABELS[wx]}({wx[0]})")
        for wx in ["Water", "Fire", "Wood", "Metal", "Earth"]
    ]
    ax.legend(handles=legend_elements, loc=loc, fontsize=10, framealpha=0.9)


XLIM = (-3.1, 4.3)
YLIM = (-3.1, 3.5)

# --- 01: 원본 그래프 ---
fig, ax = plt.subplots(figsize=(10, 9))
draw_axis_bands(ax)
draw_edges(ax)
draw_nodes(ax)
ax.add_patch(plt.Circle((0, 0), 0.44, fill=False, edgecolor="#333333",
                        linewidth=1.5, linestyle=(0, (2, 2)), zorder=1))
ax.text(0.58, 0.55, "중심 5\n(두 축 공유)", ha="left", va="bottom", fontsize=9, color="#333333")
ax.set_title("範數用五圖 (범수용오도) — 원본 십자 구조\n"
             "1~9 각 1회 · 두 축 각 합 25 · 전체 합 45 · 2×25 = 45+5",
             fontsize=15, fontweight="bold")
ax.set_xlim(*XLIM)
ax.set_ylim(*YLIM)
ax.set_aspect("equal")
ax.axis("off")
wuxing_legend(ax)
save_fig("01_original_graph.png")
plt.close()

# --- 02: 오행별 서브그래프 분해 ---
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()
ax = axes[0]
draw_axis_bands(ax)
draw_edges(ax)
draw_nodes(ax)
ax.set_title("전체 그래프", fontsize=13, fontweight="bold")
ax.set_xlim(*XLIM)
ax.set_ylim(*YLIM)
ax.set_aspect("equal")
ax.axis("off")

for idx, wx in enumerate(["Water", "Fire", "Wood", "Metal", "Earth"]):
    ax = axes[idx + 1]
    draw_axis_bands(ax)
    draw_edges(ax, gray=True)
    wx_nodes = [n for n in range(1, 10) if phase_of(n) == wx]
    draw_nodes(ax, dim_values=[n for n in range(1, 10) if n not in wx_nodes])
    for n in wx_nodes:
        x, y = POSITIONS[n]
        ax.add_patch(plt.Circle((x, y), 0.36, facecolor=PHASE_COLOR[wx],
                                edgecolor="black", linewidth=2.5, zorder=3))
        ax.text(x, y, str(n), ha="center", va="center", fontsize=12,
                fontweight="bold", color="white" if wx in ["Water", "Wood"] else "black",
                zorder=4)
    ax.set_title(f"{DISPLAY_LABELS[wx]}({wx[0]}) · {len(wx_nodes)}개 · 합 {sum(wx_nodes)}",
                 fontsize=13, fontweight="bold", color=PHASE_COLOR[wx])
    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.set_aspect("equal")
    ax.axis("off")

plt.suptitle("오행(五行)별 서브그래프 분해 — 각 축은 다섯 오행을 정확히 한 번씩 포함",
             fontsize=16, fontweight="bold", y=1.0)
plt.tight_layout()
save_fig("02_wuxing_decomposition.png")
plt.close()

# --- 03: 인접 행렬 + 스펙트럼 ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
im = ax.imshow(adj, cmap="YlOrRd", interpolation="nearest")
ax.set_xticks(range(9))
ax.set_yticks(range(9))
ax.set_xticklabels(node_order, fontsize=9)
ax.set_yticklabels(node_order, fontsize=9)
wx_sorted = [phase_of(n) for n in node_order]
boundaries = [i - 0.5 for i in range(1, 9) if wx_sorted[i] != wx_sorted[i - 1]]
for b in boundaries:
    ax.axhline(y=b, color="blue", linewidth=1.5, alpha=0.7)
    ax.axvline(x=b, color="blue", linewidth=1.5, alpha=0.7)
plt.colorbar(im, ax=ax, shrink=0.8)
ax.set_title("인접 행렬 (오행별 정렬)", fontsize=13, fontweight="bold")

ax = axes[1]
sorted_ev = sorted(eigenvalues, reverse=True)
ax.bar(range(9), sorted_ev, color="#4488CC", edgecolor="black", alpha=0.85)
ax.axhline(y=0, color="red", linestyle="--", linewidth=1)
for i, v in enumerate(sorted_ev):
    ax.text(i, v + 0.08 if v >= 0 else v - 0.22, f"{v:.2f}", ha="center", fontsize=9)
ax.set_xlabel("지표", fontsize=11)
ax.set_ylabel("고유값", fontsize=11)
ax.set_title(f"그래프 스펙트럼\nλ_max = {lam_max:.4f} (= √5), λ_min = {lam_min:.4f}"
             " — 원점 대칭 (이분 트리)",
             fontsize=13, fontweight="bold")
ax.grid(True, alpha=0.3)
plt.tight_layout()
save_fig("03_adjacency_spectrum.png")
plt.close()

# --- 04: 사이클 분석 (트리이므로 고리·레벨 구조로 대체) ---
fig, axes = plt.subplots(2, 2, figsize=(16, 14))

ax = axes[0, 0]
# 거리 고리(반지름 1, 2)를 점선 원으로 표시
for radius, label in [(1, "내륜 (거리 1)"), (2, "외륜 (거리 2)")]:
    ax.add_patch(plt.Circle((0, 0), radius, fill=False, edgecolor="#999999",
                            linewidth=1.5, linestyle=(0, (5, 5)), zorder=0))
    ax.text(radius * np.cos(np.radians(135)), radius * np.sin(np.radians(135)) + 0.16,
            label, ha="center", fontsize=10, color="#555555")
draw_edges(ax)
draw_nodes(ax, role_colors=True)
ax.set_title("거리별 동심 고리 구조 (트리)", fontsize=13, fontweight="bold")
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect("equal")
ax.axis("off")
role_legend = [
    mpatches.Patch(facecolor=ROLE_COLOR[r], edgecolor="black", label=DISPLAY_LABELS[r])
    for r in ["center", "inner", "outer"]
]
ax.legend(handles=role_legend, loc="lower right", fontsize=10, framealpha=0.9)

ax = axes[0, 1]
# 중심에서의 거리 레벨로 다시 그린 트리 (레이어드 레이아웃)
level_pos = {CENTER: (0, 0)}
level1 = [8, 4, 1, 7]
child_of = {8: 2, 4: 6, 1: 9, 7: 3}
for i, n in enumerate(level1):
    level_pos[n] = (1, 1.5 - i)
    level_pos[child_of[n]] = (2, 1.5 - i)
for n in level1:
    ax.plot([0, 1], [0, level_pos[n][1]], color="#999999", linewidth=2, zorder=1)
    c = child_of[n]
    ax.plot([1, 2], [level_pos[n][1], level_pos[c][1]], color="#999999", linewidth=2, zorder=1)
for n, (x, y) in level_pos.items():
    face = ROLE_COLOR[role_of(n)]
    ax.add_patch(plt.Circle((x, y), 0.16, facecolor=face, edgecolor="#333333",
                            linewidth=2, zorder=2))
    ax.text(x, y, str(n), ha="center", va="center", fontsize=10, fontweight="bold", zorder=3)
for x, label in [(0, "거리 0\n(중심)"), (1, "거리 1\n(내륜)"), (2, "거리 2\n(외륜)")]:
    ax.text(x, -2.2, label, ha="center", fontsize=11, fontweight="bold", color="#555555")
ax.set_title("중심 기준 레벨(거리) 구조", fontsize=13, fontweight="bold")
ax.set_xlim(-0.6, 2.6)
ax.set_ylim(-2.7, 2.1)
ax.set_aspect("equal")
ax.axis("off")

ax = axes[1, 0]
ax.text(
    0.5, 0.5,
    "트리(Tree) 구조\n\n"
    f"노드 9 · 엣지 8 (= 노드 - 1)\n"
    f"연결됨 · 사이클 없음 (사이클 계수 0)\n"
    f"girth: 정의되지 않음\n"
    f"지름 4 (예: 3-7-5-4-6)\n"
    f"반경 2 · 그래프 중심 = 노드 5",
    ha="center", va="center", fontsize=13, fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.6", facecolor="lightyellow", edgecolor="black"),
)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

ax = axes[1, 1]
arm_names = list(ARMS.keys())
arm_vals = [arm_sums[k] for k in arm_names]
bars = ax.bar([DISPLAY_LABELS[k] for k in arm_names], arm_vals,
              color=["#CC4444", "#4488CC", "#44AA44", "#CC9944"],
              edgecolor="black", linewidth=1.5)
ax.axhline(y=10, color="red", linestyle="--", linewidth=2)
for bar, val in zip(bars, arm_vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.15, str(val),
            ha="center", fontsize=13, fontweight="bold")
ax.set_ylim(0, 12.5)
ax.set_title("팔(방사 쌍) 합 — 모두 10 (= 2 × 중심 5)", fontsize=13, fontweight="bold")
ax.set_ylabel("합", fontsize=10)

plt.suptitle("사이클 분석 — 트리이므로 고리·레벨 구조를 대신 보여줌", fontsize=15, fontweight="bold")
plt.tight_layout(rect=[0, 0, 1, 0.97])
save_fig("04_cycle_analysis.png")
plt.close()

# --- 05: 중심성 + 합 불변량 ---
fig, axes = plt.subplots(2, 2, figsize=(16, 13))

ax = axes[0, 0]
degrees = dict(G.degree())
nodes_sorted = sorted(G.nodes(), key=lambda n: (-degrees[n], n))
ax.bar(range(9), [degrees[n] for n in nodes_sorted],
       color=[PHASE_COLOR[phase_of(n)] for n in nodes_sorted], edgecolor="black")
ax.set_xticks(range(9))
ax.set_xticklabels([str(n) for n in nodes_sorted], fontsize=9)
ax.set_title("차수 (중심 5만 차수 4)", fontsize=12, fontweight="bold")
ax.set_ylabel("차수", fontsize=10)

ax = axes[0, 1]
betw_sorted = sorted(G.nodes(), key=lambda n: (-betw[n], n))
ax.bar(range(9), [betw[n] for n in betw_sorted],
       color=[PHASE_COLOR[phase_of(n)] for n in betw_sorted], edgecolor="black")
ax.set_xticks(range(9))
ax.set_xticklabels([str(n) for n in betw_sorted], fontsize=9)
for i, n in enumerate(betw_sorted):
    ax.text(i, betw[n] + 0.015, f"{betw[n]:.3f}", ha="center", fontsize=8)
ax.set_title("매개 중심성 (중심 5 = 6/7 ≈ 0.857)", fontsize=12, fontweight="bold")
ax.set_ylabel("중심성", fontsize=10)

ax = axes[1, 0]
wx_names = ["Water", "Fire", "Wood", "Metal", "Earth"]
wx_vals = [sum(n for n in range(1, 10) if phase_of(n) == wx) for wx in wx_names]
bars = ax.bar([DISPLAY_LABELS[w] for w in wx_names], wx_vals,
              color=[PHASE_COLOR[w] for w in wx_names], edgecolor="black", linewidth=1.5)
for bar, val in zip(bars, wx_vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2, str(val),
            ha="center", fontsize=12, fontweight="bold")
ax.plot(range(4), wx_vals[:4], "o--", color="black", alpha=0.5, linewidth=2)
ax.set_title("오행별 수 합 — 수·화·목·금은 7, 9, 11, 13 (공차 2)", fontsize=12, fontweight="bold")
ax.set_ylabel("합", fontsize=10)

ax = axes[1, 1]
components = {
    "가로축": 25, "세로축": 25, "내륜": inner_sum, "외륜": outer_sum, "전체": 45,
}
bars = ax.bar(list(components.keys()), list(components.values()),
              color=["#CC4444", "#4488CC", ROLE_COLOR["inner"], ROLE_COLOR["outer"], "#333333"],
              edgecolor="black", linewidth=1.5)
for bar, val in zip(bars, list(components.values())):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.7, str(val),
            ha="center", fontsize=12, fontweight="bold")
ax.set_title("구조적 부분집합 합 (축 25 · 고리 20 · 전체 45)", fontsize=12, fontweight="bold")
ax.set_ylabel("합", fontsize=10)
ax.set_ylim(0, 52)

plt.tight_layout()
save_fig("05_centrality_invariants.png")
plt.close()

# --- 06: 오행 상생상극 ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
phase_graph = nx.DiGraph()
phase_relations = [
    ("Wood", "Fire", "generation"),
    ("Fire", "Earth", "generation"),
    ("Earth", "Metal", "generation"),
    ("Metal", "Water", "generation"),
    ("Water", "Wood", "generation"),
    ("Wood", "Earth", "overcoming"),
    ("Earth", "Water", "overcoming"),
    ("Water", "Fire", "overcoming"),
    ("Fire", "Metal", "overcoming"),
    ("Metal", "Wood", "overcoming"),
]
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
class_keys = ["generation", "overcoming", "same_phase"]
class_vals = [wx_edge_counts.get(k, 0) for k in class_keys]
bars = ax.bar([DISPLAY_LABELS[k] for k in class_keys], class_vals,
              color=["#44AA44", "#CC4444", "#CC9944"], edgecolor="black", linewidth=1.5)
for bar, val in zip(bars, class_vals):
    pct = 100 * val / total_edges
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
            f"{val} ({pct:.1f}%)", ha="center", fontsize=12, fontweight="bold")
ax.set_ylim(0, 7.5)
ax.set_title(f"오행 엣지 분류 (전체 {total_edges}개)\n"
             "가로축 4개 엣지는 모두 상생, 상극 2개는 세로축의 중심 인접 엣지",
             fontsize=13, fontweight="bold")
ax.set_ylabel("엣지 수", fontsize=10)

plt.tight_layout()
save_fig("06_wuxing_relations.png")
plt.close()

# --- 07: 확장 및 일반화 ---
fig, axes = plt.subplots(1, 2, figsize=(17, 7.5))

ax = axes[0]
x = np.arange(len(FAMILY))
width = 0.27
metric_vals = {"N (값의 수)": [m["N"] for m in FAMILY],
               "S (축 합)": [m["S"] for m in FAMILY],
               "R (고리 합)": [m["R"] for m in FAMILY]}
metric_colors = {"N (값의 수)": "#888888", "S (축 합)": "#CC4444", "R (고리 합)": "#4488CC"}
for i, (label, vals) in enumerate(metric_vals.items()):
    bars = ax.bar(x + (i - 1) * width, vals, width, label=label,
                  color=metric_colors[label], edgecolor="black")
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2, str(val),
                ha="center", fontsize=9, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels([f"{m['name']}\n축 {m['axes']} × {m['cells']}자 · 중심 {m['center']}"
                    for m in FAMILY], fontsize=10)
ax.set_title("등축·등륜 별 가족\nN = a(L-1)+1 · S = (T+(a-1)L)/a · R = (T-L)/a",
             fontsize=12, fontweight="bold")
ax.legend(fontsize=10)
ax.set_ylabel("값", fontsize=10)

ax = axes[1]
schem_colors = ["#CC4444", "#44AA44", "#4488CC"]
for i, m in enumerate(FAMILY):
    cx = i * 3.2
    a = m["axes"]
    for k in range(a):
        theta = np.pi / 2 - k * np.pi / a
        dx, dy = np.cos(theta), np.sin(theta)
        ax.plot([cx - 1.15 * dx, cx + 1.15 * dx], [-1.15 * dy, 1.15 * dy],
                color=schem_colors[i], linewidth=2.2, alpha=0.8, zorder=1)
    ax.add_patch(plt.Circle((cx, 0), 0.20, facecolor="#F7E3A0", edgecolor="black",
                            linewidth=2, zorder=3))
    ax.text(cx, 0, str(m["center"]), ha="center", va="center", fontsize=9,
            fontweight="bold", zorder=4)
    ax.text(cx, -1.75, f"{m['name']}\n축 {a} × {m['cells']}자 · N={m['N']}\n"
                       f"S={m['S']} · R={m['R']}",
            ha="center", va="top", fontsize=10, fontweight="bold", color=schem_colors[i])
ax.set_xlim(-1.8, 8.2)
ax.set_ylim(-3.3, 1.8)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("등축 별(star) 모식도 — 축 수 a = 2, 3, 4", fontsize=12, fontweight="bold")

plt.tight_layout()
save_fig("07_local_extensions.png")
plt.close()

# --- 08: 위치 패턴 (팔 / 고리 / 대향 쌍) ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

ax = axes[0]
labels = [DISPLAY_LABELS[k] for k in ARMS] + ["내륜", "외륜"]
vals = [arm_sums[k] for k in ARMS] + [inner_sum, outer_sum]
colors = ["#4488CC"] * 4 + [ROLE_COLOR["inner"], ROLE_COLOR["outer"]]
bars = ax.bar(labels, vals, color=colors, edgecolor="black", linewidth=1.5)
ax.axhline(y=10, color="#4488CC", linestyle="--", linewidth=1.5, alpha=0.7)
ax.axhline(y=20, color="#CC4444", linestyle="--", linewidth=1.5, alpha=0.7)
for bar, val in zip(bars, vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(val),
            ha="center", fontsize=12, fontweight="bold")
ax.set_ylim(0, 24)
ax.set_title("팔 합 = 10 (4개), 내륜 합 = 외륜 합 = 20", fontsize=13, fontweight="bold")
ax.set_ylabel("합", fontsize=10)

ax = axes[1]
ap_labels = ["외륜 좌우\n(3,6)", "외륜 상하\n(2,9)", "내륜 좌우\n(7,4)", "내륜 상하\n(8,1)"]
ap_keys = ["outer_horizontal", "outer_vertical", "inner_horizontal", "inner_vertical"]
ap_vals = [antipodal_sums[k] for k in ap_keys]
bars = ax.bar(ap_labels, ap_vals,
              color=[ROLE_COLOR["outer"], ROLE_COLOR["outer"],
                     ROLE_COLOR["inner"], ROLE_COLOR["inner"]],
              edgecolor="black", linewidth=1.5)
for bar, val in zip(bars, ap_vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2, str(val),
            ha="center", fontsize=13, fontweight="bold")
ax.axhline(y=10, color="#999999", linestyle="--", linewidth=1.2)
ax.set_ylim(0, 14)
ax.set_title("대향 쌍 합의 교차: 외륜 9·11, 내륜 11·9\n9 + 11 = 20 = 각 고리의 합",
             fontsize=13, fontweight="bold")
ax.set_ylabel("합", fontsize=10)

plt.tight_layout()
save_fig("08_position_patterns.png")
plt.close()

# ============================================================
# 8. 요약
# ============================================================

print("\n" + "=" * 60)
print("검증된 핵심 성질 요약")
print("=" * 60)
print("✓ 값 집합: 1~9 각 1회, 전체 합 T = 45")
print("✓ 두 축 각 합 S = 25, 중복 계수 방정식 2·25 = 45 + 5 (作 9자, 用 10자)")
print("✓ 그래프: 9노드 8엣지 트리 (중심 차수 4, 중간점 차수 2, 끝점 차수 1)")
print("✓ 매개 중심성: 중심 5 = 0.857, 중간점 = 0.250, 끝점 = 0.000")
print("✓ 각 축은 다섯 오행을 정확히 한 번씩 포함")
print(f"✓ 가로축 잉여열 {h_residues} = 상생 순환 (모든 이웃 상생: {h_all_generation})")
print(f"✓ 오행 엣지: 상생 {wx_edge_counts.get('generation', 0)}개 (75.0%),"
      f" 상극 {wx_edge_counts.get('overcoming', 0)}개 (25.0%), 동질 0개")
print(f"✓ 네 팔 합 모두 10: {arm_vals}")
print(f"✓ 내륜 합 = 외륜 합 = 20 = (45 − 5)/2")
print(f"✓ 대향 쌍 합 교차: {ap_vals} (9 + 11 = 20)")
print(f"✓ 스펙트럼: λ_max = {lam_max:.4f} = √5, λ_min = {lam_min:.4f} (원점 대칭)")

print("\n생성된 파일:")
for f in ["01_original_graph.png", "02_wuxing_decomposition.png",
          "03_adjacency_spectrum.png", "04_cycle_analysis.png",
          "05_centrality_invariants.png", "06_wuxing_relations.png",
          "07_local_extensions.png", "08_position_patterns.png"]:
    print(f"  {f}")
print("모든 이미지 생성 완료!")
