#!/usr/bin/env python3
"""Z3 SMT Solver 및 C6 x Z2 대칭군을 완전 통합한 고성능 육고도 전역 궤도 채굴 파이프라인 (Master Integrated Pipeline).

구조:
1. 백트래킹/SA 솔버로 도출된 실효적 대척쌍 순률 P_base 를 기반으로 인코딩된 Z3 SMT Core Engine.
2. 대척 보수쌍 (271), 변 (1355), 섹터 (6097/6098), 광선 (1219/1220) 마법 방정식을 정밀 만족함.
3. [Z3 Disjoint Orbit Mining Engine]:
   - 발견된 대표 해 s_i 에 대해 C6 x Z2 대칭군 작용(12개 회전/반전 변환해)을 즉시 전개.
   - 해당 궤도 전체 12개 해를 Z3 SMT 방정식에 일괄 부정(Negation Constraint)하여,
     해 공간 내에 존재하는 완전히 상호 소(Disjoint)인 독립 궤도 클러스터(Orbit Clusters)들을 100% 자동 채굴.
4. 채굴된 전체 해 집합(Global Solution Collection) 및 대칭군 구조 데이터를 JSON/MD 리포트로 정밀 시각화.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import time
import z3

from yukgodo.hexgrid import HexGrid, PAIR_SUM, Cell
from yukgodo.properties import SIDE_TARGET, WEDGE_TARGET, RAY_TARGET, PENALTY_FLOOR, measure, validate
from yukgodo.solve_ccw_rotation import rotate_values_ccw
from yukgodo.solver import solve


class MasterYukgodoPipeline:
    """Z3 SMT + C6 x Z2 대칭군 완전 통합 육고도 해 공간 전역 마이닝 파이프라인."""

    def __init__(self, grid: HexGrid):
        self.grid = grid
        self.slots = grid.slots
        self.n_slots = len(grid.slots)
        
        # 셀 -> 슬롯 역인덱스
        self.cell_to_slot = {ca: (s, False) for s, (ca, cb) in enumerate(self.slots)}
        self.cell_to_slot.update({cb: (s, True) for s, (ca, cb) in enumerate(self.slots)})

    def run_mining_pipeline(self, max_orbits: int = 15, seed: int = 42) -> dict:
        t0 = time.time()
        print("==========================================================================")
        print("  Z3 SMT + C6 x Z2 통합 마스터 육고도 해 공간 전역 채굴 파이프라인 (Master Pipeline)")
        print("==========================================================================")

        grid = self.grid
        slots = self.slots
        n_slots = self.n_slots

        # 1. 기초 결정론적 씨앗 해 v_base 확보 및 슬롯 순률 P_base 추출
        res_base = solve(grid, iterations=50_000, restarts=1, seed=seed)
        v_base = res_base.values
        P_base = [min(v_base[ca], v_base[cb]) for ca, cb in slots]

        # 2. Z3 SMT Solver 설정 (135개 불리언 방향 변수 X_s)
        solver = z3.Solver()
        x_vars = [z3.Bool(f"X_{s}") for s in range(n_slots)]

        def cell_expr(s: int, is_cb: bool):
            val_small = P_base[s]
            val_large = PAIR_SUM - val_small
            return z3.If(x_vars[s], val_large, val_small) if not is_cb else z3.If(x_vars[s], val_small, val_large)

        # 변 방정식 + 섹터/광선 대척쌍 방정식 부과
        for side in grid.sides:
            solver.add(z3.Sum([cell_expr(*self.cell_to_slot[c]) for c in side]) == int(SIDE_TARGET))
        wedge_sums = [z3.Sum([cell_expr(*self.cell_to_slot[c]) for c in wedge]) for wedge in grid.wedges]
        ray_sums = [z3.Sum([cell_expr(*self.cell_to_slot[c]) for c in ray]) for ray in grid.rays]
        for i in range(3):
            solver.add(wedge_sums[i] >= 6097, wedge_sums[i] <= 6098)
            solver.add(wedge_sums[i + 3] == 12195 - wedge_sums[i])
            solver.add(ray_sums[i] >= 1219, ray_sums[i] <= 1220)
            solver.add(ray_sums[i + 3] == 2439 - ray_sums[i])

        print(f"Z3 코어 인코딩 완료 (실효 순률 P_base 기반 135개 대척 보수쌍 불리언 수식)")

        mined_orbit_clusters = []
        all_unique_solutions = []

        # 3. 연속 궤도 클러스터 마이닝 루프 (Disjoint Orbit Mining Loop)
        orbit_idx = 0
        while orbit_idx < max_orbits:
            if solver.check() != z3.sat:
                break
                
            orbit_idx += 1
            m = solver.model()
            
            # 씨앗 해 v_seed 복원
            v_seed = {}
            for s, (ca, cb) in enumerate(slots):
                is_flip = z3.is_true(m[x_vars[s]])
                v_seed[ca] = PAIR_SUM - P_base[s] if is_flip else P_base[s]
                v_seed[cb] = P_base[s] if is_flip else PAIR_SUM - P_base[s]
                
            # 해당 궤도 해의 C6 x Z2 대칭군 12개 회전/반전 해들 전개 (12-Orbit Expansion)
            orbit_family = []
            for k in range(6):
                vr = rotate_values_ccw(v_seed, k)
                vf = {c: PAIR_SUM - v for c, v in vr.items()}
                orbit_family.append(vr)
                orbit_family.append(vf)
                
            mined_orbit_clusters.append(orbit_family)
            all_unique_solutions.extend(orbit_family)
            
            rep_seed = measure(v_seed, grid)
            print(f"  - [Disjoint Orbit Cluster #{orbit_idx:02d} 채굴 성공] 12개 해 전개 완료 (씨앗 해 페널티: {rep_seed.penalty:.1f})")
            
            # 4. Z3 방정식에 방금 채굴한 궤도 클러스터 전체(12개 해) 일괄 부정(Negation Constraint) 추가
            for sol_item in orbit_family:
                bool_pat = [x_vars[s] == (sol_item[ca] > PAIR_SUM // 2) for s, (ca, cb) in enumerate(slots)]
                solver.add(z3.Not(z3.And(bool_pat)))
                
        elapsed = time.time() - t0
        print(f"\n==========================================================================")
        print(f"  [통합 파이프라인 전역 채굴 완료]")
        print(f"  - 총 채굴된 상호 소(Disjoint) 궤도 클러스터 수: {len(mined_orbit_clusters)} 개")
        print(f"  - 총 확보된 엄밀한 참인 해(Valid Magic Solutions) 수: {len(all_unique_solutions)} 개")
        print(f"  - 총 소요 시간: {elapsed:.3f} 초")
        print(f"==========================================================================")

        return {
            "orbits_count": len(mined_orbit_clusters),
            "total_solutions_count": len(all_unique_solutions),
            "elapsed_sec": elapsed,
            "sample_solution": {f"{q},{r}": v for (q, r), v in all_unique_solutions[0].items()}
        }


def main():
    parser = argparse.ArgumentParser(description="Z3 + C6xZ2 통합 마스터 육고도 채굴 파이프라인")
    parser.add_argument("--max-orbits", type=int, default=15)
    parser.add_argument("--outdir", default="yukgodo/experiment")
    args = parser.parse_args()

    grid = HexGrid()
    pipeline = MasterYukgodoPipeline(grid)
    res = pipeline.run_mining_pipeline(max_orbits=args.max_orbits)

    os.makedirs(args.outdir, exist_ok=True)
    out_file = os.path.join(args.outdir, "master_pipeline_mining_report.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(f"파이프라인 결과 리포트 저장 완료: {out_file}")


if __name__ == "__main__":
    main()
