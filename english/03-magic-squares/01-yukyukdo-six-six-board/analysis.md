# Yukyukdo (Six-Six Board, 六六圖)

Order: 6×6

Two normal 6×6 magic squares. In both, every row, column and diagonal sums to 111. Rotation and reflection do not carry one to the other, but they share the same construction.

## Construction

Both examples follow the same plan. Divide the 6×6 square into nine 2×2 blocks, and let L be the number of the Lo Shu L = (4 9 2 / 3 5 7 / 8 1 6) at the block's position. Every cell then holds

    v = L + 9k,  k ∈ {0, 1, 2, 3}

so each block contains the four numbers L, L+9, L+18, L+27 once each. The top-left block (L=4), for example, holds 4, 13, 22, 31, and the central block (L=5) holds 5, 14, 23, 32. Each block therefore sums to 4L+54, and the nine block sums 70 90 62 / 66 74 82 / 86 58 78 again follow the Lo Shu arrangement.

The 6×6 array of the k values has every row, column and main diagonal summing to 9. The Lo Shu part contributes 2×15=30 to each line and the k part 9×9=81, so each line sums to 30+81=111.

The two examples use the same four numbers in every block and differ only in how k is placed inside the blocks. Since 6 leaves remainder 2 on division by 4, no associative magic square (in which every two cells symmetric about the centre sum to 37) and no pandiagonal magic square (in which even the broken diagonals sum to 111) exists of this order. Neither example is therefore associative or pandiagonal.

k array of example 1:

```
1 2 1 2 1 2
3 0 3 0 3 0
1 2 1 2 1 2
3 0 0 3 3 0
1 2 1 2 1 2
0 3 3 0 0 3
```

k array of example 2:

```
0 1 3 2 3 0
2 3 1 0 1 2
0 2 2 3 2 0
3 1 0 1 1 3
1 2 2 3 0 1
3 0 1 0 2 3
```

## Example 1
- Value range: 1 ~ 36
- Normal set (consecutive integers): Yes
- Reference magic constant: 111
- Row sums: [111, 111, 111, 111, 111, 111]
- Column sums: [111, 111, 111, 111, 111, 111]
- Diagonal sums: [111, 111]
- Semi-magic: Yes
- Magic square: Yes
- Pan-diagonal: No
- Wrapped diagonal sums: [111, 147, 102, 165, 39, 102, 108, 159, 57, 144, 87, 111]
- Associated: No (center-symmetric sum = 46)
- Bimagic: No
- 180° rotational symmetry: No

## Example 2
- Value range: 1 ~ 36
- Normal set (consecutive integers): Yes
- Reference magic constant: 111
- Row sums: [111, 111, 111, 111, 111, 111]
- Column sums: [111, 111, 111, 111, 111, 111]
- Diagonal sums: [111, 111]
- Semi-magic: Yes
- Magic square: Yes
- Pan-diagonal: No
- Wrapped diagonal sums: [111, 129, 129, 111, 84, 102, 90, 96, 111, 135, 123, 111]
- Associated: No (center-symmetric sum = 37)
- Bimagic: No
- 180° rotational symmetry: No

## Value Frequency Analysis (Example 1)
- Total cells: 36
- Distinct values: 36
- No duplicates
