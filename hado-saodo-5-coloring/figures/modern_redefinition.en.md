# Modern Combinatorial Redefinition of the Hado 5-Coloring Puzzle

> A definition document that translates the original diagram into modern discrete mathematics language: graphs, colorings, block designs, and rewriting systems. Only elements explicitly present in the original text are treated as primary data; inferred structures are separated into an interpretive layer.

---

## 1. Primitive Objects

The smallest unit of this puzzle is not a "number." What is directly observed in the original text is a **mark**.

Each mark carries four pieces of information simultaneously.

```
mark = (position, circle, numeral, numeral_orientation)
```

- `position`: geometric position in the symmetric cross-shaped layout
- `circle`: circular boundary mark `○`
- `numeral`: Arabic numeral inside the circle
- `numeral_orientation`: rotation angle of the numeral

**Important**: `numeral_orientation` is not a mere rendering option; it is data present in the original figure. Thus a numeral is recorded not simply as `13` but as `(13, -30°)`.

---

## 2. Formal Definition

The structure directly extractable from the original text is as follows.

```
P = (C, L, Θ, X, D, G, R, I)
```

| Symbol | Meaning | Modern Term |
|---|---|---|
| `C` | 20 circular marks | circular marks |
| `L` | numeral label assigned to each circle | labeling function `L: C → {1,…,20}` |
| `Θ` | rotation angle of each numeral | orientation function `Θ: C → SO(2)` |
| `X` | symmetric cross-shaped geometric layout | geometric embedding |
| `D` | direction marks shown in the figure | direction marks |
| `G` | partition into 5 residue classes | residue-class partition |
| `R` | relations among groups (opposition, complement, etc.) | stated group relations |
| `I` | 共積210 | checksum invariant |

This definition contains no **graph** term, because no edge is explicitly given in the original text. `X` is only a coordinate placement, not an edge set.

---

## 3. Geometric Layout

The circles are placed in the following symmetric cross-shaped structure.

```
        ○  ○
        ○  ○

○ ○ ○ ○ ○ ○
○ ○ ○ ○ ○ ○

        ○  ○
        ○  ○
```

Row sizes: `2, 2, 6, 6, 2, 2` → 20 in total.

Substituting the numeral labels gives:

```
        19  2
        7  14

13 8 5 16 4 17
18 3 11 10 12 9

        15 1
        6 20
```

Introducing a coordinate system:

```
X = { (x, y) | 
      y ∈ {4,3}, x ∈ {-1,0}           ∪
      y ∈ {1,0}, x ∈ {-3,-2,-1,0,1,2} ∪
      y ∈ {-1,-2}, x ∈ {-1,0}
    }
```

The label corresponding to each coordinate is the same as in the diagram above.

---

## 4. Numerical Constraint: 共積210

```
Σ_{v∈C} L(v) = 1 + 2 + … + 20 = 210
```

This is a global invariant. Whatever interpretation is added, this sum must be preserved.

---

## 5. Residue Classification: 5-Coloring

The numbers are partitioned into 5 groups according to `mod 5`, using 5 instead of 0.

| Group | Phase | Elements |
|---|---|---|
| 1 | Water | {1, 6, 11, 16} |
| 2 | Fire | {2, 7, 12, 17} |
| 3 | Wood | {3, 8, 13, 18} |
| 4 | Metal | {4, 9, 14, 19} |
| 5 | Earth | {5, 10, 15, 20} |

Formally, there is a coloring function

```
c: C → {Water, Fire, Wood, Metal, Earth}
```

given by `c(v) = L(v) mod 5`. This is an example of a **proper 5-coloring** dividing 20 vertices into 5 color classes.

---

## 6. Group Relations

The relations described in the original text are as follows.

### 6.1 Opposition / Involution

- Water group ↔ Earth group

Formally, an involution on the color set:

```
σ: {1,…,5} → {1,…,5},  σ(1)=5, σ(5)=1
```

It satisfies `σ² = Id`.

### 6.2 Complement / Mutual Support

- Fire group ↔ Metal group

Formally, another involution on the color set:

```
τ: {1,…,5} → {1,…,5},  τ(2)=4, τ(4)=2
```

It satisfies `τ² = Id`.

Together, `σ` and `τ` give two disjoint transpositions `(1 5)` and `(2 4)` on the color set. The remaining element `3` (Wood) is a fixed point.

---

## 7. Operational Interpretation (Optional Interpretive Layer)

The original phrases can be translated into operations as follows.

### 7.1 Generation Rule

> "When wood rubs against wood, fire catches."

```
Wood ⋆ Wood = Fire
```

This is an example of a binary operation `⋆: G × G → G`.

### 7.2 Annihilation Rule

> "When metal and fire stay together, it melts and flows."

```
Metal ⋆ Fire = ∅   (or identity/annihilator)
```

This can be viewed as an absorbing operation.

Formally, this is an example of a partially defined magma or a term rewriting system. Since no edge is directly given in the original text, this part is classified as an **interpretive layer**.

---

## 8. Original Text Interpretation: 河圖五五卽上天數圖，六五卽上地數圖

The original text

> 河圖五五卽上天數圖，六五卽上地數圖

is explained in modern combinatorial language as follows.

### 8.1 Heaven Numbers and Earth Numbers

In classical Heto, the natural numbers 1 through 10 are divided into **Heaven numbers (odd)** and **Earth numbers (even)**.

```
H = {1, 3, 5, 7, 9}      (Heaven numbers, 5 of them)
E = {2, 4, 6, 8, 10}     (Earth numbers, 5 of them)
```

- `|H| = 5`, `ΣH = 1+3+5+7+9 = 25 = 5²`  → **五五(5×5) = chart of Heaven numbers**
- `|E| = 5`, `ΣE = 2+4+6+8+10 = 30 = 5·6` → **六五(6×5) = chart of Earth numbers**

Thus "5×5" and "6×5" are not simple grid sizes but combinatorial identifiers of the **sums** of the two number sets.

### 8.2 Extension to 20 Elements

Extending the Heaven/Earth partition to `V = {1,…,20}` gives:

```
H' = {n ∈ V | n odd}  = {1,3,5,7,9,11,13,15,17,19},  |H'| = 10,  ΣH' = 100
E' = {n ∈ V | n even} = {2,4,6,8,10,12,14,16,18,20}, |E'| = 10,  ΣE' = 110
```

Since `H' = H ∪ (H+10)` and `E' = E ∪ (E+10)`, the Heto structure of 1–10 repeats once more in 11–20. In other words, "5×5 / 6×5" is the basic structure of the interval 1–10, and the 20 numbers form a **2-cycle extension** of this structure.

### 8.3 Block Design Perspective

The following block families can be defined on `V`.

- Heaven block family `B_H`: for each Heaven number `h ∈ H`, a block combining the two cycles
  ```
  B_H = { {1,11}, {3,13}, {5,15}, {7,17}, {9,19} }
  ```
  This partitions `H'` into 5 blocks.

- Earth block family `B_E`: for each Earth number `e ∈ E`, a block combining the two cycles
  ```
  B_E = { {2,12}, {4,14}, {6,16}, {8,18}, {10,20} }
  ```
  This partitions `E'` into 5 blocks.

The phrase "六五(6×5)" does not directly indicate 6 blocks. The key point is the number-theoretic identity that the sum of the 5 Heaven numbers is `25 (=5×5)` and the sum of the 5 Earth numbers is `30 (=5×6)`. The families `B_H` and `B_E` above are block-design interpretations reflecting this identity on the 20 elements.

---

## 9. Unknowns and Research Directions

The following elements are not yet fixed in the original text.

1. **Meaning of numeral rotation Θ**: Is it mere notation, a traversal direction, or a hint at adjacency?
2. **Exact role of direction marks D**: How do they combine with the circular marks?
3. **Whether group relation R is an operation or a relation**: Is it a rewrite rule or a static relation?
4. **Relation between the top/bottom 2×2 arms and the central 2×6 body**: What symmetry group acts on them?

These are subjects for further research. The basic definition `P = (C, L, Θ, X, D, G, R, I)` in this document explicitly includes these unknowns.

---

## 10. Summary

This diagram is, in modern combinatorial terms, the following composite structure.

- **Colored labeled structure**: `(C, L, G)`
- **Geometric embedding**: `(C, X, Θ)`
- **Symmetric relations**: `σ, τ` on the color set
- **Optional operational interpretation**: partial magma `⋆` and term rewriting
- **Heaven/Earth number partition**: `H = {1,3,5,7,9}`, `E = {2,4,6,8,10}` with `ΣH=25=5²`, `ΣE=30=5·6`
- **Block design hypothesis**: `B_H = {{1,11},{3,13},…}`, `B_E = {{2,12},{4,14},…}`

The most conservative definition based only on data explicitly stated in the original text is:

> A geometric number puzzle in which circular marks with rotated numeral labels are placed on a symmetric cross-shaped layout, accompanied by separate direction marks, a 5-residue group partition, group relations, and the checksum condition 共積210.
