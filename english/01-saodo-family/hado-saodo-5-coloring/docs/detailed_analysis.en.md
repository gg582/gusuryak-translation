# Detailed Property Autopsy

> This document systematically dissects the form, numerics, spatial distribution, classical correspondences, and unknown elements of the Hado 5-Coloring Puzzle.

---

## 1. Data Summary

The final verified layout of the 20 elements is:

```
        19  2
        7  14
13  8   5   16  4   17
18  3   11  10  12   9
        15  1
        6  20
```

- Element set: `{1, 2, …, 20}`
- Total sum: `210` (= 1+2+…+20)
- Structure: top arm 2×2, central body 2×6, bottom arm 2×2

---

## 2. Symmetry Analysis

### 2.1 Formal Symmetry

The outline of the layout is a symmetric cross. However, the full figure including numeral labels does **not** satisfy geometric symmetry.

### 2.2 180° Rotation

A 180° rotation about the origin `(x, y) → (-x, -y)` maps circles away from existing slots. For example, `(-1, 4) = 19` rotates to `(1, -4)`, where no slot exists.

Thus the **shape is symmetric, but the labeling is not**.

### 2.3 Reflection

- Reflection across `x = 0`: `(-1, 4) = 19` would move to `(1, 4)`, which has no slot.
- Horizontal reflection similarly fails.

**Conclusion**: The puzzle has **shape symmetry** but **no labeling symmetry**. The layout is a frame, and the numbers are intentionally filled in a non-symmetric way.

---

## 3. Row and Column Sum Analysis

### 3.1 Row Sums

| y-coordinate | Elements | Sum |
|---|---|---|
| 4 | 19, 2 | 21 |
| 3 | 7, 14 | 21 |
| 1 | 13, 8, 5, 16, 4, 17 | 63 |
| 0 | 18, 3, 11, 10, 12, 9 | 63 |
| -1 | 15, 1 | 16 |
| -2 | 6, 20 | 26 |

- Top arm sum: `21 + 21 = 42`
- Central body sum: `63 + 63 = 126`
- Bottom arm sum: `16 + 26 = 42`
- Total: `42 + 126 + 42 = 210`

**The top and bottom arms have equal sums (42 each).** The two rows of the central body also have equal sums (63 each).

### 3.2 Column Sums

| x-coordinate | Elements | Sum |
|---|---|---|
| -3 | 13, 18 | 31 |
| -2 | 8, 3 | 11 |
| -1 | 19, 7, 5, 11, 15, 6 | 63 |
| 0 | 2, 14, 16, 10, 1, 20 | 63 |
| 1 | 4, 12 | 16 |
| 2 | 17, 9 | 26 |

**The x = -1 and x = 0 columns both sum to 63**, matching the central body row sums.

---

## 4. Group Distribution and Spatial Structure

The positions of the mod-5 groups are:

| Group | Phase | Elements | Spatial Feature |
|---|---|---|---|
| 1 | Water | 1, 6, 11, 16 | Central columns (x=-1, 0), lower + center |
| 2 | Fire | 2, 7, 12, 17 | Top arm + central right |
| 3 | Wood | 3, 8, 13, 18 | **Entire left 2 columns** of central body |
| 4 | Metal | 4, 9, 14, 19 | Top arm + central right |
| 5 | Earth | 5, 10, 15, 20 | Central columns (x=-1, 0), lower + center |

**Notable features**:

1. **Wood occupies the entire left two columns of the central body** (13, 18, 8, 3), corresponding to the classical Heto direction "East = Wood."
2. **Fire and Metal are distributed in the top arm and central right**, corresponding to "South = Fire" and "West = Metal."
3. **Water and Earth are interleaved in the central columns and bottom arm**, corresponding to "North = Water" and "Center = Earth."
4. Water and Earth are **vertically interleaved**. For example, along x = -1 we see 5(Water), 11(Water), 15(Earth), 6(Water).

---

## 5. Correspondence with the Classical Heto

The classical Heto five-direction / five-phase correspondence is:

| Direction | Numbers | Phase |
|---|---|---|
| North (bottom) | 1, 6 | Water |
| South (top) | 2, 7 | Fire |
| East (left) | 3, 8 | Wood |
| West (right) | 4, 9 | Metal |
| Center | 5, 10 | Earth |

Mapping the current layout onto this frame:

- **East (left) = Wood**: The left four slots of the central body are all Wood. This correspondence is very strong.
- **South (top) / West (right) = Fire/Metal**: The top arm and central right are filled with Fire/Metal, though the two groups are mixed.
- **North (bottom) / Center = Water/Earth**: The bottom arm and central columns are filled with Water/Earth, also mixed.

**Interpretation**: In modern terms, this layout is an example of a **5-direction coloring**. Not every direction is filled with a single pure group, but each direction is dominated by one of two groups.

---

## 6. Adjacency Hypothesis

The original text contains no explicit edges. To apply graph theory, we must introduce adjacency hypotheses.

### 6.1 Simplest Hypothesis: Grid Adjacency

Connect slots that are immediate neighbors in the same row or column. Then the central body becomes part of a 2×6 grid graph.

### 6.2 Distance-Based Hypothesis: k-Nearest Neighbors

Connect each slot to its k nearest Euclidean neighbors. For k=2, each slot has about 2 neighbors.

### 6.3 Graph-Theoretic Implications

Under any adjacency hypothesis, we must check:

- **Proper coloring**: Do adjacent vertices ever share the same color?
- **Connectedness**: Is the graph connected?
- **Symmetry**: What is the automorphism group of the graph?

The current mod-5 coloring is **not a proper graph coloring**: for example, 13 and 18 are adjacent and both Wood. This confirms that the coloring is a **mod-5 residue partition**, not a graph-theoretic proper coloring.

---

## 7. Numeral Orientation Analysis

In the original diagram, all numerals are tilted by approximately **-30°**.

### 7.1 Possible Interpretations

1. **Decorative element**: It may simply be a font style.
2. **Rotated coordinate system**: The whole figure may imply a rotated frame.
3. **Direction / flow indicator**: Since all numerals point the same way, they may indicate a common "flow."
4. **Reading direction**: They may hint at the order in which numerals are read.

### 7.2 Current Conclusion

The tilt is certainly data, but its **meaning remains unclear**. Without additional textual or visual context, no definite interpretation is possible.

---

## 8. Integrated Interpretation

This puzzle is a superposition of three layers.

1. **Geometric layer**: A symmetric cross-shaped layout. The shape is symmetric, but the labeling is not.
2. **Numerical layer**: The integers 1–20, total sum 210, and structural equalities among row/column/arm sums.
3. **Symbolic layer**: The mod-5 five-phase partition, Heto Heaven/Earth numbers, and opposition/complement relations.

These layers are not independent. For example:

- Top arm sum = bottom arm sum = 42
- Central body row sums = central column sums = 63
- Wood group concentrated on the left side of the central body

These structures appear intentional rather than accidental.

---

## 9. Open Problems

1. **Meaning of orientation Θ**: Decoration or computational direction?
2. **Exact definition of direction marks D**: How do they combine with circular slots?
3. **Explicit adjacency relation E**: What graph structure should be assumed?
4. **Operationalization of σ and τ**: Are they static relations or rewrite rules?
5. **Geometric link between 5×5/6×5 and the 20-slot layout**: Which parts of the layout correspond to the Heaven/Earth sums?
