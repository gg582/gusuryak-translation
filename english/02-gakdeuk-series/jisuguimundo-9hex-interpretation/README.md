# Jisuguimundo 9-Hex Interpretation

This folder contains a self-contained study of the representative **30-vertex, 9-hexagon Jisuguimundo** (지수귀문도 / Hexagonal Tortoise Problem).

---

## Files

| File | Purpose |
|---|---|
| `jisu_9hex_topology.json` | Exact graph: 30 vertices, 9 hexagons, coordinates, edges |
| `jisu_9hex_solution.json` | A valid assignment with magic constant S = 93 |
| `solve_jisu_9hex.py` | MILP solver that reproduces the solution |
| `draw_jisu_9hex.py` | Renders the solved graph |
| `analyze_jisu_9hex.py` | Modular / CRT analysis and figure generation |
| `visualize_jisu_9hex_extended.py` | Generates extended interpretive visualisations |
| `origin_text.md` | Original Chinese text + English first translation |
| `jisu_9hex_solution.png` | Visualisation of the solved graph |
| `modN_distribution.png` | Spatial residue plots for N = 2, 3, 4, 5, 6, 9, 12 |
| `crt_modA_times_modB.png` | CRT reconstructions mod 3×4, 3×5, 4×5 |
| `jisu_9hex_multiplicity.png` | Made/Used (作/用) separation by vertex multiplicity |
| `jisu_9hex_mod2_symmetry.png` | Parity distribution with reflection axes |
| `jisu_9hex_9to12_palaces.png` | 9 palaces reinterpreted as 12 directional palaces |
| `jisu_9hex_center_periphery.png` | Central three palaces vs surrounding six |
| `jisu_9hex_adjacency_spectrum.png` | Adjacency matrix, degree distribution, spectrum |
| `jisu_9hex_magic_constant.png` | Magic constant 93 emphasised in every hexagon |

---

## Original text

> 六子各得九十三數 — "Each six-number group obtains 93."
> 九宮共得八百三十七數 — "The nine palaces together obtain 837."
> 中眷三宮，三宮爲主則 — "The centre watches over three palaces; three palaces are the master."
> 左右十二子 分爲二宮 若爲以 — "The twelve left/right numbers are divided into two palaces."
> 四正爲四宮，中間六子合爲一宮 — "The four orthogonals are four palaces; the six middle numbers form one palace."
> 凡九宮化爲十二宮 — "Thus the nine palaces are transformed into twelve palaces."

See `origin_text.md` for the full Chinese / English parallel text.

---

## Make / Use separation (作 / 用)

| Quantity | Value |
|---|---:|
| Distinct numbers written (作) | 30 (1–30) |
| Positions used by the structure (用) | 54 (9 hexagons × 6 vertices) |
| Overlap positions | 24 |
| Plain sum of written numbers | 465 |
| Repeated hexagon-total sum H·S | 9 × 93 = 837 |
| Duplication weight D | 372 |

This matches the original phrase **三十子作， 五十四子用**.

### Multiplicity of each vertex

| Multiplicity | Vertices (original id = assigned value) |
|---|---|
| 1 | 1=1, 3=30, 4=5, 5=25, 7=12, 9=4, 11=19, 20=26, 22=13, 24=11, 26=16, 28=8, 29=28, 30=20 |
| 2 | 2=14, 6=27, 8=3, 10=2, 19=21, 23=18, 25=15, 27=22 |
| 3 | 12=9, 13=17, 14=7, 15=24, 16=29, 17=6, 18=10, 21=23 |

---

## Modular classification

Residues are 1-based: `r = value % mod`, with `r = mod` when divisible by `mod`.

### mod 2

| Class | Count | Sum |
|---|---:|---:|
| r1 (odd) | 15 | 225 |
| r2 (even) | 15 | 240 |

The odd/even nodes are distributed fairly evenly across the left/right and top/bottom halves of the graph.

### mod 3

| Class | Count | Sum |
|---|---:|---:|
| r1 | 10 | 145 |
| r2 | 10 | 155 |
| r3 | 10 | 165 |

### mod 4

| Class | Count | Sum |
|---|---:|---:|
| r1 | 8 | 120 |
| r2 | 8 | 128 |
| r3 | 7 | 105 |
| r4 | 7 | 112 |

### mod 5

| Class | Count | Sum |
|---|---:|---:|
| r1 | 6 | 81 |
| r2 | 6 | 87 |
| r3 | 6 | 93 |
| r4 | 6 | 99 |
| r5 | 6 | 105 |

### mod 6, 9, 12

The same residue machinery is applied to moduli 6 (= 2×3), 9 (= 3²), and 12 (= 2²×3).
The generated images `mod6_distribution.png`, `mod9_distribution.png`, and `mod12_distribution.png` show the spatial layout of each classification.

---

## CRT reconstruction (Jin Jiushao / Qin Jiushao)

For coprime pairs of moduli we reconstruct the combined residue using the Chinese Remainder Theorem.

| Pair | Combined modulus | Purpose |
|---|---|---|
| mod 3 × mod 4 | mod 12 | Recovers the mod-12 classes from mod-3 and mod-4 data |
| mod 3 × mod 5 | mod 15 | Links the 3-way and 5-way structures |
| mod 4 × mod 5 | mod 20 | Links the 4-way and 5-way structures |

The figures `crt_mod3_times_mod4.png`, `crt_mod3_times_mod5.png`, and `crt_mod4_times_mod5.png` visualise these combined classes on the graph.

---

## 2·3-based mutation scheme

- **mod 2** is the smallest prime modulus; it controls parity and reflection symmetry.
- **mod 3** is the next basic modulus; it corresponds to the threefold / 9-palace skeleton.
- **mod 4 = 2×2** is a refinement of mod 2.
- **mod 6 = 2×3** combines parity and the threefold structure.
- **mod 9 = 3×3** is the square of the threefold modulus, matching the 9-palace framework.
- **mod 12 = 2²×3** is completely recovered by CRT from mod 3 and mod 4.

This family of moduli is not arbitrary: it grows out of the two base moduli 2 and 3, exactly as the spatial grouping grows out of the four-way / five-way interplay.

---

## Extended visualisation interpretations

### Made / Used separation (`jisu_9hex_multiplicity.png`)

- Thirty distinct numbers (作) are placed into fifty-four hexagon positions (用).
- Vertices closer to the centre are shared by more hexagons, so their multiplicity grows.
- The eight vertices with multiplicity 3 all lie in or around the central hexagon (Hex5).
- This directly illustrates the original phrase **三十子作， 五十四子用**.

### mod 2 symmetry (`jisu_9hex_mod2_symmetry.png`)

- There are exactly 15 odd and 15 even numbers.
- Odd nodes are spread fairly evenly with respect to the vertical (x = 0) and horizontal (y = 0) reflection axes.
- The image visualises the balance between the hexagonal lattice reflection symmetry and the partial-sum invariant.

### 9 palaces → 12 palaces (`jisu_9hex_9to12_palaces.png`)

- Inner blue circles represent the nine hexagon palaces (九宫).
- Outer orange circles represent twelve directional palace units (十二宫), labelled by the twelve earthly branches.
- Grey lines map each hexagon centre to the adjacent directional sectors.
- This visualises the original phrase **凡九宮化爲十二宮**: the nine hexagon units can be reinterpreted as twelve directional units.

### Central three palaces (`jisu_9hex_center_periphery.png`)

- The vertical central column Hex2, Hex5, and Hex8 is highlighted in red.
- These three hexagons form the core axis that governs the six surrounding hexagons.
- This corresponds to the original phrase **中眷三宮， 三宮爲主則**.

### Graph spectrum (`jisu_9hex_adjacency_spectrum.png`)

- The 30×30 adjacency matrix reveals the sparse block pattern created by shared vertices between hexagons.
- The degree distribution is dominated by degree-2 and degree-3 vertices, with a few higher-degree central vertices.
- Adjacency and Laplacian eigenvalues quantify the symmetry and connectivity of the graph.

### Magic constant emphasis (`jisu_9hex_magic_constant.png`)

- The number **93** is placed at the centre of every hexagon, together with the six values that form it.
- All nine hexagons visibly sum to 93.
- This is a direct visualisation of the original phrase **六子各得九十三數**.

---

## Genetic-algorithm solvers

Two GA-based solvers are also provided for finding (or attempting to find)
valid node placements from the gakdeuk perspective.

| File | Description |
|---|---|
| `ga_gakdeuk_solver.py` | Generic permutation GA with optional full or consecutive swap local search |
| `paper_hga_htp_solver.py` | Implementation of the GECCO 2003 hybrid GA for the Hexagonal Tortoise Problem |
| `compare_ga_paper.md` | Comparison of the two GA approaches and the reference paper |

Run them with:

```bash
python ga_gakdeuk_solver.py      # generic GA gakdeuk solver
python paper_hga_htp_solver.py   # paper's hybrid GA
```

Both solvers use variance of cluster sums as the fitness function and report
`optimal` when a perfect assignment is found, or `not_found_within_limit` when
the budget is exhausted without reaching fitness 0.

---

## How to run

```bash
source ../../venv/bin/activate
python solve_jisu_9hex.py                 # recompute the S=93 solution
python draw_jisu_9hex.py                  # draw the solved graph
python analyze_jisu_9hex.py               # generate mod / CRT images and report
python visualize_jisu_9hex_extended.py    # generate extended interpretive figures
python ga_gakdeuk_solver.py               # generic GA gakdeuk solver
python paper_hga_htp_solver.py            # paper's hybrid GA
```

---

## Reference

- Park, Donghwi. *Range of magic constant on Hexagonal Tortoise Problem*, arXiv:1501.03104 (2015).
