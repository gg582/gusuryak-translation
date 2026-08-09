#!/usr/bin/env python3
"""낙서 계열 공통 규칙의 데이터 대조를 검사한다."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from yukgodo.nakseo_family_audit import family_evidence  # noqa: E402


def main() -> None:
    evidence = family_evidence()
    assert evidence["lo_shu_control_arrays"]["all_dihedrally_lo_shu"]
    assert evidence["base_rule"]["opposite_pair_sum"] == 10
    assert evidence["base_rule"]["center_fixed_value"] == 5
    assert evidence["documented_extension"]["constant_complement_sum"] == 91
    assert evidence["yukgodo_tier_lift"]["constant_sum"] == 60
    assert all(
        not item["holds"]
        for item in evidence["equivariance_scope"]["expanded_cells"].values()
    )
    print("낙서 계열 공통 규칙 감사 테스트 통과")


if __name__ == "__main__":
    main()
