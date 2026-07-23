#!/usr/bin/env python3
"""來積法 판독 수치의 수리적 검증 및 계산 그래프 정밀 모델링.

이 스크립트는 수전사 업데이트로 규명된 '五百四(504)', '去중觚(중구 제외)' 등을 포함하여
來積法의 수치적 계산 흐름을 유향 비순환 그래프(DAG)로 모델링하고 정밀하게 검증합니다.
"""

from __future__ import annotations
import os
import sys
from collections import Counter
from itertools import permutations, product

from yukgodo import hexgrid

# ────────────────────────────────────────────────
# 1. 기하 상수 검증 (격자 모델 확정)
# ────────────────────────────────────────────────
grid = hexgrid.HexGrid()
RING_SIZES = [len(grid.rings[k]) for k in range(1, 10)]
ROW_GROUPS = Counter(q for (q, _r) in grid.cells)
ROW_LENGTHS = [ROW_GROUPS[q] for q in sorted(ROW_GROUPS)]
WEDGE_SIZES = sorted(len(w) for w in grid.wedges)
AXIS_LEN = len(grid.axes[0])
UPPER9 = sum(ROW_LENGTHS[:9])

assert RING_SIZES == [6 * k for k in range(1, 10)]
assert ROW_LENGTHS == list(range(10, 20)) + list(range(18, 9, -1))
assert hexgrid.N_CELLS == 271 and hexgrid.N_FILLED == 270
assert hexgrid.SIDE == 10
assert AXIS_LEN == 19
assert WEDGE_SIZES == [45] * 6
assert UPPER9 == 126

# ────────────────────────────────────────────────
# 2. 문헌 판독 수치 풀 정의
# ────────────────────────────────────────────────
TEXT: dict[str, int] = {
    "五十四(校計周)": 54,
    "六(添六/係以六)": 6,
    "六十(添六得六十)": 60,
    "十(六而一得一十)": 10,
    "二十(倍之得二十)": 20,
    "十九(중觚)": 19,
    "十二(寄左以數十二)": 12,
    "十一(添十一)": 11,
    "九(九乘/九環)": 9,
    "一百52": 152,
    "二百五cell": 252,
    "二百五十二": 252,
    "百(合百)": 100,
    "五百四(倍之得)": 504,
    "五百(오독/오기)": 500,
    "五百六(오독/오기)": 506,
    "二百七十(共積)": 270,
    "二百七十一(虛一 전체)": 271,
    "四十五(洛書數)": 45,
    "一(虛一/而一加一)": 1,
}

DERIVED: dict[str, int] = {
    "上九行和(10+..+18)": UPPER9,                 # 126
    "首十+末十八": ROW_LENGTHS[0] + ROW_LENGTHS[8],   # 28
    "二十−十二": 20 - 12,                          # 8
    "九×十九": 9 * 19,                             # 171
    "六十×九": 60 * 9,                             # 540
    "二百七십−이십": 270 - 20,                     # 250
    "首環+末環(6+54)": 6 + 54,                     # 60
}

OPS = [
    ("+", lambda a, b: a + b),
    ("-", lambda a, b: a - b),
    ("×", lambda a, b: a * b),
    ("÷", lambda a, b: a // b if b and a % b == 0 else None),
]

# ────────────────────────────────────────────────
# 3. DAG 기반 계산 노드 구조 정의 및 모델링
# ────────────────────────────────────────────────
class Node:
    def __init__(self, key: str, value: int, expression: str, src: str):
        self.key = key
        self.value = value
        self.expression = expression
        self.src = src

class NaejeokDAG:
    def __init__(self):
        self.nodes: dict[str, Node] = {}
        
    def add(self, key: str, value: int, expression: str, src: str):
        node = Node(key, value, expression, src)
        self.nodes[key] = node
        
    def verify_all(self):
        print("=" * 64)
        print("來積法 정밀 계산 그래프(DAG) 검증 결과")
        print("=" * 64)
        for key, node in self.nodes.items():
            # 평가식 계산 검증
            calculated = eval(node.expression, {}, {k: n.value for k, n in self.nodes.items()})
            assert calculated == node.value, f"불일치 오류: {key} (기대 {node.value}, 실제 {calculated})"
            print(f"  [성립] {node.src:35s} -> {node.value:4d}  (식: {node.expression})")

dag = NaejeokDAG()

# 상수 및 기하 기초값 등록
dag.add("C54", 54, "54", "외주 54 (置外周五十四)")
dag.add("C6", 6, "6", "기초 증가분 6 (添六/六而一)")
dag.add("C1", 1, "1", "허일 1 (虛一/減一)")
dag.add("C12", 12, "12", "기좌 12 (寄左以數十二)")
dag.add("C11", 11, "11", "첨십일 11 (添十一)")
dag.add("C9", 9, "9", "고리 수 9 (九乘)")
dag.add("C100", 100, "100", "합백 100 (合百)")
dag.add("C2", 2, "2", "배지 2 (倍之/折半)")

# 유도 연산 사슬
dag.add("V60", 60, "C54 + C6", "외주 + 6 = 60 (置外周添六得六十)")
dag.add("V10", 10, "V60 // C6", "60 / 6 = 10 (六而一得一十 - 변당 칸 수)")
dag.add("V20", 20, "V10 * C2", "10 * 2 = 20 (倍之得二十)")
dag.add("V19", 19, "V20 - C1", "20 - 1 = 19 (減一為十九 - 중구 수)")
dag.add("V18", 18, "V10 + V20 - C12", "10 + 8 = 18 (상9행의 마지막 행 길이)")
dag.add("V126", 126, "(V10 + V18) * C9 // C2", "상9행 합 = 126 ((10+18)*9/2)")
dag.add("V252_AP", 252, "(V10 + V18) * C9", "(10 + 18) * 9 = 252 (九乘得二百五十二 - 나누기 2 누락)")
dag.add("V252_AP_CHECK", 252, "V126 * C2", "상9행 합의 2배 = 252 (검산)")

# 152 분기 및 합류
dag.add("V8", 8, "V20 - C12", "20 - 12 = 8 (기좌 연산용 차분)")
dag.add("V152", 152, "V8 * V19", "8 * 19 = 152 (一百五十二 - 독립 분기)")
dag.add("V252_COMB", 252, "V152 + C100", "152 + 100 = 252 (二百五十二 - 사슬 합류)")

# 504 배배(倍之) 및 중구 제외(去中觚) 수전사 핵심 사슬
dag.add("V504", 504, "V252_COMB * C2", "252 * 2 = 504 (二百五十二倍之得五百四)")
dag.add("V252_HALF", 252, "V504 // C2", "504 / 2 = 252 (折半淂二百五十二)")
dag.add("V271", 271, "V252_HALF + V8 + C11", "252 + 8 + 11 = 271 (加八(寄九)淂二百七十一)")
dag.add("V270_GEOM", 270, "V271 - C1", "271 - 1 = 270 (합종구목 - 9개 고리 전체 칸 수)")
dag.add("V18_AXIS", 18, "V19 - C1", "19 - 1 = 18 (중구의 실사용 칸 수)")
dag.add("V252_GEOM", 252, "V270_GEOM - V18_AXIS", "270 - 18 = 252 (합종구목 - 중구 제외 = 252 (不倍, 去中觚))")
dag.add("V270", 270, "V271 - C1", "271 - 1 = 270 (虛一則二百七十 - 최종 사용 칸 수)")

# ────────────────────────────────────────────────
# 4. Mermaid Flowchart 생성 함수
# ────────────────────────────────────────────────
def generate_mermaid_code(dag: NaejeokDAG) -> str:
    lines = ["```mermaid", "graph TD"]
    # 노드 출력
    for key, node in dag.nodes.items():
        if node.key.startswith("C"):
            lines.append(f'  {node.key}["{node.src} ({node.value})"]:::const')
        else:
            lines.append(f'  {node.key}["{node.src} -> {node.value}"]:::calc')
    
    # 엣지 연결 (수동 구성으로 레이아웃 최적화)
    deps = [
        ("C54", "V60"), ("C6", "V60"),
        ("V60", "V10"), ("C6", "V10"),
        ("V10", "V20"), ("C2", "V20"),
        ("V20", "V19"), ("C1", "V19"),
        ("V10", "V18"), ("V20", "V18"), ("C12", "V18"),
        ("V10", "V126"), ("V18", "V126"), ("C9", "V126"), ("C2", "V126"),
        ("V10", "V252_AP"), ("V18", "V252_AP"), ("C9", "V252_AP"),
        ("V126", "V252_AP_CHECK"), ("C2", "V252_AP_CHECK"),
        ("V20", "V8"), ("C12", "V8"),
        ("V8", "V152"), ("V19", "V152"),
        ("V152", "V252_COMB"), ("C100", "V252_COMB"),
        ("V252_COMB", "V504"), ("C2", "V504"),
        ("V504", "V252_HALF"), ("C2", "V252_HALF"),
        ("V252_HALF", "V271"), ("V8", "V271"), ("C11", "V271"),
        ("V271", "V270"), ("C1", "V270"),
        ("V270", "V270_GEOM"),
        ("V270_GEOM", "V252_GEOM"), ("V18_AXIS", "V252_GEOM"),
        ("V19", "V18_AXIS"), ("C1", "V18_AXIS")
    ]
    for src, dest in deps:
        lines.append(f"  {src} --> {dest}")
        
    lines.append("  classDef const fill:#e1f5fe,stroke:#01579b,stroke-width:2px;")
    lines.append("  classDef calc fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px;")
    lines.append("```")
    return "\n".join(lines)

# ────────────────────────────────────────────────
# 5. 경로 탐색 알고리즘 (BFS)
# ────────────────────────────────────────────────
def find_shortest_path(start_vals: dict[str, int], target: int, max_steps: int = 2) -> list[str]:
    """기초 수치로부터 사칙연산을 조합하여 대상 수치에 도달하는 최단 수식들을 탐색."""
    from collections import deque
    queue = deque([([], start_vals)])
    visited = {}
    solutions = []
    
    while queue:
        path, current_pool = queue.popleft()
        if len(path) > max_steps:
            continue
            
        for (ka, va), (kb, vb) in permutations(current_pool.items(), 2):
            for sym, fn in OPS:
                if sym == "÷" and (vb == 0 or va % vb != 0):
                    continue
                if sym in "×÷" and vb == 1:
                    continue
                val = fn(va, vb)
                if val is None or val <= 0:
                    continue
                
                step_str = f"({ka}{sym}{kb})"
                new_pool = dict(current_pool)
                new_pool[step_str] = val
                
                if val == target:
                    solutions.append(step_str)
                elif val not in visited or len(path) + 1 < visited[val]:
                    visited[val] = len(path) + 1
                    queue.append((path + [step_str], new_pool))
                    
    return list(set(solutions))

# ────────────────────────────────────────────────
# 6. 메인 실행 및 독립 검증
# ────────────────────────────────────────────────
def main() -> None:
    dag.verify_all()
    
    print("\n## 독립 검산 경로 (모두 정확히 270에 도달)")
    checks = [
        ("洛書數六倍: 6 × 45", 6 * 45, 270),
        ("고리 등차급수: (首環6 + 末環54) × 9 ÷ 2", (6 + 54) * 9 // 2, 270),
        ("외주 × 5: 54 × 5", 54 * 5, 270),
        ("전체 칸 - 虛一: 271 - 1", 271 - 1, 270),
    ]
    for label, got, want in checks:
        assert got == want, label
        print(f"  [성립] {label} = {got}")
        
    print("\n## 사칙연산 경로 탐색 (BFS)")
    base_constants = {k: v for k, v in TEXT.items() if v not in (504, 500, 506)}
    for target in (504, 500, 506):
        paths = find_shortest_path(base_constants, target, max_steps=2)
        print(f"  [{target}] 도달 가능한 최단 수식 ({len(paths)}건 발견):")
        # 주요 수식 위주 출력
        for p in sorted(paths)[:5]:
            print(f"    {p} = {target}")
            
    print("\n## [Mermaid 계산 시각화 다이어그램]")
    print(generate_mermaid_code(dag))

if __name__ == "__main__":
    main()
