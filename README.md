# Gusuryak Puzzle Collection

A repository collecting modern combinatorial redefinitions, verification code, reports, and visualizations for a family of Korean/Chinese mathematical diagrams found in classical texts such as 《구수력(九數略)》.

The collection is organized into two language folders:

- **`english/`** — English-language reports, code, and figures.
- **`korean/`** — Korean-language reports, code, and figures.

Both folders cover overlapping material, often with different emphasis or detail. All cultural or rhetorical interpretations are treated as secondary; the primary focus is observable data and mathematical structure.

---

## Repository structure

```text
.
├── english/                                    # English edition
│   ├── README.md                               # English readme
│   ├── LICENSE.md
│   ├── blog_post.en.md                         # Synthesis blog post
│   ├── english_figure_generators.py            # Shared figure utilities
│   ├── first-post/                             # Introductory post and assets
│   ├── gujagakdeuk-nine-each-gets/             # Gujagakdeuk (九子各得)
│   ├── nakseo-sagudo/                          # Nakseo Sagudo (洛書四九圖)
│   ├── paljagakdeuk-eight-each-gets/           # Paljagakdeuk (八子各得)
│   └── saodo-and-chilja-gakdeuk/               # Saodo, Chiljagakdeuk, generalization
│       ├── chiljagakdeuk-seven-each-gets/      # Chiljagakdeuk (七子各得)
│       ├── hado-saodo-5-coloring/              # Hado / Saodo 5-coloring puzzle
│       └── saodo-chiljagakdeuk-generalization/ # Unified Π(p, q, T) framework
└── korean/                                     # Korean edition
    ├── LICNSE.ko.md
    ├── 구자각득/                                # Gujagakdeuk (九子各得)
    ├── 낙서사구도/                              # Nakseo Sagudo (洛書四九圖)
    ├── 사오도와-칠자각득/                       # Saodo and Chiljagakdeuk
    └── 팔자각득/                                # Paljagakdeuk (八子各得)
```

---

## Puzzles

### 1. Hado / Saodo 5-coloring puzzle

A symmetric cross of 20 numbered circles partitioned by mod-5 residue.

- **English**: `english/saodo-and-chilja-gakdeuk/hado-saodo-5-coloring/`
- **Korean**: `korean/사오도와-칠자각득/하도사오도-지만-사실-5-컬러링-문제/`

Key facts:
- Element set `V = {1, 2, …, 20}`, total sum `Σ V = 210`.
- Five residue classes (Water, Fire, Wood, Metal, Earth) with sums `34, 38, 42, 46, 50`.
- Heaven/Earth number structure: `H = {1,3,5,7,9}`, `E = {2,4,6,8,10}`.

---

### 2. Chiljagakdeuk (七子各得, "Seven Each Gets")

Five clusters of seven numbers, each summing to 120.

- **English**: `english/saodo-and-chilja-gakdeuk/chiljagakdeuk-seven-each-gets/`
- **Korean**: `korean/사오도와-칠자각득/칠자각득-일곱이-따로따로/`

Key facts:
- 5 clusters, each with one center and six peripheral slots.
- Total sum (with multiplicity): `600 = 5 × 120`.
- Centers `{1,2,3,4,5}` form a complete residue system modulo 5.

---

### 3. Unified framework `Π(p, q, T)`

A parameterized framework that contains both Saodo and Chiljagakdeuk as special cases.

- **English**: `english/saodo-and-chilja-gakdeuk/saodo-chiljagakdeuk-generalization/`
- **Korean**: `korean/사오도와-칠자각득/사오도와-칠자각득의-일반화/`

| Puzzle                | p | q | T                              |
|-----------------------|---|---|--------------------------------|
| Chiljagakdeuk         | 5 | 6 | 120 (uniform)                  |
| Saodo (color classes) | 5 | 3 | 34, 38, 42, 46, 50 (variable)  |

---

### 4. Gujagakdeuk (九子各得, "Nine Each Gets")

Five 3×3 grids, each containing nine numbers that sum to 207.

- **English**: `english/gujagakdeuk-nine-each-gets/`
- **Korean**: `korean/구자각득/`

Key facts:
- Uses numbers `1..45`, each exactly once.
- Five grids arranged in a cross; each grid sum is 207.
- Corner sums are all 92; edge-midpoint sums form `90, 91, 92, 93, 94`.

---

### 5. Paljagakdeuk (八子各得, "Eight Each Gets")

Five 3×3 grids with the center cell removed, each containing eight numbers that sum to 164.

- **English**: `english/paljagakdeuk-eight-each-gets/`
- **Korean**: `korean/팔자각득/`

Key facts:
- Uses numbers `1..40`, each exactly once.
- Each of the five grids forms a single 8-cycle.
- The four corner nodes of the center grid act as gateways between the five cycles.

---

### 6. Nakseo Sagudo (洛書四九圖)

A corrected 20-node graph representation of the Nakseo (Luoshu) 4-9 diagram.

- **English**: `english/nakseo-sagudo/`
- **Korean**: `korean/낙서사구도/`

Key facts:
- 20 nodes, 24 edges; four shared vertices `{5, 10, 11, 16}` of degree 4.
- Outer Hamiltonian 20-cycle (sum 210) plus inner 4-cycle (sum 42).
- Nine 4-element palaces, each summing to 42.
- The graph is bipartite (2-colorable) and 2-vertex-connected.

---

## How to run the code

Each puzzle directory contains standalone Python scripts. Typical usage:

```bash
cd english/nakseo-sagudo
python3 analyze_saodo_graph.py          # basic analysis and figures
python3 analyze_saodo_graph_advanced.py # extended graph invariants
```

Most scripts depend only on `matplotlib`, `numpy`, and `networkx`.

---

## Open problems

1. **Existence conditions for `Π(p, q, T)`**: for which triples does a puzzle exist?
2. **Uniformization of Saodo**: can the 20 marks be rearranged into 5 clusters of 7 with equal sum while preserving coloring and geometric constraints?
3. **Graph structure of Nakseo Sagudo**: why does the corrected 20-node graph exhibit perfect 4-fold symmetry in every centrality measure?
4. **Relation between Gujagakdeuk, Paljagakdeuk, and Chiljagakdeuk**: can they be placed inside a single parameterized family extending `Π(p, q, T)`?
5. **Duplication structure in Chiljagakdeuk**: why do certain values appear twice?
