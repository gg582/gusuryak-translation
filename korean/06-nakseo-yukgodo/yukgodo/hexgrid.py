"""落書六觚圖의 육각 격자(六觚 도안) 기하 모델.

《漢書·律曆志》 "二百七十一枚而成六觚, 爲一握" 및 蘇林 注
"其表六九五十四, 算中積凡得二百七十一枚"에 대응하는 구조:

    - 중심 1칸 + 고리 k (k=1..9, 각 6k칸) = 271칸
    - 한 변 10칸, 외주(가장 바깥 고리) 54칸
    - 중심은 虛一로 비우고 270칸에 수를 배치

좌표는 axial coordinates (q, r)을 사용하고, 세 번째 cube 좌표는
s = -q - r 로 복원한다. 셀의 고리 번호는 max(|q|, |r|, |q+r|).
"""

from __future__ import annotations

import math

RADIUS = 9                                # 중심에서 꼭짓점까지의 고리 수
SIDE = RADIUS + 1                         # 한 변의 점 수 = 10
N_CELLS = 3 * RADIUS * (RADIUS + 1) + 1   # 271 (六觚一握)
N_FILLED = N_CELLS - 1                    # 270 (虛一則二百七十數)
PAIR_SUM = N_CELLS                        # 보수쌍의 합 = 271
TOTAL_SUM = N_FILLED * PAIR_SUM // 2      # 1+...+270 = 36585
OUTER_RING = RADIUS                       # 외주 고리 번호 = 9 (周五十四數)

# 6개 방향 단위 벡터 (axial, 반시계 순서)
DIRECTIONS: list[tuple[int, int]] = [
    (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)
]

Cell = tuple[int, int]
CENTER: Cell = (0, 0)


def add(a: Cell, b: Cell) -> Cell:
    return (a[0] + b[0], a[1] + b[1])


def scale(d: Cell, k: int) -> Cell:
    return (d[0] * k, d[1] * k)


def ring_of(cell: Cell) -> int:
    """셀의 고리 번호 (0=중심, 9=외주)."""
    q, r = cell
    return max(abs(q), abs(r), abs(q + r))


def antipode(cell: Cell) -> Cell:
    """중심 기준 점대칭 셀 (대점)."""
    return (-cell[0], -cell[1])


def cube(cell: Cell) -> tuple[int, int, int]:
    q, r = cell
    return (q, r, -q - r)


def to_pixel(cell: Cell, size: float = 1.0) -> tuple[float, float]:
    """pointy-top 육각 격자의 화면 좌표 (y는 위가 +)."""
    q, r = cell
    x = size * math.sqrt(3.0) * (q + r / 2.0)
    y = size * 1.5 * r
    return (x, y)


class HexGrid:
    """반지름 9의 육각 격자와 그 부분 구조들.

    Attributes:
        cells:      전체 271칸 (중심 포함)
        filled:     虛一을 제외한 270칸
        rings:      rings[k] = 고리 k의 셀 목록 (순서 무관)
        ring_walk:  ring_walk[k] = 고리 k의 순회 순서 (꼭짓점에서 시작)
        rays:       rays[i] = 중심→꼭짓점 i로 뻗는 광선 9칸 (i=0..5)
        sides:      sides[j] = 외주의 변 j, 꼭짓점 포함 10칸 (j=0..5)
        wedges:     wedges[i] = 觚(섹터) i, 45칸씩 270칸을 분할 (i=0..5)
        axes:       axes[a] = 중심을 지나는 축 a, 19칸 (a=0..2, 中觔)
        slots:      대점 슬롯 135개, 각 (cell, antipode(cell)) 쌍
    """

    def __init__(self, radius: int = RADIUS) -> None:
        self.radius = radius
        self.cells: list[Cell] = [
            (q, r)
            for q in range(-radius, radius + 1)
            for r in range(-radius, radius + 1)
            if max(abs(q), abs(r), abs(q + r)) <= radius
        ]
        self.cell_set = frozenset(self.cells)
        self.filled: list[Cell] = [c for c in self.cells if c != CENTER]

        self.rings: list[list[Cell]] = [[] for _ in range(radius + 1)]
        for c in self.cells:
            self.rings[ring_of(c)].append(c)

        self.ring_walk: list[list[Cell]] = [self._walk_ring(k) for k in range(radius + 1)]

        # 광선: 중심에서 꼭짓점 방향 i로 뻗는 9개 셀
        self.rays: list[list[Cell]] = [
            [scale(DIRECTIONS[i], k) for k in range(1, radius + 1)]
            for i in range(6)
        ]
        self.sides: list[list[Cell]] = [self._side(j) for j in range(6)]
        self.wedges: list[list[Cell]] = [self._wedge(i) for i in range(6)]
        self.axes: list[list[Cell]] = [
            [scale(DIRECTIONS[a], t) for t in range(-radius, radius + 1)]
            for a in range(3)
        ]

        # 셀 → 구조 역참조
        self.wedge_of: dict[Cell, int] = {}
        for i, w in enumerate(self.wedges):
            for c in w:
                self.wedge_of[c] = i
        self.ray_of: dict[Cell, int] = {}
        for i, ry in enumerate(self.rays):
            for c in ry:
                self.ray_of[c] = i
        self.sides_of: dict[Cell, list[int]] = {}
        for j, s in enumerate(self.sides):
            for c in s:
                self.sides_of.setdefault(c, []).append(j)

        # 대점 슬롯: 270칸을 135개의 점대칭 쌍으로 묶음
        seen: set[Cell] = set()
        self.slots: list[tuple[Cell, Cell]] = []
        for c in self.filled:
            if c in seen:
                continue
            a = antipode(c)
            seen.add(c)
            seen.add(a)
            self.slots.append((c, a))

    def _walk_ring(self, k: int) -> list[Cell]:
        """고리 k를 꼭짓점(방향 4)에서 시작해 방향 0→…→5 순으로 순회."""
        if k == 0:
            return [CENTER]
        walk: list[Cell] = []
        pos = scale(DIRECTIONS[4], k)
        for j in range(6):
            for _ in range(k):
                walk.append(pos)
                pos = add(pos, DIRECTIONS[j])
        return walk

    def _side(self, j: int) -> list[Cell]:
        """외주 변 j: 꼭짓점 C_j에서 다음 꼭짓점까지 꼭짓점 포함 10칸."""
        corner = scale(DIRECTIONS[(j + 4) % 6], self.radius)
        return [add(corner, scale(DIRECTIONS[j], t)) for t in range(self.radius + 1)]

    def _wedge(self, i: int) -> list[Cell]:
        """觚(섹터) i: 광선 i를 시계쪽 경계로 포함하는 60° 쐐기, 45칸.

        고리 k에서는 k칸 (광선 i 위 1칸 + 남쪽 날개 k-1칸)을 차지하고,
        6개 섹터는 270칸을 겹침 없이 분할한다. 대점은 섹터 (i+3)%6으로 이동.
        """
        cells: list[Cell] = []
        for k in range(1, self.radius + 1):
            base = scale(DIRECTIONS[i], k)
            step = DIRECTIONS[(i + 2) % 6]
            for t in range(k):
                cells.append(add(base, scale(step, t)))
        return cells

    def rows(self, a: int) -> dict[int, list[Cell]]:
        """축 a에 수직인 직선 행들: cube 좌표 a 성분이 m인 셀들 (m=-9..9).

        m=0 인 행이 中觔(19칸)이고, |m|가 커질수록 19-|m| 칸이 된다.
        """
        rows: dict[int, list[Cell]] = {m: [] for m in range(-self.radius, self.radius + 1)}
        for c in self.cells:
            rows[cube(c)[a]].append(c)
        return rows

    def perimeter_walk(self) -> list[Cell]:
        """외주 54칸의 순회 순서 (校計周五十四數)."""
        return self.ring_walk[self.radius]

    def corners(self) -> list[Cell]:
        """외주 꼭짓점 6개 (방향 0..5 순)."""
        return [scale(DIRECTIONS[i], self.radius) for i in range(6)]
