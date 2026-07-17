# Jungsang-yonggudo (象上用九圖) — Modern Graph & Combinatorial Analysis Report

> A modern mathematical re-reading of the Jungsang-yonggudo diagram from the 《Gusuryak (九數略)》 family.
> **Subject**: the integers 1–33 placed on four axes of 9 cells each, all sharing the center cell 9 — an eight-rayed star.
> Source commentary: 「斜直四行 周圍四重 各得一百四十七數」 ("the four slanting and straight lines and the four surrounding rings each obtain 147"), 「本積五百六十一」 ("base total 561"), 「演積一千一百四十八」 ("expanded total 1148"), 「三十三子作 七十二子用」 ("33 made, 72 used").

---

## 1. Basic structure and checksums

### 1.1 Data summary

Jungsang-yonggudo consists of four axes (vertical, horizontal, two diagonals) sharing the center 9. Each axis is a straight line of 9 cells: 4 cells on each side of the center.

| Axis | 9 cells (one end → other end) | Sum |
|:---:|:---|:---:|
| Vertical | 20, 16, 23, 10, 9, 2, 29, 32, 6 | 147 |
| Horizontal | 28, 5, 11, 25, 9, 7, 19, 31, 12 | 147 |
| Diagonal 1 | 27, 15, 3, 24, 9, 30, 14, 21, 4 | 147 |
| Diagonal 2 | 33, 1, 13, 22, 9, 18, 26, 17, 8 | 147 |

- **Values used**: 1 through 33, once each (三十三子作)
- **Total**: 561 (= 1+2+...+33, matching 本積五百六十一)
- **Number of axes**: 4 (斜直四行)
- **Sum per axis**: 147 (matching 各得一百四十七數)
- **Checksum**: 4 × 147 = 588 = 561 + 27, where 27 = 3 × 9 is the duplicated use of the center 9

### 1.2 Duplication count (make / use)

The four axes cover 36 cells (= 4 × 9) but only 33 distinct values exist; the center 9 is used in all four axes.

```
k·S = T + D   ⇔   4 × 147 = 588 = 561 + 3×9
```

- **make 33, use 36** (axes only): 33 values fill 36 cells.
- Every non-center value belongs to exactly one axis (one ray).

The title's 「七十二子用」 ("72 used") reads as an extended accounting that also counts the four rings (周圍四重) as 9 cells each (8 ring cells + center): 36 + 36 = 72 (see §4.4, §5).

> Observation 1: the only duplication is the center 9, and D = 3×9 = 27 matches the axis-sum excess (588 − 561) exactly.

---

## 2. Graph-theoretic analysis

### 2.1 Graph construction

Define the graph `G` by connecting values adjacent along each axis.

- Nodes: 33
- Edges: 32 (= 4 axes × 8 edges)
- Connected components: 1
- **Tree** (connected, acyclic): a spider tree of 8 rays (spokes) of length 4 radiating from the center 9
- Diameter: 8 (tip → center → opposite tip)

### 2.2 Degree distribution

| Degree | Count | Nodes |
|:---:|:---:|:---|
| 8 | 1 | center 9 |
| 2 | 24 | the 24 nodes of rings d1, d2, d3 |
| 1 | 8 | the 8 endpoints of ring d4 |

> Observation 2: degree is completely determined by distance from the center. The center 9 is the only branching point (degree 8).

### 2.3 Cycle analysis

`G` is a tree, so the cycle basis is empty and girth is undefined. The structural units are the 8 rays and the 4 concentric octagonal rings (d1–d4) around the center (§4).

> Observation 3: unlike diagrams built on polygon cycles (e.g. Gichaek-yongpaldo), Jungsang-yonggudo is a pure tree of eight rays. Geometrically, however, connecting each distance level yields four octagons (8-cycles) — see the rotation analysis.

### 2.4 Centrality analysis

Betweenness centrality, top 10:

| Rank | Node | Wuxing | Role | Betweenness |
|:---:|:---:|:---:|:---:|:---:|
| 1 | 9 | Metal | center | 0.903 |
| 2 | 2 | Fire | d1 | 0.175 |
| 2 | 7 | Fire | d1 | 0.175 |
| 2 | 10 | Earth | d1 | 0.175 |
| 2 | 18 | Wood | d1 | 0.175 |
| 2 | 22 | Fire | d1 | 0.175 |
| 2 | 24 | Metal | d1 | 0.175 |
| 2 | 25 | Earth | d1 | 0.175 |
| 2 | 30 | Earth | d1 | 0.175 |
| 10 | 3 | Wood | d2 | 0.121 |

> Observation 4: the center's betweenness 0.903 is overwhelming — every shortest path between nodes on different rays passes through it. The eight d1 nodes tie at 0.175, followed by d2 at 0.121; within a ring the values are exactly equal.

---

## 3. Wuxing (五行) mod-5 analysis

### 3.1 Classes and sums

| Wuxing | mod 5 | Values | Count | Sum |
|:---:|:---:|:---|:---:|:---:|
| Water | 1 | 1, 6, 11, 16, 21, 26, 31 | 7 | 112 |
| Fire | 2 | 2, 7, 12, 17, 22, 27, 32 | 7 | 119 |
| Wood | 3 | 3, 8, 13, 18, 23, 28, 33 | 7 | 126 |
| Metal | 4 | 4, 9, 14, 19, 24, 29 | 6 | 99 |
| Earth | 5 | 5, 10, 15, 20, 25, 30 | 6 | 105 |

> Observation 5: the three 7-value classes (Water/Fire/Wood) sum to 112, 119, 126 — an arithmetic progression with difference 7. The two 6-value classes (Metal/Earth) keep difference 6 (99, 105). Since 33 = 5×7 − 2, the last two classes have 6 values. The center 9 belongs to Metal.

### 3.2 Wuxing composition per axis

| Axis | Wuxing distribution |
|:---:|:---|
| Vertical | Earth 2, Fire 2, Metal 2, Water 2, Wood 1 |
| Horizontal | Earth 2, Fire 2, Metal 2, Water 2, Wood 1 |
| Diagonal 1 | Earth 2, Fire 1, Metal 4, Water 1, Wood 1 |
| Diagonal 2 | Fire 2, Metal 1, Water 2, Wood 4 |

> Observation 6: the vertical and horizontal axes have identical wuxing distributions (Earth/Fire/Metal/Water two each, Wood one). Different wuxing mixtures realize the same sum 147 — a flexible design.

### 3.3 Edge wuxing relations

Classifying all 32 edges:

| Type | Count | Share |
|:---:|:---:|:---:|
| Overcoming (相剋) | 17 | 53.1% |
| Generation (相生) | 14 | 43.8% |
| Same phase | 1 | 3.1% |
| Neutral | 0 | 0% |

> Observation 7: overcoming edges dominate at 53.1%. Only a single same-phase edge exists — almost every adjacent pair mixes phases.

---

## 4. Positional analysis (rays / concentric rings / axis decomposition)

### 4.1 Ray-sum invariant

The 8 rays (4 cells each) radiating from the center 9:

| Ray | Nodes (center → outward) | Sum |
|:---:|:---|:---:|
| N | 10, 23, 16, 20 | 69 |
| S | 2, 29, 32, 6 | 69 |
| W | 25, 11, 5, 28 | 69 |
| E | 7, 19, 31, 12 | 69 |
| NW | 24, 3, 15, 27 | 69 |
| SE | 30, 14, 21, 4 | 69 |
| NE | 22, 13, 1, 33 | 69 |
| SW | 18, 26, 17, 8 | 69 |

> Observation 8: **all eight rays sum to 69.** This is the direct source of the axis sum 147 = 69 + 9 + 69, and the core principle of the whole design (the same device as Beomsu-yongodo's arm sums of 10 and Jangchaek-yongchildo's spoke-pair sums of 61).

### 4.2 Concentric ring-sum invariant

Grouping the 32 outer nodes by graph distance from the center gives four octagonal rings:

| Ring | Nodes | Sum |
|:---:|:---|:---:|
| d1 (distance 1) | 2, 7, 10, 18, 22, 24, 25, 30 | 138 |
| d2 (distance 2) | 3, 11, 13, 14, 19, 23, 26, 29 | 138 |
| d3 (distance 3) | 1, 5, 15, 16, 17, 21, 31, 32 | 138 |
| d4 (distance 4) | 4, 6, 8, 12, 20, 27, 28, 33 | 138 |

> Observation 9: **all four rings sum to 138 = (561 − 9)/4** (周圍四重). Adding the center 9 to any ring gives 147, matching the source's 「周圍四重 各得一百四十七數」 — consistent with the 「七十二子用」 reading in which the ring accounting includes the center.

### 4.3 Axis decomposition

```
each axis = ray + center + ray   ⇔   147 = 69 + 9 + 69   (all four axes)
```

> Observation 10: the single ray invariant (69) explains both the axis sum 147 (stated in the source) and the ring sum 138. Since all eight rays sum to 69, any opposite pair of rays forms an axis summing to 147.

### 4.4 Examining 演積 1148

The source records the duplication-inclusive total as 「演積一千一百四十八」. Candidate accountings:

| Accounting | Computation | Value |
|:---|:---|:---:|
| 4 axes only (measured 147) | 4 × 147 | 588 |
| axes + 4 rings (measured 138) | 588 + 552 | 1140 |
| axes + rings + center once | 1140 + 9 | 1149 |
| 用72 accounting (axes 36 + rings-with-center 36) | 588 + 588 | 1176 |

> Observation 11: no natural accounting yields exactly 1148 (the closest is 1149, off by one). This may be transcription damage in the surviving edition or an accounting convention not yet identified; we record it here as an unresolved discrepancy, in the same spirit as the transcription-damage policy used for the 03-magic-squares series.

---

## 5. Generalization family

Jungsang-yonggudo belongs to the star family of the 《Gusuryak》 lineage (a axes × L cells per axis, center L):

| Diagram | a (axes) | L (cells) | N = a(L−1)+1 | T = N(N+1)/2 | Axis sum S | Ring sum R = (T−L)/a |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| Beomsu-yongodo (範數用五圖) | 2 | 5 | 9 | 45 | 25 | 20 |
| Jangchaek-yongchildo (章策用七圖) | 3 | 7 | 19 | 190 | 68 | 61 |
| **Jungsang-yonggudo (象上用九圖)** | **4** | **9** | **33** | **561** | **147** | **138** |

Common relations: the center equals L; from k·S = T + (a−1)·L we get S = (T + (a−1)·L)/a and ring sum R = (T − L)/a.

> Observation 12: Jungsang-yonggudo is the a=4, L=9 member. All three diagrams use 1..N once, center on L, and satisfy the equal-axis/equal-ring relations — an observed common pattern. Moreover all three share the same design device of a **same-ray sum invariant** (Beomsu: arm 10; Jangchaek: spoke-pair 61; Jungsang: ray 69). Whether such placements exist for arbitrary (a, L) remains an open question.

---

## 6. Spectral analysis

The adjacency matrix is 33×33 symmetric.

- λ_max ≈ 3.0233
- λ_min ≈ −3.0233
- The spectrum is symmetric about the origin

> Observation 13: as a tree, `G` is bipartite and its spectrum is origin-symmetric (λ_min = −λ_max). λ_max ≈ 3.02 exceeds √8 ≈ 2.83 (the star K₁,₈), reflecting the spread of centrality along the longer rays. Within the star family, λ_max grows monotonically: Beomsu (√5 ≈ 2.236) < Jangchaek (≈ 2.676) < Jungsang (≈ 3.023).

---

## 7. Conclusion

Jungsang-yonggudo is an elaborate combinatorial structure: the integers 1–33 on four 9-cell axes (eight rays) sharing the center 9.

### Key findings

1. **Four 9-cell axes**: each sums to 147 (matching 斜直四行 各得一百四十七數); only the center 9 is used four times.
2. **Duplication equation**: 4 × 147 = 588 = 561 + 3×9 (make 33, use 36; 本積 561 confirmed).
3. **Spider tree**: 33 nodes, 32 edges, acyclic, degree distribution {8: 1, 2: 24, 1: 8}, diameter 8.
4. **Center betweenness 0.903**: overwhelming; all eight d1 nodes tie at 0.175.
5. **Ray sums 69 (×8)**: the source of every sum invariant — axis 147 = 69+9+69.
6. **Ring-sum invariant**: d1 = d2 = d3 = d4 = 138 = (561−9)/4 (周圍四重); with the center, 147 — matching the source.
7. **Wuxing arithmetic**: Water 112, Fire 119, Wood 126 (difference 7); Metal 99, Earth 105 (difference 6).
8. **Overcoming edges dominate**: overcoming 53.1%, generation 43.8%, same-phase 3.1%.
9. **Bipartite spectrum**: λ_max = −λ_min ≈ 3.0233, monotone within the star family.
10. **演積 1148 unresolved**: natural accountings give 1140/1149/1176 — recorded as possible transcription damage or an unidentified accounting.
11. **Star-family member**: a=4, L=9 — shares the relations and the same-ray device with Beomsu (a=2) and Jangchaek (a=3).

---

## 8. Generated figures

Running `analyze_jungsang_yonggudo.py` produces these 8 images:

- `01_original_graph.png` — original 4-axis star structure (wuxing colors + ring guides)
- `02_wuxing_decomposition.png` — per-phase subgraph decomposition
- `03_adjacency_spectrum.png` — adjacency matrix + graph spectrum
- `04_cycle_analysis.png` — tree structure (no cycles) and concentric ring levels
- `05_centrality_invariants.png` — degree, betweenness, wuxing sums, axis sums
- `06_wuxing_relations.png` — wuxing generation/overcoming + edge classification
- `07_local_extensions.png` — star family (a×L) comparison and skeleton schematic
- `08_position_patterns.png` — ray/ring sum analysis

Running `analyze_rotations.py` additionally produces `rotation_report.txt`, eight per-cluster `rotation_cluster_*.png` figures, and `rotation_overview.png`.
