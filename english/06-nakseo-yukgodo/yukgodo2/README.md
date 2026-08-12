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

## Deep assessment: the "Choyukche-ga" (초육체가) series theory in the Gyowusa edition's commentary

### Background

The modern-language commentary of the published translation of the 九數略, Kun (坤) volume (tr. Jeong Hae-nam and Heo Min, Gyowusa), proposes the center-wrapping series 1+(6+12+18+…) under the name "초육체가" (Choyukche-ga), and puts forward the theory that this series grows as (1+6+12+18+27+36+54+54+63+72+81) and is visualized as nine rings. Here we assess how far that theory remains persuasive inside the 來積法 and where it breaks down.

### Where it is persuasive

The partial sums run 1, 7, 19, 37, … — **up through the third growth term they coincide exactly with the centered hexagonal numbers 1+3n(n+1)**.

| partial sum / term | point of contact with the 來積法 and related documents |
| --- | --- |
| 1+6 = 7 | the 7-cell 圓束樣式 figure (same edition, p. 48) — the minimal vacant-center case |
| 1+6+12 = 19 | the 來積法's 中觚數 19 (though the 來積法 derives it independently as 2×10−1) |
| first three terms 6, 12, 18 | coincide with the first three 逓加 rings 6k |
| partial sum through …+63 = 271 | matches the grand total 271 (共積 + 虛一) |
| the term 54 (appearing twice) | the perimeter of 枚外周五十四數 |

### Where it breaks down

1. **Point of departure from the centered hexagonal numbers**: at the fourth growth term the geometry requires 24 (partial sum 61); the theory places 27 (partial sum 64). The theory agrees with the geometry only through ring 3 and breaks from ring 4 onward.
2. **Violation of 係以六**: 27, 63, and 81 are not multiples of 6. Every operation of the 來積法 — 添六, 六歸, 六而一, 六倍 — rests on six-regularity, and that ring sizes are multiples of 6 is a direct consequence of 以筭法則係以六.
3. **No generating rule**: reading the terms after 18 as multiples of 9 gives quotients 3, 4, (5 skipped), 6, 6 (duplicated), 7, 8, 9 — with a skip and a duplication, no single generating rule holds. The 來積法's operations are all regular (添六, 倍之, 折半, 六歸).
4. **Mismatch of the ring count**: there are 10 growth terms after the 1. The total 271 appears at the ninth partial sum (center + 8 terms = 9 levels), whereas the 來積法 independently derives **nine rings** via 54÷6=9 (center + 9 rings = 10 levels). "Visualized as nine rings" is off by one layer from the Naejeok structure.
5. **Violation of the perimeter ceiling**: 63, 72, and 81 exceed the perimeter 54. No ring beyond 54 can geometrically exist on a radius-9 hexagonal board, and 枚外周五十四數 is confirmed text.
6. **Mismatch of the grand total**: the full series sums to 424, which matches no confirmed figure of the board (270, 271). Since 271 appears only as an intermediate partial sum, the series would have to be cut there — but the text supplies no such cutoff point.
7. **Failure to generate the confirmed nodes**: the series does not produce the 來積法's confirmed nodes 60, 252, 504. The relation 252 = 271−19 is only an after-the-fact pairing of two partial sums.

### Verdict

- The **bare concept** of 六包一/초육체가 — "one center wrapped by rings of six" — is coherent with the 來積法's cell-count structure (1+6×45 = 271) and meshes with the reading of 包中六外成六觚 in the Bing section.
- However, the **nine-ring visualization theory** with the growth sequence (…27, 36, 54, 54, 63, 72, 81) collides head-on with the 來積法's six-regularity, its derivation of the ring count (54÷6=9), the perimeter ceiling (54), and the centered-hexagonal geometry. The partial-sum coincidences (7, 19, 271) are strongly in the nature of chance matches dependent on choosing a cutoff.
- The theory is therefore recorded as an extended interpretation from the edition's commentary, and is not written as directly supported by the 來積法. The yukgodo2 reconstruction keeps the 6k ring regularity of 逓加.

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
