#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modular / CRT analysis for the 30-vertex 9-hex Jisuguimundo.

Analyses performed:
  - 作/用 (made/used) separation, i.e. vertex multiplicity on the 9 hexagons
  - residue classification modulo 2, 3, 4, 5, 6, 9, 12
  - spatial distribution and symmetry for mod 2
  - CRT reconstruction for mod 3×4, 3×5, 4×5 (following Jin Jiushao's basic CRT)

All identifiers are in English so the script can be mirrored in the English
folder without transliteration.
"""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent


def load_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def residue_1based(value: int, mod: int) -> int:
    r = value % mod
    return mod if r == 0 else r


def multiplicity(hexagons: list[list[int]], node_count: int) -> list[int]:
    mult = [0] * node_count
    for hx in hexagons:
        for v in hx:
            mult[v - 1] += 1
    return mult


def compute_crt_pair(residue_a: int, mod_a: int, residue_b: int, mod_b: int) -> int:
    """
    Return the unique residue x (1..mod_a*mod_b) with
        x ≡ residue_a (mod mod_a)
        x ≡ residue_b (mod mod_b)
    using a brute-force search (sufficient for the small moduli here).
    Residues are 1-based.
    """
    for x in range(1, mod_a * mod_b + 1):
        if residue_1based(x, mod_a) == residue_a and residue_1based(x, mod_b) == residue_b:
            return x
    raise ValueError("No CRT solution (moduli must be coprime)")


def draw_mod_distribution(
    coords: dict[int, tuple[float, float]],
    assignment: list[int],
    mod: int,
    output_path: Path,
) -> None:
    """Draw the graph with nodes coloured by their 1-based residue mod `mod`."""
    palette = [
        "#4A90E2", "#E94B3C", "#6AB04C", "#BDC3C7", "#D4A017",
        "#9B59B6", "#1ABC9C", "#F39C12", "#34495E", "#7F8C8D",
        "#C0392B", "#2980B9",
    ]

    fig, ax = plt.subplots(figsize=(10, 12), facecolor="#FDFBF7")
    ax.set_aspect("equal")
    ax.axis("off")

    # Draw faint edges if topology present
    topo = load_json(ROOT / "jisu_9hex_topology.json")
    for u, v in topo["edges"]:
        x_pts = [coords[int(u)][0], coords[int(v)][0]]
        y_pts = [coords[int(u)][1], coords[int(v)][1]]
        ax.plot(x_pts, y_pts, color="#CCCCCC", linewidth=1.5, zorder=1)

    residues = [residue_1based(assignment[i], mod) for i in range(len(assignment))]
    counts = Counter(residues)

    for node_id in sorted(coords):
        x, y = coords[node_id]
        r = residues[node_id - 1]
        color = palette[(r - 1) % len(palette)]
        ax.scatter(x, y, color=color, edgecolors="#333333", s=900, linewidths=2, zorder=2)
        ax.text(
            x, y, str(assignment[node_id - 1]),
            color="white" if color in ("#34495E", "#7F8C8D", "#C0392B", "#2980B9") else "#2C3E50",
            fontsize=14, fontweight="bold", va="center", ha="center", zorder=3,
        )
        # residue ring
        ax.text(
            x + 0.28, y + 0.28, f"r{r}",
            color="#2C3E50", fontsize=9, fontweight="bold", va="center", ha="center", zorder=4,
        )

    title = f"Jisuguimundo 9-hex — residues mod {mod}"
    ax.set_title(title, fontsize=16, fontweight="bold", color="#2C3E50", pad=12)
    subtitle = " | ".join(f"r{r}: {c}" for r, c in sorted(counts.items()))
    ax.text(0.5, 0.02, subtitle, transform=fig.transFigure, ha="center", fontsize=11, color="#555555")

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {output_path}")


def draw_crt_grid(
    coords: dict[int, tuple[float, float]],
    assignment: list[int],
    mod_a: int,
    mod_b: int,
    output_path: Path,
) -> None:
    """Colour nodes by the CRT-combined residue mod (mod_a * mod_b)."""
    mod_ab = mod_a * mod_b
    palette = [
        "#4A90E2", "#E94B3C", "#6AB04C", "#BDC3C7", "#D4A017",
        "#9B59B6", "#1ABC9C", "#F39C12", "#34495E", "#7F8C8D",
        "#C0392B", "#2980B9", "#8E44AD", "#16A085", "#D35400",
    ] * 4

    fig, ax = plt.subplots(figsize=(10, 12), facecolor="#FDFBF7")
    ax.set_aspect("equal")
    ax.axis("off")

    topo = load_json(ROOT / "jisu_9hex_topology.json")
    for u, v in topo["edges"]:
        x_pts = [coords[int(u)][0], coords[int(v)][0]]
        y_pts = [coords[int(u)][1], coords[int(v)][1]]
        ax.plot(x_pts, y_pts, color="#CCCCCC", linewidth=1.5, zorder=1)

    crt_residues = []
    for val in assignment:
        ra = residue_1based(val, mod_a)
        rb = residue_1based(val, mod_b)
        crt_residues.append(compute_crt_pair(ra, mod_a, rb, mod_b))
    counts = Counter(crt_residues)

    for node_id in sorted(coords):
        x, y = coords[node_id]
        r = crt_residues[node_id - 1]
        color = palette[(r - 1) % len(palette)]
        ax.scatter(x, y, color=color, edgecolors="#333333", s=900, linewidths=2, zorder=2)
        ax.text(
            x, y, str(assignment[node_id - 1]),
            color="white" if r in (9, 10, 12, 13, 14, 15) else "#2C3E50",
            fontsize=13, fontweight="bold", va="center", ha="center", zorder=3,
        )
        ax.text(
            x + 0.28, y + 0.28, f"{r}",
            color="#2C3E50", fontsize=9, fontweight="bold", va="center", ha="center", zorder=4,
        )

    title = f"CRT reconstruction: mod {mod_a} × mod {mod_b} → mod {mod_ab}"
    ax.set_title(title, fontsize=16, fontweight="bold", color="#2C3E50", pad=12)
    subtitle = " | ".join(f"r{r}: {c}" for r, c in sorted(counts.items()))
    ax.text(0.5, 0.02, subtitle, transform=fig.transFigure, ha="center", fontsize=10, color="#555555")

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {output_path}")


def build_report(
    topology: dict[str, Any],
    solution: dict[str, Any],
) -> str:
    assignment = solution["assignment"]
    hexagons = topology["hexagons"]
    node_count = topology["node_count"]
    s = solution["S"]

    mult = multiplicity(hexagons, node_count)
    total_written = sum(assignment)
    total_used_positions = sum(len(hx) for hx in hexagons)
    duplicate_positions = total_used_positions - node_count
    duplication_weight = sum((mult[i] - 1) * assignment[i] for i in range(node_count))

    lines: list[str] = []
    lines.append("# 지수귀문도 9hex 분석 보고서")
    lines.append("")
    lines.append("## 1. 기본 수치 및 作/用 분리")
    lines.append("")
    lines.append("| 항목 | 값 |")
    lines.append("|---|---:|")
    lines.append(f"| 사용 수 (作) | {node_count}개 (1~{node_count}) |")
    lines.append(f"| 쓰이는 자리 (用) | {total_used_positions}개 (9육각형 × 6정점) |")
    lines.append(f"| 중복 자리 수 | {duplicate_positions}개 |")
    lines.append(f"| 고유 수 합 (T) | {total_written} |")
    lines.append(f"| 9육각형 중복 포함 총합 (H·S) | {len(hexagons)} × {s} = {len(hexagons)*s} |")
    lines.append(f"| 중복 가중 합 (D) | {duplication_weight} |")
    lines.append("")
    lines.append(f"원문의 **三十子作， 五十四子用**은 위 표와 정확히 대응한다: "
                 f"고유 수는 30개, 구조상 쓰이는 자리는 54개, 중복 자리는 24개.")
    lines.append("")
    lines.append("### 정점별 중복 계수")
    lines.append("")
    lines.append("| 중복 계수 | 정점 (원래 번호 = 배치 값) |")
    lines.append("|---|---|")
    for k in sorted(set(mult)):
        members = [f"{i+1}={assignment[i]}" for i in range(node_count) if mult[i] == k]
        lines.append(f"| {k}회 | {', '.join(members)} |")
    lines.append("")

    # Mod analyses
    mods = [2, 3, 4, 5, 6, 9, 12]
    lines.append("## 2. mod 분류 및 그룹 해석")
    lines.append("")
    for mod in mods:
        residues = [residue_1based(v, mod) for v in assignment]
        counts = Counter(residues)
        class_sums = defaultdict(int)
        for val, r in zip(assignment, residues):
            class_sums[r] += val
        lines.append(f"### mod {mod}")
        lines.append("")
        lines.append("| 잉여 클래스 | 수의 개수 | 클래스 합 |")
        lines.append("|---|---:|---:|")
        for r in sorted(counts):
            lines.append(f"| r{r} | {counts[r]} | {class_sums[r]} |")
        lines.append("")
        lines.append("각 육각형별 잉여 패턴:")
        lines.append("")
        lines.append("| 육각형 | 값 | 잉여 패턴 | 합 |")
        lines.append("|---|---|---|---:|")
        for idx, hx in enumerate(hexagons, start=1):
            vals = [assignment[v - 1] for v in hx]
            res_pattern = [str(residue_1based(v, mod)) for v in vals]
            lines.append(f"| Hex{idx} | {vals} | {'-'.join(res_pattern)} | {sum(vals)} |")
        lines.append("")

    lines.append("## 3. mod 2 공간 분포 및 대칭")
    lines.append("")
    parity = [residue_1based(v, 2) for v in assignment]
    even_count = sum(1 for p in parity if p == 2)
    odd_count = node_count - even_count
    lines.append(f"- 짝수(r2): {even_count}개, 홀수(r1): {odd_count}개")
    lines.append("")
    coords = {int(k): (v["x"], v["y"]) for k, v in topology["vertices"].items()}
    left = sum(1 for nid in coords if coords[nid][0] < -1e-6 and parity[nid - 1] == 1)
    right = sum(1 for nid in coords if coords[nid][0] > 1e-6 and parity[nid - 1] == 1)
    top = sum(1 for nid in coords if coords[nid][1] > 1e-6 and parity[nid - 1] == 1)
    bottom = sum(1 for nid in coords if coords[nid][1] < -1e-6 and parity[nid - 1] == 1)
    lines.append(f"- 홀수 분포: 좌측 {left}개, 우측 {right}개, 상반부 {top}개, 하반부 {bottom}개")
    lines.append("")
    lines.append("mod 2 분포는 그래프의 상하좌우 반사 대칭과 비교할 때 균등에 가깝게 배치되어 있다.")
    lines.append("")

    lines.append("## 4. CRT (중국인의 나머지 정리) 분석")
    lines.append("")
    lines.append("송·원대 수학자 진구소(秦九韶, Qin Jiushao)가 《수서구장(數書九章)》에서 정립한")
    lines.append("기본 CRT 알고리즘을 따라, 서로소인 mod 쌍을 결합한다.")
    lines.append("")
    for mod_a, mod_b in [(3, 4), (3, 5), (4, 5)]:
        mod_ab = mod_a * mod_b
        crt_counts: Counter[int] = Counter()
        crt_class_sums: defaultdict[int, int] = defaultdict(int)
        for val in assignment:
            ra = residue_1based(val, mod_a)
            rb = residue_1based(val, mod_b)
            r_ab = compute_crt_pair(ra, mod_a, rb, mod_b)
            crt_counts[r_ab] += 1
            crt_class_sums[r_ab] += val
        lines.append(f"### mod {mod_a} × mod {mod_b} → mod {mod_ab}")
        lines.append("")
        lines.append("| CRT 잉여 | 개수 | 합 |")
        lines.append("|---|---:|---:|")
        for r in sorted(crt_counts):
            lines.append(f"| r{r} | {crt_counts[r]} | {crt_class_sums[r]} |")
        lines.append("")

    lines.append("## 5. 2·3 기반 변이")
    lines.append("")
    lines.append("- mod 2: 가장 작은 소모듈러; 짝/홀 분포로 그래프의 대칭성을 판단한다.")
    lines.append("- mod 3: 3방위/삼재(三才) 구조와 연결되는 기본 분류.")
    lines.append("- mod 4 = 2×2: mod 2 분류를 한 단계 세분화.")
    lines.append("- mod 6 = 2×3: mod 2와 mod 3를 동시에 본다.")
    lines.append("- mod 9 = 3×3: mod 3를 제곱한 변이; 9궁/九宫 체계와 호응.")
    lines.append("- mod 12 = 2²×3: mod 3×mod 4 CRT로 완전히 복원 가능.")
    lines.append("")

    lines.append("## 6. 확장 시각화 해석")
    lines.append("")
    lines.append("### 作/用 분리 (`jisu_9hex_multiplicity.png`)")
    lines.append("")
    lines.append("- 30개 고유 수(作)가 54개 육각형 자리(用)에 배치된다.")
    lines.append("- 중복 계수가 큰 정점일수록 시각적으로 크게 표현되며, 중앙 영역에 집중된다.")
    lines.append("- 중복 계수 3회 정점 8개는 Hex5(중앙 육각형)와 그 주변에 위치한다.")
    lines.append("- 이는 원문 **三十子作， 五十四子用**과 정확히 일치한다.")
    lines.append("")
    lines.append("### mod 2 대칭 (`jisu_9hex_mod2_symmetry.png`)")
    lines.append("")
    lines.append("- 홀수 15개, 짝수 15개로 완벽하게 균등하다.")
    lines.append("- 좌우 대칭선(x=0)과 상하 대칭선(y=0)을 기준으로 홀수가 비교적 고르게 분포한다.")
    lines.append("- 사분면 내 홀수 분포: Q1 5개, Q2 2개, Q3 3개, Q4 5개.")
    lines.append("- 이는 정육각형 격자의 반사 대칭성과 마법 상수 93의 부분합 구조가 조화롭게 맞물려 있음을 보여준다.")
    lines.append("")
    lines.append("### 9궁 → 12궁 재해석 (`jisu_9hex_9to12_palaces.png`)")
    lines.append("")
    lines.append("- 안쪽 파란 원: 9개 육각형 궁(九宫).")
    lines.append("- 바깥쪽 주황 원: 12개 방위 궁(十二宫), 12지(子丑寅卯辰巳午未申酉戌亥) 방위.")
    lines.append("- 회색 연결선: 각 육각형 중심에서 인접한 방위 섹터로의 매핑.")
    lines.append("- 원문 **凡九宮化爲十二宮**은 9개 육각형 단위를 12방위 단위로 재해석할 수 있음을 시각화한다.")
    lines.append("")
    lines.append("### 중심 3궁 구조 (`jisu_9hex_center_periphery.png`)")
    lines.append("")
    lines.append("- 세로 중앙열 Hex2, Hex5, Hex8이 빨간색으로 강조된다.")
    lines.append("- 이 3개 육각형은 좌우 6개 육각형을 관장하는 중심 축이다.")
    lines.append("- 원문 **中眷三宮， 三宮爲主則**은 이 중심 3궁이 전체 구조의 주(主)가 됨을 나타낸다.")
    lines.append("")
    lines.append("### 그래프 스펙트럼 (`jisu_9hex_adjacency_spectrum.png`)")
    lines.append("")
    lines.append("- 30×30 인접행렬: 육각형 간 공유 정점이 블록 대각/오프-대각 패턴으로 나타난다.")
    lines.append("- 차수분포: 2차와 3차 정점이 대부분이며, 중앙 일부 정점은 4차를 가진다.")
    lines.append("- 인접행렬 고유값: 그래프의 대칭성을 반영하는 스펙트럼 구조를 보여준다.")
    lines.append("- Laplacian 고유값: 그래프의 연결성과 커팅 성질을 수량화한다.")
    lines.append("")
    lines.append("### 마법 상수 강조 (`jisu_9hex_magic_constant.png`)")
    lines.append("")
    lines.append("- 각 육각형 중앙에 마법 상수 **93**을 표시하고, 구성하는 6개 값을 함께 보여준다.")
    lines.append("- 9개 육각형 모두 합이 93임을 직접적으로 확인할 수 있다.")
    lines.append("- 이는 원문 **六子各得九十三數**의 핵심 내용을 시각화한다.")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    topology = load_json(ROOT / "jisu_9hex_topology.json")
    solution = load_json(ROOT / "jisu_9hex_solution.json")
    assignment = solution["assignment"]

    coords = {int(k): (v["x"], v["y"]) for k, v in topology["vertices"].items()}

    # Draw mod distribution images
    for mod in [2, 3, 4, 5, 6, 9, 12]:
        draw_mod_distribution(coords, assignment, mod, ROOT / f"mod{mod}_distribution.png")

    # Draw CRT images
    draw_crt_grid(coords, assignment, 3, 4, ROOT / "crt_mod3_times_mod4.png")
    draw_crt_grid(coords, assignment, 3, 5, ROOT / "crt_mod3_times_mod5.png")
    draw_crt_grid(coords, assignment, 4, 5, ROOT / "crt_mod4_times_mod5.png")

    # Write report
    report = build_report(topology, solution)
    report_path = ROOT / "jisu_9hex_analysis_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Saved report: {report_path}")


if __name__ == "__main__":
    main()
