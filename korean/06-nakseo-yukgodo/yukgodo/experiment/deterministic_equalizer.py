#!/usr/bin/env python3
"""결정론적 구조적 나선-섹터 균등 배치 알고리즘 (Deterministic Spiral-Wedge Equalizer Solver).

원리:
대척 보수쌍 (v, 271-v)을 135개 슬롯에 배치할 때,
6개 변(Target: 1355)과 6개 섹터(Target: 6097/6098), 6개 광선(Target: 1219/1220)의 균형을
난수 없이 '결정론적 순률(Deterministic Rotation & Flip Rule)'로 부여하여 수수형 최적해 생성.
"""

from __future__ import annotations

import argparse
import json
import math
import os

from yukgodo.hexgrid import HexGrid, PAIR_SUM, Cell, antipode
from yukgodo.properties import PENALTY_FLOOR, measure, validate


def solve_deterministic_equalizer(grid: HexGrid) -> tuple[dict[Cell, int], float]:
    """난수 시드 없이 순수한 결정론적 대칭/순률 교대 규칙만으로 해 구성."""
    values: dict[Cell, int] = {}
    
    # 1. 135개 슬롯을 (고리 번호 k, 반시계 위상 θ) 순으로 결정론적 정렬
    slots = grid.slots
    slot_info = []
    for s, (ca, cb) in enumerate(slots):
        ring = max(abs(ca[0]), abs(ca[1]), abs(ca[0] + ca[1]))
        wedge = grid.wedge_of[ca]
        # axial 각도 순서
        angle = math.atan2(ca[1], ca[0])
        slot_info.append((ring, wedge, angle, s, ca, cb))
        
    # 결정론적 1차 정렬 (고리 내 외부 순서, 섹터 교대)
    slot_info.sort(key=lambda x: (x[0], x[1], x[2]))
    
    # 2. 결정론적 값 배정 및 방향 Flip 순률 적용
    # 1..135 쌍을 고리 및 섹터 위치별로 반시계 방향 균등 교대 배정
    for rank, (ring, wedge, _, s, ca, cb) in enumerate(slot_info, start=1):
        val_small = rank
        val_large = PAIR_SUM - rank
        
        # 결정론적 Flip 규칙: (wedge + ring + rank) 짝수 여부에 따라 방향 결정
        flip = ((wedge * 2 + ring + rank) % 2 == 0)
        
        va, vb = (val_large, val_small) if flip else (val_small, val_large)
        values[ca] = va
        values[cb] = vb
        
    rep = measure(values, grid)
    return values, rep.penalty


def main():
    grid = HexGrid()
    vals, pen = solve_deterministic_equalizer(grid)
    print(f"=== 결정론적 균등 배치 알고리즘 (Deterministic Equalizer Solver) ===")
    print(f"  - 난수 사용 여부: 0% (완전 결정론적 방식)")
    print(f"  - 측정 페널티:   {pen:.1f}")
    
    errs = validate(vals, grid)
    print(f"  - 격자 검증:    {'통과 (Valid)' if not errs else errs}")
    
if __name__ == "__main__":
    main()
