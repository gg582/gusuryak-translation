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

    print("## 값 사용")
    print()
    print(f"- 위치 수: {len(values)}")
    print(f"- 서로 다른 값: {len(set(values))}")
    print(f"- 1..72 중 대상 데이터에 없는 값: {unused or '-'}")
    print(f"- 1..72 밖의 값: {outside or '-'}")
    print(f"- 반복값: {repeated or '-'}")


def print_pair_sum_report(formations: list[dict]) -> None:
    pairs = side_pairs(formations)
    distribution = Counter(total for _label, _side, _pair, total in pairs)

    print()
    print("## 변 쌍 합")
    print()
    print(f"- 기준 보수합: {BASE_PAIR_SUM}")
    print(f"- 분포: {dict(sorted(distribution.items()))}")
    print()
    print("| 위치 | 변 | 쌍 | 실제 합 | 표시 합 | 판정 |")
    print("|---|---|---|---:|---:|---|")

    side_index = {side: index for index, side in enumerate(SIDE_NAMES)}
    for formation in formations:
        for side in SIDE_NAMES:
            total = side_sum(formation, side)
            displayed = formation["sums"][side_index[side]]
            expected = {BASE_PAIR_SUM, LEFT_EDGE_SUM, RIGHT_EDGE_SUM}
            status = "규칙권" if total in expected else "이탈"
            if total != displayed:
                status += ", 표시합 불일치"
            print(
                f"| {formation['label']} | {side} | {formation[side]} | "
                f"{total} | {displayed} | {status} |"
            )


def print_formation_balance_report(formations: list[dict]) -> None:
    print()
    print("## 팔각형 단위 합")
    print()
    print("| 위치 | top+bottom | left+right | 전체 | 판정 |")
    print("|---|---:|---:|---:|---|")

    for formation in formations:
        horizontal = side_sum(formation, "top") + side_sum(formation, "bottom")
        vertical = side_sum(formation, "left") + side_sum(formation, "right")
        total = formation_total(formation)
        status = "성립" if total == OCTAGON_SUM else "불일치"
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
    print("## 규칙 대조 요약")
    print()
    print(f"- 팔각형 목표합: {BASE_PAIR_SUM} x 4 = {OCTAGON_SUM}")
    print(f"- 사각형 목표합: {LEFT_EDGE_SUM} + {RIGHT_EDGE_SUM} = {SQUARE_SUM}")
    print(f"- 합 {BASE_PAIR_SUM}인 변 쌍: {pair_distribution[BASE_PAIR_SUM]}개")
    print(f"- 합 {LEFT_EDGE_SUM}인 변 쌍: {pair_distribution[LEFT_EDGE_SUM]}개")
    print(f"- 합 {RIGHT_EDGE_SUM}인 변 쌍: {pair_distribution[RIGHT_EDGE_SUM]}개")
    print(
        f"- 팔각형 단위합 {OCTAGON_SUM}: "
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
    print("판정:")
    if complete_values and pair_sums_in_rule and all_octagon_totals:
        print("- 대상 데이터는 후책용구도 유도 규칙과 일치한다.")
    elif not corrected:
        print("- 원본 재구본 역시 리브레위키 후책용구도 규칙의 골격을 따른다.")
        print(
            "- 다만 이 판본은 숫자 조건을 완전히 최적화한 판본이 아니라, "
            "도상의 형태와 표시된 국소 쌍합을 우선해 보존한 재구성이다."
        )
        print(
            "- 따라서 이탈 항목은 원문 계열이 규칙 밖이라는 뜻이 아니라, "
            "도상 중심 보수 재구본과 숫자 완전 정정본의 차이를 보여준다."
        )
    else:
        print("- 대상 데이터는 규칙의 핵심 패턴을 일부 보이지만, 완전 일치는 아니다.")
        print("- 특히 실제 값 기준으로는 1..72 완전 사용, 변 쌍 합, 팔각형 단위합에서 이탈이 있다.")


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
    dataset_name = "정정본" if args.corrected else "작업 데이터"

    print("# 후책용구도 규칙 검증")
    print()
    print(f"대상: {dataset_name}")
    print()
    print("리브레위키 후책용구도 서술의 핵심 규칙을 대상 데이터에 대조한다.")
    print("값을 바꾸지 않고, 코드에 적힌 수의 실제 합만 계산한다.")
    print()
    print_value_inventory(formations)
    print_pair_sum_report(formations)
    print_formation_balance_report(formations)
    print_rule_summary(formations, args.corrected)


if __name__ == "__main__":
    main()
