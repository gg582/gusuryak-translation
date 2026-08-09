#!/usr/bin/env python3
"""대척보수 감사 반례가 재현되는지 검사한다."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from yukgodo.antipodal_audit import audit  # noqa: E402


def main() -> None:
    report = audit()
    assert report["verdict"] == "not_derived"
    assert report["preserved"]["value_set_1_to_270"]
    assert report["antipodal"]["before_all_pairs_sum_271"]
    assert report["antipodal"]["after_pair_absolute_deviation"] > 0
    assert report["antipodal"]["after_pairs_summing_271"] < report["antipodal"]["number_of_pairs"]
    assert all(6097 <= value <= 6098 for value in report["also_satisfies_solver_balance_ranges"]["wedge_sums"])
    assert all(1219 <= value <= 1220 for value in report["also_satisfies_solver_balance_ranges"]["ray_sums"])
    print("대척보수 비도출 반례 테스트 통과")


if __name__ == "__main__":
    main()
