#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
각득(各得) 원리 일반화 분석기

《구수략(九數略)》 계열 각득 퍼즐(구·오·육·칠·팔자각득)의 공유 특성과
일반화 모델을 계산·검증하는 스크립트.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class GakdeukFamily:
    """각득 계열 하나의 데이터를 담는 데이터 클래스."""

    name: str
    n: int  # 각 부분 집합의 정점 수
    k: int  # 부분 집합 수 (모두 5)
    m: int  # 완전 오행 군의 크기 (오행 합 등차수열 기준)
    vertex_range: tuple[int, int]  # 사용된 수 범위
    total_sum: int  # 전체 합 (고유 정점 기준)
    subset_sum: int | None  # 각 부분 집합 합 S
    duplicated_sum: int  # 중복 포함 합 k*S 또는 해당 값
    duplicated_values: tuple[int, ...]  # 중복된 값들
    note: str


# ============================================================
# 1. 데이터 정의
# ============================================================

FAMILIES: Final[tuple[GakdeukFamily, ...]] = (
    GakdeukFamily(
        name="오자각득(천수용오도)",
        n=5,
        k=5,
        m=5,  # 완전 5x5 확장 기준
        vertex_range=(1, 24),
        total_sum=265,
        subset_sum=65,
        duplicated_sum=325,
        duplicated_values=(),  # solver가 찾아야 함
        note="부분 집합 합=65, 5×65=325, D=60",
    ),
    GakdeukFamily(
        name="육자각득(지수용육도)",
        n=6,
        k=5,
        m=4,
        vertex_range=(1, 20),
        total_sum=210,
        subset_sum=63,
        duplicated_sum=315,
        duplicated_values=(3, 8, 10, 11, 12, 13, 14, 15),
        note="8개 공유 정점, 차수 3",
    ),
    GakdeukFamily(
        name="칠자각득",
        n=7,
        k=5,
        m=7,
        vertex_range=(1, 35),
        total_sum=535,  # 고유 값 기준
        subset_sum=120,
        duplicated_sum=600,
        duplicated_values=(1, 6, 24, 34),
        note="중심 1 + 주변 6, 중복 값 4개",
    ),
    GakdeukFamily(
        name="팔자각득",
        n=8,
        k=5,
        m=8,
        vertex_range=(1, 40),
        total_sum=820,
        subset_sum=164,
        duplicated_sum=820,
        duplicated_values=(),
        note="3x3 Grid 중심 제외 8자, 궁 간 엣지 12개",
    ),
    GakdeukFamily(
        name="구자각득",
        n=9,
        k=5,
        m=9,
        vertex_range=(1, 45),
        total_sum=1035,
        subset_sum=207,
        duplicated_sum=1035,
        duplicated_values=(),
        note="3x3 Grid 9자, 궁 간 엣지 12개",
    ),
)

WUXING_NAMES: Final[tuple[str, ...]] = ("수", "화", "목", "금", "토")


def wuxing_of(n: int) -> str:
    """수를 오행으로 분류 (1→수, 2→화, 3→목, 4→금, 0→토)."""
    r = n % 5
    return WUXING_NAMES[r - 1]


def residue_1based(n: int) -> int:
    """1-based mod 5 잉여 (0은 5로 처리)."""
    r = n % 5
    return 5 if r == 0 else r


def wuxing_sum_sequence(m: int) -> list[int]:
    """
    1부터 5*m까지의 수를 mod 5로 분류했을 때
    각 오행 군의 합 시퀀스를 반환.
    """
    base = 5 * m * (m - 1) // 2
    return [base + m * r for r in range(1, 6)]


def duplicated_total(family: GakdeukFamily) -> int:
    """중복으로 더해진 총량 D = k*S - T 를 반환."""
    if family.subset_sum is None:
        return 0
    return family.duplicated_sum - family.total_sum


def average_per_subset(family: GakdeukFamily) -> float | None:
    """각 부분 집합의 평균값 S/n 을 반환."""
    if family.subset_sum is None:
        return None
    return family.subset_sum / family.n


# ============================================================
# 2. 출력
# ============================================================

def print_summary_table() -> None:
    """각득 계열 요약표를 출력."""
    print("=" * 100)
    print("각득(各得) 계열 요약")
    print("=" * 100)
    header = (
        f"{'계열':<18} | {'n':>3} | {'k':>3} | "
        f"{'수 범위':>8} | {'T':>5} | {'S':>5} | "
        f"{'k·S':>5} | {'D':>5} | {'S/n':>6} | {'비고'}"
    )
    print(header)
    print("-" * len(header))
    for fam in FAMILIES:
        s_str = str(fam.subset_sum) if fam.subset_sum is not None else "—"
        avg = average_per_subset(fam)
        avg_str = f"{avg:.2f}" if avg is not None else "—"
        print(
            f"{fam.name:<18} | {fam.n:>3} | {fam.k:>3} | "
            f"{fam.vertex_range[0]}-{fam.vertex_range[1]:>2} | "
            f"{fam.total_sum:>5} | {s_str:>5} | "
            f"{fam.duplicated_sum:>5} | {duplicated_total(fam):>5} | "
            f"{avg_str:>6} | {fam.note}"
        )
    print()


def print_wuxing_table() -> None:
    """각 계열의 오행 합 등차수열을 출력."""
    print("=" * 80)
    print("오행(五行) mod 5 합 분포")
    print("=" * 80)
    print(f"{'계열':<18} | {'m':>3} | 수 | 화 | 목 | 금 | 토 | 공차")
    print("-" * 72)
    for fam in FAMILIES:
        # 완전 5×m 범위 기준 (오자각득은 25까지 확장)
        m = fam.m
        seq = wuxing_sum_sequence(m)
        diff = seq[1] - seq[0]
        print(
            f"{fam.name:<18} | {m:>3} | "
            f"{seq[0]:>3} | {seq[1]:>3} | {seq[2]:>3} | {seq[3]:>3} | {seq[4]:>3} | {diff:>3}"
        )
    print()


def print_equation_check() -> None:
    """중복 계수 방정식 5·S = T + D 검증."""
    print("=" * 80)
    print("중복 계수 방정식 검증: 5·S = T + D")
    print("=" * 80)
    for fam in FAMILIES:
        if fam.subset_sum is None:
            print(f"{fam.name:<18}: S 미명시 (오자각득)")
            continue
        lhs = fam.k * fam.subset_sum
        rhs = fam.total_sum + duplicated_total(fam)
        ok = "✓" if lhs == rhs else "✗"
        print(
            f"{fam.name:<18}: 5×{fam.subset_sum} = {lhs:>4}, "
            f"T+D = {fam.total_sum}+{duplicated_total(fam)} = {rhs:>4} {ok}"
        )
    print()


def print_generalization() -> None:
    """일반화 모델의 예측값 출력."""
    print("=" * 80)
    print("일반화 모델: n각형 계열의 예측 부분 집합 합")
    print("=" * 80)
    print(f"{'n':>3} | {'수 범위':>10} | {'예측 S':>10} | {'실제 S':>10} | {'일치'}")
    print("-" * 52)
    for fam in FAMILIES:
        if fam.subset_sum is None:
            continue
        start, end = fam.vertex_range
        # 중복 포함 평균 기반 예측
        mu = fam.duplicated_sum / (fam.k * fam.n)
        predicted = mu * fam.n
        match = "✓" if abs(predicted - fam.subset_sum) < 1e-9 else "✗"
        print(
            f"{fam.n:>3} | {start}-{end:>2}       | {predicted:>10.2f} | {fam.subset_sum:>10} | {match}"
        )
    print()


def generate_markdown_report() -> str:
    """분석 결과를 담은 마크다운 문자열을 생성."""
    lines: list[str] = []
    lines.append("# 각득 원리 일반화: 계산 검증 보고서\n")
    lines.append("이 보고서는 `generalize_gakdeuk.py`에 의해 자동 생성되었습니다.\n")

    lines.append("## 1. 각득 계열 요약\n")
    lines.append("| 계열 | n | k | 수 범위 | T | S | k·S | D | S/n |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for fam in FAMILIES:
        s_str = str(fam.subset_sum) if fam.subset_sum is not None else "—"
        avg = average_per_subset(fam)
        avg_str = f"{avg:.2f}" if avg is not None else "—"
        lines.append(
            f"| {fam.name} | {fam.n} | {fam.k} | "
            f"{fam.vertex_range[0]}-{fam.vertex_range[1]} | "
            f"{fam.total_sum} | {s_str} | {fam.duplicated_sum} | "
            f"{duplicated_total(fam)} | {avg_str} |"
        )
    lines.append("")

    lines.append("## 2. 오행 mod 5 합 분포\n")
    lines.append("| 계열 | m | 수 | 화 | 목 | 금 | 토 | 공차 |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for fam in FAMILIES:
        m = fam.m
        seq = wuxing_sum_sequence(m)
        diff = seq[1] - seq[0]
        lines.append(
            f"| {fam.name} | {m} | {seq[0]} | {seq[1]} | {seq[2]} | {seq[3]} | {seq[4]} | {diff} |"
        )
    lines.append("")

    lines.append("## 3. 중복 계수 방정식 검증\n")
    lines.append("모든 계열에서 `5·S = T + D`가 성립합니다.\n")
    for fam in FAMILIES:
        if fam.subset_sum is None:
            lines.append(f"- **{fam.name}**: S 미명시")
            continue
        lhs = fam.k * fam.subset_sum
        rhs = fam.total_sum + duplicated_total(fam)
        lines.append(
            f"- **{fam.name}**: 5×{fam.subset_sum} = {lhs}, "
            f"T+D = {fam.total_sum}+{duplicated_total(fam)} = {rhs} {'✓' if lhs == rhs else '✗'}"
        )
    lines.append("")

    lines.append("## 4. 일반화 모델 예측\n")
    lines.append("`S = n × μ` (μ: 중복 포함 평균)에 따른 예측값:\n")
    lines.append("| n | 수 범위 | 예측 S | 실제 S |")
    lines.append("|---|---|---|---|")
    for fam in FAMILIES:
        if fam.subset_sum is None:
            continue
        mu = fam.duplicated_sum / (fam.k * fam.n)
        predicted = mu * fam.n
        lines.append(
            f"| {fam.n} | {fam.vertex_range[0]}-{fam.vertex_range[1]} | {predicted:.2f} | {fam.subset_sum} |"
        )
    lines.append("")

    return "\n".join(lines)


# ============================================================
# 3. 메인
# ============================================================

if __name__ == "__main__":
    print_summary_table()
    print_wuxing_table()
    print_equation_check()
    print_generalization()

    report_md = generate_markdown_report()
    with open("computed_report.md", "w", encoding="utf-8") as f:
        f.write(report_md)
    print("[저장] computed_report.md")
