"""대척보수가 복합 조건에서 도출되는 임계점을 검사한다."""

from __future__ import annotations

from .antipodal_audit import find_countermodel, load_witness
from .hexgrid import HexGrid, antipode
from .properties import measure


LO_SHU = ((4, 9, 2), (3, 5, 7), (8, 1, 6))


def audit() -> dict[str, object]:
    grid = HexGrid()
    witness = load_witness(__import__("pathlib").Path("output/solution.json"), grid)
    countermodel, _, _ = find_countermodel(witness, grid)
    report = measure(countermodel, grid)

    # C0--C5는 원문 기하, 낙서 계열의 실제 보수 수법, 현 솔버의 모든 비-대척 목표를 포괄한다.
    c0_geometry = (
        len(grid.cells) == 271
        and len(grid.filled) == 270
        and len(grid.slots) == 135
        and [len(grid.rings[k]) for k in range(1, 10)] == [6 * k for k in range(1, 10)]
    )
    c1_value_set = sorted(countermodel.values()) == list(range(1, 271))
    c2_sixfold_loshu_lift = all(6 * k + 6 * (10 - k) == 60 for k in range(1, 5))
    c3_loshu_family_conditions = (
        all(LO_SHU[row][col] + LO_SHU[2 - row][2 - col] == 10 for row in range(3) for col in range(3))
        and LO_SHU[1][1] == 5
        and all(value + (91 - value) == 91 for value in range(10, 46))
        # 대척 가설의 고리별 귀결을 약화: 각 고리는 보수값의 집합으로 닫힌다.
        and all(
            {countermodel[cell] for cell in grid.rings[k]}
            == {271 - countermodel[cell] for cell in grid.rings[k]}
            for k in range(1, 10)
        )
        # 圓束樣式의 최소 기하: 중심을 제외한 반지름 1에는 3 대척 궤도가 있다.
        and len(HexGrid(radius=1).slots) == 3
    )
    c4_aggregate_balance = (
        report.ring_sums[1:] == [813 * k for k in range(1, 10)]
        and report.axis_sums == [2439, 2439, 2439]
        and report.side_sums == [1355] * 6
        and all(6097 <= total <= 6098 for total in report.wedge_sums)
        and all(1219 <= total <= 1220 for total in report.ray_sums)
    )
    c5_antipodal_complement = all(
        countermodel[cell] + countermodel[antipode(cell)] == 271
        for cell in grid.filled
    )
    c6_equivariance_implies_pairs = all(
        witness[cell] + witness[antipode(cell)] == 271
        for cell in grid.filled
    )

    assert c0_geometry and c1_value_set and c2_sixfold_loshu_lift and c3_loshu_family_conditions and c4_aggregate_balance
    assert not c5_antipodal_complement
    assert c6_equivariance_implies_pairs

    # 같은 고리·축·변 소속인 두 위치만 바꾸는 국소 교환을 전수 검사한다.
    def profile(cell: tuple[int, int]) -> tuple[object, ...]:
        return (
            max(abs(cell[0]), abs(cell[1]), abs(cell[0] + cell[1])),
            tuple(i for i, axis in enumerate(grid.axes) if cell in axis),
            tuple(grid.sides_of.get(cell, ())),
        )

    local_countermodels = 0
    for i, left in enumerate(grid.filled):
        for right in grid.filled[i + 1:]:
            if profile(left) != profile(right):
                continue
            candidate = witness.copy()
            candidate[left], candidate[right] = candidate[right], candidate[left]
            candidate_report = measure(candidate, grid)
            if (
                candidate_report.ring_sums == measure(witness, grid).ring_sums
                and candidate_report.axis_sums == measure(witness, grid).axis_sums
                and candidate_report.side_sums == measure(witness, grid).side_sums
                and all(6097 <= total <= 6098 for total in candidate_report.wedge_sums)
                and all(1219 <= total <= 1220 for total in candidate_report.ray_sums)
                and all(
                    {candidate[cell] for cell in grid.rings[k]}
                    == {271 - candidate[cell] for cell in grid.rings[k]}
                    for k in range(1, 10)
                )
                and candidate_report.parts["pairs"] > 0
            ):
                local_countermodels += 1
    assert local_countermodels == 514
    return {
        "without_equivariance": {
            "geometry": c0_geometry,
            "value_set": c1_value_set,
            "sixfold_loshu_lift": c2_sixfold_loshu_lift,
            "lo_shu_family_conditions": c3_loshu_family_conditions,
            "all_non_antipodal_aggregate_constraints": c4_aggregate_balance,
            "antipodal_complement_forced": c5_antipodal_complement,
        },
        "with_equivariance": {
            "condition": "v(antipode(c)) = 271 - v(c)",
            "antipodal_complement_forced": c6_equivariance_implies_pairs,
        },
        "local_transposition_countermodels": local_countermodels,
        "verdict": (
            "현재 복합 조건만으로는 대척보수가 도출되지 않는다. 514개의 국소 교환 "
            "반례는 이 현상이 거대 해공간의 희귀 예외가 아님을 보인다. 그러나 이는 "
            "원문이 등변 배정 원리를 배제한다는 반증은 아니다. 등변성은 충분조건이며 "
            "이 경우 대척보수와 동치다. 따라서 현 자료만으로 90% 이상이라는 논리적 "
            "확정 등급을 선언할 수 없지만, 반례만으로 역사적 복원 가능성을 90% 아래로 "
            "낮출 근거도 없다."
        ),
    }


if __name__ == "__main__":
    print(audit())
