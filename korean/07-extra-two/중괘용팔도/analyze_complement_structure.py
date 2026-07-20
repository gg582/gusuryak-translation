#!/usr/bin/env python3
"""
Analyze complement-pair structure in the eight-formation diagram.

The method follows the Nakseo Gugudo description on LibreWiki: establish a
baseline complement sum, then look for local redistribution of complement
halves between neighboring formations.
"""

from __future__ import annotations

from dataclasses import dataclass


COMPLEMENT_SUM = 65


@dataclass(frozen=True)
class Formation:
    key: str
    label: str
    values: tuple[int, ...]

    @property
    def total(self) -> int:
        return sum(self.values)

    @property
    def value_set(self) -> set[int]:
        return set(self.values)


FORMATIONS = [
    Formation("TL", "1행 1열", (40, 20, 57, 9, 8, 56, 29, 41)),
    Formation("T", "1행 2열", (14, 51, 19, 46, 35, 30, 62, 3)),
    Formation("TR", "1행 3열", (45, 24, 52, 4, 13, 61, 25, 36)),
    Formation("L", "2행 1열", (48, 32, 49, 16, 17, 33, 1, 64)),
    Formation("R", "2행 3열", (37, 21, 60, 12, 5, 53, 28, 44)),
    Formation("BL", "3행 1열", (38, 22, 59, 11, 6, 54, 27, 43)),
    Formation("B", "3행 2열", (7, 58, 26, 39, 42, 23, 55, 10)),
    Formation("BR", "3행 3열", (47, 31, 50, 2, 15, 63, 18, 34)),
]


def complement(value: int) -> int:
    return COMPLEMENT_SUM - value


def internal_pairs(formation: Formation) -> list[tuple[int, int]]:
    remaining = set(formation.values)
    pairs: list[tuple[int, int]] = []

    for value in sorted(formation.values):
        other = complement(value)
        if value in remaining and other in remaining and value != other:
            pairs.append((min(value, other), max(value, other)))
            remaining.remove(value)
            remaining.remove(other)

    return pairs


def unpaired_values(formation: Formation) -> list[int]:
    paired = {value for pair in internal_pairs(formation) for value in pair}
    return sorted(formation.value_set - paired)


def split_pairs(left: Formation, right: Formation) -> list[tuple[int, int]]:
    pairs: list[tuple[int, int]] = []
    left_values = left.value_set
    right_values = right.value_set

    for value in sorted(left_values):
        other = complement(value)
        if other in right_values:
            pairs.append((value, other))

    return pairs


def format_pairs(pairs: list[tuple[int, int]]) -> str:
    if not pairs:
        return "-"
    return ", ".join(f"({a},{b})" for a, b in pairs)


def print_formation_report() -> None:
    target_sum = COMPLEMENT_SUM * 4

    print("# 팔진도 보수쌍 구조 분석")
    print()
    print(f"기준 보수합: {COMPLEMENT_SUM}")
    print(f"진형 기준합: {COMPLEMENT_SUM} x 4 = {target_sum}")
    print()
    print("## 진형별 내부 보수쌍")
    print()
    print("| 위치 | 합 | 내부 보수쌍 | 내부에서 닫히지 않는 수 |")
    print("|---|---:|---|---|")

    for formation in FORMATIONS:
        pairs = internal_pairs(formation)
        loose = unpaired_values(formation)
        loose_text = ", ".join(map(str, loose)) if loose else "-"
        print(
            f"| {formation.label} | {formation.total} | "
            f"{format_pairs(pairs)} | {loose_text} |"
        )


def print_split_report() -> None:
    print()
    print("## 진형 간 분할 보수쌍")
    print()
    print("| 진형 A | 진형 B | A-B 사이에서 닫히는 보수쌍 |")
    print("|---|---|---|")

    for index, left in enumerate(FORMATIONS):
        for right in FORMATIONS[index + 1 :]:
            pairs = split_pairs(left, right)
            if pairs:
                print(f"| {left.label} | {right.label} | {format_pairs(pairs)} |")


def print_top_corner_balance() -> None:
    top_left = FORMATIONS[0]
    top_right = FORMATIONS[2]
    left_loose = unpaired_values(top_left)
    right_loose = unpaired_values(top_right)

    print()
    print("## 위쪽 모서리형 균형")
    print()
    print(f"{top_left.label} 미폐합 수: {', '.join(map(str, left_loose))}")
    print(f"{top_right.label} 미폐합 수: {', '.join(map(str, right_loose))}")
    print(
        "두 진형 사이의 분할 보수쌍: "
        f"{format_pairs(split_pairs(top_left, top_right))}"
    )
    print()
    print("합 분해:")
    print(f"- {top_left.label}: 내부쌍 {len(internal_pairs(top_left))}개 = 130, 미폐합 수 합 = {sum(left_loose)}")
    print(f"- {top_right.label}: 내부쌍 {len(internal_pairs(top_right))}개 = 130, 미폐합 수 합 = {sum(right_loose)}")


def main() -> None:
    print_formation_report()
    print_split_report()
    print_top_corner_balance()


if __name__ == "__main__":
    main()
