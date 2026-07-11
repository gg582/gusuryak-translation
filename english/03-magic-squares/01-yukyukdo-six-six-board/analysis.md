# Yukyukdo (Six-Six Board, 六六圖)

Order: 6×6

## Normal Magic Square Status

Yukyukdo is a **normal magic square**. It uses each of the natural numbers 1 through 36 exactly once, and every row, column, and both main diagonals sum to the magic constant 111.

However, it is **not an associated magic square**. Moreover, order 6 is **singly even** (\(6 \equiv 2 \pmod 4\)), so a 6×6 associated magic square is mathematically impossible. Therefore Yukyukdo cannot be "corrected" to associated. The original square is already a valid magic square; it simply is not associated.

## Generation Rule Summary

The magic constant is

\[
M_6 = \frac{6(6^2+1)}{2} = 111
\]

and both examples have all rows, columns, and both main diagonals summing to 111.

A 6×6 square is **singly even** (\(n \equiv 2 \pmod 4\)), so its construction rule is more complicated than for odd orders or doubly even (multiples of 4) orders. It is also the smallest non-trivial magic square.

## Example 1

```
13 22 18 27 11 20
31  4 36  9 29  2
12 21 14 23 16 25
30  3  5 32 34  7
17 26 10 19 15 24
 8 35 28  1  6 33
```

- Value range: 1 ~ 36
- Normal set (consecutive integers): Yes
- Magic constant: 111
- Row sums: [111, 111, 111, 111, 111, 111]
- Column sums: [111, 111, 111, 111, 111, 111]
- Diagonal sums: [111, 111]
- Semi-magic: Yes
- Magic square: Yes
- Pan-diagonal: No
- Wrapped diagonal sums: [111, 147, 102, 165, 39, 102, 108, 159, 57, 144, 87, 111]
- Associated: No (min/max center-symmetric sum = 19 / 55)
- Complementary pairs summing to 37 (=n²+1): 0
- Bimagic: No
- 180° rotational symmetry: No

### 3×3 Block Structure

Dividing the 6×6 square into four 3×3 blocks, the diagonal blocks (top-left, bottom-right) each sum to 171, while the off-diagonal blocks (top-right, bottom-left) each sum to 162.

```
[13 22 18 | 27 11 20]       171 | 162
[31  4 36 |  9 29  2]  =>   ----+----
[12 21 14 | 23 16 25]       162 | 171
---------+----------
[30  3  5 | 32 34  7]       162 | 171
[17 26 10 | 19 15 24]  =>   ----+----
[ 8 35 28 |  1  6 33]       171 | 162
```

This pattern is a general property of 6×6 magic squares. The corresponding rows (or columns) of each 3×3 block pair up so that their sums equal the magic constant 111.

### 2×3 and 3×2 Block Sums

- 2×3 block sums: 124 / 98 / 85 / 137 / 124 / 98
- 3×2 block sums: 103 / 127 / 103 / 119 / 95 / 119

The 2×3 blocks have integer sums rather than half the magic constant (55.5), which is possible because a 6×6 square can be tiled by 2×3 rectangles.

## Example 2

```
 4 13 36 27 29  2
22 31 18  9 11 20
 3 21 23 32 25  7
30 12  5 14 16 34
17 26 19 28  6 15
35  8 10  1 24 33
```

- Value range: 1 ~ 36
- Normal set (consecutive integers): Yes
- Magic constant: 111
- Row sums: [111, 111, 111, 111, 111, 111]
- Column sums: [111, 111, 111, 111, 111, 111]
- Diagonal sums: [111, 111]
- Semi-magic: Yes
- Magic square: Yes
- Pan-diagonal: No
- Wrapped diagonal sums: [111, 129, 129, 111, 84, 102, 90, 96, 111, 135, 123, 111]
- Associated: No (min/max center-symmetric sum = 28 / 46)
- Complementary pairs summing to 37: 32 / 36 (almost associated)
- Bimagic: No
- 180° rotational symmetry: No

### Example 2 Peculiarity: "Almost Associated"

In Example 2, most centrally symmetric pairs sum to 37 (=6²+1). For a normal 6×6 associated magic square, all 18 pairs would have to sum to 37, but Example 2 has only 32 such pairs; the remaining four pairs sum to 28 or 46.

```
Pairs that are not 37:
  (1,2): 18 + 28 = 46
  (1,3):  9 + 19 = 28
  (4,2): 19 +  9 = 28
  (4,3): 28 + 18 = 46
```

These four pairs form the 2×2 submatrix
```
18  9
19 28
```
and its centrally symmetric counterpart
```
28 19
 9 18
```
Only this region breaks the complementary relationship. In other words, Example 2 is close to an associated structure overall, but looks as if a single 2×2 region has been swapped.

### 3×3 Block Structure

Example 2 also has diagonal 3×3 block sums equal to 171 and off-diagonal block sums equal to 162, just like Example 1.

## Relationship Between the Two Examples

The two examples are different magic squares. They are not obtained from each other by simple rotation or reflection; they are different arrangements of the numbers 1~36 at the same order.

Looking at the movement pattern, the two examples share the following features:
- Some numbers, such as 1, 5, 9, 14, 17, 21, 27, 30, and 33, remain in the same positions.
- The remaining numbers have been rearranged within rows and columns.

Example 1 is a typical 6×6 magic square with no associated structure, while Example 2 is a variant that is very close to associated.

## Mathematical Classification

| Property | Example 1 | Example 2 |
|---|---|---|
| Normal magic square | Yes | Yes |
| Magic constant | 111 | 111 |
| Associated | No | Almost (32/36) |
| Pan-diagonal | No | No |
| Bimagic | No | No |
| 180° rotational symmetry | No | No |

## Note

The total number of normal 6×6 magic squares is known to be 177,147,6. Therefore the two Yukyukdo examples can be regarded as two different samples from this huge set.
