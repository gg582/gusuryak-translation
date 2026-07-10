# Gusuryak Puzzle Collection

A repository collecting modern combinatorial redefinitions, verification code, reports, and visualizations for a family of Korean/Chinese mathematical diagrams found in classical texts such as 《구수력(九數略)》.

The collection is organized into two language editions:

- **`english/`** — English-language reports, code, and figures.
- **`korean/`** — Korean-language reports, code, and figures.

Within each edition the puzzles are grouped by lineage:

1. **First post / introduction** — overview and motivating examples.
2. **Saodo family** — diagrams built on the Hado/Luoshu mod-5 coloring tradition.
3. **Gakdeuk series** — the "Each Gets" puzzles with fixed per-cluster sums.
4. **Unification** — parameterized frameworks that contain the above as special cases.

All cultural or rhetorical interpretations are treated as secondary; the primary focus is observable data and mathematical structure.

---

## Repository structure

```text
.
├── english/                                    # English edition
│   ├── README.md
│   ├── LICENSE.md
│   ├── blog_post.en.md                         # Synthesis blog post
│   ├── english_figure_generators.py            # Shared figure utilities
│   ├── 00-first-post/                          # Introduction and assets
│   ├── 01-saodo-family/                        # Hado / Luoshu lineage
│   │   ├── hado-saodo-5-coloring/              # Hado / Saodo 5-coloring puzzle
│   │   └── nakseo-sagudo/                      # Nakseo Sagudo (洛書四九圖)
│   ├── 02-gakdeuk-series/                      # "Each Gets" puzzles
│   │   ├── chiljagakdeuk-seven-each-gets/      # Chiljagakdeuk (七子各得)
│   │   ├── gujagakdeuk-nine-each-gets/         # Gujagakdeuk (九子各得)
│   │   └── paljagakdeuk-eight-each-gets/       # Paljagakdeuk (八子各得)
│   └── 03-unification/                         # Unified frameworks
│       └── saodo-chiljagakdeuk-generalization/ # Π(p, q, T) framework
└── korean/                                     # Korean edition
    ├── LICNSE.ko.md
    ├── blog_post.ko.md                         # Synthesis blog post
    ├── 01-saodo-family/                        # 하도/낙서 계열
    │   ├── 하도사오도-지만-사실-5-컬러링-문제/
    │   └── 낙서사구도/
    ├── 02-gakdeuk-series/                      # 각득 계열
    │   ├── 구자각득/                           # 九子各得
    │   ├── 팔자각득/                           # 八子各得
    │   └── 칠자각득-일곱이-따로따로/            # 七子各得
    └── 03-unification/                         # 통합 일반화
        └── 사오도와-칠자각득의-일반화/
```

---

## Puzzle lineages

### 01. Saodo family (Hado / Luoshu tradition)

Diagrams built on a symmetric arrangement of 20 numbered circles partitioned by mod-5 residue.

| Puzzle | English path | Korean path |
|--------|--------------|-------------|
| Hado / Saodo 5-coloring | `english/01-saodo-family/hado-saodo-5-coloring/` | `korean/01-saodo-family/하도사오도-지만-사실-5-컬러링-문제/` |
| Nakseo Sagudo (洛書四九圖) | `english/01-saodo-family/nakseo-sagudo/` | `korean/01-saodo-family/낙서사구도/` |

Key facts:
- Element set `V = {1, 2, …, 20}`, total sum `Σ V = 210`.
- Five residue classes (Water, Fire, Wood, Metal, Earth) with sums `34, 38, 42, 46, 50`.
- Nakseo Sagudo is a 20-node bipartite graph with an outer Hamiltonian 20-cycle and an inner 4-cycle of sum 42.

---

### 02. Gakdeuk series ("Each Gets")

Diagrams in which a set of numbers is split into clusters, each cluster having the same prescribed sum.

| Puzzle | English path | Korean path |
|--------|--------------|-------------|
| Chiljagakdeuk (七子各得, 7 each) | `english/02-gakdeuk-series/chiljagakdeuk-seven-each-gets/` | `korean/02-gakdeuk-series/칠자각득-일곱이-따로따로/` |
| Paljagakdeuk (八子各得, 8 each) | `english/02-gakdeuk-series/paljagakdeuk-eight-each-gets/` | `korean/02-gakdeuk-series/팔자각득/` |
| Gujagakdeuk (九子各得, 9 each) | `english/02-gakdeuk-series/gujagakdeuk-nine-each-gets/` | `korean/02-gakdeuk-series/구자각득/` |

Key facts:
- **Chiljagakdeuk**: 5 clusters of 7 numbers, each summing to 120.
- **Paljagakdeuk**: 5 clusters of 8 numbers, each summing to 164; each cluster forms an 8-cycle.
- **Gujagakdeuk**: 5 3×3 grids of 9 numbers, each summing to 207.

---

### 03. Unification

A parameterized framework `Π(p, q, T)` that contains both Saodo and Chiljagakdeuk as special cases.

| Puzzle | English path | Korean path |
|--------|--------------|-------------|
| Saodo–Chiljagakdeuk generalization | `english/03-unification/saodo-chiljagakdeuk-generalization/` | `korean/03-unification/사오도와-칠자각득의-일반화/` |

| Puzzle | p | q | T |
|--------|---|---|---|
| Chiljagakdeuk | 5 | 6 | 120 (uniform) |
| Saodo color classes | 5 | 3 | 34, 38, 42, 46, 50 (variable) |

---

## How to run the code

Each puzzle directory contains standalone Python scripts. Typical usage:

```bash
cd english/01-saodo-family/nakseo-sagudo
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
