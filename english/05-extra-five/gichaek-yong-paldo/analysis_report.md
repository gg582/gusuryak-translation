# Gichaek-yongpaldo (奇策用八圖) — Modern Graph & Combinatorial Analysis Report

> A modern mathematical re-reading of the Gichaek-yongpaldo diagram from the 《Gusuryak (九數略)》 family.
> **Subject**: the integers 1–24 placed eight at a time on the vertices of four regular octagons; adjacent octagons share one complete edge (two vertices).

---

## 1. Basic structure and checksums

### 1.1 Data summary

Gichaek-yongpaldo consists of four regular octagons (Top/Left/Right/Bottom) arranged around a central square. Each octagon is a filled 8-vertex cycle.

| Octagon | 8 values (cyclic order) | Sum |
|:---:|:---|:---:|
| Top | 4, 9, 14, 23, 5, 8, 19, 18 | 100 |
| Left | 8, 5, 15, 22, 3, 10, 20, 17 | 100 |
| Right | 1, 12, 18, 19, 6, 7, 13, 24 | 100 |
| Bottom | 7, 6, 17, 20, 2, 11, 16, 21 | 100 |

- **Values used**: 1 through 24, once each (24 made)
- **Total T**: 300
- **Number of octagons k**: 4
- **Sum per octagon S**: 100
- **Checksum**: 4 × 100 = 400 = 300 + 100

### 1.2 Shared edges and the duplication equation

Adjacent octagons share one edge (two vertices).

| Shared edge | Vertices |
|:---:|:---:|
| Top ∩ Left | {5, 8} |
| Top ∩ Right | {18, 19} |
| Left ∩ Bottom | {17, 20} |
| Right ∩ Bottom | {6, 7} |

The 8 shared vertices {5, 6, 7, 8, 17, 18, 19, 20} are counted in two octagons. Hence 32 uses (= 4 × 8) against 24 made values, with duplication D = 5+6+7+8+17+18+19+20 = 100.

$$k \cdot S = T + D \quad\Longrightarrow\quad 4 \times 100 = 300 + 100$$

> Observation 1: the duplication D = 100 equals the octagon sum S = 100 exactly — the eight shared vertices alone would fill one octagon.

---

## 2. Graph-theoretic analysis

### 2.1 Graph construction

**Octagon-cycle graph `G`**: nodes are the 24 vertices; edges are the octagon sides (shared edges counted once).

- Nodes: 24
- Edges: 28 (= 4 × 8 − 4 shared)
- Connected components: 1 (connected)
- Bipartite: yes (every face has even length)

### 2.2 Degree distribution

| Degree | Nodes | Values |
|:---:|:---:|:---|
| 3 | 8 | 5, 6, 7, 8, 17, 18, 19, 20 (shared vertices) |
| 2 | 16 | the rest (unique vertices) |

> Observation 2: a shared vertex has degree 3, not 4. Of the four octagon sides touching it, two are the same shared edge, so only 3 distinct edges remain in the union graph. The degree sum 8×3 + 16×2 = 56 = 2×28 matches the handshake lemma.

### 2.3 Cycle analysis

- **Cycle rank**: E − V + 1 = 28 − 24 + 1 = 5
- **Minimum cycle basis**: lengths [4, 8, 8, 8, 8] — one central square plus four octagon faces
- **Girth**: 4 (the central square)

> Observation 3: the face structure is exactly one patch of the truncated-square (4.8.8) tiling — one square and four octagons. The five bounded faces form a basis of the cycle space.

### 2.4 Centrality analysis

Betweenness centrality, top 10:

| Rank | Node | Wuxing | Degree | Betweenness |
|:---:|:---:|:---:|:---:|:---:|
| 1 | 8 | Wood | 3 | 0.290 |
| 1 | 19 | Metal | 3 | 0.290 |
| 1 | 6 | Water | 3 | 0.290 |
| 1 | 17 | Fire | 3 | 0.290 |
| 5 | 5 | Earth | 3 | 0.243 |
| 5 | 7 | Fire | 3 | 0.243 |
| 5 | 18 | Wood | 3 | 0.243 |
| 5 | 20 | Earth | 3 | 0.243 |
| 9 | 10 | Earth | 2 | 0.086 |
| 9 | 13 | Wood | 2 | 0.086 |

> Observation 4: the central square's four vertices {8, 19, 6, 17} tie for the highest betweenness (0.290), followed by the outer shared vertices {5, 7, 18, 20} (0.243). Betweenness takes exactly four levels (0.2905 ×4, 0.2431 ×4, 0.0860 ×8, 0.0464 ×8), matching the geometric ring structure (§4). (The 8 nodes after rank 9 tie at 0.0860; only the first two alphabetically are shown.)

---

## 3. Wuxing (五行) mod-5 analysis

### 3.1 Classes and sums

| Wuxing | mod 5 | Values | Count | Sum |
|:---:|:---:|:---|:---:|:---:|
| Water | 1 | 1, 6, 11, 16, 21 | 5 | 55 |
| Fire | 2 | 2, 7, 12, 17, 22 | 5 | 60 |
| Wood | 3 | 3, 8, 13, 18, 23 | 5 | 65 |
| Metal | 4 | 4, 9, 14, 19, 24 | 5 | 70 |
| Earth | 5 | 5, 10, 15, 20 | 4 | 50 |

> Observation 5: the Water/Fire/Wood/Metal class sums 55, 60, 65, 70 form an arithmetic progression with difference 5. Since 24 = 5×5 − 1, the Earth class alone has 4 values (sum 50), closing the progression. The five sums total 55+60+65+70+50 = 300.

### 3.2 Wuxing composition per octagon

| Octagon | Wuxing distribution |
|:---:|:---|
| Top | Metal 4, Wood 3, Earth 1 |
| Left | Earth 4, Wood 2, Fire 2 |
| Right | Water 2, Fire 2, Wood 2, Metal 2 |
| Bottom | Water 4, Fire 3, Earth 1 |

> Observation 6: the Right octagon is perfectly balanced across the four non-Earth phases (two each), while Top uses only Metal/Wood/Earth and Bottom only Water/Fire/Earth. Different wuxing mixtures realize the same sum 100 — a flexible design.

### 3.3 Edge wuxing relations

Classifying all 28 edges (the 5 generation pairs and 5 overcoming pairs cover every mixed pair, so neutral edges cannot exist):

| Edge type | Count | Share |
|:---:|:---:|:---:|
| Overcoming (相剋) | 13 | 46.4% |
| Generation (相生) | 9 | 32.1% |
| Same phase | 6 | 21.4% |
| Neutral | 0 | 0% |

> Observation 7: overcoming edges dominate at 46.4%, the same tendency as Gujagakdeuk (40.3%). The 6 same-phase edges are the only same-class adjacencies.

---

## 4. Positional analysis (shared/unique, central square, concentric rings, opposite pairs)

### 4.1 The 50/50 shared–unique split

Each octagon's 8 vertices split into 4 shared + 4 unique.

| Octagon | Shared 4 | Sum | Unique 4 | Sum |
|:---:|:---|:---:|:---|:---:|
| Top | 5, 8, 18, 19 | 50 | 4, 9, 14, 23 | 50 |
| Left | 5, 8, 17, 20 | 50 | 3, 10, 15, 22 | 50 |
| Right | 6, 7, 18, 19 | 50 | 1, 12, 13, 24 | 50 |
| Bottom | 6, 7, 17, 20 | 50 | 2, 11, 16, 21 | 50 |

> Observation 8: **in every octagon the four shared vertices and the four unique vertices both sum to exactly 50 = S/2** — the strongest positional invariant of Gichaek-yongpaldo.

### 4.2 The central square and the alternating split of the 8 shared vertices

Joining each octagon's inner edge (the edge facing the center) yields the 4-cycle 8 → 19 → 6 → 17 → 8; all four edges exist in the graph.

- Central square {8, 19, 6, 17}: sum 50
- Outer shared quadruple {5, 18, 7, 20}: sum 50

> Observation 9: the 8 shared vertices split into two alternating squares around the center, {8, 19, 6, 17} and {5, 18, 7, 20}, each summing to 50 = S/2. The inner four form the central square (the minimum cycle) and coincide exactly with the betweenness ranking (Observation 4).

### 4.3 Concentric rings

Grouping the 24 vertices by distance from the center gives four rings.

| Ring | Radius r | Vertices | Count | Sum |
|:---:|:---:|:---|:---:|:---:|
| 1 | ≈1.245 | 6, 8, 17, 19 | 4 | 50 |
| 2 | ≈3.005 | 5, 7, 18, 20 | 4 | 50 |
| 3 | ≈4.428 | 2, 4, 10, 12, 13, 15, 21, 23 | 8 | 100 |
| 4 | ≈5.205 | 1, 3, 9, 11, 14, 16, 22, 24 | 8 | 100 |

> Observation 10: the four concentric ring sums are 50, 50, 100, 100. Rings 1–2 are exactly the shared vertices (degree 3), rings 3–4 the unique ones (degree 2), and 50+50+100+100 = 300 restores the total.

### 4.4 Opposite-vertex pairs

For each octagon's cyclic order, the sums of positions i and i+4:

| Octagon | Pair 1 | Pair 2 | Pair 3 | Pair 4 |
|:---:|:---:|:---:|:---:|:---:|
| Top | 4+5=9 | 9+8=17 | 14+19=33 | 23+18=41 |
| Left | 8+3=11 | 5+10=15 | 15+20=35 | 22+17=39 |
| Right | 1+6=7 | 12+7=19 | 18+13=31 | 19+24=43 |
| Bottom | 7+2=9 | 6+11=17 | 17+16=33 | 20+21=41 |

> Observation 11: opposite-pair sums are not constant, but each octagon's four pair sums are symmetric about 25 and pair into complements of 50 (Top: 9+41 = 17+33 = 50, etc.). Top and Bottom share the identical multiset {9, 17, 33, 41}, and Right's sums 7, 19, 31, 43 form an arithmetic progression with difference 12.

---

## 5. Generalization family

Gichaek-yongpaldo belongs to the "equal-sum 8-cycle" design family (the 用八 class): several 8-cycles filled to the same sum. Comparison within the family:

| Diagram | 8-cycles | Value range | Cluster sum | Total |
|:---|:---:|:---:|:---:|:---:|
| Gichaek-yongpaldo (奇策用八圖) | 4 | 1–24 | 100 | 300 |
| Paljagakdeuk (八子各得) | 5 | 1–40 | 164 | 820 |

> Observation 12: both diagrams are equal-sum cycle designs built from 8-vertex cycles. Paljagakdeuk places five palaces in a cross with no shared vertices, while Gichaek-yongpaldo binds four octagons through shared edges — a structural difference. This is an observation of design-pattern similarity, not a lineage claim.

> Observation 13: the geometry (1 square + 4 octagons) is a patch of the 4.8.8 tiling, so a geometric extension adding more octagons around the outside is possible (see the schematic in figure 07). Whether an equal-sum placement exists on such an extension is outside the scope of this analysis.

---

## 6. Spectral analysis

The adjacency matrix of `G` is a 24×24 symmetric matrix.

- λ_max ≈ 2.6180 (= φ², where φ = (1+√5)/2 ≈ 1.618 is the golden ratio)
- λ_min ≈ −2.6180
- Symmetry: the spectrum is symmetric about the origin — consistent with the bipartite-spectrum theorem (§2.1)

> Observation 14: since the maximum degree is 3, λ_max < 3; the actual value is the square of the golden ratio, φ² = φ + 1 ≈ 2.618. λ_max = −λ_min re-confirms bipartiteness spectrally.

---

## 7. Conclusion

Gichaek-yongpaldo is an elaborate combinatorial structure in which four octagon 8-cycles are bound by shared edges around a central square.

### Key findings

1. **Four 8-cycles**: each octagon is a cycle of vertex sum 100.
2. **Duplication equation 4×100 = 300 + 100**: 32 uses = 24 made + 8 duplicated; D = 100 = S.
3. **Shared vertices have degree 3**: 8 shared (degree 3) + 16 unique (degree 2); connected bipartite graph.
4. **Cycle rank 5**: the central square (girth 4) plus four octagon faces form the minimum cycle basis.
5. **Central square sums to 50**: 8 → 19 → 6 → 17 → 8, matching the top-betweenness quadruple.
6. **Alternating split of the 8 shared vertices**: {8, 19, 6, 17} and {5, 18, 7, 20} each sum to 50 = S/2.
7. **50/50 split per octagon**: shared four sum = unique four sum = 50 — the strongest positional invariant.
8. **Ring sums 50, 50, 100, 100**: the four concentric rings match the degree/centrality structure.
9. **25-symmetry of opposite pairs**: each octagon's pair sums pair into complements summing to 50.
10. **Wuxing arithmetic progression**: Water 55, Fire 60, Wood 65, Metal 70 (step 5); Earth 50 (4 values).
11. **Overcoming edges dominate**: overcoming 46.4%, generation 32.1%, same-phase 21.4%.
12. **Spectrum λ_max = φ² ≈ 2.618**: origin-symmetric spectrum (bipartite graph).

---

## 8. Generated figures

Running `analyze_gichaek_yongpaldo.py` produces these 8 images:

- `01_original_graph.png` — original structure (wuxing-colored nodes, octagon regions, shared edges)
- `02_wuxing_decomposition.png` — per-phase subgraph decomposition (full + 5 wuxing panels)
- `03_adjacency_spectrum.png` — adjacency-matrix heatmap + graph spectrum
- `04_cycle_analysis.png` — octagon 8-cycles, central square 4-cycle, minimum cycle basis, per-face sums
- `05_centrality_invariants.png` — degree, betweenness, wuxing sums, octagon sums
- `06_wuxing_relations.png` — generation/overcoming pentagram + edge-classification pie
- `07_local_extensions.png` — 8-cycle family comparison + 4.8.8 tiling extension schematic
- `08_position_patterns.png` — concentric ring sums, shared/unique 50/50, opposite-pair 25-symmetry
