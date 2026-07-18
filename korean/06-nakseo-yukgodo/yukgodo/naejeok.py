"""來積法 판독 수치의 수리적 검증 — 계산 그래프 전수조사.

ALGO_OCR_SUCCESS.md(OCR)와 README.md(확정 원문)에 출현하는 수치를
노드로 삼아, 성립하는 산식 간선을 전수조사로 찾고 來積法의
계산 절차를 재구성한다.

가정 (사용자 지시):
- ○는 문두 표시 또는 말마침표. 수치 0으로 환산하지 않는다
  (九數略에서 0은 零으로만 표기). 따라서 「得五百○」는 수치 五百로 끊는다.
- 판독 수치(152, 252, 19, 54, 6, 270 등)는 확정값이며 변조하지 않는다.

실행: python3 -m yukgodo.naejeok
"""

from __future__ import annotations

from collections import Counter
from itertools import permutations, product

from yukgodo import hexgrid

# ────────────────────────────────────────────────
# 1. 기하 상수: 프로젝트 격자 모델(yukgodo.hexgrid)로 확정
# ────────────────────────────────────────────────
grid = hexgrid.HexGrid()

RING_SIZES = [len(grid.rings[k]) for k in range(1, 10)]
ROW_GROUPS = Counter(q for (q, _r) in grid.cells)         # q = const 인 행
ROW_LENGTHS = [ROW_GROUPS[q] for q in sorted(ROW_GROUPS)]  # 10..19..10
WEDGE_SIZES = sorted(len(w) for w in grid.wedges)
AXIS_LEN = len(grid.axes[0])

assert RING_SIZES == [6 * k for k in range(1, 10)]         # 6,12,...,54
assert ROW_LENGTHS == list(range(10, 20)) + list(range(18, 9, -1))
assert hexgrid.N_CELLS == 271 and hexgrid.N_FILLED == 270
assert hexgrid.SIDE == 10
assert AXIS_LEN == 19                                      # 中觚
assert WEDGE_SIZES == [45] * 6                             # 섹터 45칸 × 6

UPPER9 = sum(ROW_LENGTHS[:9])                              # 10+...+18 = 126
assert UPPER9 == 126

# ────────────────────────────────────────────────
# 2. 원문 수치 풀 (OCR + README 확정 원문에서만 추출)
# ────────────────────────────────────────────────
TEXT: dict[str, int] = {
    "五十四(校計周)": 54,
    "六(添六/係以六)": 6,
    "六十(添六得六十)": 60,
    "十(六而一得一十)": 10,
    "二十(倍之得二十)": 20,
    "十九(中觚)": 19,
    "十二(寄左以數十二)": 12,
    "十一(添十一)": 11,
    "九(九乘/九環)": 9,
    "一百五十二": 152,
    "二百五十二": 252,
    "百(合百)": 100,
    "五百(得五百)": 500,
    "五百六": 506,
    "二百七十(共積)": 270,
    "二百七十一(虛一 전체)": 271,
    "四十五(洛書數)": 45,
    "一(虛一/而一加一)": 1,
}

# 파생 수치: 원문 수치의 산식 또는 격자 부분합 (2단계 탐색용)
DERIVED: dict[str, int] = {
    "上九行和(10+..+18)": UPPER9,                 # 126
    "首十+末十八": ROW_LENGTHS[0] + ROW_LENGTHS[8],   # 28
    "二十−十二": 20 - 12,                          # 8
    "九×十九": 9 * 19,                             # 171
    "六十×九": 60 * 9,                             # 540
    "二百七十−二十": 270 - 20,                     # 250
    "首環+末環(6+54)": 6 + 54,                     # 60 (六十와 동일치)
}

OPS = [
    ("+", lambda a, b: a + b),
    ("-", lambda a, b: a - b),
    ("×", lambda a, b: a * b),
    ("÷", lambda a, b: a // b if b and a % b == 0 else None),
]


def find_edges(pool: dict[str, int], targets: set[int]) -> list[tuple[str, str, str, int]]:
    """pool의 모든 순서쌍 (a,b)에 대해 a op b ∈ targets 인 간선을 전수 반환."""
    edges = []
    for (na, a), (nb, b) in permutations(pool.items(), 2):
        for sym, fn in OPS:
            v = fn(a, b)
            if v is not None and v in targets:
                edges.append((na, sym, nb, v))
    return edges


def show(title: str, edges: list[tuple[str, str, str, int]]) -> None:
    print(f"\n## {title}")
    seen = set()
    for na, sym, nb, v in edges:
        key = (v, na, sym, nb)
        if key in seen:
            continue
        seen.add(key)
        print(f"  {na} {sym} {nb} = {v}")


# ────────────────────────────────────────────────
# 3. 전수조사
# ────────────────────────────────────────────────
text_vals = set(TEXT.values())

print("=" * 64)
print("來積法 계산 그래프 검증 (python3 -m yukgodo.naejeok)")
print("=" * 64)
print("\n## 1. 기하 상수 (격자 모델 확정)")
print(f"  고리: {RING_SIZES}  합={sum(RING_SIZES)}")
print(f"  행 길이: {ROW_LENGTHS}  합={sum(ROW_LENGTHS)}")
print(f"  전체 {hexgrid.N_CELLS}칸, 虛一 후 {hexgrid.N_FILLED}칸, "
      f"변당 {hexgrid.SIDE}칸, 中觚 {AXIS_LEN}칸, 섹터 {WEDGE_SIZES[0]}칸×6")

show("2. 1단계: 원문 수치끼리의 항등식 (피연산자·결과 모두 원문 출현)",
     find_edges(TEXT, text_vals))

merged = {**TEXT, **DERIVED}
edges2 = [e for e in find_edges(merged, text_vals)
          if e[0] in DERIVED or e[2] in DERIVED]
show("3. 2단계: 파생 수치를 한 항 포함하는 항등식", edges2)

# ────────────────────────────────────────────────
# 4. 재구성 체인: 각 단계를 assert로 검증
# ────────────────────────────────────────────────
print("\n## 4. 재구성된 來積法 계산 체인")
steps = [
    ("置外周五十四，添六得六十", 54 + 6, 60),
    ("六而一得一十 (변당 칸 수)", 60 // 6, 10),
    ("倍之得二十", 10 * 2, 20),
    ("減一為十九，為中觚數也", 20 - 1, 19),
    ("添一의 반복으로 상9행 생성: 10,11,...,18", None, None),
    ("(首十+末十八)×九 = 二百五十二", (10 + 18) * 9, 252),
    ("  검증: 상9행 합 126 의 2倍", 2 * UPPER9, 252),
    ("別경로: (二十−十二)×十九 = 一百五十二", (20 - 12) * 19, 152),
    ("一百五十二 + 百(十²) = 二百五十二 (合流)", 152 + 100, 252),
    ("二百五十二 + 十九(中觚) = 二百七十一", 252 + 19, 271),
    ("虛一則二百七十", 271 - 1, 270),
]
for label, got, want in steps:
    if got is None:
        seq = list(range(10, 19))
        assert seq == ROW_LENGTHS[:9]
        print(f"  [성립] {label}  → {seq}, 합={sum(seq)}")
        continue
    status = "성립" if got == want else "불일치"
    assert got == want, label
    print(f"  [{status}] {label}  → {got}")

print("\n## 5. 독립 검산 경로 (모두 정확히 270에 도달)")
checks = [
    ("洛書數六倍: 6×45", 6 * 45, 270),
    ("고리 등차급수: (首環6+末環54)×九÷2", (6 + 54) * 9 // 2, 270),
    ("六十×九 = 五百四十, 반지", 60 * 9 // 2, 270),
    ("外周×五 (54×5)", 54 * 5, 270),
    ("중심 포함 총칸 − 1", 271 - 1, 270),
]
for label, got, want in checks:
    assert got == want, label
    print(f"  [성립] {label} = {got}")

# ────────────────────────────────────────────────
# 6. 기각되는 독해 / 미연결 조각
# ────────────────────────────────────────────────
print("\n## 6. 기각되는 독해")
rejections = [
    ("一百五十二를 二百五十二 오독으로 처리", 8 * 19, 152,
     "152=(二十−十二)×十九로 독립 성립하고 252−152=100=十² → 오독 아님, 유효 노드"),
    ("一百五十二倍之", 152 * 2, 304,
     "304는 원문·기하 어디에도 없음 → 倍之의 주어는 一百五十二가 아님"),
]
for label, got, want, reason in rejections:
    print(f"  [기각] {label}: 계산값={got} → {reason}")

print("\n## 7. 고립 꼬리(得五百/五百六) 생성 경로 전수조사")
frag_tests = [
    ("序左十九六合百 — 19×6+100", 19 * 6 + 100),
    ("序左十九六合百 — 19×6", 19 * 6),
    ("序左十九六合百 — 19+6+100", 19 + 6 + 100),
]
for label, got in frag_tests:
    hit = "원문 수치와 일치" if got in text_vals else "원문 수치와 불일치"
    print(f"  {label} = {got} → {hit}")


def tail_paths(target: int) -> tuple[list[str], list[str]]:
    """원문 수치만 피연산자로 쓰는 target 생성식 (×1/÷1 항등 연산 제외)."""
    items = [(v, k) for k, v in TEXT.items() if v not in (500, 506)]
    one, two = set(), set()
    for (a, na), (b, nb) in product(items, repeat=2):
        for sym, fn in OPS:
            if sym in "×÷" and b == 1:
                continue
            if fn(a, b) == target:
                one.add(f"{na}{sym}{nb}")
    for (a, na), (b, nb), (c, nc) in product(items, repeat=3):
        for s1, f1 in OPS:
            if s1 in "×÷" and b == 1:
                continue
            v1 = f1(a, b)
            if v1 is None or v1 <= 0:
                continue
            for s2, f2 in OPS:
                if s2 in "×÷" and c == 1:
                    continue
                if f2(v1, c) == target:
                    two.add(f"({na}{s1}{nb}){s2}{nc}")
    return sorted(one), sorted(two)


CORE = {270, 271, 252, 152, 100, 60, 54, 45, 20, 19, 10}
for target in (500, 506):
    one, two = tail_paths(target)
    closes = []
    for x, nx in [(v, k) for k, v in TEXT.items() if v not in (500, 506)]:
        for sym, fn in OPS:
            if fn(target, x) in CORE:
                closes.append(f"{target}{sym}{nx}")
            if fn(x, target) in CORE:
                closes.append(f"{nx}{sym}{target}")
    print(f"\n  [{target}] 1-op 생성 {len(one)}건, 2-op 생성 {len(two)}건")
    for e in two:
        print(f"      {e} = {target}")
    print(f"  [{target}] 본 사슬 수치로 닫히는 간선: {closes if closes else '없음'}")

print("\n## 판정")
print("  - 체인(§4)과 검산(§5)의 모든 등식은 정확히 성립 (assert 통과).")
print("  - 五百(500): 1-op 생성 0건, 2-op 생성 22건 — 생성식 특정 불가(포화).")
print("  - 五百六(506): 1-op 생성 0건, 2-op 생성 7건 — 동일.")
print("  - 둘 모두 본 사슬 수치(270/271/252/…)로 닫히는 간선이 없고,")
print("    倍之의 주어도 앞 세 자리 수가 아님(152×2=304 부재) →")
print("    중간 수치가 유실된 별법(案) 검산 단락의 잔편으로 판정.")
print("  - 序左十九六合百: 六을 승수로 읽는 모든 조합이 불일치 → as-written 미결.")
