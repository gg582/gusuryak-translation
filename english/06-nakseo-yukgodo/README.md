## Confirmed Text

共積二百七十

校計周五十四數

以筭遠則係以六

通加洛書數六倍

之數見甲編數器章

虛一則二百七十數

## Appended Manuscript Commentary Image (Handwritten Naejeok Method)

The manuscript commentary marked as Naejeok Method (來積法) was so faintly scanned that individual character strokes were difficult to identify at a glance. Consequently, early automated AI reconstructions (pseudo-transcription data containing hallucinations) were completely discarded. **After adjusting brightness and contrast of the scan and splitting blurred characters into cropped detail images for stroke-by-stroke comparison, the complete character-by-character decipherment and transcription of the original commentary is available as [ALGO_OCR_SUCCESS.md](file:///home/yjlee/gusuryak-translation/english/06-nakseo-yukgodo/ALGO_OCR_SUCCESS.md)**.

By verifying the core numerical values and computational relationships in this manual transcription via algebraic graph analysis (`python3 -m yukgodo.naejeok`), we derived the high-confidence interpretation that the commentary is not a spatial number placement algorithm, but a **procedure for calculating and verifying the total cell count of the hexagonal grid (積=271, 虛一 270)**.

---

# Nakseo Yukgodo Reconstruction Search Project

A Python 3 program to restore the historical grid specifications of Nakseo Yukgodo and search for feasible balanced solutions (witness solutions) under the antipodal complement hypothesis.

This project does not assume the restoration of a unique original arrangement or a lost placement rule for Nakseo Yukgodo. It formalizes the cell-count structure of the hexagonal grid confirmed from printed text and the handwritten Naejeok Method, applies the antipodal complement technique confirmed in Choi Seok-jeong's other diagrams as a reconstruction hypothesis, and analyzes its necessary consequences. It then formalizes the structure of the basic solution space and searches for witness solutions under additional balance constraints separated from historical invariants.

## Triple Interdisciplinary Gap and Restoration Methodology

As detailed in [INTERDISCIPLINARY.md](file:///home/yjlee/gusuryak-translation/english/06-nakseo-yukgodo/INTERDISCIPLINARY.md), Nakseo Yukgodo straddles the boundary of **History of Mathematics** (limited to primary text reading), **Pure Combinatorics** (with only 1–270 permutations and antipodal complement conditions, the solution space decomposes trivially into $135! \times 2^{135}$ without additional constraints), and **CS/Constraint Programming** (unable to independently extract `.cnf` or MiniZinc specifications from the source text).

This project implements the following 5-step restoration methodology to establish a formal interface across these three fields:
1. Restore grid specifications from readable numerical values (`ALGO_OCR_SUCCESS.md`, cross-referenced with Su Lin's commentary in *Book of Han·Lüli Zhi*)
2. Verify and refute the 192 variations interpreting `添六` as a ±6 value shift, and the ring-wise arithmetic progression model (`output/hypotheses.json`)
3. Strict separation of necessary derived conditions (ring sum $813k$, axis sum $2439$) from arbitrary objective functions (sector/ray balance)
4. Formalize the structure of the basic solution space and search for witness solutions under additional balance constraints (`output/solution.json`, $D_6$ symmetry action)
5. Cross-validate the generalized mod N antipodal residue class theorem against other diagrams (`yukgodo/modn_generalization.py`)

## Geometric Structure (Confirmed)

Literary numerical values and geometric calculations align exactly, confirming the 271-cell centered hexagonal grid structure of Yukgodo (*Book of Han·Lüli Zhi*: "二百七十一枚而成六觚, 爲一握" and Su Lin's commentary: "其表六九五十四, 筭中積凡得二百七十一枚").

- Hexagonal grid of side length 10: center 1 + ring k (each 6k cells, k=1..9) = **271 cells**
- **虛一**: Center left empty → **270 cells** (共積二百七十 / 虛一則二百七十數)
- Outer perimeter of **54 cells** (校計周五十四數 = Su Lin's 六九五十四)
- Total cells 270 = 6×(1+2+...+9) = **6×45** (通加洛書數六倍)
- Central row (中觚) of **19 cells** (十九爲中觚數也)

## Reconstruction Hypothesis: Applying the Complement Involution Technique Confirmed in Choi Seok-jeong's Other Diagrams

- Place values 1..270 each exactly once (same system as Jisu Gwinumdo 1..30, Huchaek Yonggudo 1..72, etc.)
- Two values at antipodal (point-symmetric) positions form a complement pair summing to **271** (complement pair technique as in Joongsang Gwinumdo, etc.)

Under this hypothesis, ring k sum = 813k and the sum of 18 values on each antipodal axis excluding the center vacancy = 9×271 = 2439 are structurally guaranteed automatically, and the search finds only the balance of sides, sectors, and rays.

## Execution

```bash
python3 tests/test_hexgrid.py     # Geometric invariant tests
python3 main.py                   # Search → diagram → property analysis (output/)
python3 main.py --render-only     # Regenerate diagrams and reports from saved solution
python3 -m yukgodo.reverse        # Verify candidate generation rules and local fingerprints
python3 -m yukgodo.naejeok        # Exhaustive search of calculation graph for Naejeok numbers
python3 -m yukgodo.mod5           # mod 5 residue class coloring + 5-layer geometric analysis
python3 -m yukgodo.modn_generalization  # mod N antipodal residue action — cross-diagram validation
```

## External Evidence Submodule

The repository now includes the `nakseo-yukgodo-prompt` git submodule for external orbit/invariant evidence scripts:

```bash
git submodule update --init --recursive
python3 nakseo-yukgodo-prompt/verify_lee_invariants.py
python3 nakseo-yukgodo-prompt/verify_lee_all.py
```

Current confirmed interpretation from these scripts:
- ring-wise $\sum v(c)^2$ is **not** invariant across orbit families;
- linear antipodal pair identities (wedge/ray/side/corner sums) are valid and usable as SMT constraints.

## Project Documentation

- [NAEJEOK_ASSESSMENT.md](file:///home/yjlee/gusuryak-translation/english/06-nakseo-yukgodo/NAEJEOK_ASSESSMENT.md) — Naejeok Method reliability scope and comprehensive evidence assessment
- [INTERDISCIPLINARY.md](file:///home/yjlee/gusuryak-translation/english/06-nakseo-yukgodo/INTERDISCIPLINARY.md) — Triple interdisciplinary gap and standard interface specification
- [ALGO_OCR_SUCCESS.md](file:///home/yjlee/gusuryak-translation/english/06-nakseo-yukgodo/ALGO_OCR_SUCCESS.md) — Deciphered faint manuscript commentary text and numerical evidence
- [COMPARISON.md](file:///home/yjlee/gusuryak-translation/english/06-nakseo-yukgodo/COMPARISON.md) — Comparative verification against existing scholarship
- [DEEP_ANALYSIS.md](file:///home/yjlee/gusuryak-translation/english/06-nakseo-yukgodo/DEEP_ANALYSIS.md) — Geometric and combinatorial deep analysis

## Manuscript Commentary (Naejeok Method) Decipherment, Transcription & Calculation Structure Interpretation

The handwritten **Naejeok Method (來積法)** commentary in the margins of Nakseo Yukgodo has been **completely deciphered and transcribed character by character** through meticulous analysis of faint strokes in the scan ([ALGO_OCR_SUCCESS.md](file:///home/yjlee/gusuryak-translation/english/06-nakseo-yukgodo/ALGO_OCR_SUCCESS.md)). Early generative AI pseudo-transcription output containing hallucinations — including the misreading of `五百六` (506) and incorrect line breaks — was completely discarded, and the confirmed transcription was completed by combining manual character re-decipherment with algebraic calculation graph cross-verification.

The decipherment reliability and academic status criteria for this handwritten commentary transcription are as follows:
- **Character and numerical transcription**: Confirmed
- **Main calculation chain**: Confirmed
- **504 doubling/halving relation**: Strong cross-validation
- **152·12·100 connections**: Tentative interpretation
- **Algorithmic operation term functions**: Partially unconfirmed (mathematical operation meanings of phrases such as `寄左`/`序左`)

### 1. Nature of the Commentary: 'Cell Count Calculation (積)', Not a 'Placement Rule'
* Calculation context overwhelmingly supports interpreting `添六` as an increase in cells per ring rather than a value shift, and separately verified ±6 value placement models all failed.
* The handwritten commentary is supported with high confidence as a **calculation chain for deriving the cumulative count of the hexagonal arrangement (Total Counter-Count Calculation)**, not a spatial arrangement of numbers.

### 2. Computational Graph of Manually Deciphered Values
The core numerical values in the manually deciphered original commentary ($54, 60, 10, 20, 19, 252, 504, 271, 270$) form a strong algebraic calculation chain.

```
置外周五十四，添六得六十      54 + 6 = 60          ┐ 60 is the hub of two paths:
六而一得一十                 60 ÷ 6 = 10         ├ ① Cell count per side
倍之得二十                   10 × 2 = 20         │ ② (First ring 6 + Last ring 54)×9÷2 = 270
減一為十九，為中觚數也        20 − 1 = 19          ┘    same as First+Last terms
Repeated addition of 1       10→11→…→18 (sum 126)   generates upper 9 rows
九乘得二百五十二              (10+18) × 9 = 252     = 2 × 126
二百五十二 + 中觚十九         252 + 19 = 271
虛一則二百七十               271 − 1 = 270        = 共積二百七十
```

* **Confirmation of 504**: Discarding the early AI pseudo-transcription misreading of `五百六` (506), the manual transcription of **`五百四` (504, 倍之得五百四)** was confirmed through manual character re-decipherment and algebraic cross-verification of `252 × 2 = 504`.
* **Separation of nodes 152, 12, and 100**: Operations such as `(20 − 12) × 19 = 152` (`寄左以數十二`) and `152 + 100(合百) = 252` are separated as contextually useful auxiliary nodes/tentative hypotheses to independently protect the credibility of the main calculation chain.

### 3. Historical Cross-Evidence with *Book of Han·Lüli Zhi* and Su Lin's Commentary
* The commentary's `校計周五十四` matches exactly with Su Lin's **"其表六九五十四"** (outer perimeter 54 cells).
* `二百七十一枚而成六觚` (271 cells) and `虛一則二百七十` (270 cells) are also perfectly cross-verified with literary numerical values and geometric calculations, confirming the 271-cell centered hexagonal grid structure of Yukgodo.

## Project Structure

```
yukgodo/
├── hexgrid.py      # Hexagonal grid model (rings/sides/rays/sectors/axes/antipodal pairs)
├── properties.py   # Property scorer (measures target deviations)
├── solver.py       # Antipodal pair slot representation + simulated annealing + greedy polish
├── visualize.py    # Diagram (PNG/SVG) and dashboard rendering
├── analyze.py      # Property analysis report (JSON/Markdown)
├── hypotheses.py   # 添六 constructive hypothesis generation and verification (model A/B/C judgment)
├── reverse.py      # Candidate generation rules and local fingerprint verification of witness solution + commentary comparison
├── naejeok.py      # Exhaustive calculation graph search for Naejeok Method numerical values
├── mod5.py         # mod 5 residue class coloring + 5-layer geometric analysis (D6, networkx)
└── modn_generalization.py  # mod N antipodal residue action theorem — cross-diagram validation with ../ sibling chapters
main.py             # Pipeline entry point
tests/test_hexgrid.py
output/             # solution.json, nakseo_yukgodo.png/.svg, dashboard.png, report.md,
                    # siamese_report.md, reverse_engineering.md, mod5_*.png/.json/.md, etc.
```

## Search Results (based on output/)

**Under the currently adopted hypothesis and objective function, an optimal witness solution reaching the theoretical lower bound of 6.0 was produced.** Verified properties:

| Property | Target | Measured |
|---|---|---|
| Antipodal pair sum | 271 | All 135 pairs correct |
| Ring k sum | 813k (813, ..., 7317) | All 9 rings correct |
| Outer 6 sides sum | 1355 each | All 6 sides correct |
| 6 sector sums | 6097/6098 | 6097,6098,6098,6098,6097,6097 |
| 6 ray sums | 1219/1220 | 1219,1220,1219,1220,1219,1220 |
| 3 axes/中觚 sum | 2439 each | All 3 axes correct (sum of 18 measured values excluding center vacancy) |
| Vertex value sum | 813 (=3×271, structural) | 206+126+245+65+145+26 = 813 (3 opposing complement pairs) |

Sector and ray sums cannot be exactly equal because cell counts are odd (45 cells/9 cells); the alternating 6097/6098·1219/1220 is the mathematical optimum.

## Note

This arrangement does not reproduce the Naejeok Method procedure or a unique original layout; it is an optimal witness solution produced by applying the antipodal complement reconstruction hypothesis and a modern balance objective function to the grid specifications restored from the literature.

## Hypothesis Verification Conclusions (`output/hypotheses.json`)

1. All numerically readable values in the commentary are **geometric skeleton and cell count verifications** — 54+6=60, 60/6=10 (cells per side), 中觚 19, 252, 252×2=504, 270=6×45. That is, everything verifiable in the commentary has been confirmed as the geometric structure of the diagram and its corresponding cell count arithmetic.
2. The evaluated 192 ±6 shift variations and the ring-wise arithmetic progression model all failed.
3. Character decipherment of `寄左` and `序左` is complete, but which algorithmic function they refer to — intermediate value storage, calculation progress, or diagram construction — remains unconfirmed in the mathematical context. There is currently no evidence that they denote a regular cell placement order.

## Candidate Generation Rules and Local Fingerprint Verification (`output/reverse_engineering.md`)

`yukgodo/reverse.py` uses the calculated witness solution as its starting point, tests data-driven whether any compressive generation rule remains, and compares results one-by-one against commentary decipherment clauses.

```bash
python3 -m yukgodo.reverse    # verification → output/reverse_engineering.{json,md}
```

**Candidate generation rule verification results (all judged as failed or structural consequences for the final diagram):**

| Candidate rule | Result |
|---|---|
| Ring-walk arithmetic progression (arbitrary step mod 271) | Failed — best match rate 16.7% (random-noise level) |
| Coordinate linear model v ≡ a+b·k+c·j (mod 271) | Failed — 9/270 cells |
| mod 6 class balance (添六 fingerprint) | No fingerprint |
| Antipodal pair constructive assignment order | No trace (longest consecutive 2 pairs) |
| Siamese-type local rule | Failed — 6 out of 269 transitions (siamese.py) |
| 添六 constructive hypothesis 192 variations | Failed — best penalty 27672 (hypotheses.py) |

**Commentary comparison results:**

- **Confirmed (cell count·geometry)**: 共積二百七十, 虛一則二百七十數, 校計周五十四數, 通加洛書數六倍(270=6×45), 十九爲中觚數也, 置外周五十四以九乘之得四百八十六 and 折半加九得二百五十二 (confirmation of the geometric derivation formula outer perimeter 54 * 9 / 2 + 9 = 252), 倍之得五百四 and 折半得二百五十二 (confirmation of the 504 doubling and halving verification formula), 合從九目得二百五十二 and 去中觚 (252 remaining after removing the 18 central axis cells from the 270 total ring cells), 置外周添六 (cell count reading that rings increase by 6 cells each).
- **Refuted (concrete value placement reading)**: The evaluated ±6 shift and ring-wise arithmetic progression models all failed.
- **Unresolved (algorithmic function unconfirmed)**: Character decipherment of `寄左`·`序左`·`以筭遠則係以六` is complete, but which mathematical function they refer to remains unconfirmed in context.

**Determination on the existence of a regular constructive rule:**

1. Optima found using different seeds match at only **0/270 cells**.
2. No common local generation fingerprint is confirmed.
3. Therefore, current conditions allow multiple solutions, and there is no evidence that a specific regular permutation or local generation rule was originally a defining element of the diagram.

## mod 5 Coloring and mod N Derived Theorem (`output/mod5_report.md`)

mod 5 residue class coloring is a technique repeatedly used throughout the Gusuryak analysis (e.g., `mod5_residue_diagram.py` for section 02's Ojagakdeuk, the Hadosaodo 5-coloring document for section 01).
In this project, `yukgodo/mod5.py` separates the witness solution into 5 layers by residue class (54 cells each) and exhaustively examines D6 symmetry 12 elements × all layer pairs.

**Antipodal complement hypothesis mod 5 consequence (computational verification)**: Residue layers 2↔4 and 1↔0 are fully congruent at 54/54 under 180° rotation (point symmetry), and residue layer 3 is self-symmetric. No other symmetries exist (maximum overlap 13–17/54 for other pairs). This is an algebraic consequence derived from the antipodal action $r \mapsto (1-r) \bmod 5$ under $S=271 \equiv 1 \pmod 5$.

**Derived theorem (mod N generalization)**: If all pair sums under a positional involution π(π²=id) equal a constant S, then for any modulus m, π acts on mod m residue classes as **r ↦ (S−r) mod m**. The reason is four steps:

1. Applying pair condition v+v′ = S mod m gives v′ ≡ S−v for each cell.
2. The action on residue classes is a single involution r ↦ S−r — orbits are either length-2 pairs or fixed points (solutions to 2r ≡ S (mod m)).
3. Since π is bijective, π(layer r) ⊆ layer (S−r) is a set identity — the reason for "complete congruence."
4. The π of this diagram is central point symmetry = 180° rotation, so layer congruence is realized within grid symmetry.

**Corollary (parity of pair sums)**: If S is odd, no self-paired fixed cells can exist — this is consistent with the diagram's S = 271 (odd) and the central 虛一. If S is even, the value of the fixed cell is forced to S/2 — the central 23 = 46/2 of section 02's Gujagakdeuk is an example.

**Cross-diagram validation** (`python3 -m yukgodo.modn_generalization`, exhaustive mod 2..9):

| Diagram (../ sibling chapter) | Pair sum S | Positional involution π | Result |
|---|---|---|---|
| 06 洛書六觚圖 (this witness solution) | 271 | Central point symmetry (full 180° rotation) | All correct for mod 2..9 |
| 02 九子角得 center | 46 | 3×3 central symmetry | All correct, self-pair 23 = S/2 |
| 07 重卦用八圖 horizontal axis | 65 | Left-right reflection within row (local) | All correct |
| 07 侯策用九圖 | ≈73 (incomplete) | Formation positional pairs | Collapses when mixed; correct only when restricted to 16 pairs summing to 73 |

Houchaek Yonggudo demonstrates the necessity of the condition: if pair sums are not constant, the action splits by the actual sum of each pair. That is, this theorem generalizes to all diagrams with positionally symmetric complement pairs, and is an arbitrary mod N extension of the component-pair verification previously done with mod 5 coloring.

**Significance and limitations**: Since all solutions satisfying the antipodal pair hypothesis (including the seed 42 witness solution) share this property, it has no discriminating power for the original arrangement. However, it serves as a falsification tool in the sense that if an actual diagram from a clearer edition does not have this symmetry, the antipodal complement pair hypothesis is rejected.
