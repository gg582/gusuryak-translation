#!/usr/bin/env python3
"""09 구구자수변궁양도/음도(九九子數變宮陽圖/陰圖) 검산 및 구조 분석.

07/08(모수도, 순서쌍)과 달리 09(자수도)는 각 칸이 두 수의 곱(구구수)이다.
"""
from collections import Counter

yang = [
    [16, 36,  8, 36, 81, 18,  8, 18,  4],
    [12, 20, 28, 27, 45, 63,  6, 10, 14],
    [32,  4, 24, 72,  9, 54, 16,  2, 12],
    [12, 27,  6, 20, 45, 10, 28, 63, 14],
    [ 9, 15, 21, 15, 25, 35, 21, 35, 49],
    [24,  3, 18, 40,  5, 30, 56,  7, 42],
    [32, 72, 16,  4,  9,  2, 24, 54, 12],
    [24, 40, 56,  3,  5,  7, 18, 30, 42],
    [64,  8, 48,  8,  1,  6, 48,  6, 36],
]
yin = [
    [ 9,  8,  7,  6,  5, 54, 63, 72,  1],
    [18, 21, 14,  8, 10, 12,  6, 64, 72],
    [27, 24, 24, 12, 35, 18, 16,  6, 63],
    [36, 32, 28, 16, 20,  9, 18, 12, 54],
    [45, 30, 15, 40, 25, 20, 35, 10,  5],
    [ 4, 48, 42, 49, 40, 16, 12,  8,  6],
    [ 3, 56, 36, 42, 15, 28, 24, 14,  7],
    [ 2,  4, 56, 48, 30, 32, 24, 21,  8],
    [81,  2,  3,  4, 45, 36, 27, 18,  9],
]

# 구구수(1~9 두 수의 곱) 여부
GUGU = {a * b for a in range(1, 10) for b in range(1, 10)}
# 구구단 81곱의 다중집합 (순서쌍별 1회)
MULT81 = Counter(a * b for a in range(1, 10) for b in range(1, 10))
# 낙서(洛書) 3x3
L = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]


def rows(g):
    return [sum(r) for r in g]

def cols(g):
    return [sum(g[r][c] for r in range(9)) for c in range(9)]

def blocks(g):
    return {(br, bc): sum(g[r][c] for r in range(br, br + 3) for c in range(bc, bc + 3))
            for br in (0, 3, 6) for bc in (0, 3, 6)}

def diags(g):
    return (sum(g[i][i] for i in range(9)), sum(g[i][8 - i] for i in range(9)))


def report(name, g):
    print(f"== {name} ==")
    bad = [(r, c, g[r][c]) for r in range(9) for c in range(9) if g[r][c] not in GUGU]
    print("  non-구구수 cells:", bad or "없음")
    print("  row sums:", rows(g))
    print("  col sums:", cols(g))
    print("  block sums:", blocks(g))
    print("  diagonals (main, anti):", diags(g))
    cnt = Counter(v for row in g for v in row)
    print("  total:", sum(cnt[k] * k for k in cnt),
          "| multiset == 81 products of 九九:", cnt == MULT81)


report("yang", yang)
report("yin", yin)

# --- 양도 크로네커(낙서⊗낙서) 구조 검증 ---
print("\n### 양도: cell == L(궁위치) x L(궁내위치) ? ###")
mismatch = [((r, c), yang[r][c], L[r // 3][c // 3] * L[r % 3][c % 3])
            for r in range(9) for c in range(9)
            if yang[r][c] != L[r // 3][c // 3] * L[r % 3][c % 3]]
print("  일치하지 않는 칸:", mismatch or "없음 — 완전한 낙서⊗낙서")
# 각 궁이 소마방진(궁 내 각 소행·소열 합 동일)인지
print("  궁별 소행/소열 합:")
for br in (0, 3, 6):
    for bc in (0, 3, 6):
        rs = [sum(yang[r][c] for c in range(bc, bc + 3)) for r in range(br, br + 3)]
        cs = [sum(yang[r][c] for r in range(br, br + 3)) for c in range(bc, bc + 3)]
        ok = len(set(rs)) == 1 and len(set(cs)) == 1 and rs[0] == cs[0]
        print(f"    block({br},{bc}): rows={rs} cols={cs} mini-magic={ok}")

# --- 음도 반대각선 대칭 검증 ---
print("\n### 음도: cell(r,c) == cell(8-c, 8-r) 반대각선 대칭? ###")
asym = [((r, c), yin[r][c], (8 - c, 8 - r), yin[8 - c][8 - r])
        for r in range(9) for c in range(9)
        if yin[r][c] != yin[8 - c][8 - r]]
print("  비대칭 칸:", asym or "없음 — 완전 대칭")
print("  반대각선 값:", [yin[i][8 - i] for i in range(9)])
print("  주대각선 값:", [yin[i][i] for i in range(9)])

# --- 양도·음도 같은 좌표 겹침 ---
print("\n### 양도·음도 같은 좌표 겹침 ###")
same = [(r, c, yang[r][c]) for r in range(9) for c in range(9) if yang[r][c] == yin[r][c]]
print("  양·음 같은 값인 칸:", same)
print("done")
