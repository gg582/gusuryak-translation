# Baekjasaengseong-gyosu (Hundred-Numbers Crossed-Numbers Diagram, 百子生成交數圖)

Order: 10×10

10×10 number arrangement. This example is not a normal 1-through-100 set, and its row, column, and diagonal sums are not all 505. It resembles Baekjasaengseong-sunsu but has a different character. The positions of each pair appear crossed or exchanged, as the name 'gyosu (crossed numbers)' suggests. The verification does not classify it as a magic square or an associated magic square.

## Example 1
- Value range: 6 ~ 100
- Normal set (consecutive integers): No
- Reference magic constant: 505
- Row sums: [595, 495, 495, 495, 505, 485, 495, 495, 495, 595]
- Column sums: [495, 495, 495, 495, 495, 595, 595, 495, 495, 495]
- Diagonal sums: [723, 287]
- Semi-magic: No
- Magic square: No
- Pan-diagonal: No
- Wrapped diagonal sums: [723, 520, 733, 556, 499, 332, 400, 332, 499, 556, 470, 277, 434, 511, 758, 710, 758, 511, 434, 287]
- Associated: No (center-symmetric sum = 110)
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
- Distinct values: 52
- Duplicated values: {46: 2, 55: 2, 64: 2, 73: 2, 82: 2, 91: 2, 100: 2, 19: 2, 28: 2, 37: 2, 7: 2, 94: 2, 53: 2, 62: 2, 71: 2, 85: 2, 16: 2, 20: 2, 39: 2, 48: 2, 18: 2, 83: 2, 92: 2, 51: 2, 65: 2, 74: 2, 27: 2, 36: 2, 40: 2, 9: 2, 29: 2, 72: 2, 81: 2, 95: 2, 54: 2, 63: 2, 38: 2, 47: 2, 6: 2, 10: 2, 30: 2, 61: 2, 75: 2, 84: 2, 93: 2, 8: 2, 17: 2, 26: 2}
