#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate English visual assets for the translated puzzle folders."""

from __future__ import annotations

import math
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False

PHASES = ["Water", "Fire", "Wood", "Metal", "Earth"]
PHASE_COLORS = {
    "Water": "#4488CC",
    "Fire": "#CC4444",
    "Wood": "#44AA44",
    "Metal": "#888888",
    "Earth": "#CC9944",
}


def phase_of(value: int) -> str:
    return PHASES[(value - 1) % 5]


def save(fig, folder: str | Path, name: str) -> None:
    fig.tight_layout()
    fig.savefig(Path(folder) / name, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def build_positions(palaces: dict, origins: dict):
    pos, owner, cell = {}, {}, {}
    for palace, grid in palaces.items():
        ox, oy = origins[palace]
        for r, row in enumerate(grid):
            for c, value in enumerate(row):
                if value is None:
                    continue
                pos[value] = (ox + c, oy + (2 - r))
                owner[value] = palace
                cell[value] = (r, c)
    return pos, owner, cell


def build_edges(pos: dict, owner: dict | None = None, intra_only: bool = False):
    pos_to_value = {point: value for value, point in pos.items()}
    edges = set()
    for value, (x, y) in pos.items():
        for dx, dy in [(1, 0), (0, 1)]:
            other = pos_to_value.get((x + dx, y + dy))
            if other is None:
                continue
            if intra_only and owner[value] != owner[other]:
                continue
            edges.add(tuple(sorted((value, other))))
    return sorted(edges)


def draw_graph(folder, name, pos, edges, title, subtitle="", highlight=None):
    graph = nx.Graph()
    graph.add_nodes_from(pos)
    graph.add_edges_from(edges)
    highlight = highlight or set()
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_aspect("equal")
    ax.axis("off")
    nx.draw_networkx_edges(graph, pos, ax=ax, edge_color="#555555", width=1.4)
    nodes = sorted(pos)
    nx.draw_networkx_nodes(
        graph,
        pos,
        nodelist=nodes,
        node_color=["#FFE680" if n in highlight else "#EAF2FF" for n in nodes],
        edgecolors=[PHASE_COLORS[phase_of(n)] for n in nodes],
        linewidths=2.2,
        node_size=540,
        ax=ax,
    )
    nx.draw_networkx_labels(graph, pos, labels={n: str(n) for n in nodes}, font_size=10, font_weight="bold", ax=ax)
    ax.set_title(title + (f"\n{subtitle}" if subtitle else ""), fontsize=15, fontweight="bold")
    save(fig, folder, name)


def phase_decomposition(folder, name, pos, edges, title):
    graph = nx.Graph()
    graph.add_nodes_from(pos)
    graph.add_edges_from(edges)
    fig, axes = plt.subplots(2, 3, figsize=(13, 8))
    for ax in axes.ravel():
        ax.axis("off")
        ax.set_aspect("equal")
    ax = axes[0, 0]
    nx.draw_networkx_edges(graph, pos, ax=ax, edge_color="#BBBBBB")
    nx.draw_networkx_nodes(
        graph,
        pos,
        ax=ax,
        node_color=[PHASE_COLORS[phase_of(n)] for n in graph],
        node_size=260,
        edgecolors="black",
    )
    nx.draw_networkx_labels(graph, pos, ax=ax, font_size=8)
    ax.set_title("Full graph")
    for ax, phase in zip(axes.ravel()[1:], PHASES):
        phase_nodes = [n for n in graph if phase_of(n) == phase]
        nx.draw_networkx_edges(graph, pos, ax=ax, edge_color="#DDDDDD")
        nx.draw_networkx_nodes(graph, pos, ax=ax, nodelist=list(graph), node_color="#EEEEEE", node_size=180)
        nx.draw_networkx_nodes(
            graph,
            pos,
            ax=ax,
            nodelist=phase_nodes,
            node_color=PHASE_COLORS[phase],
            node_size=300,
            edgecolors="black",
        )
        nx.draw_networkx_labels(graph, pos, labels={n: str(n) for n in phase_nodes}, ax=ax, font_size=8)
        ax.set_title(f"{phase}: sum {sum(phase_nodes)}")
    fig.suptitle(title, fontsize=15, fontweight="bold")
    save(fig, folder, name)


def matrix_spectrum(folder, name, graph, title):
    nodes = sorted(graph.nodes(), key=lambda n: ((n - 1) % 5, n))
    matrix = nx.to_numpy_array(graph, nodelist=nodes)
    eig = np.linalg.eigvalsh(matrix)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].imshow(matrix, cmap="Greys", interpolation="nearest")
    axes[0].set_title("Adjacency matrix by mod-5 phase")
    axes[0].set_xticks([])
    axes[0].set_yticks([])
    axes[1].bar(range(len(eig)), sorted(eig), color="#4A90E2")
    axes[1].axhline(0, color="black", lw=0.8)
    axes[1].set_title("Adjacency eigenvalues")
    axes[1].set_xlabel("Index")
    axes[1].set_ylabel("Eigenvalue")
    fig.suptitle(title, fontsize=15, fontweight="bold")
    save(fig, folder, name)


def phase_relations(folder, name, graph, title):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    ax = axes[0]
    ax.axis("off")
    ax.set_aspect("equal")
    angles = np.linspace(math.pi / 2, math.pi / 2 - 2 * math.pi, 6)[:-1]
    phase_pos = {phase: (math.cos(angle), math.sin(angle)) for phase, angle in zip(PHASES, angles)}
    for phase, (x, y) in phase_pos.items():
        ax.scatter([x], [y], s=900, c=PHASE_COLORS[phase], edgecolors="black")
        text_color = "white" if phase in {"Water", "Fire", "Wood"} else "black"
        ax.text(x, y, phase, ha="center", va="center", fontsize=10, fontweight="bold", color=text_color)
    generating = [("Water", "Wood"), ("Wood", "Fire"), ("Fire", "Earth"), ("Earth", "Metal"), ("Metal", "Water")]
    overcoming = [("Water", "Fire"), ("Fire", "Metal"), ("Metal", "Wood"), ("Wood", "Earth"), ("Earth", "Water")]
    for a, b in generating:
        ax.plot([phase_pos[a][0], phase_pos[b][0]], [phase_pos[a][1], phase_pos[b][1]], color="#44AA44", lw=2)
    for a, b in overcoming:
        ax.plot([phase_pos[a][0], phase_pos[b][0]], [phase_pos[a][1], phase_pos[b][1]], color="#CC4444", lw=1, ls="--")
    ax.set_title("Five-phase relations")
    counts = Counter()
    for u, v in graph.edges():
        a, b = phase_of(u), phase_of(v)
        if a == b:
            counts["same"] += 1
        elif (a, b) in generating or (b, a) in generating:
            counts["generating"] += 1
        elif (a, b) in overcoming or (b, a) in overcoming:
            counts["overcoming"] += 1
        else:
            counts["neutral"] += 1
    axes[1].bar(counts.keys(), counts.values(), color=["#CC9944", "#44AA44", "#CC4444", "#888888"])
    axes[1].set_title("Edge relation counts")
    fig.suptitle(title, fontsize=15, fontweight="bold")
    save(fig, folder, name)


def grouped_bars(folder, name, labels, series, title, ylabel="Sum"):
    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(labels))
    width = 0.8 / max(1, len(series))
    for index, (label, values, color) in enumerate(series):
        ax.bar(x + (index - (len(series) - 1) / 2) * width, values, width, label=label, color=color, edgecolor="black")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.legend()
    save(fig, folder, name)


def generate_palace_family(folder, palaces, total_n, target_sum, title):
    origins = {"Top": (3, 6), "Left": (0, 3), "Center": (3, 3), "Right": (6, 3), "Bottom": (3, 0)}
    pos, owner, cell = build_positions(palaces, origins)
    intra_edges = build_edges(pos, owner, intra_only=True)
    full_edges = build_edges(pos, owner, intra_only=False)
    graph = nx.Graph()
    graph.add_nodes_from(pos)
    graph.add_edges_from(full_edges)
    draw_graph(folder, "01_original_graph.png", pos, full_edges, f"{title}: original cross structure", f"Five palaces, target sum {target_sum}")
    phase_decomposition(folder, "02_wuxing_decomposition.png", pos, full_edges, f"{title}: mod-5 phase decomposition")
    matrix_spectrum(folder, "03_adjacency_spectrum.png", graph, f"{title}: adjacency matrix and spectrum")
    draw_graph(folder, "04_cycle_analysis.png", pos, intra_edges, f"{title}: internal palace graph", "Palace-internal adjacency only")
    betweenness = nx.betweenness_centrality(graph)
    top_nodes = set(sorted(betweenness, key=betweenness.get, reverse=True)[:4])
    draw_graph(folder, "05_centrality_invariants.png", pos, full_edges, f"{title}: centrality gateways", "Highlighted nodes have highest betweenness", top_nodes)
    phase_relations(folder, "06_wuxing_relations.png", graph, f"{title}: five-phase edge relations")
    start, step = (148, 8) if total_n == 40 else (189, 9)
    grouped_bars(
        folder,
        "07_local_extensions.png",
        ["M0=1", "M0=2", "M0=3", "M0=4", "M0=5"],
        [("palace sum", [start + i * step for i in range(5)], "#4A90E2")],
        f"{title}: generalized family",
    )
    palace_names = ["Top", "Left", "Center", "Right", "Bottom"]
    corner_sums, edge_sums, center_values = [], [], []
    for palace in palace_names:
        corner_sum = edge_sum = center_value = 0
        for row in palaces[palace]:
            for value in row:
                if value is None:
                    continue
                r, c = cell[value]
                if (r, c) == (1, 1):
                    center_value = value
                elif (r, c) in {(0, 0), (0, 2), (2, 0), (2, 2)}:
                    corner_sum += value
                else:
                    edge_sum += value
        corner_sums.append(corner_sum)
        edge_sums.append(edge_sum)
        center_values.append(center_value)
    series = [("corners", corner_sums, "#CC4444"), ("edge midpoints", edge_sums, "#4488CC")]
    if any(center_values):
        series.append(("centers", center_values, "#44AA44"))
    grouped_bars(folder, "08_position_patterns.png", palace_names, series, f"{title}: positional sum patterns")


def generate_eight_each_gets(folder="."):
    palaces = {
        "Top": [[39, 7, 34], [12, None, 19], [24, 2, 27]],
        "Left": [[33, 18, 28], [8, None, 3], [38, 13, 23]],
        "Center": [[30, 5, 21], [16, None, 15], [31, 10, 36]],
        "Right": [[22, 14, 37], [4, None, 9], [29, 17, 32]],
        "Bottom": [[26, 1, 25], [20, None, 11], [35, 6, 40]],
    }
    generate_palace_family(folder, palaces, 40, 164, "Paljagakdeuk")


def generate_nine_each_gets(folder="."):
    palaces = {
        "Top": [[12, 44, 9], [19, 21, 29], [37, 2, 34]],
        "Left": [[13, 43, 8], [18, 25, 26], [38, 3, 33]],
        "Center": [[15, 41, 6], [16, 23, 30], [40, 5, 31]],
        "Right": [[14, 42, 7], [17, 24, 28], [39, 4, 32]],
        "Bottom": [[11, 45, 10], [20, 22, 27], [36, 1, 35]],
    }
    generate_palace_family(folder, palaces, 45, 207, "Gujagakdeuk")


def text_panel(folder, name, title, items):
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.axis("off")
    ax.set_title(title, fontsize=16, fontweight="bold")
    y = 0.85
    for item in items:
        ax.text(0.05, y, item, fontsize=12, va="top")
        y -= 0.12
    save(fig, folder, name)


def generate_four_each_gets_luoshu(folder="."):
    pos = {
        19: (-2, 3), 2: (-3, 2), 14: (-2, 1), 5: (-1, 0), 16: (0, 1), 7: (-1, 2),
        17: (2, 3), 4: (1, 2), 9: (3, 2), 12: (2, 1), 10: (1, 0),
        18: (-2, -1), 3: (-3, -2), 13: (-2, -3), 8: (-1, -2), 11: (0, -1),
        6: (2, -1), 1: (3, -2), 20: (2, -3), 15: (1, -2),
    }
    edges = [
        (19, 2), (2, 14), (14, 5), (5, 16), (16, 7), (7, 19),
        (17, 4), (4, 16), (16, 10), (10, 12), (12, 9), (9, 17),
        (5, 18), (18, 3), (3, 13), (13, 8), (8, 11), (11, 5),
        (10, 6), (6, 1), (1, 20), (20, 15), (15, 11), (11, 10),
    ]
    graph = nx.Graph()
    graph.add_nodes_from(pos)
    graph.add_edges_from(edges)
    draw_graph(folder, "01_original_graph.png", pos, edges, "Nakseo Sagudo: corrected source graph", "3x2 structure with four shared vertices", {5, 16, 10, 11})
    phase_decomposition(folder, "02_wuxing_decomposition.png", pos, edges, "Nakseo Sagudo: mod-5 phase decomposition")
    matrix_spectrum(folder, "03_adjacency_spectrum.png", graph, "Nakseo Sagudo: adjacency matrix and spectrum")
    draw_graph(folder, "04_cycle_analysis.png", pos, edges, "Nakseo Sagudo: outer and inner cycles", "Inner 4-cycle sum: 42", {5, 16, 10, 11})
    draw_graph(folder, "05_centrality_invariants.png", pos, edges, "Nakseo Sagudo: centrality invariants", "Shared vertices are central gateways", {5, 16, 10, 11})
    phase_relations(folder, "06_wuxing_relations.png", graph, "Nakseo Sagudo: five-phase edge relations")
    grouped_bars(folder, "07_local_extensions.png", ["20", "40", "60", "80", "100", "120"], [("scaled nodes", [20, 40, 60, 80, 100, 120], "#4A90E2")], "Nakseo Sagudo: source-based extensions", "Nodes")
    lap = np.linalg.eigvalsh(nx.laplacian_matrix(graph, nodelist=sorted(graph)).toarray())
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(range(len(lap)), lap, color="#4A90E2")
    ax.set_title("Laplacian spectrum", fontweight="bold")
    ax.set_ylabel("Eigenvalue")
    save(fig, folder, "08_laplacian_spectrum.png")
    dist = dict(nx.all_pairs_shortest_path_length(graph))
    matrix = np.array([[dist[i][j] for j in sorted(graph)] for i in sorted(graph)])
    fig, ax = plt.subplots(figsize=(6, 5))
    image = ax.imshow(matrix, cmap="viridis")
    fig.colorbar(image, ax=ax)
    ax.set_title("Shortest-path distance matrix", fontweight="bold")
    ax.set_xticks([])
    ax.set_yticks([])
    save(fig, folder, "09_distance_matrix.png")
    cycles = nx.cycle_basis(graph)
    length_counts = Counter(map(len, cycles))
    sum_counts = Counter(sum(cycle) for cycle in cycles)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].bar(length_counts.keys(), length_counts.values(), color="#4488CC")
    axes[0].set_title("Cycle lengths")
    axes[1].bar([str(k) for k in sum_counts.keys()], sum_counts.values(), color="#CC9944")
    axes[1].set_title("Cycle sum frequencies")
    save(fig, folder, "10_cycle_distributions.png")
    panels = {
        "11_dual_graph.png": ("Dual Graph of Four Faces", ["Vertices: NW, NE, SW, SE", "Shared weights: 5, 16, 10, 11", "Weight sum: 42"]),
        "12_wuxing_block_matrix.png": ("Five-Phase Block Matrix", ["Rows and columns are Water, Fire, Wood, Metal, Earth.", "Edges are same-phase, generating, or overcoming.", "Overcoming edges dominate this graph."]),
        "13_extension_120.png": ("120-Node Extension", ["Six cyclic copies of the 20-node source graph.", "Shared vertices connect to the next copy.", "Total nodes: 120. Total edges: 168."]),
        "14_shared_vertex_symmetry.png": ("Shared Vertex Symmetry", ["Shared vertices: 5, 16, 10, 11.", "All have degree 4.", "They share high centrality values."]),
        "15_sw_wood_concentration.png": ("SW Face Wood Concentration", ["SW face: 5, 18, 3, 13, 8, 11.", "Wood vertices: 3, 8, 13, 18.", "The Wood phase is concentrated in one face."]),
        "origin_01_hutu_5palaces.png": ("Hado 4-5 Basis", ["Four directions plus five phases.", "4 x 5 = 20 source numbers.", "4 + 5 = 9 palace blocks."]),
        "origin_02_9palace_grid.png": ("Nine Palace Blocks with Sum 42", ["Nine blocks: NW, N, NE, W, C, E, SW, S, SE.", "Each block has four numbers.", "Every block sums to 42."]),
        "origin_03_right_rotation.png": ("Right Rotation Structure", ["Boundary blocks follow clockwise order.", "The center block stays fixed.", "This is the right-rotation reading."]),
        "origin_04_mutual_transformation_1890.png": ("Mutual Transformation Gives 1890", ["Five phase classes times nine blocks gives 45 incidences.", "Each incidence carries weight 42.", "45 x 42 = 1890."]),
        "origin_05_42_invariants.png": ("The 42 Invariant", ["Inner 4-cycle sum: 42.", "Wood phase sum: 42.", "Every nine-palace block sum: 42."]),
        "origin_06_graph_with_9palace.png": ("Nine Palaces on the Source Graph", ["Nine blocks are read from neighboring overlaps.", "The center block is the inner 4-cycle.", "Corner blocks use outer vertices of faces."]),
        "origin_translated_01_terms.png": ("Annotation Terms in Modern Language", ["Neighboring stars combine: adjacent block overlap.", "Five palaces become nine: residue classes become blocks.", "Each obtains four numbers: block size 4."]),
        "origin_translated_02_blocks.png": ("From Five Classes to Nine Blocks", ["Input: five mod-5 residue classes.", "Output: nine balanced four-element blocks.", "Invariant: every block sums to 42."]),
        "origin_translated_03_overlap.png": ("Overlap Interpretation", ["Adjacent blocks share elements.", "The system is an incidence structure, not a partition.", "Overlap explains neighboring combination."]),
        "origin_translated_04_invariant_table.png": ("Invariant Table", ["Total sum 1..20: 210.", "Average phase sum: 42.", "Inner cycle sum: 42.", "Nine block sums: all 42."]),
        "origin_translated_05_cyclic_action.png": ("Cyclic Action", ["Eight boundary blocks rotate clockwise around the center.", "The center block remains fixed.", "This is the right-rotation reading."]),
        "origin_translated_06_weighted_incidence.png": ("Weighted Incidence Count", ["5 phase classes x 9 blocks = 45 incidences.", "Each incidence has weight 42.", "Total weighted count: 1890."]),
    }
    for name, (title, items) in panels.items():
        text_panel(folder, name, title, items)
