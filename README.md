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
│   │   ├── nakseo-ogudo/                       # Nakseo Ogudo (洛書五九圖)
│   │   ├── nakseo-chilgudo/                    # Nakseo Chilgudo (洛書七九圖)
│   │   └── saodo-gakdeuk-dual-reading/         # Side-by-side Gakdeuk / Saodo conversion
│   ├── 02-gakdeuk-series/                      # "Each Gets" puzzles
│   │   ├── chiljagakdeuk-seven-each-gets/      # Chiljagakdeuk (七子各得)
│   │   ├── gujagakdeuk-nine-each-gets/         # Gujagakdeuk (九子各得)
│   │   ├── paljagakdeuk-eight-each-gets/       # Paljagakdeuk (八子各得)
│   │   ├── ojagakdeuk-five-each-gets/          # Ojagakdeuk (五子各得 / Cheonsu-yongodo)
│   │   ├── yukjagakdeuk-six-each-gets/         # Yukjagakdeuk (六子各得 / Jisu-yongyukdo & Jisu-guimundo)
│   │   │   ├── jisu-yong-yukdo/
│   │   │   └── jisu-guimun-and-yongyukdo/
│   │   └── jisuguimundo-9hex-interpretation/   # 30-vertex 9-hex Jisuguimundo (지수귀문도)
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
    ├── LICENSE.ko.md
    ├── blog_post.ko.md                         # Synthesis blog post
    ├── 01-saodo-family/                        # 하도/낙서 계열
    │   ├── 하도사오도-지만-사실-5-컬러링-문제/
    │   ├── 낙서사구도/
    │   ├── 낙서오구도/
    │   ├── 낙서칠구도/
    │   └── 사오도와-각득의-상호해석/             # 각득 ↔ 사오도 상호 변환 정리
    ├── 02-gakdeuk-series/                      # 각득 계열
    │   ├── 구자각득/
    │   ├── 팔자각득/
    │   ├── 칠자각득-일곱이-따로따로/
    │   ├── 오자각득(천수용오도)/
    │   ├── 육자각득(지수용육도와 지수귀문도)/
    │   └── 지수귀문도-9hex-원문해석/             # 30정점 9육각형 지수귀문도
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
| Nakseo Chilgudo (洛書七九圖) | `english/01-saodo-family/nakseo-chilgudo/` | `korean/01-saodo-family/낙서칠구도/` |
| Gakdeuk ↔ Saodo dual reading | `english/01-saodo-family/saodo-gakdeuk-dual-reading/` | `korean/01-saodo-family/사오도와-각득의-상호해석/` |

Key facts:
- Hado / Saodo element set `V = {1, 2, …, 20}`, total sum `Σ V = 210`.
- Five residue classes (Water, Fire, Wood, Metal, Earth) with sums `34, 38, 42, 46, 50`.
- Nakseo Sagudo is a 20-node bipartite graph with an outer Hamiltonian 20-cycle and an inner 4-cycle of sum 42.
- Nakseo Ogudo places the numbers `1` through `33`, each used once, in nine plus-shaped palaces; every palace sums to `85`, and the repeated-count palace total is `765`.
- Nakseo Chilgudo places the numbers `1` through `63` in nine palaces arranged on a 3×3 Luoshu grid; each palace has seven numbers and is intended to sum to `224` (7 × 32). The current data files contain transcription errors (duplicates `23, 38, 43` and omissions `45, 51, 58`); a corrected partition restoring all nine sums to `224` is given in the directory.

#### Nakseo Chilgudo in the two readings

**Gakdeuk reading.** The diagram is a partition of the integers `1` through `63` into nine blocks of seven numbers, each summing to `224` (= 7 × 32, the average of 1..63). Unlike Sagudo and Ogudo, there is no overlap, so `make = use = 63` and the duplication weight `D = 0`. The current data are corrupted: the palace centered at `6` sums to `174`, while the other eight palaces already sum to `224`. A corrected partition preserving 50 of the 54 surrounding numbers is:

| Palace (center) | Seven numbers | Sum |
|---|---|---:|
| 4 | 4, 22, 27, 31, 37, 43, 60 | 224 |
| 9 | 9, 10, 15, 36, 45, 54, 55 | 224 |
| 2 | 2, 17, 28, 29, 39, 47, 62 | 224 |
| 3 | 3, 16, 26, 30, 40, 48, 61 | 224 |
| 5 | 5, 14, 23, 32, 41, 50, 59 | 224 |
| 7 | 7, 20, 24, 34, 38, 44, 57 | 224 |
| 8 | 8, 11, 12, 35, 49, 53, 56 | 224 |
| 1 | 1, 18, 19, 25, 46, 52, 63 | 224 |
| 6 | 6, 13, 21, 33, 42, 51, 58 | 224 |

**Saodo reading.** The nine centers form the classical 3×3 Luoshu magic square, giving the nine-palace (九宫) spatial skeleton. Each palace receives seven numbers, which can be read as seven stars / seven qi distributed over the nine palaces. When every palace sums to `224`, the 3×3 grid of palace sums is also magic: every row, column, and diagonal sums to `672`.

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
| Jisuguimundo 9-hex (地數龜文圖) | `english/02-gakdeuk-series/jisuguimundo-9hex-interpretation/` | `korean/02-gakdeuk-series/지수귀문도-9hex-원문해석/` |

Key facts:
- **Chiljagakdeuk**: 5 clusters of 7 numbers, each summing to 120.
- **Gujagakdeuk**: 5 full 3×3 grids of 9 numbers, each summing to 207; every palace has corner sum 92.
- **Paljagakdeuk**: 5 clusters of 8 numbers, each summing to 164; each cluster forms an 8-cycle.
- **Ojagakdeuk**: 21 numbers from `1..24` (omitting 3, 10, 22) placed in the Cheonsu-yongodo form, total sum 265, with left/right region sums both equal to 86.
- **Yukjagakdeuk**: the numbers `1..20` placed in five hexagons, each summing to 63; the figure has 8 shared vertices and forms a planar graph with `V = 20`, `E = 24`, `F = 6`. Jisu-guimundo generalizes the same rule to other hexagonal tilings.
- **Jisuguimundo 9-hex**: a representative 30-vertex, 9-hexagon tiling with magic constant `S = 93`; 30 distinct numbers are written (作) and 54 positions are used (用), giving 24 overlaps. The folder contains the exact graph, a verified solution, modular analysis (mod 2/3/4/5/6/9/12), CRT reconstructions, and per-hexagon rotation analysis.

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

## Two readings: the Gakdeuk interpretation and the Saodo interpretation

The puzzles in `01-saodo-family/` can be read in two ways, both of which are documented in this repository. A side-by-side mutual conversion is given in:

- `english/01-saodo-family/saodo-gakdeuk-dual-reading/saodo_gakdeuk_dual_reading.md`
- `korean/01-saodo-family/사오도와-각득의-상호해석/saodo_gakdeuk_dual_reading.md`

### The Gakdeuk (各得, “Each Gets”) reading

In this reading the diagram is treated as a partition of numbers into subsets that all share the same sum.

- **Sajagakdeuk (Four-Each-Gets, 四子各得)**: the nine palaces of Nakseo Sagudo each contain four numbers and each sum to 42.
- **Ojagakdeuk (Five-Each-Gets, 五子各得)**: the nine palaces of Nakseo Ogudo each contain five numbers and each sum to 85.
- **Chiljagakdeuk (Seven-Each-Gets, 七子各得)**: the nine palaces of Nakseo Chilgudo each contain seven numbers and are intended to sum to 224, using the integers 1 through 63 exactly once.

This is the more modern-looking reading. It foregrounds:

- partial-sum invariants (`42` for Sagudo, `85` for Ogudo);
- the duplication-count equation `k·S = T + D`, where `k` is the number of palaces, `S` the palace sum, `T` the total of all distinct numbers, and `D` the overlap-weighted duplication;
- block design and overlap structure (neighboring palaces share elements);
- graph-theoretic properties (central core, four-direction extension, Hamiltonian cycles).

### The Saodo (四/五道, “Four/Five Way”) reading

In this reading the diagram is treated as an interplay between the number 4 and the number 5, rooted in the traditional wuxing-direction cosmology.

- **Four-Way (사도)**: four cardinal directions, four seasons, 4-cycles, four children per palace.
- **Five-Way (오도)**: five wuxing phases, five directions, five children per palace.
- **Nine-Palace Luoshu grid (九宫)**: the 3×3 Luoshu square, most clearly visible in Nakseo Chilgudo, where nine palaces each receive seven numbers and the centers themselves form the classical magic square.

This reading foregrounds:

- mod-5 residue classes (Water, Fire, Wood, Metal, Earth);
- the transformation of five classes into nine palaces (`五宫化爲九宫`);
- cyclic / rotational order (`右旋`) and mutual transformation numbers (`1890`, `765`);
- the embedding of traditional cosmological symbols.

### Which reading is more advanced for the late-imperial publication period (~1700)?

The answer depends on what “advanced” means.

| Criterion | Gakdeuk reading | Saodo reading |
|---|---|---|
| Mathematical generality | Higher: partial-sum invariants generalize to `Π(p, q, T)` and MILP search. | Lower: tied to the specific 4/5 cosmological framework. |
| Verifiability | Higher: sums, overlaps, and graph invariants can be checked mechanically. | Lower: symbolic relations require interpretive choices. |
| Period naturalness | Lower: explicit equality of subset sums was not the standard language of the time. | Higher: wuxing, directions, and 4/5 numerology were mainstream scholarly tools. |
| Modern tractability | Higher: directly maps to combinatorics and graph theory. | Lower: requires translation before formal analysis. |

From a **modern standpoint**, the Gakdeuk reading is the more progressive one, because it isolates an observable invariant and makes the puzzle part of a parameterized family.  
From a **late-imperial Korean/Chinese scholarly standpoint**, the Saodo reading would have looked more natural and complete, because it embeds the numbers in the then-dominant wuxing-direction cosmology.

Neither reading is anachronistic. The source annotations already contain both: phrases such as `每宫四子 各得四十二數` and `五子各得 八十五數` are essentially Gakdeuk statements, while `五宫化爲九宫`, `右旋`, and the wuxing classification are Saodo statements. The two readings are therefore **mutually convertible interpretations** of the same diagram, not competitors.

### What to look at for a modern reinterpretation

To reinterpret these diagrams in modern terms, focus on the following observable features rather than on symbolic exegesis:

1. **Number set and total sum** — which integers are used and what their sum is.
2. **Palace/cluster structure** — how many subsets exist, how large each is, and which elements they share.
3. **Partial-sum invariant** — whether every subset has the same sum, and how that sum relates to the average.
4. **mod-5 residue classes (wuxing)** — the arithmetic progression of class sums and its deviation from uniformity.
5. **Duplication / overlap counts** — the equation `k·S = T + D` and the geometric origin of `D`.
6. **Graph structure** — adjacency, shared vertices, central cycles, and symmetry when edges are well defined.
7. **Parameterized placement** — whether the diagram fits into `Π(p, q, T)` or can be generated by the MILP solver in `04-unification/gakdeuk-principle-shared-properties/`.

A modern reading is most productive when it treats the Gakdeuk and Saodo layers as two complementary descriptions: Gakdeuk gives the invariant, Saodo gives the cosmological motivation, and together they form a single object that can be studied combinatorially.

---

## Computational complexity of the subtasks

The historical diagrams themselves are small, concrete objects: verifying any stated sum, coloring, or graph property is polynomial-time. The classifications below apply to the **natural generalizations** of those diagrams to arbitrary sizes or arbitrary target values.

| Puzzle / family | Subtask | Complexity | Reason / remark |
|---|---|---|---|
| **Hado / Saodo 5-coloring** | Verify checksum 210 and mod-5 color classes | **P** | Direct summation and residue test; O(\|V\|). |
| **Hado / Saodo 5-coloring** | Decide whether a labeling of a given geometric slot graph satisfies the 5-coloring / checksum constraints | **NP-complete** | Captures graph coloring (k ≥ 3) and exact-cover-type slot constraints. |
| **Hado / Saodo 5-coloring** | Check involutions σ, τ and the block-design intersection matrix | **P** | Finite, constant-size checks. |
| **Hado / Saodo 5-coloring** | Decide confluence of the interpretive term-rewriting rules | **P** (for this finite system) | General TRS confluence is undecidable, but the two-rule system here is finite and can be exhausted. |
| **Nakseo Sagudo (Sajagakdeuk)** | Verify every palace sums to 42 | **P** | 9 palaces × 4 numbers. |
| **Nakseo Sagudo (Sajagakdeuk)** | Decide existence of a placement of 1..20 into 9 overlapping 4-sets all summing to 42 | **NP-complete** | Exact-cover / integer-programming with overlap constraints; the MILP solver in `04-unification` handles small instances. |
| **Nakseo Sagudo (Sajagakdeuk)** | Decide Hamiltonicity of the inferred boundary 20-cycle graph | **NP-complete** (general) | Hamiltonian cycle is NP-complete in general; for this specific 20-node graph the answer is known by inspection. |
| **Nakseo Ogudo (Ojagakdeuk)** | Verify every palace sums to 85 and the 9-palace total is 765 | **P** | Direct summation. |
| **Nakseo Ogudo (Ojagakdeuk)** | Decide existence of a placement of 1..33 into nine plus-shaped palaces all summing to 85 | **NP-complete** | Same structure as Sagudo with a different overlap graph. |
| **Nakseo Chilgudo (Chiljagakdeuk)** | Verify every palace sums to 224 | **P** | Direct summation; 9 palaces × 7 numbers. |
| **Nakseo Chilgudo (Chiljagakdeuk)** | Decide whether 1..63 can be partitioned into nine 7-element blocks, each summing to 224, with fixed Luoshu centers | **NP-complete** | Equal-sum set partition with fixed elements; the current data is a corrupted witness. |
| **Nakseo Chilgudo (Chiljagakdeuk)** | Find the corrected partition given in `korean/01-saodo-family/낙서칠구도/chiljagakdeuk.md` | **NP-hard** | Solved by MILP while preserving 50 of 54 surrounding numbers. |
| **Chiljagakdeuk** | Verify the 5 clusters of 7 numbers each sum to 120 | **P** | O(35) additions. |
| **Chiljagakdeuk** | Decide existence of a `Π(5, 6, 120)` placement | **NP-complete** | Multiway number partitioning with repetition and mod-5 center constraints. |
| **Chiljagakdeuk** | Find a valid placement | **NP-hard** | Solved by the MILP solver for the known instance; general search is NP-hard. |
| **Gujagakdeuk** | Verify the five 3×3 grids sum to 207 and corner sums to 92 | **P** | Direct checks. |
| **Gujagakdeuk** | Decide existence of a placement satisfying the grid / corner-sum constraints | **NP-complete** | Exact-cover over 3×3 sub-grids with shared cells. |
| **Paljagakdeuk** | Verify five 8-cycles each sum to 164 | **P** | Direct checks. |
| **Paljagakdeuk** | Decide existence of a placement of 1..40 into five overlapping 8-cycles | **NP-complete** | Generalizes equal-sum cycle decomposition. |
| **Ojagakdeuk (Cheonsu-yongodo)** | Verify left/right sums and per-region sums | **P** | Direct checks. |
| **Ojagakdeuk (Cheonsu-yongodo)** | Decide existence of a placement of 21 numbers from 1..24 with missing set {3,10,22} and prescribed region sums | **NP-complete** | Constrained subset selection with shared boundary vertices. |
| **Yukjagakdeuk (Jisu-yong-yukdo / Jisu-guimundo)** | Verify five hexagons each sum to 63 | **P** | Direct checks. |
| **Yukjagakdeuk (Jisu-yong-yukdo / Jisu-guimundo)** | Decide existence of a honeycomb placement of 1..20 into five 6-cycles all summing to 63 | **NP-complete** | Honeycomb adjacency plus equal-sum hexagons; solved by MILP for the known instance. |
| **Magic squares** | Verify a filled square is normal magic | **P** | O(n²) row/column/diagonal checks. |
| **Magic squares** | Construct a normal magic square of order n | **P** | Deterministic methods (Siamese, Strachey, etc.) run in O(n²) for every n ≠ 2. |
| **Magic squares** | Complete a partially filled magic square | **NP-complete** | Generalizes Latin-square completion, which is NP-complete. |
| **Magic squares** | Correct one of the 10×10 source squares to a valid magic square while preserving a given set of entries | **NP-hard** | Search version of the completion problem. |
| **Π(p, q, T) / Gakdeuk MILP** | Decide whether a puzzle exists for arbitrary `(p, q, T)` | **NP-complete** | Captures exact cover and bounded multiway partitioning. |
| **Π(p, q, T) / Gakdeuk MILP** | Find an optimal or feasible placement | **NP-hard** | Mixed-integer linear programming is NP-hard in general. |
| **Π(p, q, T) / Gakdeuk MILP** | Verify a candidate placement against the constraints | **P** | Linear-time constraint evaluation. |

### Why the contrast matters

For every puzzle in this collection there are two different questions:

1. **Verification**: “Does this concrete diagram satisfy its stated rule?” — always easy (P).
2. **Existence / completion**: “Is there *any* diagram that satisfies the rule for these parameters?” — usually hard (NP-complete or NP-hard) when the size is not fixed.

This is why the repository separates the *given historical instances* (verified directly) from the *generalized search problems* (attacked with MILP, heuristic, and constructive algorithms). The historical diagrams act as witnesses for specific NP witnesses, but finding new witnesses for arbitrary parameters remains computationally difficult.

---

## Per-cluster rotation analysis

Every diagram that has cyclic clusters now has an `analyze_rotations.py` script, including the new 30-vertex 9-hex Jisuguimundo. These scripts treat each cluster/palace/hexagon as a rotating object, report cyclic orders, opposite-position sums, mod-residue patterns around the cycle, cluster-level rotational invariants, and global rotation mappings between clusters.

To run the rotation analysis for a single puzzle:

```bash
cd english/02-gakdeuk-series/chiljagakdeuk-seven-each-gets
python3 analyze_rotations.py
```

To run all rotation analyses at once:

```bash
find . -name analyze_rotations.py -print0 | \
  while IFS= read -r -d '' script; do
    (cd "$(dirname "$script")" && python3 analyze_rotations.py)
  done
```

Outputs are saved locally in each puzzle directory:

- `rotation_report.txt` — cyclic orders, residue patterns, invariants, and global symmetry mappings.
- `rotation_cluster_*.png` — circular per-cluster visualizations.
- `rotation_overview.png` — combined overview of all clusters.

Nakseo Chilgudo additionally emits separate corrupted-data and corrected-partition rotation reports/figures.

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

## Miscellaneous interesting points

A curated list of the most intriguing and not-easily-resolved findings from
the whole exploration is maintained in both languages:

- `english/04-unification/misc-interesting-points.md`
- `korean/04-unification/misc-interesting-points.md`

Topics include the made/used (作/用) gap, perfect mod-2 balance, the 9→12
palace reinterpretation, the rugged fitness landscape of the Hexagonal
Tortoise Problem, and open questions about 18th-century solution methods.

---

## Open problems

1. **Existence conditions for `Π(p, q, T)`**: for which triples does a puzzle exist?
2. **Uniformization of Saodo**: can the 20 marks be rearranged into 5 clusters of 7 with equal sum while preserving coloring and geometric constraints?
3. **Graph structure of Nakseo Sagudo**: why does the corrected 20-node graph exhibit perfect 4-fold symmetry in every centrality measure?
4. **Relation between Gujagakdeuk, Paljagakdeuk, and Chiljagakdeuk**: can they be placed inside a single parameterized family extending `Π(p, q, T)`?
5. **Duplication structure in Chiljagakdeuk**: why do certain values appear twice?
