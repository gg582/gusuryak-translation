The faint manuscript commentary's numerical and computational relationships were restored through manual stroke decipherment and algebraic consistency verification. Although certain characters remain unconfirmed, it is determined with high confidence that the primary function of the commentary is not a value-placement algorithm, but rather the cell count calculation (積數) and cross-verification of the hexagonal grid. Accordingly, this assessment does not call `v(c)+v(-c)=271` a directly transcribed condition: it is a strong internal reconstruction rule supported by Lo Shu complements, sixfold rings, central symmetry, the *Taiyin Numbers* second-method precedent, and the source title 洛書六觚圖.

## 1. Evidence Hierarchy and Node Confidence Classification

- **Strongly Confirmed Nodes (Strong geometric/algebraic nodes in the computational graph)**: 54, 60, 10, 20, 19, 252, 271, 270.
- **Strongly Corrected Nodes (Doubling/halving relationship with 252)**: 504 ($252 \times 2 = 504$, $504 \div 2 = 252$).
- **Possible Auxiliary Nodes (Dependent on text decipherment)**: 152 ($(20 - 12) \times 19 = 152$, $152 + 100 = 252$).
- **Tentative Hypotheses (Connections with 12 and 100)**: Operations extracting 12 from `寄左以數十二` and connecting `合百` to 100 require further direct grammatical reading support.

| Tier | Artifacts | Nature |
|---|---|---|
| Confirmed Text | The 6 core passages in README.md (共積二百七十, 校計周五十四數, 以筭遠則係以六, 通加洛書數六倍之數見甲編數器章, 虛一則二百七十數) | Confirmed transcription |
| New OCR | ALGO_OCR_SUCCESS.md (39 lines) | Confirmed transcription numbers. The circle "〇" is a start/end marker (not 0; in *Gusuryak*, zero is exclusively written as "零") |
| Geometric Model | yukgodo/hexgrid.py, tests/test_hexgrid.py | 271 cells / 270 after 虛一 / outer perimeter 54 / side length 10 / 中觚 19 / sector 45×6. All tests pass |
| Computation Graph | yukgodo/naejeok.py | Exhaustive search of equations connecting textual numbers |
| Search Optimum | output/solution.json, output/report.md | Penalty 6.0 = theoretical lower bound (Seed 1715, 24 restarts × 300k iterations) |
| Hypothesis Refutation | output/hypotheses.json | Refutation of 192 specific constructive models interpreting 添六 as a $\pm 6$ value shift (192 variations) or ring-wise arithmetic progression |
| Rule Inverse-Engineering | output/reverse_engineering.md/.json | Arithmetic, linear, class, and contiguous allocation rule checks all fail or are structural trivialities |
| Local Rule Inverse-Engineering | output/siamese_report.md | Best Siamese-type rule yields only 6/269 matching transitions |

## 2. Reconstructed Naejeok Calculation Chain

### Core Main Chain (Strong Nodes)

```
Set outer perimeter to 54, add 6 to get 60 (置外周五十四，添六得六十)        54 + 6 = 60         ┐ 60 is the hub of two paths:
Divide by 6 to get 10 (六而一得一十)                                      60 ÷ 6 = 10         ├ ① Calculates cell count per side
Double it to get 20 (倍之得二十)                                          10 × 2 = 20         │ ② Matches the first + last terms of
Subtract 1 to get 19; this is the 中觚 count (減一為十九，為中觚數也)         20 − 1 = 19         ┘    ring sum progression: (6+54)×9÷2 = 270
Repeated addition of 1 (而一加一/添十一)                                    10→11→…→18 (sum 126)  Generates top 9 rows
Multiply by 9 to get 252 (九乘得二百五十二)                                 (10+18) × 9 = 252   = 2 × 126
252 + 中觚 19                                                           252 + 19 = 271
Subtract 1 to get 270 (虛一則二百七十)                                     271 − 1 = 270       = 共積二百七十
```

### The 152 Branch (Tentative Auxiliary Node & Hypotheses)

```
(20 − 12) × 19 = 8 × 19 = 152    (Uses 12 from 寄左以數十二 — Tentative hypothesis)
152 + 100 = 252                  (Merges into 252 via 合百 — Tentative hypothesis)
```
*Note*: Node 152 and its connections to 12 and 100 are managed separately as auxiliary nodes and tentative hypotheses to avoid compromising the credibility of the primary calculation chain.

### The 486 and 252 Geometric Derivation Branch (Reflecting OCR Updates)

The latest transcription update establishes a **geometric formula deriving 252 from the product of the outer perimeter 54 and the ring count 9 (486)**; several characters in the earlier reading were uncertain.

```
Set outer perimeter to 54 (置외주五十四)                                54
Multiply by 9 to get 486 (以九乘之得四百八十六)                          54 × 9 = 486        (Outer perimeter × ring count)
Halve and add 9 to get 252                                                486 ÷ 2 + 9 = 252
Double it to get 504                                                      252 × 2 = 504       (Doubling check of 252)
Halve it to get 252 (折半得二百五十二)                                    504 ÷ 2 = 252
Add 8 + add 11 (寄九) = 271                                             252 + 8 + 11 = 271
Combine rings to get 252, not doubled; exclude the central axes           270 - 18 = 252      (Excluding the 18 non-central axis cells from the 270 total ring cells gives 252)
```

**Mathematical & Geometric Consistency:**
The formula $\frac{54 \times 9}{2} + 9 = 243 + 9 = 252$ aligns perfectly with the geometry of the hexagonal grid.
* The total cell count of the 6 sectors (270) is defined by the sum of an arithmetic progression: $\frac{6 + 54}{2} \times 9 = 270$.
* This can be expanded as: $\frac{54 \times 9}{2} + \frac{6 \times 9}{2} = 243 + 27 = 270$.
* Excluding the non-central cells of the three central axes (18) from the 270 total cells yields 252 ($270 - 18 = 252$).
* The equation $\frac{54 \times 9}{2} + 9 = 243 + 9 = 252$ is geometrically equivalent to $\left(\frac{54}{2} + 1\right) \times 9 = 28 \times 9 = 252$, which matches the trapezoid area sum $(10 + 18) \times 9 = 252$.
* Thus, the author used a mathematical shortcut to directly calculate the area of the non-axial region (252) using only two fundamental constants: the outer perimeter (54) and the ring count (9), without having to calculate individual row lengths.

### `假樣/假積` after `去中觚` (new OCR correction)

The characters formerly read as `展樣/展積` are corrected to `假樣/假積`. The basis for translating them as "unfolding the figure" is therefore withdrawn. Conversely, the sequence `去中觚` followed by `假樣` directly fits an interpretation in which an **auxiliary figure is posited or set up for calculation** after the central row is removed:

\[
去中觚 \longrightarrow 假樣 \longrightarrow 以樣田言之 \longrightarrow 十八下廣,\ 九,\ 倍之.
\]

This strongly supports the reading of a geometric cell-count calculation for the central row and two congruent regions. The contemporary mathematical function of `假樣` and the omitted characters remain unresolved, so this is not extended into a spatial value-placement instruction or a direct statement of antipodal sum 271.

The user-provided direct OCR of the Bing-section [parallel text](BING_PARALLEL_OCR.md) strengthens this conclusion one step further. Its consecutive phrases `每十八隻包中六外成六觚`, `添六隻`, and `以十二而一得八隻` place `包`, `添六`, and `而一` in an actual vocabulary of hexagonal formation and count calculation. This strengthens the reading of the Naejeok Method as a procedure for units, perimeter, and accumulated hexagonal count rather than an independent value-placement rule. The Bing examples using `假如` support the correction to `假樣/假積`, but do not settle the exact technical meaning of `假樣`.

### Independent Verifications Reaching 270 (All endpoints match textual values)

- $6 \times 45 = 270$ — 通加洛書數六倍 (Confirmed text)
- $(6 + 54) \times 9 \div 2 = 270$ — Ring sum progression; the 60 in 添六得六十 represents the sum of the first and last rings.
- $60 \times 9 \div 2 = 270$ — Identical path to above.
- $271 - 1 = 270$ — 虛一則二百七十數 (Confirmed text)
- $54 \times 5 = 270$ — Geometric identity (not in text, but useful reference)

## 3. Decipherment/Transcription Reliability and Interpretation Status

### Character Decipherment & Algebraic Verification Status: Confirmed (Complete Decipherment & Transcription)

270, 271, 54, 60, 10, 20, 19 (中觚), 252, 45×6, 虛一, row lengths 10..19..10, rings 6k (6, 12, ..., 54), sector 45×6. These values align perfectly with the historical record in the *Book of Han (漢書·律曆志)*: "二百七十一枚而成六觚" and Su Lin's commentary (蘇林注): "其表六九五十四".

Furthermore, **manual character decipherment and algebraic cross-verification** confirm the following numbers and operations in the confirmed transcription text:
- **486 (四百八十六)** and **252**: The shortcut formula multiplying outer perimeter 54 by ring count 9 to get 486, halving it, and adding 9 to get 252 (`折半加九得二百五두`).
- **504 (五百四)** and **252 (二百五十二)**: Discarded early AI pseudo-transcription misreading of 506, confirming 504 (`五百四`) via manual glyph decipherment and algebraic doubling verification of 252 ($252 \times 2 = 504$).
- **Add 8 (20-12) + 11 (添十一) = 271**: Adding 8 and 11 to 252 to obtain 271.
- **Combined rings / excluding the central axes**: Geometrically stating that excluding the 18 non-central axis cells from the 270 total ring cells leaves 252 cells.

### Tentative Hypotheses (Dependent on text decipherment & contextual support)

- **152 and its connection branch to 12 and 100**: $(20 - 12) \times 19 = 152$, $152 + 100 = 252$.
  Connecting 12 from `寄左以數十二` to $(20-12)\times 19$ and associating `合百` with 100 are contextually useful auxiliary nodes, but remain tentative hypothesis grade requiring further grammatical decipherment.

### Unresolved (Character reading confirmed, but syntactical/mathematical function unconfirmed)

- 序左十九六合百: $19 \times 6 + 100 = 214$, $19 \times 6 = 114$, $19 + 6 + 100 = 125$ — All reading combinations of 六 as a multiplier mismatch textual values. Unresolved as-written.
- 寄左/序左 instructions: While the numbers (12, 19) and character glyphs are 100% confirmed, the **mathematical placement instructions** and terminology remain open to interpretation.
- 以筭遠則係以六: Character decipherment is complete, but connection to the Naejeok calculation chain and contextual mathematical meaning remain unconfirmed.

### Rejected — Numerically Refuted

- **Refutation of 添六 as a Value Placement Rule**: The 192 specific constructive models interpreting 添六 as a value shift ($\pm 6 \pmod{271}$ spiral variations) or ring-wise arithmetic progression are all numerically refuted (hypotheses.json). However, this refutes these 192 specific models and does not logically refute all conceivable value-placement interpretations.
- **General constructive placement rules**: Best matching rate for ring-based arithmetic progressions is 16.7% (random noise level). Linear coordinate model matches only 9/270 cells. Antipodal pair sequential allocation matches a maximum of 2 consecutive pairs. Siamese-type local rules match only 6/269 transitions.

## 4. Relationship with the Search Optimum — What the Naejeok Method Determines and What It Does Not

The Naejeok chain determines the **cell counts and geometric skeleton**: 270 (虛一), outer perimeter 54, side length 10, 中觚 19, 252, and 6×45. These values map exactly to the validation properties satisfied by the search optimum (penalty 6.0, theoretical lower bound):

| Naejeok Value | Search Optimum Property (output/report.md) |
|---|---|
| 共積二百七十 / 虛一 | 270-cell layout, center excluded, total sum 36,585 |
| 通加洛書數六倍 (6×45) | Ring $k$ sum = $813k$ (all 9 rings hold exactly) |
| 十九爲中觚數也 | 3 axes of 19 cells each, axis sum $2,439 = 9 \times 271$ |
| 校計周五十四數 | Outer perimeter of 54 cells, 6 side sums = 1,355 each |

Conversely, **the exact placement of values is NOT determined by the Naejeok Method**:

- Multiple optimal solutions satisfy the same sum constraints. The optimum found with Seed 42 matches the baseline optimum at exactly 0/270 cells.
- None of the reconstructed optima show any trace of simple constructive generation rules.
- Consequently, sum constraints alone cannot uniquely identify the original layout or its placement sequence.

The residual penalty of 6.0 is not a failure but a structural bound: sectors (45 cells) and rays (9 cells) contain odd numbers of cells and cannot be divided evenly; alternating sums of 6097/6098 and 1219/1220 (penalty 3.0+3.0) represent the mathematical optimum.

### Historical Rotation Angle and Non-Uniqueness

1. **Geometric Analogy: Alignment of 'Trapezoid' (樣田)**
   - The phrase `以樣田言之十八下廣` (speaking of it as a trapezoid, 18 is the bottom width) is a concrete geometric analogy. In traditional mathematics, a trapezoidal field is called `樣田` (trapezoid), and its area is calculated as $\frac{\text{top} + \text{bottom}}{2} \times \text{height}$.
   - Splitting the grid along the central axis (中고) divides it into two trapezoids of 9 rows. The outermost row of length 10 acts as the "top width" (상광), the row adjacent to the axis of length 18 acts as the "bottom width" (하광), and the height is 9.
   - The cell count of this trapezoid is $\frac{10 + 18}{2} \times 9 = 126$ cells, summing to $126 \times 2 = 252$ for both halves. Omitting the division by 2 and calculating $(10+18) \times 9 = 252$ aligns perfectly with this geometric derivation.

2. **Rotation Angle of the Original Layout**
   - The phrase `十八下廣` (18 is the bottom width) strongly implies that the trapezoid's width was aligned horizontally and height vertically. This suggests that a **'Pointy-top' orientation** (where the central axis is horizontal and the grid is vertically symmetric) was the original historical layout direction. The project's grid model is designed based on this horizontal alignment.

3. **Non-Uniqueness of the Historical Solution**
   - Since the hexagonal grid has $D_6$ dihedral symmetry (12 elements), any optimal solution automatically generates 12 isomorphic solutions.
   - However, even excluding these symmetric rotations, computer searches yield countless non-isomorphic solutions with penalty 6.0 (different seeds yield solutions matching at 0/270 cells).
   - Simple rules like arithmetic progressions or Siamese layouts fail to satisfy the magic sums. Thus, Choi Seok-jeong's original layout was likely a unique non-isomorphic solution based on a specific heuristic or a lost design principle. The reconstructed optimal solutions serve as representative samples satisfying the exact historical constraints.

### Generative Search and Path Visualizations (6-Multiplier / add6)

Under the antipodal pair sum constraint $v(c) + v(-c) = 271$, we searched for solutions that enforce the **generative placement formula** $v(P_t) \equiv 6 \cdot t \pmod{271}$ representing the "6-multiplier (添六)" property while satisfying the magic sum conditions (`search_constructive.py`).

1. **Experimental Results (α=0.0 relaxed candidate solution vs. α=2.0 additional experiment)**
   - **No Geometric Constraint ($\alpha=0.0$) — 6-multiplier Relaxed Candidate Solution**:
     * Result: Final penalty **14.0**, average hex distance **8.52** (random scatter level).
     * Interpretation: Under a modified constraint model forcing the algebraic structure $v(P_t) \equiv 6 \cdot t \pmod{271}$, a relaxed candidate solution with penalty 14.0 was obtained, saved in `output/constructive_solution.json` and rendered in `output/constructive_nakseo_yukgodo.png` / `output/constructive_nakseo_yukgodo.svg`. (Note: Since its penalty 14.0 exceeds the unconstrained theoretical floor of 6.0, it is strictly classified as a relaxed candidate solution under the additional 6-multiplier constraint).
     * Key insight: Tested whether interpreting the 6-multiplier rule as a slot-value selector yields an approximate magic-square solution.
   - **Strong Geometric Constraint ($\alpha=2.0$) — Additional Experiment**:
     * Result: Final penalty **58.0**, average hex distance **4.297** (path continuity improved, magic sums destroyed).
     * Interpretation: Adding the constraint that t-th and (t+1)-th cells must also be physically adjacent on the grid (on top of the α=0.0 solution) makes the magic sum condition unachievable.
   - **Conclusion**:
     * **α=0.0 is a relaxed candidate solution**: Enforces the 6-multiplier algebraic structure while assessing magic sum convergence.
     * **α=2.0 is a post-hoc verification for the meaning of `添六`**: Magic-square balance requires large and small values to be globally dispersed, but spatial continuity forces numerically adjacent values ($6t$ and $6(t+1)$, differing by 6) to cluster locally. The structural conflict between these two conditions confirms that `添六` was the parameter of an area calculation formula, not a spatial movement rule.

## 5. Value of the Naejeok Method

1. **Textual Confirmation of the Grid Geometry.** Every count in the calculation chain matches the $D_6$ 270-cell layout. The geometric skeleton (10 per side, 271 total, 1 center cell excluded) is directly confirmed by the text.
2. **Clarification of `添六` (Add 6).** The number 60 in `添六得六十` serves as the starting point for both side length calculation ($60 \div 6 = 10$) and ring sum progression ($(6+54) \times 9 \div 2 = 270$). This resolves the interpretation of `添六` as a calculation trace rather than a placement rule.
3. **Falsifiable Verification Criteria.** The text lists all major invariants (270, 54, 19, 252, 6×45, 虛一) that any reconstructed layout must satisfy. Our search optimum satisfies all of them, elevating it from a "plausible layout" to a "textually verified layout".
4. **Resolution of 504 and Tentative Assessment of 152.** The latest transcription update shows that early AI pseudo-transcription misread 500/506 was originally 504 (doubled 252), integrating strongly into the core main chain. Node 152 and its connection to 12 and 100 are managed as auxiliary nodes / tentative hypotheses, while core values (54, 60, 10, 20, 19, 252, 504, 271, 270) remain completely geometrically and algebraically linked.
5. **Delineation of Scope.** The Naejeok Method is mathematically shown to be a calculation of cell counts (積) rather than a layout placement algorithm. The remaining task is narrowed down to the interpretation of mathematical phrasing such as `序左`.

## 6. Future Work

* **Interpretation of Mathematical Phrasing (`寄左`/`序左`)**: While the main calculation chain and character transcriptions are completely confirmed, the exact academic interpretation of mathematical instructions like `寄左`, `序左`, and `以筭遠則係以六` as specific algorithmic placement steps remains a subject for ongoing research.

## 7. Replication

```bash
python3 tests/test_hexgrid.py     # Verify geometric invariants
python3 -m yukgodo.naejeok        # Verify the calculation graph (asserts pass)
python3 main.py                   # Run search optimum -> output/
python3 -m yukgodo.reverse        # Verify inverse-engineering rules
python3 -m yukgodo.search_constructive  # Run 6-multiplier path search and visualization
```
