#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Per-cluster rotation analysis for the 30-vertex 9-hex Jisuguimundo.

Each hexagon is treated as a 6-element cyclic cluster.  The cycle is
canonicalised to start at the top vertex and proceed clockwise, then analysed
for residue pattern (mod 6), opposite-pair sums, and rotational invariance.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt


def _find_project_root() -> Path:
    p = Path(__file__).resolve()
    while p.parent != p:
        if (p / "rotation_analysis.py").exists():
            return p
        p = p.parent
    raise RuntimeError("Could not find project root containing rotation_analysis.py")


ROOT = _find_project_root()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rotation_analysis import (
    analyze_cycle,
    canonicalize_by_angle,
    draw_individual_clusters,
    draw_overview,
    find_global_rotation_symmetries,
    write_report,
)

OUTPUT_DIR = Path(".")


def load_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Noto Sans CJK KR", "Noto Sans CJK JP", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    topology = load_json(OUTPUT_DIR / "jisu_9hex_topology.json")
    solution = load_json(OUTPUT_DIR / "jisu_9hex_solution.json")
    assignment = solution["assignment"]

    coords = {int(k): (v["x"], v["y"]) for k, v in topology["vertices"].items()}

    analyses = []
    hex_centers: dict[str, tuple[float, float]] = {}
    for idx, hx in enumerate(topology["hexagons"], start=1):
        # hx uses 1-based node ids
        values = [assignment[v - 1] for v in hx]
        canonical = canonicalize_by_angle(values, coords, clockwise=True)
        analysis = analyze_cycle(canonical, modulo=6, name=f"Hex{idx}")
        analysis.notes.append(f"vertices = {hx}")
        analyses.append(analysis)
        hex_centers[f"Hex{idx}"] = (
            sum(coords[v][0] for v in hx) / len(hx),
            sum(coords[v][1] for v in hx) / len(hx),
        )

    global_syms = find_global_rotation_symmetries(hex_centers, candidates=[90, 120, 180, 270])

    draw_individual_clusters(analyses, str(OUTPUT_DIR / "rotation_cluster"))
    draw_overview(
        analyses,
        global_title="지수귀문도 9hex — 육각형별 회전 분석",
        save_path=str(OUTPUT_DIR / "rotation_overview.png"),
        ncols=3,
        modulo=6,
    )

    write_report(
        puzzle_name="지수귀문도 9hex (30정점 9육각형)",
        analyses=analyses,
        global_symmetries=global_syms,
        save_path=str(OUTPUT_DIR / "rotation_report.txt"),
    )


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
