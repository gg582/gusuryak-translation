#!/usr/bin/env python3
"""중심 공백 7칸의 최소 대척 구조를 검사한다."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from yukgodo.minimal_pairing import report  # noqa: E402


def main() -> None:
    result = report()
    assert result["small_cells"] == 7
    assert result["small_center_removed"]
    assert result["small_antipodal_pairs"] == 3
    assert result["full_cells"] == 271
    assert result["full_center_removed"]
    assert result["full_antipodal_pairs"] == 135
    print("중심 공백 최소 대척 구조 테스트 통과")


if __name__ == "__main__":
    main()
