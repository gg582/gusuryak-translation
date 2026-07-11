# Baekjajasuyin-yang-chakjong (Hundred-Numbers Yin-Yang Intertwining Diagram, 百子子數陰陽錯綜圖)

Order: 10×10

## Normal Magic Square Status

**Not a normal magic square.** This matrix presents two Latin squares. Each has constant row and column sums, but they do not use the numbers 1~100 exactly once, and their diagonal sums do not match the magic constant 505.

A valid 10×10 magic square correction is given separately in [`corrected.md`](corrected.md).

## Generation Rule Summary

Baekjajasuyin-yang-chakjong presents two 10×10 **Latin squares** together. The terms "yin-yang (陰陽)" and "chakjong (錯綜, intertwining)" in the name suggest that the two matrices have a complementary and interlocking structure.

- First matrix: uses the symbols 1, 2, ..., 10
- Second matrix: uses the symbols 0, 1, ..., 9

Both matrices have each of the 10 symbols appearing exactly once in every row and every column, satisfying the definition of a Latin square.

## Example 1: 1~10 Latin Square

```
10  9  8  7  6  5  4  3  2  1
 1 10  9  8  7  6  5  4  3  2
 2  1 10  9  8  7  6  5  4  3
 3  2  1 10  9  8  7  6  5  4
 4  3  2  1 10  9  8  7  6  5
 5  4  3  2  1 10  9  8  7  6
 6  5  4  3  2  1 10  9  8  7
 7  6  5  4  3  2  1 10  9  8
 8  7  6  5  4  3  2  1 10  9
 9  8  7  6  5  4  3  2  1 10
```

- Row sums: [55, 55, 55, 55, 55, 55, 55, 55, 55, 55]
- Column sums: [55, 55, 55, 55, 55, 55, 55, 55, 55, 55]
- Latin square: Yes (each row/column contains 1~10 exactly once)
- This matrix is a **reverse circulant** form.

## Example 2: 0~9 Latin Square

```
0 1 2 3 4 5 6 7 8 9
9 0 1 2 3 4 5 6 7 8
8 9 0 1 2 3 4 5 6 7
7 8 9 0 1 2 3 4 5 6
6 7 8 9 0 1 2 3 4 5
5 6 7 8 9 0 1 2 3 4
4 5 6 7 8 9 0 1 2 3
3 4 5 6 7 8 9 0 1 2
2 3 4 5 6 7 8 9 0 1
1 2 3 4 5 6 7 8 9 0
```

- Row sums: [45, 45, 45, 45, 45, 45, 45, 45, 45, 45]
- Column sums: [45, 45, 45, 45, 45, 45, 45, 45, 45, 45]
- Latin square: Yes (each row/column contains 0~9 exactly once)
- This matrix is a **forward circulant** form.

## Orthogonality Check

When the two Latin squares L1 (1~10) and L2 (0~9) are superimposed, the ordered pairs (L1[i,j], L2[i,j]) obtained from the 100 cells contain only 10 distinct pairs.

```
(10,0), (9,1), (8,2), (7,3), (6,4), (5,5), (4,6), (3,7), (2,8), (1,9)
```

Each ordered pair appears exactly 10 times. Therefore, the two Latin squares are **not orthogonal**.

If they were orthogonal Latin squares, all 100 ordered pairs would be distinct. Here only 10 ordered pairs appear, so the two matrices are a "complementary pair" but not orthogonal.

## Attempting to Combine into a Magic Square

Combining the two matrices in the form 10×L1 + L2 gives:

- Value range: 19 ~ 100
- Row sums: 595 (all rows equal)
- Column sums: 595 (all columns equal)
- But the diagonal sums are 1000 and 550, which differ
- The set of values is not 1~100

Thus a simple combination does not produce a magic square, because the two Latin squares are not orthogonal.

## Meaning of the "Yin-Yang" Structure

Examples 1 and 2 have the following complementary relationship:
- Each row of Example 1 is the reverse cycle 10, 9, ..., 1.
- Each row of Example 2 is the forward cycle 0, 1, ..., 9.
- At the same position, L1[i,j] + L2[i,j] = 10 (e.g., 10+0, 9+1, ..., 1+9).

Thus the two matrices form a "yin-yang pair" that maintains a constant positional sum of 10. This corresponds to the "eum-yang-chakjong" in the name.

## Mathematical Classification

| Property | Example 1 | Example 2 |
|---|---|---|
| Latin square | Yes | Yes |
| Circulant | Reverse circulant | Forward circulant |
| Orthogonal | No | No |
| Magic square | No | No |
| Constant row/column sum | Yes (55) | Yes (45) |

## Note

These two Latin squares are not candidates for producing a 10×10 magic square by orthogonal Latin squares. However, they are an interesting structure that visualizes the concept of "yin-yang" through the complementary pair of 1~10 and 0~9.
