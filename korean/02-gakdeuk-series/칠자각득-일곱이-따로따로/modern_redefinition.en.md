# Modern Combinatorial Redefinition of the Chiljagakdeuk (七子各得) Puzzle

> This document avoids traditional terminology and redefines the diagram using only observed data and modern combinatorial / discrete-mathematical language.

---

## 1. Observed Objects

The diagram consists of the following elements.

- **5 clusters**: sets of 7 elements placed inside circular boundaries
- **Center**: 1 element at the middle of each cluster
- **Peripheral slots**: 6 elements surrounding the center
- **Connecting lines**: line segments joining the center to each peripheral slot
- **Numeral labels**: natural numbers assigned to each element
- **Spatial layout**: 5 clusters arranged in a cross shape
- **Sum condition**: the 7 elements in each cluster sum to 120

In this definition, the circular boundary is only a visual frame; mathematically it is a set-theoretic separator distinguishing clusters. The connection set `E` is an explicitly given edge set, which means—unlike the previous Saodo puzzle—**graph structure is part of the data**.

The observed five clusters are:

| Cluster | Center | Peripheral slots | Sum |
|---|---|---|---|
| C₁ (top) | 2 | 29, 1, 24, 34, 11, 19 | 120 |
| C₂ (left) | 3 | 6, 33, 23, 13, 34, 8 | 120 |
| C₃ (center) | 5 | 22, 7, 20, 30, 26, 10 | 120 |
| C₄ (right) | 4 | 15, 28, 9, 18, 32, 14 | 120 |
| C₅ (bottom) | 1 | 35, 16, 21, 24, 6, 17 | 120 |

- Total element count (with multiplicity): 35
- Distinct values: 31
- Repeated values: 1, 6, 24, 34 (each appears twice)
- Total sum (with multiplicity): 600 = 5 × 120

---

## 2. Formal Definition

The structure directly extractable from the original text is:

```
P = (C, K, S, X, E, I)
```

| Symbol | Meaning | Modern term |
|---|---|---|
| `C` | set of 5 clusters | cluster set |
| `K` | center label function `K: C → ℕ` | center labeling |
| `S` | peripheral slot label function `S: C → ℕ⁶` | peripheral slot labeling |
| `X` | 2D geometric placement of clusters | geometric embedding |
| `E` | set of center-periphery connecting lines | radial edge set |
| `I` | cluster sum invariant `Σ(c) = 120` | local sum invariant |

---

## 3. mod-5 Structure

The centers form exactly one copy of each residue class modulo 5:

```
K = {1, 2, 3, 4, 5}
```

This is a complete residue system of `ℤ/5ℤ`.

The residue distribution of peripheral slots is:

| Cluster | Center residue | Peripheral residue counts |
|---|---|---|
| C₁ | 2 | 1×2, 4×4 |
| C₂ | 3 | 1×1, 3×4, 4×1 |
| C₃ | 5 | 1×1, 2×2, 5×3 |
| C₄ | 4 | 2×1, 3×2, 4×2, 5×1 |
| C₅ | 1 | 1×3, 2×1, 4×1, 5×1 |

For every cluster, the sum of residues is divisible by 5, consistent with each cluster sum 120 ≡ 0 (mod 5).

---

## 4. Geometric Layout

The five clusters are placed at the following coordinates.

```
        C₁(0, 3.3)
            |
C₂(-3.3, 0) — C₃(0,0) — C₄(3.3, 0)
            |
        C₅(0, -3.3)
```

Inside each cluster, the six peripheral slots are arranged approximately on a regular hexagon around the center. Thus the whole structure can be viewed as **five 7-point star configurations arranged in a cross**.

---

## 5. Modern Reinterpretation of the “Saodo Rule”

The original note states that the diagram “follows the rule of Saodo.” In modern language, this means:

1. **Five direction-center correspondences**: the 5 clusters lie in 5 directions (top, bottom, left, right, center), and each direction’s center is one of `{1,2,3,4,5}`.
2. **Center-periphery split**: each cluster is split into 1 center and 6 peripheral elements, a “center + 6 directions” structure.
3. **Directional sum invariant**: each direction (cluster) has the same total sum, 120.
4. **mod-5 residue completeness**: the centers form a complete residue system modulo 5.

Generalized, the diagram can be viewed as a **weight function on a direction set `D`**.

```
D = {top, left, center, right, bottom}
K: D → ℤ/5ℤ   (bijection)
S: D → (ℕ⁶)
Σ_{d∈D} (K(d) + ΣS(d)) = 600
∀d∈D: K(d) + ΣS(d) = 120
```

---

## 6. Modern Combinatorial Problems

### Problem 1. Sum-invariant equation

Count the number of ways to choose six peripheral numbers for each cluster so that the cluster sum is 120. State the allowed range and repetition conditions explicitly.

### Problem 2. mod-5 coloring

Investigate how the center and peripheral slots of each cluster distribute residues modulo 5. Explain why the residue sum of each cluster is 0 (mod 5).

### Problem 3. Duplication structure

The values 1, 6, 24, and 34 each appear in two clusters. Analyze whether this duplication is accidental or hints at an inter-cluster relation.

### Problem 4. Direction graph

Define a graph whose vertices are the 5 clusters, with edges based on shared numbers or spatial adjacency. Investigate its connectivity and symmetry.

---

## 7. Strengths and Weaknesses

### Strengths

1. A clear sum invariant (120) exists.
2. The centers form a complete mod-5 residue system.
3. The geometric layout (cross + hexagon) is regular.
4. Center-periphery edges are explicit, so the graph structure is clear.

### Weaknesses

1. The rule for choosing peripheral numbers is not stated.
2. The meaning of duplicated values (1, 6, 24, 34) is unclear.
3. The origin of the sum 120 is unexplained.
4. Inter-cluster relations (edges, operations, etc.) are not defined.
