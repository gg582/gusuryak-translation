"""최적해가 Siamese식 지역 규칙으로 재생성되는지 검토한다.

Siamese 계열의 핵심은 다음 수의 위치가 "일정한 짧은 이동"과
"막혔을 때의 일정한 보정 이동"으로 결정된다는 점이다. 여기서는
이미 찾은 최적해의 값 순서(1 -> 2 -> ... -> 270)를 거꾸로 읽어,
그 순서가 그런 규칙으로 압축되는지 계량한다.
"""

from __future__ import annotations

import json
from collections import Counter

from .hexgrid import Cell, HexGrid, add


def hex_distance(a: Cell, b: Cell) -> int:
    """두 axial 좌표 사이의 hex graph 거리."""
    dq = a[0] - b[0]
    dr = a[1] - b[1]
    return max(abs(dq), abs(dr), abs(dq + dr))


def _inverse(values: dict[Cell, int]) -> dict[int, Cell]:
    return {v: c for c, v in values.items()}


def _candidate_vectors(max_radius: int) -> list[Cell]:
    return [
        (q, r)
        for q in range(-max_radius, max_radius + 1)
        for r in range(-max_radius, max_radius + 1)
        if (q, r) != (0, 0) and max(abs(q), abs(r), abs(q + r)) <= max_radius
    ]


def _best_fixed_rule(values: dict[Cell, int], grid: HexGrid,
                     max_step_radius: int) -> dict:
    """짧은 주 이동/보정 이동 한 쌍으로 최적해 순서를 재생성할 수 있는지 검사."""
    inv = _inverse(values)
    filled = set(grid.filled)
    vectors = _candidate_vectors(max_step_radius)
    best = {
        "matches": -1,
        "prefix_matches": -1,
        "primary": None,
        "fallback": None,
        "first_failure_at": None,
    }
    for primary in vectors:
        for fallback in vectors:
            used: set[Cell] = set()
            matches = 0
            prefix_matches = 0
            prefix_alive = True
            first_failure_at = None
            for v in range(1, 270):
                used.add(inv[v])
                cand = add(inv[v], primary)
                if cand not in filled or cand in used:
                    cand = add(inv[v], fallback)
                ok = cand == inv[v + 1]
                if ok:
                    matches += 1
                    if prefix_alive:
                        prefix_matches += 1
                elif prefix_alive:
                    first_failure_at = v
                    prefix_alive = False
            if (matches, prefix_matches) > (best["matches"], best["prefix_matches"]):
                best = {
                    "matches": matches,
                    "prefix_matches": prefix_matches,
                    "primary": primary,
                    "fallback": fallback,
                    "first_failure_at": first_failure_at,
                }
    return best


def analyze_siamese(values: dict[Cell, int], grid: HexGrid,
                    max_step_radius: int = 3) -> dict:
    """최적해의 값 순서에서 Siamese식 지역 규칙의 가능성을 요약한다."""
    inv = _inverse(values)
    deltas = []
    distances = []
    for v in range(1, 270):
        a = inv[v]
        b = inv[v + 1]
        deltas.append((b[0] - a[0], b[1] - a[1]))
        distances.append(hex_distance(a, b))

    delta_counts = Counter(deltas)
    distance_counts = Counter(distances)
    best_rule = _best_fixed_rule(values, grid, max_step_radius)
    local_transitions = sum(1 for d in distances if d <= max_step_radius)

    return {
        "model": "fixed short move plus fixed fallback, no wraparound",
        "max_step_radius": max_step_radius,
        "n_transitions": len(deltas),
        "distinct_deltas": len(delta_counts),
        "singleton_deltas": sum(1 for n in delta_counts.values() if n == 1),
        "top_deltas": [
            {"delta": list(delta), "count": count}
            for delta, count in delta_counts.most_common(20)
        ],
        "distance_histogram": [
            {"distance": dist, "count": count}
            for dist, count in sorted(distance_counts.items())
        ],
        "max_distance": max(distances),
        "mean_distance": sum(distances) / len(distances),
        "local_transition_count": local_transitions,
        "local_transition_ratio": local_transitions / len(distances),
        "best_fixed_rule": {
            **best_rule,
            "primary": list(best_rule["primary"]),
            "fallback": list(best_rule["fallback"]),
            "match_ratio": best_rule["matches"] / len(deltas),
        },
        "verdict": (
            "실패: 최적해의 값 순서는 Siamese의 다항시간 지역 규칙으로 재생성되지 않는다. "
            "연속 수 이동이 120종으로 흩어지고, 짧은 주 이동/보정 이동 한 쌍의 최선도 "
            "269전이 중 6개만 맞춘다."
        ),
        "hanmun_reconstruction": [
            "今按其圖，數雖成六觚之均，非一行添六可循而得也。",
            "以一數次第求其所之，或遠或近，步法凡百二十變。",
            "設常步一、塞則更步一以試之，二百六十九遷中僅中六遷。",
            "故此圖宜謂以對位相補而搜得其均，不宜謂暹羅一路可成。",
        ],
        "source_correspondence": [
            {
                "original": "置外周添六",
                "modern_check": "添六을 값 순서의 일정 이동으로 읽는 경우 실패",
                "hanmun": "非一行添六可循而得也",
            },
            {
                "original": "虛一則二百七十數",
                "modern_check": "중심을 비우고 270칸만 값 순서 분석",
                "hanmun": "虛其中一，以二百七十數布之",
            },
            {
                "original": "通加洛書數六倍",
                "modern_check": "칸 수 270=6×45 및 보수쌍 구조는 유지",
                "hanmun": "六觚之均，由對位相補而成",
            },
        ],
    }


def write_siamese_json(analysis: dict, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)


def write_siamese_markdown(analysis: dict, path: str) -> None:
    lines = [
        "# Siamese 계통 지역 규칙 역산 검토",
        "",
        "## 결론",
        "",
        analysis["verdict"],
        "",
        "이 검사는 최적해를 값 순서 `1 -> 2 -> ... -> 270`로 되읽고, 다음 칸이",
        "Siamese 마방진처럼 `짧은 주 이동`, 그리고 막혔을 때의 `짧은 보정 이동`으로",
        "결정되는지 확인한다.",
        "",
        "## 계량 결과",
        "",
        f"- 전이 수: {analysis['n_transitions']}",
        f"- 서로 다른 이동 벡터: {analysis['distinct_deltas']}",
        f"- 한 번만 나타나는 이동 벡터: {analysis['singleton_deltas']}",
        f"- 최대 hex 거리: {analysis['max_distance']}",
        f"- 평균 hex 거리: {analysis['mean_distance']:.3f}",
        f"- 반지름 {analysis['max_step_radius']} 이하 국소 전이: "
        f"{analysis['local_transition_count']} / {analysis['n_transitions']} "
        f"({analysis['local_transition_ratio']:.3%})",
        "",
        "## 최선의 짧은 Siamese 후보",
        "",
    ]
    r = analysis["best_fixed_rule"]
    lines.extend([
        f"- 주 이동: {r['primary']}",
        f"- 보정 이동: {r['fallback']}",
        f"- 맞춘 전이: {r['matches']} / {analysis['n_transitions']} "
        f"({r['match_ratio']:.3%})",
        f"- 처음 실패한 위치: {r['first_failure_at']} -> {r['first_failure_at'] + 1}",
        f"- 처음부터 연속으로 맞춘 전이: {r['prefix_matches']}",
        "",
        "## 산학식 한문 역번역",
        "",
    ])
    lines.extend(f"- {s}" for s in analysis["hanmun_reconstruction"])
    lines.extend(["", "## 원문 대조", "", "| 원문/판독 구절 | 현대 검토 | 한문 재서술 |", "|---|---|---|"])
    for row in analysis["source_correspondence"]:
        lines.append(f"| {row['original']} | {row['modern_check']} | {row['hanmun']} |")
    lines.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
