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
    return {
        "compound_non_equivariant_conditions_hold": aggregates_hold,
        "lo_shu_family_conditions_hold": loshu_family_conditions,
        "antipodal_complement_forced_without_equivariance": pairs_hold,
        "equivariance_forces_antipodal_complement": equivariant_witness,
    }


if __name__ == "__main__":
    print(audit())
