#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重儀用六圖 (중의용육도) — 현대 그래프·조합론적 심층 분석

《구수략(九數略)》계열 도상 중 중의용육도(重儀用六圖)를 현대 수학 언어로 재해석.
분석 대상: 1부터 16까지의 수를 4개의 겹치는 6자 그룹(상·하·좌·우)에 배치한 구조.
각 그룹의 합은 51, 인접 그룹은 2개 값을 공유한다.

두 가지 그래프 관점을 사용한다.
  (a) T-숲: 원본 도상에 그려진 4개의 T자 화살표 (엣지 12개, forest)
  (b) 공동 소속 그래프: 같은 그룹에 속한 값 쌍을 모두 연결 (그룹 = K6 클리크)
"""

import itertools
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


def setup_cjk_fonts() -> None:
    """한글/한자 출력을 위한 CJK 폰트 부트스트랩."""
    try:
        font_manager.fontManager.addfont(
            "/usr/share/fonts/naver-nanum-gothic-fonts/NanumGothic.ttf"
        )
    except Exception:
        pass  # NanumGothic이 없으면 아래 폰트 스캔 결과에 의존
    available = {f.name for f in font_manager.fontManager.ttflist}
    preferred = [
        "NanumGothic",
        "NanumBarunGothic",
        "NanumMyeongjo",
        "Noto Sans CJK KR",
        "Noto Sans CJK JP",
        "Noto Serif CJK KR",
        "Malgun Gothic",
        "AppleGothic",
    ]
    chosen = [name for name in preferred if name in available]
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = chosen + ["DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False


setup_cjk_fonts()

os.chdir(Path(__file__).parent)
OUTPUT_DIR = Path(".")


def save_fig(name: str) -> None:
    path = OUTPUT_DIR / name
    plt.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    print(f"[저장] {path}")


# ============================================================
# 1. 원본 데이터 구조화 (visualize.py의 좌표·엣지를 그대로 사용)
# ============================================================

# 16개 노드의 2차원 좌표
POSITIONS = {
    7: (-2.5, 3), 16: (-1, 3.2), 1: (1, 3.2), 6: (2.5, 3),
    13: (-3, 1.5), 11: (-1, 1), 10: (1, 1), 4: (3, 1.5),
    3: (-3, -1.5), 9: (-1, -1), 12: (1, -1), 14: (3, -1.5),
    8: (-2.5, -3), 2: (-1, -3.2), 15: (1, -3.2), 5: (2.5, -3),
}

# 4개의 T자 화살표 엣지 (각 T의 중심이 차수 3)
T_EDGES = [
    # 좌상단 T (중심 7 -> 16, 13, 11)
    (7, 16), (7, 13), (7, 11),
    # 우상단 T (중심 6 -> 1, 10, 4)
    (6, 1), (6, 10), (6, 4),
    # 좌하단 T (중심 8 -> 3, 9, 2)
    (8, 3), (8, 9), (8, 2),
    # 우하단 T (중심 5 -> 12, 14, 15)
    (5, 12), (5, 14), (5, 15),
]

# 합 51을 이루는 4개의 6자 그룹
GROUPS = {
    "top": [7, 16, 1, 6, 11, 10],
    "left": [7, 13, 11, 3, 9, 8],
    "bottom": [8, 2, 9, 12, 15, 5],
    "right": [6, 10, 4, 12, 14, 5],
}

# visualize.py와 동일한 그룹 영역 타원
GROUP_REGIONS = {
    "top": ((0, 2.5), 6.8, 3.0, "#FFD700"),
    "left": ((-2.0, 0), 3.5, 6.8, "#87CEEB"),
    "bottom": ((0, -2.5), 6.8, 3.0, "#3CB371"),
    "right": ((2.0, 0), 3.5, 6.8, "#F08080"),
}

DISPLAY_LABELS = {
    "top": "상단 그룹",
    "left": "좌측 그룹",
    "bottom": "하단 그룹",
    "right": "우측 그룹",
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

TARGET_SUM = 51
TOTAL_SUM = 136

RESIDUE_STYLE = {
    1: {"face": "#E5E5E5", "edge": "#444444", "name": "Water"},
    2: {"face": "#F6D0D0", "edge": "#B54141", "name": "Fire"},
    3: {"face": "#D5E3FA", "edge": "#3D6DB3", "name": "Wood"},
    4: {"face": "#D7D7D7", "edge": "#1F1F1F", "name": "Metal"},
    0: {"face": "#F7E3A0", "edge": "#B58A00", "name": "Earth"},
}

PHASE_COLOR = {
    "Water": "#4488CC",
    "Fire": "#CC4444",
    "Wood": "#44AA44",
    "Metal": "#888888",
    "Earth": "#CC9944",
}

PHASE_HANJA = {"Water": "水", "Fire": "火", "Wood": "木", "Metal": "金", "Earth": "土"}


def phase_of(n: int) -> str:
    return RESIDUE_STYLE[n % 5]["name"]


def residue_1based(n: int) -> int:
    r = n % 5
    return 5 if r == 0 else r


# ============================================================
# 2. 그래프 구성
# ============================================================

# (a) T-숲: 원본 도상의 4개 T자 화살표
G_T = nx.Graph()
G_T.add_nodes_from(range(1, 17))
G_T.add_edges_from(tuple(sorted(e)) for e in T_EDGES)

# (b) 공동 소속 그래프: 같은 그룹에 속한 값 쌍을 모두 연결 (그룹 = K6 클리크)
G_co = nx.Graph()
G_co.add_nodes_from(range(1, 17))
for members in GROUPS.values():
    for u, v in itertools.combinations(sorted(members), 2):
        G_co.add_edge(u, v)

T_CENTERS = sorted(n for n, d in G_T.degree() if d == 3)
T_SPOKES = sorted(n for n, d in G_T.degree() if d == 1)

# 공유 값: 두 그룹에 속하는 8개 값
membership_count = Counter(v for members in GROUPS.values() for v in members)
SHARED_VALUES = sorted(v for v, c in membership_count.items() if c == 2)
UNSHARED_VALUES = sorted(v for v, c in membership_count.items() if c == 1)

# 위치 구조: 외곽 12환(시계방향, 좌상단 7에서 시작)과 내측 4환
PERIMETER = [7, 16, 1, 6, 4, 14, 5, 15, 2, 8, 3, 13]
INNER = [11, 10, 12, 9]


# ============================================================
# 3. 검산
# ============================================================

def validate() -> None:
    all_values = [v for members in GROUPS.values() for v in members]
    distinct = sorted(set(all_values))
    if distinct != list(range(1, 17)):
        raise ValueError(f"값 집합이 1..16이 아님: {distinct}")
    if len(all_values) != 24:
        raise ValueError(f"그룹 소속 횟수 합이 24가 아님: {len(all_values)}")
    if sum(distinct) != TOTAL_SUM:
        raise ValueError(f"전체 합이 {TOTAL_SUM}이 아님: {sum(distinct)}")
    for key, members in GROUPS.items():
        if len(members) != 6:
            raise ValueError(f"{DISPLAY_LABELS[key]}이 6자가 아님: {members}")
        if sum(members) != TARGET_SUM:
            raise ValueError(f"{DISPLAY_LABELS[key]} 합이 {TARGET_SUM}이 아님: {sum(members)}")

    # 인접 그룹의 공유 쌍 검증
    expected_overlaps = {
        ("top", "left"): {7, 11},
        ("top", "right"): {6, 10},
        ("left", "bottom"): {8, 9},
        ("right", "bottom"): {5, 12},
    }
    for (a, b), expected in expected_overlaps.items():
        actual = set(GROUPS[a]) & set(GROUPS[b])
        if actual != expected:
            raise ValueError(f"{a}∩{b} 공유 쌍 불일치: {actual} != {expected}")
    for a, b in itertools.combinations(GROUPS, 2):
        if (a, b) in expected_overlaps or (b, a) in expected_overlaps:
            continue
        if set(GROUPS[a]) & set(GROUPS[b]):
            raise ValueError(f"대각 그룹 {a}∩{b}이 비어 있어야 함")

    duplication = sum(SHARED_VALUES)
    if len(SHARED_VALUES) != 8:
        raise ValueError(f"공유 값이 8개가 아님: {SHARED_VALUES}")
    if 4 * TARGET_SUM != TOTAL_SUM + duplication:
        raise ValueError("중복 검산식 4·S = T + D 불성립")

    print("[검산] 사용 값: 1..16 각 1회 (make 16, use 24) ✓")
    print("[검산] 전체 합: 1+2+...+16 = 136 ✓")
    for key, members in GROUPS.items():
        eq = "+".join(map(str, members))
        print(f"[검산] {DISPLAY_LABELS[key]}: {eq} = {sum(members)} ✓")
    for (a, b), expected in expected_overlaps.items():
        print(f"[검산] {DISPLAY_LABELS[a]} ∩ {DISPLAY_LABELS[b]} = {sorted(expected)} ✓")
    print(f"[검산] 공유 8값 {SHARED_VALUES}의 합 D = {duplication} ✓")
    print(f"[검산] 4 × 51 = {4 * TARGET_SUM} = 136 + {duplication} (k·S = T + D) ✓")


validate()

# ============================================================
# 4. 조합론·그래프 이론 분석
# ============================================================

print("\n" + "=" * 60)
print("重儀用六圖 (중의용육도) 현대 그래프·조합론 분석")
print("=" * 60)

print("\n--- 그래프 요약 ---")
print(f"T-숲: 노드 {G_T.number_of_nodes()}, 엣지 {G_T.number_of_edges()}, "
      f"연결 성분 {nx.number_connected_components(G_T)}")
print(f"공동 소속 그래프: 노드 {G_co.number_of_nodes()}, 엣지 {G_co.number_of_edges()}, "
      f"연결 성분 {nx.number_connected_components(G_co)}")

deg_T = Counter(d for _, d in G_T.degree())
deg_co = Counter(d for _, d in G_co.degree())
print(f"차수 분포(T-숲): {dict(sorted(deg_T.items()))}")
print(f"  T 중심(차수 3): {T_CENTERS} (합 {sum(T_CENTERS)})")
print(f"  T 스포크(차수 1): {T_SPOKES} (합 {sum(T_SPOKES)})")
print(f"차수 분포(공동 소속): {dict(sorted(deg_co.items()))}")


def girth(G: nx.Graph) -> int | None:
    """각 엣지를 제거하고 최단 경로를 재는 방식으로 최소 사이클 길이 계산."""
    best = None
    for u, v in G.edges():
        H = G.copy()
        H.remove_edge(u, v)
        try:
            d = nx.shortest_path_length(H, u, v)
        except nx.NetworkXNoPath:
            continue
        if best is None or d + 1 < best:
            best = d + 1
    return best


girth_T = girth(G_T)
girth_co = girth(G_co)
cycle_rank_co = G_co.number_of_edges() - G_co.number_of_nodes() + nx.number_connected_components(G_co)
print(f"\nGirth(T-숲): {girth_T} (forest이므로 사이클 없음)")
print(f"Girth(공동 소속): {girth_co}, 사이클 랭크: {cycle_rank_co}")

betw_co = nx.betweenness_centrality(G_co)
betw_T = nx.betweenness_centrality(G_T)
print("\n매개 중심성 Top 10 (공동 소속 그래프):")
for n, v in sorted(betw_co.items(), key=lambda x: (-x[1], x[0]))[:10]:
    shared = "공유" if n in SHARED_VALUES else "비공유"
    print(f"  {n}({DISPLAY_LABELS[phase_of(n)]}, {shared}): {v:.4f}")
print("매개 중심성 (T-숲, 0이 아닌 노드):")
for n, v in sorted(betw_T.items(), key=lambda x: (-x[1], x[0])):
    if v > 0:
        print(f"  {n}({DISPLAY_LABELS[phase_of(n)]}, T 중심): {v:.4f}")


# --- 보수 쌍(합 17 = N+1) 완전매칭 검사 ---
def perfect_matchings(values: tuple[int, ...]):
    if not values:
        yield []
        return
    first = values[0]
    for i in range(1, len(values)):
        second = values[i]
        rest = values[1:i] + values[i + 1:]
        for matching in perfect_matchings(rest):
            yield [(first, second)] + matching


def complement_matching(values: list[int], target: int):
    for matching in perfect_matchings(tuple(sorted(values))):
        if all(a + b == target for a, b in matching):
            return matching
    return None


print("\n--- 그룹별 보수 쌍(합 17) 완전매칭 ---")
COMPLEMENT_MATCHINGS = {}
for key, members in GROUPS.items():
    matching = complement_matching(members, 17)
    COMPLEMENT_MATCHINGS[key] = matching
    if matching:
        pairs = ", ".join(f"({a},{b})" for a, b in matching)
        print(f"  {DISPLAY_LABELS[key]}: {pairs} — 3쌍 모두 합 17")
    else:
        print(f"  {DISPLAY_LABELS[key]}: 합 17 완전매칭 불가 (15개 매칭 전수 조사)")

print("\n--- 공유 쌍 합 ---")
SHARED_PAIR_SUMS = {}
for (a, b), pair in {
    ("top", "left"): (7, 11),
    ("top", "right"): (6, 10),
    ("left", "bottom"): (8, 9),
    ("right", "bottom"): (5, 12),
}.items():
    SHARED_PAIR_SUMS[pair] = pair[0] + pair[1]
    print(f"  {DISPLAY_LABELS[a]} ∩ {DISPLAY_LABELS[b]} = {pair}: 합 {pair[0] + pair[1]}")

print("\n--- 위치 구조 합 ---")
print(f"  외곽 12환 {PERIMETER}: 합 {sum(PERIMETER)}")
print(f"  내측 4환(직사각형) {INNER}: 합 {sum(INNER)}")
print(f"  T 중심 4값 {T_CENTERS}: 합 {sum(T_CENTERS)} (연속 4정수)")
print(f"  T 스포크 12값: 합 {sum(T_SPOKES)}")
print(f"  공유 8값: 합 {sum(SHARED_VALUES)}, 비공유 8값 {UNSHARED_VALUES}: 합 {sum(UNSHARED_VALUES)}")

# y 좌표별 행 합 (위에서 아래로)
rows: dict[float, list[int]] = {}
for value, (x, y) in POSITIONS.items():
    rows.setdefault(y, []).append(value)
ROW_SUMS = []
print("\n--- y 좌표별 행 합 (위에서 아래로) ---")
for y in sorted(rows, reverse=True):
    vals = sorted(rows[y])
    ROW_SUMS.append(sum(vals))
    print(f"  y={y:+.1f}: {vals} 합 {sum(vals)}")
print(f"  행 합 수열: {ROW_SUMS} — 회문 여부: {ROW_SUMS == ROW_SUMS[::-1]}")

# 좌우 거울 쌍 (x -> -x)
pos_to_value = {pos: value for value, pos in POSITIONS.items()}
print("\n--- 좌우 거울 쌍 (x ↔ -x) ---")
MIRROR_PAIR_SUMS = []
seen = set()
for value, (x, y) in POSITIONS.items():
    if value in seen:
        continue
    mirror = pos_to_value[(-x, y)]
    seen.add(value)
    seen.add(mirror)
    MIRROR_PAIR_SUMS.append(value + mirror)
    print(f"  ({value},{mirror}): 합 {value + mirror}")
print(f"  거울 쌍 합 분포: {Counter(MIRROR_PAIR_SUMS)}")

# ============================================================
# 5. 오행(五行) mod 5 분석
# ============================================================

print("\n--- 오행별 분류 및 합 ---")
WX_SUMS = {}
for r in [1, 2, 3, 4, 5]:
    nodes = [n for n in range(1, 17) if residue_1based(n) == r]
    wx = RESIDUE_STYLE[r % 5]["name"]
    WX_SUMS[wx] = sum(nodes)
    print(f"  {DISPLAY_LABELS[wx]}({PHASE_HANJA[wx]}, mod5={r}): {nodes} 합 {sum(nodes)}")

print("\n--- 그룹별 오행 분포 ---")
GROUP_WX_DIST = {}
for key, members in GROUPS.items():
    counts = Counter(phase_of(v) for v in members)
    GROUP_WX_DIST[key] = counts
    counts_ko = {DISPLAY_LABELS[k]: v for k, v in sorted(counts.items())}
    print(f"  {DISPLAY_LABELS[key]}: {counts_ko}")

GENERATION = [
    ("Wood", "Fire"), ("Fire", "Earth"), ("Earth", "Metal"),
    ("Metal", "Water"), ("Water", "Wood"),
]
OVERCOMING = [
    ("Wood", "Earth"), ("Earth", "Water"), ("Water", "Fire"),
    ("Fire", "Metal"), ("Metal", "Wood"),
]


def classify_edge(u: int, v: int) -> str:
    wu, wv = phase_of(u), phase_of(v)
    if wu == wv:
        return "same_phase"
    pair = (wu, wv)
    if pair in GENERATION or (wv, wu) in GENERATION:
        return "generation"
    if pair in OVERCOMING or (wv, wu) in OVERCOMING:
        return "overcoming"
    return "neutral"


def classify_graph_edges(G: nx.Graph) -> Counter:
    counts: Counter = Counter()
    for u, v in G.edges():
        counts[classify_edge(u, v)] += 1
    return counts


wx_edges_T = classify_graph_edges(G_T)
wx_edges_co = classify_graph_edges(G_co)
print("\n--- 오행 엣지 관계 분류 ---")
for label, G, counts in [("T-숲", G_T, wx_edges_T), ("공동 소속", G_co, wx_edges_co)]:
    total = G.number_of_edges()
    print(f"  [{label}, 엣지 {total}개]")
    for key in ["generation", "overcoming", "same_phase", "neutral"]:
        cnt = counts.get(key, 0)
        if cnt or key != "neutral":
            print(f"    {DISPLAY_LABELS[key]}: {cnt} ({100 * cnt / total:.1f}%)")

# ============================================================
# 6. 스펙트럼 분석
# ============================================================

A_co = nx.to_numpy_array(G_co, nodelist=list(range(1, 17)))
A_T = nx.to_numpy_array(G_T, nodelist=list(range(1, 17)))
eig_co = np.linalg.eigvalsh(A_co)
eig_T = np.linalg.eigvalsh(A_T)
print("\n--- 그래프 스펙트럼 ---")
print(f"  공동 소속 그래프: λ_max = {eig_co[-1]:.4f}, λ_min = {eig_co[0]:.4f}")
print(f"  T-숲: λ_max = {eig_T[-1]:.4f} (= √3, 중복 4), λ_min = {eig_T[0]:.4f} (= -√3, 중복 4)")

# ============================================================
# 7. 시각화
# ============================================================


def draw_group_regions(ax, with_sum_labels: bool = True) -> None:
    for key, (center, w, h, color) in GROUP_REGIONS.items():
        ax.add_patch(
            mpatches.Ellipse(
                center, w, h,
                facecolor=color, alpha=0.15, edgecolor=color, linewidth=1.2, zorder=0,
            )
        )
    if with_sum_labels:
        label_font = {"weight": "bold", "color": "#333333"}
        ax.text(0, 4.35, "합 = 51", ha="center", fontdict=label_font, fontsize=12)
        ax.text(-4.35, 0, "합 = 51", va="center", rotation=90, fontdict=label_font, fontsize=12)
        ax.text(0, -4.35, "합 = 51", ha="center", fontdict=label_font, fontsize=12)
        ax.text(4.35, 0, "합 = 51", va="center", rotation=-90, fontdict=label_font, fontsize=12)


def draw_t_edges(ax, color="#333333", lw=2.2, alpha=0.85, zorder=1, per_center=False) -> None:
    center_colors = {7: "#CC4444", 6: "#4488CC", 8: "#44AA44", 5: "#CC9944"}
    for u, v in T_EDGES:
        x1, y1 = POSITIONS[u]
        x2, y2 = POSITIONS[v]
        c = center_colors.get(u if u in T_CENTERS else v, color) if per_center else color
        ax.plot([x1, x2], [y1, y2], color=c, linewidth=lw, alpha=alpha, zorder=zorder)


def draw_nodes(ax, values=None, radius=0.34, fontsize=11, dim_values=None,
               highlight=None, zorder=2) -> None:
    values = values if values is not None else list(POSITIONS)
    for value in values:
        x, y = POSITIONS[value]
        style = RESIDUE_STYLE[value % 5]
        face, edge, lw = style["face"], style["edge"], 2.0
        if dim_values is not None and value in dim_values:
            face, edge, lw = "#F5F5F5", "#CCCCCC", 1.0
        if highlight and value in highlight:
            edge, lw = "red", 3.5
        ax.add_patch(
            plt.Circle((x, y), radius, facecolor=face, edgecolor=edge,
                       linewidth=lw, zorder=zorder)
        )
        text_color = "#AAAAAA" if (dim_values is not None and value in dim_values) else "black"
        ax.text(x, y, str(value), ha="center", va="center", fontsize=fontsize,
                fontweight="bold", color=text_color, zorder=zorder + 1)


def phase_legend(ax, loc="lower right") -> None:
    handles = [
        mpatches.Patch(facecolor=PHASE_COLOR[w], edgecolor="black",
                       label=f"{DISPLAY_LABELS[w]}({PHASE_HANJA[w]})")
        for w in ["Water", "Fire", "Wood", "Metal", "Earth"]
    ]
    ax.legend(handles=handles, loc=loc, fontsize=10, framealpha=0.9)


def setup_geo_ax(ax, title: str) -> None:
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlim(-5.0, 5.0)
    ax.set_ylim(-5.2, 5.2)
    ax.set_aspect("equal")
    ax.axis("off")


# --- 01: 원본 그래프 ---
fig, ax = plt.subplots(figsize=(10, 10))
draw_group_regions(ax)
draw_t_edges(ax)
draw_nodes(ax)
setup_geo_ax(
    ax,
    "重儀用六圖 (중의용육도) — 원본 구조\n"
    "4개 그룹 × 6자 · 각 그룹 합 51 · 전체 합 136 (1~16 각 1회)",
)
phase_legend(ax)
save_fig("01_original_graph.png")
plt.close()

# --- 02: 오행별 서브그래프 분해 ---
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()
ax = axes[0]
draw_group_regions(ax, with_sum_labels=False)
draw_t_edges(ax, color="#CCCCCC", lw=1.5, alpha=0.7)
draw_nodes(ax)
setup_geo_ax(ax, "전체 그래프")

for idx, wx in enumerate(["Water", "Fire", "Wood", "Metal", "Earth"]):
    ax = axes[idx + 1]
    draw_group_regions(ax, with_sum_labels=False)
    draw_t_edges(ax, color="#EEEEEE", lw=1.2, alpha=0.6, zorder=0)
    wx_nodes = [n for n in range(1, 17) if phase_of(n) == wx]
    others = [n for n in range(1, 17) if n not in wx_nodes]
    draw_nodes(ax, values=others, radius=0.26, fontsize=8, dim_values=set(others), zorder=1)
    for n in wx_nodes:
        x, y = POSITIONS[n]
        ax.add_patch(
            plt.Circle((x, y), 0.36, facecolor=PHASE_COLOR[wx], edgecolor="black",
                       linewidth=2.5, zorder=2)
        )
        ax.text(x, y, str(n), ha="center", va="center", fontsize=11,
                fontweight="bold",
                color="white" if wx in ["Water", "Wood"] else "black", zorder=3)
    setup_geo_ax(
        ax,
        f"{DISPLAY_LABELS[wx]}({PHASE_HANJA[wx]}) · {len(wx_nodes)}개 · 합 {WX_SUMS[wx]}",
    )
    ax.title.set_color(PHASE_COLOR[wx])

plt.suptitle("오행(五行)별 서브그래프 분해", fontsize=16, fontweight="bold", y=1.02)
plt.tight_layout()
save_fig("02_wuxing_decomposition.png")
plt.close()

# --- 03: 인접 행렬 + 스펙트럼 ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
im = ax.imshow(A_co, cmap="YlOrRd", interpolation="nearest")
ax.set_xticks(range(16))
ax.set_yticks(range(16))
ax.set_xticklabels(range(1, 17), fontsize=8)
ax.set_yticklabels(range(1, 17), fontsize=8)
plt.colorbar(im, ax=ax, shrink=0.8)
ax.set_title("인접 행렬 (공동 소속 그래프)", fontsize=13, fontweight="bold")

ax = axes[1]
x = np.arange(16)
ax.bar(x - 0.2, sorted(eig_co, reverse=True), width=0.4, color="#4488CC",
       edgecolor="black", alpha=0.85, label="공동 소속 그래프")
ax.bar(x + 0.2, sorted(eig_T, reverse=True), width=0.4, color="#CC4444",
       edgecolor="black", alpha=0.85, label="T-숲 (4 × K(1,3))")
ax.axhline(y=0, color="black", linestyle="--", linewidth=1)
ax.set_xlabel("지표", fontsize=11)
ax.set_ylabel("고유값", fontsize=11)
ax.set_title(
    f"그래프 스펙트럼\n공동 소속 λ_max={eig_co[-1]:.2f}, λ_min={eig_co[0]:.2f} · "
    f"T-숲 λ=±√3≈±1.73",
    fontsize=13,
    fontweight="bold",
)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
plt.tight_layout()
save_fig("03_adjacency_spectrum.png")
plt.close()

# --- 04: 사이클 분석 (T-숲은 forest이므로 구조와 환 레벨을 대신 표시) ---
fig, axes = plt.subplots(2, 2, figsize=(17, 15))

ax = axes[0, 0]
draw_group_regions(ax, with_sum_labels=False)
draw_t_edges(ax, per_center=True, lw=3.0, alpha=0.9)
draw_nodes(ax, highlight=set(T_CENTERS))
setup_geo_ax(ax, "T-숲: 4개의 T-스타 K(1,3)\n사이클 없음(forest) · 중심 7·6·8·5 (차수 3)")

ax = axes[0, 1]
draw_group_regions(ax, with_sum_labels=False)
for u, v in G_co.edges():
    x1, y1 = POSITIONS[u]
    x2, y2 = POSITIONS[v]
    ax.plot([x1, x2], [y1, y2], color="#BBBBBB", linewidth=0.8, alpha=0.5, zorder=0)
triangle = [7, 16, 11]
for i in range(3):
    u, v = triangle[i], triangle[(i + 1) % 3]
    x1, y1 = POSITIONS[u]
    x2, y2 = POSITIONS[v]
    ax.plot([x1, x2], [y1, y2], color="red", linewidth=3.5, alpha=0.9, zorder=1)
draw_nodes(ax, highlight=set(triangle))
setup_geo_ax(ax, f"공동 소속 그래프: Girth {girth_co}\n최소 사이클 예시: 7-16-11-7 (상단 그룹 K6 클리크 내)")

ax = axes[1, 0]
per_x = [POSITIONS[v][0] for v in PERIMETER] + [POSITIONS[PERIMETER[0]][0]]
per_y = [POSITIONS[v][1] for v in PERIMETER] + [POSITIONS[PERIMETER[0]][1]]
ax.plot(per_x, per_y, color="#4488CC", linewidth=2, linestyle="--", alpha=0.8, zorder=1)
inn_x = [POSITIONS[v][0] for v in INNER] + [POSITIONS[INNER[0]][0]]
inn_y = [POSITIONS[v][1] for v in INNER] + [POSITIONS[INNER[0]][1]]
ax.plot(inn_x, inn_y, color="#CC4444", linewidth=2, linestyle="--", alpha=0.8, zorder=1)
draw_nodes(ax, values=PERIMETER, zorder=2)
draw_nodes(ax, values=INNER, zorder=2, highlight=set(INNER))
setup_geo_ax(ax, f"환 레벨: 외곽 12환 Σ={sum(PERIMETER)} · 내측 4환 Σ={sum(INNER)}")
ring_handles = [
    Line2D([0], [0], color="#4488CC", lw=2, linestyle="--", label=f"외곽 12환 (Σ={sum(PERIMETER)})"),
    Line2D([0], [0], color="#CC4444", lw=2, linestyle="--", label=f"내측 4환 (Σ={sum(INNER)})"),
]
ax.legend(handles=ring_handles, loc="lower right", fontsize=10)

ax = axes[1, 1]
cycle_text = (
    "사이클 구조 요약\n\n"
    "T-숲 (도상에 그려진 엣지)\n"
    "· 연결 성분 4개 (T-스타 K(1,3) × 4)\n"
    "· 사이클 없음 — forest\n\n"
    "공동 소속 그래프 (그룹 = K6 클리크)\n"
    f"· 엣지 56개 = 4 × C(6,2) - 4 (공유 쌍 엣지 중복)\n"
    f"· 사이클 랭크 {cycle_rank_co}\n"
    f"· Girth {girth_co} (삼각형, 예: 7-16-11)"
)
ax.text(0.5, 0.5, cycle_text, ha="center", va="center", fontsize=13,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.6", facecolor="lightyellow", edgecolor="black"))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

plt.tight_layout()
save_fig("04_cycle_analysis.png")
plt.close()

# --- 05: 중심성 + 합 불변량 ---
fig, axes = plt.subplots(2, 2, figsize=(16, 13))

ax = axes[0, 0]
degrees = dict(G_co.degree())
nodes_sorted = sorted(G_co.nodes(), key=lambda n: (-degrees[n], n))
ax.bar(range(16), [degrees[n] for n in nodes_sorted],
       color=[PHASE_COLOR[phase_of(n)] for n in nodes_sorted], edgecolor="black")
ax.set_xticks(range(16))
ax.set_xticklabels([str(n) for n in nodes_sorted], fontsize=8)
ax.set_title("차수 (공동 소속 그래프): 공유 8값은 9, 비공유 8값은 5", fontsize=12, fontweight="bold")
ax.set_ylabel("차수", fontsize=10)

ax = axes[0, 1]
betw_sorted = sorted(G_co.nodes(), key=lambda n: (-betw_co[n], n))
ax.bar(range(16), [betw_co[n] for n in betw_sorted],
       color=[PHASE_COLOR[phase_of(n)] for n in betw_sorted], edgecolor="black")
ax.set_xticks(range(16))
ax.set_xticklabels([str(n) for n in betw_sorted], fontsize=8)
ax.set_title("매개 중심성 (공동 소속 그래프)", fontsize=12, fontweight="bold")
ax.set_ylabel("중심성", fontsize=10)

ax = axes[1, 0]
wx_names = ["Water", "Fire", "Wood", "Metal", "Earth"]
wx_vals = [WX_SUMS[w] for w in wx_names]
ax.bar([f"{DISPLAY_LABELS[w]}({PHASE_HANJA[w]})" for w in wx_names], wx_vals,
       color=[PHASE_COLOR[w] for w in wx_names], edgecolor="black", linewidth=1.5)
ax.set_title("오행별 수 합", fontsize=12, fontweight="bold")
for bar, val in zip(ax.patches, wx_vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, str(val),
            ha="center", fontsize=12, fontweight="bold")

ax = axes[1, 1]
group_keys = list(GROUPS.keys())
group_sums = [sum(GROUPS[k]) for k in group_keys]
group_colors = [GROUP_REGIONS[k][3] for k in group_keys]
ax.bar([DISPLAY_LABELS[k] for k in group_keys], group_sums,
       color=group_colors, edgecolor="black", linewidth=1.5)
ax.axhline(y=TARGET_SUM, color="red", linestyle="--", linewidth=2)
ax.set_ylim(0, 60)
ax.set_title("그룹별 6자 합 (모두 51)", fontsize=12, fontweight="bold")
for bar, val in zip(ax.patches, group_sums):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, str(val),
            ha="center", fontsize=12, fontweight="bold")

plt.tight_layout()
save_fig("05_centrality_invariants.png")
plt.close()

# --- 06: 오행 상생상극 ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
ax = axes[0]
phase_graph = nx.DiGraph()
phase_relations = [(u, v, "generation") for u, v in GENERATION] + [
    (u, v, "overcoming") for u, v in OVERCOMING
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
nx.draw_networkx_labels(
    phase_graph, wx_pos,
    labels={n: f"{DISPLAY_LABELS[n]}\n{PHASE_HANJA[n]}" for n in phase_graph.nodes()},
    font_size=13, ax=ax,
)
rel_handles = [
    Line2D([0], [0], color="#44AA44", lw=3, label="상생(相生)"),
    Line2D([0], [0], color="#CC4444", lw=2, linestyle="--", label="상극(相剋)"),
]
ax.legend(handles=rel_handles, loc="upper right", fontsize=11)
ax.set_title("오행 상생상극 관계도", fontsize=13, fontweight="bold")
ax.set_xlim(-3, 3.5)
ax.set_ylim(-2.5, 3)
ax.axis("off")

ax = axes[1]
categories = ["generation", "overcoming", "same_phase"]
cat_labels = [DISPLAY_LABELS[c] for c in categories]
counts_T = [wx_edges_T.get(c, 0) for c in categories]
counts_co = [wx_edges_co.get(c, 0) for c in categories]
x = np.arange(3)
bars1 = ax.bar(x - 0.2, counts_T, width=0.4, color="#4488CC", edgecolor="black",
               label="T-숲 (12엣지)")
bars2 = ax.bar(x + 0.2, counts_co, width=0.4, color="#CC9944", edgecolor="black",
               label="공동 소속 (56엣지)")
for bars, total in [(bars1, 12), (bars2, 56)]:
    for bar, cnt in zip(bars, [c for c in (counts_T if total == 12 else counts_co)]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.4,
                f"{cnt}\n({100 * cnt / total:.0f}%)", ha="center", fontsize=10,
                fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(cat_labels, fontsize=12)
ax.set_title("오행 엣지 관계 분류", fontsize=13, fontweight="bold")
ax.set_ylabel("엣지 수", fontsize=10)
ax.legend(fontsize=10)
plt.tight_layout()
save_fig("06_wuxing_relations.png")
plt.close()

# --- 07: 일반화 가족 / 확장 개요 ---
fig, axes = plt.subplots(1, 2, figsize=(17, 8))

ax = axes[0]
draw_group_regions(ax, with_sum_labels=False)
draw_nodes(ax, radius=0.28, fontsize=9)
hinge_annotations = [
    ((7, 11), "7·11\nΣ=18", (-2.6, 2.0)),
    ((6, 10), "6·10\nΣ=16", (2.6, 2.0)),
    ((8, 9), "8·9\nΣ=17", (-2.6, -2.0)),
    ((5, 12), "5·12\nΣ=17", (2.6, -2.0)),
]
for (a, b), label, (lx, ly) in hinge_annotations:
    x1, y1 = POSITIONS[a]
    x2, y2 = POSITIONS[b]
    ax.plot([x1, x2], [y1, y2], color="red", linewidth=2.5, alpha=0.8, zorder=2)
    ax.text(lx, ly, label, ha="center", va="center", fontsize=10, fontweight="bold",
            color="red",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="red",
                      alpha=0.9),
            zorder=3)
setup_geo_ax(ax, "구조 청사진: 4개의 6자 그룹 + 4개의 공유 쌍(경첩)")
ax.text(0, -4.9, "검산: 4 × 51 = 204 = 136 + 68   (k·S = T + D, 공유 8값 이중 계산)",
        ha="center", fontsize=12, fontweight="bold", color="#333333")

ax = axes[1]
pair_lines = [
    ("상단 그룹 (합 51 = 3 × 17)", [(16, 1), (6, 11), (7, 10)], True),
    ("하단 그룹 (합 51 = 3 × 17)", [(8, 9), (2, 15), (12, 5)], True),
    ("좌측 그룹", [(7, 10), (13, 4), (11, 6)], False),
    ("우측 그룹", [(6, 11), (10, 7), (4, 13)], False),
]
y_cursor = 0.92
for title, pairs, ok in pair_lines:
    color = "#226622" if ok else "#AA2222"
    ax.text(0.03, y_cursor, title, fontsize=13, fontweight="bold", color=color,
            transform=ax.transAxes)
    y_cursor -= 0.09
    if ok:
        for i, (a, b) in enumerate(pairs):
            x0 = 0.06 + i * 0.31
            ax.text(x0 + 0.09, y_cursor, f"{a} + {b} = 17", fontsize=12,
                    ha="center", transform=ax.transAxes,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="#E8F5E9",
                              edgecolor="#226622"))
    else:
        missing = ", ".join(f"{a}의 보수 {b} 부재" for a, b in pairs[:2]) + " …"
        ax.text(0.06, y_cursor, f"합 17 완전매칭 불가: {missing}", fontsize=11,
                color="#AA2222", transform=ax.transAxes)
    y_cursor -= 0.12
ax.text(0.03, y_cursor - 0.02,
        "보수 쌍(합 17 = N+1) 장치는 4×4 마방진 전통과 같은 원리.\n"
        "상·하단 그룹만 이 장치를 온전히 구현하고,\n"
        "좌·우측 그룹은 공유 쌍 배치를 위해 이를 포기한 비대칭 설계.",
        fontsize=11, transform=ax.transAxes, va="top",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="lightyellow", edgecolor="black"))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")
ax.set_title("일반화 관찰: 보수 쌍(Σ=17) 장치", fontsize=13, fontweight="bold")

plt.tight_layout()
save_fig("07_local_extensions.png")
plt.close()

# --- 08: 위치 패턴 ---
fig, axes = plt.subplots(1, 3, figsize=(21, 7.5))

ax = axes[0]
per_x = [POSITIONS[v][0] for v in PERIMETER] + [POSITIONS[PERIMETER[0]][0]]
per_y = [POSITIONS[v][1] for v in PERIMETER] + [POSITIONS[PERIMETER[0]][1]]
ax.plot(per_x, per_y, color="#4488CC", linewidth=1.8, linestyle="--", alpha=0.7, zorder=1)
inn_x = [POSITIONS[v][0] for v in INNER] + [POSITIONS[INNER[0]][0]]
inn_y = [POSITIONS[v][1] for v in INNER] + [POSITIONS[INNER[0]][1]]
ax.plot(inn_x, inn_y, color="#CC4444", linewidth=1.8, linestyle="--", alpha=0.7, zorder=1)
draw_t_edges(ax, color="#DDDDDD", lw=1.5, alpha=0.8, zorder=0)
draw_nodes(ax, highlight=set(T_CENTERS))
setup_geo_ax(ax, "위치 역할: T 중심(붉은 테두리) · 외곽/내측 환")
role_handles = [
    Line2D([0], [0], marker="o", color="w", markerfacecolor="#F6D0D0",
           markeredgecolor="red", markersize=12, label=f"T 중심 4값 (Σ={sum(T_CENTERS)})"),
    Line2D([0], [0], color="#4488CC", lw=2, linestyle="--", label=f"외곽 12환 (Σ={sum(PERIMETER)})"),
    Line2D([0], [0], color="#CC4444", lw=2, linestyle="--", label=f"내측 4환 (Σ={sum(INNER)})"),
]
ax.legend(handles=role_handles, loc="lower right", fontsize=9)

ax = axes[1]
pos_subsets = [
    ("외곽\n12환", sum(PERIMETER), "#4488CC"),
    ("내측\n4환", sum(INNER), "#CC4444"),
    ("T 중심\n4값", sum(T_CENTERS), "#44AA44"),
    ("T 스포크\n12값", sum(T_SPOKES), "#CC9944"),
    ("공유\n8값", sum(SHARED_VALUES), "#9966CC"),
    ("비공유\n8값", sum(UNSHARED_VALUES), "#669999"),
]
ax.bar([s[0] for s in pos_subsets], [s[1] for s in pos_subsets],
       color=[s[2] for s in pos_subsets], edgecolor="black", linewidth=1.5)
for bar, (_, val, _) in zip(ax.patches, pos_subsets):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5, str(val),
            ha="center", fontsize=12, fontweight="bold")
ax.set_ylim(0, 125)
ax.set_title("위치 부분집합 합", fontsize=13, fontweight="bold")
ax.set_ylabel("합", fontsize=10)
ax.axhline(y=68, color="#9966CC", linestyle=":", linewidth=1.5, alpha=0.8)

ax = axes[2]
y_levels = sorted(rows, reverse=True)
row_labels = []
for y in y_levels:
    vals = sorted(rows[y])
    row_labels.append("+".join(map(str, vals)))
bar_colors = ["#4488CC" if i < 4 else "#CC9944" for i in range(8)]
ax.bar(range(8), ROW_SUMS, color=bar_colors, edgecolor="black", linewidth=1.5)
for i, val in enumerate(ROW_SUMS):
    ax.text(i, val + 0.3, str(val), ha="center", fontsize=12, fontweight="bold")
ax.set_xticks(range(8))
ax.set_xticklabels(row_labels, fontsize=8, rotation=30, ha="right")
ax.set_title(f"y 좌표별 행 합: {ROW_SUMS}\n상하 대칭(회문) 성립", fontsize=13, fontweight="bold")
ax.set_ylabel("행 합", fontsize=10)
ax.set_ylim(0, 25)

plt.tight_layout()
save_fig("08_position_patterns.png")
plt.close()

# ============================================================
# 8. 요약
# ============================================================

print("\n" + "=" * 60)
print("검증된 핵심 성질 요약")
print("=" * 60)
print("1. 1~16 각 1회, 전체 합 136, 4개 그룹 각 합 51")
print("2. k·S = T + D: 4 × 51 = 204 = 136 + 68 (공유 8값 이중 계산)")
print(f"3. T 중심 {T_CENTERS}: 연속 4정수, 합 {sum(T_CENTERS)}")
print(f"4. T 스포크 12값 합 {sum(T_SPOKES)}")
print("5. 상·하단 그룹은 합 17 보수 쌍 3개로 분해, 좌·우측 그룹은 불가 (비대칭)")
print(f"6. 공유 쌍 합: 7+11=18, 6+10=16, 8+9=17, 5+12=17")
print(f"7. 내측 4환 합 {sum(INNER)}, 외곽 12환 합 {sum(PERIMETER)}")
print(f"8. 공유 8값 합 {sum(SHARED_VALUES)} = 비공유 8값 합 {sum(UNSHARED_VALUES)} = 68")
print(f"9. 행 합 회문: {ROW_SUMS}")
print(f"10. 스펙트럼: 공동 소속 λ_max={eig_co[-1]:.4f}, λ_min={eig_co[0]:.4f}; T-숲 λ=±√3")

print("\n" + "=" * 60)
print("모든 이미지 생성 완료!")
print(f"출력 디렉토리: {OUTPUT_DIR.resolve()}/")
print("=" * 60)
