# Beomsu-yongodo (範數用五圖) — Modern Graph & Combinatorial Analysis Report

> A modern mathematical re-reading of the Beomsu-yongodo diagram from the 《Gusuryak (九數略)》 family.
> **Subject**: the integers 1–9 placed on two axes of a cross (+) shape — a horizontal 5-cell line and a vertical 5-cell line — sharing the center cell 5.

---

## 1. Basic structure and checksums

### 1.1 Data summary

Beomsu-yongodo consists of two 5-cell axes sharing the center 5.

| Axis | 5 values | Sum |
|:---:|:---|:---:|
| Horizontal | 3, 7, 5, 4, 6 | 25 |
| Vertical | 2, 8, 5, 1, 9 | 25 |

- **Values used**: 1 through 9, once each
- **Total**: 45
- **Number of axes**: 2
- **Sum per axis**: 25
- **Checksum**: 2 × 25 = 50 = 45 + 5

### 1.2 Duplication equation

Summing both axes counts the center 5 twice. In the form `k·S = T + D`:

```
2 × 25 = 50 = 45 + 5        (k=2, S=25, T=45, D=5)
```

Nine numbers are made (作) and ten positions are used (用); the duplication D = 5 is exactly the center value.

### 1.3 The cross layout

```
        2
        8
3 — 7 — 5 — 4 — 6
        1
        9
```

From the center 5, four arms extend: up (2, 8), down (9, 1), left (3, 7), right (6, 4).

---

## 2. Graph-theoretic analysis

### 2.1 Graph construction

Define the graph `G` with cells as nodes and adjacency along the axes as edges.

- Nodes: 9
- Edges: 8 — (3,7), (7,5), (5,4), (4,6), (2,8), (8,5), (5,1), (1,9)
- Connected components: 1
- Cycles: none (empty cycle basis)

> Observation 1: with 8 edges = 9 nodes − 1 and connected, `G` is a **tree** — precisely the starlike tree S(2,2,2,2) with four arms of length 2 from the center. Unlike the Gakdeuk diagrams built from cycles, Beomsu-yongodo has no cycles at all. Its diameter is 4 (e.g. 3-7-5-4-6), radius 2, and the graph center is the single node 5.

### 2.2 Degree distribution

Degree sequence: `[4, 2, 2, 2, 2, 1, 1, 1, 1]` (mean degree 16/9 ≈ 1.78)

| Degree | Count | Nodes | Positional role |
|:---:|:---:|:---|:---|
| 4 | 1 | 5 | center |
| 2 | 4 | 7, 4, 8, 1 | inner ring (midpoints) |
| 1 | 4 | 3, 6, 2, 9 | outer ring (endpoints) |

> Observation 2: the degree distribution matches the geometric roles exactly — the center, inner ring, and outer ring can be recovered from topology alone.

### 2.3 Cycle analysis

Being a tree, the graph has no cycles and girth is undefined. The structural unit is instead the distance level from the center: distance 0 (1 cell), distance 1 (inner ring, 4 cells), distance 2 (outer ring, 4 cells). (`04_cycle_analysis.png` visualizes this ring/level structure instead.)

### 2.4 Centrality analysis

Betweenness centrality (all 9 nodes):

| Rank | Node | Wuxing | Role | Betweenness |
|:---:|:---:|:---:|:---:|:---:|
| 1 | 5 | Earth | center | 0.857 |
| 2 | 1 | Water | inner | 0.250 |
| 2 | 4 | Metal | inner | 0.250 |
| 2 | 7 | Fire | inner | 0.250 |
| 2 | 8 | Wood | inner | 0.250 |
| 6 | 2 | Fire | outer | 0.000 |
| 6 | 3 | Wood | outer | 0.000 |
| 6 | 6 | Water | outer | 0.000 |
| 6 | 9 | Metal | outer | 0.000 |

> Observation 3: the center's betweenness is 6/7 ≈ 0.857. Among the 28 pairs of the other 8 nodes, the 24 pairs on different arms all have shortest paths through the center (24/28 = 6/7). Each inner-ring node is a bridge for its own arm's endpoint only (0.250); endpoints score 0.

---

## 3. Wuxing (五行) mod-5 analysis

### 3.1 Classes and sums

| Wuxing | mod 5 | Values | Sum |
|:---:|:---:|:---|:---:|
| Water | 1 | 1, 6 | 7 |
| Fire | 2 | 2, 7 | 9 |
| Wood | 3 | 3, 8 | 11 |
| Metal | 4 | 4, 9 | 13 |
| Earth | 5 | 5 | 5 |

> Observation 4: the four doubled phases (Water/Fire/Wood/Metal) sum to 7, 9, 11, 13 — an arithmetic progression with difference 2. Earth is the single center 5.

### 3.2 Wuxing composition per axis

| Axis | Wuxing sequence | Distribution |
|:---:|:---|:---|
| Horizontal | Wood → Fire → Earth → Metal → Water | all five phases, once each |
| Vertical | Fire → Wood → Earth → Water → Metal | all five phases, once each |

> Observation 5: **each axis contains all five phases exactly once (wuxing complete set).** Both axes realize the sum 25 by the same "one of each phase" principle.

> Observation 6: reading the horizontal axis left to right gives 3(Wood) → 7(Fire) → 5(Earth) → 4(Metal) → 6(Water) — exactly the generation cycle **Wood→Fire→Earth→Metal→Water**. All four horizontal edges are generation pairs.

### 3.3 Edge wuxing relations

Classifying all 8 edges:

| Type | Count | Share | Edges |
|:---:|:---:|:---:|:---|
| Generation (相生) | 6 | 75.0% | (3,7), (7,5), (5,4), (4,6), (2,8), (1,9) |
| Overcoming (相剋) | 2 | 25.0% | (8,5) Wood–Earth, (5,1) Earth–Water |
| Same phase | 0 | 0.0% | — |

> Observation 7: generation edges dominate at 75%. Both overcoming edges touch the center 5 on the vertical axis. Since any two distinct phases are always related, neutral edges cannot occur.

---

## 4. Positional analysis (center / rings / arms / antipodal pairs)

The 9 cells split into the center (1), the inner ring (4 midpoints), and the outer ring (4 endpoints). A same-direction inner+outer pair is called an arm.

| Part | Values | Sum |
|:---:|:---|:---:|
| Center | 5 | 5 |
| Arm up | 2, 8 | 10 |
| Arm right | 6, 4 | 10 |
| Arm down | 9, 1 | 10 |
| Arm left | 3, 7 | 10 |
| Inner ring (8, 4, 1, 7) | — | 20 |
| Outer ring (2, 6, 9, 3) | — | 20 |

> Observation 8: **all four arms sum to 10 (= 2 × center 5).** The complementary pairs summing to 10 — (1,9), (2,8), (3,7), (4,6) — are placed on the same rays. This is the direct source of the axis sum 25 = 10 + 10 + 5, and the core principle of the whole design.

> Observation 9: inner ring sum = outer ring sum = 20 = (45 − 5)/2. The equal ring sums follow automatically once every arm sums to 10.

Antipodal pair sums alternate:

| Antipodal pair | Sum |
|:---:|:---:|
| outer left–right (3, 6) | 9 |
| outer up–down (2, 9) | 11 |
| inner left–right (7, 4) | 11 |
| inner up–down (8, 1) | 9 |

> Observation 10: antipodal sums alternate between 9 and 11 (horizontal: outer 9 / inner 11; vertical: outer 11 / inner 9). In either ring the two pairs total 9 + 11 = 20, the full ring sum.

---

## 5. Generalization family

Beomsu-yongodo is observed to belong, together with two other 05-extra-five diagrams, to an **equal-axis/equal-ring star family**. With `a` axes and `L` cells per axis (the 用 number):

```
N = a(L−1) + 1        (number of values; the center is shared by a axes)
T = N(N+1)/2          (total)
S = (T + (a−1)·L)/a   (axis sum; the center is counted a times)
R = (T − L)/a         (equal sum of the concentric distance rings)
```

| Diagram | axes a × L | N | center (= 用) | T | axis sum S | ring sum R |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Beomsu-yongodo (範數用五圖) | 2 × 5 | 9 | 5 | 45 | 25 | 20 |
| Jangchaek-yongchildo (章策用七圖) | 3 × 7 | 19 | 7 | 190 | 68 | 61 |
| Jungsang-yonggudo (象上用九圖) | 4 × 9 | 33 | 9 | 561 | 147 | 138 |

> Observation 11: in all three diagrams **the 用 number = axis length = center value** (用五→5, 用七→7, 用九→9), and N, S, R match the formulas exactly. The values for Beomsu-yongodo are verified directly in this report (S=25, R=20); the Jangchaek and Jungsang values are the stated figures from their own analyses (68/61, 147/138), checked only for formula consistency. This is a pattern observed across three instances; whether such equal-axis/equal-ring placements exist for arbitrary (a, L) is beyond this report's scope.

---

## 6. Spectral analysis

The adjacency matrix is 9×9 symmetric. Eigenvalues (descending):

```
+2.2361, +1, +1, +1, 0, −1, −1, −1, −2.2361
```

- λ_max = √5 ≈ 2.2361
- λ_min = −√5 ≈ −2.2361
- The spectrum is symmetric about the origin

> Observation 12: a tree is bipartite, so spectral symmetry and λ_min = −λ_max follow automatically. λ_max = √5 matches the largest eigenvalue of the quotient matrix [[0,4,0],[1,0,1],[0,1,0]] of the equitable partition {center}, {inner ring}, {outer ring}.

---

## 7. Conclusion

Beomsu-yongodo is the smallest and most transparent combinatorial structure in this collection: the integers 1–9 on two 5-cell axes.

### Key findings

1. **1–9 once each, both axes sum to 25**: duplication equation 2·25 = 45 + 5 (9 made, 10 used).
2. **9-node 8-edge tree**: the starlike tree S(2,2,2,2) with four arms of length 2.
3. **Degree = positional role**: center degree 4, inner ring 2, outer ring 1.
4. **Center betweenness 6/7 ≈ 0.857**: 24 of 28 shortest paths pass through the center.
5. **Wuxing complete set**: each axis contains all five phases exactly once.
6. **Horizontal axis = generation chain**: left→right reads Wood→Fire→Earth→Metal→Water (100% generation edges).
7. **Edge relations**: generation 6 (75.0%), overcoming 2 (25.0%, both adjacent to the center on the vertical axis), same-phase 0.
8. **Arm sums = 10 (×4)**: complementary 10-pairs placed on the same rays — the source of every sum invariant.
9. **Inner = outer = 20**: equal-ring invariant R = (45 − 5)/2; antipodal pairs alternate 9/11.
10. **Spectrum λ_max = √5**: origin-symmetric (bipartite tree), matching the quotient matrix.
11. **Equal-axis/equal-ring star family**: Beomsu (2 axes, 用五) — Jangchaek (3 axes, 用七) — Jungsang (4 axes, 用九) share N = a(L−1)+1, S = (T+(a−1)L)/a, R = (T−L)/a (observed pattern).

---

## 8. Generated figures

Running `analyze_beomsu_yongodo.py` produces these 8 images:

- `01_original_graph.png` — original cross structure (wuxing colors + both axes)
- `02_wuxing_decomposition.png` — per-phase subgraph decomposition
- `03_adjacency_spectrum.png` — adjacency matrix + graph spectrum
- `04_cycle_analysis.png` — tree distance rings/levels and arm sums (no cycles)
- `05_centrality_invariants.png` — degree, betweenness, wuxing sums, structural subset sums
- `06_wuxing_relations.png` — wuxing generation/overcoming + edge classification
- `07_local_extensions.png` — the equal-axis/equal-ring star family (2, 3, and 4 axes)
- `08_position_patterns.png` — arm/ring/antipodal pair sum analysis

Running `analyze_rotations.py` additionally produces `rotation_report.txt`, four per-cluster `rotation_cluster_*.png` figures, and `rotation_overview.png`.
