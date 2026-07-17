# Shared Properties and Generalization of Puzzles Following the Gakdeuk (各得) Principle

## 1. Overview

The **Gakdeuk (各得)** puzzles recorded in the repository's *Gusuryak
(九數略)* source material are combinatorial diagrams in which several subsets
are arranged so that each one "obtains" the same sum. The repository groups
the documented families Gujagakdeuk (九子各得), Ojagakdeuk (五子各得 /
Cheonsuyongodo), Yukjagakdeuk (六子各得 / Jisuyongyukdo), Chiljagakdeuk
(七子各得), and Paljagakdeuk (八子各得) by their subset sizes; this grouping is
a computational organization, not a claim about an unbroken transmission line.

This report extracts the structural properties shared by these Gakdeuk families and generalizes them in the language of modern combinatorics and graph theory.

---

## 2. Summary of Gakdeuk Family Data

| Family | Hanja | Subset size `n` | Number of subsets `k` | Number range | Total sum `T` | Subset sum `S` | Duplication-inclusive sum `k·S` | Duplication sum `k·S − T` | Notes |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| Ojagakdeuk | 五子各得 | 5 | 5 | 21 of 1–24 | 265 | 65 | 325 | 60 | Cheonsuyongodo, subset sum = 65 |
| Yukjagakdeuk | 六子各得 | 6 | 5 | 1–20 | 210 | 63 | 315 | 105 | Jisuyongyukdo, intersecting honeycomb hexagons |
| Chiljagakdeuk | 七子各得 | 7 | 5 | 1–35 (31 unique) | 535 | 120 | 600 | 65 | Center 1 + periphery 6, 4 duplicates |
| Paljagakdeuk | 八子各得 | 8 | 5 | 1–40 | 820 | 164 | 820 | 0 | 3×3 grid minus center, 8 characters |
| Gujagakdeuk | 九子各得 | 9 | 5 | 1–45 | 1035 | 207 | 1035 | 0 | Full 3×3 grid, 9 characters |

\* Chiljagakdeuk has duplicated values (1, 6, 24, 34), so the unique-vertex sum is 535, while the duplication-inclusive total is 600 = 5×120. Hence the duplication amount is D = 600 − 535 = 65.

---

## 3. Shared Structural Properties

### 3.1 Five Subsets and a Central Core

Every Gakdeuk family consists of **five subsets**. Spatially, they follow a cruciform layout:

```
        Up
         │
    Left ─ Center ─ Right
         │
       Down
```

- **Center** acts as the core of the whole structure.
- **Up, Down, Left, Right** are placed in the four directions around the center.
- Five is the number of the Wuxing (Five Elements/Phases) and the basic unit expressing a center plus four directions in astronomy and geography.

Specifically:

- **Gujagakdeuk · Paljagakdeuk**: the central palace connects the four directional palaces through the grid.
- **Yukjagakdeuk**: the central hexagon shares vertices and edges with the four outer hexagons.
- **Chiljagakdeuk**: the central cluster (C₃) is arranged together with the four directional clusters.
- **Ojagakdeuk**: in the Cheonsuyongodo, the central vertical axis (19–6–20–5–17–2) forms the structural axis.

### 3.2 Sum Invariant

The most salient property of the Gakdeuk family is that **all subsets have the same sum**. This common sum is called the **sum invariant** `S`.

| Family | Subset sum `S` | Average `S/n` |
|:---:|:---:|:---:|
| Yukjagakdeuk | 63 | 10.5 |
| Chiljagakdeuk | 120 | ≈17.14 |
| Paljagakdeuk | 164 | 20.5 |
| Gujagakdeuk | 207 | 23.0 |

The average `S/n` coincides with the average of the used number range (or the duplication-inclusive average).

- Paljagakdeuk: average of 1–40 = 20.5 = 164/8
- Gujagakdeuk: average of 1–45 = 23.0 = 207/9
- Yukjagakdeuk: duplication-inclusive average = 315/30 = 10.5 = 63/6
- Chiljagakdeuk: duplication-inclusive average = 600/35 ≈ 17.14 = 120/7

Therefore, the sum invariant `S` is generalized as:

```
S = n × μ
```

where `μ` is the average of the numbers used in the subset (duplication-inclusive).

### 3.3 Duplication Coefficients and Connectivity

When subsets share vertices, the following relation holds between the total sum `T` and the duplication-inclusive sum `k·S`:

```
k·S = T + D
```

- `D`: total amount by which shared vertices are counted multiple times

| Family | `k·S` | `T` | `D` | Sharing structure |
|:---:|:---:|:---:|:---:|:---|
| Yukjagakdeuk | 315 | 210 | 105 | 8 shared vertices, degree 3 |
| Paljagakdeuk | 820 | 820 | 0 | 12 inter-palace edges, no vertex sharing |
| Gujagakdeuk | 1035 | 1035 | 0 | 12 inter-palace edges, no vertex sharing |
| Chiljagakdeuk | 600 | 535 (unique) | 65 | 4 duplicated values (1, 6, 24, 34) |

Yukjagakdeuk achieves direct connections between subsets through shared vertices; Paljagakdeuk and Gujagakdeuk connect palaces by edges without sharing vertices. Chiljagakdeuk has a weaker connection through duplicated numerical values between subsets.

### 3.4 Wuxing (Five Elements) mod 5 Arithmetic Progression

In every Gakdeuk family, if numbers are classified into the five Wuxing groups (Water, Fire, Wood, Metal, Earth) according to their remainder modulo 5 (with 0 treated as 5), the **sum per Wuxing group forms an arithmetic progression**.

In general, dividing the numbers 1 through `5m` into five residue classes gives the following class sums:

```
WX(r) = 5·m(m−1)/2 + m·r    (r = 1, 2, 3, 4, 5)
```

| Family | `m` (Wuxing-group size) | Wuxing sum sequence | Common difference |
|:---:|:---:|:---|:---:|
| Yukjagakdeuk | 4 | 34, 38, 42, 46, 50 | 4 |
| Ojagakdeuk (full 5×5) | 5 | 55, 60, 65, 70, 75 | 5 |
| Chiljagakdeuk (full 5×7) | 7 | 112, 119, 126, 133, 140 | 7 |
| Paljagakdeuk | 8 | 148, 156, 164, 172, 180 | 8 |
| Gujagakdeuk | 9 | 189, 198, 207, 216, 225 | 9 |

The common difference equals the Wuxing-group size `m`, because each group contains `m` consecutive numbers spaced by 5.

Moreover, each subset sum `S` often coincides with the middle term (Wood group sum) of this arithmetic progression.

- Yukjagakdeuk: S = 63 = Wood (42)? No. But 63 = (34+50)/2 + 14; complicated.
- Paljagakdeuk: S = 164 = Wood group sum 164 (exact match)
- Gujagakdeuk: S = 207 = Wood group sum 207 (exact match)
- Chiljagakdeuk: S = 120, while the full 5×7 Wood group sum is 126. 120 = 126 − 6.

The fact that `S` matches the Wood group sum in Paljagakdeuk and Gujagakdeuk allows the interpretation that they are representatives of the generalization family corresponding to "M0 = 3" (Wood).

### 3.5 Common Graph-Theoretic Patterns

Viewing each family as a graph reveals the following shared patterns:

| Property | Shared? | Description |
|:---|:---:|:---|
| Planar graph | ○ | Most can be drawn on paper without crossings |
| Central core | ○ | The central subset connects the four directions |
| Degree hierarchy | ○ | Central/boundary vertices have high degree; outer vertices have low degree |
| Cycle basis | △ | Paljagakdeuk (8-cycle), Yukjagakdeuk (6-cycle), Gujagakdeuk (3×3 grid 4-cycle) |
| Betweenness centrality | ○ | Vertices in the central subset attain the maximum |

### 3.6 Wuxing Edge Distribution

If intra-subset or inter-subset connections are classified by Wuxing relationships, **controlling (相剋) relationships tend to be the most frequent or at least substantial**.

| Family | Controlling | Generating | Same-type | Neutral |
|:---:|:---:|:---:|:---:|:---:|
| Yukjagakdeuk | 12 (50.0%) | 9 (37.5%) | 3 (12.5%) | 0 |
| Paljagakdeuk | 29 (55.8%) | 6 (11.5%) | 17 (32.7%) | 0 |
| Gujagakdeuk | 29 (40.3%) | 18 (25.0%) | 20 (27.8%) | 0 |

(Ojagakdeuk and Chiljagakdeuk are omitted because they lack explicit edge definitions.)

This distribution shows that Gakdeuk puzzles visualize not merely harmony but **tension and constraint among the Wuxing**.

---

## 4. Variations and Special Features

### 4.1 Ojagakdeuk (Cheonsuyongodo): A Geometry-Centered Puzzle

Ojagakdeuk (Cheonsuyongodo) also has the subset sum invariant **65**, placing five numbers in each of five subsets. Since 5×65 = 325 and the sum of the 21 used numbers is 265, the duplication sum of the shared vertices is 60.

This shows that the Gakdeuk principle is not realized only through "equal subset sums" but can also appear as a **spatially symmetric, axis-centered sum invariant**.

### 4.2 Chiljagakdeuk: Center-Periphery Split and Duplicated Values

Chiljagakdeuk splits each cluster into **1 center + 6 periphery** numbers. A distinctive feature is that the centers are `{1, 2, 3, 4, 5}`, forming a complete residue system modulo 5. In addition, four values (1, 6, 24, 34) appear in two clusters each, creating a duplication structure different from the other families.

### 4.3 Gujagakdeuk · Paljagakdeuk: The 3×3 Grid Family

Both Gujagakdeuk (9 characters) and Paljagakdeuk (8 characters) are based on a 3×3 grid.

- Gujagakdeuk: all nine cells of the 3×3 grid are used.
- Paljagakdeuk: the eight peripheral cells of the 3×3 grid are used, excluding the center.

Both exhibit strong positional invariants in the analysis of edge-midpoint sums and corner sums.

- Paljagakdeuk: edge-midpoint sums = 38, 40, 42, 44, 46 (common difference 2)
- Gujagakdeuk: edge-midpoint sums = 90, 91, 92, 93, 94 (common difference 1), corner sum = 92 (same for every palace)

---

## 5. Generalization Model

### 5.1 Symbol Definitions

We abstract a Gakdeuk puzzle as follows:

```
P = (C, V, E, φ, S, w)
```

- `C`: set of five subsets (palaces / clusters / hexagons)
- `V`: set of all numbers used (vertices)
- `E ⊂ V × V`: adjacency / connection relation (edges)
- `φ: V → {1,2,3,4,5}`: mod 5 Wuxing labeling
- `S`: subset sum invariant
- `w: V → ℕ`: duplication coefficient of each vertex (number of subsets it belongs to)

### 5.2 Sum Invariant Equation

For every subset `c ∈ C`:

```
Σ_{v ∈ c} v = S
```

Taking duplication coefficients into account, the following relation holds between the total sum `T = Σ_{v ∈ V} v` and `S`:

```
5·S = Σ_{v ∈ V} w(v)·v = T + Σ_{v: w(v)>1} (w(v)−1)·v
```

### 5.3 Wuxing Invariant

Defining `φ(v) = v mod 5` (with 0 mapped to 5), the sum of each Wuxing group among the numbers 1 through `5m` is:

```
WX(r) = m·(5m−1)/2 + r·m    (r = 1, ..., 5)
```

Or, in arithmetic-progression form:

```
WX(r) = WX(1) + (r−1)·m
```

### 5.4 General Average Formula

Using the duplication-inclusive average `μ`, each subset sum is generalized as:

```
S = n · μ
```

- If no vertices are shared between subsets: `μ = (V_max + 1)/2`
- If vertices are shared between subsets: `μ = (Σ_{v∈V} w(v)·v) / (5n)`

### 5.5 Spatial Generalization of Five Subsets

Every Gakdeuk family follows the common spatial template:

```
        C_Up
          │
    C_Left ─ C_Center ─ C_Right
          │
        C_Down
```

This template naturally connects the five directions (Up, Down, Left, Right, Center) with the Wuxing (Water, Fire, Wood, Metal, Earth) correspondence and the traditional cosmological "four directions + center" model.

---

## 6. Generalization Families of Each Puzzle

### 6.1 Wuxing-Centered Generalization

One can define a family parameterized by a starting value `M0 ∈ {1,2,3,4,5}`, where each subset sum `S` changes accordingly. This has already been observed for Paljagakdeuk and Gujagakdeuk.

| Family | Common difference | M0=1 (Water) | M0=2 (Fire) | M0=3 (Wood) | M0=4 (Metal) | M0=5 (Earth) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Yukjagakdeuk | 4 | — | — | 63? | — | — |
| Paljagakdeuk | 8 | 148 | 156 | 164 | 172 | 180 |
| Gujagakdeuk | 9 | 189 | 198 | 207 | 216 | 225 |

Currently, Yukjagakdeuk's sum 63 does not correspond directly to this simple Wuxing-centered generalization, indicating that Yukjagakdeuk has its own sum condition due to its shared-vertex structure.

### 6.2 Generalization by n-gon / Grid Size

Generalization according to subset size `n`:

| `n` | Family | Number range | Subset sum `S` | Average `S/n` |
|:---:|:---|:---:|:---:|:---:|
| 5 | Ojagakdeuk | 1–24 (21 numbers) | — | — |
| 6 | Yukjagakdeuk | 1–20 | 63 | 10.5 |
| 7 | Chiljagakdeuk | 1–35 | 120 | ≈17.14 |
| 8 | Paljagakdeuk | 1–40 | 164 | 20.5 |
| 9 | Gujagakdeuk | 1–45 | 207 | 23.0 |

As `n` increases by 1, the number range and subset sum naturally grow.

---

## 7. Extension Possibilities

### 7.1 Gakdeuk Puzzles with 10 or More Characters

Following the above pattern, one can design a **Shipjagakdeuk** (ten-character Gakdeuk) for `n = 10`. With five subsets of ten numbers each and no duplication, a total of 50 numbers (1–50) can be used. The natural candidate for each subset sum is **255**, obtained by multiplying the average of 1–50, namely 25.5, by 10.

### 7.2 Other Duplication-Coefficient Designs

Yukjagakdeuk creates duplication coefficients through shared vertices. Extending this idea, one can design new puzzles with various duplication-coefficient structures between subsets.

### 7.3 Three-Dimensional Extension

The current Gakdeuk families are arranged on a two-dimensional plane, but one could extend to a three-dimensional placement by adding **four directions + center + up/down (Heaven/Earth)** (for example, selecting 5 of the 12 faces of a regular dodecahedron).

---

## 8. Conclusion

The Gakdeuk family is not merely a numerical arrangement; it shares the following common mathematical structures:

1. **Five subsets + central core**: the Up-Down-Left-Right-Center five-direction template.
2. **Sum invariant**: every subset has the same sum.
3. **Duplication equation**: `5·S = T + D`.
4. **Wuxing mod 5 arithmetic progression**: `WX(r) = WX(1) + (r−1)·m`.
5. **Planar graph + centrality hierarchy**: central vertices have high connectivity and centrality.
6. **Controlling-dominant Wuxing edges**: visualizing constraint and tension.
7. **Positional invariants**: corner / edge-midpoint sums, left-right symmetric sums, etc.

Through these common principles, Gakdeuk puzzles can be seen as **diagrams exploring the harmony of numbers and space**, naturally connecting traditional numerology with modern combinatorics and graph theory.
