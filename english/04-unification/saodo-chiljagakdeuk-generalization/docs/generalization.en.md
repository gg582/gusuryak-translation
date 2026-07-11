# Generalization of Saodo and Chiljagakdeuk: Does Saodo Follow the Rule of Chiljagakdeuk?

> This document unifies the Hado (Saodo) puzzle and the Chiljagakdeuk puzzle within a single abstract framework, and formally verifies to what extent Saodo satisfies the structural rule of Chiljagakdeuk. Traditional terminology is excluded; only modern combinatorial and discrete-mathematical language is used.

---

## 1. Motivation

Both puzzles share the following properties.

- Five groups or clusters exist.
- Numbers are classified by their residue modulo 5.
- Some form of sum invariant exists.
- Geometric placement is part of the data.

However, their concrete structures differ. Chiljagakdeuk has explicit clusters, a center-periphery split, and connecting lines, while Saodo has 20 marks, five color classes, and inter-group relations. This document proposes a general definition that encompasses both, and step-by-step decides whether Saodo follows the rule of Chiljagakdeuk.

---

## 2. General Definition: 5-ary Direction-Weighted Puzzle

The following abstract structure captures both puzzles.

```
Π = (D, M, X, E, K, S, W, Φ)
```

| Symbol | Meaning |
|---|---|
| `D` | Direction set. Here identified with `{1,2,3,4,5}` or `{top,bottom,left,right,center}` |
| `M` | Set of marks or elements |
| `X` | Geometric placement function `X: M → ℝ²` |
| `E` | Connection relation (edge set), `E ⊆ M × M` |
| `K` | Direction-center correspondence `K: D → M` or `K: D → ℤ/5ℤ` |
| `S` | Per-direction peripheral set `S: D → 2^M` |
| `W` | Weight function `W: M → ℕ` (numeral label) |
| `Φ` | Set of invariant conditions |

This definition includes both puzzles as special cases.

---

## 3. Rule of Chiljagakdeuk: Strict Definition

The structural rule satisfied by Chiljagakdeuk is formalized as follows.

### Rule C1. Five direction-clusters

```
|D| = 5
```

### Rule C2. Center-periphery split

For each direction `d ∈ D`,

```
M_d = {K(d)} ∪ S(d)
|S(d)| = 6
|M_d| = 7
```

### Rule C3. Mod-5 residue completeness of centers

```
K: D → ℤ/5ℤ is a bijection
```

That is, the set of center labels is exactly `{1,2,3,4,5}`.

### Rule C4. Per-direction sum invariant

```
∃ T ∈ ℕ,  ∀d ∈ D:  W(K(d)) + Σ_{s∈S(d)} W(s) = T
```

For Chiljagakdeuk, `T = 120`.

### Rule C5. Explicit center-periphery edges

```
E ⊇ { (K(d), s) | d ∈ D, s ∈ S(d) }
```

That is, the edge set `E` contains the edges joining each center to its peripheral slots.

---

## 4. Mapping Saodo into the General Framework

Translating Saodo’s data into the general structure `Π` gives the following.

- `D = {1,2,3,4,5}`: the five color classes.
- `M`: the 20 circular marks.
- `X`: symmetric cross placement.
- `E = ∅`: no edges are explicitly given in the original text.
- `K`: how should a "center" be defined for each color class?
- `S`: the remaining three elements of each color class may be viewed as peripheral slots.
- `W`: the numeral label of each mark.
- `Φ`: total sum `Σ W = 210`, 5-coloring structure, etc.

The crucial question is:

> How do we select the center `K(d)` for each color class of Saodo?

A natural choice is to take the smallest element of each color class as the center.

| Color class | Center `K(d)` | Peripheral slots `S(d)` | Sum |
|---|---|---|---|
| Water (1) | 1 | {6, 11, 16} | 34 |
| Fire (2) | 2 | {7, 12, 17} | 38 |
| Wood (3) | 3 | {8, 13, 18} | 42 |
| Metal (4) | 4 | {9, 14, 19} | 46 |
| Earth (5) | 5 | {10, 15, 20} | 50 |

Under this mapping, the center set is `{1,2,3,4,5}`, so mod-5 residue completeness (C3) holds. However, each class has only 3 peripheral slots, not 6, and the per-direction sums are not equal.

Another possibility is to split each color class into two "layers" using the 2-cycle extension.

| Color class | Layer 1 | Layer 2 |
|---|---|---|
| Water | {1, 6} | {11, 16} |
| Fire | {2, 7} | {12, 17} |
| Wood | {3, 8} | {13, 18} |
| Metal | {4, 9} | {14, 19} |
| Earth | {5, 10} | {15, 20} |

The per-layer sums are then:

| Color class | Layer 1 sum | Layer 2 sum |
|---|---|---|
| Water | 7 | 27 |
| Fire | 9 | 29 |
| Wood | 11 | 31 |
| Metal | 13 | 33 |
| Earth | 15 | 35 |

Again, the sum invariant (C4) fails.

---

## 5. Hierarchical Definition of "Following"

The statement "Saodo follows the rule of Chiljagakdeuk" can be interpreted at several levels.

### Level 0. Following the 5-ary directional structure

```
|D| = 5 and each direction is assigned a mod-5 residue.
```

Saodo satisfies this level.

### Level 1. Following the center-periphery split

```
Each direction is split into one center and n peripheral slots.
```

Saodo admits such a split, but the number of peripheral slots is 3, not 6.

### Level 2. Following the peripheral-slot count

```
∀d ∈ D: |S(d)| = 6
```

Saodo does not satisfy this.

### Level 3. Following the per-direction sum invariant

```
∃ T, ∀d ∈ D: W(K(d)) + Σ_{s∈S(d)} W(s) = T
```

Saodo does not satisfy this. The color-class sums are 34, 38, 42, 46, 50.

### Level 4. Following explicit edges

```
Center-periphery edges are included in the original data.
```

Saodo does not satisfy this. The original text contains no explicit edges.

---

## 6. Conclusion: Does Saodo Follow the Rule of Chiljagakdeuk?

**In the strict sense, no.**

Saodo fails the core Chiljagakdeuk rules C2, C4, and C5. In particular, it differs in the number of peripheral slots, the per-direction sum invariant, and the presence of explicit edges.

**However, in a weak sense, it shares the common skeleton.**

Saodo shares with Chiljagakdeuk the five-direction structure, mod-5 residue classification, complete residue system of centers, and a global sum invariant. Thus Saodo may be viewed as a **weakened variant** or **different parameter setting** of the same family.

Formally:

> Saodo follows the "5-ary direction-center skeleton" of Chiljagakdeuk, but not its "6-peripheral-slot, equal-sum, edge-explicit structure".

---

## 7. Unified Generalization: A Parameterized Puzzle Family

Both puzzles can be placed in a single parameterized family.

```
Π(p, q, T)
```

- `p`: number of directions (here 5).
- `q`: number of peripheral slots per direction.
- `T`: target sum for each direction (cluster).

Chiljagakdeuk is `Π(5, 6, 120)`.

Viewed by color class, Saodo is `Π(5, 3, T_d)` where `T_d` varies by direction. Thus Saodo is another example of the same family with a **non-uniform parameter setting**.

| Puzzle | p | q | T |
|---|---|---|---|
| Chiljagakdeuk | 5 | 6 | 120 (same for all directions) |
| Saodo (color classes) | 5 | 3 | 34, 38, 42, 46, 50 (direction-dependent) |

---

## 8. Modern Combinatorial Problems

### Problem 1. Existence conditions for the parameter family

For given `p, q, T`, find necessary and sufficient conditions for a puzzle of the form `Π(p, q, T)` to exist. Specifically for `p = 5`, investigate what constraints `q` and `T` satisfy over the natural numbers.

### Problem 2. Uniformization of Saodo

Can Saodo’s 20 marks be rearranged into 5 clusters of 7 elements each with equal sum, while preserving as much as possible of the original 5-coloring and geometric placement?

### Problem 3. Necessity of the per-direction sum invariant

Chiljagakdeuk has a constant per-direction sum, but Saodo does not. What effect does this difference have on the puzzle’s "completeness" or "difficulty"? When no per-direction sum invariant exists, what additional conditions are needed?

### Problem 4. Absence of edges and compensation mechanisms

Saodo has no explicit edges. Suggest a minimal edge set `E` that creates a Chiljagakdeuk-style graph structure, while minimizing assumptions not present in the original text.

---

## 9. Summary

- Saodo and Chiljagakdeuk are special cases of a common framework `Π(p, q, T)`.
- Chiljagakdeuk has the strict structure `Π(5, 6, 120)`.
- Saodo has the non-uniform structure `Π(5, 3, T_d)`; it belongs to the same family but does not follow the strict rule of Chiljagakdeuk.
- Therefore, the claim "Saodo follows the rule of Chiljagakdeuk" is justified only as far as **weak skeletal sharing** is concerned; the stronger claim of **structural identity** is false.
