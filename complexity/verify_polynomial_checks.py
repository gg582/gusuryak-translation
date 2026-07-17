#!/usr/bin/env python3
"""Run the repository's direct verification checks and scaling measurements.

This script does not claim that timing proves a complexity class.  The P claims
come from the explicit scans in the check functions below; timings are included
only as reproducible empirical evidence that the implementations follow those
scans as input size grows.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path


def read_matrices(path: Path, width: int | None = None) -> list[list[list[int]]]:
    matrices: list[list[list[int]]] = []
    current: list[list[int]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        values = [int(value) for value in re.findall(r"(?<!\d)\d+(?!\d)", line)]
        if values and (width is None or len(values) == width):
            current.append(values)
        elif current and (width is None or len(values) != width):
            matrices.append(current)
            current = []
    if current:
        matrices.append(current)
    return matrices


def check_normal_magic(matrix: list[list[int]], order: int, magic_sum: int) -> bool:
    """O(order^2): coverage, rows, columns, and the two main diagonals."""
    if len(matrix) != order or any(len(row) != order for row in matrix):
        return False
    if sorted(value for row in matrix for value in row) != list(range(1, order * order + 1)):
        return False
    if any(sum(row) != magic_sum for row in matrix):
        return False
    if any(sum(matrix[row][col] for row in range(order)) != magic_sum for col in range(order)):
        return False
    return (
        sum(matrix[index][index] for index in range(order)) == magic_sum
        and sum(matrix[index][order - 1 - index] for index in range(order)) == magic_sum
    )


def check_normal_set(matrix: list[list[int]], order: int) -> bool:
    return (
        len(matrix) == order
        and all(len(row) == order for row in matrix)
        and sorted(value for row in matrix for value in row) == list(range(1, order * order + 1))
    )


def check_groups(groups: list[list[int]], target: int, values: list[int]) -> bool:
    """O(number of memberships): check coverage, duplicate use, and group sums."""
    flattened = [value for group in groups for value in group]
    return (
        sorted(flattened) == sorted(values)
        and all(sum(group) == target for group in groups)
    )


def check_source_coverage(values: list[int], upper: int) -> bool:
    """O(n log n) with sorting, or O(n) with a bounded boolean table."""
    return sorted(values) == list(range(1, upper + 1))


def benchmark_direct_check() -> list[dict[str, float]]:
    results: list[dict[str, float]] = []
    for order in (8, 16, 32, 64, 96):
        matrix = [list(range(row * order + 1, (row + 1) * order + 1)) for row in range(order)]
        started = time.perf_counter()
        repetitions = max(1, 20000 // order)
        for _ in range(repetitions):
            check_normal_magic(matrix, order, order * (order * order + 1) // 2)
        elapsed = time.perf_counter() - started
        results.append({"order": order, "cells": order * order, "seconds": elapsed})
    return results


def corrected_results(root: Path) -> list[dict[str, object]]:
    results = []
    for language in ("korean", "english"):
        base = root / language / "03-magic-squares"
        for path in sorted(base.glob("0[3-6]-*/corrected.md")):
            matrices = read_matrices(path, width=10)
            ok = len(matrices) == 1 and check_normal_magic(matrices[0], 10, 505)
            results.append({"file": str(path.relative_to(root)), "normal_magic_10x10": ok})
    return results


def source_square_results(root: Path) -> list[dict[str, object]]:
    results = []
    for language in ("korean", "english"):
        path = root / language / "03-magic-squares" / "square.md"
        six = read_matrices(path, width=6)
        nine = read_matrices(path, width=9)
        ten = read_matrices(path, width=10)
        results.append({
            "file": str(path.relative_to(root)),
            "yukyukdo_6x6_magic": len(six) == 2 and all(check_normal_magic(m, 6, 111) for m in six),
            "gusudo_9x9_magic": len(nine) == 2 and all(check_normal_magic(m, 9, 369) for m in nine),
            "baekja_10x10_normal_set": [check_normal_set(m, 10) for m in ten],
        })
    return results


def run_hexgrid_tests(root: Path) -> list[dict[str, object]]:
    results = []
    for language in ("english", "korean"):
        path = root / language / "06-nakseo-yukgodo" / "tests" / "test_hexgrid.py"
        completed = subprocess.run([sys.executable, str(path)], cwd=root, text=True, capture_output=True)
        results.append({
            "file": str(path.relative_to(root)),
            "returncode": completed.returncode,
            "output": (completed.stdout + completed.stderr).strip(),
        })
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    report = {
        "scope": "direct verification only; timings are empirical and do not prove P",
        "source_square_checks": source_square_results(root),
        "corrected_10x10": corrected_results(root),
        "hexgrid_tests": run_hexgrid_tests(root),
        "direct_check_benchmark": benchmark_direct_check(),
        "check_complexities": {
            "check_normal_magic": "O(n^2) scan plus bounded-value coverage check",
            "check_groups": "O(memberships) after input groups are supplied",
            "check_source_coverage": "O(n log n) using sorting",
        },
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if all(item["normal_magic_10x10"] for item in report["corrected_10x10"]) and all(item["returncode"] == 0 for item in report["hexgrid_tests"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
