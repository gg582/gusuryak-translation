# Integrated Report: Modern Combinatorial Redefinition of the Hado 5-Coloring Puzzle

**Date**: 2026-07-07

---

## 1. Overview

This report systematically redefines a Heto-based 5-coloring diagram in the language of modern combinatorics and discrete mathematics, and presents a detailed autopsy of its properties. Only data explicitly stated in the original text is treated as primary; inferred structures are clearly marked.

---

## 2. Final Data

```
        19  2
        7  14
13  8   5   16  4   17
18  3   11  10  12   9
        15  1
        6  20
```

- Element set: `V = {1, 2, …, 20}`
- Total sum: `ΣV = 210`
- Structure: top arm 2×2, central body 2×6, bottom arm 2×2

---

## 3. Modern Combinatorial Definition

```
P = (C, L, Θ, X, D, G, R, I)
```

| Symbol | Meaning |
|---|---|
| `C` | 20 circular marks |
| `L` | numeral labeling function `L: C → {1,…,20}` |
| `Θ` | numeral orientation function `Θ: C → SO(2)` |
| `X` | symmetric cross-shaped geometric embedding |
| `D` | direction marks |
| `G` | five-phase partition by mod 5 |
| `R` | group relations (opposition, complement, etc.) |
| `I` | checksum invariant 共積210 |

---

## 4. Key Findings

### 4.1 5-Coloring Structure

- `c(v) = L(v) mod 5` partitions the vertices into 5 color classes of 4 each.
- Classes: Water `{1,6,11,16}`, Fire `{2,7,12,17}`, Wood `{3,8,13,18}`, Metal `{4,9,14,19}`, Earth `{5,10,15,20}`.

### 4.2 Heaven and Earth Numbers

- From the original text "河圖五五卽上天數圖，六五卽上地數圖":
  - Heaven numbers `H = {1,3,5,7,9}`, `ΣH = 25 = 5²`
  - Earth numbers `E = {2,4,6,8,10}`, `ΣE = 30 = 5·6`
- Extension to 1–20: `H' = H ∪ (H+10)`, `E' = E ∪ (E+10)` with `ΣH' = 100`, `ΣE' = 110`.

### 4.3 Opposition and Complement

- `σ = (1 5)`: Water ↔ Earth (opposition)
- `τ = (2 4)`: Fire ↔ Metal (complement)
- Wood (3) is the fixed point.

### 4.4 Symmetry

- The layout shape is a symmetric cross, but the **numeral labeling is not symmetric**.
- 180° rotation, x=0 reflection, and horizontal reflection all fail.

### 4.5 Row and Column Sums

- Top arm sum = bottom arm sum = 42
- Central body row sums = 63 each
- Central column sums (x=-1, x=0) = 63 each
- `42 + 126 + 42 = 210`

### 4.6 Spatial Group Distribution

- Wood: entire left four slots of the central body
- Fire/Metal: top arm + central right
- Water/Earth: central columns + bottom arm

---

## 5. Historical Assessment

| Era | Evidence |
|---|---|
| Ancient | Heto, five phases, Heaven/Earth numbers, five-direction correspondence |
| Medieval | Continuation of I-Ching-style symbolic interpretation |
| Early Modern | Precursor of verification conditions such as 共積210 |
| Modern | Traces of set, function, and symmetry thinking, but no axiom system |
| Contemporary | Translatable into graphs, colorings, block designs, rewriting systems |

**Overall**: computational potential in a premodern source diagram; no priority
or direct-transmission claim is made here.

---

## 6. Strengths

1. Exact partition of 1–20 into five groups of four by mod 5.
2. Heaven/Earth structure repeats in 11–20 as a 2-cycle.
3. Structural equalities among row, column, and arm sums.
4. Spatial concentration of Wood and correspondence to Heto east direction.
5. Opposition/complement formalizable as clean involutions.

---

## 7. Weaknesses and Open Problems

1. Meaning of numeral orientation Θ unclear.
2. Exact role of direction marks D unclear.
3. No adjacency relation (graph edge) given.
4. Operational rules (generation/annihilation) incompletely defined.
5. Geometric link between 5×5/6×5 and the 20-slot layout unclear.

---

## 8. Deliverables

### Documents

- `figures/modern_redefinition.ko.md` / `modern_redefinition.en.md` — modern combinatorial redefinition
- `docs/explanation.ko.md` / `explanation.en.md` — historical classification, strengths, weaknesses
- `docs/detailed_analysis.ko.md` / `detailed_analysis.en.md` — detailed property autopsy
- `docs/reconstruction_policy.ko.md` / `reconstruction_policy.en.md` — conservative source-data reconstruction policy and script
- `figures/math_problems.ko.md` / `math_problems.en.md` — modern combinatorial problems extracted from mathematical texts

### Code

- `figures/visualize_puzzle.py` — base puzzle and relation visualizations
- `figures/reconstruct_source.py` — conservative reconstruction of source data (positions, labels, orientations, groups, checksum)
- `figures/extract_problems.py` — per-problem visualization generator
- `figures/analyze_properties.py` — detailed property analysis visualizations

### Images

| File | Content |
|---|---|
| `puzzle_base.png` | symmetric cross-shaped original layout |
| `puzzle_reconstruction.png` | conservative reconstruction preserving positions, circles, labels, orientations, groups, checksum |
| `puzzle_filled_groups.png` | 5-coloring visualization with circles filled by residue group |
| `puzzle_relations.png` | five-phase opposition/complement diagram |
| `puzzle_block_design.png` | 5×5/6×5 block design hypothesis |
| `puzzle_heaven_earth.png` | Heaven/Earth number partition visualization |
| `problem_01_coloring.png` ~ `problem_06_checksum.png` | 6 modern combinatorial problem visualizations |
| `analysis_01_symmetry.png` | symmetry analysis |
| `analysis_02_rowcol.png` | row/column sum analysis |
| `analysis_03_distribution.png` | group spatial distribution |
| `analysis_04_heto.png` | Heto direction correspondence |
| `analysis_05_adjacency.png` | adjacency hypothesis |
| `analysis_06_orientation.png` | numeral orientation analysis |

---

## 9. Conclusion

This puzzle is a body of data expressed in ancient language. Yet its numerical, spatial, and symbolic structures are refined enough for modern combinatorics. This report conservatively defines the data, visualizes it, and proposes several modern interpretive frameworks. The remaining task is to clarify the unknowns `Θ`, `D`, and `E` (edges), and on that basis formalize a complete mathematical problem.
