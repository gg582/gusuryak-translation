# Report: Modern Combinatorial Analysis of the Chiljagakdeuk (Seven-Each-Gets) Puzzle

---

## 1. Overview

The Chiljagakdeuk (Seven-Each-Gets) puzzle is a diagram composed of five clusters. Each cluster contains seven numbers: one center and six peripheral slots, and each cluster sums to 120. Although the original note says it follows the "Hado-Saodo rule," this report avoids such traditional terminology and redefines the puzzle using only modern combinatorial language.

## 2. Data

| Cluster | Direction | Center | Peripheral slots | Sum |
|---|---|---|---|---|
| C1 | top | 2 | 29, 1, 24, 34, 11, 19 | 120 |
| C2 | left | 3 | 6, 33, 23, 13, 34, 8 | 120 |
| C3 | center | 5 | 22, 7, 20, 30, 26, 10 | 120 |
| C4 | right | 4 | 15, 28, 9, 18, 32, 14 | 120 |
| C5 | bottom | 1 | 35, 16, 21, 24, 6, 17 | 120 |

- Total elements (with multiplicity): 35
- Distinct values: 31
- Repeated values: 1, 6, 24, 34
- Total sum (with multiplicity): 600 = 5 × 120

## 3. Modern Combinatorial Definition

```
P = (C, K, S, X, E, I)
```

- `C`: set of 5 clusters
- `K: C → ℕ`: center labeling function
- `S: C → ℕ⁶`: peripheral slot labeling function
- `X`: 5-direction geometric embedding
- `E`: center-periphery edge set
- `I`: local sum invariant `Σ(c) = 120`

## 4. Key Findings

1. **Sum invariant**: every cluster sums to 120.
2. **Complete mod-5 residue system**: centers `{1,2,3,4,5}` form `ℤ/5ℤ`.
3. **5-direction layout**: top/bottom/left/right/center cross.
4. **Hexagonal peripheral slots**: within each cluster, six slots are arranged roughly on a hexagon.
5. **Duplication structure**: values 1, 6, 24, 34 each appear in two clusters.

## 5. Strengths and Weaknesses

### Strengths
- Clear sum invariant.
- Complete mod-5 residue system at centers.
- Explicit center-periphery graph structure.

### Weaknesses
- Origin of the sum 120 is unexplained.
- Rule for choosing peripheral numbers is not stated.
- Meaning of duplicated values is unclear.
- Inter-cluster relations are not defined.

## 6. Deliverables

- `modern_redefinition.ko.md` / `modern_redefinition.en.md`: modern combinatorial redefinition
- `visualize.py`: visualization code
- `figures/base_layout.png`: base layout
- `figures/residue_distribution.png`: mod-5 residue distribution
- `figures/cluster_structure.png`: cluster template
- `figures/duplication_graph.png`: duplication graph
- `figures/direction_graph.png`: direction graph
