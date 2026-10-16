#!/usr/bin/env python3
"""Analyze and verify the Nakseo Gugudo arrangement."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Cluster:
    label: str
    center: int
    values: tuple[int, ...]


# Ring values are ordered clockwise from the upper-left circle.
# Transcribed from the source diagram and corrected back to the original
# values by reconstruct_milp.py (4 transcription errors: 四+47,
# 三 71->19, 七 3->31, 六 38->30).
CLUSTERS: tuple[tuple[Cluster, ...], ...] = (
    (
        Cluster("upper-left", 8, (16, 51, 56, 27, 64, 32, 40, 75)),
        Cluster("upper-center", 1, (69, 34, 77, 12, 53, 58, 45, 20)),
        Cluster("upper-right", 6, (38, 79, 14, 63, 46, 22, 71, 30)),
    ),
    (
        Cluster("middle-left", 3, (11, 76, 60, 36, 19, 68, 52, 44)),
        Cluster("middle-center", 5, (29, 24, 62, 37, 70, 81, 48, 13)),
        Cluster("middle-right", 7, (74, 26, 55, 31, 42, 50, 66, 18)),
    ),
    (
        Cluster("lower-left", 4, (15, 80, 61, 23, 28, 72, 39, 47)),
        Cluster("lower-center", 9, (49, 57, 17, 73, 41, 25, 65, 33)),
        Cluster("lower-right", 2, (54, 43, 67, 10, 59, 21, 78, 35)),
    ),
)

MAGIC_SUM = 369
MODULUS = 9


def flatten_clusters() -> list[Cluster]:
    return [cluster for row in CLUSTERS for cluster in row]


def verify_loshu_center() -> None:
    square = [[cluster.center for cluster in row] for row in CLUSTERS]
    line_sums: list[int] = []
    line_sums.extend(sum(row) for row in square)
    line_sums.extend(sum(square[row][col] for row in range(3)) for col in range(3))
    line_sums.append(sum(square[i][i] for i in range(3)))
    line_sums.append(sum(square[i][2 - i] for i in range(3)))
    assert all(total == 15 for total in line_sums), line_sums


def verify_number_range() -> None:
    used = [cluster.center for cluster in flatten_clusters()]
    for cluster in flatten_clusters():
        used.extend(cluster.values)
    assert sorted(used) == list(range(1, 82))


def verify_cluster_sums() -> None:
    for cluster in flatten_clusters():
        total = cluster.center + sum(cluster.values)
        assert total == MAGIC_SUM, (cluster.center, sum(cluster.values), total)


def verify_mod9_transversal() -> None:
    """Each ring holds exactly one representative of every residue
    class mod 9 other than its own center's class."""
    for cluster in flatten_clusters():
        residues = sorted(value % MODULUS for value in cluster.values)
        expected = sorted(r for r in range(MODULUS) if r != cluster.center % MODULUS)
        assert residues == expected, (cluster.label, residues, expected)


def verify_class_spread() -> None:
    """Each residue class r mod 9 is absent only from the palace whose
    center is r, and appears exactly once in every other ring."""
    for residue in range(MODULUS):
        owners = {
            cluster.center: [v for v in cluster.values if v % MODULUS == residue]
            for cluster in flatten_clusters()
        }
        for center, members in owners.items():
            if center == (residue if residue != 0 else 9):
                assert members == [], (residue, center, members)
            else:
                assert len(members) == 1, (residue, center, members)


def markdown_report() -> str:
    lines = [
        "| palace (center) | ring sum | total | missing mod 9 residue |",
        "|---|---:|---:|---|",
    ]
    for cluster in flatten_clusters():
        ring_sum = sum(cluster.values)
        missing = cluster.center % MODULUS
        lines.append(
            f"| {cluster.label} ({cluster.center}) | {ring_sum} | "
            f"{cluster.center + ring_sum} | {missing} |"
        )
    return "\n".join(lines)


def main() -> None:
    verify_loshu_center()
    verify_number_range()
    verify_cluster_sums()
    verify_mod9_transversal()
    verify_class_spread()

    print("Nakseo Gugudo verification passed.")
    print()
    print(f"Magic sum: {MAGIC_SUM} (= 9 x 41; each cluster is a full mod-9 transversal)")
    print()
    print(markdown_report())
    print()
    for cluster in flatten_clusters():
        residues = [value % MODULUS for value in cluster.values]
        print(f"center {cluster.center}: residues {residues}")


if __name__ == "__main__":
    main()
