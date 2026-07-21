# Baekjajasuyin-yang-chakjong (百子子數陰陽錯綜圖) Latin Composition Benchmark Report

## Executive Summary
This report analyzes the decimal composition of Parent ($0 \sim 9$, sum $45$) and Child ($1 \sim 10$, sum $55$) Latin squares to generate a 10x10 magic square with magic constant $505$.

## Key Findings & Matrix Properties

1. **Spectral Convergence to Magic Constant ($505.0$)**
   - The matrix spectral radius converges to **$505.0$**, matching the row and column magic sums.

2. **Latin Composition Invariant**
   - Matrix entries $M_{i,j} = 10 \cdot P_{i,j} + C_{i,j}$ yield exact row/column sums: $10 \times 45 + 55 = 505$.

3. **D8 Isomorphism Solution Classes**
   - Classification under D8 symmetry yields 2 non-isomorphic solution families (circulant Latin square composition vs corrected original magic square).

![Baekjajasuyin Latin Matrix](baekjajasuyin_latin_matrix.png)

## Execution Metrics
- **Non-Isomorphic Solutions Count:** 2
- **Spectral Radius:** `[505.0000]`
- **Graph Betweenness Centrality:** `[0.1270, 0.1270, 0.1270]`
