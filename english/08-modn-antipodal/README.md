# 08. Mod-N Residue Generalization for Diagrams with Positionally Symmetric Complementary Pairs

A cross-chapter analysis of the residue symmetry that the positionally
symmetric complementary-pair structure (position pairs whose values sum to a
constant) — common to the Gusuryak diagrams — produces for arbitrary
moduli. The verification code lives in the `korean/06-nakseo-yukgodo/`
project.

## Background: the mod-5 coloring tradition

Mod-5 residue coloring is an analysis technique used repeatedly throughout
this repository.

- `01-saodo-family/hado-saodo-5-coloring/` — the analysis that the
  Hado-Saodo is effectively a 5-coloring problem
- `02-gakdeuk-series/ojagakdeuk-five-each-gets/mod5_residue_diagram.py` —
  diagramming the mod-5 residue groups of the values
- `06-nakseo-yukgodo/yukgodo/mod5.py` — splits the reconstructed optimum
  into five layers by mod-5 residue (54 cells each) and exhaustively checks
  all 12 D6 symmetry elements against every layer pair

The fact found in chapter 06's exhaustive check: the residue 2↔4 and 1↔0
layers are exactly congruent (54/54) under 180° rotation (point symmetry),
the residue-3 layer is self-symmetric, and no other symmetry exists (the
best overlap of any other pair is 13–17/54 = noise level). This chapter
states and verifies that the finding is not special to mod 5 or to the
Yukgodo, but generalizes to every diagram with positionally symmetric
complementary pairs.

## Derived theorem

**Theorem.** If a value placement has a positional involution π (π² = id)
and every pair of values sums to a constant S, then for every modulus m, π
acts on the mod-m residue classes as

```
r ↦ (S − r) mod m
```

Hence residue layers are either congruent to each other under π-symmetry
(orbits of length 2) or self-congruent (fixed points: the solutions of
2r ≡ S (mod m)).

**Reason (4 steps).**

1. Reducing the pair condition v + v′ = S mod m gives v′ ≡ S − v, cell by
   cell.
2. The action on residue classes is the single involution r ↦ S − r, and
   the orbits of an involution are either pairs of length 2 or fixed points
   (2r ≡ S).
3. Since π is one-to-one and the layer sizes are finite,
   π(layer r) ⊆ layer (S−r) is already set equality — the reason the
   overlap is exact rather than approximate.
4. If π is a geometric symmetry of the lattice (e.g. the Yukgodo's central
   point symmetry = 180° rotation), the layer congruences are realized
   within the lattice symmetry group.

**Corollary (parity of the pair sum).**

- If S is odd, no self-paired fixed cell value can exist — the fixed cell
  must be empty. The Yukgodo's S = 271 (odd) and the central 虛一 are
  consistent with this.
- If S is even, a fixed cell's value is forced to be S/2. The center
  23 = 46/2 of the Guja-gakdeuk center palace is an example.

## Cross-diagram verification

`python3 -m yukgodo.modn_generalization` (the 06 project), exhaustive over
moduli 2..9. It checks the antipode pairing matrix A[i][j] (the number of
pairs in which a cell with value ≡ i has an antipode value ≡ j) for whether
every nonzero entry lies on an (i, S−i) orbit.

| Diagram | Pair sum S | Positional involution π | Result |
|---|---|---|---|
| 06 洛書六觚圖 (reconstructed optimum) | 271 | central point symmetry (global 180° rotation) | exact for all of mod 2..9 |
| 02 九子角得 center palace | 46 | 3×3 central symmetry | all exact; self-pair 23 = S/2 |
| 07 重卦用八圖 horizontal formation (Paljin-do) | 65 | left-right flip within a row (local symmetry) | all exact |
| 07 侯策用九圖 | ≈73 (imperfect) | formation position pairs | breaks when mixed (12 off-orbit entries); exact when restricted to the 16 pairs summing to 73 |

侯策用九圖 demonstrates the necessity of the condition: when the pair sums
are not constant (16 pairs of 73, 9 pairs of 74, 7 pairs of 72, 4 outlier
pairs), the residue action does not gather into r ↦ S−r but splits into the
per-pair actual sums. Restricting to the pairs summing to 73 makes the
pattern exact again.

### Orbit structure at mod 5 (by S)

| S mod 5 | Orbits | Fixed points |
|---|---|---|
| 271 ≡ 1 (Yukgodo) | {0,1} {2,4} | {3} |
| 46 ≡ 1 (Guja-gakdeuk center palace) | {0,1} {2,4} | {3} |
| 65 ≡ 0 (Paljin-do horizontal formation) | {1,4} {2,3} | {0} |

Since the Yukgodo and the Guja-gakdeuk center palace share S ≡ 1 (mod 5)
and hence the same orbit structure, the same pairings (0↔1, 2↔4, 3 self)
appear under mod-5 coloring.

## Significance and limits

1. **Generalization of the component-pair cross-check.** The
   complementary-pair verification that each chapter performed with mod-5
   colored components is justified by this theorem as the same procedure at
   arbitrary mod N.
2. **A falsification tool.** Any reconstruction claiming positionally
   symmetric complementary pairs must exhibit the corresponding orbit
   structure. If an actual edition violates it, the complementary-pair
   hypothesis is rejected.
3. **No discriminating power (a limit).** Every placement satisfying the
   constant pair-sum condition has this property (even the Yukgodo's
   distinct optima all do), so it cannot by itself identify the original
   placement.

## Reproduction

```bash
cd korean/06-nakseo-yukgodo
python3 -m yukgodo.mod5                   # mod-5 coloring + exhaustive five-layer D6/networkx analysis
python3 -m yukgodo.modn_generalization    # the mod-N theorem — cross-diagram verification (mod 2..9)
```

## Data sources

- 06 洛書六觚圖: `06-nakseo-yukgodo/output/solution.json` (135 antipodal pairs, sum 271)
- 02 九子角得 center palace: `02-gakdeuk-series/gujagakdeuk-nine-each-gets/analyze_gujagakdeuk.py:61-65`
  (center palace 3×3, 4 opposite pairs summing to 46, center 23)
- 07 重卦用八圖 horizontal formation: `07-extra-two/junggwae-yong-paldo/visualize_corrected.py:139-144,210-215`
  (8 left-right pairs, sum 65)
- 07 侯策用九圖: `07-extra-two/huchaek-yong-gudo/visualize.py:91-167`
  (9 formations × 4 position pairs; pair-sum distribution {67:1, 68:1, 72:7, 73:16, 74:9, 75:1, 78:1})
