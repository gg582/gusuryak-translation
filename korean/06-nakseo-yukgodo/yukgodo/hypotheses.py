"""승적법(添六) 건설 가설 생성 및 검증.

주석의 添六(6을 더해 감)을 문자 그대로 구현한 건설적 배치 후보들:

    - add6 계열: 순회 t번째 칸에 값 (±6·t) mod 271 을 배정.
      271은 소수이고 gcd(6, 271)=1 이므로 값은 1..270을 정확히 한 번씩
      도는 완전 순열이 되며, 0 ≡ 271 이 떨어지는 칸이 곧 虛一이 된다.
      즉 虛一이 장식이 아니라 添六 진행의 자연 귀결이 되는지 검증한다.
    - seq 계열: 1..270 순차 배정 (비교 기준선).

순회(walk) 변형: 안쪽/바깥 진행 × 시작 꼭짓점 6 × 회전 방향 2 ×
고리 진입 방식(같은 꼭짓점/나선 연속) — 전부 측정해 벌점 순으로 정렬한다.
"""

from __future__ import annotations

import json

from .hexgrid import CENTER, DIRECTIONS, HexGrid, add, scale
from .properties import PENALTY_FLOOR, PropertyReport, measure

MODULUS = 271  # 六觚一握, 소수


def ring_walk_from(grid: HexGrid, k: int, corner: int, ccw: bool) -> list:
    """고리 k를 꼭짓점 corner에서 시작해 ccw/cw 방향으로 순회."""
    pos = scale(DIRECTIONS[corner], k)
    walk = []
    for j in range(6):
        step = DIRECTIONS[(corner + 2 + j) % 6] if ccw else DIRECTIONS[(corner - 2 - j) % 6]
        for _ in range(k):
            walk.append(pos)
            pos = add(pos, step)
    return walk


def spiral_walk(grid: HexGrid, start_corner: int, ccw: bool,
                inward: bool, continuous: bool) -> list:
    """중심을 포함한 271칸 전체 순회 (inward면 중심이 마지막)."""
    cells: list = []
    ks = range(grid.radius, 0, -1) if inward else range(1, grid.radius + 1)
    corner = start_corner
    for k in ks:
        cells.extend(ring_walk_from(grid, k, corner, ccw))
        # 나선 연속 진행: 다음 고리의 시작 꼭짓점을 회전 방향으로 한 칸 옮김
        if continuous:
            corner = (corner - 1) % 6 if ccw else (corner + 1) % 6
    if inward:
        cells.append(CENTER)
    else:
        cells.insert(0, CENTER)
    return cells


def construct(grid: HexGrid, walk: list, kind: str) -> dict:
    """순회에 따라 값을 배정한다. 중심 칸은 결과 dict에서 제외(虛一)."""
    values: dict = {}
    filled = [c for c in walk if c != CENTER]
    for t, c in enumerate(filled):
        if kind == "add6":
            v = (6 * (t + 1)) % MODULUS
        elif kind == "sub6":
            v = (-6 * (t + 1)) % MODULUS
        elif kind == "seq":
            v = t + 1
        elif kind == "rev":
            v = len(filled) - t
        else:
            raise ValueError(kind)
        values[c] = v
    return values


def evaluate_all(grid: HexGrid) -> list[dict]:
    """모든 건설 가설을 측정해 벌점 순으로 돌려준다."""
    results: list[dict] = []
    for kind in ("add6", "sub6", "seq", "rev"):
        for inward in (True, False):
            for continuous in (False, True):
                for ccw in (True, False):
                    for corner in range(6):
                        walk = spiral_walk(grid, corner, ccw, inward, continuous)
                        values = construct(grid, walk, kind)
                        rep = measure(values, grid)
                        results.append({
                            "kind": kind,
                            "inward": inward,
                            "continuous": continuous,
                            "ccw": ccw,
                            "corner": corner,
                            "penalty": rep.penalty,
                            "parts": rep.parts,
                            "side_sums": rep.side_sums,
                            "wedge_sums": rep.wedge_sums,
                            "ray_sums": rep.ray_sums,
                            "pair_dev": sum(abs(d) for d in rep.pair_devs),
                        })
    results.sort(key=lambda r: r["penalty"])
    return results


def ring_ap_analysis() -> dict:
    """모형 B 검증: 고리별 +6 등차(mod 271)로 고리 합 813k를 달성하는 시작값.

    각 고리 k마다 시작값이 유일하게 존재하며 a_k = 274 - 18k 의 등차를
    이루는 것은 주목할 구조이나, 값 집합이 고리 간에 중복되어
    1..270 한 번씩 배치 조건을 만족하지 못함을 확인한다.
    """
    per_ring = {}
    used: set[int] = set()
    for k in range(1, 10):
        n, target = 6 * k, 813 * k
        good = []
        for a in range(1, 271):
            s, v, ok = 0, a, True
            for _ in range(n):
                if v == 0:
                    ok = False
                    break
                s += v
                v = (v + 6) % MODULUS
            if ok and s == target:
                good.append(a)
        per_ring[k] = good
        # 대표 후보로 값 집합 누적 (중복 검증용)
        if good:
            v = good[0]
            for _ in range(n):
                used.add(v)
                v = (v + 6) % MODULUS
    class_sums = {
        str(r): sum(v for v in range(1, 271) if v % 6 == r % 6)
        for r in range(1, 7)
    }
    return {
        "per_ring_starts": {str(k): v for k, v in per_ring.items()},
        "start_pattern": "a_k = 274 - 18k (각 고리 유일 해)",
        "distinct_values": len(used),
        "valid": len(used) == 270,
        "verdict": "모형 B는 고리 합은 정확히 맞추지만 값이 중복되어 "
                   "1..270 배치 조건 불만족 → 배치 규칙으로 부적합",
        "model_C_class_sums": class_sums,
        "model_C_note": "mod 6 잔여류 6류 × 45값 = 通加洛書數六倍의 또 다른 독해. "
                        "류별 합은 5985..6210(45 등차), 마주 보는 류 쌍은 12195.",
    }


def main() -> None:
    grid = HexGrid()
    results = evaluate_all(grid)
    best = results[0]
    print(f"건설 가설 {len(results)}개 측정 완료 (탐색 최적해 벌점 {PENALTY_FLOOR} 기준)")
    print("\n상위 10개:")
    for r in results[:10]:
        print(f"  벌점 {r['penalty']:8.1f}  {r['kind']:5s} "
              f"{'내향' if r['inward'] else '외향'} "
              f"{'나선' if r['continuous'] else '동일각'} "
              f"{'ccw' if r['ccw'] else ' cw'} 꼭짓점{r['corner']} "
              f"변편차 {r['parts']['sides']:.0f} 쌍편차 {r['pair_dev']:.0f}")
    print("\n하위 3개 (최악):")
    for r in results[-3:]:
        print(f"  벌점 {r['penalty']:8.1f}  {r['kind']:5s}")

    ring_ap = ring_ap_analysis()
    print("\n모형 B (고리별 +6 등차) 검증:")
    print(f"  고리별 시작값: {ring_ap['per_ring_starts']}")
    print(f"  패턴: {ring_ap['start_pattern']}")
    print(f"  서로 다른 값: {ring_ap['distinct_values']}/270 → {ring_ap['verdict']}")

    out = {
        "note": "添六 건설 가설 검증: 벌점 하한 6.0 = 탐색 최적해 수준",
        "penalty_floor": PENALTY_FLOOR,
        "n_hypotheses": len(results),
        "best": best,
        "top10": results[:10],
        "ring_ap_model_B": ring_ap,
        "conclusion": (
            "주석의 판독 가능한 수치(54+6=60, 60/6=10, 中觔 19, 252×2=504, "
            "270=6×45)는 모두 칸 수 검산일 뿐 값 배치 규칙은 아님. "
            "添六을 값 배치 규칙으로 읽는 모든 건설 가설(±6 mod 271 나선 192변형, "
            "고리별 등차)은 마법 성질 또는 일대일 배치 조건을 만족하지 못함. "
            "따라서 복원 최적해(대점 보수쌍 271 모형)가 현재 최선의 후보이며, "
            "배치 순서 규칙(寄左/序左)은 더 선명한 판본이 필요한 미해결 항목."
        ),
    }
    with open("output/hypotheses.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\n저장: output/hypotheses.json")


if __name__ == "__main__":
    main()
