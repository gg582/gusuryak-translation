"""배치의 마법 성질 측정 및 채점.

배치(values: 셀 → 1..270의 수)에 대해 주석과 대조 가능한 성질들을 측정한다.

목표치 산출 근거 (대척 보수쌍 가설: 점대칭 두 칸의 합 = 271):

    - 고리 k 합    = 3k × 271 = 813k        (고리 k는 3k개의 대척쌍)
    - 변 합         = 5 × 271 = 1355         (마주 보는 변끼리 2710으로 자동 균형)
    - 섹터(觚) 합  ≈ 12195 / 2 = 6097.5     (45칸 = 홀수라 정확한 균등은 불가,
                                               최적은 6097/6098 교대)
    - 광선 합      ≈ 2439 / 2 = 1219.5      (마주 보는 광선 쌍 = 9 × 271)
    - 축(中觚) 합  = 9 × 271 = 2439         (대척쌍 가설 하에서 자동 성립)

penalty 는 목표와의 절대 편차 총합이며, 이론적 하한은 6.0이다
(섹터 3.0 + 광선 3.0; 홀수 칸 구조 때문에 0이 될 수 없다).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .hexgrid import (
    N_FILLED,
    OUTER_RING,
    PAIR_SUM,
    TOTAL_SUM,
    HexGrid,
    antipode,
    ring_of,
)

SIDE_TARGET = 5 * PAIR_SUM               # 1355
WEDGE_TARGET = 45 * PAIR_SUM / 2         # 6097.5
RAY_TARGET = 9 * PAIR_SUM / 2            # 1219.5
AXIS_TARGET = 9 * PAIR_SUM               # 2439
PENALTY_FLOOR = 6.0                      # 섹터·광선의 반칸 오차 한계


def ring_target(k: int) -> int:
    """고리 k의 목표 합 = 813k (通加洛書數六倍: 합계는 6×45×271/2 의 고리별 배분)."""
    return 3 * k * PAIR_SUM


@dataclass
class PropertyReport:
    """한 배치에 대한 성질 측정 결과."""

    ring_sums: list[int]                 # 고리 0..9 (0은 중심=0)
    side_sums: list[int]                 # 변 6개
    wedge_sums: list[int]                # 섹터 6개
    ray_sums: list[int]                  # 광선 6개
    axis_sums: list[int]                 # 축 3개 (中觚 포함)
    pair_devs: list[int]                 # 대척쌍 합 - 271, 슬롯별
    corner_values: list[int]             # 외주 꼭짓점 값 6개
    total: int                           # 전체 합 (검증용: 36585)
    penalty: float = 0.0
    parts: dict[str, float] = field(default_factory=dict)


def measure(values: dict, grid: HexGrid) -> PropertyReport:
    """배치의 모든 성질을 측정한다."""
    ring_sums = [0] * (grid.radius + 1)
    for c, v in values.items():
        ring_sums[ring_of(c)] += v

    side_sums = [sum(values[c] for c in side) for side in grid.sides]
    wedge_sums = [sum(values[c] for c in wedge) for wedge in grid.wedges]
    ray_sums = [sum(values[c] for c in ray) for ray in grid.rays]
    axis_sums = [
        sum(values.get(c, 0) for c in axis) for axis in grid.axes
    ]
    pair_devs = [
        values[a] + values[b] - PAIR_SUM for a, b in grid.slots
    ]
    corner_values = [values[c] for c in grid.corners()]
    total = sum(values.values())

    parts = {
        "sides": sum(abs(s - SIDE_TARGET) for s in side_sums),
        "wedges": sum(abs(w - WEDGE_TARGET) for w in wedge_sums),
        "rays": sum(abs(r - RAY_TARGET) for r in ray_sums),
        "pairs": sum(abs(d) for d in pair_devs),
        "rings": sum(
            abs(ring_sums[k] - ring_target(k)) for k in range(1, grid.radius + 1)
        ),
        "axes": sum(abs(s - AXIS_TARGET) for s in axis_sums),
    }
    penalty = sum(parts.values())
    return PropertyReport(
        ring_sums=ring_sums,
        side_sums=side_sums,
        wedge_sums=wedge_sums,
        ray_sums=ray_sums,
        axis_sums=axis_sums,
        pair_devs=pair_devs,
        corner_values=corner_values,
        total=total,
        penalty=penalty,
        parts=parts,
    )


def validate(values: dict, grid: HexGrid) -> list[str]:
    """배치가 기본 조건을 만족하는지 검증하고 위반 목록을 돌려준다."""
    errors: list[str] = []
    if len(values) != N_FILLED:
        errors.append(f"채워진 칸 수 {len(values)} != {N_FILLED}")
    extra = [c for c in values if c not in grid.cell_set or c == (0, 0)]
    if extra:
        errors.append(f"격자 밖/중심 칸 {len(extra)}개 존재")
    vals = sorted(values.values())
    if vals != list(range(1, N_FILLED + 1)):
        errors.append("값이 1..270을 한 번씩 사용하지 않음")
    if sum(vals) != TOTAL_SUM:
        errors.append(f"총합 {sum(vals)} != {TOTAL_SUM}")
    outer = [c for c in values if ring_of(c) == OUTER_RING]
    if len(outer) != 54:
        errors.append(f"외주 칸 수 {len(outer)} != 54")
    return errors
