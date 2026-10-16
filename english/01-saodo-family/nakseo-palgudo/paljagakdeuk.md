# Rereading Nakseo Palgudo as Palja-Gakdeuk (八子各得)

Nakseo Palgudo (洛書八九圖) is drawn in the form of the **O-pal-jeong-jeon-do (五八井田圖)**, the Five-Eight Well-Field Diagram.
On a 7×7 well-field (井田) grid, the nine well (井) positions are left empty, and the integers from 1 to 40 are placed in the surrounding cells.
Like an Easter egg built into the name, it has the **palja-gakdeuk** structure: **each well obtains 8 cells (八子), and every well reaches the same sum of 164.**

---

## 1. Basic figures of palja-gakdeuk

| Item | Value |
|---|---:|
| Numbers used | 1 to 40, each exactly once |
| Sum of all numbers | 820 |
| Number of wells (宮) | 9 |
| Cells obtained per well (子) | 8 |
| Sum per well | **164** |
| Multiplicity-weighted total over 9 wells | 164 × 9 = **1476** |

The per-well sum 164 is the result of the fair-share rule:

```
164 = 8 × (40 + 1) / 2 = grand total 820 × 8 / 40
```

That is, each well receives exactly **one eighth** of the full set of 40 numbers.

---

## 2. Separating 作 (making) from 用 (using): forty numbers made, seventy-two numbers used

- **四十子作 (forty numbers made)**: the integers 1 to 40 are each written exactly once on the diagram. Their total is 820.
- **七十二子用 (seventy-two numbers used)**: since each of the nine wells obtains 8 cells, the structure has 9 × 8 = 72 positions in total.
- The difference **72 − 40 = 32** is the number of overlap positions shared by adjacent wells.

Multiplicity equation:

```
9 × 164 = 820 + D
1476 = 820 + D
D = 656
```

The per-cell duplication degrees are as follows.

| Duplication degree | Number of cells | Contribution |
|---|---:|---:|
| Belongs to exactly 1 well | 16 | 16 |
| Belongs to 2 wells | 20 | 40 |
| Belongs to 4 wells | 4 | 16 |
| Total | 40 | 72 |

16 + 40 + 16 = 72, which matches 9 × 8.

---

## 3. Placing the nine wells: each well obtains eight numbers

On the 7×7 grid, the nine wells are 3×3 blocks centered at (odd, odd) coordinates, and their center cells are empty.
The arrangement reconstructed by `reconstruct_milp.py` (the `grid_data` in `visualize.py`) satisfies the following.

- The integers 1 to 40 are used exactly once.
- The 8 cells surrounding each of the nine wells all sum to **164**.

The reconstruction corrects only **6 cells** of the observed arrangement. The corrections form two 3-cycles.

```
(0,4): 4 -> 9,  (0,6): 9 -> 13,  (2,6): 13 -> 4
(1,4): 33 -> 29, (2,5): 29 -> 37, (5,0): 37 -> 33
```

In the observed arrangement the well sums were 160, 163, 164, 164, 164, 165, 168; after the correction all nine become 164.

---

## 4. The double Easter egg of 五八 (five-eight)

The name O-pal-jeong-jeon-do (五八井田圖) embeds two numbers.

- **八 (8)**: the number of cells each well obtains (八子) — exactly the y-rule of the Nakseo Y-gudo family
- **五八 = 40**: the total count of numbers used (1–40)

The name itself carries the design specification: "place 40 numbers into nine 8-cell wells."

---

## 5. Relation to the Gusuryak palja-gakdeuk

The palja-gakdeuk of the Gusuryak series in `02-gakdeuk-series/paljagakdeuk-eight-each-gets` places **8 numbers in each of 5 palaces** and makes every palace sum to **164** (5 × 164 = 820, an exact partition).

| Item | Nakseo Palgudo (O-pal-jeong-jeon-do) | Gusuryak palja-gakdeuk |
|---|---|---|
| Number of groups | 9 wells | 5 palaces |
| Cells per group | 8 cells | 8 numbers |
| Group sum | 164 | 164 |
| Numbers used | 1–40 | 1–40 |
| Overlap | yes (72 used / 40 made) | none (40 used / 40 made) |

They are two implementations of the same **y = 8, T = 164** rule.
If Nakseo Palgudo is the same rule spread with overlaps over a 9-palace space, the Gusuryak palja-gakdeuk is the same rule divided exactly into 5 palaces.

---

## 6. Seen from the saodo (四/五道) viewpoint

Nakseo Palgudo is a structure that realizes a **paldo (八道)** partial-sum invariant of 8 cells on a space (sado, 四道) in which nine wells are arranged in a 3×3 layout.
The 8 cells of each well are the remainder of a 3×3 block with its center removed, and the empty center forms the hole of the well (井).
The essence of palja-gakdeuk is that all well sums stay at 164 even where neighboring wells share edges and overlap (corresponding to 鄰星相兼, neighboring stars sharing).

---

## 7. Summary

| Viewpoint | Summary |
|---|---|
| Combinatorial structure | 40 numbers → 9 wells, 8 cells per well |
| Invariant | every well sums to 164 |
| Generation principle | fair share: grand total × 8/40 |
| Spatial structure | 7×7 well-field grid, nine empty well centers |
| Overlap | 72 used / 40 made, 32 simple overlap positions |
| Numbers in the name | 八 = cell count, 五八 = 40 = number count |

Nakseo Palgudo is a combinatorial design that packs the integers 1 to 40 into nine wells, 8 cells each with overlaps, under the name palja-gakdeuk.
164 is the exact share of the whole that each well receives, and the MILP reconstruction restores that design by changing only 6 cells of the observed arrangement.
