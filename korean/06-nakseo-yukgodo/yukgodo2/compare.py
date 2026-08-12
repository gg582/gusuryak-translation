"""yukgodo2 — 두 재구 가설의 성질 비교.

상위 프로젝트의 대척보수 증인해(../output/solution.json)와 이 리포의
고리별 연속값 해(output/solution.json)를 같은 기하 지표로 측정하여
output/comparison.{json,md}에 저장한다.

지표 목표값(상위 프로젝트 README 기준):
    고리 k 합 813k, 섹터 6097/6098, 광선 1219/1220, 변 1355,
    축 2439(중심 제외 18칸), 꼭짓점 합 813(=3×271), 대척쌍 합 271.
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from yukgodo.hexgrid import HexGrid

RADIUS = 9
TARGETS = {
    "ring_sums": [813 * k for k in range(1, RADIUS + 1)],
    "wedge_sums": [6097.5] * 6,
    "ray_sums": [1219.5] * 6,
    "side_sums": [1355] * 6,
    "axis_sums": [2439] * 3,
    "corner_sum": 813,
}


def load_values(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        tuple(map(int, key.split(","))): value
        for key, value in data["values"].items()
    }


def metrics(grid, values):
    def total(cells):
        return sum(values[c] for c in cells if c in values)

    pair_sums = [values[a] + values[b] for a, b in grid.slots]

    return {
        "ring_sums": [total(grid.rings[k]) for k in range(1, RADIUS + 1)],
        "wedge_sums": [total(w) for w in grid.wedges],
        "ray_sums": [total(r) for r in grid.rays],
        "side_sums": [total(s) for s in grid.sides],
        "axis_sums": [total(a) for a in grid.axes],
        "corner_sum": total(grid.corners()),
        "antipodal_pair_sum_min": min(pair_sums),
        "antipodal_pair_sum_max": max(pair_sums),
        "antipodal_pairs_eq_271": sum(1 for s in pair_sums if s == 271),
    }


def max_deviation(series, target):
    return max(abs(s - target) for s in series)


def main():
    grid = HexGrid()

    antipodal = metrics(
        grid, load_values(HERE.parent / "output" / "solution.json")
    )
    consecutive = metrics(grid, load_values(HERE / "output" / "solution.json"))

    result = {"antipodal": antipodal, "consecutive": consecutive}
    (HERE / "output" / "comparison.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    lines = []
    lines.append("# 두 재구 가설의 기하 지표 비교")
    lines.append("")
    lines.append(
        "대척보수 증인해(상위 `output/solution.json`, 시드 1715)와 "
        "고리별 연속값 해(`yukgodo2/output/solution.json`)를 같은 "
        "격자 지표로 측정했다."
    )
    lines.append("")

    lines.append("## 고리합 (목표 813k)")
    lines.append("")
    lines.append("| 고리 k | 목표 813k | 대척보수 해 | 연속값 해 (18k³+3k) |")
    lines.append("| ---: | ---: | ---: | ---: |")
    for k in range(1, RADIUS + 1):
        lines.append(
            f"| {k} | {813 * k} | {antipodal['ring_sums'][k - 1]} "
            f"| {consecutive['ring_sums'][k - 1]} |"
        )
    lines.append("")

    def simple_section(title, key, target):
        lines.append(f"## {title} (목표 {target})")
        lines.append("")
        lines.append("| 지표 | 대척보수 해 | 연속값 해 |")
        lines.append("| --- | --- | --- |")
        lines.append(
            f"| 값 | {antipodal[key]} | {consecutive[key]} |"
        )
        lines.append(
            f"| 최대 편차 | {max_deviation(antipodal[key], target)} "
            f"| {max_deviation(consecutive[key], target)} |"
        )
        lines.append("")

    simple_section("섹터(觚) 합", "wedge_sums", 6097.5)
    simple_section("광선 합", "ray_sums", 1219.5)
    simple_section("외주 변 합", "side_sums", 1355)
    simple_section("축(中觚 계열) 합", "axis_sums", 2439)

    lines.append("## 대척쌍·꼭짓점")
    lines.append("")
    lines.append("| 지표 | 대척보수 해 | 연속값 해 |")
    lines.append("| --- | ---: | ---: |")
    lines.append(
        f"| 대척쌍 합 = 271 인 쌍 수 (135 중) "
        f"| {antipodal['antipodal_pairs_eq_271']} "
        f"| {consecutive['antipodal_pairs_eq_271']} |"
    )
    lines.append(
        f"| 대척쌍 합 최소–최대 "
        f"| {antipodal['antipodal_pair_sum_min']}–{antipodal['antipodal_pair_sum_max']} "
        f"| {consecutive['antipodal_pair_sum_min']}–{consecutive['antipodal_pair_sum_max']} |"
    )
    lines.append(
        f"| 꼭짓점 합 (구조적 목표 813) "
        f"| {antipodal['corner_sum']} | {consecutive['corner_sum']} |"
    )
    lines.append("")
    lines.append(
        "연속값 해의 지표는 시작점·회전 방향의 정규화 선택에 따라 "
        "회전 동역학적으로만 정해진다(회전하면 섹터·광선·변 값은 순열된다). "
        "어느 쪽도 원문이 직접 지시한 배치라는 뜻은 아니다."
    )
    lines.append("")

    (HERE / "output" / "comparison.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )

    print(f"comparison written -> {HERE / 'output'}")
    print(f"  antipodal   : rings all 813k = "
          f"{all(s == 813 * (i + 1) for i, s in enumerate(antipodal['ring_sums']))}, "
          f"pairs=271: {antipodal['antipodal_pairs_eq_271']}/135")
    print(f"  consecutive : pairs=271: {consecutive['antipodal_pairs_eq_271']}/135, "
          f"corner sum {consecutive['corner_sum']}")


if __name__ == "__main__":
    main()
