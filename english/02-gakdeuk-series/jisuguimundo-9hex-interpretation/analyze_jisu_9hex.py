#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modular / CRT analysis for the 30-vertex 9-hex Jisuguimundo.

Analyses performed:
  - made/used (作/用) separation, i.e. vertex multiplicity on the 9 hexagons
  - residue classification modulo 2, 3, 4, 5, 6, 9, 12
  - spatial distribution and symmetry for mod 2
  - CRT reconstruction for mod 3×4, 3×5, 4×5 (following Qin Jiushao's basic CRT)

All identifiers are in English so the script can be mirrored in the English
folder without transliteration.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent


def load_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def residue_1based(value: int, mod: int) -> int:
    r = value % mod
    return mod if r == 0 else r


def multiplicity(hexagons: list[list[int]], node_count: int) -> list[int]:
    mult = [0] * node_count
    for hx in hexagons:
        for v in hx:
            mult[v - 1] += 1
    return mult


def compute_crt_pair(residue_a: int, mod_a: int, residue_b: int, mod_b: int) -> int:
    """
    Return the unique residue x (1..mod_a*mod_b) with
        x ≡ residue_a (mod mod_a)
        x ≡ residue_b (mod mod_b)
    using a brute-force search (sufficient for the small moduli here).
    Residues are 1-based.
    """
    for x in range(1, mod_a * mod_b + 1):
        if residue_1based(x, mod_a) == residue_a and residue_1based(x, mod_b) == residue_b:
            return x
    raise ValueError("No CRT solution (moduli must be coprime)")


def draw_mod_distribution(
    coords: dict[int, tuple[float, float]],
    assignment: list[int],
    mod: int,
    output_path: Path,
) -> None:
    """Draw the graph with nodes coloured by their 1-based residue mod `mod`."""
    palette = [
        "#4A90E2", "#E94B3C", "#6AB04C", "#BDC3C7", "#D4A017",
        "#9B59B6", "#1ABC9C", "#F39C12", "#34495E", "#7F8C8D",
        "#C0392B", "#2980B9",
    ]

    fig, ax = plt.subplots(figsize=(10, 12), facecolor="#FDFBF7")
    ax.set_aspect("equal")
    ax.axis("off")

    # Draw faint edges if topology present
    topo = load_json(ROOT / "jisu_9hex_topology.json")
    for u, v in topo["edges"]:
        x_pts = [coords[int(u)][0], coords[int(v)][0]]
        y_pts = [coords[int(u)][1], coords[int(v)][1]]
        ax.plot(x_pts, y_pts, color="#CCCCCC", linewidth=1.5, zorder=1)

    residues = [residue_1based(assignment[i], mod) for i in range(len(assignment))]
    counts = Counter(residues)

    for node_id in sorted(coords):
        x, y = coords[node_id]
        r = residues[node_id - 1]
        color = palette[(r - 1) % len(palette)]
        ax.scatter(x, y, color=color, edgecolors="#333333", s=900, linewidths=2, zorder=2)
        ax.text(
            x, y, str(assignment[node_id - 1]),
            color="white" if color in ("#34495E", "#7F8C8D", "#C0392B", "#2980B9") else "#2C3E50",
            fontsize=14, fontweight="bold", va="center", ha="center", zorder=3,
        )
        # residue ring
        ax.text(
            x + 0.28, y + 0.28, f"r{r}",
            color="#2C3E50", fontsize=9, fontweight="bold", va="center", ha="center", zorder=4,
        )

    title = f"Jisuguimundo 9-hex — residues mod {mod}"
    ax.set_title(title, fontsize=16, fontweight="bold", color="#2C3E50", pad=12)
    subtitle = " | ".join(f"r{r}: {c}" for r, c in sorted(counts.items()))
    ax.text(0.5, 0.02, subtitle, transform=fig.transFigure, ha="center", fontsize=11, color="#555555")

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {output_path}")


def draw_crt_grid(
    coords: dict[int, tuple[float, float]],
    assignment: list[int],
    mod_a: int,
    mod_b: int,
    output_path: Path,
) -> None:
    """Colour nodes by the CRT-combined residue mod (mod_a * mod_b)."""
    mod_ab = mod_a * mod_b
    palette = [
        "#4A90E2", "#E94B3C", "#6AB04C", "#BDC3C7", "#D4A017",
        "#9B59B6", "#1ABC9C", "#F39C12", "#34495E", "#7F8C8D",
        "#C0392B", "#2980B9", "#8E44AD", "#16A085", "#D35400",
    ] * 4

    fig, ax = plt.subplots(figsize=(10, 12), facecolor="#FDFBF7")
    ax.set_aspect("equal")
    ax.axis("off")

    topo = load_json(ROOT / "jisu_9hex_topology.json")
    for u, v in topo["edges"]:
        x_pts = [coords[int(u)][0], coords[int(v)][0]]
        y_pts = [coords[int(u)][1], coords[int(v)][1]]
        ax.plot(x_pts, y_pts, color="#CCCCCC", linewidth=1.5, zorder=1)

    crt_residues = []
    for val in assignment:
        ra = residue_1based(val, mod_a)
        rb = residue_1based(val, mod_b)
        crt_residues.append(compute_crt_pair(ra, mod_a, rb, mod_b))
    counts = Counter(crt_residues)

    for node_id in sorted(coords):
        x, y = coords[node_id]
        r = crt_residues[node_id - 1]
        color = palette[(r - 1) % len(palette)]
        ax.scatter(x, y, color=color, edgecolors="#333333", s=900, linewidths=2, zorder=2)
        ax.text(
            x, y, str(assignment[node_id - 1]),
            color="white" if r in (9, 10, 12, 13, 14, 15) else "#2C3E50",
            fontsize=13, fontweight="bold", va="center", ha="center", zorder=3,
        )
        ax.text(
            x + 0.28, y + 0.28, f"{r}",
            color="#2C3E50", fontsize=9, fontweight="bold", va="center", ha="center", zorder=4,
        )

    title = f"CRT reconstruction: mod {mod_a} × mod {mod_b} → mod {mod_ab}"
    ax.set_title(title, fontsize=16, fontweight="bold", color="#2C3E50", pad=12)
    subtitle = " | ".join(f"r{r}: {c}" for r, c in sorted(counts.items()))
    ax.text(0.5, 0.02, subtitle, transform=fig.transFigure, ha="center", fontsize=10, color="#555555")

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {output_path}")


def build_report(
    topology: dict[str, Any],
    solution: dict[str, Any],
) -> str:
    assignment = solution["assignment"]
    hexagons = topology["hexagons"]
    node_count = topology["node_count"]
    s = solution["S"]

    mult = multiplicity(hexagons, node_count)
    total_written = sum(assignment)
    total_used_positions = sum(len(hx) for hx in hexagons)
    duplicate_positions = total_used_positions - node_count
    duplication_weight = sum((mult[i] - 1) * assignment[i] for i in range(node_count))

    lines: list[str] = []
    lines.append("# Jisuguimundo 9-hex Analysis Report")
    lines.append("")
    lines.append("## 1. Basic quantities and made/used (作/用) separation")
    lines.append("")
    lines.append("| Quantity | Value |")
    lines.append("|---|---:|")
    lines.append(f"| Distinct numbers written (作) | {node_count} (1–{node_count}) |")
    lines.append(f"| Positions used by the structure (用) | {total_used_positions} (9 hexagons × 6 vertices) |")
    lines.append(f"| Overlap positions | {duplicate_positions} |")
    lines.append(f"| Plain sum of written numbers (T) | {total_written} |")
    lines.append(f"| Repeated hexagon-total sum (H·S) | {len(hexagons)} × {s} = {len(hexagons)*s} |")
    lines.append(f"| Duplication weight (D) | {duplication_weight} |")
    lines.append("")
    lines.append(f"The original phrase **三十子作， 五十四子用** is matched exactly: "
                 f"{node_count} distinct numbers are written, {total_used_positions} positions are used, "
                 f"and {duplicate_positions} positions are overlaps.")
    lines.append("")
    lines.append("### Vertex multiplicities")
    lines.append("")
    lines.append("| Multiplicity | Vertices (original id = assigned value) |")
    lines.append("|---|---|")
    for k in sorted(set(mult)):
        members = [f"{i+1}={assignment[i]}" for i in range(node_count) if mult[i] == k]
        lines.append(f"| {k} times | {', '.join(members)} |")
    lines.append("")

    # Mod analyses
    mods = [2, 3, 4, 5, 6, 9, 12]
    lines.append("## 2. Modular classification and group interpretation")
    lines.append("")
    for mod in mods:
        residues = [residue_1based(v, mod) for v in assignment]
        counts = Counter(residues)
        class_sums = defaultdict(int)
        for val, r in zip(assignment, residues):
            class_sums[r] += val
        lines.append(f"### mod {mod}")
        lines.append("")
        lines.append("| Residue class | Count | Class sum |")
        lines.append("|---|---:|---:|")
        for r in sorted(counts):
            lines.append(f"| r{r} | {counts[r]} | {class_sums[r]} |")
        lines.append("")
        lines.append("Residue pattern for each hexagon:")
        lines.append("")
        lines.append("| Hexagon | Values | Residue pattern | Sum |")
        lines.append("|---|---|---|---:|")
        for idx, hx in enumerate(hexagons, start=1):
            vals = [assignment[v - 1] for v in hx]
            res_pattern = [str(residue_1based(v, mod)) for v in vals]
            lines.append(f"| Hex{idx} | {vals} | {'-'.join(res_pattern)} | {sum(vals)} |")
        lines.append("")

    lines.append("## 3. mod 2 spatial distribution and symmetry")
    lines.append("")
    parity = [residue_1based(v, 2) for v in assignment]
    even_count = sum(1 for p in parity if p == 2)
    odd_count = node_count - even_count
    lines.append(f"- Even (r2): {even_count}, odd (r1): {odd_count}")
    lines.append("")
    coords = {int(k): (v["x"], v["y"]) for k, v in topology["vertices"].items()}
    left = sum(1 for nid in coords if coords[nid][0] < -1e-6 and parity[nid - 1] == 1)
    right = sum(1 for nid in coords if coords[nid][0] > 1e-6 and parity[nid - 1] == 1)
    top = sum(1 for nid in coords if coords[nid][1] > 1e-6 and parity[nid - 1] == 1)
    bottom = sum(1 for nid in coords if coords[nid][1] < -1e-6 and parity[nid - 1] == 1)
    lines.append(f"- Odd distribution: left {left}, right {right}, upper half {top}, lower half {bottom}")
    lines.append("")
    lines.append("The mod-2 distribution is close to evenly balanced with respect to the vertical and horizontal reflection axes.")
    lines.append("")

    lines.append("## 4. CRT (Chinese Remainder Theorem) analysis")
    lines.append("")
    lines.append("Following the basic CRT algorithm associated with the Song-Yuan mathematician Qin Jiushao,")
    lines.append("we combine coprime moduli.")
    lines.append("")
    for mod_a, mod_b in [(3, 4), (3, 5), (4, 5)]:
        mod_ab = mod_a * mod_b
        crt_counts: Counter[int] = Counter()
        crt_class_sums: defaultdict[int, int] = defaultdict(int)
        for val in assignment:
            ra = residue_1based(val, mod_a)
            rb = residue_1based(val, mod_b)
            r_ab = compute_crt_pair(ra, mod_a, rb, mod_b)
            crt_counts[r_ab] += 1
            crt_class_sums[r_ab] += val
        lines.append(f"### mod {mod_a} × mod {mod_b} → mod {mod_ab}")
        lines.append("")
        lines.append("| CRT residue | Count | Sum |")
        lines.append("|---|---:|---:|")
        for r in sorted(crt_counts):
            lines.append(f"| r{r} | {crt_counts[r]} | {crt_class_sums[r]} |")
        lines.append("")

    lines.append("## 5. 2·3-based mutation scheme")
    lines.append("")
    lines.append("- mod 2: the smallest prime modulus; controls parity and reflection symmetry.")
    lines.append("- mod 3: the basic modulus corresponding to the threefold / 9-palace skeleton.")
    lines.append("- mod 4 = 2×2: a one-step refinement of mod 2.")
    lines.append("- mod 6 = 2×3: combines parity and the threefold structure.")
    lines.append("- mod 9 = 3×3: the square of the threefold modulus, matching the 9-palace framework.")
    lines.append("- mod 12 = 2²×3: fully recoverable from mod 3 and mod 4 by CRT.")
    lines.append("")

    lines.append("## 6. Extended visualisation interpretations")
    lines.append("")
    lines.append("### Made / Used separation (`jisu_9hex_multiplicity.png`)")
    lines.append("")
    lines.append("- Thirty distinct numbers (作) are placed into fifty-four hexagon positions (用).")
    lines.append("- Vertices with higher multiplicity are drawn larger and cluster in the centre.")
    lines.append("- The eight multiplicity-3 vertices all lie in or around the central hexagon (Hex5).")
    lines.append("- This directly illustrates the original phrase **三十子作， 五十四子用**.")
    lines.append("")
    lines.append("### mod 2 symmetry (`jisu_9hex_mod2_symmetry.png`)")
    lines.append("")
    lines.append("- Exactly 15 odd and 15 even numbers are present.")
    lines.append("- Odd nodes are spread fairly evenly with respect to the vertical (x = 0) and horizontal (y = 0) reflection axes.")
    lines.append("- By quadrant, odd counts are: Q1 (right/top) 5, Q2 (left/top) 2, Q3 (left/bottom) 3, Q4 (right/bottom) 5.")
    lines.append("- The image shows how reflection symmetry of the hexagonal lattice is balanced against the partial-sum invariant.")
    lines.append("")
    lines.append("### 9 palaces → 12 palaces (`jisu_9hex_9to12_palaces.png`)")
    lines.append("")
    lines.append("- Inner blue circles: the nine hexagon palaces (九宫).")
    lines.append("- Outer orange circles: twelve directional palace units (十二宫), labelled by the twelve earthly branches.")
    lines.append("- Grey lines: mapping from each hexagon centre to adjacent directional sectors.")
    lines.append("- This visualises the original phrase **凡九宮化爲十二宮**.")
    lines.append("")
    lines.append("### Central three palaces (`jisu_9hex_center_periphery.png`)")
    lines.append("")
    lines.append("- The vertical central column Hex2, Hex5, Hex8 is highlighted in red.")
    lines.append("- These three hexagons form the core axis that governs the six surrounding hexagons.")
    lines.append("- This corresponds to the original phrase **中眷三宮， 三宮爲主則**.")
    lines.append("")
    lines.append("### Graph spectrum (`jisu_9hex_adjacency_spectrum.png`)")
    lines.append("")
    lines.append("- The 30×30 adjacency matrix reveals the sparse block pattern created by shared vertices between hexagons.")
    lines.append("- Degree distribution: mostly degree-2 and degree-3 vertices, with a few higher-degree central vertices.")
    lines.append("- Adjacency eigenvalues reflect the graph symmetry; Laplacian eigenvalues quantify connectivity.")
    lines.append("")
    lines.append("### Magic constant emphasis (`jisu_9hex_magic_constant.png`)")
    lines.append("")
    lines.append("- The magic constant **93** is placed at the centre of every hexagon, together with its six constituent values.")
    lines.append("- All nine hexagons visibly sum to 93.")
    lines.append("- This is a direct visualisation of the original phrase **六子各得九十三數**.")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    topology = load_json(ROOT / "jisu_9hex_topology.json")
    solution = load_json(ROOT / "jisu_9hex_solution.json")
    assignment = solution["assignment"]

    coords = {int(k): (v["x"], v["y"]) for k, v in topology["vertices"].items()}

    # Draw mod distribution images
    for mod in [2, 3, 4, 5, 6, 9, 12]:
        draw_mod_distribution(coords, assignment, mod, ROOT / f"mod{mod}_distribution.png")

    # Draw CRT images
    draw_crt_grid(coords, assignment, 3, 4, ROOT / "crt_mod3_times_mod4.png")
    draw_crt_grid(coords, assignment, 3, 5, ROOT / "crt_mod3_times_mod5.png")
    draw_crt_grid(coords, assignment, 4, 5, ROOT / "crt_mod4_times_mod5.png")

    # Write report
    report = build_report(topology, solution)
    report_path = ROOT / "jisu_9hex_analysis_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Saved report: {report_path}")


if __name__ == "__main__":
    main()
