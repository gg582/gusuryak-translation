"""대척보수 이외의 육고도 배치 조건을 같은 척도로 비교하는 실험.

모든 모델은 1..270을 한 번씩 쓰고 중심을 빈 칸으로 둔다. 여기서 ``정합``은
원문 직접성의 점수가 아니라, (a) 해당 모델의 자체 조건, (b) 원문에서 읽히는
고리·외주 기하, (c) 기존의 변·섹터·광선 균형을 각각 분리해 측정하는 뜻이다.
"""

from __future__ import annotations

import json
import math
import random
from pathlib import Path

from .antipodal_audit import find_countermodel, load_witness
from .hexgrid import Cell, HexGrid, PAIR_SUM, antipode, ring_of
from .properties import RAY_TARGET, SIDE_TARGET, WEDGE_TARGET, measure, validate
from .solver import solve_with_pairing


def rotate60(c: Cell) -> Cell:
    """축좌표에서 반시계 60도 회전. 세 번이면 대척점이다."""
    q, r = c
    return (-r, q + r)


def rotation_orbits(grid: HexGrid) -> list[tuple[Cell, ...]]:
    seen: set[Cell] = set()
    result: list[tuple[Cell, ...]] = []
    for start in grid.filled:
        if start in seen:
            continue
        orbit = []
        current = start
        for _ in range(6):
            orbit.append(current)
            seen.add(current)
            current = rotate60(current)
        assert current == start and len(set(orbit)) == 6
        result.append(tuple(orbit))
    assert len(result) == 45
    return result


def ring_adjacent_pairs(grid: HexGrid) -> list[tuple[Cell, Cell]]:
    """각 고리 순회에서 이웃한 두 칸을 짝짓는, 대척이 아닌 고리 내부 보수쌍."""
    slots = []
    for k in range(1, grid.radius + 1):
        walk = grid.ring_walk[k]
        slots.extend((walk[i], walk[i + 1]) for i in range(0, len(walk), 2))
    assert len(slots) == 135
    assert all(antipode(a) != b for a, b in slots)
    return slots


def global_nonantipodal_pairs(grid: HexGrid) -> list[tuple[Cell, Cell]]:
    """고리를 넘나드는, 대척점이 아닌 완전 보수 매칭 하나를 결정론적으로 만든다."""
    rng = random.Random(271)
    for _ in range(100):
        cells = list(grid.filled)
        rng.shuffle(cells)
        slots = [(cells[i], cells[i + 1]) for i in range(0, len(cells), 2)]
        if all(antipode(a) != b for a, b in slots):
            # 무작위 순서는 서로 다른 고리 사이의 짝도 포함한다.
            assert any(ring_of(a) != ring_of(b) for a, b in slots)
            return slots
    raise RuntimeError("비대척 완전 매칭을 만들지 못함")


def _pair_sums(values: dict[Cell, int], slots: list[tuple[Cell, Cell]]) -> bool:
    return all(values[a] + values[b] == PAIR_SUM for a, b in slots)


def _groups() -> list[tuple[int, int, int, int, int, int]]:
    """1..270을 합 813인 45개 6원소 묶음으로 분할한다."""
    result = []
    for a in range(1, 46):
        b, c = a + 45, a + 90
        # 반대 위치(세 칸 뒤)가 보수쌍이 되지 않는 순서.
        result.append((a, b, c, PAIR_SUM - b, PAIR_SUM - c, PAIR_SUM - a))
    assert sorted(v for group in result for v in group) == list(range(1, 271))
    assert all(sum(group) == 813 for group in result)
    return result


def _balance_score(values: dict[Cell, int], grid: HexGrid) -> float:
    report = measure(values, grid)
    return (
        sum(abs(x - SIDE_TARGET) for x in report.side_sums)
        + sum(abs(x - WEDGE_TARGET) for x in report.wedge_sums)
        + sum(abs(x - RAY_TARGET) for x in report.ray_sums)
        + sum(abs(x - 2439) for x in report.axis_sums)
    )


def _orbit_values(
    orbits: list[tuple[Cell, ...]], groups: list[tuple[int, ...]],
    assignment: list[int], phases: list[int], permutations: list[tuple[int, ...]] | None = None,
) -> dict[Cell, int]:
    values: dict[Cell, int] = {}
    for oi, orbit in enumerate(orbits):
        sequence = groups[assignment[oi]]
        if permutations is not None:
            sequence = tuple(sequence[j] for j in permutations[oi])
        phase = phases[oi]
        for j, cell in enumerate(orbit):
            values[cell] = sequence[(j + phase) % 6]
    return values


def _solve_orbits(grid: HexGrid, fixed_transform: bool, iterations: int, seed: int) -> dict[Cell, int]:
    """6회전 궤도합 813을 보존한 채 균형을 낮춘다.

    fixed_transform=True이면 한 45-원소 값 변환의 6회 적용(위상·궤도 배정만 변경)을
    유지한다. False이면 각 궤도 안의 여섯 값도 자유롭게 섞을 수 있다.
    """
    rng = random.Random(seed)
    orbits, groups = rotation_orbits(grid), _groups()
    assignment = list(range(45))
    rng.shuffle(assignment)
    phases = [rng.randrange(6) for _ in orbits]
    permutations = None if fixed_transform else [tuple(rng.sample(range(6), 6)) for _ in orbits]
    values = _orbit_values(orbits, groups, assignment, phases, permutations)
    current = _balance_score(values, grid)
    best = values.copy()
    best_score = current
    for step in range(iterations):
        temperature = 35.0 * math.exp(math.log(0.03 / 35.0) * step / iterations)
        old_assignment, old_phases = assignment[:], phases[:]
        old_permutations = None if permutations is None else permutations[:]
        if rng.random() < 0.45:
            i, j = rng.sample(range(45), 2)
            assignment[i], assignment[j] = assignment[j], assignment[i]
        elif fixed_transform or rng.random() < 0.55:
            phases[rng.randrange(45)] = rng.randrange(6)
        else:
            i = rng.randrange(45)
            permutations[i] = tuple(rng.sample(range(6), 6))
        candidate = _orbit_values(orbits, groups, assignment, phases, permutations)
        new = _balance_score(candidate, grid)
        if new <= current or rng.random() < math.exp(-(new - current) / max(temperature, 1e-9)):
            values, current = candidate, new
            if new < best_score:
                best, best_score = candidate.copy(), new
        else:
            assignment, phases, permutations = old_assignment, old_phases, old_permutations
    return best


def _summary(name: str, values: dict[Cell, int], grid: HexGrid, condition: dict[str, bool], note: str) -> dict[str, object]:
    report = measure(values, grid)
    return {
        "name": name,
        "valid_values": not validate(values, grid),
        "condition": condition,
        "balance_penalty_side_wedge_ray": (
            report.parts["sides"] + report.parts["wedges"] + report.parts["rays"]
        ),
        "axis_deviation": report.parts["axes"],
        "ring_deviation_from_813k": report.parts["rings"],
        "antipodal_absolute_deviation": report.parts["pairs"],
        "antipodal_pairs_summing_271": sum(d == 0 for d in report.pair_devs),
        "note": note,
    }


def run(iterations: int = 45_000, seed: int = 1715) -> dict[str, object]:
    grid = HexGrid()
    witness = load_witness(Path("output/solution.json"), grid)
    countermodel, _, _ = find_countermodel(witness, grid)

    ring_slots = ring_adjacent_pairs(grid)
    global_slots = global_nonantipodal_pairs(grid)
    ring_pairs = solve_with_pairing(grid, ring_slots, iterations=iterations, restarts=4, seed=seed).values
    nonant_pairs = solve_with_pairing(grid, global_slots, iterations=iterations, restarts=4, seed=seed + 1).values
    orbit_free = _solve_orbits(grid, fixed_transform=False, iterations=iterations, seed=seed + 2)
    sector_generated = _solve_orbits(grid, fixed_transform=True, iterations=iterations, seed=seed + 3)

    orbits = rotation_orbits(grid)
    expected_orbits = lambda values: all(sum(values[c] for c in orbit) == 813 for orbit in orbits)
    expected_rings = lambda values: all(sum(values[c] for c in grid.rings[k]) == 813 * k for k in range(1, 10))

    models = [
        _summary("antipodal_complement", witness, grid,
                 {"antipodal_pairs": True, "ring_sums": expected_rings(witness)},
                 "문헌 내적 대척보수 복원원리의 기준 증인해."),
        _summary("aggregate_only_countermodel", countermodel, grid,
                 {"aggregate_balance": True, "ring_sums": expected_rings(countermodel), "antipodal_pairs": False},
                 "동일 고리·축·변 프로필의 교환으로 대척만 깨뜨린 집계 조건 증인."),
        _summary("ring_internal_complement_pairs", ring_pairs, grid,
                 {"ring_internal_complements": _pair_sums(ring_pairs, ring_slots), "no_slot_is_antipodal": True, "ring_sums": expected_rings(ring_pairs)},
                 "각 고리의 이웃 위치쌍에 271 보수값을 배치."),
        _summary("global_nonantipodal_complement_pairs", nonant_pairs, grid,
                 {"nonantipodal_complements": _pair_sums(nonant_pairs, global_slots), "no_slot_is_antipodal": True},
                 "고리를 넘나드는 임의의 비대척 보수 매칭."),
        _summary("rotation_orbit_sum_813", orbit_free, grid,
                 {"all_rotation_orbits_sum_813": expected_orbits(orbit_free), "ring_sums": expected_rings(orbit_free)},
                 "각 6회전 궤도합 813만 고정; 궤도 내부의 값 순서는 자유."),
        _summary("one_sector_sixfold_value_transform", sector_generated, grid,
                 {"all_rotation_orbits_sum_813": expected_orbits(sector_generated), "ring_sums": expected_rings(sector_generated), "fixed_six_cycle_transform": True},
                 "45칸 한 섹터를 고정 6-순환 값 변환으로 여섯 번 생성."),
    ]
    return {
        "common_conditions": ["values_1_to_270", "central_vacancy", "hexagon_271", "nine_rings"],
        "models": models,
        "cheonsu_yong_o_precedent": {
            "location": "육고도 직전 재인쇄된 天水用五圖 계열의 저장소 전사",
            "transcription": [
                "去中宮十五",
                "外合得二百一十六",
                "無宮各得五十四爲六九之數",
                "二十二子作二十五子用同前",
            ],
            "arithmetic": {"216_equals_4_times_54": 216 == 4 * 54, "54_equals_6_times_9": 54 == 6 * 9},
            "supports": {
                "central_removal_and_equal_region_aggregates": "strong",
                "six_by_nine_outer_count": "strong",
                "nine_ring_LoShu_control_with_separate_placement": "moderate_to_strong",
                "antipodal_cell_complements": "not_direct",
                "sixfold_rotation_value_transform": "not_direct",
            },
            "boundary": (
                "이 재인쇄는 去中宮과 54=六九, 그리고 외부 영역의 등집계를 직접 보여 준다. "
                "그러나 54의 네 영역 분배를 육고도의 6개 섹터나 셀별 대척보수로 바로 동일시하지 않는다."
            ),
        },
        "interpretive_boundary": (
            "이 실험은 수학적 양립성과 균형 비용을 비교한다. 가장 낮은 비용이 원문 의도를 "
            "자동으로 증명하지 않으며, 직접 원문·병행문·낙서 계열 선례의 증거 등급은 별도로 평가한다."
        ),
    }


def main() -> None:
    print(json.dumps(run(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
