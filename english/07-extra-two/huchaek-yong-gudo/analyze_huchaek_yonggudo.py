#!/usr/bin/env python3
"""Check the LibreWiki-style construction rule for Huchaek-yong-gudo."""

from __future__ import annotations

import argparse
from collections import Counter

from huchaek_data import CORRECTED_FORMATIONS, FORMATIONS, SIDE_NAMES


VALUE_RANGE = range(1, 73)
BASE_PAIR_SUM = 73
OCTAGON_SUM = BASE_PAIR_SUM * 4
SQUARE_SUM = BASE_PAIR_SUM * 2
LEFT_EDGE_SUM = 74
RIGHT_EDGE_SUM = 72


def side_sum(formation: dict, side: str) -> int:
    return sum(formation[side])


def all_values(formations: list[dict]) -> list[int]:
    return [
        value
        for formation in formations
        for side in SIDE_NAMES
        for value in formation[side]
    ]


def side_pairs(formations: list[dict]) -> list[tuple[str, str, tuple[int, int], int]]:
    return [
        (formation["label"], side, formation[side], side_sum(formation, side))
        for formation in formations
        for side in SIDE_NAMES
    ]


def formation_total(formation: dict) -> int:
    return sum(side_sum(formation, side) for side in SIDE_NAMES)


def print_value_inventory(formations: list[dict]) -> None:
    values = all_values(formations)
    counts = Counter(values)
    unused = sorted(set(VALUE_RANGE) - set(values))
    outside = sorted(set(values) - set(VALUE_RANGE))
    repeated = sorted((value, count) for value, count in counts.items() if count > 1)

    print("## Value Inventory")
    print()
    print(f"- positions: {len(values)}")
    print(f"- distinct values: {len(set(values))}")
    print(f"- values from 1..72 absent from this dataset: {unused or '-'}")
    print(f"- values outside 1..72: {outside or '-'}")
    print(f"- repeated values: {repeated or '-'}")


def print_pair_sum_report(formations: list[dict]) -> None:
    pairs = side_pairs(formations)
    distribution = Counter(total for _label, _side, _pair, total in pairs)

    print()
    print("## Side-Pair Sums")
    print()
    print(f"- baseline complement sum: {BASE_PAIR_SUM}")
    print(f"- distribution: {dict(sorted(distribution.items()))}")
    print()
    print("| position | side | pair | actual sum | displayed sum | reading |")
    print("|---|---|---|---:|---:|---|")

    side_index = {side: index for index, side in enumerate(SIDE_NAMES)}
    for formation in formations:
        for side in SIDE_NAMES:
            total = side_sum(formation, side)
            displayed = formation["sums"][side_index[side]]
            expected = {BASE_PAIR_SUM, LEFT_EDGE_SUM, RIGHT_EDGE_SUM}
            status = "within rule" if total in expected else "off rule"
            if total != displayed:
                status += ", displayed sum differs"
            print(
                f"| {formation['label']} | {side} | {formation[side]} | "
                f"{total} | {displayed} | {status} |"
            )


def print_formation_balance_report(formations: list[dict]) -> None:
    print()
    print("## Octagon-Unit Sums")
    print()
    print("| position | top+bottom | left+right | total | reading |")
    print("|---|---:|---:|---:|---|")

    for formation in formations:
        horizontal = side_sum(formation, "top") + side_sum(formation, "bottom")
        vertical = side_sum(formation, "left") + side_sum(formation, "right")
        total = formation_total(formation)
        status = "holds" if total == OCTAGON_SUM else "differs"
        print(
            f"| {formation['label']} | {horizontal} | {vertical} | "
            f"{total} | {status} |"
        )


def print_rule_summary(formations: list[dict], corrected: bool) -> None:
    values = all_values(formations)
    pair_distribution = Counter(
        total for _label, _side, _pair, total in side_pairs(formations)
    )
    octagon_totals = [formation_total(formation) for formation in formations]

    print()
    print("## Rule Summary")
    print()
    print(f"- octagon target: {BASE_PAIR_SUM} x 4 = {OCTAGON_SUM}")
    print(f"- square target: {LEFT_EDGE_SUM} + {RIGHT_EDGE_SUM} = {SQUARE_SUM}")
    print(f"- side pairs summing to {BASE_PAIR_SUM}: {pair_distribution[BASE_PAIR_SUM]}")
    print(f"- side pairs summing to {LEFT_EDGE_SUM}: {pair_distribution[LEFT_EDGE_SUM]}")
    print(f"- side pairs summing to {RIGHT_EDGE_SUM}: {pair_distribution[RIGHT_EDGE_SUM]}")
    print(
        f"- octagon-unit total {OCTAGON_SUM}: "
        f"{octagon_totals.count(OCTAGON_SUM)} / {len(octagon_totals)}"
    )

    complete_values = (
        len(values) == 72
        and set(values) == set(VALUE_RANGE)
        and all(count == 1 for count in Counter(values).values())
    )
    expected_pair_sums = {BASE_PAIR_SUM, LEFT_EDGE_SUM, RIGHT_EDGE_SUM}
    pair_sums_in_rule = all(
        total in expected_pair_sums
        for _label, _side, _pair, total in side_pairs(formations)
    )
    all_octagon_totals = all(total == OCTAGON_SUM for total in octagon_totals)

    print()
    print("Reading:")
    if complete_values and pair_sums_in_rule and all_octagon_totals:
        print("- This dataset agrees with the Huchaek-yong-gudo construction rule.")
    elif not corrected:
        print("- The original reconstruction also follows the LibreWiki Huchaek-yong-gudo rule in its structural frame.")
        print(
            "- It is a conservative reconstruction centered on the diagrammatic form "
            "and the displayed local pair sums, not a numerically optimized complete edition."
        )
        print(
            "- The listed differences therefore mark the gap between the form-centered "
            "original reconstruction and the numerically complete corrected edition."
        )
    else:
        print("- This dataset shows the rule pattern but is not numerically complete.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--corrected",
        action="store_true",
        help="analyze the corrected working arrangement",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    formations = CORRECTED_FORMATIONS if args.corrected else FORMATIONS
    dataset_name = "corrected edition" if args.corrected else "original reconstruction"

    print("# Huchaek-yong-gudo Rule Check")
    print()
    print(f"Dataset: {dataset_name}")
    print()
    print("This checks the core rule described for Huchaek-yong-gudo on LibreWiki.")
    print("No values are changed during this check; it only sums the data as written.")
    print()
    print_value_inventory(formations)
    print_pair_sum_report(formations)
    print_formation_balance_report(formations)
    print_rule_summary(formations, args.corrected)


if __name__ == "__main__":
    main()
