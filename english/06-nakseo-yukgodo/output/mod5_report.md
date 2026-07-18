# 洛書六觚圖 mod-5 Residue Analysis

Values v are classified by v mod 5 (1 black · 2 red · 3 blue · 4 gray ·
0 yellow). 270 cells = 5 classes × 54 cells. Layer sums: residue 1 = 7209,
residue 2 = 7263, residue 3 = 7317, residue 4 = 7371, residue 0 = 7425
(determined by the value space).

## 1. Exhaustive inter-layer D6 congruence check (240 = 5×4 ordered pairs × 12 elements)

**Congruent pairs: residue 2 ↔ residue 4, residue 1 ↔ residue 0 (180° rotation = point symmetry).**

| Layer | → Layer | Symmetry element |
|---|---|---|
| residue 0 | residue 1 | 180° rotation |
| residue 1 | residue 0 | 180° rotation |
| residue 2 | residue 4 | 180° rotation |
| residue 4 | residue 2 | 180° rotation |

D6 maximum overlap over all ordered pairs (54/54 = exact congruence):

| Pair | Max overlap | Achieving element |
|---|---|---|
| residue 0 ↔ residue 1 | 54/54 | 180° rotation **(congruent)** |
| residue 0 ↔ residue 2 | 17/54 | reflection + 180° rotation |
| residue 0 ↔ residue 3 | 13/54 | reflection + 60° rotation |
| residue 0 ↔ residue 4 | 17/54 | reflection + 0° rotation |
| residue 1 ↔ residue 2 | 17/54 | reflection + 0° rotation |
| residue 1 ↔ residue 3 | 13/54 | reflection + 60° rotation |
| residue 1 ↔ residue 4 | 17/54 | reflection + 180° rotation |
| residue 2 ↔ residue 3 | 16/54 | reflection + 120° rotation |
| residue 2 ↔ residue 4 | 54/54 | 180° rotation **(congruent)** |
| residue 3 ↔ residue 4 | 16/54 | reflection + 120° rotation |

## 2. Layer self-symmetry (stabilizers)

| Layer | Self-symmetry elements |
|---|---|
| residue 1 | 0° rotation |
| residue 2 | 0° rotation |
| residue 3 | 0° rotation, 180° rotation |
| residue 4 | 0° rotation |
| residue 0 | 0° rotation |

## 3. The antipode's action on residue classes — pair sum 271 ≡ 1 (mod 5)

Since antipodal pairs sum to 271, the residue classes must act as
r ↦ (1−r) mod 5. Measured mismatched pairs: **0** (must be 0).

| Layer | Antipode image |
|---|---|
| residue 1 | residue 0 |
| residue 2 | residue 4 |
| residue 3 | residue 3 |
| residue 4 | residue 2 |
| residue 0 | residue 1 |

Antipode pairing matrix A[i][j] = number of cells whose antipode of a
layer-i cell lies in layer j (if all off-diagonal entries are 0, the layers
are closed):

| | residue0 | residue1 | residue2 | residue3 | residue4 |
|---|---|---|---|---|---|
| residue0 | 0 | 54 | 0 | 0 | 0 |
| residue1 | 54 | 0 | 0 | 0 | 0 |
| residue2 | 0 | 0 | 0 | 0 | 54 |
| residue3 | 0 | 0 | 0 | 54 | 0 |
| residue4 | 0 | 0 | 54 | 0 | 0 |

Reading: A[0][1] = A[1][0] = 54 (layers 0 and 1 are each other's antipode
image), A[2][4] = A[4][2] = 54 (layers 2 and 4 are each other's antipode
image), A[3][3] = 54 (layer 3 is its own antipode image — 27 point-symmetric
pairs). This is all of the congruence in §1: the 180°-rotation congruence of
0↔1 and 2↔4 and the self-symmetry of layer 3 are nothing but the mod-5
residue action r ↦ 1−r of the antipodal pair sum 271.
Proof figure: `mod5_symmetry.png` (colored layer vs. the antipode image ○ of
the opposite layer, overlaid).

## 4. Per-layer adjacency structure (networkx induced subgraphs)

| Layer | Internal edges | Component size sequence |
|---|---|---|
| residue 1 | 29 | [5, 4, 4, 4, 3, 3, 3, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] |
| residue 2 | 34 | [9, 6, 4, 4, 4, 4, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] |
| residue 3 | 24 | [4, 4, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] |
| residue 4 | 34 | [9, 6, 4, 4, 4, 4, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] |
| residue 0 | 29 | [5, 4, 4, 4, 3, 3, 3, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] |

Shape-isomorphic (graph-isomorphic) pairs:
- residue 0 ↔ residue 1: **isomorphic** (VF2 verdict)
- residue 0 ↔ residue 2: non-isomorphic (signature mismatch (VF2 skipped))
- residue 0 ↔ residue 3: non-isomorphic (signature mismatch (VF2 skipped))
- residue 0 ↔ residue 4: non-isomorphic (signature mismatch (VF2 skipped))
- residue 1 ↔ residue 2: non-isomorphic (signature mismatch (VF2 skipped))
- residue 1 ↔ residue 3: non-isomorphic (signature mismatch (VF2 skipped))
- residue 1 ↔ residue 4: non-isomorphic (signature mismatch (VF2 skipped))
- residue 2 ↔ residue 3: non-isomorphic (signature mismatch (VF2 skipped))
- residue 2 ↔ residue 4: **isomorphic** (VF2 verdict)
- residue 3 ↔ residue 4: non-isomorphic (signature mismatch (VF2 skipped))

## 5. Inter-layer adjacency quotient matrix M[i][j] (number of layer-i–layer-j adjacency edges)

| | residue0 | residue1 | residue2 | residue3 | residue4 |
|---|---|---|---|---|---|
| residue0 | 29 | 58 | 60 | 62 | 56 |
| residue1 | 58 | 29 | 56 | 62 | 60 |
| residue2 | 60 | 56 | 34 | 61 | 64 |
| residue3 | 62 | 62 | 61 | 24 | 61 |
| residue4 | 56 | 60 | 64 | 61 | 34 |

## 6. Per-layer distribution deviation (χ² against uniformity)

| Layer | Sector χ² (expected 9) | Ray χ² (expected 1.8) | Ring χ² (expected 1.2k) |
|---|---|---|---|
| residue 1 | 5.33 | 1.91 | 9.37 |
| residue 2 | 3.33 | 4.47 | 6.59 |
| residue 3 | 12.44 | 14.36 | 15.38 |
| residue 4 | 3.33 | 4.47 | 6.59 |
| residue 0 | 5.33 | 1.91 | 9.37 |

## 7. The value-shift map T: position(v) → position(v+5)

- Cycle structure: [54, 54, 54, 54, 54] (five cycles of length 54 = 270/5, as expected)
- Walk-distance distribution: {1: 4, 2: 12, 3: 16, 4: 16, 5: 24, 6: 8, 7: 26, 8: 24, 9: 32, 10: 15, 11: 18, 12: 20, 13: 16, 14: 14, 15: 10, 16: 8, 17: 4, 18: 3}
- Best match against D6 elements: 2/270 cells at reflection + 60° rotation (would have to be 270 if it were a structural rotation)

## 8. Derived theorem — mod-N generalization (record)

**Theorem.** If a value placement has a positional involution π (π² = id)
and every pair of values sums to a constant S, then for every modulus m, π
acts on the mod-m residue classes as **r ↦ (S − r) mod m**. Hence residue
layers are either congruent to each other under π-symmetry (orbits of
length 2) or self-congruent (fixed points: the solutions of
2r ≡ S (mod m)).

Reason (4 steps):
1. Reducing the pair condition v + v′ = S mod m gives v′ ≡ S − v — it holds
   cell by cell.
2. The action on residue classes is the single involution r ↦ S − r, and the
   orbits of an involution are either pairs of length 2 or fixed points
   (2r ≡ S).
3. Since π is one-to-one and the layer sizes are finite,
   π(layer r) ⊆ layer (S−r) is already set equality — the reason the overlap
   is exact rather than approximate.
4. In this diagram π is central point symmetry = 180° rotation, so the layer
   congruences are realized within the lattice symmetry group D6 (verified
   by the exhaustive check in §1).

Corollary (parity of the pair sum):
- If S is odd, no self-paired (fixed) cell value can exist — this diagram's
  S = 271 (odd) and the central 虛一 are consistent with it.
- If S is even, a fixed cell's value is forced to be S/2 — the center
  23 = 46/2 of the Guja-gakdeuk (九子角得) center palace is an example.

Cross-diagram verification (`python3 -m yukgodo.modn_generalization`,
exhaustive over moduli 2..9):

| Diagram | Pair sum S | π (positional involution) | Result |
|---|---|---|---|
| 06 洛書六觚圖 (this optimum) | 271 | central point symmetry (global 180° rotation) | exact for all of mod 2..9 |
| 02 九子角得 center palace | 46 | 3×3 central symmetry | exact for all of mod 2..9; self-pair 23 = S/2 |
| 07 重卦用八圖 horizontal formation | 65 | left-right flip within a row (local) | exact for all of mod 2..9 |
| 07 侯策用九圖 | ≈73 (imperfect) | formation position pairs | breaks when mixed (12 off-orbit entries); exact when restricted to the 16 pairs summing to 73 |

The 侯策用九圖 case demonstrates the necessity of the condition: when the
pair sums are not constant, the action does not gather into r ↦ S−r but
splits into the per-pair actual sums.

Significance and limits: **every** solution satisfying the antipodal-pair
hypothesis (including the seed-42 optimum) has this property, so it carries
no discriminating power for the original placement. However, mod-5 coloring
is a technique used repeatedly across the Gusuryak analyses
(Ojagakdeuk's mod5_residue_diagram.py, the Hado-Saodo 5-coloring documents),
and this theorem generalizes that component-pair cross-check to arbitrary
mod N. It is a falsification tool in the sense that if the actual diagram of
a clearer edition did not have this symmetry, the antipodal
complementary-pair hypothesis would be rejected.
