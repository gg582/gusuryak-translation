# Baekjado (Hundred Sons Diagram / 百子圖)

Order: 10×10

[Corrected version] This page records the 10×10 Baekjado in the *Gusuryak* transcription alongside a corrected arrangement. The correction uses every integer from 1 through 100 once and makes every row and column sum to 505. Its two main diagonals sum to 490 and 520, so it is a normal semi-magic square rather than a complete magic square.

## Example (Reconstructed Version)
- Value Range: 1 ~ 100
- Valid Consecutive Set: Yes
- Magic Constant: 505
- Row Sums: [505, 505, 505, 505, 505, 505, 505, 505, 505, 505]
- Column Sums: [505, 505, 505, 505, 505, 505, 505, 505, 505, 505]
- Diagonal Sums: [490, 520]
- Semi-magic: Yes
- Magic square: No
- Pan-diagonal: No
- Wrapped Diagonal Sums: [490, 560, 565, 412, 562, 360, 491, 560, 490, 560, 450, 520, 450, 519, 650, 448, 598, 445, 450, 520]
- Associated: No (central symmetry sum = 11)
- Bimagic: No
- 180° Rotational Symmetry: No

## Value Frequency Analysis (Reconstructed Version)
- Total Cells: 100
- Unique Values: 100
- No Duplicates

## Differences between the source array and the correction

- **Changed cells**: 14

| Coordinates (Row, Col) | Original Manuscript Value | Reconstructed Value | Numerical Error (Reconstructed - Original) |
| :---: | :---: | :---: | :---: |
| (Row 5, Col 1) | 5 | 96 | +91 |
| (Row 5, Col 2) | 16 | 86 | +70 |
| (Row 5, Col 3) | 25 | 75 | +50 |
| (Row 5, Col 8) | 76 | 26 | -50 |
| (Row 5, Col 9) | 85 | 15 | -70 |
| (Row 6, Col 1) | 95 | 6 | -89 |
| (Row 6, Col 2) | 86 | 16 | -70 |
| (Row 6, Col 3) | 75 | 25 | -50 |
| (Row 6, Col 8) | 26 | 76 | +50 |
| (Row 6, Col 9) | 15 | 85 | +70 |
| (Row 7, Col 1) | 14 | 87 | +73 |
| (Row 7, Col 10) | 87 | 14 | -73 |
| (Row 8, Col 1) | 88 | 13 | -75 |
| (Row 8, Col 10) | 13 | 88 | +75 |

Every row and column of the corrected array sums to 505. Since the main
diagonals sum to 490 and 520, this property does not make Baekjado a complete
order-ten magic square.
