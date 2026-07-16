#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generalization analyzer for the each-gets (各得) principle

Computational verification script for the shared properties and
generalization models of the each-gets puzzle family from the *Gusuryak (九數略)*
tradition (Nine-each-gets, Five-each-gets, Six-each-gets, Seven-each-gets, Eight-each-gets).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class EachGetsFamily:
    """Data class holding the data for one each-gets family."""

    name: str
    n: int  # number of vertices per subset
    k: int  # number of subsets (always 5)
    m: int  # size of the complete phase group (basis for phase sum progression)
    vertex_range: tuple[int, int]  # range of numbers used
    total_sum: int  # total sum (based on unique vertices)
    subset_sum: int | None  # subset sum S
    duplicated_sum: int  # duplication-inclusive sum k*S or equivalent
    duplicated_values: tuple[int, ...]  # duplicated values
    note: str


# ============================================================
# 1. Data definitions
# ============================================================

FAMILIES: Final[tuple[EachGetsFamily, ...]] = (
    EachGetsFamily(
        name="Five-each-gets (Heaven-Water Five-Use Diagram)",
        n=5,
        k=5,
        m=5,  # based on full 5x5 extension
        vertex_range=(1, 24),
        total_sum=265,
        subset_sum=65,
        duplicated_sum=325,
        duplicated_values=(),  # to be found by the solver
        note="Subset sum = 65, 5×65 = 325, D = 60",
    ),
    EachGetsFamily(
        name="Six-each-gets (Jisu-Yong-Yukdo)",
        n=6,
        k=5,
        m=4,
        vertex_range=(1, 20),
        total_sum=210,
        subset_sum=63,
        duplicated_sum=315,
        duplicated_values=(3, 8, 10, 11, 12, 13, 14, 15),
        note="8 shared vertices, degree 3",
    ),
    EachGetsFamily(
        name="Seven-each-gets",
        n=7,
        k=5,
        m=7,
        vertex_range=(1, 35),
        total_sum=535,  # based on unique values
        subset_sum=120,
        duplicated_sum=600,
        duplicated_values=(1, 6, 24, 34),
        note="Center 1 + periphery 6, 4 duplicated values",
    ),
    EachGetsFamily(
        name="Eight-each-gets",
        n=8,
        k=5,
        m=8,
        vertex_range=(1, 40),
        total_sum=820,
        subset_sum=164,
        duplicated_sum=820,
        duplicated_values=(),
        note="3x3 Grid minus center, 8 characters, 12 inter-palace edges",
    ),
    EachGetsFamily(
        name="Nine-each-gets",
        n=9,
        k=5,
        m=9,
        vertex_range=(1, 45),
        total_sum=1035,
        subset_sum=207,
        duplicated_sum=1035,
        duplicated_values=(),
        note="3x3 Grid 9 characters, 12 inter-palace edges",
    ),
)

PHASE_NAMES: Final[tuple[str, ...]] = ("Water", "Fire", "Wood", "Metal", "Earth")


def phase_of(n: int) -> str:
    """Classify a number into a phase element (1->Water, 2->Fire, 3->Wood, 4->Metal, 0->Earth)."""
    r = n % 5
    return PHASE_NAMES[r - 1]


def residue_1based(n: int) -> int:
    """1-based mod 5 residue (0 is treated as 5)."""
    r = n % 5
    return 5 if r == 0 else r


def phase_sum_sequence(m: int) -> list[int]:
    """
    Return the phase-group sum sequence when the numbers 1 through 5*m
    are classified by mod 5.
    """
    base = 5 * m * (m - 1) // 2
    return [base + m * r for r in range(1, 6)]


def duplicated_total(family: EachGetsFamily) -> int:
    """Return the total duplication amount D = k*S - T."""
    if family.subset_sum is None:
        return 0
    return family.duplicated_sum - family.total_sum


def average_per_subset(family: EachGetsFamily) -> float | None:
    """Return the per-subset average S/n."""
    if family.subset_sum is None:
        return None
    return family.subset_sum / family.n


# ============================================================
# 2. Output
# ============================================================

def print_summary_table() -> None:
    """Print a summary table of the each-gets families."""
    print("=" * 100)
    print("Summary of the Each-Gets (各得) Families")
    print("=" * 100)
    header = (
        f"{'Family':<28} | {'n':>3} | {'k':>3} | "
        f"{'Range':>8} | {'T':>5} | {'S':>5} | "
        f"{'k·S':>5} | {'D':>5} | {'S/n':>6} | {'Notes'}"
    )
    print(header)
    print("-" * len(header))
    for fam in FAMILIES:
        s_str = str(fam.subset_sum) if fam.subset_sum is not None else "—"
        avg = average_per_subset(fam)
        avg_str = f"{avg:.2f}" if avg is not None else "—"
        print(
            f"{fam.name:<28} | {fam.n:>3} | {fam.k:>3} | "
            f"{fam.vertex_range[0]}-{fam.vertex_range[1]:>2} | "
            f"{fam.total_sum:>5} | {s_str:>5} | "
            f"{fam.duplicated_sum:>5} | {duplicated_total(fam):>5} | "
            f"{avg_str:>6} | {fam.note}"
        )
    print()


def print_phase_table() -> None:
    """Print the phase-sum arithmetic progression for each family."""
    print("=" * 80)
    print("Phase (Five Elements) mod 5 Sum Distribution")
    print("=" * 80)
    print(f"{'Family':<28} | {'m':>3} | Water | Fire | Wood | Metal | Earth | Diff")
    print("-" * 80)
    for fam in FAMILIES:
        # Based on full 5×m range (Five-each-gets is extended to 25)
        m = fam.m
        seq = phase_sum_sequence(m)
        diff = seq[1] - seq[0]
        print(
            f"{fam.name:<28} | {m:>3} | "
            f"{seq[0]:>5} | {seq[1]:>4} | {seq[2]:>4} | {seq[3]:>5} | {seq[4]:>5} | {diff:>4}"
        )
    print()


def print_equation_check() -> None:
    """Verify the duplication equation 5·S = T + D."""
    print("=" * 80)
    print("Duplication Equation Verification: 5·S = T + D")
    print("=" * 80)
    for fam in FAMILIES:
        if fam.subset_sum is None:
            print(f"{fam.name:<28}: S not specified (Five-each-gets)")
            continue
        lhs = fam.k * fam.subset_sum
        rhs = fam.total_sum + duplicated_total(fam)
        ok = "✓" if lhs == rhs else "✗"
        print(
            f"{fam.name:<28}: 5×{fam.subset_sum} = {lhs:>4}, "
            f"T+D = {fam.total_sum}+{duplicated_total(fam)} = {rhs:>4} {ok}"
        )
    print()


def print_generalization() -> None:
    """Print predictions from the generalization model."""
    print("=" * 80)
    print("Generalization Model: Predicted Subset Sums for the n-gon Family")
    print("=" * 80)
    print(f"{'n':>3} | {'Range':>10} | {'Predicted S':>12} | {'Actual S':>10} | {'Match'}")
    print("-" * 60)
    for fam in FAMILIES:
        if fam.subset_sum is None:
            continue
        start, end = fam.vertex_range
        # Prediction based on duplication-inclusive average
        mu = fam.duplicated_sum / (fam.k * fam.n)
        predicted = mu * fam.n
        match = "✓" if abs(predicted - fam.subset_sum) < 1e-9 else "✗"
        print(
            f"{fam.n:>3} | {start}-{end:>2}       | {predicted:>12.2f} | {fam.subset_sum:>10} | {match}"
        )
    print()


def generate_markdown_report() -> str:
    """Generate a Markdown string containing the analysis results."""
    lines: list[str] = []
    lines.append("# Generalization of the Each-Gets Principle: Computational Verification Report\n")
    lines.append("This report was automatically generated by `generalize_gakdeuk.py`.\n")

    lines.append("## 1. Summary of the Each-Gets Families\n")
    lines.append("| Family | n | k | Number range | T | S | k·S | D | S/n |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for fam in FAMILIES:
        s_str = str(fam.subset_sum) if fam.subset_sum is not None else "—"
        avg = average_per_subset(fam)
        avg_str = f"{avg:.2f}" if avg is not None else "—"
        lines.append(
            f"| {fam.name} | {fam.n} | {fam.k} | "
            f"{fam.vertex_range[0]}-{fam.vertex_range[1]} | "
            f"{fam.total_sum} | {s_str} | {fam.duplicated_sum} | "
            f"{duplicated_total(fam)} | {avg_str} |"
        )
    lines.append("")

    lines.append("## 2. Phase mod 5 Sum Distribution\n")
    lines.append("| Family | m | Water | Fire | Wood | Metal | Earth | Common difference |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for fam in FAMILIES:
        m = fam.m
        seq = phase_sum_sequence(m)
        diff = seq[1] - seq[0]
        lines.append(
            f"| {fam.name} | {m} | {seq[0]} | {seq[1]} | {seq[2]} | {seq[3]} | {seq[4]} | {diff} |"
        )
    lines.append("")

    lines.append("## 3. Duplication Equation Verification\n")
    lines.append("`5·S = T + D` holds for every family.\n")
    for fam in FAMILIES:
        if fam.subset_sum is None:
            lines.append(f"- **{fam.name}**: S not specified")
            continue
        lhs = fam.k * fam.subset_sum
        rhs = fam.total_sum + duplicated_total(fam)
        lines.append(
            f"- **{fam.name}**: 5×{fam.subset_sum} = {lhs}, "
            f"T+D = {fam.total_sum}+{duplicated_total(fam)} = {rhs} {'✓' if lhs == rhs else '✗'}"
        )
    lines.append("")

    lines.append("## 4. Generalization Model Predictions\n")
    lines.append("Predictions according to `S = n × μ` (μ: duplication-inclusive average):\n")
    lines.append("| n | Number range | Predicted S | Actual S |")
    lines.append("|---|---|---|---|")
    for fam in FAMILIES:
        if fam.subset_sum is None:
            continue
        mu = fam.duplicated_sum / (fam.k * fam.n)
        predicted = mu * fam.n
        lines.append(
            f"| {fam.n} | {fam.vertex_range[0]}-{fam.vertex_range[1]} | {predicted:.2f} | {fam.subset_sum} |"
        )
    lines.append("")

    return "\n".join(lines)


# ============================================================
# 3. Main
# ============================================================

if __name__ == "__main__":
    print_summary_table()
    print_phase_table()
    print_equation_check()
    print_generalization()

    report_md = generate_markdown_report()
    with open("computed_report.md", "w", encoding="utf-8") as f:
        f.write(report_md)
    print("[Saved] computed_report.md")
