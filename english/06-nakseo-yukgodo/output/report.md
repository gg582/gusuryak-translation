# Nakseo Yukgodo (洛書六觚圖) reconstructed optimum — property analysis

## 1. Search result summary

- seed: 1715, restarts: 24, iterations per restart: 300,000
- restart penalties: [6.0]
- final penalty: **6.0** (theoretical floor 6.0)
- penalty breakdown: {'sides': 0, 'wedges': 3.0, 'rays': 3.0, 'pairs': 0, 'rings': 0, 'axes': 0}

## 2. Cross-check against the commentary OCR

| Commentary phrase | Meaning | Check in the reconstructed diagram |
|---|---|---|
| 共積二百七十 | 270 cells are filled | 270 cells (center excluded by 虛一) |
| 虛一則二百七十數 | voiding the one leaves 270 numbers | center cell unused |
| 校計周五十四數 | counting the perimeter gives 54 | outermost ring has 54 cells |
| 通加洛書數六倍 | six times the Luoshu number (1+..+9=45) = 270 | total cells = 6×45 |
| 十九爲中觚數也 | the central row has 19 | 中觚 (row through the center) has 19 cells |
| 置外周添六 | proceeds around the outer ring adding six | ring k has 6k cells (6,12,...,54) |
| 之數見甲編數器章 | provenance note for the numbers | values 1..270 (籌數略 system) |

## 3. Basic validation

- filled cells: 270 (target 270)
- grand total: 36585 (target 36585)
- all antipodal pairs (sum 271) hold: True (135 pairs)

## 4. Sums by structure

### Rings (通加洛書數六倍)

| ring k | cells 6k | sum | target 813k | met |
|---|---|---|---|---|
| 1 | 6 | 813 | 813 | ✓ |
| 2 | 12 | 1626 | 1626 | ✓ |
| 3 | 18 | 2439 | 2439 | ✓ |
| 4 | 24 | 3252 | 3252 | ✓ |
| 5 | 30 | 4065 | 4065 | ✓ |
| 6 | 36 | 4878 | 4878 | ✓ |
| 7 | 42 | 5691 | 5691 | ✓ |
| 8 | 48 | 6504 | 6504 | ✓ |
| 9 | 54 | 7317 | 7317 | ✓ |

### Six perimeter sides (target 1355 each)

- measured: [1355, 1355, 1355, 1355, 1355, 1355]

### Six gu-sectors (觚) (target 6097.5 each, ideal distribution 6097/6098)

- measured: [6097, 6098, 6098, 6098, 6097, 6097]

### Six rays (target 1219.5 each, ideal distribution 1219/1220)

- measured: [1219, 1220, 1219, 1220, 1219, 1220]

### Three axes / 中觚 (target 2439 each)

- measured axis sums: [2439, 2439, 2439]
- 中觚 (direction 0): 19 cells, sum 2439
- 中觚 (direction 1): 19 cells, sum 2439
- 中觚 (direction 2): 19 cells, sum 2439

## 5. Corner values (for Luoshu cross-check)

- values: [206, 126, 245, 65, 145, 26]
- mod 9: [8, 0, 2, 2, 1, 8]
- mod 6: [2, 0, 5, 5, 1, 2]

## 6. Perimeter traversal sequence (for algorithm-pattern review)

- 54 values: [145, 216, 197, 44, 148, 81, 53, 256, 189, 26, 127, 268, 120, 20, 210, 244, 85, 49, 206, 93, 129, 188, 103, 70, 71, 166, 203, 126, 55, 74, 227, 123, 190, 218, 15, 82, 245, 144, 3, 151, 251, 61, 27, 186, 222, 65, 178, 142, 83, 168, 201, 200, 105, 68]
- adjacent differences (clockwise, mod 270): [71, 251, 117, 104, 203, 242, 203, 203, 107, 101, 141, 122, 170, 190, 34, 111, 234, 157, 157, 36, 59, 185, 237, 1, 95, 37, 193, 199, 19, 153, 166, 67, 28, 67, 67, 163, 169, 129, 148, 100, 80, 236, 159, 36, 113, 113, 234, 211, 85, 33, 269, 175, 233, 77]

## 7. Interpretation notes

- This placement is a **search optimum** under the 虛一 + antipodal
  complementary-pair (sum 271) hypothesis; it does not replay the commentary's
  seungjeokbeop procedure but reverse-engineers a placement satisfying its numeric conditions.
- Ring sums 813k, axis sums 2439, and pair sums 271 are structural consequences of the
  hypothesis; side 1355, sector 6097/6098, and ray 1219/1220 balances are search-only goals.
