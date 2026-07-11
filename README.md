# Gusuryak Puzzle Collection

A repository collecting modern combinatorial redefinitions, verification code, reports, and visualizations for a family of Korean/Chinese mathematical diagrams found in classical texts such as 《구수략(九數略)》.

**TODO: VISUALIZERS ARE BROKEN. NEED HEURISTIC VISUALIZER**

The collection is organized into two language editions:

- **`english/`** — English-language reports, code, and figures.
- **`korean/`** — Korean-language reports, code, and figures.

Within each edition the puzzles are grouped by lineage:

1. **First post / introduction** — overview and motivating examples.
2. **Saodo family** — diagrams built on the Hado/Luoshu mod-5 coloring tradition.
3. **Gakdeuk series** — the "Each Gets" puzzles with fixed per-cluster sums.
4. **Magic squares** — classical magic-square constructions and corrections.
5. **Unification** — parameterized frameworks that contain the above as special cases.

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
│   │   └── index.md
│   ├── 01-saodo-family/                        # Hado / Luoshu lineage
│   │   ├── hado-saodo-5-coloring/              # Hado / Saodo 5-coloring puzzle
│   │   ├── nakseo-sagudo/                      # Nakseo Sagudo (洛書四九圖)
│   │   └── nakseo-ogudo/                       # Nakseo Ogudo (洛書五九圖)
│   ├── 02-gakdeuk-series/                      # "Each Gets" puzzles
│   │   ├── chiljagakdeuk-seven-each-gets/      # Chiljagakdeuk (七子各得)
│   │   ├── gujagakdeuk-nine-each-gets/         # Gujagakdeuk (九子各得)
│   │   ├── paljagakdeuk-eight-each-gets/       # Paljagakdeuk (八子各得)
│   │   ├── ojagakdeuk-five-each-gets/          # Ojagakdeuk (五子各得 / Cheonsu-yongodo)
│   │   └── yukjagakdeuk-six-each-gets/         # Yukjagakdeuk (六子各得 / Jisu-yongyukdo & Jisu-guimundo)
│   │       ├── jisu-yong-yukdo/
│   │       └── jisu-guimun-and-yongyukdo/
│   ├── 03-magic-squares/                       # Magic-square analysis
│   │   ├── 01-yukyukdo-six-six-board/
│   │   ├── 02-gusudo-nine-palace/
│   │   ├── 03-baekjajasuyin-yang-chakjong/
│   │   ├── 04-baekjasaengseong-sunsu/
│   │   ├── 05-baekjasaengseong-gyosu/
│   │   ├── 06-baekjayin-yang-jamo-chakjong/
│   │   ├── ANALYSIS_SUMMARY.md
│   │   ├── analyze_squares.py
│   │   ├── generate_and_visualize.py
│   │   └── square.md
│   └── 04-unification/                         # Unified frameworks
│       ├── saodo-chiljagakdeuk-generalization/ # Π(p, q, T) framework
│       └── gakdeuk-principle-shared-properties/# Shared properties of Gakdeuk puzzles
└── korean/                                     # Korean edition
    ├── LICNSE.ko.md
    ├── blog_post.ko.md                         # Synthesis blog post
    ├── 01-saodo-family/                        # 하도/낙서 계열
    │   ├── 하도사오도-지만-사실-5-컬러링-문제/
    │   ├── 낙서사구도/
    │   └── 낙서오구도/
    ├── 02-gakdeuk-series/                      # 각득 계열
    │   ├── 구자각득/
    │   ├── 팔자각득/
    │   ├── 칠자각득-일곱이-따로따로/
    │   ├── 오자각득(천수용오도)/
    │   └── 육자각득(지수용육도와 지수귀문도)/
    ├── 03-magic-squares/                       # 마방진 계열
    │   ├── 01-yukyukdo/
    │   ├── 02-gusudo/
    │   ├── 03-baekjajasuyin-yang-chakjong/
    │   ├── 04-baekjasaengseong-sunsu/
    │   ├── 05-baekjasaengseong-gyosu/
    │   ├── 06-baekjayin-yang-jamo-chakjong/
    │   ├── ANALYSIS_SUMMARY.md
    │   ├── analyze_squares.py
    │   ├── generate_and_visualize.py
    │   └── square.md
    └── 04-unification/                         # 통합 일반화
        ├── 사오도와-칠자각득의-일반화/
        └── 각득 원리를 따르는 퍼즐들의 공유 특성 및 일반화/
```

---

## Puzzle lineages

### 01. Saodo family (Hado / Luoshu tradition)

Diagrams built on a symmetric arrangement of numbered circles partitioned by mod-5 residue.

| Puzzle | English path | Korean path |
|--------|--------------|-------------|
| Hado / Saodo 5-coloring | `english/01-saodo-family/hado-saodo-5-coloring/` | `korean/01-saodo-family/하도사오도-지만-사실-5-컬러링-문제/` |
| Nakseo Sagudo (洛書四九圖) | `english/01-saodo-family/nakseo-sagudo/` | `korean/01-saodo-family/낙서사구도/` |
| Nakseo Ogudo (洛書五九圖) | `english/01-saodo-family/nakseo-ogudo/` | `korean/01-saodo-family/낙서오구도/` |

Key facts:
- Hado / Saodo element set `V = {1, 2, …, 20}`, total sum `Σ V = 210`.
- Five residue classes (Water, Fire, Wood, Metal, Earth) with sums `34, 38, 42, 46, 50`.
- Nakseo Sagudo is a 20-node bipartite graph with an outer Hamiltonian 20-cycle and an inner 4-cycle of sum 42.
- Nakseo Ogudo places the numbers `1` through `33`, each used once, in nine plus-shaped palaces; every palace sums to `85`, and the repeated-count palace total is `765`.

---

### 02. Gakdeuk series ("Each Gets")

Diagrams in which a set of numbers is split into clusters, each cluster having the same prescribed sum.

| Puzzle | English path | Korean path |
|--------|--------------|-------------|
| Chiljagakdeuk (七子各得, 7 each) | `english/02-gakdeuk-series/chiljagakdeuk-seven-each-gets/` | `korean/02-gakdeuk-series/칠자각득-일곱이-따로따로/` |
| Gujagakdeuk (九子各得, 9 each) | `english/02-gakdeuk-series/gujagakdeuk-nine-each-gets/` | `korean/02-gakdeuk-series/구자각득/` |
| Paljagakdeuk (八子各得, 8 each) | `english/02-gakdeuk-series/paljagakdeuk-eight-each-gets/` | `korean/02-gakdeuk-series/팔자각득/` |
| Ojagakdeuk (五子各得, 5 each / Cheonsu-yongodo) | `english/02-gakdeuk-series/ojagakdeuk-five-each-gets/` | `korean/02-gakdeuk-series/오자각득(천수용오도)/` |
| Yukjagakdeuk (六子各得, 6 each / Jisu-yongyukdo & Jisu-guimundo) | `english/02-gakdeuk-series/yukjagakdeuk-six-each-gets/` | `korean/02-gakdeuk-series/육자각득(지수용육도와 지수귀문도)/` |

Key facts:
- **Chiljagakdeuk**: 5 clusters of 7 numbers, each summing to 120.
- **Gujagakdeuk**: 5 full 3×3 grids of 9 numbers, each summing to 207; every palace has corner sum 92.
- **Paljagakdeuk**: 5 clusters of 8 numbers, each summing to 164; each cluster forms an 8-cycle.
- **Ojagakdeuk**: 21 numbers from `1..24` (omitting 3, 10, 22) placed in the Cheonsu-yongodo form, total sum 265, with left/right region sums both equal to 86.
- **Yukjagakdeuk**: the numbers `1..20` placed in five hexagons, each summing to 63; the figure has 8 shared vertices and forms a planar graph with `V = 20`, `E = 24`, `F = 6`. Jisu-guimundo generalizes the same rule to other hexagonal tilings.

---

### 03. Magic squares

Classical magic-square diagrams recorded in the source texts, together with modern verification and corrected completions.

| Puzzle | English path | Korean path |
|--------|--------------|-------------|
| Yukyukdo (Six-Six Board, 六六圖) | `english/03-magic-squares/01-yukyukdo-six-six-board/` | `korean/03-magic-squares/01-yukyukdo/` |
| Gusudo (Nine Palace, 九數圖) | `english/03-magic-squares/02-gusudo-nine-palace/` | `korean/03-magic-squares/02-gusudo/` |
| Baekjajasuyin-yang-chakjong (百子子數陰陽錯綜圖) | `english/03-magic-squares/03-baekjajasuyin-yang-chakjong/` | `korean/03-magic-squares/03-baekjajasuyin-yang-chakjong/` |
| Baekjasaengseong-sunsu (百子生成純數圖) | `english/03-magic-squares/04-baekjasaengseong-sunsu/` | `korean/03-magic-squares/04-baekjasaengseong-sunsu/` |
| Baekjasaengseong-gyosu (百子生成交數圖) | `english/03-magic-squares/05-baekjasaengseong-gyosu/` | `korean/03-magic-squares/05-baekjasaengseong-gyosu/` |
| Baekjayin-yang-jamo-chakjong (百子陰陽子母錯綜圖) | `english/03-magic-squares/06-baekjayin-yang-jamo-chakjong/` | `korean/03-magic-squares/06-baekjayin-yang-jamo-chakjong/` |

Key facts:
- Magic constants: `M_6 = 111`, `M_9 = 369`, `M_10 = 505`.
- **Yukyukdo** (`6×6`) and **Gusudo** (`9×9`) are normal magic squares; a `6×6` associated square is impossible.
- **Gusudo** Example 1 is fully associated (`a_{i,j} + a_{8-i,8-j} = 82`); Example 2 can be corrected to associated.
- The four `10×10` squares are not normal magic squares; valid corrections using `1..100` with all rows, columns, and diagonals summing to `505` are provided in `corrected.md` files.
- None of the six squares is pan-diagonal.

---

### 04. Unification

Parameterized frameworks that contain the earlier puzzles as special cases.

| Puzzle | English path | Korean path |
|--------|--------------|-------------|
| Saodo–Chiljagakdeuk generalization | `english/04-unification/saodo-chiljagakdeuk-generalization/` | `korean/04-unification/사오도와-칠자각득의-일반화/` |
| Gakdeuk-principle shared properties | `english/04-unification/gakdeuk-principle-shared-properties/` | `korean/04-unification/각득 원리를 따르는 퍼즐들의 공유 특성 및 일반화/` |

Key facts:
- The `Π(p, q, T)` framework captures both Saodo color classes and Chiljagakdeuk.

| Puzzle | p | q | T |
|--------|---|---|---|
| Chiljagakdeuk | 5 | 6 | 120 (uniform) |
| Saodo color classes | 5 | 3 | 34, 38, 42, 46, 50 (variable) |

- The shared-properties directory unifies the whole Gakdeuk family (Gujagakdeuk, Ojagakdeuk, Yukjagakdeuk, Chiljagakdeuk, Paljagakdeuk) through common invariants such as `S = n × μ` and the duplication equation `5S = T + D`, and provides a MILP solver for searching new placements.

---

## How to run the code

Each puzzle directory contains standalone Python scripts. Typical usage:

```bash
cd english/01-saodo-family/nakseo-sagudo
python3 analyze_saodo_graph.py          # basic analysis and figures
python3 analyze_saodo_graph_advanced.py # extended graph invariants
```

For the magic-square analyses:

```bash
cd english/03-magic-squares
python3 analyze_squares.py
python3 generate_and_visualize.py
```

For the Gakdeuk-principle MILP solver:

```bash
cd english/04-unification/gakdeuk-principle-shared-properties
python3 gakdeuk_solver.py --all --time-limit 120
```

Most scripts depend only on `matplotlib`, `numpy`, and `networkx`; the MILP solver additionally requires `pulp`.

---

## Open problems

1. **Existence conditions for `Π(p, q, T)`**: for which triples does a puzzle exist?
2. **Uniformization of Saodo**: can the 20 marks be rearranged into 5 clusters of 7 with equal sum while preserving coloring and geometric constraints?
3. **Graph structure of Nakseo Sagudo**: why does the corrected 20-node graph exhibit perfect 4-fold symmetry in every centrality measure?
4. **Relation between Gujagakdeuk, Paljagakdeuk, and Chiljagakdeuk**: can they be placed inside a single parameterized family extending `Π(p, q, T)`?
5. **Duplication structure in Chiljagakdeuk**: why do certain values appear twice?
