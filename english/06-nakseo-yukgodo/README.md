## Confirmed original text

共積二百七十

校計周五十四數

以算遠則係以六

通加洛書數六倍

之數見甲編數器章

虛一則二百七十數

## Attached commentary image

The commentary to the algorithm known as naejeokbeop(來積法, Iterative Accumulation Method) is scanned so faintly
that the original type is hard to make out. A rough picture reconstructed in
Python 3 with the help of generative AI is attached
(`original_comments_reconstructed_by_genai.png`). Even so, it cannot be
denied that this reconstruction, too, contains portions restored by
guesswork.

Nevertheless, by reverse-engineering the algorithm itself to a fair extent,
we have come one step closer to the true form of the Nakseo Yukgodo
(洛書六觚圖) — and therein lies the significance of this work.

---

# Nakseo Yukgodo (洛書六觚圖) Reconstruction Search Project

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
- Central horizontal row (中觚) **19 cells** (十九爲中觚數也)

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
python3 -m yukgodo.reverse        # reverse-engineer the generation rule → commentary cross-check
python3 -m yukgodo.naejeok        # exhaustive computation-graph check of the 來積法 figures
python3 -m yukgodo.mod5           # mod-5 residue coloring + exhaustive five-layer geometry
python3 -m yukgodo.modn_generalization  # mod-N antipode residue action — cross-diagram verification
```

## Project structure

```
yukgodo/
├── hexgrid.py      # hexagonal lattice model (rings/sides/rays/觚-sectors/axes/antipodal pairs)
├── properties.py   # property scorer (target-deviation measurement)
├── solver.py       # antipodal-pair slot representation + simulated annealing + greedy polish
├── visualize.py    # diagram (PNG/SVG) and dashboard rendering
├── analyze.py      # property analysis report (JSON/Markdown)
├── hypotheses.py   # generation/verification of 添六 constructive hypotheses (models A/B/C verdicts)
├── reverse.py      # reverse-engineering of the generation rule + commentary cross-check
├── naejeok.py      # exhaustive computation-graph check of the 來積法 figures
├── mod5.py         # mod-5 residue coloring + exhaustive five-layer geometry (D6, networkx)
└── modn_generalization.py  # mod-N antipode residue action theorem — cross-checks against the other diagrams in ../
main.py             # pipeline entry point
tests/test_hexgrid.py
output/             # solution.json, nakseo_yukgodo.png/.svg, dashboard.png, report.md,
                    # siamese_report.md, reverse_engineering.md, mod5_*.png/.json/.md, etc.
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
| three axes / 中觚 sums | 2439 each | all 3 axes exact |
| corner value sum | 813 (=3×271, structural) | 206+126+245+65+145+26 = 813 |

The sector and ray sums have odd cell counts (45 / 9 cells), so exact
equality is impossible; the alternating 6097/6098 and 1219/1220 patterns
are the mathematical optimum.

## Caveat

This placement does not reproduce the commentary's naejeokbeop procedure
step by step; it is a **search optimum reverse-engineered to satisfy the
commentary's numeric conditions**.

## Hypothesis-verification verdict (`output/hypotheses.json`)

1. Every legible figure in the commentary is a **cell-count check** —
   54+6=60, 60/6=10 (cells per side), 中觚 19, 252(=271−19)×2=504,
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

## Reverse-engineering the generation rule: final diagram → faint-commentary cross-check (`output/reverse_engineering.md`)

`yukgodo/reverse.py` starts from the final reconstructed diagram, tests
data-driven whether any compressive generation rule survives in it, and
compares each outcome against the legible commentary fragments.

```bash
python3 -m yukgodo.reverse    # reverse-engineering → output/reverse_engineering.{json,md}
```

**Attempts (each judged a failure or a structural consequence on the final diagram):**

| Candidate rule | Result |
|---|---|
| ring-walk AP (any step mod 271) | failed — best match 16.7% (noise level) |
| coordinate-linear model v ≡ a+b·k+c·j (mod 271) | failed — 9/270 cells |
| mod-6 class balance (添六 fingerprint) | no fingerprint |
| constructive pair-assignment order | no trace (longest run 2 pairs) |
| Siamese-style local rule | failed — 6 of 269 transitions (siamese.py) |
| 添六 construction hypotheses (192 variants) | failed — best penalty 27672 (hypotheses.py) |

**Commentary cross-check:**

- **Confirmed (cell counts, geometry)**: 共積二百七十, 虛一則二百七十數,
  校計周五十四數, 通加洛書數六倍 (270=6×45), 十九爲中觚數也,
  二百五十二倍之得五百○ (252×2=504), 置外周添六 (cell-count reading:
  rings grow by six cells).
- **Refuted (value-rule readings)**: every variant reading 添六 as a
  value-placement rule.
- **Undecidable**: 寄左/序左 (placement order), 以算遠則係以六 (uncertain reading).

**Verdict — the algorithm cannot be confirmed from the present evidence:**

1. An optimum found under another seed (42) agrees with the stored optimum in
   **0 of 270 cells**: many placements satisfy the conditions, and the
   reconstructed diagram is only one specimen.
2. No constructive trace (APs, linear rules, classes, consecutive assignments,
   local rules) survives in these specimens, so neither the original placement
   nor its order rule can be recovered from sum conditions alone.
3. What can be settled extends to the geometric skeleton, the sum conditions,
   and the refutation of the value-rule readings of 添六. Confirming the body
   of the naejeokbeop requires a clearer edition of the commentary.

## Mod-5 coloring and the mod-N derived theorem (`output/mod5_report.md`)

Mod-5 residue coloring is a technique used repeatedly across the Gusuryak
analyses (the Ojagakdeuk `mod5_residue_diagram.py` in 02, the Hado-Saodo
5-coloring documents in 01). In this project `yukgodo/mod5.py` splits the
optimum into five layers by residue class (54 cells each) and exhaustively
checks all 12 D6 symmetry elements against every layer pair.

**Finding**: the residue 2↔4 and 1↔0 layers are exactly congruent (54/54)
under 180° rotation (point symmetry), and the residue-3 layer is
self-symmetric. No other symmetry exists (the best overlap of any other pair
is 13–17/54).

**Derived theorem (mod-N generalization)**: under a positional involution π
(π²=id) with every pair of values summing to a constant S, π acts on mod-m
residue classes as **r ↦ (S−r) mod m** for every modulus m. The reason has
four steps:

1. Reducing the pair condition v+v′ = S mod m gives v′ ≡ S−v, cell by cell.
2. The action on residue classes is the single involution r ↦ S−r — its
   orbits are either pairs of length 2 or fixed points (the solutions of
   2r ≡ S (mod m)).
3. Since π is one-to-one, π(layer r) ⊆ layer (S−r) is already set equality —
   the reason the overlap is exact rather than approximate.
4. In this diagram π is central point symmetry = 180° rotation, so the layer
   congruences are realized inside the lattice symmetries.

**Corollary (parity of the pair sum)**: if S is odd, no self-paired fixed
cell can exist — this diagram's S = 271 (odd) and the central 虛一 are
consistent with it. If S is even, a fixed cell's value is forced to be S/2 —
the center 23 = 46/2 of the Guja-gakdeuk (九子角得) center palace in 02 is
an example.

**Cross-diagram verification** (`python3 -m yukgodo.modn_generalization`,
exhaustive over moduli 2..9):

| Diagram (sibling chapter in ../) | Pair sum S | Positional involution π | Result |
|---|---|---|---|
| 06 洛書六觚圖 (this optimum) | 271 | central point symmetry (global 180° rotation) | exact for all of mod 2..9 |
| 02 九子角得 center palace | 46 | 3×3 central symmetry | all exact; self-pair 23 = S/2 |
| 07 重卦用八圖 horizontal formation | 65 | left-right flip within a row (local) | all exact |
| 07 侯策用九圖 | ≈73 (imperfect) | formation position pairs | breaks when mixed; exact when restricted to the 16 pairs summing to 73 |

侯策用九圖 demonstrates the necessity of the condition: when the pair sums
are not constant, the action splits into the per-pair actual sums. In other
words, the theorem generalizes to every diagram with positionally symmetric
complementary pairs, and extends the component-pair cross-check done with
mod-5 coloring to arbitrary mod N.

**Significance and limits**: every solution satisfying the antipodal-pair
hypothesis (including the seed-42 optimum) has this property, so it carries
no discriminating power for the original placement. It is, however, a
falsification tool: if the actual diagram of a clearer edition did not have
this symmetry, the antipodal complementary-pair hypothesis would be rejected.
