#!/usr/bin/env python3
"""복합 조건의 대척보수 비도출/등변성 도출 경계를 검사한다."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from yukgodo.equivariance_threshold_audit import audit  # noqa: E402


def main() -> None:
    result = audit()
    assert result["without_equivariance"]["lo_shu_family_conditions"]
    assert result["without_equivariance"]["all_non_antipodal_aggregate_constraints"]
    assert not result["without_equivariance"]["antipodal_complement_forced"]
    assert result["with_equivariance"]["antipodal_complement_forced"]
    assert result["local_transposition_countermodels"] == 514
    print("등변성 임계 감사 테스트 통과")


if __name__ == "__main__":
    main()
