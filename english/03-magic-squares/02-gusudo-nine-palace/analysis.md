# Gusudo (Nine Palace, 九數圖)

Order: 9×9

## Normal Magic Square Status

Gusudo is a **normal magic square**. It uses each of the natural numbers 1 through 81 exactly once, and every row, column, and both main diagonals sum to the magic constant 369. No correction is needed; the original is already a valid magic square.

## Generation Rule Summary

The magic constant is

\[
M_9 = \frac{9(9^2+1)}{2} = 369
\]

and both examples have all rows, columns, and both main diagonals summing to 369.

A 9×9 square is of odd order, so it can be constructed by a variant of the traditional Siamese method (continuous placement), or, as Choi Seok-jeong used, by combining **orthogonal Latin squares**. The structure of Gusudo is closely related to the construction of a 9th-order magic square using orthogonal Latin squares.

## Example 1

```
31 76 13 36 81 18 29 74 11
22 40 58 27 45 63 20 38 56
67  4 49 72  9 54 65  2 47
30 75 12 32 77 14 34 79 16
21 39 57 23 41 59 25 43 61
66  3 48 68  5 50 70  7 52
35 80 17 28 73 10 33 78 15
26 44 62 19 37 55 24 42 60
71  8 53 64  1 46 69  6 51
```

- Value range: 1 ~ 81
- Normal set (consecutive integers): Yes
- Magic constant: 369
- Row sums: [369, 369, 369, 369, 369, 369, 369, 369, 369]
- Column sums: [369, 369, 369, 369, 369, 369, 369, 369, 369]
- Diagonal sums: [369, 369]
- Semi-magic: Yes
- Magic square: Yes
- Pan-diagonal: No
- Wrapped diagonal sums: [369, 621, 144, 396, 621, 117, 342, 594, 117, 285, 444, 360, 285, 453, 378, 294, 453, 369]
- Associated: Yes (center-symmetric sum = 82 = 9²+1)
- Bimagic: No
- 180° rotational symmetry: No

### Associated Property

In Example 1, the two cells in every centrally symmetric position sum to 82. This matches the definition of an associated magic square for a normal 9×9 magic square.

\[
a_{i,j} + a_{8-i,8-j} = 82
\]

## Example 2

```
50 18 55 70  5 48  3 76 44
66 31 26 29 81 13 52 11 60
 7 74 42 24 37 62 68 36 19
54 67  2 65 25 33 28 23 72
59 21 43  9 41 73 15 61 47
10 35 78 49 57 17 80 39  4
79  6 38 20 69 34 32 64 27
30 71 22 45  1 77 16 51 56
14 46 63 58 53 12 75  8 40
```

- Value range: 1 ~ 81
- Normal set (consecutive integers): Yes
- Magic constant: 369
- Row sums: [369, 369, 369, 369, 369, 369, 369, 369, 369]
- Column sums: [369, 369, 369, 369, 369, 369, 369, 369, 369]
- Diagonal sums: [369, 369]
- Semi-magic: Yes
- Magic square: Yes
- Pan-diagonal: No
- Wrapped diagonal sums: [369, 380, 311, 519, 252, 438, 219, 523, 310, 392, 335, 399, 472, 298, 339, 339, 378, 369]
- Associated: No (min/max center-symmetric sum = ? / ?)
- Bimagic: No
- 180° rotational symmetry: No

### Correcting Example 2 to Associated

To make Example 2 an associated magic square, the numbers would have to be rearranged so that **every centrally symmetric pair sums to 82**. In other words, for each number \(x\), the cell centrally symmetric to it must contain \(82 - x\).

In Example 2, the center value 41 is already at the exact center \((4,4)\), satisfying a necessary condition for associated squares, but the remaining 40 complementary pairs are not placed as centrally symmetric pairs. In fact, the center-symmetric sums of Example 2 are scattered from 26 to 138. For example:

```
(0,0)=50 <-> (8,8)=40: sum=90  (not 82)
(0,1)=18 <-> (8,7)= 8: sum=26  (not 82)
(0,2)=55 <-> (8,6)=75: sum=130 (not 82)
```

Therefore, turning Example 2 into an associated square would require not just swapping a few numbers, but **rearranging all 40 complementary pairs into centrally symmetric positions**. This is essentially equivalent to designing a new 9×9 associated magic square.

An example of an associated 9×9 magic square is given in [`corrected_associated.md`](corrected_associated.md) and in the visualization file `gusudo_associated_correction.png`. This correction has every row, column, and both main diagonals summing to 369, and every centrally symmetric pair summing to 82.

### Relationship Between the Two Examples

Example 2 is also a normal 9×9 magic square, but it differs from Example 1 in the associated property: Example 1 is associated, while Example 2 is not.

Checking whether the two examples are connected by any basic transformation (row permutation, column permutation, reversal, rotation) would clarify how Example 2 relates to Example 1. Visually, the two examples show different arrangement patterns and are not obtained from each other by simple reversal or rotation.

## 3×3 Block Structure

Dividing a 9×9 magic square into nine 3×3 blocks, the block sums are not uniform, but they have a structure related to the magic constant 369. In odd-order magic squares, 3×3 blocks have different properties than in even-order squares.

## Mathematical Classification

| Property | Example 1 | Example 2 |
|---|---|---|
| Normal magic square | Yes | Yes |
| Magic constant | 369 | 369 |
| Associated | Yes | No |
| Pan-diagonal | No | No |
| Bimagic | No | No |

## Historical Context

Choi Seok-jeong (1646–1715) constructed the 9×9 magic square in *Gusuryak* using orthogonal Latin squares. This attempt is evaluated as having preceded Leonhard Euler by about 60 years. The structure of Gusudo appears to have been generated by summing (or combining) orthogonal Latin squares.
