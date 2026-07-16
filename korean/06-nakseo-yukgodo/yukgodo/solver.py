"""洛書六觚圖 배치 탐색 엔진.

탐색 공간:
    270칸을 135개의 대점 슬롯(점대칭 쌍)으로 묶고, 각 슬롯에 보수쌍
    (i, 271-i) 중 하나를 배정하며 방향(어느 쪽에 큰 수를 놓을지)을 정한다.
    이 표현은 다음을 구조적으로 정확히 만족시킨다:

        - 대점쌍 합 271                 (虛一·共積二百七十의 보수 구조)
        - 고리 k 합 = 813k              (通加洛書數六倍의 고리별 배분)
        - 축(中觚) 합 = 2439            (十九爲中觚數也)

    남은 목표(변 합 1355 균등, 섹터·광선 반칸 균형)만 탐색 목적 함수로 둔다.

방법:
    1. 건설적 시드(나선 순서 배정)와 난수 시드에서 출발
    2. simulated annealing (flip / pair-swap / swap+flip 이동)
    3. 탐욕적 마무리(greedy polish)
    4. 다중 재시작 후 최적해 선택
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field

from .hexgrid import PAIR_SUM, HexGrid
from .properties import (
    PENALTY_FLOOR,
    RAY_TARGET,
    SIDE_TARGET,
    WEDGE_TARGET,
)

N_SLOTS = 135


@dataclass
class SolveResult:
    values: dict[tuple[int, int], int]
    penalty: float
    restart_penalties: list[float] = field(default_factory=list)
    iterations: int = 0


class _State:
    """슬롯 단위 상태와 구조 합계의 증분 갱신."""

    def __init__(self, grid: HexGrid) -> None:
        self.grid = grid
        self.cell_index = {c: i for i, c in enumerate(grid.filled)}
        self.slots = [
            (self.cell_index[a], self.cell_index[b]) for a, b in grid.slots
        ]
        # 셀 → 구조 소속: (변 목록, 섹터, 광선 or -1)
        self.side_mem: list[tuple[int, ...]] = []
        self.wedge_mem: list[int] = []
        self.ray_mem: list[int] = []
        for c in grid.filled:
            self.side_mem.append(tuple(grid.sides_of.get(c, ())))
            self.wedge_mem.append(grid.wedge_of[c])
            self.ray_mem.append(grid.ray_of.get(c, -1))
        self.val = [0] * len(grid.filled)
        self.side_sum = [0] * 6
        self.wedge_sum = [0] * 6
        self.ray_sum = [0] * 6

    def set_slot(self, s: int, small: int, flip: bool) -> None:
        ca, cb = self.slots[s]
        large = PAIR_SUM - small
        a, b = (large, small) if flip else (small, large)
        self.val[ca] = a
        self.val[cb] = b
        for arr, mem in (
            (self.side_sum, self.side_mem),
            (self.wedge_sum, self.wedge_mem),
            (self.ray_sum, self.ray_mem),
        ):
            for ci, v in ((ca, a), (cb, b)):
                if arr is self.side_sum:
                    for m in mem[ci]:
                        arr[m] += v
                elif arr is self.ray_sum:
                    if mem[ci] >= 0:
                        arr[mem[ci]] += v
                else:
                    arr[mem[ci]] += v

    def penalty(self) -> float:
        p = 0.0
        for x in self.side_sum:
            p += abs(x - SIDE_TARGET)
        for x in self.wedge_sum:
            p += abs(x - WEDGE_TARGET)
        for x in self.ray_sum:
            p += abs(x - RAY_TARGET)
        return p

    def _apply_delta(self, ci: int, d: int) -> None:
        for m in self.side_mem[ci]:
            self.side_sum[m] += d
        self.wedge_sum[self.wedge_mem[ci]] += d
        r = self.ray_mem[ci]
        if r >= 0:
            self.ray_sum[r] += d

    def do_flip(self, s: int) -> None:
        ca, cb = self.slots[s]
        d = self.val[cb] - self.val[ca]
        self._apply_delta(ca, d)
        self._apply_delta(cb, -d)
        self.val[ca], self.val[cb] = self.val[cb], self.val[ca]

    def do_swap(self, s1: int, s2: int, flip_s2: bool = False) -> None:
        """두 슬롯의 보수쌍을 교환. flip_s2이면 한쪽 방향도 뒤집는다."""
        a1, b1 = self.slots[s1]
        a2, b2 = self.slots[s2]
        va1, vb1, va2, vb2 = self.val[a1], self.val[b1], self.val[a2], self.val[b2]
        na1, nb1 = (vb2, va2) if flip_s2 else (va2, vb2)
        na2, nb2 = (vb1, va1) if flip_s2 else (va1, vb1)
        self._apply_delta(a1, na1 - va1)
        self._apply_delta(b1, nb1 - vb1)
        self._apply_delta(a2, na2 - va2)
        self._apply_delta(b2, nb2 - vb2)
        self.val[a1], self.val[b1] = na1, nb1
        self.val[a2], self.val[b2] = na2, nb2

    def recompute_sums(self) -> None:
        """val 배열로부터 구조 합계를 전부 다시 계산한다."""
        self.side_sum = [0] * 6
        self.wedge_sum = [0] * 6
        self.ray_sum = [0] * 6
        for ci, v in enumerate(self.val):
            self._apply_delta(ci, v)

    def to_values(self) -> dict[tuple[int, int], int]:
        return {c: self.val[i] for c, i in self.cell_index.items()}


def _seed_spiral(state: _State) -> None:
    """건설적 시드: 외주에서 안쪽으로 나선 순회하며 보수쌍을 순서대로 배정."""
    grid = state.grid
    slot_of: dict[tuple[int, int], int] = {}
    for s, (a, b) in enumerate(grid.slots):
        slot_of[a] = s
        slot_of[b] = s
    seen: set[tuple[int, int]] = set()
    order: list[int] = []
    for k in range(grid.radius, 0, -1):
        for c in grid.ring_walk[k]:
            if c in seen:
                continue
            seen.add(c)
            seen.add((-c[0], -c[1]))
            order.append(slot_of[c])
    for s, slot_s in enumerate(order):
        state.set_slot(slot_s, s + 1, flip=(s % 2 == 1))


def _seed_random(state: _State, rng: random.Random) -> None:
    pairs = list(range(1, N_SLOTS + 1))
    rng.shuffle(pairs)
    for s in range(N_SLOTS):
        state.set_slot(s, pairs[s], flip=rng.random() < 0.5)


def _anneal(state: _State, rng: random.Random, iterations: int,
            t0: float = 40.0, t1: float = 0.05) -> float:
    n = len(state.slots)
    cur = state.penalty()
    best = cur
    best_snapshot = list(state.val)
    ratio = math.log(t1 / t0)
    for it in range(iterations):
        if cur <= PENALTY_FLOOR:
            break
        t = t0 * math.exp(ratio * it / iterations)
        move = rng.random()
        if move < 0.4:
            s = rng.randrange(n)
            state.do_flip(s)
            new = state.penalty()
            if new <= cur or rng.random() < math.exp(-(new - cur) / t):
                cur = new
            else:
                state.do_flip(s)  # 되돌리기
        else:
            s1 = rng.randrange(n)
            s2 = rng.randrange(n)
            if s1 == s2:
                continue
            flip = move >= 0.7
            state.do_swap(s1, s2, flip)
            new = state.penalty()
            if new <= cur or rng.random() < math.exp(-(new - cur) / t):
                cur = new
            else:
                state.do_swap(s1, s2, flip)  # 되돌리기 (동일 연산의 역연산)
        if cur < best:
            best = cur
            best_snapshot = list(state.val)
    state.val[:] = best_snapshot
    state.recompute_sums()
    return best


def _polish(state: _State, rng: random.Random, max_rounds: int = 40) -> float:
    """개선이 없을 때까지 flip / swap 탐욕 탐색."""
    n = len(state.slots)
    cur = state.penalty()
    for _ in range(max_rounds):
        improved = False
        order = list(range(n))
        rng.shuffle(order)
        for s in order:
            state.do_flip(s)
            new = state.penalty()
            if new < cur:
                cur = new
                improved = True
            else:
                state.do_flip(s)
        for _ in range(4 * n):
            s1 = rng.randrange(n)
            s2 = rng.randrange(n)
            if s1 == s2:
                continue
            state.do_swap(s1, s2)
            new = state.penalty()
            if new < cur:
                cur = new
                improved = True
            else:
                state.do_swap(s1, s2)
        if cur <= PENALTY_FLOOR or not improved:
            break
    return cur


def solve(grid: HexGrid, iterations: int = 150_000, restarts: int = 8,
          seed: int = 1715) -> SolveResult:
    """다중 재시작 담금질로 최적 배치를 찾는다."""
    rng = random.Random(seed)
    best_values: dict[tuple[int, int], int] | None = None
    best_pen = math.inf
    restart_pens: list[float] = []
    for r in range(restarts):
        state = _State(grid)
        if r == 0:
            _seed_spiral(state)
        else:
            _seed_random(state, rng)
        pen = _anneal(state, rng, iterations)
        pen = _polish(state, rng)
        restart_pens.append(pen)
        if pen < best_pen:
            best_pen = pen
            best_values = state.to_values()
        if best_pen <= PENALTY_FLOOR:
            break
    assert best_values is not None
    return SolveResult(
        values=best_values,
        penalty=best_pen,
        restart_penalties=restart_pens,
        iterations=iterations,
    )
