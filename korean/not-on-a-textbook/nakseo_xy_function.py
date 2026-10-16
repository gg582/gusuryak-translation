#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Not-on-a-textbook experiment: the map x -> y hidden in the names of the
Gusuryak "nakseo" family.

Every diagram in the nakseo (洛書) family except Nakseo Yukgodo
(洛書六觚圖) is named 낙서xy도 (Nakseo X-gudo), and the two name digits
x and y literally enter the arithmetic:

  - x = the number of cells each group obtains (子): it appears in the
    fair-share rule  T = x * (N + 1) / 2  for the common group sum T.
  - y = the number of groups: it appears in the slot count 用 = x * y.

This script verifies the identities against the observed family, prints
the domain / image of the map x -> y, and probes which (x, y) extensions
pass the arithmetic gate for the exact-partition subclass (N = x * y).
"""

from __future__ import annotations

# Observed family (numbers verified against the diagrams):
#   name, x (cells per group), y (number of groups), N (作, distinct
#   numbers used), slots (用, multiplicity-counted positions),
#   group_sum (the common partial sum, 各得).
MEMBERS = [
    ("Nakseo Sagudo (洛書四九圖)",    4, 9, 20, 36,  42),
    ("Nakseo Ogudo (洛書五九圖)",     5, 9, 33, 45,  85),
    ("Nakseo Chilgudo (洛書七九圖)",  7, 9, 63, 63, 224),
    ("Nakseo Palgudo (洛書八九圖)",   8, 9, 40, 72, 164),
    ("Nakseo Gugudo (洛書九九圖)",    9, 9, 81, 81, 369),
]

# Nakseo Yukgodo (洛書六觚圖) is excluded: its name digit 6 is the
# number of sides of the hexagon, not a participant in the x/y naming
# scheme used by the other five diagrams.


def verify_identities() -> None:
    """(a) slots == x * y  and  (b) group_sum == x * (N + 1) / 2."""
    for name, x, y, n, slots, group_sum in MEMBERS:
        assert slots == x * y, (name, slots, x * y)
        expected_sum = x * (n + 1) // 2
        assert x * (n + 1) % 2 == 0, (name, "fair share not integral")
        assert group_sum == expected_sum, (name, group_sum, expected_sum)


def report_map() -> None:
    """(c) domain, observed y values, image, and the constant hypothesis."""
    xs = sorted({x for _, x, *_ in MEMBERS})
    ys = sorted({y for _, _, y, *_ in MEMBERS})
    image = sorted({y for _, _, y, *_ in MEMBERS})
    print("map x -> y from the observed nakseo family:")
    print(f"  domain X       = {xs}")
    print(f"  observed y     = {ys}")
    print(f"  image  f(X)    = {image}")
    constant_hypothesis = all(y == 9 for _, _, y, *_ in MEMBERS)
    print(f"  constant-function hypothesis (y == 9 for all members): "
          f"{constant_hypothesis}")


def probe_extensions() -> list[tuple[int, int, int]]:
    """(d) exact-partition subclass: N = x * y, so T = x * (x*y + 1) / 2.

    Enumerate x in 1..12 and y in 3..12; keep the pairs for which T is an
    integer (the minimal arithmetic gate for a fair-share partition).
    Returns the feasible (x, y, T) triples.
    """
    feasible = []
    for x in range(1, 13):
        for y in range(3, 13):
            n = x * y
            numerator = x * (n + 1)
            if numerator % 2 == 0:
                feasible.append((x, y, numerator // 2))
    return feasible


def print_feasibility_grid(feasible: list[tuple[int, int, int]]) -> None:
    feasible_set = {(x, y) for x, y, _ in feasible}
    observed_set = {(x, y) for _, x, y, *_ in MEMBERS}
    print("\nextension probe (exact-partition subclass N = x*y):")
    print("  grid of y for each x ('.' = infeasible, 'y' = feasible,")
    print("  'F' = feasible but historically absent, '*' = observed member)")
    header = "  x\\y |" + "".join(f"{y:>4}" for y in range(3, 13))
    print(header)
    print("  ----+" + "----" * 10)
    for x in range(1, 13):
        row = f"  {x:>3} |"
        for y in range(3, 13):
            if (x, y) in observed_set:
                mark = "*"
            elif (x, y) in feasible_set:
                mark = "F"
            else:
                mark = "."
            row += f"{mark:>4}"
        print(row)
    gap = sorted({y for x, y in feasible_set if x == 6})
    non9 = [(x, y) for x, y in feasible_set if y != 9]
    print(f"\n  x = 6 (a hypothetical Nakseo Yuk-gudo 洛書六九圖) passes the "
          f"gate at y = {gap}, yet is historically absent.")
    print(f"  pairs with y != 9 that also pass the gate: {len(non9)} of "
          f"{len(feasible_set)} feasible pairs")
    print("  -> the name-based codomain {9} is NOT forced by arithmetic.")


def report_duplication() -> None:
    """(e) duplication slots D = x*y - N per member."""
    print("\nduplication slots D = (用) x*y - (作) N per member:")
    for name, x, y, n, slots, _ in MEMBERS:
        d = slots - n
        kind = "exact partition" if d == 0 else "overlap"
        print(f"  {name}: x*y = {slots}, N = {n}, D = {d}  ({kind})")


def main() -> None:
    verify_identities()
    report_map()
    feasible = probe_extensions()
    print_feasibility_grid(feasible)
    report_duplication()
    print("\nall assertions passed.")


if __name__ == "__main__":
    main()
