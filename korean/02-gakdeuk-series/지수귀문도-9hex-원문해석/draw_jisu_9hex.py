#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Draw the exact 30-vertex 9-hex Jisuguimundo (지수귀문도) graph.

This script uses the topology and a solved assignment to render a
publication-style figure.  All identifiers are intentionally in English so the
code can be reused by the English-language folder without transliteration.
"""

from __future__ import annotations

import json
import math
import os
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent


def load_topology(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_solution(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_coords(topology: dict[str, Any]) -> dict[int, tuple[float, float]]:
    """Return {original_node_id: (x, y)} using the stored vertex coordinates."""
    coords: dict[int, tuple[float, float]] = {}
    for node_id_str, pt in topology["vertices"].items():
        coords[int(node_id_str)] = (float(pt["x"]), float(pt["y"]))
    return coords


def build_unique_edges(topology: dict[str, Any]) -> set[tuple[int, int]]:
    """Return the undirected edge set from the stored edge list."""
    unique: set[tuple[int, int]] = set()
    for u, v in topology["edges"]:
        unique.add(tuple(sorted((int(u), int(v)))))
    return unique


def draw_solution(
    topology: dict[str, Any],
    solution: dict[str, Any],
    output_path: Path,
    figsize: tuple[float, float] = (10, 14),
) -> None:
    coords = build_coords(topology)
    edges = build_unique_edges(topology)
    assignment: list[int] = solution["assignment"]
    magic_constant: int = solution["S"]

    fig, ax = plt.subplots(figsize=figsize, facecolor="#5e5e5e")
    ax.set_aspect("equal")
    ax.axis("off")

    # Edges
    for u, v in edges:
        x_pts = [coords[u][0], coords[v][0]]
        y_pts = [coords[u][1], coords[v][1]]
        ax.plot(x_pts, y_pts, color="#7f7f7f", linewidth=4, zorder=1)

    # Nodes with solved values
    for node_id in sorted(coords):
        x, y = coords[node_id]
        value = assignment[node_id - 1]
        ax.scatter(
            x, y,
            color="#ffffff",
            edgecolors="#a6a6a6",
            s=1500,
            linewidths=3.5,
            zorder=2,
        )
        ax.text(
            x, y, str(value),
            color="#2c2c2c",
            fontsize=18,
            fontweight="bold",
            va="center",
            ha="center",
            zorder=3,
        )

    # Magic constant in each hexagon centre
    dy = math.sqrt(3) / 2
    hex_centers = [
        (0.0, 3.0 * dy),
        (-0.5, 1.5 * dy),
        (0.5, 1.5 * dy),
        (-1.0, 0.0 * dy),
        (0.0, 0.0 * dy),
        (1.0, 0.0 * dy),
        (-0.5, -1.5 * dy),
        (0.5, -1.5 * dy),
        (0.0, -3.0 * dy),
    ]
    for cx, cy in hex_centers:
        ax.text(
            cx, cy, str(magic_constant),
            color="#757575",
            fontsize=22,
            fontweight="bold",
            va="center",
            ha="center",
            zorder=1,
        )

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {output_path}")


def main() -> None:
    topology = load_topology(ROOT / "jisu_9hex_topology.json")
    solution = load_solution(ROOT / "jisu_9hex_solution.json")
    output = ROOT / "jisu_9hex_solution.png"
    draw_solution(topology, solution, output)


if __name__ == "__main__":
    main()
