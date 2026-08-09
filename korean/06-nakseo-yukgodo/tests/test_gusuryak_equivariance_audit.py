#!/usr/bin/env python3
"""구수략 전체 범위의 등변성 목록을 회귀 검사한다."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from yukgodo.gusuryak_equivariance_audit import audit  # noqa: E402


def main() -> None:
    result = audit()
    exact = result["exact_positional_instances"]
    assert exact["three_Lo_Shu_control_arrays"]["uses"] == 3
    assert exact["guja_gakdeuk_center_palace"]["pair_sum"] == 46
    assert exact["paljin_horizontal_formations"]["pair_sum"] == 65
    huchaek = result["negative_or_partial_control"]["huchaek_yonggudo"]
    assert huchaek["dominant_pairs"] == 16
    assert huchaek["total_pairs"] == 36
    assert result["negative_or_partial_control"]["beomsu_yongodo"]["pair_sum_distribution"] == {9: 2, 11: 2}
    print("구수략 등변성 범위 감사 테스트 통과")


if __name__ == "__main__":
    main()
