#!/usr/bin/env python3
"""양도(07)와 음도(08)를 같은 좌표끼리 겹쳐 두 방진 사이의 관계를 분석."""
from collections import defaultdict

yang = [
    [(5,1),(6,3),(4,2),(8,7),(9,9),(7,8),(2,4),(3,6),(1,5)],
    [(4,3),(5,2),(6,1),(7,9),(8,8),(9,7),(1,6),(2,5),(3,4)],
    [(6,2),(4,1),(5,3),(9,8),(7,7),(8,9),(3,5),(1,4),(2,6)],
    [(2,7),(3,9),(1,8),(5,4),(6,6),(4,5),(8,1),(9,3),(7,2)],
    [(1,9),(2,8),(3,7),(4,6),(5,5),(6,4),(7,3),(8,2),(9,1)],
    [(3,8),(1,7),(2,9),(6,5),(4,4),(5,6),(9,2),(7,1),(8,3)],
    [(8,4),(9,6),(7,5),(2,1),(3,3),(1,2),(5,7),(6,9),(4,8)],
    [(7,6),(8,5),(9,4),(1,3),(2,2),(3,1),(4,9),(5,8),(6,7)],
    [(9,5),(7,4),(8,6),(3,2),(1,1),(2,3),(6,8),(4,7),(5,9)],
]
yin = [
    [(5,6),(9,2),(1,7),(7,8),(5,1),(3,6),(1,3),(9,4),(5,8)],
    [(3,8),(4,4),(8,3),(2,4),(9,9),(4,2),(6,7),(2,2),(7,6)],
    [(7,1),(2,9),(6,5),(6,3),(1,5),(8,7),(8,5),(4,9),(3,1)],
    [(1,2),(8,4),(9,6),(6,4),(1,9),(8,2),(9,8),(6,2),(4,1)],
    [(5,7),(3,3),(7,5),(7,3),(5,5),(3,7),(3,5),(7,7),(5,3)],
    [(6,9),(4,8),(2,1),(2,8),(9,1),(4,6),(1,4),(2,6),(8,9)],
    [(7,9),(6,1),(2,5),(2,3),(9,5),(4,7),(4,5),(8,1),(3,9)],
    [(3,4),(8,8),(4,3),(8,6),(1,1),(6,8),(2,7),(6,6),(7,2)],
    [(5,2),(1,6),(9,7),(7,4),(5,9),(3,2),(9,3),(1,8),(5,4)],
]

# --- 기본 검산 ---
for name, g in (("yang", yang), ("yin", yin)):
    pairs = [p for row in g for p in row]
    rows = [sum(a+b for a,b in row) for row in g]
    cols = [sum(g[r][c][0]+g[r][c][1] for r in range(9)) for c in range(9)]
    blocks = [sum(g[r][c][0]+g[r][c][1] for r in range(br,br+3) for c in range(bc,bc+3))
              for br in (0,3,6) for bc in (0,3,6)]
    print(f"{name}: pairs unique={len(set(pairs))==81}, rows={set(rows)}, cols={set(cols)}, blocks={sorted(set(blocks))}")

# --- 겹침: 같은 좌표의 양도쌍 (a,b) -> 음도쌍 (c,d) ---
perm = {}
for r in range(9):
    for c in range(9):
        perm[yang[r][c]] = yin[r][c]

# 순열의 순환 구조
seen, cycles = set(), []
for p in perm:
    if p not in seen:
        cyc, x = [], p
        while x not in seen:
            seen.add(x); cyc.append(x); x = perm[x]
        cycles.append(cyc)
print("cycle lengths:", sorted(len(c) for c in cycles))
print("involution:", all(perm[perm[p]] == p for p in perm))
print("fixed points:", [p for p in perm if perm[p] == p])

# 성분별 대응: c가 a만의 함수인가 등
maps = {k: defaultdict(set) for k in ("a->c","a->d","b->c","b->d","a+b->c+d")}
for (a,b),(c,d) in perm.items():
    maps["a->c"][a].add(c); maps["a->d"][a].add(d)
    maps["b->c"][b].add(c); maps["b->d"][b].add(d)
    maps["a+b->c+d"][a+b].add(c+d)
for k, m in maps.items():
    print(k, "is function:", all(len(v)==1 for v in m.values()), {k2: sorted(v2) for k2,v2 in sorted(m.items())})

# 좌표별 4성분 조합의 중복 여부 (직교성 판별)
tests = {
    "(a,c)": lambda a,b,c,d:(a,c), "(a,d)": lambda a,b,c,d:(a,d),
    "(b,c)": lambda a,b,c,d:(b,c), "(b,d)": lambda a,b,c,d:(b,d),
    "(a+b,c+d)": lambda a,b,c,d:(a+b,c+d),
    "(a,c+d)": lambda a,b,c,d:(a,c+d), "(b,c+d)": lambda a,b,c,d:(b,c+d),
    "(a+b,c)": lambda a,b,c,d:(a+b,c), "(a+b,d)": lambda a,b,c,d:(a+b,d),
    "(a-b,c-d)": lambda a,b,c,d:(a-b,c-d),
}
cells = [(yang[r][c], yin[r][c]) for r in range(9) for c in range(9)]
for name, f in tests.items():
    vals = [f(a,b,c,d) for (a,b),(c,d) in cells]
    print(f"{name}: distinct={len(set(vals))}/81")

# 합/차 관계
print("sum pairs (a+b -> c+d):")
sd = defaultdict(list)
for (a,b),(c,d) in cells: sd[a+b].append(c+d)
for s in sorted(sd): print(" ", s, "->", sorted(sd[s]))

# 위치 구조: 음도 좌표가 양도의 변환(회전/대칭/보수)인가
transforms = {
    "identity": lambda r,c:(r,c), "rot90": lambda r,c:(c,8-r),
    "rot180": lambda r,c:(8-r,8-c), "rot270": lambda r,c:(8-c,r),
    "flip_h": lambda r,c:(r,8-c), "flip_v": lambda r,c:(8-r,c),
    "transpose": lambda r,c:(c,r), "anti_transpose": lambda r,c:(8-c,8-r),
}
comp = lambda p:(10-p[0],10-p[1])
swap = lambda p:(p[1],p[0])
for tname, t in transforms.items():
    hits = {"id":0,"comp":0,"swap":0,"comp+swap":0}
    for r in range(9):
        for c in range(9):
            tr, tc = t(r,c)
            y = yang[tr][tc]
            if yin[r][c] == y: hits["id"] += 1
            if yin[r][c] == comp(y): hits["comp"] += 1
            if yin[r][c] == swap(y): hits["swap"] += 1
            if yin[r][c] == comp(swap(y)): hits["comp+swap"] += 1
    print("positional", tname, hits)

# --- 값 기준 정렬: 인코딩 v=9(a-1)+b (1..81) 의 양도 위치 -> 음도 위치 사상 ---
pos_y = {9*(a-1)+b: (r,c) for r,row in enumerate(yang) for c,(a,b) in enumerate(row)}
pos_n = {9*(a-1)+b: (r,c) for r,row in enumerate(yin) for c,(a,b) in enumerate(row)}
sigma = {v: pos_n[v] for v in pos_y}  # v -> yin position
# sigma가 대칭/회전인가
for tname, t in transforms.items():
    ok = all(sigma[v] == t(*pos_y[v]) for v in sigma)
    if ok: print("value-position map = dihedral:", tname)
# sigma가 궁(3x3 블록)을 블록 단위로 옮기는가
def blk(p): return (p[0]//3, p[1]//3)
b2b = defaultdict(set)
for v in sigma: b2b[blk(pos_y[v])].add(blk(sigma[v]))
print("sigma maps blocks to single block:", all(len(s)==1 for s in b2b.values()))

# --- mod 9 아핀 성분 사상 c = αa+βb+γ (mod 9, 0=9) ---
def m9(x): return 9 if x % 9 == 0 else x % 9
cells2 = [((a,b),(c,d)) for (a,b),(c,d) in cells]
cand_c = [(A,B,G) for A in range(9) for B in range(9) for G in range(9)
          if all(m9(A*a+B*b+G) == c for (a,b),(c,d) in cells2)]
cand_d = [(A,B,G) for A in range(9) for B in range(9) for G in range(9)
          if all(m9(A*a+B*b+G) == d for (a,b),(c,d) in cells2)]
print("affine mod9 for c:", cand_c[:5], "for d:", cand_d[:5])

# --- 궁별(블록별) 겹침 성질: 각 블록 안에서 (a,c),(b,d) 등의 다양도 ---
for name, f in tests.items():
    ok = True
    for br in (0,3,6):
        for bc in (0,3,6):
            vals = [f(*yang[r][c], *yin[r][c]) for r in range(br,br+3) for c in range(bc,bc+3)]
            if len(set(vals)) != 9: ok = False
    print("per-block 9-distinct", name, ok)

# --- 양도 블록 합 짝: 180 보수 관계 확인 ---
bsums = {(br,bc): sum(yang[r][c][0]+yang[r][c][1] for r in range(br,br+3) for c in range(bc,bc+3))
         for br in (0,3,6) for bc in (0,3,6)}
print("yang block sums:", bsums)
print("done")
