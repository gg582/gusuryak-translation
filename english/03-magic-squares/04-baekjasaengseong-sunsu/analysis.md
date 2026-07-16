# Baekjasaengseong-sunsu (Hundred-Numbers Pure-Generation Diagram, 百子生成純數圖)

Order: 10×10

10×10 number arrangement. This example is not a normal 1-through-100 set, and its row, column, and diagonal sums are not all 505. Some rows and columns retain symmetric relationships, but the verification does not classify it as a magic square or an associated magic square.

## Example 1
- Value range: 1 ~ 99
- Normal set (consecutive integers): No
- Reference magic constant: 505
- Row sums: [495, 474, 485, 495, 495, 477, 495, 495, 495, 495]
- Column sums: [477, 504, 465, 495, 495, 495, 495, 495, 485, 495]
- Diagonal sums: [709, 210]
- Semi-magic: No
- Magic square: No
- Pan-diagonal: No
- Wrapped diagonal sums: [709, 662, 519, 436, 263, 412, 253, 436, 519, 692, 288, 491, 563, 717, 560, 729, 554, 491, 298, 210]
- Associated: No (center-symmetric sum = 180)
- Bimagic: No
- 180° rotational symmetry: No

## Source and Correction Note

The original array fails the normal `1..100` set check, and its line sums also
fail the stated magic-square conditions. Considering the source properties
together with differences between printed editions, the discrepancy is most
consistent with a publication error or a copying error by a proofreader. The
original array is retained as transcription evidence; `corrected.md` provides a
separate arrangement satisfying the normal-set and line-sum conditions.

## Value Frequency Analysis (Example 1)
- Total cells: 100
- Distinct values: 51
- Duplicated values: {90: 2, 89: 2, 78: 2, 67: 2, 56: 2, 45: 2, 34: 2, 23: 2, 12: 2, 1: 2, 86: 2, 79: 3, 58: 2, 97: 2, 4: 2, 43: 2, 32: 2, 21: 2, 15: 2, 77: 2, 66: 2, 50: 2, 99: 2, 88: 2, 13: 2, 2: 2, 41: 2, 25: 3, 24: 3, 68: 2, 57: 2, 96: 2, 80: 2, 22: 2, 11: 2, 5: 2, 44: 2, 33: 2, 59: 2, 98: 2, 87: 2, 76: 2, 60: 2, 31: 2, 14: 2, 3: 2}
