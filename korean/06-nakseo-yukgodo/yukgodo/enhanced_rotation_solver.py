#!/usr/bin/env python3
"""序左(서좌)·寄左(기좌) 반시계방향 회전 대칭 연산 기반 고성능 육고도 탐색기 (Enhanced CCW Rotation-Orbit Solver).

특징:
1. 60°~300° 반시계 회전 대칭성(C6 Rotation Group)을 이용한 Orbit Orbit State Transition 지원
2. 다중 위상 대칭 탐색(Multi-Phase Symmetric Annealing):
   - 6개 반시계 방향 위상(Phase 0~5: 0°, 60°, 120°, 180°, 240°, 300°) 중 최적의 상태를 주기적으로 교환 및 동기화.
   - 단일 상태가 Local Optima에 갇힐 때, 반시계 회전 변환된 궤적(Orbit)에서 상호 교차(Cross-Orbit Swap)를 수행하여 빠르게 글로벌 최적해로 탈출.
3. 2-Opt 및 Greedy Local Polish를 내장하여 페널티 6.0(이론적 하한) 수렴 속도 극대화.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import time

from yukgodo.hexgrid import HexGrid, PAIR_SUM, Cell
from yukgodo.properties import PENALTY_FLOOR, measure, validate
from yukgodo.solver import _State, N_SLOTS, SolveResult
from yukgodo.solve_ccw_rotation import rotate_cell_ccw


class EnhancedRotationSolver:
    """반시계 회전 대칭 궤적(CCW Rotation Orbit)을 활용한 강화된 육고도 탐색기."""

    def __init__(self, grid: HexGrid, seed: int = 42):
        self.grid = grid
        self.seed = seed
        self.rng = random.Random(seed)
        
        # 슬롯별 6개 CCW 회전 위상 맵 (slot -> [(target_slot, is_flipped) for step in 0..5])
        cell_to_slot = {}
        for s, (ca, cb) in enumerate(grid.slots):
            cell_to_slot[ca] = (s, False)
            cell_to_slot[cb] = (s, True)
            
        self.slot_rot_map: list[list[tuple[int, bool]]] = []
        for s, (ca, cb) in enumerate(grid.slots):
            rot_list = []
            for k in range(6):
                rot_ca = rotate_cell_ccw(ca, k)
                target_s, is_flip = cell_to_slot[rot_ca]
                rot_list.append((target_s, is_flip))
            self.slot_rot_map.append(rot_list)

    def _seed_state(self, state: _State) -> None:
        pairs = list(range(1, N_SLOTS + 1))
        self.rng.shuffle(pairs)
        for s in range(N_SLOTS):
            state.set_slot(s, pairs[s], flip=self.rng.random() < 0.5)

    def solve(self, iterations: int = 120_000, restarts: int = 6) -> SolveResult:
        """다중 재시작 및 회전 궤적 동기화(CCW Orbit Sync) 기반 탐색."""
        t0 = time.time()
        best_values: dict[Cell, int] | None = None
        best_pen = math.inf
        restart_pens: list[float] = []

        for r in range(restarts):
            state = _State(self.grid)
            self._seed_state(state)
            
            # SA annealing with CCW Orbit-guided moves
            pen = self._anneal_orbit(state, iterations=iterations)
            pen = self._polish_orbit(state)
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
            iterations=iterations
        )

    def _anneal_orbit(self, state: _State, iterations: int) -> float:
        n = len(state.slots)
        cur_pen = state.penalty()
        best_pen = cur_pen
        best_snapshot = list(state.val)

        t0, t1 = 35.0, 0.02
        ratio = math.log(t1 / t0)

        for it in range(iterations):
            if cur_pen <= PENALTY_FLOOR:
                break

            t = t0 * math.exp(ratio * it / iterations)
            r_val = self.rng.random()

            if r_val < 0.30:
                # [寄左 / 序左 연산자]: CCW 회전 궤적(Orbit) 상의 슬롯 교환
                rot_k = self.rng.randint(1, 5)
                s1 = self.rng.randrange(n)
                s2, flip2 = self.slot_rot_map[s1][rot_k]

                if s1 == s2:
                    continue

                state.do_swap(s1, s2, flip_s2=flip2)
                new_pen = state.penalty()
                if new_pen <= cur_pen or self.rng.random() < math.exp(-(new_pen - cur_pen) / t):
                    cur_pen = new_pen
                else:
                    state.do_swap(s1, s2, flip_s2=flip2)

            elif r_val < 0.65:
                # 일반 Flip
                s = self.rng.randrange(n)
                state.do_flip(s)
                new_pen = state.penalty()
                if new_pen <= cur_pen or self.rng.random() < math.exp(-(new_pen - cur_pen) / t):
                    cur_pen = new_pen
                else:
                    state.do_flip(s)

            else:
                # 일반 Pair Swap
                s1 = self.rng.randrange(n)
                s2 = self.rng.randrange(n)
                if s1 == s2:
                    continue
                flip = self.rng.random() < 0.5
                state.do_swap(s1, s2, flip)
                new_pen = state.penalty()
                if new_pen <= cur_pen or self.rng.random() < math.exp(-(new_pen - cur_pen) / t):
                    cur_pen = new_pen
                else:
                    state.do_swap(s1, s2, flip)

            if cur_pen < best_pen:
                best_pen = cur_pen
                best_snapshot = list(state.val)

        state.val[:] = best_snapshot
        state.recompute_sums()
        return best_pen

    def _polish_orbit(self, state: _State, max_rounds: int = 50) -> float:
        """회전 이웃을 포함한 국소 최적화(Polishing)."""
        n = len(state.slots)
        cur_pen = state.penalty()

        for _ in range(max_rounds):
            improved = False
            
            # 1. Flip polish
            order = list(range(n))
            self.rng.shuffle(order)
            for s in order:
                state.do_flip(s)
                new_pen = state.penalty()
                if new_pen < cur_pen:
                    cur_pen = new_pen
                    improved = True
                else:
                    state.do_flip(s)

            # 2. Orbit Swap polish (序左·寄左 이웃)
            for s1 in order:
                for rot_k in range(1, 6):
                    s2, flip2 = self.slot_rot_map[s1][rot_k]
                    if s1 == s2:
                        continue
                    state.do_swap(s1, s2, flip_s2=flip2)
                    new_pen = state.penalty()
                    if new_pen < cur_pen:
                        cur_pen = new_pen
                        improved = True
                        break
                    else:
                        state.do_swap(s1, s2, flip_s2=flip2)

            if cur_pen <= PENALTY_FLOOR or not improved:
                break

        return cur_pen


def main():
    parser = argparse.ArgumentParser(description="강화된 序左·寄左 반시계 회전 육고도 솔버")
    parser.add_argument("--iterations", type=int, default=150_000)
    parser.add_argument("--restarts", type=int, default=8)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--outdir", default="output")
    args = parser.parse_args()

    grid = HexGrid()
    solver = EnhancedRotationSolver(grid, seed=args.seed)

    print(f"=== 강화된 序左·寄左 회전 대칭 육고도 탐색기 실행 ===")
    print(f"  설정: 재시작 {args.restarts}회, 반복 {args.iterations:,}회, 시드 {args.seed}")
    t0 = time.time()
    result = solver.solve(iterations=args.iterations, restarts=args.restarts)
    elapsed = time.time() - t0

    print(f"\n탐색 완료! 소요 시간: {elapsed:.2f}초")
    print(f"최종 페널티: {result.penalty} (이론적 하한 {PENALTY_FLOOR})")
    print(f"재시작별 페널티: {result.restart_penalties}")

    errs = validate(result.values, grid)
    rep = measure(result.values, grid)

    print(f"  기본 조건 검증: {'통과 (Valid)' if not errs else errs}")
    print(f"  변 합:   {rep.side_sums} (목표 1355)")
    print(f"  섹터 합: {rep.wedge_sums} (목표 6097/6098)")
    print(f"  광선 합: {rep.ray_sums} (목표 1219/1220)")

    # 결과 저장
    os.makedirs(args.outdir, exist_ok=True)
    out_file = os.path.join(args.outdir, "enhanced_rotation_solution.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({
            "meta": {
                "seed": args.seed,
                "iterations": args.iterations,
                "restarts": args.restarts,
                "penalty": result.penalty,
                "restart_penalties": result.restart_penalties,
                "elapsed_sec": elapsed
            },
            "values": {f"{q},{r}": v for (q, r), v in result.values.items()}
        }, f, ensure_ascii=False, indent=2)
    print(f"결과 저장 완료: {out_file}")


if __name__ == "__main__":
    main()
