# Antipodal-Complement Audit

## Verdict

`v(c)+v(-c)=271` is **not logically derived** from the presently deciphered Naejeok Method and the geometric values. Lo Shu complementary pair sums, `通加洛書數六倍`, `54+6=60`, centrally symmetric geometry, and the complementary set 1…270 form strong internal coherence. The Bing-section `圓束樣式` adds a geometrical precedent for a vacant centre; its `一百四十四隻` uses `隻` to count one member of each pair, adding a strong internal precedent for the antipodal-pair unit as well.

The documentation therefore distinguishes the following two levels.

| Level | Assessment |
| --- | --- |
| 271 cells; 虛一; outer perimeter 54; side length 10; 中觚 19; `19+2×((10+18)×9/2)=271` | Directly or strongly supported by the text and geometry |
| An antipodal pair’s values sum to 271 | Strong reconstruction condition; no direct wording connecting position and value has been found |

The precedent in the second method (二之四) of *Taiyin Numbers* (〈太陰之數〉) is a minimal model: leave the centre’s unique fixed point empty, and retain the surroundings as pairs (7→6=2×3). It has the same structure as the Yukgodo’s `271→270=2×135`. See the corresponding README section for the full transcription and schematic.

## Hypothesis-removal experiment

The existing `yukgodo.solver` initially places `(i, 271-i)` in all 135 antipodal slots. That model can find a witness solution under the hypothesis, but it cannot test whether antipodal complements follow from the other conditions. To avoid this limitation, `yukgodo.antipodal_audit` swaps the values of two cells with identical structural memberships in a stored conditional witness solution.

To reproduce:

```bash
python3 tests/test_antipodal_audit.py
python3 -m yukgodo.antipodal_audit
```

In the 2026-08-09 run, it swapped the values `10` and `124` of two cells, `(-9,1)` and `(-9,2)`, which are both in outer ring 9 and side 5, and in no 中觚 axis. The results were as follows.

| Condition | Result |
| --- | --- |
| Value set | 1…270 used once each; total 36585 retained |
| Ring sums | `813, 1626, …, 7317` all retained |
| Axis sums | `2439, 2439, 2439` retained |
| Six side sums | 1355 each retained |
| Sector sums | All remain 6097 or 6098 |
| Ray sums | All remain 1219 or 1220 |
| Antipodal sum 271 | Only 133 of 135 pairs hold; total absolute deviation 228 |

Therefore, even with the other balance targets and these aggregate values used by the current solver, antipodal complements are not necessary. An exhaustive scan of the same type of local swap across the conditional witness solution finds more than 500 valid swaps. This is not an isolated exception accidentally found in a vast solution space; it is a structural fact that aggregate constraints cannot substitute for position–value equivariance.

![Local countermodel for aggregate proxy constraints](output/antipodal_countermodel.png)

This countermodel does not mean that there is little historical reason to adopt the principle, nor that the source rejects antipodal complements. It is only a counterfactual constructed by intentionally removing `v∘τ=κ_{271}∘v` for the test. Thus, it is a boundary that prevents logical certainty above 90 percent; it is not negative evidence that by itself lowers the interpretive plausibility of the source.

## Relation to the decipherment of the Naejeok Method

The most coherent latter calculation network has the following geometrical accumulated-count interpretation:

\[
271 = 19 + 2\left(\frac{10+18}{2}\times9\right).
\]

It explains the 中觚 and the decomposition into two isomorphic trapezoidal-field (梯田) regions. However, here 271 is the total number of cells; the confirmed text contains no sentence such as `對觚相合二百七十一` or `相對二數合二百七十一` that instructs the antipodal sum of cell values. The strengthened Naejeok decipherment and the strong internal motivation for the antipodal-complement reconstruction principle are therefore recognised, but they are not merged into the same evidential level.
