# In-Depth Analysis Report: Jisu-yong-yukdo (Earth-Number Six-Use Diagram / Six-Each-Gets)

## 1. Overview and Historical/Conceptual Background

**Jisu-yong-yukdo (地數用六圖)** is a traditional arithmetic diagram puzzle handed down in the *Gusuryeok* (九數略) family of late-Joseon mathematical texts. “Jisu (地數)” refers to the numbers of Earth, contrasted with the numbers of Heaven (天數, odd numbers 1, 3, 5, 7, 9); it symbolizes even numbers and the principle of yin. “Yong-yuk (用六)” means that the number 6 is used as the core unit. “Yukjagakdeuk (六子各得)” means that each hexagon, holding six numbers, “obtains” the same sum 63.

The core rules of this diagram are as follows.

- Use the natural numbers 1 through 20 exactly once.
- Place them in 5 hexagons, 6 numbers per hexagon.
- Adjacent hexagons share some vertices and edges.
- **The sum of the 6 numbers in every hexagon is 63**.

This is not a simple number game but a combinatorial structure combining a **total-sum invariant** with a **shared-vertex duplication coefficient**. In modern mathematics it can be viewed as a **planar graph** with 20 vertices and 24 edges, or as a fragment of a honeycomb lattice.

### Basic Quantitative Indicators

| Item | Value | Meaning |
|---|---|---|
| Vertices | 20 | 1–20, each used once |
| Hexagons | 5 | upper-left, upper-right, center, lower-left, lower-right |
| Edges | 24 | Hexagon sides reduced to graph edges |
| Connected components | 1 | The whole graph is connected |
| Hexagon sum | 63 | Core invariant |
| Total sum | 210 | 1 + 2 + … + 20 |
| Duplicated total | 315 | 63 × 5 (shared vertices counted multiple times) |

---

## 2. Hexagon Data and the Mathematics of Sum 63

### 2.1 Number Placement in Each Hexagon

| Hexagon | Six vertices | Sum |
|---|---|---|
| Upper-left | 5 + 18 + 16 + 3 + 8 + 13 | 63 |
| Upper-right | 1 + 13 + 8 + 14 + 20 + 7 | 63 |
| Center | 3 + 8 + 14 + 15 + 11 + 12 | 63 |
| Lower-left | 12 + 11 + 10 + 2 + 19 + 9 | 63 |
| Lower-right | 15 + 4 + 17 + 6 + 10 + 11 | 63 |

### 2.2 How Was the Sum 63 Determined?

The sum of 1 through 20 is 210. The “duplication-included” total of the 5 hexagons is 63 × 5 = 315, so the extra amount added by shared vertices is **315 − 210 = 105**.

The sum 63 is also statistically natural. The average of the 20 numbers is 10.5, and because each hexagon has 6 vertices, the “average” hexagon sum is **10.5 × 6 = 63**. Thus 63 is the natural center of this data and a **balance condition** designed so that every hexagon has the same weight.

Moreover, 63 can be decomposed as **60 + 3**, so it can also be read as one cycle (60, the gapja cycle) plus 3. We cannot assert that this was the original author’s intention, but in traditional numerology 60 and 6 are connected with time/space cycles, the six yao (六爻), and the six spirits (六神), leaving room for interesting interpretations.

### 2.3 Duplication Coefficient of Shared Vertices

Let the **multiplicity** of each vertex be the number of hexagons it belongs to. Then

```
Σ(each hexagon sum) = Σ(vertex value × its multiplicity)
                    = Σ(vertex value) + Σ(shared vertex value × (multiplicity − 1))
315 = 210 + 105
```

Therefore, the weighted sum of the “additional counts” of shared vertices is 105. The shared vertices are {3, 8, 10, 11, 12, 13, 14, 15}, and their duplication-weighted sum is 105.

---

## 3. Wuxing (Five Phases) Analysis

### 3.1 mod 5 Classification

Wuxing (五行) consists of the five categories Water, Fire, Wood, Metal, and Earth. Classifying the numbers 1–20 by their remainder modulo 5 (with 0 treated as 5, i.e. Earth) gives exactly 4 numbers in each phase.

| Wuxing | Residue | Numbers | Sum |
|---|---|---|---|
| Water (水) | 1 | 1, 6, 11, 16 | 34 |
| Fire (火) | 2 | 2, 7, 12, 17 | 38 |
| Wood (木) | 3 | 3, 8, 13, 18 | 42 |
| Metal (金) | 4 | 4, 9, 14, 19 | 46 |
| Earth (土) | 0→5 | 5, 10, 15, 20 | 50 |

### 3.2 Meaning of the Arithmetic Progression

The wuxing sums 34, 38, 42, 46, 50 form an **arithmetic progression with common difference 4**. This is not accidental. The numbers 1–20 are evenly divided into 5 residue classes with 4 numbers each, and adjacent residue classes differ by 5. The common difference 4 exactly matches the **width obtained by dividing the total range 20 into 5 classes (20/5 = 4)**.

In general, classifying 1 through 5k by mod 5 gives the following residue-class sums.

```
S(r) = Σ_{i=0}^{k-1} (5i + r) = 5·k(k−1)/2 + k·r
```

Here k = 4, so S(r) = 30 + 4r (r = 1, 2, 3, 4, 5). Therefore the values 34, 38, 42, 46, 50 necessarily arise from the specific range 1–20.

### 3.3 Wuxing Distribution Within Each Hexagon

We can examine which wuxing combinations occur in each hexagon. If wuxing “energy” flows between hexagons through shared vertices, the balance of the distribution reveals the harmony of the structure.

| Hexagon | Water | Fire | Wood | Metal | Earth | Total |
|---|---|---|---|---|---|---|
| Upper-left | 1 | 0 | 3 | 0 | 2 | 6 |
| Upper-right | 2 | 1 | 1 | 1 | 1 | 6 |
| Center | 0 | 1 | 1 | 1 | 3 | 6 |
| Lower-left | 0 | 2 | 0 | 2 | 2 | 6 |
| Lower-right | 1 | 1 | 0 | 1 | 3 | 6 |

Every hexagon has 6 vertices across 5 phases, so at least one phase must repeat. Upper-left is strong in Wood (3) and Earth (2), while Center and Lower-right are prominent in Earth (3). This allows the interpretation that Center and Lower-right carry much of the Earth (centrality, stability) quality.

---

## 4. Graph-Theoretic Indicators

### 4.1 Basic Graph Information

Treating each hexagon side as a graph **edge** and each number as a **vertex**, Jisu-yong-yukdo becomes the following planar graph.

- Vertices: 20
- Edges: 24
- Connected components: 1
- Minimum degree: 2
- Maximum degree: 3
- Degree sequence (descending): [3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

There are 8 vertices of degree 3 and 12 vertices of degree 2. This corresponds exactly to the distribution of shared and unique vertices: **shared vertices belong to 2 or more hexagons, so they have degree 3, while unique vertices belong to only one hexagon, so they have degree 2**.

### 4.2 Properties as a Planar Graph

Applying Euler’s formula V − E + F = 2 (including the outer face):

```
20 − 24 + F = 2  ⇒  F = 6
```

This means 5 hexagonal faces plus 1 outer face, for a total of 6 faces. Thus Jisu-yong-yukdo is a **planar graph composed of five 6-cycles and one outer cycle**.

### 4.3 Centrality

#### Top 5 Betweenness Centrality

Betweenness centrality measures how often a vertex appears on shortest paths between other vertices. Higher values indicate a gateway through which information or energy passes.

| Rank | Vertex | Wuxing | Betweenness |
|---|---|---|---|
| 1 | 15 | Earth | 0.290 |
| 1 | 12 | Fire | 0.290 |
| 1 | 3 | Wood | 0.290 |
| 1 | 14 | Metal | 0.290 |
| 5 | 8 | Wood | 0.279 |

Four vertices (15, 12, 3, 14) share the same highest centrality, and they are all **shared vertices connecting the center hexagon with adjacent hexagons**. In particular, 3 and 14 connect Upper-left, Upper-right, and Center, while 12 and 15 connect Center, Lower-left, and Lower-right. The vertex 8 (Wood) also spans Upper-left, Upper-right, and Center, giving it high centrality.

This shows that Jisu-yong-yukdo is not simply five hexagons in a row but forms a **radial/mesh structure centered on the center hexagon**.

#### Degree Centrality

Because degrees are only 2 or 3, degree centrality directly reflects whether a vertex is shared. A degree-3 vertex is a structural hub.

| Degree | Vertices | Role |
|---|---|---|
| 3 | 3, 8, 10, 11, 12, 13, 14, 15 | Shared vertices, structural hubs |
| 2 | 1, 2, 4, 5, 6, 7, 9, 16, 17, 18, 19, 20 | Unique vertices, outer vertices |

### 4.4 Spectrum

Computing the eigenvalues of the adjacency matrix gives the following.

| Indicator | Value |
|---|---|
| λ_max | 2.5884 |
| λ_min | −2.5884 |
| Eigenvalue range | 5.1767 |

λ_max can be interpreted as the **propagation/connectivity strength** of the graph. Jisu-yong-yukdo is a relatively sparse and planar graph, so its λ_max is modest. The roughly symmetric distribution of eigenvalues around 0 hints at a relatively balanced structure even though the graph is not bipartite.

---

## 5. Cycle Structure

### 5.1 Each Hexagon Forms a 6-Cycle

Each hexagon forms a cycle of length 6.

| Hexagon | 6-Cycle |
|---|---|
| Upper-left | 5 → 18 → 16 → 3 → 8 → 13 → 5 |
| Upper-right | 1 → 13 → 8 → 14 → 20 → 7 → 1 |
| Center | 3 → 8 → 14 → 15 → 11 → 12 → 3 |
| Lower-left | 12 → 11 → 10 → 2 → 19 → 9 → 12 |
| Lower-right | 15 → 4 → 17 → 6 → 10 → 11 → 15 |

### 5.2 Cycle Basis

The five hexagon cycles are independent and form the **cycle basis** of this graph. The size of the cycle basis can be checked by the formula

```
|Cycle basis| = E − V + 1 = 24 − 20 + 1 = 5
```

Thus the five 6-cycles generate all cycles of the graph. For example, the union cycle of two adjacent hexagons (e.g. Upper-left ∪ Center) can be expressed as the symmetric difference of basis cycles.

### 5.3 Role of the Center Hexagon

The center hexagon shares vertices with all four surrounding hexagons. That is, all six vertices of the center hexagon {3, 8, 14, 15, 11, 12} are shared vertices. This means the center hexagon acts as the **core** of the whole structure. Removing the center disconnects the graph into four pieces (Upper-left, Upper-right, Lower-left, Lower-right).

---

## 6. Position Pattern: Shared Vertices vs. Unique Vertices

### 6.1 Shared and Unique Vertices

| Classification | Vertices |
|---|---|
| Shared vertices (2 or more hexagons) | {3, 8, 10, 11, 12, 13, 14, 15} |
| Unique vertices (1 hexagon) | {1, 2, 4, 5, 6, 7, 9, 16, 17, 18, 19, 20} |

Shared vertices act as **junctions** between hexagons and decisively influence the graph’s connectivity and centrality. Because there are 8 shared vertices, they are duplicated across 2 or 3 hexagons.

### 6.2 Wuxing Distribution of Shared Vertices

The 8 shared vertices by wuxing are as follows.

| Wuxing | Shared vertices |
|---|---|
| Water | 13 |
| Fire | 12 |
| Wood | 3, 8 |
| Metal | 14 |
| Earth | 10, 11, 15 |

Earth (10, 11, 15) is the most common with 3 vertices, Wood (3, 8) has 2, and the rest have 1 each. The abundance of Earth in the central connections agrees with the traditional wuxing notion that Earth has the character of **mediation, stability, and connection**.

### 6.3 Wuxing Distribution of Unique Vertices

The 12 unique vertices are as follows.

| Wuxing | Unique vertices |
|---|---|
| Water | 1, 6, 16 |
| Fire | 2, 7, 17 |
| Wood | 18 |
| Metal | 4, 9, 19 |
| Earth | 5, 20 |

Unique vertices are located mostly on the outer parts of each hexagon and play a role close to the “leaves” of the graph.

---

## 7. Wuxing Edge Distribution

Classifying the graph’s 24 edges by the wuxing relationship of their two endpoints gives the following.

| Classification | Count | Ratio |
|---|---|---|
| Overcoming | 12 | 50% |
| Generation | 9 | 37.5% |
| Same-phase | 3 | 12.5% |

- **Generation (相生)**: Connections in the directions Water→Wood, Wood→Fire, Fire→Earth, Earth→Metal, Metal→Water.
- **Overcoming (相剋)**: Connections in the directions Water→Fire, Fire→Metal, Metal→Wood, Wood→Earth, Earth→Water.
- **Same-phase**: Connections between vertices of the same wuxing.

The fact that overcoming relationships outnumber generative ones is interesting. It can be read as evidence that Jisu-yong-yukdo contains **tension and change as well as harmony**. With only 3 same-phase edges, most adjacency relations are interactions between different wuxing.

---

## 8. Generalization and Extension

### 8.1 General Formula for mod 5 Residue-Class Sums

Classifying 1 through 5k by mod 5, the class sums generalize as follows.

```
S(r) = 5·k(k−1)/2 + k·r   (r = 1, 2, 3, 4, 5)
```

For k = 4:

| M0 | Wuxing | Class sum | Formula |
|---|---|---|---|
| 1 | Water | 34 | 30 + 4×1 |
| 2 | Fire | 38 | 30 + 4×2 |
| 3 | Wood | 42 | 30 + 4×3 |
| 4 | Metal | 46 | 30 + 4×4 |
| 5 | Earth | 50 | 30 + 4×5 |

### 8.2 Extension of the Hexagonal Lattice

Jisu-yong-yukdo can be viewed as a **core** of 20 vertices. Extending this structure concentrically yields larger hexagonal lattices with 20k vertices. To keep every hexagon sum constant, the numbers added in each new layer must follow the core’s wuxing distribution and sum rules.

Jisu-yong-yukdo also forms a pair with **Cheonsu-yong-odo (天數用五圖)**, the “Heaven-Number Five-Use Diagram” dealing with the odd numbers 1, 3, 5, 7, 9 in pentagonal/circular structures. A natural extension is also the relationship with even-number structures based on the Earth numbers 2, 4, 6, 8, 10.

---

## 9. Visualization Outputs

The image files in the same directory show Jisu-yong-yukdo from various viewpoints.

| File | Content |
|---|---|
| `01_original_graph.png` | Original honeycomb intersection structure |
| `02_wuxing_decomposition.png` | Wuxing subgroup decomposition |
| `03_adjacency_spectrum.png` | Adjacency matrix and graph spectrum |
| `04_cycle_analysis.png` | Cycle structure and hexagon sums |
| `05_centrality_invariants.png` | Centrality and sum invariants |
| `06_wuxing_relations.png` | Wuxing generation/overcoming relation diagram |
| `07_local_extensions.png` | Generalization and concentric extension |
| `08_position_patterns.png` | Shared vertices vs. unique vertex patterns |
| `jisu_yong_yukdo.png` / `.svg` | Overall summary visualization |

---

## 10. Conclusion

Jisu-yong-yukdo may look like a simple puzzle of placing 1–20 into five hexagons, but it contains the following rich mathematical structures.

1. **Sum invariant**: every hexagon has the same sum 63, the natural result of the average 10.5 × 6.
2. **Shared-vertex structure**: 8 shared vertices create the duplication coefficient, complete the total 315, and determine the graph’s connectivity.
3. **Wuxing arithmetic progression**: mod 5 classification gives phase sums 34, 38, 42, 46, 50, an arithmetic progression with difference 4.
4. **Planar graph**: 20 vertices, 24 edges, and 6 faces satisfying Euler’s formula.
5. **Central core**: the center hexagon is the key hub connecting the four outer hexagons.
6. **Cycle basis**: five 6-cycles form the cycle basis of the graph.

These structures show a meeting point between traditional numerology and modern combinatorics/graph theory, and encourage us to re-evaluate Jisu-yong-yukdo not as a mere mental-calculation puzzle but as a **diagram for exploring the harmony of numbers and spatial structure**.
