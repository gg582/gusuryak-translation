"""구수략 도안에서 확인 가능한 위치-값 등변성의 범위를 감사한다.

여기서 등변성은 위치 대합 tau와 값 보수 kappa_S에 대해
v(tau(p)) = S - v(p)를 뜻한다. 모든 도안에 동일한 전면 좌표 전사가
있는 것은 아니므로, 이 감사는 확인 가능한 배정 단위만 등급별로 세며
전체 책의 발생 빈도에 대한 임의의 백분율은 주장하지 않는다.
"""

from __future__ import annotations

from collections import Counter

from .nakseo_family_audit import family_evidence


# 02 九子各得 중궁: 3x3 중심대칭 4쌍과 중심 고정점.
GUJA_CENTER = [(15, 31), (41, 5), (6, 40), (16, 30), (23, 23)]

# 07 重卦用八圖: 두 가로 진의 행 내 좌우 대칭쌍.
PALJIN_HORIZONTAL = [
    (14, 51), (19, 46), (35, 30), (62, 3),
    (7, 58), (26, 39), (42, 23), (55, 10),
]

# 07 侯策用九圖: 9개 formation의 위치쌍. 상수합이 아닌 사례도 함께
# 기록해야 보수쌍의 사용 범위를 과장하지 않는다.
HUCHAEK = [
    (5, 68), (33, 45), (41, 31), (67, 6),
    (3, 70), (34, 40), (39, 33), (64, 4),
    (73, 1), (36, 38), (37, 35), (71, 2),
    (18, 55), (19, 56), (54, 20), (11, 62),
    (16, 57), (21, 51), (52, 22), (58, 15),
    (14, 59), (23, 49), (50, 24), (60, 13),
    (11, 62), (26, 48), (42, 25), (61, 12),
    (9, 64), (28, 46), (45, 27), (63, 10),
    (7, 66), (30, 44), (43, 29), (65, 8),
]

# 05 範數用五圖: 십자 고리의 네 대향쌍. 전면 상수합의 음성 대조다.
BEOMSU_ANTIPODAL = [(3, 6), (2, 9), (7, 4), (8, 1)]


def _constant_sum(pairs: list[tuple[int, int]]) -> int | None:
    totals = {left + right for left, right in pairs}
    return totals.pop() if len(totals) == 1 else None


def audit() -> dict[str, object]:
    family = family_evidence()
    control = family["lo_shu_control_arrays"]
    guja_total = _constant_sum(GUJA_CENTER)
    paljin_total = _constant_sum(PALJIN_HORIZONTAL)
    huchaek_distribution = dict(sorted(Counter(left + right for left, right in HUCHAEK).items()))
    beomsu_distribution = dict(sorted(Counter(left + right for left, right in BEOMSU_ANTIPODAL).items()))

    assert control["all_dihedrally_lo_shu"]
    assert guja_total == 46 and GUJA_CENTER[-1] == (23, 23)
    assert paljin_total == 65
    assert huchaek_distribution == {67: 1, 68: 1, 72: 7, 73: 16, 74: 9, 75: 1, 78: 1}
    assert beomsu_distribution == {9: 2, 11: 2}

    return {
        "definition": "v(tau(p)) = S - v(p)",
        "exact_positional_instances": {
            "three_Lo_Shu_control_arrays": {
                "uses": 3,
                "pair_sum": 10,
                "fixed_center": 5,
                "status": "exact at the shared 3x3 control layer",
            },
            "guja_gakdeuk_center_palace": {
                "pairs": len(GUJA_CENTER),
                "pair_sum": guja_total,
                "fixed_center": 23,
                "status": "exact local 3x3 positional equivariance",
            },
            "paljin_horizontal_formations": {
                "pairs": len(PALJIN_HORIZONTAL),
                "pair_sum": paljin_total,
                "status": "exact local left-right equivariance",
            },
        },
        "complement_construction_without_full_positional_equivariance": {
            "nakseo_gugudo": {
                "pairs": 36,
                "pair_sum": 91,
                "status": "explicit construction pairs; full expanded cells fail positional equivariance",
            },
            "paljin_remaining_formations": {
                "pair_sum": 65,
                "status": "complement pairs are distributed or split across formations",
            },
        },
        "negative_or_partial_control": {
            "huchaek_yonggudo": {
                "pair_sum_distribution": huchaek_distribution,
                "dominant_sum": 73,
                "dominant_pairs": 16,
                "total_pairs": len(HUCHAEK),
                "status": "not a global equivariant placement",
            },
            "beomsu_yongodo": {
                "pair_sum_distribution": beomsu_distribution,
                "status": "cross-shaped diagram with no constant antipodal sum",
            },
            "nakseo_expanded_cells": family["equivariance_scope"]["expanded_cells"],
        },
        "yukgodo_status": (
            "The source confirms the geometric count calculation; 271-antipodal "
            "equivariance remains a reconstruction condition supported by this inventory, "
            "not a directly transcribed Yukgodo placement instruction."
        ),
        "scope": (
            "This is an auditable inventory of stored, coordinate-resolved examples, not a "
            "denominator for every Gusuryak diagram or a frequency percentage."
        ),
    }


if __name__ == "__main__":
    print(audit())
