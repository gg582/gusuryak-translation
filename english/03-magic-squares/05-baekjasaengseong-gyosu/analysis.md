# Baekjasaengseong-gyosu (Hundred-Numbers Crossed-Numbers Diagram, 百子生成交數圖)

Order: 10×10

## Normal Magic Square Status

**Not a normal magic square.** The value set is not the consecutive integers 1~100, and the row, column, and diagonal sums do not match the magic constant 505.

A valid 10×10 magic square correction is given separately in [`corrected.md`](corrected.md).

## Generation Rule Summary

Baekjasaengseong-gyosu is a 10×10 matrix that pairs with Baekjasaengseong-sunsu. The term "gyosu (交數, crossed numbers)" indicates that the numbers are arranged in a mutually crossing or exchanged form. This matrix is also not a normal magic square and is thought to be a structure made by superimposing two 10th-order Latin squares.

## Matrix

```
46 55 64 73 82 91 100 19 28 37
 7 94 53 62 71 85  16 20 39 48
18 83 92 51 65 74  27 36 40  9
29 72 81 95 54 63  38 47  6 10
30 61 75 84 93 52  59  8 17 26
61 30 26 17  8 49  42 93 84 75
72 29 10  6 47 38  63 54 95 81
83 18  9 40 36 27  74 65 51 92
94  7 48 39 20 16  85 71 62 53
55 46 37 28 19 100 91 82 73 64
```

## Basic Numerical Data

- Value range: 6 ~ 100
- Normal set (consecutive 1~100): No
- Number of distinct values: 52 (out of 100 cells)
- Some duplicated values: most values appear twice
- Magic constant (for a normal 10×10): 505
- Actual row sums: [595, 495, 495, 495, 505, 485, 495, 495, 495, 595]
- Actual column sums: [495, 495, 495, 495, 495, 595, 595, 495, 495, 495]
- Diagonal sums: [723, 287]
- Semi-magic: No
- Magic square: No
- Pan-diagonal: No
- Associated: No
- Bimagic: No

## Why Is It Not a Magic Square?

1. **Value set mismatch**: It does not use each of the consecutive integers 1~100 exactly once. The numbers 1~5 are missing, and some values are duplicated.
2. **Row/column sum mismatch**: Not all row and column sums equal 505. In particular, rows 1 and 10 and columns 6 and 7 jump to 595.
3. **Diagonal sum mismatch**: The diagonals are 723 and 287, a large difference.

## Relationship to Sunsu

Baekjasaengseong-gyosu shares a similar generation principle with Baekjasaengseong-sunsu, but the arrangement of numbers is crossed. Comparing the two matrices:
- Sunsu: the reverse-order complementary pair structure is prominent.
- Gyosu: the top-bottom complementary pairs appear to have been exchanged.

For example, rows 1 and 10 of Gyosu:
- Row 1: 46 55 64 73 82 91 100 19 28 37
- Row 10: 55 46 37 28 19 100 91 82 73 64

These two rows are reverse-order pairs while also having their first and second halves exchanged. This is the meaning of "gyosu."

## Latin Square Interpretation

Like Baekjasaengseong-sunsu, Gyosu also appears to be a combination of two Latin square components rather than a single Latin square. Adding or combining the two matrices can produce values in the range 1~100, but they do not satisfy the conditions for orthogonal Latin squares.

## Top-Bottom Symmetry Observation

The upper half (rows 1~5) and lower half (rows 6~10) of the matrix show the following relationship:
- A number in an upper row is changed to a different number at the corresponding lower position.
- The same number is maintained at some specific positions.

This is evidence of a generation rule in which top-bottom pairs are crossed or exchanged, as suggested by the name "gyosu."

## Conclusion

Baekjasaengseong-gyosu is not a normal magic square, but together with Baekjasaengseong-sunsu it forms an important pair for understanding Choi Seok-jeong's study of 10th-order Latin squares. The name "gyosu" reflects a structure in which the two components are arranged in a mutually crossing manner.
