# Jangchaek-yong-chil-do (章策用七圖) — Modern Graph and Combinatorial Analysis Report

> A reinterpretation of Jangchaek-yong-chil-do, one of the diagrams in the Gusuryak (九數略) series, in modern mathematical language.
> **Analysis target**: a star structure arranging the numbers 1 through 19 on three axes of 7 cells each, all sharing the central cell 7.

---

## 1. Basic Structure and Checksums

### 1.1 Data Summary

Jangchaek-yong-chil-do consists of three axes sharing the center 7. Each axis is a straight line of 7 cells: 3 cells on each side of the center.

| Axis | 7-cell arrangement (one end → opposite end) | Sum |
|:---:|:---|:---:|
| Vertical (90°) | 5, 18, 9, 7, 12, 2, 15 | 68 |
| Diagonal (150°) | 4, 10, 19, 7, 1, 14, 13 | 68 |
| Diagonal (30°) | 8, 6, 17, 7, 3, 11, 16 | 68 |

- **Values used**: 1 through 19, each exactly once
- **Total sum**: 190 (= 1+2+...+19)
- **Number of axes**: 3
- **Sum of each axis**: 68
- **Checksum**: 3 × 68 = 204 = 190 + 14, where 14 = 2 × 7 accounts for the triple use of the center 7

### 1.2 Duplication Count (make / use)

From the cell perspective, the 21 cells (= 3 axes × 7 cells) are filled with only 19 distinct values. Since the center 7 is used three times across the axes:

```
k·S = T + D   ⇔   3 × 68 = 204 = 190 + 2×7
```

- **make 19, use 21**: 19 values fill 21 cells.
- Every value other than the center belongs to exactly one axis.

> Observation 1: The only duplication is the center 7, and the duplicated amount D = 2×7 = 14 matches exactly the excess of the axis-sum total (204 − 190).

---

## 2. Graph-Theoretic Analysis

### 2.1 Graph Construction

Define the graph `G` by connecting values adjacent along each axis.

- Nodes: 19
- Edges: 18 (= 3 axes × 6 edges)
- Connected components: 1
- **Tree** (connected graph without cycles): a spider tree made of six spokes of length 3 radiating from the center 7

### 2.2 Degree Distribution

| Degree | Node count | Nodes |
|:---:|:---:|:---|
| 6 | 1 | center 7 |
| 2 | 12 | the 12 nodes of rings d1 and d2 |
| 1 | 6 | the 6 endpoints of ring d3 |

> Observation 2: The degree is completely determined by position (distance from the center). The center 7, with degree 6, is the only branching point of the whole structure.

### 2.3 Cycle Analysis

Since `G` is a tree, its cycle basis is empty and the girth (minimum cycle length) is undefined. Instead, the structure is described by 6 spokes and 3 concentric rings (d1, d2, d3) around the center (see §4).

> Observation 3: Unlike the palaces of Paljagakdeuk or Gujagakdeuk, which rest on cycle-based grids, the skeleton of Jangchaek-yong-chil-do is a pure tree with no cycles at all.

### 2.4 Centrality Analysis

Top 10 nodes by betweenness centrality:

| Rank | Node | Phase | Position | Betweenness |
|:---:|:---:|:---:|:---:|:---:|
| 1 | 7 | Fire | center | 0.882 |
| 2 | 1 | Water | d1 | 0.209 |
| 2 | 3 | Wood | d1 | 0.209 |
| 2 | 9 | Metal | d1 | 0.209 |
| 2 | 12 | Fire | d1 | 0.209 |
| 2 | 17 | Fire | d1 | 0.209 |
| 2 | 19 | Metal | d1 | 0.209 |
| 8 | 2 | Fire | d2 | 0.111 |
| 8 | 6 | Water | d2 | 0.111 |
| 8 | 10 | Earth | d2 | 0.111 |

> Observation 4: The center 7 dominates with betweenness 0.882, because every shortest path between nodes on different spokes (135 pairs) passes through it. Next come the six d1 nodes (0.209), then the six d2 nodes (0.111); values within one ring are exactly equal.

---

## 3. Wuxing (五行) mod 5 Analysis

### 3.1 Classification and Sums by Phase

| Phase | mod 5 | Values | Sum |
|:---:|:---:|:---|:---:|
| Water (水) | 1 | 1, 6, 11, 16 | 34 |
| Fire (火) | 2 | 2, 7, 12, 17 | 38 |
| Wood (木) | 3 | 3, 8, 13, 18 | 42 |
| Metal (金) | 4 | 4, 9, 14, 19 | 46 |
| Earth (土) | 5 | 5, 10, 15 | 30 |

> Observation 5: Listed in the order Earth, Water, Fire, Wood, Metal, the class sums 30, 34, 38, 42, 46 form an arithmetic sequence with common difference 4. This is the result of removing 20 (an Earth value) from the class sums of 1~20 (34, 38, 42, 46, 50): 50 − 20 = 30, yet the arithmetic pattern survives. The center 7 belongs to Fire.

### 3.2 Wuxing Composition per Axis

| Axis | Phase distribution |
|:---:|:---|
| Vertical (90°) | Fire ×3, Earth ×2, Wood ×1, Metal ×1 |
| Diagonal (150°) | Metal ×3, Water ×1, Fire ×1, Wood ×1, Earth ×1 |
| Diagonal (30°) | Water ×3, Wood ×2, Fire ×2 |

> Observation 6: Only the 150° diagonal contains all five phases. The three axes use different phase combinations, yet all sum to 68 — a flexible design achieving the same sum from different wuxing mixtures.

### 3.3 Wuxing Relations of Edges

Classifying all 18 edges by wuxing relation:

| Edge type | Count | Share |
|:---:|:---:|:---:|
| Generation (相生) | 7 | 38.9% |
| Overcoming (相剋) | 7 | 38.9% |
| Same phase | 4 | 22.2% |
| Neutral (no direct relation) | 0 | 0% |

> Observation 7: Generation and overcoming edges are exactly tied at 7 each. Since any two distinct phases are always related by generation or overcoming, there are no neutral edges.

---

## 4. Position-Based Analysis (Rings / Spokes / Antipodal Pairs)

### 4.1 Sum Invariant of the Concentric Rings

By graph distance from the center 7, the 18 outer nodes split into three hexagonal rings.

| Ring | Nodes | Sum |
|:---:|:---|:---:|
| Inner d1 | 9, 12, 19, 1, 17, 3 | 61 |
| Middle d2 | 18, 2, 10, 14, 6, 11 | 61 |
| Outer d3 | 5, 15, 4, 13, 8, 16 | 61 |

> Observation 8: **All three rings sum to exactly 61.** This matches R = (190 − 7)/3 = 61, and despite the crossing axes of the star, the distribution is perfectly uniform at the ring level — the key positional invariant of Jangchaek-yong-chil-do.

### 4.2 Spoke (Half-Ray) Sums

Splitting each axis at the center gives 6 spokes (3 cells from endpoint toward center):

| Spoke | Nodes | Sum |
|:---:|:---|:---:|
| Vertical top | 5, 18, 9 | 32 |
| Vertical bottom | 12, 2, 15 | 29 |
| 150° upper-left | 4, 10, 19 | 33 |
| 150° lower-right | 1, 14, 13 | 28 |
| 30° upper-right | 8, 6, 17 | 31 |
| 30° lower-left | 3, 11, 16 | 30 |

> Observation 9: Sorted, the spoke sums are **28, 29, 30, 31, 32, 33 — exactly six consecutive integers**. Opposite spokes on the same axis sum to 61 (equal to the ring sum).

### 4.3 Antipodal-Pair Sum Matrix

Arranging the sums of antipodal pairs (two values at the same distance from the center on one axis) by axis × level:

| Axis \ Level | d1 pair | d2 pair | d3 pair | Row sum |
|:---:|:---:|:---:|:---:|:---:|
| Vertical (90°) | 9+12=21 | 18+2=20 | 5+15=20 | 61 |
| Diagonal (150°) | 19+1=20 | 10+14=24 | 4+13=17 | 61 |
| Diagonal (30°) | 17+3=20 | 6+11=17 | 8+16=24 | 61 |
| **Column sum** | **61** | **61** | **61** | |

> Observation 10: This 3×3 pair-sum matrix is a **semi-magic square with row sums and column sums all equal to 61**. The row sums restate the axis sum 68 (= 61 + center 7), while the column sums refine the ring invariant (Observation 8) to the pair level. Pair sums take only the values 17, 20, 21, 24; 20 is twice the mean of 1..19 (the ideal pair sum).

---

## 5. Generalization Family

Jangchaek-yong-chil-do belongs to a family of Gusuryak star diagrams (a axes × L cells per axis, center L).

| Diagram | a (axes) | L (cells/axis) | N = a(L−1)+1 | T = N(N+1)/2 | Axis sum S | Ring sum R = (T−L)/a |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| Beomsu-yong-odo (範數用五圖) | 2 | 5 | 9 | 45 | 25 | 20 |
| **Jangchaek-yong-chil-do (章策用七圖)** | **3** | **7** | **19** | **190** | **68** | **61** |
| Jungsang-yong-gudo (中上用九圖) | 4 | 9 | 33 | 561 | 147 | 138 |

Common relations: the center is L; from the duplication equation k·S = T + (a−1)·L one gets S = (T + (a−1)·L)/a, and the ring sum is R = (T − L)/a.

> Observation 11: Jangchaek-yong-chil-do is the a=3, L=7 member of this family. All three diagrams use 1~N once each, place L at the center, and satisfy the same axis-sum and ring-sum uniformity relations — an observed common pattern. However, whether such an arrangement exists for arbitrary (a, L) cannot be decided from this data alone; this is an observed family resemblance, not a proven general theorem.

---

## 6. Graph Spectral Analysis

The adjacency matrix is a 19×19 symmetric matrix.

- Largest eigenvalue: λ_max ≈ 2.6762
- Smallest eigenvalue: λ_min ≈ −2.6762
- The spectrum is exactly symmetric about the origin

> Observation 12: Since `G` is a tree, it is bipartite, and bipartite adjacency spectra are symmetric about 0 — indeed λ_min = −λ_max holds to within numerical precision. The value λ_max ≈ 2.68 exceeds √6 ≈ 2.45 of the perfect star K₁,₆, reflecting the diluted concentration as the spokes lengthen.

---

## 7. Conclusion

Jangchaek-yong-chil-do is an elaborate combinatorial structure placing 1~19 on three 7-cell axes that share only the center 7.

### Key Findings

1. **3 axes × 7 cells star**: every axis sums to 68; only the center 7 is used three times.
2. **Duplication equation**: 3 × 68 = 204 = 190 + 2×7 (make 19, use 21).
3. **Spider tree**: 19 nodes, 18 edges, no cycles; degree distribution {6: 1, 2: 12, 1: 6}.
4. **Dominant center 7**: betweenness 0.882, the topological hub of the whole structure.
5. **Arithmetic wuxing sums**: Earth 30 → Water 34 → Fire 38 → Wood 42 → Metal 46 (common difference 4).
6. **Tied generation/overcoming edges**: 7 each (38.9%), plus 4 same-phase edges (22.2%).
7. **Ring sum invariant**: d1 = d2 = d3 = 61 = (190−7)/3 — the strongest positional invariant.
8. **Consecutive spoke sums**: 28, 29, 30, 31, 32, 33; opposite spokes sum to 61.
9. **Semi-magic pair-sum matrix**: the 3×3 antipodal-pair sums have row sums = column sums = 61.
10. **Member of the star family**: a=3, L=7 — shares the same relations with Beomsu-yong-odo (a=2, L=5) and Jungsang-yong-gudo (a=4, L=9).
11. **Bipartite spectrum**: λ_max = −λ_min ≈ 2.6762, the origin-symmetric spectrum of a tree.

---

## 8. Generated Figures

Running `analyze_jangchaek_yongchildo.py` produces the following 8 figures.

- `01_original_graph.png` — original 3-axis structure (wuxing colors + concentric ring guides)
- `02_wuxing_decomposition.png` — subgraph decomposition by wuxing phase
- `03_adjacency_spectrum.png` — adjacency matrix + graph spectrum
- `04_cycle_analysis.png` — tree structure (no cycles) and concentric ring levels
- `05_centrality_invariants.png` — degree, betweenness, wuxing sums, axis sums
- `06_wuxing_relations.png` — wuxing generation/overcoming pentagram + edge distribution
- `07_local_extensions.png` — star family (a×L) comparison and skeleton schematics
- `08_position_patterns.png` — ring/spoke sums and the antipodal-pair sum matrix
