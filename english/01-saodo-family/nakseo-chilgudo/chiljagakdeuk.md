# Reading Nakseo Chilgudo as Chiljagakdeuk (Seven-Each-Gets)

`Nakseo Chilgudo (洛書七九圖)` places seven numbers in each of nine palaces.  
In modern terms this is a **Chiljagakdeuk (七子各得)** structure: nine palaces, each receiving seven numbers, all sharing the same sum.

Below we separate the reading into a **Gakdeuk (Each-Gets)** interpretation and a **Saodo (Four/Five Way)** interpretation.  
The data files also contain some transcription errors; we point these out and give a corrected reconstruction.

---

## 1. Observed structure

Nakseo Chilgudo arranges nine palaces on a 3×3 grid.  
The center of each palace holds one of the numbers 1 through 9 in the following pattern.

```text
4  9  2
3  5  7
8  1  6
```

This is exactly the classical **Luoshu nine-palace magic square**; every row, column, and diagonal sums to 15.

Each palace has six additional surrounding numbers, for a total of seven numbers per palace.

| Palace | Center | Six surrounding numbers | Sum |
|---|---|---|---:|
| Upper-left | 4 | 31, 43, 22, 60, 27, 37 | 224 |
| Upper-center | 9 | 15, 43, 38, 55, 10, 54 | 224 |
| Upper-right | 2 | 28, 29, 39, 62, 17, 47 | 224 |
| Middle-left | 3 | 30, 40, 26, 61, 16, 48 | 224 |
| Center | 5 | 32, 41, 23, 59, 14, 50 | 224 |
| Middle-right | 7 | 34, 38, 24, 57, 20, 44 | 224 |
| Lower-left | 8 | 35, 49, 12, 56, 11, 53 | 224 |
| Lower-center | 1 | 52, 25, 19, 63, 18, 46 | 224 |
| Lower-right | 6 | 33, 42, 21, 36, 13, 23 | **174** |

Eight palaces sum to **224**; the last palace (center 6) sums to **174**.

---

## 2. Basic numbers and data errors

The sum of the integers 1 through 63 is

```
63 × 64 / 2 = 2016
```

If the nine palaces use each integer from 1 to 63 exactly once, then each palace must sum to

```
2016 / 9 = 224
```

So the intended invariant is **“every palace receives 224.”**

### Problems in the current data

- Total positions: 9 × 7 = **63**
- Distinct values actually used: **60**
- Duplicated values: **23, 38, 43** (each appears twice)
- Missing values: **45, 51, 58**
- Overlap-weighted total of the nine palaces: **1966** (= 2016 − 50)

Thus the data in `pattern.png`, `pattern_corrected.png`, and `visualize_basic.py` is a corrupted version of the original diagram.  
The script comment says that the missing slot was filled with 36, but 36 is already present in the unique set, while 45, 51, and 58 are absent.

---

## 3. The make/use distinction

If the diagram were complete, the make/use split would be:

| Quantity | Value |
|---|---:|
| Numbers written (作) | 63 (1 through 63, each once) |
| Positions used (用) | 63 (9 palaces × 7 numbers) |
| Duplicate positions | 0 |
| Plain sum of written numbers | 2016 |
| Repeated palace-total sum | 2016 |
| Extra from duplication, D | 0 |

Nakseo Chilgudo is therefore a **partition with no overlap**.  
Unlike Nakseo Sagudo (20 made / 36 used), Nakseo Ogudo (33 made / 45 used), and Jisu-yong-yukdo (20 made / 30 used), here the make-count and use-count coincide.

The current corrupted data has 60 made / 63 used and D = 104.  
Indeed D = 23 + 38 + 43 = 104.

---

## 4. Gakdeuk interpretation

Reading Nakseo Chilgudo through the Gakdeuk principle gives the following summary.

| Quantity | Value |
|---|---:|
| Numbers used | 1 through 63, each once (intended) |
| Total sum | 2016 |
| Number of palaces | 9 |
| Numbers per palace | 7 |
| Sum per palace | **224** |
| Repeated palace-total sum | 224 × 9 = **2016** |

The value 224 is not arbitrary. The average of 1 through 63 is 32, and each palace contains seven numbers, so

```
32 × 7 = 224
```

This pattern appears in the other Gakdeuk puzzles as well.

| Puzzle | Range | Average | Numbers per palace | Target sum |
|---|---|---:|---:|---:|
| Sajagakdeuk | 1–20 | 10.5 | 4 | 42 |
| Ojagakdeuk | 1–33 | 17 | 5 | 85 |
| Yukjagakdeuk | 1–20 | 10.5 | 6 | 63 |
| **Chiljagakdeuk (Nakseo Chilgudo)** | **1–63** | **32** | **7** | **224** |

Thus Nakseo Chilgudo is the puzzle of partitioning the numbers 1 through 63 into nine blocks of seven, each summing to 224.

---

## 5. Saodo interpretation

Reading Nakseo Chilgudo through the Saodo framework reveals the following layers.

### 5.1 Center: the Luoshu nine palaces

The nine centers

```text
4  9  2
3  5  7
8  1  6
```

form the classical **Luoshu nine-palace** square. This provides the spatial skeleton for the Saodo reading.

- **Four-Way (사도)**: the four corner palaces (4, 2, 8, 6) and the four edge-midpoint palaces (9, 7, 1, 3), giving a 4+4 division.
- **Five-Way (오도)**: the four cardinal directions plus the center (5), giving a five-direction division.
- Nine = 4 + 4 + 1 = 5 + 4, so Four and Five are superimposed.

### 5.2 The meaning of seven numbers

Each palace has one center plus six surrounding numbers, for seven in total.  
The number seven can be associated with traditional concepts such as the **Seven Stars of the Big Dipper (北斗七星)** or the **seven qi (七氣)**.  
Nine palaces × seven numbers = 63 numbers, which can be read as distributing seven items among the nine palaces.

### 5.3 Magic-square property of the 3×3 palace sums

If every palace sums to 224, then the 3×3 grid of palace sums also satisfies a magic-square-like condition:

- Row sum: 224 × 3 = **672**
- Column sum: 224 × 3 = **672**
- Diagonal sum: 224 × 3 = **672**

So Nakseo Chilgudo is a superposition of two structures: a Luoshu magic square at the center and a 3×3 magic square of palace sums.

### 5.4 mod 9 residues

The centers 1 through 9 form a complete residue system modulo 9 (1, 2, 3, 4, 5, 6, 7, 8, 0).  
In the current data, the central palace (center 5) is the only palace whose surrounding numbers are all congruent to 5 modulo 9.

| Center | Surrounding numbers mod 9 |
|---|---|
| 5 | 5, 5, 5, 5, 5, 5 |

Whether this is intentional or merely a residue preserved by the data corruption needs further study.  
If the original were fully regular, each palace would probably not be a single mod-9 class; maintaining the equal-sum target of 224 requires mixing residues.

---

## 6. Corrected reconstruction: nine palaces using 1 through 63 exactly once

The following correction preserves 50 of the 54 surrounding numbers while making every palace sum to 224.  
It was obtained by MILP (mixed-integer linear programming) with the objective of keeping as many original surrounding numbers in place as possible.

| Palace (center) | Corrected seven numbers | Sum |
|---|---|---:|
| 4 | 4, 22, 27, 31, 37, 43, 60 | 224 |
| 9 | 9, 10, 15, 36, 45, 54, 55 | 224 |
| 2 | 2, 17, 28, 29, 39, 47, 62 | 224 |
| 3 | 3, 16, 26, 30, 40, 48, 61 | 224 |
| 5 | 5, 14, 23, 32, 41, 50, 59 | 224 |
| 7 | 7, 20, 24, 34, 38, 44, 57 | 224 |
| 8 | 8, 11, 12, 35, 49, 53, 56 | 224 |
| 1 | 1, 18, 19, 25, 46, 52, 63 | 224 |
| 6 | 6, 13, 21, 33, 42, 51, 58 | 224 |

### Changes from the current data

- **Palace 9 (center 6)**: 23 → 51, 36 → 58
- **Palace 2 (center 9)**: 43 → 36, 38 → 45

All other 50 surrounding numbers remain in their original palaces.  
With this correction, every integer from 1 to 63 appears exactly once and every palace sums to 224.

---

## 7. Comparison with related diagrams

| Puzzle | Palaces | Numbers per palace | Number range | Overlap? | Target sum |
|---|---|---:|---:|---|---:|
| Sajagakdeuk (Nakseo Sagudo) | 9 | 4 | 1–20 | yes (D=168) | 42 |
| Ojagakdeuk (Nakseo Ogudo) | 9 | 5 | 1–33 | yes (D=204) | 85 |
| **Chiljagakdeuk (Nakseo Chilgudo)** | **9** | **7** | **1–63** | **no (D=0)** | **224** |
| Yukjagakdeuk (Jisu-yong-yukdo) | 5 | 6 | 1–20 | yes (D=105) | 63 |
| Chiljagakdeuk (Gusuryak source) | 5 | 7 | 1–35 (4 duplicates) | yes | 120 |

The defining feature of Nakseo Chilgudo is that it partitions 1 through 63 without overlap.  
Therefore make and use coincide, and the duplication equation `k·S = T + D` has D = 0.

---

## 8. Summary

- Nakseo Chilgudo is a **Chiljagakdeuk (七子各得)** structure.
- The intended rule is that each of the nine palaces receives seven numbers summing to **224**.
- 224 = 7 × 32, the average of 1 through 63 multiplied by seven.
- The centers 1 through 9 form the classical **Luoshu nine-palace** magic square.
- The current data files contain duplicates (23, 38, 43) and omissions (45, 51, 58), so only eight palaces satisfy 224; the ninth sums to 174.
- A minimal correction preserving 50 surrounding numbers restores the full partition of 1 through 63 and makes every palace sum to 224.
