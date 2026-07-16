## Confirmed original text

共積二百七十

校計周五十四數

以算遠則係以六

通加洛書數六倍

之數見甲編數器章

虛一則二百七十數

## Attached commentary image

The commentary to the algorithm known as seungjeokbeop is scanned so faintly
that the original type is hard to make out. A rough picture reconstructed in
Python 3 with the help of generative AI is attached
(`original_comments_reconstructed_by_genai.png`). Even so, it cannot be
denied that this reconstruction, too, contains portions restored by
guesswork.

Nevertheless, by reverse-engineering the algorithm itself to a fair extent,
we have come one step closer to the true form of the Nakseo Yukgodo
(落書六觚圖) — and therein lies the significance of this work.

---

# Nakseo Yukgodo (落書六觚圖) Reconstruction Search Project

A Python 3 program that reverse-engineers, by search, a placement (the
optimum) satisfying the numeric conditions found in the commentary OCR.

## Geometry (established)

The figures in the commentary match the *Hanshu* 律曆志 passage
"二百七十一枚而成六觚, 爲一握" and Su Lin's 蘇林 commentary
"其表六九五十四, 算中積凡得二百七十一枚" exactly.

- Hexagonal lattice with 10 cells per side: center 1 + ring k (6k cells each, k=1..9) = **271 cells**
- **虛一**: the center is left void → **270 cells** (共積二百七十 / 虛一則二百七十數)
- Perimeter **54 cells** (校計周五十四數 = Su Lin's 六九五十四)
- Total cells 270 = 6×(1+2+...+9) = **6×45** (通加洛書數六倍)
- Central horizontal row (中觔) **19 cells** (十九爲中觔數也)

## Hypotheses (same technique as Choi Seok-jeong's other magic diagrams)

- Place each value 1..270 exactly once (the same scheme as Jisuguimundo 1..30, Huchaekyonggudo 1..72, etc.)
- The two values at antipodal (point-symmetric) cells form a complementary pair summing to **271** (the complementary-pair technique of the Jungsang Gugudo (中上龜九圖) and others)

Under these hypotheses, ring k sum = 813k and axis sum = 2439 hold
structurally, and the search only needs to balance sides, sectors, and rays.

## Running

```bash
python3 tests/test_hexgrid.py     # geometry invariant tests
python3 main.py                   # search → diagram → property analysis (output/)
python3 main.py --render-only     # regenerate figures/report from the saved solution
```

## Project structure

```
yukgodo/
├── hexgrid.py      # hexagonal lattice model (rings/sides/rays/觚-sectors/axes/antipodal pairs)
├── properties.py   # property scorer (target-deviation measurement)
├── solver.py       # antipodal-pair slot representation + simulated annealing + greedy polish
├── visualize.py    # diagram (PNG/SVG) and dashboard rendering
├── analyze.py      # property analysis report (JSON/Markdown)
└── hypotheses.py   # generation/verification of 添六 constructive hypotheses (models A/B/C verdicts)
main.py             # pipeline entry point
tests/test_hexgrid.py
output/             # solution.json, nakseo_yukgodo.png/.svg, dashboard.png, report.md
```

## Search result (see output/)

**An optimum matching the theoretical floor (penalty 6.0) was found.** Verified properties:

| Property | Target | Measured |
|---|---|---|
| antipodal pair sum | 271 | all 135 pairs exact |
| ring k sum | 813k (813, ..., 7317) | all 9 rings exact |
| six perimeter side sums | 1355 each | all 6 sides exact |
| six 觚-sector sums | 6097/6098 | 6097,6098,6098,6098,6097,6097 |
| six ray sums | 1219/1220 | 1219,1220,1219,1220,1219,1220 |
| three axes / 中觔 sums | 2439 each | all 3 axes exact |
| corner value sum | 813 (=3×271, structural) | 206+126+245+65+145+26 = 813 |

The sector and ray sums have odd cell counts (45 / 9 cells), so exact
equality is impossible; the alternating 6097/6098 and 1219/1220 patterns
are the mathematical optimum.

## Caveat

This placement does not reproduce the commentary's seungjeokbeop procedure
step by step; it is a **search optimum reverse-engineered to satisfy the
commentary's numeric conditions**.

## Hypothesis-verification verdict (`output/hypotheses.json`)

1. Every legible figure in the commentary is a **cell-count check** —
   54+6=60, 60/6=10 (cells per side), 中觔 19, 252(=271−19)×2=504,
   270=6×45. In other words, the verifiable content of the commentary is
   the geometry of the diagram, and all of it is confirmed.
2. All constructive hypotheses that read 添六 as a **value-placement rule** fail:
   - 192 variants of ±6 (mod 271) spiral placement: the magic-sum
     properties are not satisfied (best penalty 27672)
   - per-ring +6 arithmetic progression (model B): a unique starting value
     a_k = 274−18k exists per ring and hits the ring sums 813k exactly,
     but values duplicate across rings (only 54 distinct values), violating
     the 1..270 placement condition
3. Therefore the search optimum under the antipodal complementary-pair
   (sum 271) model is the best current reconstruction candidate, and the
   placement-order rule (the 寄左/序左 phrase) remains an open item pending
   a clearer edition.
