#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify the 1890 condition of Nakseo Sagudo (사오도 각득 42 규칙).

The original annotation says:
    鄰星相兼五宫化 爲九宫每宫四子 各得四十二數
    此即河圖四五画 右旋者 互化則一千八百九十數

互化 (mutual transformation) total 1890 is the two-direction consistency
condition between the 5 wuxing classes and the 9 palaces:

    palace direction : 9 palaces x wuxing total 210 = 1890
    wuxing direction : 5 wuxing   x palace total 378 = 1890

Both directions coincide iff every palace sums to 42, i.e. exactly the
wuxing average (210 / 5 = 42). 45 x 42 = 1890 is the fully-paired form.
"""

from __future__ import annotations

PALACES = {
    "NW": [19, 2, 14, 7],
    "N": [19, 17, 2, 4],
    "NE": [17, 4, 12, 9],
    "W": [14, 7, 18, 3],
    "C": [5, 16, 10, 11],
    "E": [9, 12, 6, 15],
    "SW": [18, 3, 13, 8],
    "S": [13, 8, 20, 1],
    "SE": [6, 1, 20, 15],
}

WUXING_ORDER = ["수", "화", "목", "금", "토"]  # residues 1,2,3,4,0 mod 5


def wuxing(n: int) -> str:
    return WUXING_ORDER[n % 5 - 1] if n % 5 != 0 else "토"


def main() -> None:
    palace_sums = {name: sum(vals) for name, vals in PALACES.items()}
    palace_total = sum(palace_sums.values())

    # Wuxing totals over the ground set 1..20 (each number once): 210 total.
    wuxing_sum = {w: 0 for w in WUXING_ORDER}
    for n in range(1, 21):
        wuxing_sum[wuxing(n)] += n
    wuxing_total = sum(wuxing_sum.values())

    print("== 각 궁의 합 (각득 42) ==")
    for name, total in palace_sums.items():
        print(f"  {name}: {palace_sums[name]}  {PALACES[name]}")
    assert all(total == 42 for total in palace_sums.values())
    print(f"  9궁 중복 총합 = {palace_total}")

    print("\n== 오행별 합 ==")
    for w in WUXING_ORDER:
        print(f"  {w}: {wuxing_sum[w]}")
    print(f"  오행 총합 = {wuxing_total}, 평균 = {wuxing_total // 5}")

    print("\n== 互化 쌍방향 총수 ==")
    palace_direction = 9 * wuxing_total
    wuxing_direction = 5 * palace_total
    full_pairing = 45 * 42
    print(f"  궁 방향: 9 x {wuxing_total} = {palace_direction}")
    print(f"  오행 방향: 5 x {palace_total} = {wuxing_direction}")
    print(f"  완전 양자화: 45 x 42 = {full_pairing}")
    assert palace_direction == wuxing_direction == full_pairing == 1890

    print("\n== 실제 5x9 incidence 행렬 (다중도) ==")
    header = "      " + "  ".join(f"{name:>2}" for name in PALACES) + "   행합"
    print(header)
    incidence = {}
    for w in WUXING_ORDER:
        counts = [sum(1 for n in PALACES[name] if wuxing(n) == w) for name in PALACES]
        incidence[w] = counts
        print(f"  {w}: " + "  ".join(f"{c:>2}" for c in counts) + f"   {sum(counts)}")
    col_totals = [sum(incidence[w][i] for w in WUXING_ORDER) for i in range(9)]
    print("      " + "  ".join(f"{t:>2}" for t in col_totals) + "   (열합 = 각 궁의 4자)")

    print("\n== 궁별 서로 다른 오행의 평균 합 (대칭성 점검) ==")
    for name, vals in PALACES.items():
        distinct = sorted({wuxing(n) for n in vals}, key=WUXING_ORDER.index)
        subtotal = sum(wuxing_sum[w] for w in distinct)
        avg = subtotal / len(distinct)
        print(f"  {name}: 오행 {{{', '.join(distinct)}}} 합 {subtotal} / {len(distinct)} = {avg:g}")
        assert avg == 42

    print("\n모든 항등식 확인: 5 x 378 = 9 x 210 = 45 x 42 = 1890  OK")
    print("1890 조건: 각 궁의 합이 오행 평균 42와 일치할 때만 쌍방향 총수가 같아진다.")


if __name__ == "__main__":
    main()
