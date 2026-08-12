# Legitimacy Comparison of the Two Yukgodo Reconstruction Hypotheses: Antipodal Complements vs Consecutive Ring Values

This document places the two plausible reconstruction hypotheses for the 洛書六觚圖 side by side and compares their textual evidence, numerical properties, weaknesses, and decisive criteria. The starting premise is that neither is a confirmed textual condition.

- **Hypothesis A — antipodal complements**: the two values at antipodal (point-symmetric) positions form a complement pair summing to 271. The parent `yukgodo/` package and the witness in `output/solution.json` adopt this hypothesis.
- **Hypothesis B — consecutive ring values**: ring k receives the consecutive interval 3k(k−1)+1 … 3k(k+1), and values proceed consecutively around each ring. [yukgodo2/](yukgodo2/) implements this hypothesis.

## 1. Shared basis (confirmed text and geometry)

The part directly supported by text and calculation, shared by both hypotheses:

| item | value | evidence |
| --- | --- | --- |
| total cells | 271 | 《漢書·律曆志》 二百七十一枚而成六觚; 來積法 252+19 |
| after 虛一 | 270 | 虛一則二百七十數, 共積二百七十 |
| outer perimeter | 54 | 校計周五十四數 = Su Lin's 六九五十四 |
| cells per side | 10 | 來積法 54+6=60, 60÷6=10 (一觚數) |
| central row 中觚 | 19 | 來積法 2×10−1=19 (中觚數) |
| ring sizes | 6k | 以筭遠則係以六, 逓加洛書數六倍 |
| ring count | 9 | 來積法 54÷6=9 |

Up to this layer the two hypotheses coincide completely; they differ only in the **placement of values**.

## 2. Layers of textual evidence

| evidence | hypothesis A (antipodal) | hypothesis B (consecutive) |
| --- | --- | --- |
| 來積法 as a whole | neutral — it is count (積) arithmetic, placement-free | neutral — same |
| `逓加` ("adding successively") vocabulary | indirect — read as sixfold rings of Lo Shu numbers | affinity — the sequential-accumulation vocabulary meshes with ring-wise consecutive accumulation |
| 六包一 series (Gyowusa ed. p. 11: 1+(6+12+…+54)) | neutral — only the cell-count structure matches | matches the cell-count structure term by term — but the series is a count, not a value placement |
| the name `洛書`六觚圖 | strong support — the essence of the Lo Shu is antipodal complement pairs (sum 10, center 5) | unsupported — uses no Lo Shu property, leaving the name meaningless |
| complement-pair construction precedents in sibling diagrams (洛書九九圖 etc.) | strong support — complement pairs serve as an actual construction rule | violated — conflicts with the balance-construction grammar |
| 圓束樣式 (vacant center, pair units; Gyowusa ed. p. 48) | support — the minimal precedent of pair structure after a central vacancy | neutral — only the vacancy is shared |
| the sixfold lift in 逓加洛書數六倍 (54+6=60) | support — `k↔10-k` lifted to `6k↔6(10-k)` | neutral |
| a direct placement command | none | none |

## 3. Measured indicators

`yukgodo2/compare.py` measures both solutions with the same geometric indicators (full figures: [yukgodo2/output/comparison.md](yukgodo2/output/comparison.md)). The A-side witness is seed 1715 (penalty 6.0 = theoretical floor); the English tree's witness is a longer run of the same seed, so only the ordering of wedge/ray values differs while the multisets agree.

### Ring sums (A's structural consequence: 813k)

| ring k | A (antipodal) | B (consecutive, 18k³+3k) |
| ---: | ---: | ---: |
| 1 | 813 | 21 |
| 2 | 1626 | 150 |
| 3 | 2439 | 495 |
| 4 | 3252 | 1164 |
| 5 | 4065 | 2265 |
| 6 | 4878 | 3906 |
| 7 | 5691 | 6195 |
| 8 | 6504 | 9240 |
| 9 | 7317 | 13149 |

### Balance indicators (max deviation)

| indicator | target | A max dev. | B max dev. |
| --- | ---: | ---: | ---: |
| wedge (觚) sums | 6097.5 | 0.5 | 712.5 |
| ray sums | 1219.5 | 0.5 | 490.5 |
| outer side sums | 1355 | 0 | 1256 |
| axis (中觚 family) sums | 2439 | 0 | 846 |

B's wedge sums form the arithmetic progression 5385, 5670, 5955, 6240, 6525, 6810 (common difference 285), and its side sums increase monotonically from 2215 to 2611.

### Antipodal pairs and corners

| indicator | A | B |
| --- | ---: | ---: |
| pairs summing to 271 (of 135) | 135 | 0 |
| pair-sum range | 271–271 | 5–513 |
| corner sum (structural target 813) | 813 | 1437 |

These indicators of B are independent of the start-point normalization: the D6 action (rotations and reflections) preserves the multisets of wedge/ray/side/axis sums, the multiset of antipodal pair sums, and the corner sum, so the deviations above are properties of the hypothesis itself, not artifacts of a coordinate convention.

## 4. What the numbers say

- **A's discriminating structure**: once A is adopted, ring sums 813k, axis sums 2439, and the corner sum 813 follow automatically and carry no discriminating power; what the optimization actually produces is the balance of wedges, rays, and sides. The solution space is vast at 135!×2¹³⁵, and witnesses from different seeds agree on 0/270 cells — there is no power to identify a particular original arrangement.
- **B's anti-balance**: B departs structurally from every balance indicator. Because values accumulate in ascending order along the rings, small values cluster in one sector and large values in the opposite one under any rotation or reflection. This is not a normalization issue but a necessity of "consecutive accumulation" itself.

## 5. Weaknesses of each hypothesis

**Hypothesis A (antipodal complements)**

- No direct position-to-value command such as `對觚相合二百七十一` has been transcribed.
- Countermodel audits (`ANTIPODAL_AUDIT.md`, `NAKSEO_FAMILY_EVIDENCE.md`): arrangements exist that preserve the value set, ring sums, axis sums, side sums, and wedge/ray balance while breaking the antipodal sums — aggregate conditions do not logically force antipodal complements.
- The vast multiplicity of witnesses means there is no power to identify the original arrangement.

**Hypothesis B (consecutive ring values)**

- It renders the name `洛書六觚圖` meaningless — it uses no Lo Shu property (neither complement pairs nor balance).
- The sibling diagrams of the 九數略 (the 3×3 Lo Shu, 洛書九九圖, 九子角得, and so on) are all balance/complement constructions, while anti-balance is a structural necessity for B.
- The evidence favoring B — `逓加` and `六包一` — concerns the cell-count (積) arithmetic, not the placement of values 1..270. The assessment that the 來積法 is count arithmetic is neutral between A and B.
- A consecutive placement is always constructible, so Z3 satisfiability by itself is not evidence.

## 6. What would decide between them

- **Reading the actual arrangement from a sharper edition**: once the real diagram is legible, (i) whether the mod-N residue coloring shows the r↔S−r symmetry under 180° rotation tests (and could falsify) A, and (ii) whether each ring's value set forms a consecutive interval tests (and could falsify) B. The two tests are independent, and both could be rejected.
- **Discovery of a direct command**: a newly transcribed passage commanding a position-to-value correspondence would change the evidence grade.
- **Further decipherment of the Bing-section arithmetic**: if a value-placement procedure is confirmed in the `三積算子` family of problems, the sequential-accumulation reading behind B would gain strength.

## 7. Verdict

Both remain unconfirmed. Their legitimacy differs in kind:

- **A** is a candidate with strong internal coherence (the naming, the family precedents, the pair structure), but it lacks direct transcription and is not logically derivable from the aggregate conditions.
- **B** is the procedurally simplest candidate and meshes exactly with the cell-count series, but it conflicts with the diagram's name and with the balance grammar of the whole book, and it departs structurally from every measured balance indicator.

On the current textual evidence, A cannot be raised above "strong internal reconstruction candidate", and B cannot be raised above "simple procedural candidate". Neither can be asserted as the original placement of the text.

Reproduction: A via `python3 main.py` (parent), B via `python3 yukgodo2/solver.py`, indicator comparison via `python3 yukgodo2/compare.py`.
