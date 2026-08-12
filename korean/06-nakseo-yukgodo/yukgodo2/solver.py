"""yukgodo2 — 고리별 연속값 재구 솔버 (六包一/逓加 계열).

원문이 직접 지지하는 산술 구조(逓加 고리 크기 6k, 來積法 사슬, 虛一)를
Z3 제약으로 부호화하고, 고리별 연속값 가설로 값 1..270을 배치한다.

- 고리 k는 연속 구간 3k(k−1)+1 … 3k(k+1)을 받는다
- 각 고리 안에서 값은 원주를 따라 연속적으로 진행한다
- 고리의 시작점과 회전 방향은 회전 대칭의 정규화이며 원문 지시가 아니다

결과는 output/ 에 저장한다 (solution.json, report.md, reconstruction.png).
"""

import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from z3 import Distinct, Int, Solver, Sum, sat

plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK JP",
    "DejaVu Sans",
    "Droid Sans Fallback",
]
plt.rcParams["font.family"] = "sans-serif"

RING_STEP = 6
LUOSHU_ORDER = 9
OUTPUT_DIR = Path(__file__).resolve().parent / "output"

# 리포트 언어: 이 리포는 한국어
LANG = "ko"


def build_arithmetic_solver():
    """원문의 수치 구조를 Z3 제약으로 재구성한다.

    逓加 경로:
        6, 12, 18, ..., 54
        6 * (1 + 2 + ... + 9) = 270

    六包一 급수 (《구수략》 곤책 교우사 판본 11쪽):
        1 + (6 + 12 + ... + 54) = 271  (중심 1을 6k 고리가 감쌈)
        虛一 뒤: 270칸

    來積法 경로:
        54 + 6 = 60
        60 / 6 = 10
        2 * 10 - 1 = 19
        19 - 1 = 18
        54 / 6 = 9
        (10 + 18) * 9 = 252
        252 + 19 = 271
    """

    solver = Solver()

    ring_count = Int("ring_count")
    outer_count = Int("outer_count")
    side_total = Int("side_total")
    side_count = Int("side_count")
    middle_span = Int("middle_span")
    adjacent_span = Int("adjacent_span")

    non_middle_count = Int("non_middle_count")
    geometric_total = Int("geometric_total")

    luoshu_sum = Int("luoshu_sum")
    occupied_count = Int("occupied_count")
    void_count = Int("void_count")

    ring_sizes = {
        k: Int(f"ring_size_{k}")
        for k in range(1, LUOSHU_ORDER + 1)
    }

    solver.add(ring_count > 0)

    # 枚外周五十四數
    solver.add(outer_count == 54)

    # 以筭法則係以六，逓加
    for k in range(1, LUOSHU_ORDER + 1):
        solver.add(ring_sizes[k] == RING_STEP * k)

    solver.add(ring_count == LUOSHU_ORDER)
    solver.add(ring_sizes[LUOSHU_ORDER] == outer_count)

    # 洛書數 = 1 + 2 + ... + 9
    solver.add(luoshu_sum == Sum(list(range(1, LUOSHU_ORDER + 1))))

    # 逓加洛書數六倍
    solver.add(
        occupied_count
        == Sum([ring_sizes[k] for k in range(1, LUOSHU_ORDER + 1)])
    )
    solver.add(occupied_count == RING_STEP * luoshu_sum)

    # 虛一
    solver.add(void_count == 1)
    solver.add(geometric_total == occupied_count + void_count)

    # 來積法: 外周添六
    solver.add(side_total == outer_count + 6)

    # 六歸之得一十
    solver.add(side_total == 6 * side_count)

    # 倍之得二十，減一為十九，為中觚數
    solver.add(middle_span == 2 * side_count - 1)

    # 去中觚 뒤 인접 최대 폭
    solver.add(adjacent_span == middle_span - 1)

    # 아홉 단계가 외주 수와 일치
    solver.add(outer_count == 6 * ring_count)

    # 전(田)식 넓이 관계의 재구
    solver.add(
        non_middle_count == (side_count + adjacent_span) * ring_count
    )

    # 中觚 복원
    solver.add(geometric_total == non_middle_count + middle_span)

    variables = {
        "ring_count": ring_count,
        "outer_count": outer_count,
        "side_total": side_total,
        "side_count": side_count,
        "middle_span": middle_span,
        "adjacent_span": adjacent_span,
        "non_middle_count": non_middle_count,
        "geometric_total": geometric_total,
        "luoshu_sum": luoshu_sum,
        "occupied_count": occupied_count,
        "void_count": void_count,
        "ring_sizes": ring_sizes,
    }

    return solver, variables


def solve_arithmetic():
    solver, variables = build_arithmetic_solver()

    if solver.check() != sat:
        raise RuntimeError("원문 산술이 모순이다.")

    model = solver.model()

    result = {
        name: model.evaluate(variable).as_long()
        for name, variable in variables.items()
        if name != "ring_sizes"
    }
    result["ring_sizes"] = {
        k: model.evaluate(variable).as_long()
        for k, variable in variables["ring_sizes"].items()
    }

    return result


def hex_distance(cell):
    q, r = cell
    return max(abs(q), abs(r), abs(q + r))


def build_hex_grid(radius):
    cells = []
    for q in range(-radius, radius + 1):
        for r in range(-radius, radius + 1):
            if hex_distance((q, r)) <= radius:
                cells.append((q, r))
    return cells


def ring_cells(radius):
    """한 고리의 셀을 원주 순서로 반환한다.

    시작점과 방향은 좌표 규약일 뿐 원문 지시로 주장하지 않는다.
    """

    if radius == 0:
        return [(0, 0)]

    directions = [
        (1, 0),
        (0, 1),
        (-1, 1),
        (-1, 0),
        (0, -1),
        (1, -1),
    ]

    q, r = 0, -radius
    result = []

    for dq, dr in directions:
        for _ in range(radius):
            result.append((q, r))
            q += dq
            r += dr

    assert len(result) == 6 * radius
    assert all(hex_distance(cell) == radius for cell in result)

    return result


def ring_value_range(ring):
    """고리별 연속값 가설: 고리 k는 다음 6k개의 연속 값을 받는다.

    고리 1: 1..6, 고리 2: 7..18, …, 고리 9: 217..270
    """

    previous_total = 3 * (ring - 1) * ring
    current_total = 3 * ring * (ring + 1)
    return previous_total + 1, current_total


def ring_sum(ring):
    """이 가설의 고리 k 합 = 18k³ + 3k (대척보수 가설의 813k와 다름)."""

    first, last = ring_value_range(ring)
    return 6 * ring * (first + last) // 2


def build_value_solver(arithmetic):
    """중심을 제외한 모든 칸을 채운다.

    원문 유래 제약:
        - 중심은 비움
        - 고리 k는 6k개 위치
        - 점유 위치 총수 = 270

    값 복원을 위한 재구 가설:
        - 값은 1..270
        - 고리 k는 대응하는 연속 구간을 받는다
        - 값은 각 고리의 원주를 따라 연속적으로 진행한다
    """

    radius = arithmetic["ring_count"]
    all_cells = build_hex_grid(radius)
    center = (0, 0)
    occupied_cells = [cell for cell in all_cells if cell != center]

    solver = Solver()
    values = {
        cell: Int(f"value_{cell[0]}_{cell[1]}") for cell in occupied_cells
    }

    for variable in values.values():
        solver.add(variable >= 1)
        solver.add(variable <= arithmetic["occupied_count"])

    solver.add(Distinct(list(values.values())))

    for ring in range(1, radius + 1):
        cells = ring_cells(ring)
        first_value, last_value = ring_value_range(ring)

        assert last_value - first_value + 1 == 6 * ring

        for cell in cells:
            solver.add(values[cell] >= first_value)
            solver.add(values[cell] <= last_value)

        # 강한 재구 가설: 값이 고리 원주를 따라 연속 진행
        for index, cell in enumerate(cells):
            solver.add(values[cell] == first_value + index)

    return solver, values, all_cells


def solve_values(arithmetic):
    solver, variables, all_cells = build_value_solver(arithmetic)

    if solver.check() != sat:
        raise RuntimeError("값 재구가 모순이다.")

    model = solver.model()
    values = {
        cell: model.evaluate(variable).as_long()
        for cell, variable in variables.items()
    }

    return values, all_cells


def verify_reconstruction(arithmetic, values, all_cells):
    radius = arithmetic["ring_count"]

    assert len(all_cells) == arithmetic["geometric_total"]
    assert len(values) == arithmetic["occupied_count"]
    assert (0, 0) not in values
    assert sorted(values.values()) == list(
        range(1, arithmetic["occupied_count"] + 1)
    )

    for ring in range(1, radius + 1):
        cells = ring_cells(ring)
        assert len(cells) == arithmetic["ring_sizes"][ring]

        actual_values = sorted(values[cell] for cell in cells)
        first_value, last_value = ring_value_range(ring)
        assert actual_values == list(range(first_value, last_value + 1))

        actual_sum = sum(values[cell] for cell in cells)
        assert actual_sum == ring_sum(ring)


def axial_to_xy(cell):
    q, r = cell
    x = math.sqrt(3) * (q + r / 2)
    y = 1.5 * r
    return x, y


def draw_reconstruction(arithmetic, values, all_cells, path):
    radius = arithmetic["ring_count"]

    fig, ax = plt.subplots(figsize=(16, 16))

    for cell in all_cells:
        x, y = axial_to_xy(cell)
        distance = hex_distance(cell)
        is_center = cell == (0, 0)
        is_outer = distance == radius

        patch = RegularPolygon(
            (x, y),
            numVertices=6,
            radius=0.98,
            orientation=0,
            facecolor="none",
            edgecolor="black",
            linewidth=1.6 if is_outer else 0.6,
        )
        ax.add_patch(patch)

        if is_center:
            ax.text(x, y, "虛", ha="center", va="center", fontsize=10)
        else:
            ax.text(
                x, y, str(values[cell]),
                ha="center", va="center", fontsize=5,
            )

    ax.set_aspect("equal")
    ax.autoscale_view()
    ax.axis("off")
    ax.set_title(
        "yukgodo2 — 고리별 연속값 재구\n"
        "六包一: 1+(6+12+…+54) = 271 | 虛一 뒤 270칸",
        fontsize=14,
    )

    plt.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def write_solution(arithmetic, values, path):
    data = {
        "hypothesis": "consecutive ring values (六包一/逓加 series)",
        "arithmetic": {
            name: (value if name != "ring_sizes" else
                   {str(k): v for k, v in value.items()})
            for name, value in arithmetic.items()
        },
        "ring_value_ranges": {
            str(k): list(ring_value_range(k))
            for k in range(1, arithmetic["ring_count"] + 1)
        },
        "ring_sums": {
            str(k): ring_sum(k)
            for k in range(1, arithmetic["ring_count"] + 1)
        },
        "values": {
            f"{q},{r}": value for (q, r), value in sorted(values.items())
        },
    }
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def write_report(arithmetic, path):
    lines = []
    a = arithmetic

    lines.append("# yukgodo2 — 고리별 연속값 재구 결과")
    lines.append("")
    lines.append("## 산술 사슬 (원문 지지분, Z3 검증)")
    lines.append("")
    lines.append("```")
    lines.append(
        f"逓加: 6 + 12 + … + 54 = {a['occupied_count']} "
        f"= 6 × {a['luoshu_sum']}"
    )
    lines.append(
        f"六包一 급수: 1 + (6 + 12 + … + 54) = {a['geometric_total']}"
    )
    lines.append(
        f"來積法: {a['outer_count']} + 6 = {a['side_total']}, "
        f"{a['side_total']} ÷ 6 = {a['side_count']}, "
        f"2 × {a['side_count']} − 1 = {a['middle_span']}"
    )
    lines.append(
        f"        ({a['side_count']} + {a['adjacent_span']}) "
        f"× {a['ring_count']} = {a['non_middle_count']}, "
        f"{a['non_middle_count']} + {a['middle_span']} "
        f"= {a['geometric_total']}"
    )
    lines.append(
        f"虛一: {a['geometric_total']} − {a['void_count']} "
        f"= {a['occupied_count']}"
    )
    lines.append("```")
    lines.append("")
    lines.append("## 고리별 배치 (재구 가설)")
    lines.append("")
    lines.append("| 고리 k | 칸 수 6k | 값 구간 | 고리합 18k³+3k |")
    lines.append("| ---: | ---: | --- | ---: |")
    for k in range(1, a["ring_count"] + 1):
        first, last = ring_value_range(k)
        lines.append(
            f"| {k} | {a['ring_sizes'][k]} | {first}..{last} "
            f"| {ring_sum(k)} |"
        )
    lines.append("")
    lines.append("## 검증")
    lines.append("")
    lines.append(
        f"- 격자 칸 수 = {a['geometric_total']} (중심 虛 1 + 점유 "
        f"{a['occupied_count']})"
    )
    lines.append("- 값 1..270이 정확히 한 번씩 배치됨")
    lines.append("- 각 고리의 값 집합이 대응 연속 구간과 정확히 일치함")
    lines.append("- 각 고리의 합이 18k³+3k와 정확히 일치함")
    lines.append("")
    lines.append("## 해석 경계")
    lines.append("")
    lines.append(
        "이 배치는 대척보수 가설(고리합 813k)과는 별개의 후보다. "
        "고리의 시작점·방향은 회전 대칭의 정규화이며, 원문이 이 값 배치를 "
        "직접 지시한다는 근거는 없다. 六包一 급수와의 대응은 칸 수 산법의 "
        "정합성을 보강할 뿐이다."
    )
    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    arithmetic = solve_arithmetic()
    values, all_cells = solve_values(arithmetic)
    verify_reconstruction(arithmetic, values, all_cells)

    write_solution(arithmetic, values, OUTPUT_DIR / "solution.json")
    write_report(arithmetic, OUTPUT_DIR / "report.md")
    draw_reconstruction(
        arithmetic, values, all_cells, OUTPUT_DIR / "reconstruction.png"
    )

    print(f"yukgodo2: solved and verified -> {OUTPUT_DIR}")
    print(
        f"  cells={arithmetic['geometric_total']} "
        f"(void {arithmetic['void_count']} + "
        f"occupied {arithmetic['occupied_count']})"
    )
    for k in range(1, arithmetic["ring_count"] + 1):
        first, last = ring_value_range(k)
        print(
            f"  ring {k}: {arithmetic['ring_sizes'][k]:2d} cells, "
            f"values {first}..{last}, sum {ring_sum(k)}"
        )


if __name__ == "__main__":
    main()
