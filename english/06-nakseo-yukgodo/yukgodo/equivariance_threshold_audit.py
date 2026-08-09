"""Test the threshold at which compound conditions force antipodal complements."""

from pathlib import Path

from .antipodal_audit import find_countermodel, load_witness
from .hexgrid import HexGrid, antipode
from .properties import measure


LO_SHU = ((4, 9, 2), (3, 5, 7), (8, 1, 6))


def audit() -> dict:
    grid = HexGrid()
    witness = load_witness(Path("output/solution.json"), grid)
    countermodel, _, _ = find_countermodel(witness, grid)
    report = measure(countermodel, grid)
    loshu_family_conditions = (
        all(LO_SHU[row][col] + LO_SHU[2 - row][2 - col] == 10 for row in range(3) for col in range(3))
        and LO_SHU[1][1] == 5
        and all(value + (91 - value) == 91 for value in range(10, 46))
        and all(
            {countermodel[cell] for cell in grid.rings[k]}
            == {271 - countermodel[cell] for cell in grid.rings[k]}
            for k in range(1, 10)
        )
        and len(HexGrid(radius=1).slots) == 3
    )
    aggregates_hold = (
        report.ring_sums[1:] == [813 * k for k in range(1, 10)]
        and report.axis_sums == [2439, 2439, 2439]
        and report.side_sums == [1355] * 6
        and all(6097 <= total <= 6098 for total in report.wedge_sums)
        and all(1219 <= total <= 1220 for total in report.ray_sums)
    )
    pairs_hold = all(
        countermodel[cell] + countermodel[antipode(cell)] == 271
        for cell in grid.filled
    )
    equivariant_witness = all(
        witness[cell] + witness[antipode(cell)] == 271
        for cell in grid.filled
    )
    assert loshu_family_conditions and aggregates_hold and not pairs_hold and equivariant_witness

    def profile(cell: tuple[int, int]) -> tuple[object, ...]:
        return (
            max(abs(cell[0]), abs(cell[1]), abs(cell[0] + cell[1])),
            tuple(i for i, axis in enumerate(grid.axes) if cell in axis),
            tuple(grid.sides_of.get(cell, ())),
        )

    # Exhaustively test local swaps only. The two locations have equal ring,
    # axis, and side membership, so the primary aggregate totals are retained.
    witness_report = measure(witness, grid)
    local_countermodels = 0
    for i, left in enumerate(grid.filled):
        for right in grid.filled[i + 1:]:
            if profile(left) != profile(right):
                continue
            candidate = witness.copy()
            candidate[left], candidate[right] = candidate[right], candidate[left]
            candidate_report = measure(candidate, grid)
            if (
                candidate_report.ring_sums == witness_report.ring_sums
                and candidate_report.axis_sums == witness_report.axis_sums
                and candidate_report.side_sums == witness_report.side_sums
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
    assert local_countermodels == 504
    return {
        "compound_non_equivariant_conditions_hold": aggregates_hold,
        "lo_shu_family_conditions_hold": loshu_family_conditions,
        "antipodal_complement_forced_without_equivariance": pairs_hold,
        "equivariance_forces_antipodal_complement": equivariant_witness,
        "local_transposition_countermodels": local_countermodels,
    }


if __name__ == "__main__":
    print(audit())
