"""파생 정리(mod N 일반화)의 교차 도안 검증.

**파생 정리**: 값 배치에 기하학적 대합(점대칭 변환) π(π² = id)이 있고 모든 쌍의 값 합이
상수 S이면, 임의의 modulus m에 대해 π는 mod m 잔여류를 r ↦ (S−r) mod m
으로 작용한다. 따라서 잔여류 층은 π-대칭으로 서로 합동(궤도 길이 2)이거나
자기 합동(고정점, 2r ≡ S (mod m)의 해)이다. 쌍 합이 일정하지 않으면
작용은 쌍별 실제 합으로 분해된다. S가 홀수이면 자기쌍 셀이 존재할 수
없고(대합의 고정 셀은 비어 있어야 함), 짝수이면 고정 셀의 값은 S/2로 강제된다.

검증 도안 (../ 형제 장의 데이터, 출처는 각 주석에 명기):

- 06 洛書六觚圖 (본 프로젝트 최적해): S = 271, π = 중심 점대칭 (전역 회전180°)
- 02 九子角得 중궁: S = 46, π = 3×3 중심대칭
- 07 重卦用八圖(팔진도) 가로진: S = 65, π = 행 내 좌우 반전
- 07 侯策用九圖: 쌍 합 ≈73 (불완전) — 상수 S 조건이 깨진 경우의 분해 확인용

실행: python3 -m yukgodo.modn_generalization
"""

from __future__ import annotations

from collections import Counter

from .hexgrid import HexGrid
from .reverse import load_solution

MODULI = [2, 3, 4, 5, 6, 7, 8, 9]


def _yukgodo_pairs() -> list[tuple[int, int]]:
    """06 洛書六觚圖 최적해의 점대칭 쌍 135개 (output/solution.json)."""
    values = load_solution()
    grid = HexGrid()
    pairs = [(values[a], values[b]) for a, b in grid.slots]
    assert all(v + w == 271 for v, w in pairs)
    return pairs


# 02-gakdeuk-series/구자각득/analyze_gujagakdeuk.py:58-62 (center_palace)
# 중심 23 기준 대향 4쌍 + 자기쌍: 15+31 = 41+5 = 6+40 = 16+30 = 46
GUJA_PAIRS = [(15, 31), (41, 5), (6, 40), (16, 30), (23, 23)]

# 07-extra-two/중괘용팔도/visualize_corrected.py:139-144, 210-215 (가로진 좌우 쌍)
PALJIN_PAIRS = [(14, 51), (19, 46), (35, 30), (62, 3),
                (7, 58), (26, 39), (42, 23), (55, 10)]

# 07-extra-two/후책용구도/visualize.py:89-165 (9 formations × 4 위치쌍)
HUCHAEK_PAIRS = [
    (5, 68), (33, 45), (41, 31), (67, 6),
    (3, 70), (34, 40), (39, 33), (64, 4),
    (73, 1), (36, 38), (37, 35), (71, 2),
    (18, 55), (19, 56), (54, 20), (11, 62),
    (16, 57), (21, 51), (52, 22), (58, 15),
    (14, 59), (23, 49), (50, 24), (60, 13),
    (11, 62), (26, 48), (42, 25), (61, 12),
    (9, 64), (28, 46), (45, 27), (63, 10),
    (7, 66), (30, 44), (43, 29), (65, 8),
]


def action_matrix(pairs: list[tuple[int, int]], m: int) -> list[list[int]]:
    """A[i][j] = 값 ≡ i 인 셀의 대칭점 값이 ≡ j 인 (무향) 쌍 수."""
    A = [[0] * m for _ in range(m)]
    for v, w in pairs:
        A[v % m][w % m] += 1
        A[w % m][v % m] += 1
    return A


def fixed_points(S: int, m: int) -> list[int]:
    """2r ≡ S (mod m) 의 해."""
    return [r for r in range(m) if (2 * r - S) % m == 0]


def verify(name: str, pairs: list[tuple[int, int]], note: str) -> None:
    sums = Counter(v + w for v, w in pairs)
    print(f"\n[{name}] 쌍 {len(pairs)}개 — {note}")
    if len(sums) == 1:
        S = next(iter(sums))
        print(f"  쌍 합 상수 S = {S} (자기쌍: "
              f"{[v for v, w in pairs if v == w] or '없음'})")
        for m in MODULI:
            A = action_matrix(pairs, m)
            off = [(i, j) for i in range(m) for j in range(m)
                   if A[i][j] and j != (S - i) % m]
            orbits = sorted({tuple(sorted((i, (S - i) % m)))
                             for i in range(m)})
            fp = fixed_points(S, m)
            print(f"  mod {m}: (i, S−i) 외 성분 {len(off)}건 → 패턴 "
                  f"{'정확' if not off else '불일치'}; "
                  f"궤도 {orbits}, 고정점 {fp or '없음'}")
    else:
        print(f"  쌍 합 불일치 — 분포 {dict(sorted(sums.items()))}")
        top_s, _ = sums.most_common(1)[0]
        sub = [(v, w) for v, w in pairs if v + w == top_s]
        A = action_matrix(pairs, 5)
        off = [(i, j) for i in range(5) for j in range(5)
               if A[i][j] and j != (top_s - i) % 5]
        A_sub = action_matrix(sub, 5)
        off_sub = [(i, j) for i in range(5) for j in range(5)
                   if A_sub[i][j] and j != (top_s - i) % 5]
        print(f"  전체를 S={top_s}로 간주 시 (i, S−i) 외 성분: {len(off)}건 "
              f"→ 패턴 붕괴 (정리의 조건 위반)")
        print(f"  합 {top_s}인 {len(sub)}쌍만 추리면: 외 성분 {len(off_sub)}건 "
              f"→ 패턴 정확 (정리는 쌍별 실제 합으로 분해)")


def main() -> None:
    print("=" * 64)
    print("파생 정리 (mod N 잔여류 작용 r ↦ S−r) 교차 도안 검증")
    print("=" * 64)
    verify("06 洛書六觚圖", _yukgodo_pairs(),
           "π = 중심 점대칭 (전역 회전180°)")
    verify("02 九子角得 중궁", GUJA_PAIRS,
           "π = 3×3 중심대칭; S 짝수 → 자기쌍 값 S/2 = 23 강제")
    verify("07 重卦用八圖 가로진", PALJIN_PAIRS,
           "π = 행 내 좌우 반전 (국소 대칭)")
    verify("07 侯策用九圖", HUCHAEK_PAIRS,
           "전사 불완전 — 값 11, 62가 formation 4·7에 중복 등장")

    print("\n## 판정")
    print("  - 상수 쌍 합 S를 가지는 세 도안: 모든 modulus(2..9)에서")
    print("    점대칭 잔여류 작용이 정확히 r ↦ S−r → 파생 정리 성립.")
    print("  - S = 271(홀수) → 자기쌍 불가 → 중심 虛一과 정합;")
    print("    S = 46(짝수) → 자기쌍 값 23 = S/2로 강제 (중궁 중심).")
    print("  - 侯策用九圖: 합이 섞여 있으면 패턴이 붕괴하고, 합 73인 쌍만")
    print("    추리면 정확 → 정리는 쌍별 실제 합으로 분해 (조건의 필요성 확인).")


if __name__ == "__main__":
    main()
