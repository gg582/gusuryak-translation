#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
木與木相摩則然 — exhaustive test of the "Wood x Wood -> Fire" multiplicative reading

Hado Saodo source text
    一六水 二七火 三八木 四九金 五十土
    此圖水土相涵 金火相守 兩木相摩
    傳曰 木與木相摩則然 金與火相守則流   (quoting Zhuangzi, "External Things")

The hypothesis reads 相摩 as multiplication. It is run the same way over every
diagram in the Gusuryak magic-figure article. Labels follow the source:
    n ≡ 1 Water(水), 2 Fire(火), 3 Wood(木), 4 Metal(金), 0 Earth(土)  (mod 5)

Checks
  A. Complement pairs : can each palace (cell) be split into pairs with sum C,
                        and what phase types (水土 / 火金 / 木木 / other) are they?
  B. Product table    : what are 木·木, 金·火, 水·土 under multiplication mod 5?
  C. Wood·Wood in a palace : is the product of two Wood numbers in the same
                        palace Fire (mod 5), or a Fire number of that diagram after
                        reduction mod N or mod C (hit rate vs base rate)?
  D. Co-occurrence    : does a palace holding two or more Woods also hold a Fire?
  E. Pair products    : n·(C−n) mod 5 by pair type.

Run: python3 wood_product_audit.py  (no external dependencies)
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations

NAME = {1: "Wa", 2: "Fi", 3: "Wo", 4: "Me", 0: "Ea"}
HANJA = {1: "水", 2: "火", 3: "木", 4: "金", 0: "土"}
WOOD, FIRE = 3, 2


def ph(n: int) -> int:
    return n % 5


# ---------------------------------------------------------------------------
# Diagram data (tables of the Librewiki "magic figures/Gusuryak" article and repository data)
# ---------------------------------------------------------------------------

GRAPHS: list[dict] = [
    {
        "name": "Hado Saodo 河圖四五圖", "N": 20, "C": 21,
        "cells": {
            "top": [19, 2, 7, 14], "left": [13, 8, 18, 3], "centre": [5, 16, 11, 10],
            "right": [4, 17, 12, 9], "bottom": [15, 1, 6, 20],
        },
    },
    {
        "name": "Nakseo Sagudo 洛書四九圖", "N": 20, "C": 21,
        "cells": {
            "NW": [19, 2, 14, 7], "N": [19, 17, 2, 4], "NE": [17, 4, 12, 9],
            "W": [14, 7, 18, 3], "C": [5, 16, 10, 11], "E": [9, 12, 6, 15],
            "SW": [18, 3, 13, 8], "S": [13, 8, 20, 1], "SE": [6, 1, 20, 15],
        },
    },
    {
        "name": "Jungui Yongyukdo 重儀用六圖", "N": 16, "C": 17,
        "cells": {
            "top": [7, 16, 1, 6, 11, 10], "left": [7, 13, 11, 3, 9, 8],
            "bottom": [8, 2, 9, 12, 15, 5], "right": [6, 10, 4, 12, 14, 5],
        },
    },
    {
        "name": "Nakseo Ogudo 洛書五九圖", "N": 33, "C": 34,
        "cells": {
            "TL": [4, 20, 16, 23, 22], "TC": [9, 16, 14, 28, 18],
            "TR": [2, 14, 33, 21, 15], "ML": [3, 31, 19, 22, 10],
            "MC": [5, 19, 26, 18, 17], "MR": [7, 26, 25, 15, 12],
            "BL": [8, 29, 11, 10, 27], "BC": [1, 11, 24, 17, 32],
            "BR": [6, 24, 30, 12, 13],
        },
    },
    {
        "name": "Nakseo Chilgudo 洛書七九圖", "N": 63, "C": 64,
        "cells": {
            "TL": [4, 31, 43, 22, 60, 27, 37], "TC": [9, 15, 45, 36, 55, 10, 54],
            "TR": [2, 28, 29, 39, 62, 17, 47], "ML": [3, 30, 40, 26, 61, 16, 48],
            "MC": [5, 32, 41, 23, 59, 14, 50], "MR": [7, 34, 38, 24, 57, 20, 44],
            "BL": [8, 35, 49, 12, 56, 11, 53], "BC": [1, 52, 25, 19, 63, 18, 46],
            "BR": [6, 33, 42, 21, 58, 13, 51],
        },
    },
    {
        "name": "Nakseo Palgudo 洛書八九圖", "N": 40, "C": 41,
        "cells": {
            "(1,1)": [5, 11, 30, 36, 17, 1, 40, 24], "(1,2)": [30, 25, 4, 17, 33, 24, 18, 12],
            "(1,3)": [4, 32, 9, 33, 28, 12, 29, 13], "(2,1)": [1, 40, 24, 27, 23, 8, 26, 15],
            "(2,2)": [24, 18, 12, 23, 19, 15, 22, 31], "(2,3)": [12, 29, 13, 19, 16, 31, 10, 35],
            "(3,1)": [8, 26, 15, 37, 38, 7, 34, 3], "(3,2)": [15, 22, 31, 38, 20, 3, 14, 21],
            "(3,3)": [31, 10, 35, 20, 2, 21, 39, 6],
        },
    },
    {
        "name": "Beomsu Yongodo 範數用五圖", "N": 9, "C": 10,
        "cells": {"horizontal": [3, 7, 5, 4, 6], "vertical": [2, 8, 5, 1, 9]},
    },
    {
        "name": "Jangchaek Yongchildo 章策用七圖", "N": 19, "C": 20,
        "cells": {
            "vertical": [5, 18, 9, 7, 12, 2, 15], "diagonal1": [4, 10, 19, 7, 1, 14, 13],
            "diagonal2": [8, 6, 17, 7, 3, 11, 16],
        },
    },
    {
        "name": "Jungsang Yonggudo 重象用九圖 (source)", "N": 33, "C": 34,
        "cells": {
            "vertical": [20, 16, 23, 10, 9, 2, 29, 32, 6],
            "horizontal": [28, 5, 11, 25, 9, 7, 19, 31, 12],
            "diagonal1": [27, 15, 3, 24, 9, 30, 14, 21, 4],
            "diagonal2": [33, 1, 13, 22, 9, 18, 26, 17, 8],
        },
    },
    {
        "name": "Nakseo Gugudo 洛書九九圖 (reading)", "N": 81, "C": 91,
        "cells": {
            "八": [8, 16, 51, 56, 27, 64, 32, 40, 75], "一": [1, 69, 34, 77, 12, 53, 58, 45, 20],
            "六": [6, 38, 79, 14, 63, 22, 46, 30, 71], "三": [3, 11, 76, 60, 36, 19, 68, 52, 44],
            "五": [5, 29, 24, 62, 37, 70, 81, 48, 13], "七": [7, 74, 26, 55, 31, 42, 50, 66, 18],
            "四": [4, 15, 80, 61, 23, 28, 72, 39, 47], "九": [9, 49, 57, 17, 73, 41, 25, 65, 33],
            "二": [2, 54, 43, 67, 10, 59, 21, 78, 35],
        },
    },
    {
        "name": "Huchaek Yonggudo 侯策用九圖 (corrected)", "N": 72, "C": 73,
        "cells": {
            "r1c1": [5, 68, 32, 42, 41, 31, 67, 6], "r1c2": [3, 70, 34, 40, 39, 33, 69, 4],
            "r1c3": [72, 1, 36, 38, 37, 35, 71, 2], "r2c1": [20, 53, 19, 55, 54, 18, 11, 62],
            "r2c2": [16, 57, 21, 51, 52, 22, 58, 15], "r2c3": [14, 59, 23, 49, 50, 24, 60, 13],
            "r3c1": [17, 56, 26, 48, 47, 25, 61, 12], "r3c2": [9, 64, 28, 46, 45, 27, 63, 10],
            "r3c3": [7, 66, 30, 44, 43, 29, 65, 8],
        },
    },
    {
        "name": "Junggwae Yongpaldo 重卦用八圖", "N": 64, "C": 65,
        "cells": {
            "TL": [40, 20, 57, 9, 8, 56, 29, 41], "T": [14, 51, 19, 46, 35, 30, 62, 3],
            "TR": [45, 24, 52, 4, 13, 61, 25, 36], "L": [48, 32, 49, 16, 17, 33, 1, 64],
            "R": [37, 21, 60, 12, 5, 53, 28, 44], "BL": [38, 22, 59, 11, 6, 54, 27, 43],
            "B": [7, 58, 26, 39, 42, 23, 55, 10], "BR": [47, 31, 50, 2, 15, 63, 18, 34],
        },
    },
    {
        "name": "Gichaek Yongpaldo 奇策用八圖", "N": 24, "C": 25,
        "cells": {
            "top": [4, 9, 14, 23, 5, 8, 19, 18], "left": [8, 5, 15, 22, 3, 10, 20, 17],
            "right": [1, 12, 18, 19, 6, 7, 13, 24], "bottom": [7, 6, 17, 20, 2, 11, 16, 21],
        },
    },
    # 河圖七五圖 removed 2026-11-12: the print annotation is 七子各得一百二十六數
    # (5 x 126 = 630 = 1+...+35), and the former 'article table' (sum 120) reuses
    # 1, 6, 24, 34. The printed counters are too worn to transcribe.
    {
        "name": "Hado Palodo 河圖八五圖", "N": 40, "C": 41,
        "cells": {
            "top": [19, 34, 7, 39, 12, 24, 2, 27], "left": [18, 33, 8, 38, 13, 23, 3, 28],
            "centre": [16, 30, 5, 21, 15, 36, 10, 31], "right": [4, 22, 14, 37, 9, 32, 17, 29],
            "bottom": [1, 25, 11, 40, 6, 35, 20, 26],
        },
    },
    {
        "name": "Hado Guodo 河圖九五圖", "N": 45, "C": 46,
        "cells": {
            "top": [12, 44, 9, 19, 21, 29, 37, 2, 34], "left": [13, 43, 8, 18, 25, 26, 38, 3, 33],
            "centre": [15, 41, 6, 16, 23, 30, 40, 5, 31], "right": [14, 42, 7, 17, 24, 28, 39, 4, 32],
            "bottom": [11, 45, 10, 20, 22, 27, 36, 1, 35],
        },
    },
    {
        "name": "Cheonsu Yongodo 天數用五圖 (revised)", "N": 21, "C": 22,
        "cells": {
            "top": [5, 12, 2, 17, 18], "bottom": [1, 6, 16, 10, 21], "left": [3, 13, 11, 7, 20],
            "right": [4, 19, 14, 9, 8], "centre": [15, 2, 6, 20, 9],
        },
    },
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def pair_type(a: int, b: int) -> str:
    key = frozenset((ph(a), ph(b)))
    if key == frozenset((1, 0)):
        return "水土"
    if key == frozenset((2, 4)):
        return "火金"
    if key == frozenset((3,)):
        return "木木"
    return HANJA[ph(a)] + HANJA[ph(b)] if ph(a) <= ph(b) else HANJA[ph(b)] + HANJA[ph(a)]


def complement_pairs(cell: list[int], C: int) -> tuple[list[tuple[int, int]], list[int]]:
    rest = list(cell)
    pairs = []
    for v in sorted(set(cell)):
        if v in rest and (C - v) in rest and v != C - v:
            rest.remove(v)
            rest.remove(C - v)
            pairs.append((v, C - v))
    return pairs, rest


def residue_profile(cell: list[int]) -> str:
    c = Counter(ph(v) for v in cell)
    return " ".join(f"{NAME[r]}{c[r]}" for r in (1, 2, 3, 4, 0) if c[r])


def mul_table() -> str:
    lines = ["     " + "  ".join(NAME[c] for c in (1, 2, 3, 4, 0))]
    for a in (1, 2, 3, 4, 0):
        lines.append(f"  {NAME[a]}  " + "  ".join(NAME[(a * b) % 5] for b in (1, 2, 3, 4, 0)))
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

def audit(g: dict) -> dict:
    N, C, cells = g["N"], g["C"], g["cells"]
    values = sorted({v for cell in cells.values() for v in cell})
    fire_nums = {v for v in values if ph(v) == FIRE}

    sigma = {r: (C - r) % 5 for r in range(5)}
    print(f"\n=== {g['name']}  (1..{N}, complement sum C={C}, C mod 5={C % 5}) ===")
    print("  complement involution σ(r)=C−r:", ", ".join(f"{NAME[r]}↔{NAME[sigma[r]]}" for r in (1, 2, 3, 4, 0) if r <= sigma[r] or sigma[r] == 0 and r == 0))
    print(f"  partner of 木: {NAME[sigma[WOOD]]}{'  (Wood is self-complementary)' if sigma[WOOD] == WOOD else ''}")

    stats = Counter()
    wood_pairs_in_cells = []
    cohab = []
    full_decomp = 0
    for key, cell in cells.items():
        pairs, rest = complement_pairs(cell, C)
        types = [pair_type(a, b) for a, b in pairs]
        stats.update(types)
        if len(rest) <= 1:
            full_decomp += 1
        prod5 = 1
        for v in cell:
            prod5 = prod5 * v % 5
        woods = [v for v in cell if ph(v) == WOOD]
        has_fire = any(ph(v) == FIRE for v in cell)
        if len(woods) >= 2:
            cohab.append((key, has_fire))
        wood_pairs_in_cells += list(combinations(woods, 2))
        print(f"  {key:>10}: {residue_profile(cell):<22} pairs {' '.join(types) or '-':<14}"
              f" rest {rest or '-'}  ∏ mod5={NAME[prod5]}")

    print(f"  pair types: {dict(stats)}  / palaces fully split {full_decomp}/{len(cells)}")

    # C. Wood·Wood products inside a palace
    hit5 = sum(1 for a, b in wood_pairs_in_cells if ph(a * b) == FIRE)
    hitN = sum(1 for a, b in wood_pairs_in_cells if (a * b) % N in fire_nums)
    hitC = sum(1 for a, b in wood_pairs_in_cells if (a * b) % C in fire_nums)
    base = len(fire_nums) / len(values)
    n = len(wood_pairs_in_cells)
    if n:
        print(f"  Wood·Wood pairs in palaces: {n}; product mod5=Fire {hit5}/{n}, "
              f"(product mod N)∈Fire {hitN}/{n}, (product mod C)∈Fire {hitC}/{n}  [base rate {base:.2f}]")
    else:
        print("  no Wood·Wood pair in a palace")
    if cohab:
        print(f"  palaces with ≥2 Woods that also hold Fire: {sum(f for _, f in cohab)}/{len(cohab)} "
              f"({', '.join(k + ('+Fi' if f else '') for k, f in cohab)})")
    return {"name": g["name"], "C5": C % 5, "stats": stats, "n": n,
            "hit5": hit5, "hitN": hitN, "hitC": hitC, "base": base,
            "wood_self": sigma[WOOD] == WOOD, "cohab": cohab,
            "full": full_decomp, "cells": len(cells)}


def main() -> None:
    print("mod 5 multiplication table (row × column):")
    print(mul_table())
    print("\npowers of Wood: " + ", ".join(f"木^{k}={NAME[pow(3, k, 5)]}" for k in range(1, 5)))
    print("complement-pair product n·(C−n) mod 5 (C≡1): "
          + ", ".join(f"{HANJA[r]}{HANJA[(1 - r) % 5]}→{NAME[r * (1 - r) % 5]}" for r in (1, 2, 3)))

    results = [audit(g) for g in GRAPHS]

    print("\n\n=== Summary ===")
    print(f"{'diagram':<40}{'C mod5':>7}{'WoSelf':>7}{'WoPairs':>8}{'mod5Fi':>7}{'modNFi':>7}{'modCFi':>7}  pair types")
    for r in results:
        print(f"{r['name']:<40}{r['C5']:>7}{'O' if r['wood_self'] else '-':>7}{r['n']:>8}"
              f"{r['hit5']:>7}{r['hitN']:>7}{r['hitC']:>7}  {dict(r['stats'])}")
    tot = sum(r["n"] for r in results)
    print(f"\nWood·Wood pairs in palaces, total {tot}; with Fire product (mod 5): {sum(r['hit5'] for r in results)}")
    print(f"(product mod N) is a Fire number of the diagram: {sum(r['hitN'] for r in results)}, "
          f"(product mod C): {sum(r['hitC'] for r in results)}, "
          f"expected (base-rate weighted) ≈ {sum(r['n'] * r['base'] for r in results):.1f}")

    print("\nNakseo Yukgodo (1..270, C=271≡1): Wood is self-complementary — antipodal pairs v+v'=271 "
          "are only of types 水土, 火金, 木木 (holds without layout data).")


if __name__ == "__main__":
    main()
