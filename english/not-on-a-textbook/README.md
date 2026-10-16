# The function x → y hidden in the names 낙서xy도 (not-on-a-textbook)

In the Gusuryak "nakseo" (洛書) family, every diagram except Nakseo Yukgodo (洛書六觚圖) is named **Nakseo X-gudo (낙서xy도, 洛書xy圖)**, and the two name digits x and y literally enter the calculation.

- **x = the number of cells each group obtains (子)**: it enters the fair-share rule **T = x × (N + 1) / 2** for the common group sum T.
- **y = the number of groups**: it enters the slot count 用 = **x × y**.

The name itself is the design specification: "distribute into y groups of x cells each." Indeed, both identities 用 = x·y and T = x(N+1)/2 hold for every observed member of the family (asserted by the script below).

Nakseo Yukgodo is excluded from this naming scheme: the digit 6 in its name is the number of sides of the hexagon (六觚), not a participant in the x/y naming system used by the other five diagrams.

## Verification table

| Diagram | x (cells per group) | y (groups) | N (作) | 用 = x·y | group sum T |
|---|---:|---:|---:|---:|---:|
| Nakseo Sagudo (洛書四九圖) | 4 | 9 | 20 | 36 | 42 |
| Nakseo Ogudo (洛書五九圖) | 5 | 9 | 33 | 45 | 85 |
| Nakseo Chilgudo (洛書七九圖) | 7 | 9 | 63 | 63 | 224 |
| Nakseo Palgudo (洛書八九圖) | 8 | 9 | 40 | 72 | 164 |
| Nakseo Gugudo (洛書九九圖) | 9 | 9 | 81 | 81 | 369 |

Sample checks: Nakseo Sagudo has T = 4 × 21 / 2 = 42; Nakseo Gugudo has T = 9 × 82 / 2 = 369.

Note: the original diagrams themselves (Nakseo Gugudo included) are intact; only their transcriptions contained errors.

## Domain, codomain, image

Reconstructing the map x → y from the observed family:

- **Domain**: {4, 5, 7, 8, 9} — the x values of the diagrams that actually exist.
- **Image**: {9} — every observed y equals 9, so the constant-function hypothesis y ≡ 9 cannot be rejected on the current data.
- **Codomain candidates**:
  - Under the nine-palace-only (九宫) hypothesis: {9} — the geometric assumption that nakseo diagrams always live on nine palaces.
  - Under the arithmetic gate alone (T = x(x·y+1)/2 integral for the exact-partition subclass N = x·y), the codomain is not forced. A hypothetical Nakseo Yuk-gudo (洛書六九圖) with x = 6 passes the gate yet is historically absent, and many pairs with y ≠ 9 also pass.

## Script

`nakseo_xy_function.py` does the following:

- (a) asserts 用 = x·y for every family member
- (b) asserts the fair-share rule T = x(N+1)/2 for every family member
- (c) prints the domain, the observed y values, the image, and tests the constant-function hypothesis y ≡ 9
- (d) extension probe for the exact-partition subclass (N = x·y): prints the feasibility grid of pairs (x, y) with x ∈ 1..12, y ∈ 3..12 for which T is an integer, highlighting the x = 6 gap and the y ≠ 9 pairs that pass
- (e) prints the duplication slots D = x·y − N per member

Run:

```bash
python3 nakseo_xy_function.py
```

Actual output:

```text
map x -> y from the observed nakseo family:
  domain X       = [4, 5, 7, 8, 9]
  observed y     = [9]
  image  f(X)    = [9]
  constant-function hypothesis (y == 9 for all members): True

extension probe (exact-partition subclass N = x*y):
  grid of y for each x ('.' = infeasible, 'y' = feasible,
  'F' = feasible but historically absent, '*' = observed member)
  x\y |   3   4   5   6   7   8   9  10  11  12
  ----+----------------------------------------
    1 |   F   .   F   .   F   .   F   .   F   .
    2 |   F   F   F   F   F   F   F   F   F   F
    3 |   F   .   F   .   F   .   F   .   F   .
    4 |   F   F   F   F   F   F   *   F   F   F
    5 |   F   .   F   .   F   .   *   .   F   .
    6 |   F   F   F   F   F   F   F   F   F   F
    7 |   F   .   F   .   F   .   *   .   F   .
    8 |   F   F   F   F   F   F   *   F   F   F
    9 |   F   .   F   .   F   .   *   .   F   .
   10 |   F   F   F   F   F   F   F   F   F   F
   11 |   F   .   F   .   F   .   F   .   F   .
   12 |   F   F   F   F   F   F   F   F   F   F

  x = 6 (a hypothetical Nakseo Yuk-gudo 洛書六九圖) passes the gate at y = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12], yet is historically absent.
  pairs with y != 9 that also pass the gate: 78 of 90 feasible pairs
  -> the name-based codomain {9} is NOT forced by arithmetic.

duplication slots D = (用) x*y - (作) N per member:
  Nakseo Sagudo (洛書四九圖): x*y = 36, N = 20, D = 16  (overlap)
  Nakseo Ogudo (洛書五九圖): x*y = 45, N = 33, D = 12  (overlap)
  Nakseo Chilgudo (洛書七九圖): x*y = 63, N = 63, D = 0  (exact partition)
  Nakseo Palgudo (洛書八九圖): x*y = 72, N = 40, D = 32  (overlap)
  Nakseo Gugudo (洛書九九圖): x*y = 81, N = 81, D = 0  (exact partition)

all assertions passed.
```

## See also

- For the shared gakdeuk principle behind these diagrams and its generalization, see ../04-unification.
