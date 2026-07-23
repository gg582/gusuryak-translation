#!/usr/bin/env python3
"""육고도 배치 탐색 알고리즘 비교/대조 벤치마크.

1. 기존 탐색법 (Baseline Solver):
   - 대척쌍 보수 구조 v(c) + v(-c) = 271 및 고리합 조건 만족
   - 135개 슬롯에 (1..135) 값을 배정하는 순열 및 방향(flip) 최적화
   - 탐색 공간: 135! * 2^135

2. 재구성된 생성적 탐색법 (Reconstructed Path Solver):
   - v(P_t) = 6 * t mod 271 조건 강제
   - P_t가 격자 상에서 연속적 경로(walk)를 형성하도록 유도 (평균 hex 거리 최소화)
   - 탐색 공간: 135! * 2^135 (기하 연속성 제약 alpha에 의해 유효 공간 축소)

이 스크립트는 두 알고리즘의 수렴 속도, 목적 함수 도달도, 기하학적 연속성을 벤치마크하고
결과를 output/comparison_results.json에 저장합니다.
"""

import time
import json
import random
import os
import math
from yukgodo.hexgrid import HexGrid, antipode
from yukgodo.solver import _State, _seed_random, _anneal
from yukgodo.search_constructive import ConstructiveSolver

def run_baseline_benchmark(grid: HexGrid, steps: int, seed: int):
    random.seed(seed)
    rng = random.Random(seed)
    state = _State(grid)
    _seed_random(state, rng)
    
    start_time = time.time()
    n = len(state.slots)
    cur = state.penalty()
    best = cur
    history = []
    
    t0, t1 = 40.0, 0.05
    ratio = math.log(t1 / t0)
    
    for it in range(steps):
        if cur <= 6.0:
            break
        t = t0 * math.exp(ratio * it / steps)
        move = rng.random()
        if move < 0.4:
            s = rng.randrange(n)
            ca, cb = state.slots[s]
            old_p = state.penalty()
            state.do_flip(s)
            new_p = state.penalty()
            delta = new_p - old_p
            if delta <= 0 or rng.random() < math.exp(-delta / t):
                cur = new_p
                if cur < best:
                    best = cur
            else:
                state.do_flip(s)
        elif move < 0.8:
            s1 = rng.randrange(n)
            s2 = rng.randrange(n)
            if s1 != s2:
                old_p = state.penalty()
                flip_s2 = rng.random() < 0.5
                state.do_swap(s1, s2, flip_s2)
                new_p = state.penalty()
                delta = new_p - old_p
                if delta <= 0 or rng.random() < math.exp(-delta / t):
                    cur = new_p
                    if cur < best:
                        best = cur
                else:
                    state.do_swap(s1, s2, flip_s2)
        else:
            s = rng.randrange(n)
            ca, cb = state.slots[s]
            old_p = state.penalty()
            state.do_flip(s)
            new_p = state.penalty()
            delta = new_p - old_p
            if delta <= 0 or rng.random() < math.exp(-delta / t):
                cur = new_p
                if cur < best:
                    best = cur
            else:
                state.do_flip(s)
                
        if it % 1000 == 0:
            history.append({"step": it, "penalty": best})
            
    elapsed = time.time() - start_time
    
    # Calculate baseline path continuity
    # Since baseline has no natural path, we define a path by sorting values from 1 to 270
    val_map = state.to_values()
    sorted_cells = sorted(val_map.keys(), key=lambda c: val_map[c])
    tot_dist = 0
    for t in range(269):
        c1 = sorted_cells[t]
        c2 = sorted_cells[t+1]
        dq = c2[0] - c1[0]
        dr = c2[1] - c1[1]
        dist = max(abs(dq), abs(dr), abs(dq + dr))
        tot_dist += dist
    avg_dist = tot_dist / 269.0
    
    return {
        "algorithm": "Baseline SA (solver.py)",
        "elapsed_seconds": elapsed,
        "final_penalty": best,
        "avg_path_distance": avg_dist,
        "history": history
    }

def run_constructive_benchmark(grid: HexGrid, steps: int, alpha: float, seed: int):
    solver = ConstructiveSolver(grid)
    start_time = time.time()
    
    rng = random.Random(seed)
    order = list(range(135))
    rng.shuffle(order)
    signs = [1 if rng.random() < 0.5 else -1 for _ in range(135)]
    
    cost, penalty, avg_dist, values = solver.evaluate(order, signs, alpha)
    best_penalty = penalty
    best_cost = cost
    best_dist = avg_dist
    
    t0, t1 = 80.0, 0.1
    ratio = math.log(t1 / t0)
    history = []
    
    for it in range(steps):
        if penalty <= 6.0 and alpha == 0.0:
            break
        t = t0 * math.exp(ratio * it / steps)
        
        # Propose move
        move_type = rng.random()
        if move_type < 0.4:
            # swap two path slots
            i = rng.randrange(135)
            j = rng.randrange(135)
            if i != j:
                order[i], order[j] = order[j], order[i]
                nc, np, nd, nv = solver.evaluate(order, signs, alpha)
                delta = nc - cost
                if delta <= 0 or rng.random() < math.exp(-delta / t):
                    cost, penalty, avg_dist, values = nc, np, nd, nv
                    if penalty < best_penalty:
                        best_penalty = penalty
                    if cost < best_cost:
                        best_cost = cost
                        best_dist = avg_dist
                else:
                    order[i], order[j] = order[j], order[i]
        elif move_type < 0.8:
            # flip direction of a slot
            i = rng.randrange(135)
            signs[i] = -signs[i]
            nc, np, nd, nv = solver.evaluate(order, signs, alpha)
            delta = nc - cost
            if delta <= 0 or rng.random() < math.exp(-delta / t):
                cost, penalty, avg_dist, values = nc, np, nd, nv
                if penalty < best_penalty:
                    best_penalty = penalty
                if cost < best_cost:
                    best_cost = cost
                    best_dist = avg_dist
            else:
                signs[i] = -signs[i]
        else:
            # joint swap & flip
            i = rng.randrange(135)
            j = rng.randrange(135)
            if i != j:
                order[i], order[j] = order[j], order[i]
                signs[i] = -signs[i]
                nc, np, nd, nv = solver.evaluate(order, signs, alpha)
                delta = nc - cost
                if delta <= 0 or rng.random() < math.exp(-delta / t):
                    cost, penalty, avg_dist, values = nc, np, nd, nv
                    if penalty < best_penalty:
                        best_penalty = penalty
                    if cost < best_cost:
                        best_cost = cost
                        best_dist = avg_dist
                else:
                    order[i], order[j] = order[j], order[i]
                    signs[i] = -signs[i]
                    
        if it % 1000 == 0:
            history.append({"step": it, "penalty": penalty, "avg_dist": avg_dist})
            
    elapsed = time.time() - start_time
    
    return {
        "algorithm": f"Constructive SA (alpha={alpha})",
        "elapsed_seconds": elapsed,
        "final_penalty": best_penalty,
        "avg_path_distance": best_dist,
        "history": history
    }

def main():
    print("=== 비교 실험 시작 ===")
    grid = HexGrid()
    
    steps = 30000
    seed = 42
    
    print("1. Baseline SA 실행 중...")
    res_base = run_baseline_benchmark(grid, steps, seed)
    print(f"  완료: Penalty={res_base['final_penalty']}, AvgDist={res_base['avg_path_distance']:.3f}, Time={res_base['elapsed_seconds']:.2f}s")
    
    print("2. Constructive SA (alpha=0.0) 실행 중...")
    res_c0 = run_constructive_benchmark(grid, steps, alpha=0.0, seed=seed)
    print(f"  완료: Penalty={res_c0['final_penalty']}, AvgDist={res_c0['avg_path_distance']:.3f}, Time={res_c0['elapsed_seconds']:.2f}s")
    
    print("3. Constructive SA (alpha=2.0) 실행 중...")
    res_c2 = run_constructive_benchmark(grid, steps, alpha=2.0, seed=seed)
    print(f"  완료: Penalty={res_c2['final_penalty']}, AvgDist={res_c2['avg_path_distance']:.3f}, Time={res_c2['elapsed_seconds']:.2f}s")
    
    results = {
        "baseline": res_base,
        "constructive_alpha_0": res_c0,
        "constructive_alpha_2": res_c2,
        "metadata": {
            "steps": steps,
            "seed": seed
        }
    }
    
    os.makedirs("output", exist_ok=True)
    with open("output/comparison_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("결과 저장 완료: output/comparison_results.json")

if __name__ == "__main__":
    main()
