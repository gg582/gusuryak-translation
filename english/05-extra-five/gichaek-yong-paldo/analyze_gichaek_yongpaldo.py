#!/usr/bin/env python3
"""Deep property analysis of Gichaek-yongpaldo (奇策用八圖).

Four octagons (top/left/right/bottom) surround a central square, and each
pair of adjacent octagons shares one complete edge.  The values 1..24 are
placed on the vertices so that every octagon sums to 100 — a member of the
Gakdeuk ("each gets") family.

Analysis items:
    - Basic checksums (value set, total, octagon sums, duplication kS = T + D)
    - Graph structure (degree distribution, cycles, centrality)
    - Wuxing (五行) mod-5 decomposition and edge generation/overcoming classes
    - Positional invariants (central square, shared vertices, opposite pairs)
    - Spectrum
    - Generalization family

Running the script saves figures 01..08 into this directory.
"""

import math
import os
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.patches import Circle, Polygon

matplotlib.rcParams["axes.unicode_minus"] = False

os.chdir(Path(__file__).parent)
OUTPUT_DIR = Path(".")


def save_fig(fig: plt.Figure, name: str) -> None:
    path = OUTPUT_DIR / name
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  saved: {path}")


# ---------------------------------------------------------------------------
# 1. Source data (identical to visualize.py)
# ---------------------------------------------------------------------------
TARGET_SUM = 100
OCTAGON_RADIUS = 2.3
ROTATION = math.pi / 8.0

# Vertex values of each octagon (counterclockwise order)
GROUPS = {
    "Top": [4, 9, 14, 23, 5, 8, 19, 18],
    "Left": [8, 5, 15, 22, 3, 10, 20, 17],
    "Right": [1, 12, 18, 19, 6, 7, 13, 24],
    "Bottom": [7, 6, 17, 20, 2, 11, 16, 21],
}

EXPECTED_SHARED = {
    ("Top", "Left"): {5, 8},
    ("Top", "Right"): {18, 19},
    ("Left", "Bottom"): {17, 20},
    ("Right", "Bottom"): {6, 7},
}


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
        "Top": (0.0, offset),
        "Left": (-offset, 0.0),
        "Right": (offset, 0.0),
        "Bottom": (0.0, -offset),
    }
    vertices = {name: octagon_vertices(c) for name, c in centers.items()}
    positions = {}
    for name, values in GROUPS.items():
        for value, point in zip(values, vertices[name]):
            positions.setdefault(value, point)
    return centers, vertices, positions


def validate() -> None:
    """Check the diagram's basic conditions (abort on violation)."""
    for name, values in GROUPS.items():
        assert len(values) == 8, f"{name} octagon vertex count error"
        assert sum(values) == TARGET_SUM, f"{name} octagon sum {sum(values)} != {TARGET_SUM}"
    all_values = sorted({v for values in GROUPS.values() for v in values})
    assert all_values == list(range(1, 25)), "value set is not 1..24"
    for (a, b), shared in EXPECTED_SHARED.items():
        actual = set(GROUPS[a]) & set(GROUPS[b])
        assert actual == shared, f"{a}&{b} shared edge {actual} != {shared}"
    # Duplication equation kS = T + D
    total = sum(all_values)                      # T = 300
    dup = sum(v for values in GROUPS.values() for v in values) - total  # D = 100
    assert 4 * TARGET_SUM == total + dup
    print(f"validation passed: 4 octagon sums = {TARGET_SUM}, values 1..24, "
          f"kS = T + D -> 400 = {total} + {dup}")


# ---------------------------------------------------------------------------
# 2. Wuxing (五行) classes
# ---------------------------------------------------------------------------
PHASES = ["Earth", "Water", "Fire", "Wood", "Metal"]  # residue 0..4
PHASE_COLOR = {
    "Water": "#3182bd", "Fire": "#de2d26", "Wood": "#31a354",
    "Metal": "#fdd049", "Earth": "#8c6d51",
}
# Generation: Wood->Fire->Earth->Metal->Water->Wood /
# Overcoming: Wood->Earth->Water->Fire->Metal->Wood
GENERATION = {("Wood", "Fire"), ("Fire", "Earth"), ("Earth", "Metal"),
              ("Metal", "Water"), ("Water", "Wood")}
OVERCOMING = {("Wood", "Earth"), ("Earth", "Water"), ("Water", "Fire"),
              ("Fire", "Metal"), ("Metal", "Wood")}


def phase_of(value: int) -> str:
    return PHASES[value % 5]


def _undirected(pairs):
    return pairs | {(b, a) for a, b in pairs}


GENERATION_U = _undirected(GENERATION)
OVERCOMING_U = _undirected(OVERCOMING)


def edge_relation(pa: str, pb: str) -> str:
    if pa == pb:
        return "same"
    if (pa, pb) in GENERATION_U:
        return "generation"
    if (pa, pb) in OVERCOMING_U:
        return "overcoming"
    return "neutral"


# ---------------------------------------------------------------------------
# 3. Graph: union of the octagon edges
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
# 4. Analysis
# ---------------------------------------------------------------------------
def main() -> None:
    print("=== Gichaek-yongpaldo (奇策用八圖) deep property analysis ===\n")
    validate()
    centers, vertices, positions = build_geometry()
    graph, edges = build_graph()

    # --- basic structure ---
    shared_vertices = sorted({v for s in EXPECTED_SHARED.values() for v in s})
    degrees = dict(graph.degree())
    deg3 = sorted(v for v, d in degrees.items() if d == 3)
    deg2 = sorted(v for v, d in degrees.items() if d == 2)
    print(f"\nnodes {graph.number_of_nodes()}, edges {graph.number_of_edges()}, "
          f"components {nx.number_connected_components(graph)}")
    print(f"degree 3 (8 shared vertices): {deg3}")
    print(f"degree 2: {deg2}")
    print(f"cycle rank: {graph.number_of_edges() - graph.number_of_nodes() + 1}, "
          f"girth: {girth(graph)}")

    # --- wuxing analysis ---
    class_values = {p: [v for v in range(1, 25) if phase_of(v) == p]
                    for p in ["Water", "Fire", "Wood", "Metal", "Earth"]}
    class_sums = {p: sum(vs) for p, vs in class_values.items()}
    print(f"\nwuxing class sums: {class_sums}")
    relations = {"same": 0, "generation": 0, "overcoming": 0, "neutral": 0}
    for a, b in (tuple(e) for e in edges):
        relations[edge_relation(phase_of(a), phase_of(b))] += 1
    print(f"edge wuxing relations: {relations} (of {len(edges)})")

    # --- centrality ---
    bet = nx.betweenness_centrality(graph)
    top10 = sorted(bet.items(), key=lambda kv: -kv[1])[:10]
    print("\nbetweenness top 10:")
    for v, c in top10:
        in_groups = [name for name, values in GROUPS.items() if v in values]
        print(f"  {v:3d} ({phase_of(v)}) {''.join(in_groups)}: {c:.3f}")

    # --- positional invariants ---
    center_cycle = [8, 19, 6, 17]
    center_edges = {
        frozenset((center_cycle[i], center_cycle[(i + 1) % 4])) for i in range(4)
    }
    assert center_edges <= edges, "central square edges missing from graph"
    center_sum = sum(center_cycle)
    quad_a = sorted({8, 19, 6, 17})
    quad_b = sorted({5, 18, 7, 20})
    print(f"\ncentral square {center_cycle} sum = {center_sum}")
    print(f"shared-vertex quadruples: {quad_a} sum {sum(quad_a)}, "
          f"{quad_b} sum {sum(quad_b)}")

    opposite_sums = {}
    for name, values in GROUPS.items():
        pairs = [(values[i], values[(i + 4) % 8]) for i in range(4)]
        opposite_sums[name] = [(a, b, a + b) for a, b in pairs]
        print(f"{name} opposite-pair sums: {[s for _, _, s in opposite_sums[name]]}")
    # Complement structure: the four pair sums pair up to 50
    for name, quads in opposite_sums.items():
        sums4 = sorted(s for _, _, s in quads)
        comp = sums4[0] + sums4[3] == sums4[1] + sums4[2] == TARGET_SUM // 2
        print(f"{name} complement pairs sum to 50: {comp} "
              f"({sums4[0]}+{sums4[3]} = {sums4[1]}+{sums4[2]})")

    # Shared/unique 50-50 split per octagon
    print("\nshared/unique 50-50 split per octagon:")
    for name, values in GROUPS.items():
        shared4 = sorted(v for v in values if v in shared_vertices)
        unique4 = sorted(v for v in values if v not in shared_vertices)
        print(f"  {name}: shared {shared4} sum {sum(shared4)}, "
              f"unique {unique4} sum {sum(unique4)}")

    # Concentric rings (by distance from the origin)
    radii = {}
    for v, (x, y) in positions.items():
        radii.setdefault(round(math.hypot(x, y), 3), []).append(v)
    rings = sorted(radii.items())
    print("\nconcentric rings:")
    ring_sums = []
    for r, vs in rings:
        vs = sorted(vs)
        ring_sums.append(sum(vs))
        print(f"  r~{r}: {vs} sum {sum(vs)}")
    assert ring_sums == [50, 50, 100, 100]

    print(f"\nbipartite: {nx.is_bipartite(graph)}")

    # --- spectrum ---
    ordered = sorted(graph.nodes())
    adj = nx.to_numpy_array(graph, nodelist=ordered)
    eig = np.linalg.eigvalsh(adj)
    print(f"\nspectrum: lambda_max = {eig[-1]:.4f}, lambda_min = {eig[0]:.4f}")

    # ===================================================================
    # Figures
    # ===================================================================
    print("\nfigures:")

    def draw_base(ax, edge_alpha=0.5, show_central=True):
        group_colors = {"Top": "#2171b5", "Left": "#238b45",
                        "Right": "#d94801", "Bottom": "#6a51a3"}
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
                    label=f"central square sum={center_sum}")
        ax.set_aspect("equal")
        ax.axis("off")

    # 01 original graph
    fig, ax = plt.subplots(figsize=(8, 8))
    draw_base(ax)
    handles = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=c,
                          markersize=10, label=p)
               for p, c in PHASE_COLOR.items()]
    handles.append(plt.Line2D([0], [0], color="#e6550d", lw=3,
                              label=f"central square sum={center_sum}"))
    ax.legend(handles=handles, loc="lower right", fontsize=10)
    ax.set_title("Gichaek-yongpaldo (奇策用八圖) — four octagons, each sum 100 "
                 "(wuxing colors)", fontsize=13)
    save_fig(fig, "01_original_graph.png")

    # 02 wuxing decomposition
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    for ax, phase in zip(axes.flat[1:], ["Water", "Fire", "Wood", "Metal", "Earth"]):
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
        ax.set_title(f"{phase}: {class_values[phase]}\nsum = {class_sums[phase]}",
                     fontsize=11)
        ax.set_aspect("equal")
        ax.axis("off")
    draw_base(axes.flat[0], show_central=False)
    axes.flat[0].set_title("full diagram", fontsize=11)
    fig.suptitle("Wuxing (五行) mod-5 decomposition — Gichaek-yongpaldo", fontsize=14)
    save_fig(fig, "02_wuxing_decomposition.png")

    # 03 adjacency matrix + spectrum
    block_order = [v for p in ["Water", "Fire", "Wood", "Metal", "Earth"]
                   for v in class_values[p]]
    adj_b = nx.to_numpy_array(graph, nodelist=block_order)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))
    ax1.imshow(adj_b, cmap="Greys", interpolation="nearest")
    bounds = np.cumsum([len(class_values[p])
                        for p in ["Water", "Fire", "Wood", "Metal", "Earth"]])
    for b in bounds[:-1]:
        ax1.axhline(b - 0.5, color="#3182bd", lw=1.2)
        ax1.axvline(b - 0.5, color="#3182bd", lw=1.2)
    ax1.set_title("adjacency matrix (wuxing block order)", fontsize=12)
    ax2.bar(range(len(eig)), eig, color="#756bb1")
    ax2.axhline(0, color="k", lw=0.6)
    ax2.set_title(f"spectrum: max {eig[-1]:.3f}, min {eig[0]:.3f}", fontsize=12)
    ax2.set_xlabel("eigenvalue index")
    save_fig(fig, "03_adjacency_spectrum.png")

    # 04 cycle analysis: four 8-cycles + central 4-cycle, per-face sums
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.5))
    draw_base(axes[0])
    axes[0].set_title("four octagon 8-cycles + central square 4-cycle", fontsize=12)
    face_names = ["central\nsquare", "Top", "Left", "Right", "Bottom"]
    face_sums = [center_sum] + [sum(GROUPS[n]) for n in ["Top", "Left", "Right", "Bottom"]]
    axes[1].bar(face_names, face_sums,
                color=["#e6550d", "#2171b5", "#238b45", "#d94801", "#6a51a3"])
    for i, v in enumerate(face_sums):
        axes[1].text(i, v + 2, str(v), ha="center", fontsize=12)
    axes[1].set_ylim(0, 125)
    axes[1].set_title(f"minimum cycle basis (rank 5, girth {girth(graph)}): per-face sums",
                      fontsize=12)
    axes[1].set_ylabel("sum")
    axes[1].tick_params(axis="x", labelsize=9)
    save_fig(fig, "04_cycle_analysis.png")

    # 05 centrality invariants
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    deg_vals = [degrees[v] for v in ordered]
    axes[0, 0].bar([str(v) for v in ordered], deg_vals,
                   color=[PHASE_COLOR[phase_of(v)] for v in ordered])
    axes[0, 0].set_title("degree distribution (8 shared vertices = degree 3)", fontsize=11)
    axes[0, 0].tick_params(axis="x", labelsize=6)
    bet_vals = [bet[v] for v in ordered]
    axes[0, 1].bar([str(v) for v in ordered], bet_vals,
                   color=[PHASE_COLOR[phase_of(v)] for v in ordered])
    axes[0, 1].set_title("betweenness centrality", fontsize=11)
    axes[0, 1].tick_params(axis="x", labelsize=6)
    phases5 = ["Water", "Fire", "Wood", "Metal", "Earth"]
    axes[1, 0].bar(phases5, [class_sums[p] for p in phases5],
                   color=[PHASE_COLOR[p] for p in phases5])
    for i, p in enumerate(phases5):
        axes[1, 0].text(i, class_sums[p] + 1, str(class_sums[p]), ha="center", fontsize=11)
    axes[1, 0].set_title("wuxing class sums (1..24)", fontsize=11)
    names = list(GROUPS)
    axes[1, 1].bar(names, [sum(GROUPS[n]) for n in names], color="#2171b5")
    axes[1, 1].axhline(TARGET_SUM, color="r", ls="--", lw=1)
    for i, n in enumerate(names):
        axes[1, 1].text(i, TARGET_SUM + 1, str(sum(GROUPS[n])), ha="center", fontsize=11)
    axes[1, 1].set_ylim(0, 125)
    axes[1, 1].set_title("octagon sums = 100 (Gakdeuk invariant)", fontsize=11)
    fig.suptitle("centrality and sum invariants", fontsize=13)
    fig.tight_layout()
    save_fig(fig, "05_centrality_invariants.png")

    # 06 wuxing generation/overcoming relations
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))
    pent = ["Wood", "Fire", "Earth", "Metal", "Water"]
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
        ax1.text(*xy[p], p[:2], ha="center", va="center", fontsize=12,
                 fontweight="bold", zorder=4)
    ax1.set_title("generation (green solid) / overcoming (red dashed)", fontsize=12)
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)
    ax1.set_aspect("equal")
    ax1.axis("off")
    rel_pairs = [(k, v) for k, v in relations.items() if v > 0]
    ax2.pie([v for _, v in rel_pairs],
            labels=[f"{k} {v} ({v / len(edges) * 100:.1f}%)" for k, v in rel_pairs],
            colors=["#9ecae1", "#a1d99b", "#fc9272", "#d9d9d9"][:len(rel_pairs)],
            startangle=90, textprops={"fontsize": 11})
    ax2.set_title(f"wuxing classification of {len(edges)} edges", fontsize=12)
    save_fig(fig, "06_wuxing_relations.png")

    # 07 generalization family + 4.8.8 tiling extension schematic
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.5))
    fam_names = ["Gichaek-yongpaldo\n(4x 8-cycles)", "Paljagakdeuk\n(5x 8-cycles)"]
    fam_s = [100, 164]
    axes[0].bar(fam_names, fam_s, color=["#2171b5", "#6a51a3"])
    for i, v in enumerate(fam_s):
        axes[0].text(i, v + 3, f"S={v}", ha="center", fontsize=12)
    axes[0].set_title("8-cycle Gakdeuk family (cluster sums)", fontsize=12)
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
    axes[1].set_title("4.8.8 tiling extension schematic (solid: present, dashed: extension)",
                      fontsize=12)
    save_fig(fig, "07_local_extensions.png")

    # 08 positional invariants: rings / shared-unique 50-50 / opposite 25-symmetry
    fig, axes = plt.subplots(1, 3, figsize=(17, 5.5))
    ring_labels = [f"ring{i + 1}\n(r~{r})" for i, (r, _) in enumerate(rings)]
    axes[0].bar(ring_labels, ring_sums, color=["#e6550d", "#238b45", "#2171b5", "#6a51a3"])
    for i, v in enumerate(ring_sums):
        axes[0].text(i, v + 2, str(v), ha="center", fontsize=12)
    axes[0].set_ylim(0, 125)
    axes[0].set_title("concentric ring sums (50, 50, 100, 100)", fontsize=12)
    width = 0.35
    for i, name in enumerate(names):
        shared4 = sum(v for v in GROUPS[name] if v in shared_vertices)
        unique4 = sum(v for v in GROUPS[name] if v not in shared_vertices)
        axes[1].bar(i - width / 2, shared4, width=width, color="#d94801",
                    label="shared 4" if i == 0 else None)
        axes[1].bar(i + width / 2, unique4, width=width, color="#2171b5",
                    label="unique 4" if i == 0 else None)
        axes[1].text(i - width / 2, shared4 + 1, str(shared4), ha="center", fontsize=11)
        axes[1].text(i + width / 2, unique4 + 1, str(unique4), ha="center", fontsize=11)
    axes[1].set_xticks(range(4))
    axes[1].set_xticklabels(names)
    axes[1].set_ylim(0, 62)
    axes[1].legend(fontsize=10)
    axes[1].set_title("shared/unique vertex sums = 50/50 per octagon", fontsize=12)
    width = 0.2
    for i, name in enumerate(names):
        sums4 = sorted(s for _, _, s in opposite_sums[name])
        axes[2].bar(np.arange(4) + i * width, sums4, width=width, label=name)
    axes[2].axhline(25, color="gray", ls=":", lw=1)
    axes[2].set_xticks(np.arange(4) + 1.5 * width)
    axes[2].set_xticklabels(["min", "2nd", "3rd", "max"])
    axes[2].legend(fontsize=10)
    axes[2].set_title("opposite-pair sums (sorted): extremes pair to 50 (25-symmetry)",
                      fontsize=12)
    fig.tight_layout()
    save_fig(fig, "08_position_patterns.png")

    print("\ndone.")


if __name__ == "__main__":
    main()
