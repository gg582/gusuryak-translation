# Jisuguimundo 9-hex Analysis Report

## 1. Basic quantities and made/used (作/用) separation

| Quantity | Value |
|---|---:|
| Distinct numbers written (作) | 30 (1–30) |
| Positions used by the structure (用) | 54 (9 hexagons × 6 vertices) |
| Overlap positions | 24 |
| Plain sum of written numbers (T) | 465 |
| Repeated hexagon-total sum (H·S) | 9 × 93 = 837 |
| Duplication weight (D) | 372 |

The original phrase **三十子作， 五十四子用** is matched exactly: 30 distinct numbers are written, 54 positions are used, and 24 positions are overlaps.

### Vertex multiplicities

| Multiplicity | Vertices (original id = assigned value) |
|---|---|
| 1 times | 1=1, 3=30, 4=5, 5=25, 7=12, 9=4, 11=19, 20=26, 22=13, 24=11, 26=16, 28=8, 29=28, 30=20 |
| 2 times | 2=14, 6=27, 8=3, 10=2, 19=21, 23=18, 25=15, 27=22 |
| 3 times | 12=9, 13=17, 14=7, 15=24, 16=29, 17=6, 18=10, 21=23 |

## 2. Modular classification and group interpretation

### mod 2

| Residue class | Count | Class sum |
|---|---:|---:|
| r1 | 15 | 225 |
| r2 | 15 | 240 |

Residue pattern for each hexagon:

| Hexagon | Values | Residue pattern | Sum |
|---|---|---|---:|
| Hex1 | [25, 16, 2, 23, 22, 5] | 1-2-2-1-2-1 | 93 |
| Hex2 | [2, 11, 27, 6, 24, 23] | 2-1-1-2-2-1 | 93 |
| Hex3 | [22, 23, 24, 17, 3, 4] | 2-1-2-1-1-2 | 93 |
| Hex4 | [27, 30, 8, 15, 7, 6] | 1-2-2-1-1-2 | 93 |
| Hex5 | [6, 24, 17, 10, 29, 7] | 2-2-1-2-1-1 | 93 |
| Hex6 | [3, 17, 10, 18, 19, 26] | 1-1-2-2-1-2 | 93 |
| Hex7 | [7, 29, 9, 21, 12, 15] | 1-1-1-1-2-1 | 93 |
| Hex8 | [10, 18, 13, 14, 9, 29] | 2-2-1-2-1-1 | 93 |
| Hex9 | [9, 21, 20, 1, 28, 14] | 1-1-2-1-2-2 | 93 |

### mod 3

| Residue class | Count | Class sum |
|---|---:|---:|
| r1 | 10 | 145 |
| r2 | 10 | 155 |
| r3 | 10 | 165 |

Residue pattern for each hexagon:

| Hexagon | Values | Residue pattern | Sum |
|---|---|---|---:|
| Hex1 | [25, 16, 2, 23, 22, 5] | 1-1-2-2-1-2 | 93 |
| Hex2 | [2, 11, 27, 6, 24, 23] | 2-2-3-3-3-2 | 93 |
| Hex3 | [22, 23, 24, 17, 3, 4] | 1-2-3-2-3-1 | 93 |
| Hex4 | [27, 30, 8, 15, 7, 6] | 3-3-2-3-1-3 | 93 |
| Hex5 | [6, 24, 17, 10, 29, 7] | 3-3-2-1-2-1 | 93 |
| Hex6 | [3, 17, 10, 18, 19, 26] | 3-2-1-3-1-2 | 93 |
| Hex7 | [7, 29, 9, 21, 12, 15] | 1-2-3-3-3-3 | 93 |
| Hex8 | [10, 18, 13, 14, 9, 29] | 1-3-1-2-3-2 | 93 |
| Hex9 | [9, 21, 20, 1, 28, 14] | 3-3-2-1-1-2 | 93 |

### mod 4

| Residue class | Count | Class sum |
|---|---:|---:|
| r1 | 8 | 120 |
| r2 | 8 | 128 |
| r3 | 7 | 105 |
| r4 | 7 | 112 |

Residue pattern for each hexagon:

| Hexagon | Values | Residue pattern | Sum |
|---|---|---|---:|
| Hex1 | [25, 16, 2, 23, 22, 5] | 1-4-2-3-2-1 | 93 |
| Hex2 | [2, 11, 27, 6, 24, 23] | 2-3-3-2-4-3 | 93 |
| Hex3 | [22, 23, 24, 17, 3, 4] | 2-3-4-1-3-4 | 93 |
| Hex4 | [27, 30, 8, 15, 7, 6] | 3-2-4-3-3-2 | 93 |
| Hex5 | [6, 24, 17, 10, 29, 7] | 2-4-1-2-1-3 | 93 |
| Hex6 | [3, 17, 10, 18, 19, 26] | 3-1-2-2-3-2 | 93 |
| Hex7 | [7, 29, 9, 21, 12, 15] | 3-1-1-1-4-3 | 93 |
| Hex8 | [10, 18, 13, 14, 9, 29] | 2-2-1-2-1-1 | 93 |
| Hex9 | [9, 21, 20, 1, 28, 14] | 1-1-4-1-4-2 | 93 |

### mod 5

| Residue class | Count | Class sum |
|---|---:|---:|
| r1 | 6 | 81 |
| r2 | 6 | 87 |
| r3 | 6 | 93 |
| r4 | 6 | 99 |
| r5 | 6 | 105 |

Residue pattern for each hexagon:

| Hexagon | Values | Residue pattern | Sum |
|---|---|---|---:|
| Hex1 | [25, 16, 2, 23, 22, 5] | 5-1-2-3-2-5 | 93 |
| Hex2 | [2, 11, 27, 6, 24, 23] | 2-1-2-1-4-3 | 93 |
| Hex3 | [22, 23, 24, 17, 3, 4] | 2-3-4-2-3-4 | 93 |
| Hex4 | [27, 30, 8, 15, 7, 6] | 2-5-3-5-2-1 | 93 |
| Hex5 | [6, 24, 17, 10, 29, 7] | 1-4-2-5-4-2 | 93 |
| Hex6 | [3, 17, 10, 18, 19, 26] | 3-2-5-3-4-1 | 93 |
| Hex7 | [7, 29, 9, 21, 12, 15] | 2-4-4-1-2-5 | 93 |
| Hex8 | [10, 18, 13, 14, 9, 29] | 5-3-3-4-4-4 | 93 |
| Hex9 | [9, 21, 20, 1, 28, 14] | 4-1-5-1-3-4 | 93 |

### mod 6

| Residue class | Count | Class sum |
|---|---:|---:|
| r1 | 5 | 65 |
| r2 | 5 | 70 |
| r3 | 5 | 75 |
| r4 | 5 | 80 |
| r5 | 5 | 85 |
| r6 | 5 | 90 |

Residue pattern for each hexagon:

| Hexagon | Values | Residue pattern | Sum |
|---|---|---|---:|
| Hex1 | [25, 16, 2, 23, 22, 5] | 1-4-2-5-4-5 | 93 |
| Hex2 | [2, 11, 27, 6, 24, 23] | 2-5-3-6-6-5 | 93 |
| Hex3 | [22, 23, 24, 17, 3, 4] | 4-5-6-5-3-4 | 93 |
| Hex4 | [27, 30, 8, 15, 7, 6] | 3-6-2-3-1-6 | 93 |
| Hex5 | [6, 24, 17, 10, 29, 7] | 6-6-5-4-5-1 | 93 |
| Hex6 | [3, 17, 10, 18, 19, 26] | 3-5-4-6-1-2 | 93 |
| Hex7 | [7, 29, 9, 21, 12, 15] | 1-5-3-3-6-3 | 93 |
| Hex8 | [10, 18, 13, 14, 9, 29] | 4-6-1-2-3-5 | 93 |
| Hex9 | [9, 21, 20, 1, 28, 14] | 3-3-2-1-4-2 | 93 |

### mod 9

| Residue class | Count | Class sum |
|---|---:|---:|
| r1 | 4 | 58 |
| r2 | 4 | 62 |
| r3 | 4 | 66 |
| r4 | 3 | 39 |
| r5 | 3 | 42 |
| r6 | 3 | 45 |
| r7 | 3 | 48 |
| r8 | 3 | 51 |
| r9 | 3 | 54 |

Residue pattern for each hexagon:

| Hexagon | Values | Residue pattern | Sum |
|---|---|---|---:|
| Hex1 | [25, 16, 2, 23, 22, 5] | 7-7-2-5-4-5 | 93 |
| Hex2 | [2, 11, 27, 6, 24, 23] | 2-2-9-6-6-5 | 93 |
| Hex3 | [22, 23, 24, 17, 3, 4] | 4-5-6-8-3-4 | 93 |
| Hex4 | [27, 30, 8, 15, 7, 6] | 9-3-8-6-7-6 | 93 |
| Hex5 | [6, 24, 17, 10, 29, 7] | 6-6-8-1-2-7 | 93 |
| Hex6 | [3, 17, 10, 18, 19, 26] | 3-8-1-9-1-8 | 93 |
| Hex7 | [7, 29, 9, 21, 12, 15] | 7-2-9-3-3-6 | 93 |
| Hex8 | [10, 18, 13, 14, 9, 29] | 1-9-4-5-9-2 | 93 |
| Hex9 | [9, 21, 20, 1, 28, 14] | 9-3-2-1-1-5 | 93 |

### mod 12

| Residue class | Count | Class sum |
|---|---:|---:|
| r1 | 3 | 39 |
| r2 | 3 | 42 |
| r3 | 3 | 45 |
| r4 | 3 | 48 |
| r5 | 3 | 51 |
| r6 | 3 | 54 |
| r7 | 2 | 26 |
| r8 | 2 | 28 |
| r9 | 2 | 30 |
| r10 | 2 | 32 |
| r11 | 2 | 34 |
| r12 | 2 | 36 |

Residue pattern for each hexagon:

| Hexagon | Values | Residue pattern | Sum |
|---|---|---|---:|
| Hex1 | [25, 16, 2, 23, 22, 5] | 1-4-2-11-10-5 | 93 |
| Hex2 | [2, 11, 27, 6, 24, 23] | 2-11-3-6-12-11 | 93 |
| Hex3 | [22, 23, 24, 17, 3, 4] | 10-11-12-5-3-4 | 93 |
| Hex4 | [27, 30, 8, 15, 7, 6] | 3-6-8-3-7-6 | 93 |
| Hex5 | [6, 24, 17, 10, 29, 7] | 6-12-5-10-5-7 | 93 |
| Hex6 | [3, 17, 10, 18, 19, 26] | 3-5-10-6-7-2 | 93 |
| Hex7 | [7, 29, 9, 21, 12, 15] | 7-5-9-9-12-3 | 93 |
| Hex8 | [10, 18, 13, 14, 9, 29] | 10-6-1-2-9-5 | 93 |
| Hex9 | [9, 21, 20, 1, 28, 14] | 9-9-8-1-4-2 | 93 |

## 3. mod 2 spatial distribution and symmetry

- Even (r2): 15, odd (r1): 15

- Odd distribution: left 5, right 5, upper half 7, lower half 8

The mod-2 distribution is close to evenly balanced with respect to the vertical and horizontal reflection axes.

## 4. CRT (Chinese Remainder Theorem) analysis

Following the basic CRT algorithm associated with the Song-Yuan mathematician Qin Jiushao,
we combine coprime moduli.

### mod 3 × mod 4 → mod 12

| CRT residue | Count | Sum |
|---|---:|---:|
| r1 | 3 | 39 |
| r2 | 3 | 42 |
| r3 | 3 | 45 |
| r4 | 3 | 48 |
| r5 | 3 | 51 |
| r6 | 3 | 54 |
| r7 | 2 | 26 |
| r8 | 2 | 28 |
| r9 | 2 | 30 |
| r10 | 2 | 32 |
| r11 | 2 | 34 |
| r12 | 2 | 36 |

### mod 3 × mod 5 → mod 15

| CRT residue | Count | Sum |
|---|---:|---:|
| r1 | 2 | 17 |
| r2 | 2 | 19 |
| r3 | 2 | 21 |
| r4 | 2 | 23 |
| r5 | 2 | 25 |
| r6 | 2 | 27 |
| r7 | 2 | 29 |
| r8 | 2 | 31 |
| r9 | 2 | 33 |
| r10 | 2 | 35 |
| r11 | 2 | 37 |
| r12 | 2 | 39 |
| r13 | 2 | 41 |
| r14 | 2 | 43 |
| r15 | 2 | 45 |

### mod 4 × mod 5 → mod 20

| CRT residue | Count | Sum |
|---|---:|---:|
| r1 | 2 | 22 |
| r2 | 2 | 24 |
| r3 | 2 | 26 |
| r4 | 2 | 28 |
| r5 | 2 | 30 |
| r6 | 2 | 32 |
| r7 | 2 | 34 |
| r8 | 2 | 36 |
| r9 | 2 | 38 |
| r10 | 2 | 40 |
| r11 | 1 | 11 |
| r12 | 1 | 12 |
| r13 | 1 | 13 |
| r14 | 1 | 14 |
| r15 | 1 | 15 |
| r16 | 1 | 16 |
| r17 | 1 | 17 |
| r18 | 1 | 18 |
| r19 | 1 | 19 |
| r20 | 1 | 20 |

## 5. 2·3-based mutation scheme

- mod 2: the smallest prime modulus; controls parity and reflection symmetry.
- mod 3: the basic modulus corresponding to the threefold / 9-palace skeleton.
- mod 4 = 2×2: a one-step refinement of mod 2.
- mod 6 = 2×3: combines parity and the threefold structure.
- mod 9 = 3×3: the square of the threefold modulus, matching the 9-palace framework.
- mod 12 = 2²×3: fully recoverable from mod 3 and mod 4 by CRT.

## 6. Extended visualisation interpretations

### Made / Used separation (`jisu_9hex_multiplicity.png`)

- Thirty distinct numbers (作) are placed into fifty-four hexagon positions (用).
- Vertices with higher multiplicity are drawn larger and cluster in the centre.
- The eight multiplicity-3 vertices all lie in or around the central hexagon (Hex5).
- This directly illustrates the original phrase **三十子作， 五十四子用**.

### mod 2 symmetry (`jisu_9hex_mod2_symmetry.png`)

- Exactly 15 odd and 15 even numbers are present.
- Odd nodes are spread fairly evenly with respect to the vertical (x = 0) and horizontal (y = 0) reflection axes.
- By quadrant, odd counts are: Q1 (right/top) 5, Q2 (left/top) 2, Q3 (left/bottom) 3, Q4 (right/bottom) 5.
- The image shows how reflection symmetry of the hexagonal lattice is balanced against the partial-sum invariant.

### 9 palaces → 12 palaces (`jisu_9hex_9to12_palaces.png`)

- Inner blue circles: the nine hexagon palaces (九宫).
- Outer orange circles: twelve directional palace units (十二宫), labelled by the twelve earthly branches.
- Grey lines: mapping from each hexagon centre to adjacent directional sectors.
- This visualises the original phrase **凡九宮化爲十二宮**.

### Central three palaces (`jisu_9hex_center_periphery.png`)

- The vertical central column Hex2, Hex5, Hex8 is highlighted in red.
- These three hexagons form the core axis that governs the six surrounding hexagons.
- This corresponds to the original phrase **中眷三宮， 三宮爲主則**.

### Graph spectrum (`jisu_9hex_adjacency_spectrum.png`)

- The 30×30 adjacency matrix reveals the sparse block pattern created by shared vertices between hexagons.
- Degree distribution: mostly degree-2 and degree-3 vertices, with a few higher-degree central vertices.
- Adjacency eigenvalues reflect the graph symmetry; Laplacian eigenvalues quantify connectivity.

### Magic constant emphasis (`jisu_9hex_magic_constant.png`)

- The magic constant **93** is placed at the centre of every hexagon, together with its six constituent values.
- All nine hexagons visibly sum to 93.
- This is a direct visualisation of the original phrase **六子各得九十三數**.
