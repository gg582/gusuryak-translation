#!/usr/bin/env python3
"""Analyze and verify the Nakseo Gugudo arrangement."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Cluster:
    label: str
    center: int
    values: tuple[int, ...]


CLUSTERS: tuple[tuple[Cluster, ...], ...] = (
    (
        Cluster("upper-left", 8, (17, 35, 56, 26, 65, 46, 42, 74)),
        Cluster("upper-center", 1, (10, 28, 63, 19, 72, 54, 41, 81)),
        Cluster("upper-right", 6, (15, 33, 58, 24, 67, 47, 43, 76)),
    ),
    (
        Cluster("middle-left", 3, (12, 30, 61, 21, 70, 53, 40, 79)),
        Cluster("middle-center", 5, (14, 32, 59, 23, 68, 52, 39, 77)),
        Cluster("middle-right", 7, (16, 34, 57, 25, 66, 51, 38, 75)),
    ),
    (
        Cluster("lower-left", 4, (13, 31, 60, 22, 69, 48, 44, 78)),
        Cluster("lower-center", 9, (18, 36, 55, 27, 64, 50, 37, 73)),
        Cluster("lower-right", 2, (11, 29, 62, 20, 71, 49, 45, 80)),
    ),
)

MAGIC_SUM = 369
COMPLEMENT_SUM = 91
DIAGRAM_CORRECTION_PAIRS = {
    8: (46, 42),
    1: (54, 41),
    6: (47, 43),
    3: (53, 40),
    5: (52, 39),
    7: (51, 38),
    4: (48, 44),
    9: (50, 37),
    2: (49, 45),
}


def flatten_clusters() -> list[Cluster]:
    return [cluster for row in CLUSTERS for cluster in row]


def find_pair_partition(values: tuple[int, ...], center: int) -> list[tuple[int, int, int]]:
    """Find three 91-complement pairs and one center-correction pair."""
    correction_pair = DIAGRAM_CORRECTION_PAIRS[center]
    correction_set = frozenset(correction_pair)
    if not correction_set.issubset(values):
        raise ValueError(f"Correction pair {correction_pair} is not in {values}")

    remaining_after_correction = tuple(x for x in values if x not in correction_set)
    target_sums = [COMPLEMENT_SUM, COMPLEMENT_SUM, COMPLEMENT_SUM]

    def search(remaining: tuple[int, ...], chosen: list[tuple[int, int, int]]):
        if not remaining:
            if sorted(pair_sum for _, _, pair_sum in chosen) == target_sums:
                return chosen
            return None

        first = remaining[0]
        for other in remaining[1:]:
            pair_sum = first + other
            if pair_sum not in target_sums:
                continue
            rest = tuple(x for x in remaining if x not in (first, other))
            result = search(rest, chosen + [(first, other, pair_sum)])
            if result is not None:
                return result
        return None

    result = search(remaining_after_correction, [])
    if result is None:
        raise ValueError(f"No valid pair partition for center {center}: {values}")
    return result + [(correction_pair[0], correction_pair[1], sum(correction_pair))]


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
        ring_sum = sum(cluster.values)
        total = cluster.center + ring_sum
        assert total == MAGIC_SUM, (cluster.center, ring_sum, total)


def markdown_report() -> str:
    lines = [
        "| position | center | correction pair | correction sum | ring sum | total |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for cluster in flatten_clusters():
        find_pair_partition(cluster.values, cluster.center)
        correction_values = DIAGRAM_CORRECTION_PAIRS[cluster.center]
        correction = (correction_values[0], correction_values[1], sum(correction_values))
        ring_sum = sum(cluster.values)
        lines.append(
            f"| {cluster.label} | {cluster.center} | "
            f"{correction[0]} + {correction[1]} | {correction[2]} | "
            f"{ring_sum} | {cluster.center + ring_sum} |"
        )
    return "\n".join(lines)


def main() -> None:
    verify_loshu_center()
    verify_number_range()
    verify_cluster_sums()

    print("Nakseo Gugudo verification passed.")
    print()
    print(f"Magic sum: {MAGIC_SUM}")
    print(f"Complement-pair sum: {COMPLEMENT_SUM}")
    print()
    print(markdown_report())
    print()

    for cluster in flatten_clusters():
        partition = sorted(find_pair_partition(cluster.values, cluster.center), key=lambda p: p[2])
        pair_text = ", ".join(f"{a}+{b}={pair_sum}" for a, b, pair_sum in partition)
        print(f"center {cluster.center}: {pair_text}")


if __name__ == "__main__":
    main()
