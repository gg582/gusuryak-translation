# Gusuryak Puzzle Collection — English Edition

This is the English edition of a repository that redefines in modern combinatorial terms the Korean-Chinese mathematical diagrams handed down in classical texts such as *Gusuryak* (九數略), and collects verification code and visualization materials.

This is primarily a computational translation project, not a complete history of
origins or transmission. Its historical question is comparative: whether
scholars working roughly three centuries ago confronted recognizable problems
of equal sums, coverage, symmetry, construction, and verification. Priority,
direct transmission, and authorial-intention claims are kept separate from the
formal algorithms unless surviving evidence establishes them.

- **`english/`** — English reports, code, and figures
- **`korean/`** — Korean reports, code, and figures

Under each language edition the puzzles are grouped into the following families:

1. **01-saodo-family** — diagrams from the Hado/Nakseo mod-5 coloring tradition
2. **02-gakdeuk-series** — *gakdeuk* (各得, "each gets") puzzles
3. **03-magic-squares** — classical magic squares and corrected completions
4. **04-unification** — a generalization framework that contains the above families as special cases
5. **05-extra-five** — five additional gakdeuk diagrams
6. **06-nakseo-yukgodo** — the Nakseo Yukgodo and the 270-cell hexagonal-lattice analysis
7. **07-extra-two** — two additional diagrams
8. **08-modn-antipodal** — mod-N residue generalization for diagrams with positionally symmetric complementary pairs (cross-chapter analysis)

---

## Two Readings: Gakdeuk Interpretation and Saodo Interpretation

Nakseo-sagudo and Nakseo-ogudo in `01-saodo-family/` can be read in two ways. This repository covers both readings; the mutual conversion table is organized in the following documents:

- `korean/01-saodo-family/사오도와-각득의-상호해석/saodo_gakdeuk_dual_reading.md`
- `english/01-saodo-family/saodo-gakdeuk-dual-reading/saodo_gakdeuk_dual_reading.md`

### 1. Gakdeuk (各得) Reading

This reading views a diagram as a placement of numbers in which every subset has the same sum.

- **Sajagakdeuk (四子各得, "Four Each Gets")**: each of the nine palaces of Nakseo-sagudo receives four numbers summing to 42.
- **Ojagakdeuk (五子各得, "Five Each Gets")**: each of the nine palaces of Nakseo-ogudo receives five numbers summing to 85.
- **Chiljagakdeuk (七子各得, "Seven Each Gets")**: each of the nine palaces of Nakseo-chilgudo receives seven numbers summing to 224 (= 7 × 32). It partitions the numbers 1 through 63 without overlap.

From a modern point of view this reading has the more advanced features. What it emphasizes is:

- partial-sum invariants (Sajagakdeuk 42, Ojagakdeuk 85)
- the duplication-coefficient equation `k·S = T + D`  
  (`k`: number of palaces, `S`: palace sum, `T`: total sum of distinct numbers, `D`: amount added by duplication)
- block-design and overlap structure (adjacent palaces share elements)
- graph-theoretic structure (central core, four-direction expansion, cycles)

### 2. Saodo (四/五道) Reading

This reading views the diagram as an interaction of 4 (*sa*) and 5 (*o*), i.e. within the framework of traditional wuxing-directional cosmology.

- **Sado (四道, "Four Ways")**: the four directions, four seasons, 4-cycle, four numbers per palace.
- **Odo (五道, "Five Ways")**: the five phases (water, fire, wood, metal, earth), five directions, five numbers per palace.
- **Jiugong (九宫, "Nine Palaces")**: a 3×3 Luoshu magic-square space. This appears most clearly in Nakseo-chilgudo, where each palace receives seven numbers and the center numbers themselves form a classical magic square.

This reading emphasizes:

- five-phase classification by mod-5 residue
- the change from five palaces to nine palaces (五宫化爲九宫)
- cyclic structure (right rotation) and interaction numbers (1,890, 765)
- the background of traditional cosmological symbolism

### 3. Which Reading Is More Useful for Computational Reinterpretation?

It depends on what "advanced" means.

| Criterion | Gakdeuk reading | Saodo reading |
|---|---|---|
| Mathematical generality | High: partial-sum invariants generalize via `Π(p, q, T)` and MILP search. | Low: tied to the specific 4/5 cosmological framework. |
| Verifiability | High: sums, duplication, and graph invariants can be checked mechanically. | Low: symbolic relations leave room for interpretation. |
| Computational formalization | Directly expresses subset-sum and incidence constraints. | Requires formalizing symbolic and directional language first. |
| Ease of modern treatment | High: maps directly to combinatorics and graph theory. | Low: requires translation work before formalization. |

For this project, the gakdeuk reading is more useful computationally because it
isolates observable invariants and makes the puzzle part of a parameterized
family. The saodo reading remains valuable as the source's symbolic and
directional vocabulary. This comparison is about analytical utility, not a
ranking of early-modern mathematical sophistication.

Both readings already exist in the original commentaries. "每宫四子 各得四十二數" and "五子各得 八十五數" are essentially gakdeuk statements, while "五宫化爲九宫", "右旋", and the five-phase classification are saodo statements. Therefore the two readings are not rivals but **two mutually convertible viewpoints on the same diagram**.

### 4. What to Look at for a Modern Reinterpretation?

A modern reinterpretation is most productive when it focuses on the following observable features rather than symbolic commentary.

1. **Numbers used and their total sum** — which integers are used and what their sum is.
2. **Palace / cluster structure** — number of subsets, size of each subset, shared elements.
3. **Partial-sum invariants** — whether every subset has the same sum and how that sum relates to the average.
4. **Mod-5 residues (wuxing)** — arithmetic progression of phase sums and deviations from uniformity.
5. **Duplication / overlap coefficients** — the equation `k·S = T + D` and the geometric origin of `D`.
6. **Graph structure** — adjacency, shared vertices, central cycles, symmetries.
7. **Parameterized placement** — whether the diagram fits into `Π(p, q, T)` and whether it can be generated by the MILP solver in `04-unification/gakdeuk-principle-shared-properties/`.

The gakdeuk reading supplies invariants; the saodo reading supplies cosmological motivation. Using both together lets traditional diagrams be studied accurately as combinatorial objects.

---

## Nakseo Chilgudo (洛書七九圖) Interpretation Summary

Nakseo Chilgudo is a **Chiljagakdeuk (七子各得)** structure in which seven numbers are placed in each of nine palaces.

### Gakdeuk reading

- Numbers used: partition of 1 through 63 without overlap.
- Palace sum: **224** (= 7 × 32, the average of 1–63 is 32).
- Total sum of nine palaces: **2016**.
- An extension of the same pattern as Sajagakdeuk (42 = 4 × 10.5), Ojagakdeuk (85 = 5 × 17), and Yukjagakdeuk (63 = 6 × 10.5).
- The current data contain transcription errors. Eight palaces satisfy 224, but the central palace 6 sums to **174**, with 23, 38, 43 duplicated and 45, 51, 58 missing.

### Corrected Nine-Palace Placement

The following MILP-corrected arrangement keeps the original 50 surrounding numbers while using each of 1–63 exactly once and making every palace sum 224.

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

Only four numbers are changed: in palace 9, 23 → 51 and 36 → 58; in palace 2, 43 → 36 and 38 → 45.

### Saodo reading

- The center numbers 1–9 form the 3×3 **Luoshu Jiugong** magic square.
- The 9 palaces × 7 numbers = 63 numbers can be viewed as distributing seven *qi* (七氣) or the Big Dipper's seven stars within the nine-palace system.
- When every palace sums to 224, the 3×3 palace grid itself acquires magic-square properties: each row, column, and diagonal sums to 672 (= 224 × 3).

---

## Jisuguimundo 9-Hex (Hexagonal Tortoise Problem) Interpretation Summary

The material is organized in a separate folder: `korean/02-gakdeuk-series/지수귀문도-9hex-원문해석/`.

### Basic numbers

- Numbers used: 1–30, each once.
- Number of regular hexagons: 9.
- Sum of the six vertices of each hexagon: **93**.
- Total sum of the nine hexagons: **837**.
- Made/Used separation: 30 made / 54 used, 24 duplicated positions, duplication-weighted sum D = 372.

### Analysis contents

- Original Chinese text → Korean first translation → English first translation (`origin_text.md`).
- MILP solver securing an S = 93 solution (`solve_jisu_9hex.py`).
- Mod 2, 3, 4, 5, 6, 9, 12 residue classification and spatial distribution (`analyze_jisu_9hex.py`).
- CRT (Chinese Remainder Theorem) reconstructions mod 3×4, 3×5, 4×5.
- Cluster-wise rotation analysis treating each hexagon as a rotating object (`analyze_rotations.py`).

---

## Miscellaneous Interesting Points

The most intriguing and not-easily-resolved findings so far are summarized in both Korean and English.

- `korean/04-unification/misc-interesting-points.md`
- `english/04-unification/misc-interesting-points.md`

Topics covered: the gap between made and used, perfect mod-2 balance, the 9→12 palace reinterpretation, the rugged fitness landscape of Jisuguimundo, and open questions about how early-modern mathematicians arrived at valid placements.

---

## Cluster-wise Rotation Analysis

The script `analyze_rotations.py` has been added to every diagram whose clusters are arranged circularly or polygonally, as well as to the newly added 30-vertex, 9-hexagon Jisuguimundo. The script treats each cluster as a rotating object and outputs clockwise order, sums of opposite positions, residue patterns, cluster-level rotational invariants, and the cluster-correspondence relations under global rotation.

To run it for one puzzle:

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

Outputs are saved in each puzzle directory:

- `rotation_report.txt` — rotation order, residue patterns, invariants, global symmetry.
- `rotation_cluster_*.png` — circular visualization per cluster.
- `rotation_overview.png` — summary figure of all clusters.

Nakseo-chilgudo additionally generates rotation-analysis results for both the current data and the corrected partition.
