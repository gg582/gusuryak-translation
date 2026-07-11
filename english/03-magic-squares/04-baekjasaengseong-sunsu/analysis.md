# Baekjasaengseong-sunsu (Hundred-Numbers Pure-Generation Diagram, 百子生成純數圖)

Order: 10×10

## Normal Magic Square Status

**Not a normal magic square.** The value set is not the consecutive integers 1~100, and the row, column, and diagonal sums do not match the magic constant 505. The paper explicitly states that it is "not an orthogonal Latin square."

A valid 10×10 magic square correction is given separately in [`corrected.md`](corrected.md).

## Generation Rule Summary

Baekjasaengseong-sunsu looks like a "hundred-numbers (1~100)" magic square, as its name suggests, but it is **not a normal magic square**. This matrix is thought to be a structure made by superimposing two 10th-order Latin squares, and the academic paper explicitly states that it is "not an orthogonal Latin square."

> "Combining these, they constructed the Baekjasaengseong-sunsu (百子生成純數圖) and Baekjasaengseong-gyosu (百子生成交數圖) as pairs, but these are not orthogonal Latin squares."  
> — Kim Sung-sook, Kang Mi-kyung, "Choi Seok-jeong's Orthogonal Latin Squares"

In addition, a Dong-A Science article pointed out that one of the 10th-order Latin squares contained in Baekjasaengseong-sunsu is **isomorphic to the addition table of the Abelian group Z₂×Z₅** under a specific correspondence rule.

## Matrix

```
90 89 78 67 56 45 34 23 12  1
86 79 39 58 97  4 43 32 21 15
77 66 50 99 88 13  2 41 25 24
68 57 96 80 79 22 11  5 44 33
59 98 87 76 60 31 25 14  3 42
24  3 14 25 31 60 76 87 98 59
33 44  5 11 22 79 80 96 57 68
24 35 41  2 13 88 99 50 66 77
15 21 32 43  4 97 58 69 70 86
 1 12 23 34 45 56 67 78 89 90
```

## Basic Numerical Data

- Value range: 1 ~ 99
- Normal set (consecutive 1~100): No
- Number of distinct values: 51 (out of 100 cells)
- Some duplicated values: 24, 25, 79 appear 3 times each; 35, 39, 42, 69, 70 appear once each, etc.
- Magic constant (for a normal 10×10): 505
- Actual row sums: [495, 474, 485, 495, 495, 477, 495, 495, 495, 495]
- Actual column sums: [477, 504, 465, 495, 495, 495, 495, 495, 485, 495]
- Diagonal sums: [709, 210]
- Semi-magic: No
- Magic square: No
- Pan-diagonal: No
- Associated: No
- Bimagic: No

## Why Is It Not a Magic Square?

1. **Value set mismatch**: It does not use each of the consecutive integers 1~100 exactly once.
2. **Row/column sum mismatch**: Not all row and column sums equal the magic constant 505.
3. **Diagonal sum mismatch**: The two main diagonals sum to 709 and 210, which are very different.

Therefore this matrix does not satisfy the definition of a magic square.

## Latin Square Interpretation

If the 51 distinct values appearing in this matrix are viewed simply as symbols, a Latin square would require each symbol to appear exactly 10 times. However, the actual frequencies are uneven, ranging from 1 to 3.

This suggests that Baekjasaengseong-sunsu is **not a single Latin square but the superposition of two 10th-order Latin squares**. That is, each entry of the matrix may be of the form

\[
S_{i,j} = f(A_{i,j}, B_{i,j})
\]

where A and B are Latin squares. In this case A and B may each be Latin squares, but S is not.

## Connection to the Abelian Group Z₂×Z₅

According to the Dong-A Science article, if one Latin square contained in Baekjasaengseong-sunsu is converted to the symbols 0~9 by a specific correspondence rule, it becomes the same as the **addition table of Z₂×Z₅**.

Z₂×Z₅ is the Abelian group with 10 elements

\[
\{(0,0),(0,1),(0,2),(0,3),(0,4),(1,0),(1,1),(1,2),(1,3),(1,4)\}
\]

and addition is performed componentwise modulo 2 and modulo 5. The claim is that the Cayley table (addition table) of this group, represented as a 10×10 Latin square, is isomorphic to one component of Baekjasaengseong-sunsu.

## Top-Bottom Symmetry Observation

Comparing the first five rows and the last five rows of the matrix reveals the following complementary relationship:
- Row 1: 90 89 78 67 56 45 34 23 12 1
- Row 10: 1 12 23 34 45 56 67 78 89 90

These two rows are reverses of each other. Similarly, other row pairs also show partial reverse/complementary relationships. This is evidence that the matrix was generated through top-bottom pairs, as suggested by the name "saengseong (生成, generation)."

## Conclusion

Baekjasaengseong-sunsu is not a magic square in the traditional sense, but rather a structure combining two 10th-order Latin squares (or their variants). Although it is not an orthogonal Latin square, the fact that one of its components is isomorphic to the addition table of the Abelian group Z₂×Z₅ makes it an interesting case connected to modern algebra.
