# yukgodo2 — Consecutive Ring-Value Reconstruction (六包一/逓加 family)

An independent mini-repo for another plausible reconstruction of the Nakseo Yukgodo (洛書六觚圖). It is a separate candidate from the antipodal-complement reconstruction of the parent project (`../yukgodo`); the legitimacy comparison of the two hypotheses is documented in [RECONSTRUCTION_COMPARISON.md](../RECONSTRUCTION_COMPARISON.md) at the chapter root.

## Status

The arrangement in this repo is a **conditional consequence of a hypothesis**. There is no evidence that the text directly prescribes this value placement, and the hypothesis is not a condition commanded by the confirmed text.

## Textual basis (directly supported part)

- 逓加洛書數六倍: ring sizes 6k (k = 1..9), 6×(1+…+9) = 6×45 = 270
- 來積法 chain: 54+6=60 (六觚數), 60÷6=10 (一觚數, cells per side), 2×10−1=19 (中觚數), (10+18)×9=252, 252+19=271, 252×2=504, 504÷2=252
- 虛一則二百七十數: the center left void, 270 occupied cells
- 共積二百七十 / 校計周五十四數
- 《漢書·律曆志》 "二百七十一枚而成六觚" with Su Lin's note "其表六九五十四" — documentary cross-evidence for perimeter 54 and total 271
- 六包一 series (published translation of the 九數略, Kun vol., tr. Jeong Hae-nam and Heo Min, Gyowusa, p. 11): 1+(6+12+…+54) = 271 — a series in which rings of 6k wrap a single center, matching this repo's cell-count structure term by term
- 圓束樣式 (same edition, p. 48; original-text format transcribed in [../minimal.md](../minimal.md)): the minimal case n=1 — 1+6 = 7 cells, center void

## Formal statement of the hypothesis

1. Grid: hexagonal board of side 10 (center 1 + ring k of 6k cells) = 271 cells. The center is left void (虛一).
2. Values: place 1..270 each exactly once.
3. Ring intervals: ring k receives the consecutive interval [3k(k−1)+1, 3k(k+1)].

   | ring k | 1 | 2 | 3 | … | 9 |
   | --- | --- | --- | --- | --- | --- |
   | interval | 1..6 | 7..18 | 19..36 | … | 217..270 |

4. Intra-ring progression: values proceed consecutively around each ring's circumference.
5. Normalization: the starting point and direction of each ring are a normalization of rotational symmetry, not a manuscript claim. The indicator multisets (wedge/ray/side/axis sums, antipodal pair sums, corner sum) are D6-invariant under this choice.

## Numerical properties

- Ring k sum = 18k³+3k: 21, 150, 495, 1164, 2265, 3906, 6195, 9240, 13149
- Total = 1+…+270 = 36,585
- Wedge (觚) sums form an arithmetic progression — not balanced (measured values in [output/comparison.md](output/comparison.md))
- Zero antipodal pairs sum to 271 — structurally distinct from the antipodal-complement hypothesis (ring sums 813k, all 135 pairs at 271)

## Run

```bash
python3 solver.py    # Z3 arithmetic check + value placement → output/: solution.json, report.md, reconstruction.png
python3 compare.py   # indicator comparison against the antipodal witness → output/: comparison.json, comparison.md
```

## File layout

```
solver.py   # Z3 encoding of the manuscript arithmetic + consecutive placement + verification + diagram/report
compare.py  # indicator comparison against the antipodal witness
output/     # solution.json, report.md, reconstruction.png, comparison.json, comparison.md
```

## Verification (asserts in solver.py)

- grid cells = 271 (central void 1 + occupied 270)
- values 1..270 each placed exactly once
- every ring's value set matches its consecutive interval exactly
- every ring sum matches 18k³+3k exactly

## Interpretive boundary

This arrangement is a separate candidate from the antipodal-complement hypothesis (ring sums 813k). The evidence from `逓加` and `六包一` concerns the cell-count (積) arithmetic, not value placement, and there is no evidence that the text directly prescribes this value placement. How the book's other diagrams all being balanced constructions coheres with the anti-balanced character of this arrangement remains unresolved.
