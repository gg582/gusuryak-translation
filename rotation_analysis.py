#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shared helpers for per-cluster rotation analysis of Gusuryak puzzle diagrams.

This module is intentionally small and dependency-light (only numpy and matplotlib)
so that it can be imported by scripts running in many different subdirectories.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

import matplotlib.pyplot as plt
import numpy as np


# ---------------------------------------------------------------------------
# Cycle analysis
# ---------------------------------------------------------------------------

@dataclass
class CycleAnalysis:
    """Result of analyzing one cyclic cluster."""

    name: str
    values: list[int]                      # canonical cyclic order
    modulo: int                            # residue modulus used (5 or 9)
    opposite_sums: list[int] | None        # for even-length cycles
    residue_pattern: list[int]             # mod `modulo` of each value
    rotation_invariants: list[int]         # shifts k (0 <= k < n) with period==1
    is_fully_invariant: bool               # invariant under every rotation
    sum_total: int
    notes: list[str] = field(default_factory=list)


def residue_1based(value: int, modulo: int) -> int:
    """1-based residue: returns `modulo` when value % modulo == 0."""
    r = value % modulo
    return modulo if r == 0 else r


def canonicalize_by_angle(
    values: list[int],
    positions: dict[int, tuple[float, float]],
    clockwise: bool = True,
) -> list[int]:
    """
    Rotate a cyclic list so it starts at the element whose position is at the
    top (12 o'clock).  The remaining elements are ordered by angle:
    clockwise if `clockwise=True`, counter-clockwise otherwise.
    """
    if not values:
        return values

    def angle_of(v: int) -> float:
        x, y = positions[v]
        return math.degrees(math.atan2(y, x))

    # Top is 90 degrees.  Pick the value whose angle is closest to 90.
    start_idx = min(range(len(values)), key=lambda i: abs(angle_of(values[i]) - 90.0))

    # Sort remaining by angle.  Clockwise from top means decreasing angle.
    ordered = [values[(start_idx + i) % len(values)] for i in range(len(values))]
    if clockwise:
        # verify / enforce decreasing angle
        angles = [angle_of(v) for v in ordered]
        # If the next element does not have a smaller angle, reverse the tail.
        # A robust way: compute all rotations and pick the clockwise one.
        pass

    # More robust: produce all rotations starting from top and pick the one
    # whose angular sequence decreases monotonically (clockwise).
    candidates = []
    for offset in range(len(values)):
        rot = [values[(start_idx + offset + i) % len(values)] for i in range(len(values))]
        angs = [angle_of(v) for v in rot]
        # score = number of consecutive steps that go clockwise
        score = sum((angs[i] - angs[(i + 1) % len(values)] + 360) % 360 for i in range(len(values)))
        candidates.append((score, rot))
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1] if clockwise else candidates[-1][1]


def rotation_period(seq: list[int]) -> int:
    """Smallest positive shift k such that rotating seq by k leaves it unchanged."""
    n = len(seq)
    for k in range(1, n + 1):
        if all(seq[i] == seq[(i + k) % n] for i in range(n)):
            return k
    return n


def analyze_cycle(
    values: list[int],
    modulo: int,
    name: str = "cluster",
) -> CycleAnalysis:
    """
    Analyze a single cyclic cluster.

    Parameters
    ----------
    values : list[int]
        Elements in canonical cyclic order (start at top / 12 o'clock, clockwise).
    modulo : int
        Modulus for the residue / phase pattern (usually 5; 9 for Luoshu-style).
    name : str
        Human-readable cluster name.
    """
    n = len(values)
    residues = [residue_1based(v, modulo) for v in values]

    inv_shifts = []
    for k in range(n):
        if all(values[i] == values[(i + k) % n] for i in range(n)):
            inv_shifts.append(k)
    is_fully_invariant = len(inv_shifts) == n and n > 1

    opposite = None
    if n % 2 == 0:
        half = n // 2
        opposite = [values[i] + values[(i + half) % n] for i in range(half)]

    return CycleAnalysis(
        name=name,
        values=list(values),
        modulo=modulo,
        opposite_sums=opposite,
        residue_pattern=residues,
        rotation_invariants=inv_shifts,
        is_fully_invariant=is_fully_invariant,
        sum_total=sum(values),
    )


# ---------------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------------

PHASE_COLORS = {
    1: "#4A90E2",  # Water
    2: "#E94B3C",  # Fire
    3: "#6AB04C",  # Wood
    4: "#BDC3C7",  # Metal
    5: "#D4A017",  # Earth
}


def _residue_color(value: int, modulo: int) -> str:
    if modulo == 5:
        return PHASE_COLORS.get(residue_1based(value, 5), "#333333")
    # generic palette for mod 9 / others
    palette = ["#4A90E2", "#E94B3C", "#6AB04C", "#BDC3C7", "#D4A017",
               "#9B59B6", "#1ABC9C", "#F39C12", "#34495E"]
    return palette[(value % modulo) % len(palette)]


def draw_cluster_circle(
    ax: plt.Axes,
    analysis: CycleAnalysis,
    radius: float = 1.0,
    node_radius: float = 0.18,
    show_residue: bool = True,
    modulo: int | None = None,
) -> None:
    """Draw a single cluster as a circular cycle on the given axes."""
    values = analysis.values
    n = len(values)
    mod = modulo if modulo is not None else analysis.modulo

    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_facecolor("#FDFBF7")

    # Outer guide circle
    guide = plt.Circle((0, 0), radius, fill=False, color="#CCCCCC", linewidth=1, linestyle="--")
    ax.add_patch(guide)

    # Nodes
    for i, v in enumerate(values):
        angle = math.radians(90 - i * 360 / n)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        color = _residue_color(v, mod) if show_residue else "#FFFFFF"
        circ = plt.Circle((x, y), node_radius, color="white", ec=color, linewidth=2.5, zorder=3)
        ax.add_patch(circ)
        ax.text(x, y, str(v), ha="center", va="center", fontsize=9,
                fontweight="bold", color="#2C3E50", zorder=4)
        # residue label
        if show_residue:
            rx = x + 0.32 * math.cos(angle)
            ry = y + 0.32 * math.sin(angle)
            ax.text(rx, ry, f"r{residue_1based(v, mod)}", ha="center", va="center",
                    fontsize=7, color="#7F8C8D", zorder=4)

    # Opposite-pair chords for even cycles
    if analysis.opposite_sums is not None:
        half = n // 2
        for i in range(half):
            j = (i + half) % n
            a = math.radians(90 - i * 360 / n)
            b = math.radians(90 - j * 360 / n)
            ax.plot([radius * math.cos(a), radius * math.cos(b)],
                    [radius * math.sin(a), radius * math.sin(b)],
                    color="#95A5A6", linewidth=1, linestyle="-", zorder=1)

    # Title with invariance note
    inv_note = ""
    if len(analysis.rotation_invariants) > 1:
        inv_note = "  [invariant]"
    ax.set_title(f"{analysis.name}  Σ={analysis.sum_total}{inv_note}",
                 fontsize=11, fontweight="bold", color="#2C3E50", pad=8)
    ax.set_xlim(-radius - 0.6, radius + 0.6)
    ax.set_ylim(-radius - 0.6, radius + 0.6)


def draw_overview(
    analyses: list[CycleAnalysis],
    global_title: str,
    save_path: str,
    ncols: int = 3,
    modulo: int | None = None,
) -> None:
    """Draw a combined overview figure of all cluster cycles."""
    n = len(analyses)
    nrows = math.ceil(n / ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(ncols * 3.3, nrows * 3.3))
    fig.patch.set_facecolor("#FDFBF7")
    if n == 1:
        axes = np.array([axes])
    axes = np.atleast_1d(axes).flatten()

    for ax, analysis in zip(axes, analyses):
        draw_cluster_circle(ax, analysis, modulo=modulo)

    for ax in axes[n:]:
        ax.axis("off")
        ax.set_facecolor("#FDFBF7")

    fig.suptitle(global_title, fontsize=14, fontweight="bold", color="#2C3E50", y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(save_path, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved overview: {save_path}")


def draw_individual_clusters(
    analyses: list[CycleAnalysis],
    save_prefix: str,
    modulo: int | None = None,
) -> None:
    """Save one circular figure per cluster."""
    for analysis in analyses:
        safe_name = "".join(c if c.isalnum() else "_" for c in analysis.name)
        path = f"{save_prefix}_{safe_name}.png"
        fig, ax = plt.subplots(figsize=(4, 4))
        fig.patch.set_facecolor("#FDFBF7")
        draw_cluster_circle(ax, analysis, modulo=modulo)
        plt.tight_layout()
        plt.savefig(path, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
        plt.close()
        print(f"Saved cluster: {path}")


# ---------------------------------------------------------------------------
# Global rotational symmetry helpers
# ---------------------------------------------------------------------------

def cluster_centers_to_polar(centers: dict[Any, tuple[float, float]]) -> dict[Any, tuple[float, float]]:
    """Convert cluster centers to (radius, angle in degrees) relative to origin."""
    out = {}
    for name, (x, y) in centers.items():
        r = math.hypot(x, y)
        theta = math.degrees(math.atan2(y, x))
        out[name] = (r, theta)
    return out


def global_rotation_mapping(
    centers: dict[Any, tuple[float, float]],
    angle_deg: float,
    tolerance: float = 1e-6,
) -> dict[Any, Any] | None:
    """
    Check whether rotating all cluster centers by `angle_deg` maps centers to centers.

    Returns a dict mapping each cluster name to its image cluster, or None if the
    rotation is not a symmetry of the set of centers.
    """
    polar = cluster_centers_to_polar(centers)
    # target set
    target_set = set(centers.values())
    mapping = {}
    for name, (x, y) in centers.items():
        theta = math.radians(math.degrees(math.atan2(y, x)) + angle_deg)
        r = math.hypot(x, y)
        tx, ty = round(r * math.cos(theta), 6), round(r * math.sin(theta), 6)
        # find matching center
        match = None
        for other_name, (ox, oy) in centers.items():
            if abs(tx - ox) < tolerance and abs(ty - oy) < tolerance:
                match = other_name
                break
        if match is None:
            return None
        mapping[name] = match
    return mapping


def find_global_rotation_symmetries(
    centers: dict[Any, tuple[float, float]],
    candidates: list[float] | None = None,
    tolerance: float = 1e-6,
) -> dict[float, dict[Any, Any]]:
    """Return all global rotational symmetries (angle -> mapping)."""
    if candidates is None:
        candidates = [90, 180, 270]
    result = {}
    for angle in candidates:
        mapping = global_rotation_mapping(centers, angle, tolerance)
        if mapping is not None:
            result[angle] = mapping
    return result


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def _fmt_residue_pattern(pattern: list[int], modulo: int) -> str:
    names = {1: "W", 2: "F", 3: "Wd", 4: "M", 5: "E"}
    if modulo == 5:
        return "-".join(names.get(r, str(r)) for r in pattern)
    return "-".join(str(r) for r in pattern)


def format_cycle_report(analysis: CycleAnalysis) -> str:
    lines = []
    lines.append(f"Cluster: {analysis.name}")
    lines.append(f"  Cyclic order ({len(analysis.values)} elements): "
                 f"{' -> '.join(map(str, analysis.values))}")
    lines.append(f"  Sum: {analysis.sum_total}")
    lines.append(f"  Residue pattern (mod {analysis.modulo}): "
                 f"{_fmt_residue_pattern(analysis.residue_pattern, analysis.modulo)}")
    if analysis.opposite_sums is not None:
        lines.append(f"  Opposite-pair sums: {analysis.opposite_sums}")
        if len(set(analysis.opposite_sums)) == 1:
            lines.append(f"    -> All opposite pairs sum to {analysis.opposite_sums[0]}")
    inv = analysis.rotation_invariants
    if len(inv) > 1:
        lines.append(f"  Invariant under nontrivial rotations by shifts: {inv[1:]}")
    else:
        lines.append("  No nontrivial rotational invariance.")
    if analysis.notes:
        for note in analysis.notes:
            lines.append(f"  Note: {note}")
    lines.append("")
    return "\n".join(lines)


def format_global_symmetry_report(
    puzzle_name: str,
    global_symmetries: dict[float, dict[Any, Any]],
) -> str:
    lines = []
    lines.append(f"Global rotational symmetry for {puzzle_name}")
    lines.append("-" * 50)
    if not global_symmetries:
        lines.append("No nontrivial global rotation maps clusters to clusters.")
    else:
        lines.append(
            "NOTE: These are geometric cluster-center mappings under a counterclockwise rotation. "
            "They describe where each cluster's center moves; they do NOT imply the labels/stars "
            "inside the clusters are preserved or that the puzzle has a true label-rotation symmetry."
        )
        for angle in sorted(global_symmetries):
            mapping = global_symmetries[angle]
            lines.append(f"  {angle}° counterclockwise rotation:")
            for src, dst in mapping.items():
                marker = " (fixed)" if src == dst else ""
                lines.append(f"    {src} -> {dst}{marker}")
    lines.append("")
    return "\n".join(lines)


def write_report(
    puzzle_name: str,
    analyses: list[CycleAnalysis],
    global_symmetries: dict[float, dict[Any, Any]],
    save_path: str,
) -> None:
    """Write a text rotation report to disk and print it."""
    lines = [
        "=" * 60,
        f"Per-cluster rotation analysis: {puzzle_name}",
        "=" * 60,
        "",
    ]
    for analysis in analyses:
        lines.append(format_cycle_report(analysis))
    lines.append(format_global_symmetry_report(puzzle_name, global_symmetries))

    report = "\n".join(lines)
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(report)
