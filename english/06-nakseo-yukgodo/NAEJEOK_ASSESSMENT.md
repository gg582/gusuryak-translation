# The Naejeokbeop (來積法): Reliability Scope and Value — a Synthesis of All Project Evidence

This document gathers every reading, computation, and search artifact in the
repository to judge **how far the 來積法 reconstruction can be trusted** and
**what its value is**. Every arithmetic statement can be reproduced by the
exhaustive check of `python3 -m yukgodo.naejeok` (all asserts pass).

## 1. Evidence layers

| Layer | Artifact | Character |
|---|---|---|
| Confirmed source text | the 6 phrases at the top of README.md (共積二百七十, 校計周五十四數, 以算遠則係以六, 通加洛書數六倍之數見甲編數器章, 虛一則二百七十數) | reading confirmed |
| New OCR | ALGO_OCR_SUCCESS.md (39 lines) | uses the confirmed figures. ○ is a sentence-initial/terminal mark (not 0 — in the 九數略 zero is written only as 零) |
| Geometric model | yukgodo/hexgrid.py, tests/test_hexgrid.py | 271 cells / 虛一 270 / perimeter 54 / 10 per side / 中觚 19 / sectors 45×6; tests pass |
| Computation graph | yukgodo/naejeok.py | exhaustive enumeration of arithmetic edges among the source figures |
| Search optimum | output/solution.json, output/report.md | penalty 6.0 = theoretical floor (seed 1715, 24 restarts × 300k iterations) |
| Hypothesis refutation | output/hypotheses.json | 192 variants of constructive 添六 value-rule hypotheses; best penalty 27672 |
| Generation-rule reverse engineering | output/reverse_engineering.md/.json | APs, linear models, classes, consecutive assignments — all fail or reduce to structural consequences |
| Local-rule reverse engineering | output/siamese_report.md | Siamese-style rule best: 6/269 transitions |

## 2. The reconstructed 來積法 computation chain (every step holds exactly)

```
置外周五十四，添六得六十      54 + 6 = 60          ┐ 60 is the hub of two routes:
六而一得一十                 60 ÷ 6 = 10          ├ ① derives the cells per side
倍之得二十                   10 × 2 = 20          │ ② equals the 首+末 term of
減一為十九，為中觚數也        20 − 1 = 19          ┘   (首環6+末環54)×9÷2 = 270
添一 repetition (而一加一/添十一)  10→11→…→18 (sum 126)   generates the upper 9 rows
九乘得二百五十二              (10+18) × 9 = 252     = 2 × 126
二百五十二 + 中觚十九         252 + 19 = 271
虛一則二百七十               271 − 1 = 270        = 共積二百七十
```

### The 一百五十二 branch (an independent node joining the main chain)

```
(二十 − 十二) × 十九 = 8 × 19 = 152    the 十二 of 寄左以數十二 connects here
一百五十二 + 百 = 二百五十二            joins the 252 node via 合百 (十² = 100)
九 × 十九 − 十九 = 152                 九×十九 = 171, and 171 + 100 = 271 also holds simultaneously
```

152 is not a misreading of 252: it is generated from source-text figures
alone, and it joins the main chain exactly via 252 − 152 = 100 = 十².

### Independent cross-checks reaching 270 (every endpoint is a source figure)

- 6 × 45 = 270 — 通加洛書數六倍 (confirmed source text)
- (6 + 54) × 9 ÷ 2 = 270 — ring arithmetic series; the 60 of 添六得六十 = 首環+末環
- 60 × 9 ÷ 2 = 270 — same route as above
- 271 − 1 = 270 — 虛一則二百七十數 (confirmed source text)
- 54 × 5 = 270 — a geometric identity (not fixed by the text; for reference)

## 3. Reliability grading

### Tier 1 — triple agreement (text + lattice model + arithmetic): confirmed

270, 271, 54, 60, 10, 20, 19 (中觚), 252, 45×6, 虛一, row lengths 10..19..10,
rings 6k (6,12,…,54), sectors 45×6. The figures also match the *Hanshu* 律曆志
passage "二百七十一枚而成六觚" and Su Lin's 蘇林 commentary "其表六九五十四"
exactly.

### Tier 2 — generated from source figures alone and joins the main chain: confirmed

- The 152 branch: (20−12)×19 = 152, 152+100 = 252
- The 添一 repetition generates the upper 9 rows (10..18) → (10+18)×9 = 252 = 2×126
- The 十二 of 寄左以數十二 → absorbed into the chain as 20−12 = 8

### Tier 3 — generating expression not identifiable, isolated from the chain: deferred

- 得五百 (500), 五百六 (506): there are **0 one-op generations** using source
  figures alone, and the two-op generations are saturated at 22 and 7
  respectively, so **the figures alone cannot identify the generating
  expression** (`python3 -m yukgodo.naejeok` §7). No edge closes back into
  the chain's figures (270/271/252/…) either.
- The subject of 倍之 is not the preceding three-digit number (neither
  152×2=304 nor 252×2=504 appears in the text). This tail is therefore
  judged to be **the remnant of a separate 案-style cross-check passage with
  its intermediate figures lost**. What it cross-checked cannot be recovered
  from the present reading.

### Tier 4 — unresolved (figures inconsistent with the text as written, or reading insufficient)

- 序左十九六合百: 19×6+100 = 214, 19×6 = 114, 19+6+100 = 125 — every
  combination reading 六 as a multiplier disagrees with the source figures.
  Unresolved as written.
- The 寄左/序左 directives: the figures (十二, 十九) connect to the chain,
  but the interpretation of the **placement-order directive** "set to the
  left, in sequence" remains open.
- 以算遠則係以六: confirmed source text, but no arithmetic connection to the
  naejeokbeop chain.

### Rejected — numerically refuted

- **The ○ = 0 reading (the 504 correction)**: 252 × 2 = 504 never appears in
  the text. The source figure is 得五百 (500), which differs from 504 by 4.
  152 × 2 = 304 likewise appears nowhere.
  → 「倍之得五百○」 is read with a break after 得五百.
- **The 152 = misread-252 theory**: 152 = 8×19 holds independently, so this
  is rejected.
- **Value-placement-rule readings of 添六**: the best of 192 ±6 (mod 271)
  spiral variants scores penalty 27672 (4600× the 6.0 floor); the per-ring
  arithmetic progression (model B) hits the ring sums but duplicates values
  down to 54 distinct ones, violating the one-to-one 1..270 placement
  (hypotheses.json).
- **Constructive generation rules in general**: ring-walk AP best match
  16.7% (noise level), coordinate-linear model 9/270 cells, longest
  consecutive antipodal-pair assignment 2 pairs, Siamese-style local rule
  6/269 transitions (reverse_engineering.md, siamese_report.md).

## 4. Relation to the search optimum — what the naejeokbeop does and does not determine

What the naejeokbeop chain determines is the **cell counts and the geometric
skeleton**: 270 (虛一), perimeter 54, 10 per side, 中觚 19, 252, 6×45. These
figures correspond exactly to the verification conditions satisfied by the
search optimum (penalty 6.0, the theoretical floor):

| Naejeokbeop figure | Corresponding optimum property (output/report.md) |
|---|---|
| 共積二百七十 / 虛一 | 270-cell placement, center excluded, total sum 36585 |
| 通加洛書數六倍 (6×45) | ring k sum = 813k (all 9 rings exact) |
| 十九爲中觚數也 | 3 axes of 19 cells each; axis sum 2439 = 9×271 |
| 校計周五十四數 | perimeter 54 cells; six side sums 1355 = 5×271 each |

The search has also confirmed, on the other hand, that **the naejeokbeop does
not determine the value placement**:

- Many optima satisfy the same sum conditions — the seed-42 optimum agrees
  with the stored optimum in 0/270 cells (reverse_engineering.md §1).
- No reconstructed optimum retains any trace of a constructive generation
  rule (the table in §3).
- Therefore the sum conditions alone cannot identify the original placement
  or its order rule.

The optimum's residual penalty of 6.0 is not a failure but a structural
floor: the sectors (45 cells) and rays (9 cells) have odd cell counts, so
even splitting is impossible, and the alternating 6097/6098 and 1219/1220
patterns (penalty 3.0+3.0) are the mathematical optimum.

## 5. The value of the 來積法

1. **Textual confirmation of the diagram's substance.** Every figure in the
   chain independently agrees with the *Hanshu* 六觚 record and Su Lin's
   commentary. The geometric skeleton of the Nakseo Yukgodo — a hexagonal
   lattice with 10 cells per side, 271 cells, 虛一 — is now fixed directly
   by the text, not by search.
2. **Settling the meaning of 添六.** The 60 of 添六得六十 is the common
   starting point of two computations: ① 60÷6=10 (cells per side) and
   ② (6+54)×9÷2=270 (the 首+末 term of the ring arithmetic series). After the
   search refutation (192 variants), reading 添六 as a value-placement rule
   is now settled at the level of the text's own arithmetic structure as
   well.
3. **Providing falsifiable verification criteria.** The text itself
   enumerates the numeric conditions a reconstruction must satisfy (270, 54,
   19, 252, 6×45, 虛一). The search optimum passes all of them, which
   elevates it from "a plausible placement" to "a placement satisfying the
   source-text conditions".
4. **Partial resolution of the 寄左 fragment.** The 十二 of 寄左以數十二 has
   been absorbed into the chain as (20−12)×19 = 152. Including the 152
   branch and 合百 (252−152=100=十²), every large figure of the new OCR (60,
   152, 252, 271, 270) now lies in a single connected computation graph.
5. **Delimiting the scope of work.** The verdict that the naejeokbeop is a
   procedure for computing 積 (cell counts), not a value-placement
   algorithm, is now backed by arithmetic. The remaining open items are
   narrowed down to two: the 得五百·五百六 tail and the order directive of
   the 序左 fragment.

## 6. Differences from earlier documents (what this document updates)

- The "二百五十二倍之得五百○ (252×2=504) confirmed" notation in the
  conclusion of output/hypotheses.json and in the §3 table of
  output/reverse_engineering.md rests on the earlier judgment that took ○ as
  an illegible character. Following the new OCR judgment (○ = a
  sentence-initial/terminal mark), the source figure is updated to **得五百
  (500)**, read with a break. 504 is not a source figure, and 得五百 is
  reclassified as Tier 3 (generatable but isolated).
- README.md's verdict that "confirming the body of the naejeokbeop requires
  a clearer edition" has been partially resolved: with the new OCR, the
  main-body chain (§2) has reached Tier-1 confirmation. The items that still
  require a clearer edition are narrowed down to the 五百 tail and the 序左
  order directive.

## 7. Reproduction

```bash
python3 tests/test_hexgrid.py     # geometry invariants (the lattice-side basis of Tier 1)
python3 -m yukgodo.naejeok        # exhaustive computation-graph check (all arithmetic in §2, §3)
python3 main.py                   # search optimum → output/ (the object verified in §4)
python3 -m yukgodo.reverse        # generation-rule reverse engineering (basis of the rejected items in §3)
```
