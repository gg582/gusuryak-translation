# Saodo, Chiljagakdeuk, and the Hado 5-Coloring Puzzle

A single repository that collects the source data, modern combinatorial redefinitions, verification code, and visualizations for three related Korean mathematical diagrams:

1. **Hado / Saodo 5-coloring puzzle** (`hado-saodo-5-coloring/`) – a symmetric cross of 20 numbered circles partitioned by mod-5 residue.
2. **Chiljagakdeuk (七子各得, "Seven Each Gets")** (`chiljagakdeuk-seven-each-gets/`) – five clusters of seven numbers, each summing to 120.
3. **Generalization** (`saodo-chiljagakdeuk-generalization/`) – a unified parameterized framework `Π(p, q, T)` that contains both puzzles as special cases.

All cultural or rhetorical interpretations are stripped away; only observable data and mathematical structure are kept.

---

## Project structure

```text
.
├── blog_post.en.md                         # Synthesis blog post
├── README.md                               # This file
├── hado-saodo-5-coloring/                  # Saodo / Hado 5-coloring puzzle
│   ├── docs/
│   │   ├── detailed_analysis.en.md         # Symmetry, row/column sums, spatial distribution
│   │   ├── explanation.en.md               # Historical placement, strengths, weaknesses
│   │   ├── reconstruction_policy.en.md     # Conservative reconstruction policy
│   │   └── report.en.md                    # Integrated report
│   └── figures/
│       ├── analyze_properties.py           # Detailed property analysis figures
│       ├── extract_problems.py             # Per-problem visualizations
│       ├── math_problems.en.md             # Six modern combinatorial problems
│       ├── modern_redefinition.en.md       # Formal definition of the puzzle
│       ├── reconstruct_source.py           # Faithful source reconstruction
│       ├── visualize_puzzle.py             # Base puzzle and relation visualizations
│       └── *.png                           # Generated figures
├── chiljagakdeuk-seven-each-gets/          # Chiljagakdeuk puzzle
│   ├── figures/                            # Generated visualizations
│   ├── from_textbook.py                    # Textbook-style matplotlib drawing
│   ├── modern_redefinition.en.md           # Formal definition
│   ├── report.en.md                        # Integrated report
│   ├── visualize.py                        # Modern visualization code
│   ├── 七子各得_예시.pdf                    # Example PDF
│   └── 七子各得_예시.png                    # Example PNG
└── saodo-chiljagakdeuk-generalization/     # Unified framework
    ├── docs/
    │   └── generalization.en.md            # General definition and comparison
    ├── compare_structures.py               # Verification script
    └── report.en.md                        # Integrated report
```

---

## Part 1: Hado / Saodo 5-coloring puzzle

### 1.1 Source data

The diagram is a symmetric cross of 20 circular slots:

```text
        19  2
        7  14
13  8   5   16  4   17
18  3   11  10  12   9
        15  1
        6  20
```

- **Element set**: `V = {1, 2, …, 20}`, each used exactly once.
- **Total sum**: `Σ V = 210` (= `1 + 2 + … + 20`).
- **Geometry**: top arm 2×2, central body 2×6, bottom arm 2×2.
- **Numeral orientation**: every numeral is slanted approximately `-30°`.
- **Coloring**: `c(v) = L(v) mod 5` (with 0 mapped to 5).

| Residue group | Phase  | Elements          |
|---------------|--------|-------------------|
| 1             | Water  | {1, 6, 11, 16}    |
| 2             | Fire   | {2, 7, 12, 17}    |
| 3             | Wood   | {3, 8, 13, 18}    |
| 4             | Metal  | {4, 9, 14, 19}    |
| 5             | Earth  | {5, 10, 15, 20}   |

### 1.2 Formal definition

The structure directly extractable from the source is

```text
P = (C, L, Θ, X, D, G, R, I)
```

| Symbol | Meaning                                                              |
|--------|----------------------------------------------------------------------|
| `C`    | 20 circular marks                                                    |
| `L`    | Labeling function `L: C → {1,…,20}`                                  |
| `Θ`    | Numeral orientation `Θ: C → SO(2)` (approx. `-30°`)                  |
| `X`    | Symmetric cross-shaped geometric embedding                           |
| `D`    | Direction marks shown in the figure (role unclear)                   |
| `G`    | Five-phase partition by mod-5 residue                                |
| `R`    | Stated group relations: opposition `σ = (1 5)`, complement `τ = (2 4)` |
| `I`    | Checksum invariant `Σ L(v) = 210`                                    |

No edge set is given in the original text, so graph-theoretic analyses require extra hypotheses.

### 1.3 Mathematical structures

**Heaven and Earth numbers.** From the classical phrase "河圖五五卽上天數圖，六五卽上地數圖":

```text
H = {1, 3, 5, 7, 9}      (Heaven numbers)
E = {2, 4, 6, 8, 10}     (Earth numbers)
ΣH = 25 = 5²
ΣE = 30 = 5·6
```

Extending to `1..20` gives `H' = H ∪ (H+10)`, `E' = E ∪ (E+10)`, with `ΣH' = 100`, `ΣE' = 110`. The original 1–10 Heto structure repeats as a 2-cycle.

**Row and column sums.**

| y-coordinate | Elements                | Sum |
|--------------|-------------------------|-----|
| 4            | 19, 2                   | 21  |
| 3            | 7, 14                   | 21  |
| 1            | 13, 8, 5, 16, 4, 17     | 63  |
| 0            | 18, 3, 11, 10, 12, 9    | 63  |
| -1           | 15, 1                   | 16  |
| -2           | 6, 20                   | 26  |

Top arm sum = bottom arm sum = 42; central body rows each sum to 63. The `x = -1` and `x = 0` columns also sum to 63.

**Symmetry.** The outline is a symmetric cross, but the numeral labeling has no geometric symmetry: 180° rotation and reflection across `x = 0` both fail.

**Group relations.** Two involutions on the color set:

```text
σ = (1 5) : Water ↔ Earth      (opposition)
τ = (2 4) : Fire ↔ Metal       (complement)
3 (Wood) is fixed
```

**Operational interpretation (optional).**

```text
Wood + Wood → Fire
Metal + Fire → ∅   (annihilation)
```

These are treated as an interpretive layer because no edges or operation domains are given explicitly.

### 1.4 Code in `hado-saodo-5-coloring/figures/`

#### `visualize_puzzle.py`

Defines the 20 nodes with coordinates and labels, draws four figures:

- `puzzle_base.png` – the symmetric cross with colored borders by residue group and rotated numerals.
- `puzzle_relations.png` – five phases on a pentagon, showing `σ` (Water↔Earth) and `τ` (Fire↔Metal).
- `puzzle_block_design.png` – the `B_H` five-phase blocks and `B_E` Heaven-number blocks.
- `puzzle_heaven_earth.png` – Heaven/Earth partition of `1..10` and its 2-cycle extension to `1..20`.

Key data structure:

```python
nodes = [
    {"pos": (-1, 3), "label": 19},
    {"pos": (0, 3),  "label": 2},
    # ... 20 entries
]

def group_of(label):
    g = label % 5
    return 5 if g == 0 else g
```

#### `reconstruct_source.py`

Conservative reconstruction preserving only data actually present in the source: positions, circles, numeral values, `-30°` orientations, mod-5 group partition, and the checksum 210. It explicitly avoids adding artificial edges, nearest-neighbor assumptions, rewrite systems, or algebraic semantics.

Key checks at runtime:

```python
assert len(labels) == 20
assert sorted(labels) == list(range(1, 21))
assert checksum(labels) == 210
```

Produces `puzzle_reconstruction.png` and `puzzle_filled_groups.png`.

#### `extract_problems.py`

Generates one figure for each of the six modern combinatorial problems:

1. Proper 5-coloring on the symmetric cross.
2. Heaven/Earth partition of `1..20` (`ΣH'=100`, `ΣE'=110`).
3. Involutions `σ` and `τ` on the five phases.
4. Block-design intersection matrix `M[i,j] = |B_H[i] ∩ B_E[j]|`.
5. Term rewriting rules `Wood+Wood→Fire`, `Metal+Fire→∅`.
6. Checksum invariant `Σ = 210`.

#### `analyze_properties.py`

Creates six detailed analysis figures:

1. `analysis_01_symmetry.png` – original layout, 180° rotation test, reflection test.
2. `analysis_02_rowcol.png` – row sums and column sums.
3. `analysis_03_distribution.png` – spatial distribution of the five residue groups.
4. `analysis_04_heto.png` – classical Heto direction-phase correspondence.
5. `analysis_05_adjacency.png` – a 2-nearest-neighbor adjacency hypothesis.
6. `analysis_06_orientation.png` – `-30°` numeral orientation.

---

## Part 2: Chiljagakdeuk (七子各得, "Seven Each Gets")

### 2.1 Source data

Five clusters, each with one center and six peripheral slots. Every cluster sums to 120.

| Cluster | Direction | Center | Peripheral slots          | Sum |
|---------|-----------|--------|---------------------------|-----|
| C1      | top       | 2      | 29, 1, 24, 34, 11, 19    | 120 |
| C2      | left      | 3      | 6, 33, 23, 13, 34, 8     | 120 |
| C3      | center    | 5      | 22, 7, 20, 30, 26, 10    | 120 |
| C4      | right     | 4      | 15, 28, 9, 18, 32, 14    | 120 |
| C5      | bottom    | 1      | 35, 16, 21, 24, 6, 17    | 120 |

- Total elements (with multiplicity): 35.
- Distinct values: 31.
- Repeated values: 1, 6, 24, 34 (each appears twice).
- Total sum (with multiplicity): `600 = 5 × 120`.

### 2.2 Formal definition

```text
P = (C, K, S, X, E, I)
```

| Symbol | Meaning                                              |
|--------|------------------------------------------------------|
| `C`    | Set of 5 clusters                                    |
| `K`    | Center labeling `K: C → ℕ`                           |
| `S`    | Peripheral slot labeling `S: C → ℕ⁶`                 |
| `X`    | 2D geometric embedding (cross + hexagon)             |
| `E`    | Center-periphery edge set (explicitly given)         |
| `I`    | Local sum invariant `Σ(cluster) = 120`               |

The centers `{1,2,3,4,5}` form a complete residue system modulo 5.

### 2.3 Geometric layout

```text
        C1(0, 3.3)
            |
C2(-3.3, 0) — C3(0,0) — C4(3.3, 0)
            |
        C5(0, -3.3)
```

Inside each cluster the six peripheral slots are arranged on a regular hexagon around the center, so the whole figure is **five 7-point star configurations arranged in a cross**.

### 2.4 Code in `chiljagakdeuk-seven-each-gets/`

#### `from_textbook.py`

A compact matplotlib script that reproduces the textbook-style example. It defines five groups of seven numbers, five cluster center positions, and seven slot offsets (six hexagonal positions plus the center), then draws each cluster with a boundary circle, radial edges, and numeral labels. Output: `chiljagakdeuk_example.png` and `.pdf`.

Key data:

```python
EXAMPLE_GROUPS = [
    [29, 1, 24, 34, 11, 19, 2],
    [6, 33, 23, 13, 34, 8, 3],
    [22, 7, 20, 30, 26, 10, 5],
    [15, 28, 9, 18, 32, 14, 4],
    [35, 16, 21, 24, 6, 17, 1],
]
```

#### `visualize.py`

A richer visualization that uses color-coded residues and produces five analysis figures:

- `figures/base_layout.png` – full layout with residue-color borders.
- `figures/residue_distribution.png` – stacked bar chart of mod-5 residue counts per cluster.
- `figures/cluster_structure.png` – generic center + 6 peripheral slots template.
- `figures/duplication_graph.png` – graph edges for values appearing in two clusters.
- `figures/direction_graph.png` – cross-shaped adjacency of the five clusters.

Residue coloring is 1-based:

```python
def residue(n):
    g = n % 5
    return 5 if g == 0 else g
```

---

## Part 3: Unified framework `Π(p, q, T)`

### 3.1 General definition

Both puzzles fit inside a single parameterized family:

```text
Π = (D, M, X, E, K, S, W, Φ)
```

| Symbol | Meaning                                              |
|--------|------------------------------------------------------|
| `D`    | Direction set, `|D| = p`                             |
| `M`    | Element / mark set                                   |
| `X`    | Geometric placement `X: M → ℝ²`                      |
| `E`    | Edge set `E ⊆ M × M`                                 |
| `K`    | Direction-center correspondence `K: D → M`           |
| `S`    | Per-direction peripheral slots `S: D → 2^M`          |
| `W`    | Weight function `W: M → ℕ`                           |
| `Φ`    | Invariant conditions                                 |

This collapses to three parameters:

```text
Π(p, q, T)
```

- `p`: number of directions.
- `q`: number of peripheral slots per direction.
- `T`: target sum per direction.

### 3.2 Parameter mapping

| Puzzle                | p | q | T                              |
|-----------------------|---|---|--------------------------------|
| Chiljagakdeuk         | 5 | 6 | 120 (same for all directions)  |
| Saodo (color classes) | 5 | 3 | 34, 38, 42, 46, 50 (variable)  |

### 3.3 Does Saodo follow the rule of Chiljagakdeuk?

| Level | Condition                              | Saodo satisfies? |
|-------|----------------------------------------|------------------|
| 0     | Five-direction structure               | Yes              |
| 1     | Center-periphery split possible        | Yes (3 slots)    |
| 2     | `q = 6` peripheral slots               | No               |
| 3     | Constant per-direction sum `T`         | No               |
| 4     | Explicit center-periphery edges        | No               |

**Verdict:** In the strict sense, no. Saodo shares the weak skeleton (five directions, mod-5 residues, complete residue system of centers, global sum invariant) but not the strong structure (six peripheral slots, constant per-direction sum, explicit edges). It is best viewed as a non-uniform parameter setting inside `Π(5, q, T)`.

### 3.4 Code in `saodo-chiljagakdeuk-generalization/`

#### `compare_structures.py`

Directly verifies both puzzles against the `Π(p, q, T)` framework.

```python
SAODO_LABELS = {
    "water": [1, 6, 11, 16],
    "fire":  [2, 7, 12, 17],
    "wood":  [3, 8, 13, 18],
    "metal": [4, 9, 14, 19],
    "earth": [5, 10, 15, 20],
}

CHILJA_CLUSTERS = {
    "top":    {"center": 2, "periphery": [29, 1, 24, 34, 11, 19]},
    "left":   {"center": 3, "periphery": [6, 33, 23, 13, 34, 8]},
    "center": {"center": 5, "periphery": [22, 7, 20, 30, 26, 10]},
    "right":  {"center": 4, "periphery": [15, 28, 9, 18, 32, 14]},
    "bottom": {"center": 1, "periphery": [35, 16, 21, 24, 6, 17]},
}

def residue(value):
    return ((value - 1) % 5) + 1
```

The script checks:

- Number of directions `p`.
- Whether centers form a complete residue system mod 5.
- Whether all clusters have the same number of peripheral slots `q`.
- Whether all cluster sums are equal to a constant `T`.

Output:

```text
Chiljagakdeuk: Π(5, 6, 120)
Saodo color classes: Π(5, 3, T_d) with T_d = 34, 38, 42, 46, 50
```

---

## Part 4: How to run the code

All Python scripts are standalone. From each directory, run:

```bash
# Hado / Saodo 5-coloring visualizations
cd hado-saodo-5-coloring/figures
python3 visualize_puzzle.py
python3 reconstruct_source.py
python3 extract_problems.py
python3 analyze_properties.py

# Chiljagakdeuk visualizations
cd ../../chiljagakdeuk-seven-each-gets
python3 visualize.py
python3 from_textbook.py

# Generalization comparison
cd ../saodo-chiljagakdeuk-generalization
python3 compare_structures.py
```

Most scripts depend only on `matplotlib` and `numpy`.

---

## Part 5: Open problems

1. **Existence conditions for `Π(p, q, T)`**: for which positive-integer triples does a puzzle exist?
2. **Uniformization of Saodo**: can the 20 marks be rearranged into 5 clusters of 7 with equal sum while preserving the 5-coloring and geometric constraints?
3. **Meaning of numeral orientation `Θ`** in the Saodo diagram: decoration, traversal order, or rotated coordinate frame?
4. **Role of direction marks `D`**: how do they combine with the circular slots?
5. **Minimal edge set for Saodo**: what is the smallest graph structure that makes the diagram Chiljagakdeuk-like without adding unsupported assumptions?
6. **Duplication structure in Chiljagakdeuk**: why do 1, 6, 24, 34 each appear twice?

---

## Summary

- The **Hado/Saodo 5-coloring puzzle** is a data-rich diagram: 20 unique numbers, a symmetric cross layout, a mod-5 5-coloring, Heaven/Earth number structure, and a checksum of 210.
- **Chiljagakdeuk** is a stricter diagram: five clusters of seven numbers with a constant per-cluster sum of 120 and explicit center-periphery edges.
- Both can be placed inside the same parameterized family **`Π(p, q, T)`**.
- Chiljagakdeuk is the uniform case **`Π(5, 6, 120)`**.
- Saodo is the non-uniform case **`Π(5, 3, T_d)`**.

By translating these traditional diagrams into modern combinatorial language, we obtain precise mathematical objects, verifiable conditions, and a list of concrete open problems.
