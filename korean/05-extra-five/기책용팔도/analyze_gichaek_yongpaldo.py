#!/usr/bin/env python3
"""기책용팔도(奇策用八圖) 심층 성질 분석.

4개의 팔각형(상·하·좌·우)이 중앙 정사각형을 둘러싸고 인접 팔각형끼리
한 변씩을 공유하는 도안. 값 1..24를 꼭짓점에 배치해 각 팔각형의 합이
100이 되게 한 각득(各得) 계열 도상이다.

분석 항목:
    - 기본 검산 (값 집합, 총합, 팔각형 합, 중복 방정식 kS = T + D)
    - 그래프 구조 (차수 분포, 사이클, 중심성)
    - 오행(五行) mod 5 분해 및 엣지 상생상극 분류
    - 위치 불변량 (중앙 정사각형, 공유 꼭짓점, 마주 보는 쌍)
    - 스펙트럼
    - 일반화 가족

실행하면 01..08 번 그림이 이 디렉터리에 저장된다.
"""

import math
import os
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import Circle, Polygon

# ---------------------------------------------------------------------------
# 0. 한글 폰트 / 출력 설정
# ---------------------------------------------------------------------------
try:
    font_manager.fontManager.addfont(
        "/usr/share/fonts/naver-nanum-gothic-fonts/NanumGothic.ttf"
    )
    matplotlib.rcParams["font.family"] = "NanumGothic"
except OSError:
    preferred = ["NanumGothic", "Noto Sans CJK KR", "Malgun Gothic", "AppleGothic"]
    available = {f.name for f in font_manager.fontManager.ttflist}
    chosen = next((f for f in preferred if f in available), None)
    if chosen:
        matplotlib.rcParams["font.family"] = chosen
matplotlib.rcParams["axes.unicode_minus"] = False

os.chdir(Path(__file__).parent)
OUTPUT_DIR = Path(".")


def save_fig(fig: plt.Figure, name: str) -> None:
    path = OUTPUT_DIR / name
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  저장: {path}")


# ---------------------------------------------------------------------------
# 1. 원본 데이터 (visualize.py 와 동일)
# ---------------------------------------------------------------------------
TARGET_SUM = 100
OCTAGON_RADIUS = 2.3
ROTATION = math.pi / 8.0

# 각 팔각형의 꼭짓점 값 (반시계 방향 순서)
GROUPS = {
    "상": [4, 9, 14, 23, 5, 8, 19, 18],
    "좌": [8, 5, 15, 22, 3, 10, 20, 17],
    "우": [1, 12, 18, 19, 6, 7, 13, 24],
    "하": [7, 6, 17, 20, 2, 11, 16, 21],
}

EXPECTED_SHARED = {
    ("상", "좌"): {5, 8},
    ("상", "우"): {18, 19},
    ("좌", "하"): {17, 20},
    ("우", "하"): {6, 7},
}

# 중앙 정사각형을 이루는 각 팔각형의 안쪽 변
CENTER_EDGES = {("상", (8, 19)), ("우", (19, 6)), ("하", (6, 17)), ("좌", (17, 8))}


def octagon_vertices(center):
    cx, cy = center
    return [
        (
            cx + OCTAGON_RADIUS * math.cos(ROTATION + i * math.pi / 4.0),
            cy + OCTAGON_RADIUS * math.sin(ROTATION + i * math.pi / 4.0),
        )
        for i in range(8)
    ]


def build_geometry():
    apothem = OCTAGON_RADIUS * math.cos(math.pi / 8.0)
    offset = math.sqrt(2.0) * apothem
    centers = {
        "상": (0.0, offset),
        "좌": (-offset, 0.0),
        "우": (offset, 0.0),
        "하": (0.0, -offset),
    }
    vertices = {name: octagon_vertices(c) for name, c in centers.items()}
    positions = {}
    for name, values in GROUPS.items():
        for value, point in zip(values, vertices[name]):
            positions.setdefault(value, point)
    return centers, vertices, positions


def validate() -> None:
    """원문 도안의 기본 조건을 검증한다 (어긋나면 중단)."""
    for name, values in GROUPS.items():
        assert len(values) == 8, f"{name} 팔각형 꼭짓점 수 오류"
        assert sum(values) == TARGET_SUM, f"{name} 팔각형 합 {sum(values)} != {TARGET_SUM}"
    all_values = sorted({v for values in GROUPS.values() for v in values})
    assert all_values == list(range(1, 25)), "값 집합이 1..24가 아님"
    for (a, b), shared in EXPECTED_SHARED.items():
        actual = set(GROUPS[a]) & set(GROUPS[b])
        assert actual == shared, f"{a}∩{b} 공유 변 {actual} != {shared}"
    # 중복 방정식 kS = T + D
    total = sum(all_values)                      # T = 300
    dup = sum(v for values in GROUPS.values() for v in values) - total  # D = 100
    assert 4 * TARGET_SUM == total + dup
    print(f"검증 통과: 4개 팔각형 합 = {TARGET_SUM}, 값 집합 1..24, "
          f"kS = T + D → 400 = {total} + {dup}")


# ---------------------------------------------------------------------------
# 2. 오행(五行) 분류
# ---------------------------------------------------------------------------
PHASES = ["토", "수", "화", "목", "금"]  # residue 0..4
PHASE_EN = {"수": "Water", "화": "Fire", "목": "Wood", "금": "Metal", "토": "Earth"}
PHASE_COLOR = {
    "수": "#3182bd", "화": "#de2d26", "목": "#31a354",
    "금": "#fdd049", "토": "#8c6d51",
}
# 상생: 목→화→토→금→수→목 / 상극: 목→토→수→화→금→목
GENERATION = {("목", "화"), ("화", "토"), ("토", "금"), ("금", "수"), ("수", "목")}
OVERCOMING = {("목", "토"), ("토", "수"), ("수", "화"), ("화", "금"), ("금", "목")}


def phase_of(value: int) -> str:
    return PHASES[value % 5]


def _undirected(pairs):
    return pairs | {(b, a) for a, b in pairs}


GENERATION_U = _undirected(GENERATION)
OVERCOMING_U = _undirected(OVERCOMING)


def edge_relation(pa: str, pb: str) -> str:
    if pa == pb:
        return "동질"
    if (pa, pb) in GENERATION_U:
        return "상생"
    if (pa, pb) in OVERCOMING_U:
        return "상극"
    return "중성"


# ---------------------------------------------------------------------------
# 3. 그래프 구성: 팔각형 변의 합집합
# ---------------------------------------------------------------------------
def build_graph():
    edges = set()
    for values in GROUPS.values():
        for i in range(8):
            a, b = values[i], values[(i + 1) % 8]
            edges.add(frozenset((a, b)))
    graph = nx.Graph()
    for value in range(1, 25):
        graph.add_node(value, phase=phase_of(value))
    graph.add_edges_from(tuple(e) for e in edges)
    return graph, edges


def girth(graph: nx.Graph) -> int:
    try:
        return nx.girth(graph)
    except Exception:
        best = math.inf
        for basis in nx.cycle_basis(graph):
            best = min(best, len(basis))
        return int(best)


# ---------------------------------------------------------------------------
# 4. 분석 본체
# ---------------------------------------------------------------------------
def main() -> None:
    print("=== 기책용팔도(奇策用八圖) 심층 성질 분석 ===\n")
    validate()
    centers, vertices, positions = build_geometry()
    graph, edges = build_graph()

    # --- 기본 구조 ---
    shared_vertices = sorted({v for s in EXPECTED_SHARED.values() for v in s})
    degrees = dict(graph.degree())
    deg3 = sorted(v for v, d in degrees.items() if d == 3)
    deg2 = sorted(v for v, d in degrees.items() if d == 2)
    print(f"\n노드 {graph.number_of_nodes()}, 엣지 {graph.number_of_edges()}, "
          f"연결 성분 {nx.number_connected_components(graph)}")
    print(f"차수 3 (공유 꼭짓점 8개): {deg3}")
    print(f"차수 2: {deg2}")
    print(f"사이클 랭크: {graph.number_of_edges() - graph.number_of_nodes() + 1}, "
          f"girth: {girth(graph)}")

    # --- 오행 분석 ---
    class_values = {p: [v for v in range(1, 25) if phase_of(v) == p] for p in PHASE_EN}
    class_sums = {p: sum(vs) for p, vs in class_values.items()}
    print(f"\n오행별 합: {class_sums}")
    per_group_phase = {
        name: {p: sum(1 for v in values if phase_of(v) == p) for p in PHASE_EN}
        for name, values in GROUPS.items()
    }
    relations = {"동질": 0, "상생": 0, "상극": 0, "중성": 0}
    for a, b in (tuple(e) for e in edges):
        relations[edge_relation(phase_of(a), phase_of(b))] += 1
    print(f"엣지 오행 관계: {relations} (총 {len(edges)})")

    # --- 중심성 ---
    bet = nx.betweenness_centrality(graph)
    top10 = sorted(bet.items(), key=lambda kv: -kv[1])[:10]
    print("\nBetweenness 상위 10:")
    for v, c in top10:
        in_groups = [name for name, values in GROUPS.items() if v in values]
        print(f"  {v:3d} ({phase_of(v)}) {''.join(in_groups)}: {c:.3f}")

    # --- 위치 불변량 ---
    center_cycle = [8, 19, 6, 17]
    center_edges = {
        frozenset((center_cycle[i], center_cycle[(i + 1) % 4])) for i in range(4)
    }
    assert center_edges <= edges, "중앙 정사각형 변이 그래프에 없음"
    center_sum = sum(center_cycle)
    quad_a = sorted({8, 19, 6, 17})
    quad_b = sorted({5, 18, 7, 20})
    print(f"\n중앙 정사각형 {center_cycle} 합 = {center_sum}")
    print(f"공유 꼭짓점 두 쌍: {quad_a} 합 {sum(quad_a)}, {quad_b} 합 {sum(quad_b)}")

    opposite_sums = {}
    for name, values in GROUPS.items():
        pairs = [(values[i], values[(i + 4) % 8]) for i in range(4)]
        opposite_sums[name] = [(a, b, a + b) for a, b in pairs]
        print(f"{name} 팔각형 마주보는 쌍 합: {[s for _, _, s in opposite_sums[name]]}")
    # 맞은편 쌍 합의 보완 구조: 네 쌍이 합 50인 두 보완 쌍으로 짝지어지는가
    for name, quads in opposite_sums.items():
        sums4 = sorted(s for _, _, s in quads)
        comp = sums4[0] + sums4[3] == sums4[1] + sums4[2] == TARGET_SUM // 2
        print(f"{name} 팔각형 보완쌍 합 50 성립: {comp} ({sums4[0]}+{sums4[3]} = {sums4[1]}+{sums4[2]})")

    # 공유/고유 꼭짓점의 50/50 분해 (팔각형별)
    print("\n팔각형별 공유/고유 50/50 분해:")
    for name, values in GROUPS.items():
        shared4 = sorted(v for v in values if v in shared_vertices)
        unique4 = sorted(v for v in values if v not in shared_vertices)
        print(f"  {name}: 공유 {shared4} 합 {sum(shared4)}, 고유 {unique4} 합 {sum(unique4)}")

    # 동심 고리 (중심에서의 거리별)
    radii = {}
    for v, (x, y) in positions.items():
        radii.setdefault(round(math.hypot(x, y), 3), []).append(v)
    rings = sorted(radii.items())
    print("\n동심 고리:")
    ring_sums = []
    for r, vs in rings:
        vs = sorted(vs)
        ring_sums.append(sum(vs))
        print(f"  r≈{r}: {vs} 합 {sum(vs)}")
    assert ring_sums == [50, 50, 100, 100]

    # 이분 그래프 확인
    print(f"\n이분 그래프: {nx.is_bipartite(graph)}")

    # --- 스펙트럼 ---
    ordered = sorted(graph.nodes())
    adj = nx.to_numpy_array(graph, nodelist=ordered)
    eig = np.linalg.eigvalsh(adj)
    print(f"\n스펙트럼: λmax = {eig[-1]:.4f}, λmin = {eig[0]:.4f}")

    # ===================================================================
    # 그림
    # ===================================================================
    print("\n그림 생성:")

    def draw_base(ax, edge_alpha=0.5, node_size=520, show_central=True):
        group_colors = {"상": "#2171b5", "좌": "#238b45", "우": "#d94801", "하": "#6a51a3"}
        for name, verts in vertices.items():
            ax.add_patch(Polygon(
                verts, closed=True, facecolor=group_colors[name],
                edgecolor=group_colors[name], linewidth=1.6, alpha=0.10, zorder=1))
        for a, b in (tuple(e) for e in edges):
            xa, ya = positions[a]
            xb, yb = positions[b]
            is_shared = a in shared_vertices and b in shared_vertices
            ax.plot([xa, xb], [ya, yb], color="#777777" if not is_shared else "#000000",
                    lw=1.2 if not is_shared else 2.4, alpha=edge_alpha, zorder=2)
        for v, (x, y) in positions.items():
            p = phase_of(v)
            ax.add_patch(Circle((x, y), 0.30, facecolor=PHASE_COLOR[p],
                                edgecolor="#202020", linewidth=1.0, zorder=3))
            ax.text(x, y, str(v), ha="center", va="center", fontsize=8,
                    fontweight="bold", zorder=4)
        if show_central:
            xs = [positions[v][0] for v in center_cycle + [8]]
            ys = [positions[v][1] for v in center_cycle + [8]]
            ax.plot(xs, ys, color="#e6550d", lw=3.0, alpha=0.9, zorder=5,
                    label=f"중앙 정사각형 Σ={center_sum}")
        ax.set_aspect("equal")
        ax.axis("off")

    # 01 원본 그래프
    fig, ax = plt.subplots(figsize=(8, 8))
    draw_base(ax)
    handles = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=c,
                          markersize=10, label=f"{p}({PHASE_EN[p]})")
               for p, c in PHASE_COLOR.items()]
    handles.append(plt.Line2D([0], [0], color="#e6550d", lw=3,
                              label=f"중앙 정사각형 Σ={center_sum}"))
    ax.legend(handles=handles, loc="lower right", fontsize=10)
    ax.set_title("기책용팔도(奇策用八圖) — 4개 팔각형, 각 합 100 (오행 색상)", fontsize=13)
    save_fig(fig, "01_original_graph.png")

    # 02 오행 분해
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    for ax, phase in zip(axes.flat[1:], ["수", "화", "목", "금", "토"]):
        for a, b in (tuple(e) for e in edges):
            xa, ya = positions[a]
            xb, yb = positions[b]
            ax.plot([xa, xb], [ya, yb], color="#cccccc", lw=0.8, zorder=1)
        for v, (x, y) in positions.items():
            on = phase_of(v) == phase
            ax.add_patch(Circle((x, y), 0.30,
                                facecolor=PHASE_COLOR[phase] if on else "#f0f0f0",
                                edgecolor="#909090", linewidth=0.8, zorder=2))
            ax.text(x, y, str(v), ha="center", va="center", fontsize=7,
                    alpha=1.0 if on else 0.45, zorder=3)
        ax.set_title(f"{phase}({PHASE_EN[phase]}): {class_values[phase]}\n"
                     f"합 = {class_sums[phase]}", fontsize=11)
        ax.set_aspect("equal")
        ax.axis("off")
    draw_base(axes.flat[0], show_central=False)
    axes.flat[0].set_title("전체 도안", fontsize=11)
    fig.suptitle("오행(五行) mod 5 분해 — 기책용팔도", fontsize=14)
    save_fig(fig, "02_wuxing_decomposition.png")

    # 03 인접 행렬 + 스펙트럼
    block_order = [v for p in ["수", "화", "목", "금", "토"] for v in class_values[p]]
    adj_b = nx.to_numpy_array(graph, nodelist=block_order)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))
    ax1.imshow(adj_b, cmap="Greys", interpolation="nearest")
    bounds = np.cumsum([len(class_values[p]) for p in ["수", "화", "목", "금", "토"]])
    for b in bounds[:-1]:
        ax1.axhline(b - 0.5, color="#3182bd", lw=1.2)
        ax1.axvline(b - 0.5, color="#3182bd", lw=1.2)
    ax1.set_title("인접 행렬 (오행 블록 정렬)", fontsize=12)
    ax2.bar(range(len(eig)), eig, color="#756bb1")
    ax2.axhline(0, color="k", lw=0.6)
    ax2.set_title(f"스펙트럼: λmax = {eig[-1]:.3f}, λmin = {eig[0]:.3f}", fontsize=12)
    ax2.set_xlabel("고유값 인덱스")
    save_fig(fig, "03_adjacency_spectrum.png")

    # 04 사이클 분석: 4개의 8-사이클 + 중앙 4-사이클, 면(사이클 기저)별 합
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.5))
    draw_base(axes[0])
    axes[0].set_title("4개 팔각형 8-사이클 + 중앙 정사각형 4-사이클", fontsize=12)
    face_names = ["중앙 정사각형", "상 팔각형", "좌 팔각형", "우 팔각형", "하 팔각형"]
    face_sums = [center_sum] + [sum(GROUPS[n]) for n in ["상", "좌", "우", "하"]]
    axes[1].bar(face_names, face_sums,
                color=["#e6550d", "#2171b5", "#238b45", "#d94801", "#6a51a3"])
    for i, v in enumerate(face_sums):
        axes[1].text(i, v + 2, str(v), ha="center", fontsize=12)
    axes[1].set_ylim(0, 125)
    axes[1].set_title(f"최소 사이클 기저 (랭크 5, girth {girth(graph)}) 의 면 별 합", fontsize=12)
    axes[1].set_ylabel("합")
    axes[1].tick_params(axis="x", labelsize=9)
    save_fig(fig, "04_cycle_analysis.png")

    # 05 중심성 불변량
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    deg_vals = [degrees[v] for v in ordered]
    axes[0, 0].bar([str(v) for v in ordered], deg_vals,
                   color=[PHASE_COLOR[phase_of(v)] for v in ordered])
    axes[0, 0].set_title("차수 분포 (공유 꼭짓점 8개 = 차수 3)", fontsize=11)
    axes[0, 0].tick_params(axis="x", labelsize=6)
    bet_vals = [bet[v] for v in ordered]
    axes[0, 1].bar([str(v) for v in ordered], bet_vals,
                   color=[PHASE_COLOR[phase_of(v)] for v in ordered])
    axes[0, 1].set_title("Betweenness centrality", fontsize=11)
    axes[0, 1].tick_params(axis="x", labelsize=6)
    phases5 = ["수", "화", "목", "금", "토"]
    axes[1, 0].bar(phases5, [class_sums[p] for p in phases5],
                   color=[PHASE_COLOR[p] for p in phases5])
    for i, p in enumerate(phases5):
        axes[1, 0].text(i, class_sums[p] + 1, str(class_sums[p]), ha="center", fontsize=11)
    axes[1, 0].set_title("오행별 합 (1..24)", fontsize=11)
    names = list(GROUPS)
    axes[1, 1].bar(names, [sum(GROUPS[n]) for n in names], color="#2171b5")
    axes[1, 1].axhline(TARGET_SUM, color="r", ls="--", lw=1)
    for i, n in enumerate(names):
        axes[1, 1].text(i, TARGET_SUM + 1, str(sum(GROUPS[n])), ha="center", fontsize=11)
    axes[1, 1].set_ylim(0, 125)
    axes[1, 1].set_title("팔각형별 합 = 100 (각득 불변량)", fontsize=11)
    fig.suptitle("중심성·합 불변량", fontsize=13)
    fig.tight_layout()
    save_fig(fig, "05_centrality_invariants.png")

    # 06 오행 상생상극
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))
    pent = ["목", "화", "토", "금", "수"]
    ang = {p: math.pi / 2 - i * 2 * math.pi / 5 for i, p in enumerate(pent)}
    xy = {p: (math.cos(ang[p]), math.sin(ang[p])) for p in pent}
    for a, b in GENERATION:
        ax1.annotate("", xy=xy[b], xytext=xy[a],
                     arrowprops=dict(arrowstyle="->", color="#31a354", lw=2))
    for a, b in OVERCOMING:
        ax1.annotate("", xy=xy[b], xytext=xy[a],
                     arrowprops=dict(arrowstyle="->", color="#de2d26", lw=1.6, ls="--"))
    for p in pent:
        ax1.add_patch(Circle(xy[p], 0.16, facecolor=PHASE_COLOR[p],
                             edgecolor="k", zorder=3))
        ax1.text(*xy[p], p, ha="center", va="center", fontsize=14,
                 fontweight="bold", zorder=4)
    ax1.set_title("상생(초록 실선)·상극(빨강 점선) 관계", fontsize=12)
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)
    ax1.set_aspect("equal")
    ax1.axis("off")
    rel_pairs = [(k, v) for k, v in relations.items() if v > 0]
    ax2.pie([v for _, v in rel_pairs],
            labels=[f"{k} {v}개 ({v / len(edges) * 100:.1f}%)" for k, v in rel_pairs],
            colors=["#9ecae1", "#a1d99b", "#fc9272", "#d9d9d9"][:len(rel_pairs)],
            startangle=90, textprops={"fontsize": 11})
    ax2.set_title(f"엣지 {len(edges)}개의 오행 관계 분류", fontsize=12)
    save_fig(fig, "06_wuxing_relations.png")

    # 07 일반화 가족: 8-사이클 각득 가족 비교 + 4.8.8 타일링 확장 모식도
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.5))
    fam_names = ["기책용팔도\n(4×8-사이클)", "팔자각득\n(5×8-사이클)"]
    fam_s = [100, 164]
    axes[0].bar(fam_names, fam_s, color=["#2171b5", "#6a51a3"])
    for i, v in enumerate(fam_s):
        axes[0].text(i, v + 3, f"Σ={v}", ha="center", fontsize=12)
    axes[0].set_title("8-사이클 각득 가족 (클스터 합 비교)", fontsize=12)
    # 4.8.8 타일링 확장 모식도: 현재 4개 + 대각선 유령 팔각형 4개
    apothem = OCTAGON_RADIUS * math.cos(math.pi / 8.0)
    offset = math.sqrt(2.0) * apothem
    for name, (cx, cy) in centers.items():
        axes[1].add_patch(Polygon(
            vertices[name], closed=True, facecolor="#9ecae1",
            edgecolor="#2171b5", linewidth=1.6, alpha=0.35, zorder=2))
    ghost_offsets = [(offset, offset), (-offset, offset),
                     (offset, -offset), (-offset, -offset)]
    for gx, gy in ghost_offsets:
        axes[1].add_patch(Polygon(
            octagon_vertices((gx, gy)), closed=True, facecolor="#f0f0f0",
            edgecolor="#909090", linewidth=1.4, alpha=0.5, linestyle="--", zorder=1))
    axes[1].plot([0], [0], marker="s", markersize=10, color="#e6550d")
    axes[1].set_xlim(-3 * offset, 3 * offset)
    axes[1].set_ylim(-3 * offset, 3 * offset)
    axes[1].set_aspect("equal")
    axes[1].axis("off")
    axes[1].set_title("4.8.8 타일링 확장 모식도 (실선: 현재, 점선: 확장)", fontsize=12)
    save_fig(fig, "07_local_extensions.png")

    # 08 위치 불변량: 동심 고리 / 공유·고유 50-50 / 맞은편 쌍 25-대칭
    fig, axes = plt.subplots(1, 3, figsize=(17, 5.5))
    ring_labels = [f"고리{i + 1}\n(r≈{r})" for i, (r, _) in enumerate(rings)]
    axes[0].bar(ring_labels, ring_sums, color=["#e6550d", "#238b45", "#2171b5", "#6a51a3"])
    for i, v in enumerate(ring_sums):
        axes[0].text(i, v + 2, str(v), ha="center", fontsize=12)
    axes[0].set_ylim(0, 125)
    axes[0].set_title("동심 고리별 합 (50·50·100·100)", fontsize=12)
    width = 0.35
    for i, name in enumerate(names):
        shared4 = sum(v for v in GROUPS[name] if v in shared_vertices)
        unique4 = sum(v for v in GROUPS[name] if v not in shared_vertices)
        axes[1].bar(i - width / 2, shared4, width=width, color="#d94801",
                    label="공유 4개" if i == 0 else None)
        axes[1].bar(i + width / 2, unique4, width=width, color="#2171b5",
                    label="고유 4개" if i == 0 else None)
        axes[1].text(i - width / 2, shared4 + 1, str(shared4), ha="center", fontsize=11)
        axes[1].text(i + width / 2, unique4 + 1, str(unique4), ha="center", fontsize=11)
    axes[1].set_xticks(range(4))
    axes[1].set_xticklabels([f"{n} 팔각형" for n in names])
    axes[1].set_ylim(0, 62)
    axes[1].legend(fontsize=10)
    axes[1].set_title("팔각형별 공유/고유 꼭짓점 합 = 50/50", fontsize=12)
    width = 0.2
    for i, name in enumerate(names):
        sums4 = sorted(s for _, _, s in opposite_sums[name])
        axes[2].bar(np.arange(4) + i * width, sums4, width=width, label=f"{name}")
    axes[2].axhline(25, color="gray", ls=":", lw=1)
    axes[2].set_xticks(np.arange(4) + 1.5 * width)
    axes[2].set_xticklabels(["최소", "차소", "차대", "최대"])
    axes[2].legend(fontsize=10)
    axes[2].set_title("맞은편 쌍 합 (정렬): 양끝끼리 50 (25-대칭)", fontsize=12)
    fig.tight_layout()
    save_fig(fig, "08_position_patterns.png")

    print("\n분석 완료.")


if __name__ == "__main__":
    main()
