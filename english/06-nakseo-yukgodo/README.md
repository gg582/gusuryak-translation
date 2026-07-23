## Confirmed Text

共積二百七十

校計周五十四數

以算遠則係以六

通加洛書數六倍

之數見甲編數器章

虛一則二百七十數

## Appended Manuscript Commentary Image

The commentary describing the algorithm called the Naejeok Method (來積法) is very faintly scanned, making it difficult to decipher the original text.
There is a rough transcription reconstructed with Python 3 via generative AI. However, it cannot be denied that this reconstruction contains some speculative readings.

Nevertheless, reverse-engineering the algorithm itself allows us to get one step closer to the reality of the Nakseo Yukgodo (洛書六觚圖).

---

# Nakseo Yukgodo Reconstruction Project

A Python 3 program to reverse-engineer layout configurations (optimal solutions) satisfying the numerical conditions from the manuscript commentary OCR.

## Geometric Structure (Confirmed)

The numerical properties in the commentary align perfectly with historical records in the *Book of Han (漢書·律曆志)*: "二百七十一枚而成六觚, 爲一握" and Su Lin's commentary: "其表六九五十四, 算中積凡得二百七十一枚".

- A hexagonal grid of side length 10: center 1 + rings $k$ (each having $6k$ cells, $k=1..9$) = **271 cells**
- **虛一 (Exclude One)**: Leaving the center cell empty $\rightarrow$ **270 cells** (共積二百七十 / 虛一則二百七十數)
- Outer perimeter of **54 cells** (校計周五十四數 = Su Lin's commentary: 六九五十四)
- Total cell count $270 = 6 \times (1 + 2 + \dots + 9) = \mathbf{6 \times 4 5}$ (通加洛書數六倍)
- Central horizontal axis (中고) of **19 cells** (十九爲中觚數也)

## Hypotheses (Consistent with Choi Seok-jeong's other magic squares)

- Placing numbers 1..270 exactly once (consistent with Jisu Gwinumdo 1..30, Huceck Yonggudo 1..72, etc.)
- Values at antipodal (point-symmetric) positions sum to **271** (consistent with the antipodal pair sums in the Joongsang Gwinumdo, etc.)

Under this hypothesis, ring sums ($813k$) and axis sums ($2439$) are structurally guaranteed, and the search optimizes only for side, sector, and ray balance.

## Execution

```bash
python3 tests/test_hexgrid.py     # Test geometric invariants
python3 main.py                   # Search -> Draw -> Analyze properties (output/)
python3 main.py --render-only     # Regenerate drawings and reports using saved solution
python3 -m yukgodo.reverse        # Reverse-engineer rules of the final layout vs. commentary
python3 -m yukgodo.naejeok        # Verify calculation graph of Naejeok commentary numbers
python3 -m yukgodo.mod5           # mod 5 coloring + 5-layer geometric analysis (D6, networkx)
python3 -m yukgodo.modn_generalization  # mod N antipodal modular action - cross-layout validation
```

## Project Structure

```
yukgodo/
├── hexgrid.py      # Hexagonal grid model (rings, sides, rays, sectors, axes, antipodal pairs)
├── properties.py   # Property scorer (measures target deviations)
├── solver.py       # Antipodal slot representation + simulated annealing + greedy polishing
├── visualize.py    # Diagram (PNG/SVG) and dashboard rendering
├── analyze.py      # Property analysis report generator (JSON/Markdown)
├── hypotheses.py   # Generator and validator for the 添六 constructive hypothesis
├── reverse.py      # Reverse-engineering of final layout rules + commentary comparison
├── naejeok.py      # Verification graph of Naejeok commentary numbers
├── mod5.py         # mod 5 coloring + 5-layer geometric analysis (D6, networkx)
└── modn_generalization.py  # mod N general theory - cross-validation of other layouts
main.py             # Pipeline entry point
tests/test_hexgrid.py
output/             # solution.json, nakseo_yukgodo.png/.svg, dashboard.png, report.md,
                    # siamese_report.md, reverse_engineering.md, mod5_*.png/.json/.md, etc.
```

## Search Results (Reference: output/)

**We successfully found an optimal solution (penalty 6.0) matching the theoretical lower bound.** Verified properties:

| Property | Target | Measured |
|---|---|---|
| Antipodal Pair Sum | 271 | All 135 pairs correct |
| Ring $k$ Sum | $813k$ (813, ..., 7317) | All 9 rings correct |
| Outer 6 Sides Sum | 1355 each | All 6 sides correct |
| 6 Sectors Sum | 6097/6098 | 6097, 6098, 6098, 6098, 6097, 6097 |
| 6 Rays Sum | 1219/1220 | 1219, 1220, 1219, 1220, 1219, 1220 |
| 3 Axes (中고) Sum | 2439 each | All 3 axes correct |
| Vertex Sum | 813 (=3×271, structural) | 206+126+245+65+145+26 = 813 |

Because the sectors (45 cells) and rays (9 cells) contain odd cell counts, exact equality is impossible. The alternating values of 6097/6098 and 1219/1220 represent the mathematical optimum.

## Note

This layout does not directly replicate the Naejeok Method calculations; rather, it is an **optimal solution reverse-engineered to satisfy the numerical conditions** specified in the text.

## Hypothesis Verification Conclusions (`output/hypotheses.json`)

1. The readable values in the commentary serve as **verification of the geometric skeleton and cell counts**: $54+6=60$, $60/6=10$ (cells per side), 中고 19, 252, $252 \times 2 = 504$, $270 = 6 \times 45$. Every verified property matches the grid's mathematical skeleton.
2. The constructive hypothesis interpreting `添六` as a **value placement rule** fails:
   - 192 variations of $\pm 6 \pmod{271}$ spiral placement: Fails to satisfy magic sums (best penalty 27,672).
   - Ring-wise $+6$ progression (Model B): The starting value for each ring is uniquely defined as $a_k = 274 - 18k$, yielding exact ring sums of $813k$, but values duplicate across rings (only 54 unique values), failing the 1..270 bijection constraint.
3. Therefore, the optimal solution under the antipodal pair model (sum 271) remains our best reconstruction candidate. Resolving the sequence ordering instructions (`序左`/`寄左` clauses) requires clearer manuscript copies.

## Inverse-Engineering of Rules: Final Layout vs. Commentary (`output/reverse_engineering.md`)

`yukgodo/reverse.py` uses the final reconstructed layout as a starting point to test for simple constructive rules and compares them against transcribed clauses.

```bash
python3 -m yukgodo.reverse    # Reverse-engineering -> output/reverse_engineering.{json,md}
```

**Reverse-Engineering Attempts (All failed or identified as structural trivialities):**

| Candidate Rule | Result |
|---|---|
| Ring-walk progression (arbitrary step mod 271) | Fails - Best match rate: 16.7% (random noise level) |
| Linear coordinate model: $v \equiv a + b \cdot k + c \cdot j \pmod{271}$ | Fails - Matches only 9/270 cells |
| mod 6 residue class balance (`添六` clause) | No pattern observed |
| Constructive order of antipodal assignment | No pattern observed (longest sequence: 2 pairs) |
| Siamese-type local rules | Fails - Matches only 6/269 transitions (`siamese.py`) |
| 192 variations of `添六` spiral hypothesis | Fails - Best penalty 27,672 (`hypotheses.py`) |

**Commentary Comparison Results:**

- **Confirmed (Cell Count & Geometry)**: 共積二百七十, 虛一則二百七十數, 校計周五十四數, 通加洛書數六倍(270=6×45), 十九爲中觚數也, 置外周五十四以九乘之得四百八十六 & 折半加九得二百52 (confirms the geometric derivation formula $\frac{54 \times 9}{2} + 9 = 252$), 倍之得五百사 & 折半得二百五재 (confirms the 504 doubling/halving check), 合從九목得二百52 & 去중觚 (confirms 252 as 270 minus the 18 central axis cells), 置외주添六 (confirms ring sizes increment by 6).
- **Refuted (Value Placement Interpretation)**: All variations reading `添六` as a value placement rule.
- **Undetermined**: 寄左/序左 (placement sequence), 以算遠則係以六 (illegible text).

**Algorithmic Confirmation — Currently Impossible:**

1. The optimum found using Seed 42 matches the baseline solution at exactly **0/270 cells**. Multiple layouts satisfy the same sum constraints, meaning the reconstructed layout is one of many representative samples.
2. None of these samples show any trace of constructive rules (arithmetic, linear, class, sequential, or local).
3. Therefore, sum constraints alone cannot uniquely restore the original layout or its ordering rules.
4. What can be confirmed is the geometric skeleton, the sum targets, and the refutation of the `添六` value-placement interpretation. Deeper validation requires clearer manuscript scans.

## mod 5 Coloring and mod N Generalization (`output/mod5_report.md`)

Coloring by mod 5 residue classes is a recurring technique in Choi's work (e.g. the 5-coloring in `mod5_residue_diagram.py` of section 02 and the Hadomabangjin 5-coloring document in section 01).
In this project, `yukgodo/mod5.py` divides the optimal solution into 5 layers of 54 cells each, checking D6 symmetries ($12 \text{ elements} \times \text{layer pairs}$).

**Findings**: Layers $2 \leftrightarrow 4$ and $1 \leftrightarrow 0$ are congruent under a 180° rotation (point symmetry), while layer 3 is self-symmetric. No other symmetries exist.

**Derivation (mod N Generalization)**: If all value pairs under an involution $\pi$ ($\pi^2 = \text{id}$) sum to a constant $S$, then for any modulus $m$, $\pi$ acts on mod $m$ residue classes as **$r \mapsto (S - r) \bmod m$**. This holds due to:

1. Applying $v + v' = S \pmod m$ gives $v' \equiv S - v$.
2. The action on residue classes is defined by the involution $r \mapsto S - r$ (orbits of length 2 or fixed points where $2r \equiv S \pmod m$).
3. Since $\pi$ is bijective, $\pi(\text{layer } r) = \text{layer } (S - r)$, explaining the perfect congruence.
4. For this layout, $\pi$ is central point symmetry (180° rotation), meaning layer congruence manifests as geometric grid symmetry.

**Corollary (Parity of Pair Sums)**: If $S$ is odd, no self-paired fixed cells exist. This aligns with our layout's $S = 271$ (odd) and empty center cell. If $S$ is even, the fixed cell's value must be $S/2$, as seen in the central cell (23) of the Joonggung layout of section 02 ($S = 46$).

**Cross-Layout Verification** (`python3 -m yukgodo.modn_generalization`, checking mod 2..9):

| Layout | Pair Sum $S$ | Involution $\pi$ | Result |
|---|---|---|---|
| 06 Nakseo Yukgodo (Reconstructed) | 271 | Central symmetry (180° rotation) | Valid for mod 2..9 |
| 02 Joonggung of Nine Squares | 46 | 3×3 central symmetry | Valid; center cell is $23 = S/2$ |
| 07 Double Eight-Trigrams (Horizontal) | 65 | Horizontal reflection | Valid |
| 07 Houceck Yonggudo | $\approx 73$ (incomplete) | Positional pairs | Fails if mixed; valid if restricted to 16 pairs summing to 73 |

The Houceck Yonggudo shows the necessity of the condition: if the pair sums are not constant, the modular action splits by individual sums. This theorem generalizes to any layout with symmetric complement pairs, extending component-pair checks to arbitrary mod N classes.

**Significance & Limitations**: This property is shared by all solutions satisfying the antipodal pair hypothesis (including Seed 42), meaning it cannot uniquely identify the original layout. However, it serves as a validation tool: if a clearer original manuscript is found and does not display this symmetry, the antipodal complement hypothesis is mathematically disproven.
