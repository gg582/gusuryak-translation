"""낙서 계열 도안과 육고도의 공통 3×3 규칙을 재검산한다.

이 감사는 원배치 복원이 아니라, 저장된 다른 낙서 도안의 데이터에서 확인 가능한
공통 제어 배열과 보수 연산만을 추린다.
"""

from __future__ import annotations

from itertools import product
from pathlib import Path
import runpy


KOREAN = Path(__file__).resolve().parents[2]
FAMILY = KOREAN / "01-saodo-family"

LO_SHU = ((8, 1, 6), (3, 5, 7), (4, 9, 2))
HANJA_DIGIT = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}


def _dihedral_forms(square: tuple[tuple[int, ...], ...]) -> set[tuple[tuple[int, ...], ...]]:
    """정사각 배열의 회전·반사 동치류를 돌려준다."""
    forms = set()
    current = square
    for _ in range(4):
        forms.add(current)
        forms.add(tuple(tuple(reversed(row)) for row in current))
        current = tuple(tuple(current[2 - col][row] for col in range(3)) for row in range(3))
    return forms


def is_lo_shu(square: tuple[tuple[int, ...], ...]) -> bool:
    return square in _dihedral_forms(LO_SHU)


def _load(path: Path) -> dict:
    return runpy.run_path(str(path))


def family_evidence() -> dict[str, object]:
    gugudo = _load(FAMILY / "낙서구구도" / "visualize.py")
    ogudo = _load(FAMILY / "낙서오구도" / "nakseo_ogudo.py")
    chilgudo = _load(FAMILY / "낙서칠구도" / "visualize_basic.py")

    gugudo_square = tuple(
        tuple(HANJA_DIGIT[cluster.center_label] for cluster in row)
        for row in gugudo["CLUSTERS"]
    )
    ogudo_values = ogudo["VALUES"]
    ogudo_square = tuple(
        tuple(ogudo_values[(x, y)] for x in (1, 3, 5))
        for y in (2, 1, 0)
    )
    chilgudo_groups = chilgudo["groups"]
    chilgudo_square = tuple(
        tuple(next(group["center"] for group in chilgudo_groups if group["pos"] == (x, y))
        for x in (1, 2, 3))
        for y in (3, 2, 1)
    )

    # 기본 낙서의 중심대칭 네 쌍은 모두 10이고, 중심 5만 고정점이다.
    antipodal_sums = [
        LO_SHU[row][col] + LO_SHU[2 - row][2 - col]
        for row, col in product(range(3), repeat=2)
        if (row, col) != (1, 1)
    ]
    assert all(total == 10 for total in antipodal_sums)
    assert LO_SHU[1][1] == 5

    tier_pairs = [(k, 10 - k, 6 * k + 6 * (10 - k)) for k in range(1, 5)]
    assert all(total == 60 for _, _, total in tier_pairs)

    # 낙서구구도의 문서화된 외곽 보수쌍: 10..81, 합 91.
    outer_pairs = [(value, 91 - value) for value in range(10, 46)]
    assert all(left + right == 91 for left, right in outer_pairs)

    result = {
        "lo_shu_control_arrays": {
            "nakseo_gugudo": gugudo_square,
            "nakseo_ogudo": ogudo_square,
            "nakseo_chilgudo": chilgudo_square,
            "all_dihedrally_lo_shu": all(is_lo_shu(square) for square in (gugudo_square, ogudo_square, chilgudo_square)),
        },
        "base_rule": {
            "opposite_pair_sum": 10,
            "center_fixed_value": 5,
            "opposite_sums": antipodal_sums,
        },
        "documented_extension": {
            "diagram": "낙서구구도",
            "outer_value_range": [10, 81],
            "constant_complement_sum": 91,
            "pair_count": len(outer_pairs),
        },
        "yukgodo_tier_lift": {
            "rule": "k ↔ 10-k  maps to  6k ↔ 6(10-k)",
            "pairs": tier_pairs,
            "constant_sum": 60,
            "textual_calculation": "54 + 6 = 60",
        },
        "boundary": (
            "이 결과는 낙서 계열이 보수쌍을 실제 구성 규칙으로 사용하고 육고도가 "
            "그 낙서 보수를 6배 고리로 올린다는 점을 보인다. 다만 이것만으로 "
            "육고도 각 대척 위치의 셀 값 합 271을 논리적으로 함의하지는 않는다."
        ),
    }
    return result


def main() -> None:
    evidence = family_evidence()
    print(evidence)


if __name__ == "__main__":
    main()
