# Dual Reading: Saodo (Four/Five Way) and Gakdeuk (Each-Gets)

Nakseo Sagudo (洛書四九圖) and Nakseo Ogudo (洛書五九圖) are read directly as **Sajagakdeuk (四子各得)** and **Ojagakdeuk (五子各得)**, but they can also be read through the **Saodo (四/五道, Four/Five Way)** lens.  
This document converts each diagram back and forth between the two systems and strengthens the unification comparison.

---

## 1. Original texts and basic numbers

### Nakseo Sagudo → Sajagakdeuk

> 鄰星相兼五宫化 爲九宫每宫四子 各得四十二數  
> 此即河圖四五画 右旋者 互化則一千八百九十數

| Quantity | Value |
|---|---:|
| Numbers used | 1–20 (20 numbers) |
| Palaces | 9 |
| Numbers per palace | 4 |
| Sum per palace | **42** |
| Repeated palace-total sum | 378 |
| Made / Used | 20 made / 36 used, D = 168 |

### Nakseo Ogudo → Ojagakdeuk

> 五子各得 八十五數  
> 九宮共得 七百六十五數

| Quantity | Value |
|---|---:|
| Numbers used | 1–33 (33 numbers) |
| Palaces | 9 |
| Numbers per palace | 5 |
| Sum per palace | **85** |
| Repeated palace-total sum | 765 |
| Made / Used | 33 made / 45 used, D = 204 |

---

## 2. Mutual conversion tables

### 2.1 Gakdeuk → Saodo

| Diagram | Gakdeuk reading | Saodo reading |
|---|---|---|
| Nakseo Sagudo | Each of 9 palaces gets 4 numbers summing to 42 (Sajagakdeuk) | Five wuxing classes are overlapped into 9 blocks. The Four-Way partial-sum invariant is realised on top of the Five-Way classification. |
| Nakseo Ogudo | Each of 9 palaces gets 5 numbers summing to 85 (Ojagakdeuk) | A 3×3 grid of plus-shaped 5-vertex palaces. The Five-Way partial-sum invariant is expanded into a Four-Way 3×3 grid. |

### 2.2 Saodo → Gakdeuk

| Saodo element | Nakseo Sagudo Gakdeuk meaning | Nakseo Ogudo Gakdeuk meaning |
|---|---|---|
| Four-Way (사도) | Each palace has 4 numbers; central 4-cycle | 9 palaces split into 4 corners + 4 edges + 1 centre |
| Five-Way (오도) | 20 numbers classified into 5 mod-5 classes | Each plus palace = 1 centre + 4 orthogonal neighbours |
| Nine Palaces (九宫) | 9 blocks, all summing to 42 | 9 plus palaces, all summing to 85 |
| Made / Used | 20 made / 36 used | 33 made / 45 used |

---

## 3. Unification: common ground and interpretive differences

### Common ground

| Feature | Sajagakdeuk (Nakseo Sagudo) | Ojagakdeuk (Nakseo Ogudo) |
|---|---|---|
| Number of palaces | 9 | 9 |
| Wuxing classification | 5 residue classes | 5 residue classes |
| Partial-sum invariant | Every palace sums to 42 | Every palace sums to 85 |
| Repeated palace-total sum | 42 × 9 = 378 | 85 × 9 = 765 |
| Core spatial structure | Central core + four-direction extension | Central core + four-direction extension |
| Made / Used distinction | Yes | Yes |

### Interpretive differences

| Feature | Sajagakdeuk (Nakseo Sagudo) | Ojagakdeuk (Nakseo Ogudo) |
|---|---|---|
| Numbers per palace | 4 | 5 |
| Range of numbers used | 1–20 (20) | 1–33 (33) |
| Central core | 4-cycle (5, 16, 10, 11) | Plus-shaped 5 vertices (5, 19, 26, 18, 17) |
| Geometry | 3×2 rectangle, four hexagonal faces | 3×3 grid, nine plus-shaped palaces |
| Original sum formula | 5 classes × 9 palaces × 42 = 1,890 | 9 palaces × 85 = 765 |
| Emphasised Way | Four-Way (사도) | Five-Way (오도) |
| Modern name | Sajagakdeuk | Ojagakdeuk |

**Summary:** Sajagakdeuk realises a **Four-Way partial-sum invariant** on a **Five-Way classification**, while Ojagakdeuk expands a **Five-Way partial-sum invariant** inside a **Four-Way 3×3 grid**.  
Both share the **Gakdeuk principle** — every palace has the same partial sum — but their geometry and totals differ according to whether the Four-Way or the Five-Way is central.

---

## 4. Place in the Π(p, q, T) framework

The parameter family introduced in `04-unification` is

```
Π(p, q, T)
```

- `p`: number of directions (or wuxing phases)
- `q`: number of peripheral slots per direction
- `T`: target sum for each direction (large cluster)

| Puzzle | p | q | T |
|---|---|---|---|
| Sajagakdeuk (9 palaces, 4 numbers) | 5 (wuxing) | 3 (two-cycle layers) | 34, 38, 42, 46, 50 |
| Ojagakdeuk (9 palaces, 5 numbers) | 5 (wuxing) | 6 or 7 | 99, 105, 112, 119, 126 |

Thus the two diagrams are two variations of the same Gakdeuk principle, differing only in the relative weight of Four and Five.

---

## 5. Modern relevance: which reading is more advanced?

- The **Saodo reading** uses the traditional cosmological vocabulary (directions, wuxing, nine palaces).
- The **Gakdeuk reading** makes the underlying **partial-sum invariant** explicit inside the same framework.
- Therefore the **Gakdeuk reading is more advanced** for the late Joseon / early 18th-century publication context: it is not merely "looks like a magic square" but states the quantitative rule that every subset has the same sum.
- For a modern reinterpretation, look at:
  1. **Integer linear equations** (`Σ_{v∈C} x_v = S` for every cluster C)
  2. **Overlap equation** (`k·S = T + D`)
  3. **Modular / CRT classification** (mod 2, 3, 4, 5, 6, 9, 12)
  4. **Cluster rotational symmetry** (`rotation_analysis.py`)
