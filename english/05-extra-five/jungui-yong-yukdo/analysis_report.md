# Jungui-yongyukdo (重儀用六圖) — Modern Graph & Combinatorial Analysis Report

> A modern mathematical re-reading of the Jungui-yongyukdo diagram from the 《Gusuryak (九數略)》 family.
> **Subject**: the integers 1–16 placed in four overlapping 6-value groups (top/left/bottom/right), each group summing to 51.
> All figures were computed and verified by running `analyze_jungui_yongyukdo.py`.

---

## 1. Basic structure and checksums

### 1.1 Data summary

Jungui-yongyukdo consists of four groups (top, left, bottom, right), each holding 6 values and summing to 51.

| Group | 6 values | Sum |
|:---:|:---|:---:|
| top | 7, 16, 1, 6, 11, 10 | 51 |
| left | 7, 13, 11, 3, 9, 8 | 51 |
| bottom | 8, 2, 9, 12, 15, 5 | 51 |
| right | 6, 10, 4, 12, 14, 5 | 51 |

- **Values used**: 1 through 16, once each (make 16)
- **Group memberships**: 24 (use 24)
- **Total**: T = 136
- **Number of groups**: k = 4
- **Sum per group**: S = 51

### 1.2 Shared pairs and the duplication equation

Adjacent groups share exactly 2 values; diagonal pairs (top∩bottom, left∩right) share none.

| Shared pair | Location | Sum |
|:---:|:---:|:---:|
| {7, 11} | top ∩ left | 18 |
| {6, 10} | top ∩ right | 16 |
| {8, 9} | left ∩ bottom | 17 |
| {5, 12} | right ∩ bottom | 17 |

The 8 shared values (5, 6, 7, 8, 9, 10, 11, 12) are counted twice when summing group totals:

```
k·S = T + D
4 × 51 = 204 = 136 + 68
```

where D = 68 is the sum of the 8 shared values.

> Observation 1: the shared sum D = 68 is exactly half of T = 136, so S = (T + D)/4 = 3T/8 = 51 holds automatically. The 8 unshared values (1, 2, 3, 4, 13, 14, 15, 16) also sum to 68.

### 1.3 Complement-pair (sum 17) decomposition per group

For each group's 6 values, all 15 perfect matchings were checked for a decomposition into 3 pairs each summing to 17 (= N+1).

| Group | Sum-17 matching | Pairs |
|:---:|:---:|:---|
| top | **possible** | (1,16), (6,11), (7,10) |
| bottom | **possible** | (2,15), (5,12), (8,9) |
| left | impossible | the complements of 7 (10), 13 (4), 11 (6), 3 (14) are absent |
| right | impossible | the complements of 6 (11), 10 (7), 4 (13), 14 (3) are absent |

> Observation 2: only the top and bottom groups decompose cleanly into three complement pairs (51 = 3 × 17). The left and right groups gave up this device to accommodate the shared pairs. This top/bottom vs. left/right asymmetry is a key design feature of the placement.

---

## 2. Graph-theoretic analysis

### 2.1 Graph constructions

Two natural graph structures are defined.

**T-forest `G_T`**: the four T-shaped arrows drawn in the source diagram.
- Nodes: 16
- Edges: 12
- Components: 4 (each a T-star K(1,3))

**Co-membership graph `G_co`**: connect every pair of values belonging to the same group (each group = a K6 clique).
- Nodes: 16
- Edges: 56 (= 4 × C(6,2) − 4; the 4 shared-pair edges are counted in two cliques)
- Components: 1

### 2.2 Degree distribution

**`G_T`**:
- degree 3: the four T-centers {5, 6, 7, 8}
- degree 1: the 12 spokes {1, 2, 3, 4, 9, 10, 11, 12, 13, 14, 15, 16}

**`G_co`**:
- degree 9: the 8 shared values (5 + 5 − 1 distinct neighbors across two groups)
- degree 5: the 8 unshared values (5 neighbors within one group)

> Observation 3: the T-centers {5, 6, 7, 8} are four consecutive integers summing to 26; the 12 spokes sum to 110, and 26 + 110 = 136 = T.

### 2.3 Cycle analysis

- `G_T` is a forest: no cycles (girth undefined).
- `G_co` has girth 3; a smallest-cycle example is the triangle 7-16-11-7 inside the top group's K6. Cycle rank: 56 − 16 + 1 = 41.

> Observation 4: the connections actually drawn in the source (the T-forest) contain no cycles at all. Unlike the ring-based diagrams of this family, Jungui-yongyukdo realizes its cyclic structure solely through group overlap (shared pairs).

### 2.4 Centrality analysis

Betweenness centrality in the co-membership graph `G_co`:

| Rank | Nodes | Role | Betweenness |
|:---:|:---:|:---:|:---:|
| 1 (tie) | 5, 6, 7, 8, 9, 10, 11, 12 | shared 8 | 0.0857 (= 3/35) |
| 9 (tie) | 1, 2, 3, 4, 13, 14, 15, 16 | unshared 8 | 0.0000 |

In the T-forest only the four T-centers have nonzero betweenness, 0.0286 (= 1/35).

> Observation 5: betweenness in the co-membership graph takes exactly two values — 3/35 for every shared value and 0 for every unshared one. The shared values are quantitatively confirmed as the only passages (hinges) between groups.

---

## 3. Wuxing (五行) mod-5 analysis

### 3.1 Classes and sums

| Wuxing | mod 5 | Values | Count | Sum |
|:---:|:---:|:---|:---:|:---:|
| Water | 1 | 1, 6, 11, 16 | 4 | 34 |
| Fire | 2 | 2, 7, 12 | 3 | 21 |
| Wood | 3 | 3, 8, 13 | 3 | 24 |
| Metal | 4 | 4, 9, 14 | 3 | 27 |
| Earth | 5 | 5, 10, 15 | 3 | 30 |

> Observation 6: since 16 is not a multiple of 5, only Water has 4 values. The Fire→Wood→Metal→Earth sums 21, 24, 27, 30 form an arithmetic progression with difference 3; Water's 34 lies outside it.

### 3.2 Wuxing composition per group

| Group | Wuxing distribution |
|:---:|:---|
| top | Water 4, Fire 1, Earth 1 |
| left | Wood 3, Fire 1, Water 1, Metal 1 |
| bottom | Earth 2, Fire 2, Wood 1, Metal 1 |
| right | Earth 2, Metal 2, Water 1, Fire 1 |

> Observation 7: the top group is extremely skewed, containing all four Water values (1, 6, 11, 16), while the bottom and right groups show balanced 2-2-1-1 distributions. The group sum 51 survives very different wuxing mixtures — the same "equal sum from different phase combinations" design seen in Gujagakdeuk.

### 3.3 Edge wuxing relations

Edges of both graphs classified into generation/overcoming/same-phase (no neutral edges can exist):

| Type | T-forest (12 edges) | Co-membership (56 edges) |
|:---:|:---:|:---:|
| Generation (相生) | 5 (41.7%) | 23 (41.1%) |
| Overcoming (相剋) | 4 (33.3%) | 20 (35.7%) |
| Same phase | 3 (25.0%) | 13 (23.2%) |

> Observation 8: both graphs show generation > overcoming > same-phase with nearly identical ratios — the statistics come from the placement itself, not from the choice of edge definition.

---

## 4. Positional analysis (rings / roles / rows)

### 4.1 Ring levels

The 16 positions split into a perimeter 12-ring and an inner 4-ring (rectangle).

| Ring | Members (clockwise) | Sum |
|:---:|:---|:---:|
| perimeter 12-ring | 7, 16, 1, 6, 4, 14, 5, 15, 2, 8, 3, 13 | 94 |
| inner 4-ring | 11, 10, 12, 9 | 42 |

Note 94 + 42 = 136 = T.

### 4.2 Sums by role

| Role | Values | Sum |
|:---:|:---|:---:|
| 4 T-centers | 5, 6, 7, 8 | 26 |
| 12 T-spokes | 1, 2, 3, 4, 9, 10, 11, 12, 13, 14, 15, 16 | 110 |
| shared 8 | 5, 6, 7, 8, 9, 10, 11, 12 | 68 |
| unshared 8 | 1, 2, 3, 4, 13, 14, 15, 16 | 68 |

> Observation 9: the shared and unshared 8-value sums are exactly equal at 68 (cf. Observation 1). The shared set {5,...,12} and the unshared set {1..4} ∪ {13..16} also split cleanly on the number line.

### 4.3 Row sums by y-coordinate

| y | Values | Row sum |
|:---:|:---|:---:|
| +3.2 | 16, 1 | 17 |
| +3.0 | 7, 6 | 13 |
| +1.5 | 13, 4 | 17 |
| +1.0 | 11, 10 | 21 |
| −1.0 | 9, 12 | 21 |
| −1.5 | 3, 14 | 17 |
| −3.0 | 8, 5 | 13 |
| −3.2 | 2, 15 | 17 |

> Observation 10: the row-sum sequence 17, 13, 17, 21, 21, 17, 13, 17 is a palindrome — row sums are preserved under top–bottom reflection.

### 4.4 Left–right mirror pairs

Sums of position pairs mirrored across the y-axis (x ↔ −x):

| Pair | (7,6) | (16,1) | (13,4) | (11,10) | (3,14) | (9,12) | (8,5) | (2,15) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Sum | 13 | 17 | 17 | 21 | 17 | 21 | 13 | 17 |

> Observation 11: of the 8 mirror pairs, 4 sum to 17 (= N+1), 2 to 13, and 2 to 21. Since 13 + 21 = 34 = 2 × 17, the deviations cancel exactly, and the mean pair sum is 17 = 136/8.

---

## 5. Generalization family

The structural principles of Jungui-yongyukdo, recorded as observations (no claim about actual variant diagrams):

- **Frame**: values 1..16 (N = 16) in four 6-value groups, adjacent groups sharing 2 values (make 16, use 24). The group sum is fixed by k·S = T + D, i.e. S = (T + D)/4.
- **Complement-pair device**: filling a group with pairs summing to N+1 = 17 automatically yields the group sum 3 × 17 = 51. The top and bottom groups implement this device fully.
- **Link to the magic-square tradition**: in 1..16, pairs summing to 17 are the same device that fills opposite cells of a 4×4 magic square (magic constant 34 = 2 × 17). Jungui-yongyukdo reads as a transplant of that device into an overlapping-group structure.
- **Role of the asymmetry**: the left and right groups abandoned pair decomposition to accept the four shared-pair hinges (§1.3). A fully symmetric placement satisfying both the complement device and the shared-pair constraints is not realized in this data.

> Observation 12: Jungui-yongyukdo can be read as combining the magic-square tradition's "pairs summing to N+1" construction device with the Gakdeuk family's "four groups linked by shared pairs" overlap structure.

---

## 6. Spectral analysis

Adjacency-matrix eigenvalues of the two graphs (`numpy.linalg.eigvalsh`):

**Co-membership graph `G_co`** (16×16 symmetric):
- λ_max ≈ 7.4721
- λ_min = −3.0000 (exactly −3)
- Spectrum: {−3, −1.8284 (×2), −1.4721, −1 (×8), 1, 3.8284 (×2), 7.4721}

**T-forest `G_T`**:
- λ_max = √3 ≈ 1.7321 (multiplicity 4)
- λ_min = −√3 ≈ −1.7321 (multiplicity 4)
- the remaining 8 eigenvalues are 0

> Observation 13: the T-forest spectrum is exactly four copies of the K(1,3)-star spectrum (±√3, 0, 0) — the forest structure shows up verbatim. The co-membership λ_max ≈ 7.47 sits close to the mean degree 7 (= 2 × 56/16), and the integral λ_min = −3 reflects the regularly overlapping four-clique symmetry.

---

## 7. Conclusion

Jungui-yongyukdo is an elaborate combinatorial structure placing 1..16 in four overlapping 6-value groups, all summing to 51.

### Key findings

1. **Duplication equation k·S = T + D**: 4 × 51 = 204 = 136 + 68 — the shared sum 68 is exactly half the total.
2. **Shared 8 = unshared 8 = 68**: {5..12} and {1..4, 13..16} have equal sums.
3. **T-centers are 4 consecutive integers**: {5, 6, 7, 8}, sum 26; spokes sum 110.
4. **Complement-pair asymmetry**: only the top and bottom groups decompose into three sum-17 pairs (51 = 3 × 17).
5. **Shared-pair sums**: 18, 16, 17, 17 — different at every hinge.
6. **T-forest is a forest**: the 12 drawn edges are 4 cycle-free T-stars; cyclic structure arises only from group overlap.
7. **Co-membership graph**: 56 edges, degree 9 (shared) / 5 (unshared), girth 3, cycle rank 41.
8. **Two-level betweenness**: shared values all 3/35, unshared all 0 — the hinge role quantified.
9. **Row-sum palindrome**: 17, 13, 17, 21, 21, 17, 13, 17 — top–bottom symmetric.
10. **Graph-independent wuxing statistics**: generation > overcoming > same-phase in both graphs (~41/36/23%).
11. **Spectra**: co-membership λ_max ≈ 7.47, λ_min = −3 (integral); T-forest ±√3 (×4) and 0 (×8), matching K(1,3) × 4.
12. **Device shared with magic squares**: complement pairs summing to N+1 = 17 (Observation 12).

---

## 8. Generated figures

Running `analyze_jungui_yongyukdo.py` produces these 8 images:

- `01_original_graph.png` — original structure (wuxing-colored nodes + group ellipses + T edges)
- `02_wuxing_decomposition.png` — per-phase subgraph decomposition
- `03_adjacency_spectrum.png` — co-membership adjacency matrix + spectrum comparison of both graphs
- `04_cycle_analysis.png` — T-forest, smallest-cycle example, ring levels, cycle summary
- `05_centrality_invariants.png` — degree, betweenness, wuxing sums, group sums
- `06_wuxing_relations.png` — wuxing pentagram + edge-relation classification
- `07_local_extensions.png` — structural blueprint (shared-pair hinges) + complement device and asymmetry
- `08_position_patterns.png` — positional roles (rings/T-centers), positional subset sums, row-sum palindrome

In addition, `analyze_rotations.py` produces the rotation analysis outputs (`rotation_report.txt`, six `rotation_cluster_*.png` figures, `rotation_overview.png`): mod-5 residue patterns and opposite sums of the perimeter 12-cycle, the inner 4-cycle, and the four groups, plus the 180° global rotation symmetry of the group centroids (top↔bottom, left↔right).
