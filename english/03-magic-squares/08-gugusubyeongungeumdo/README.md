# Gugumosubyeongungeumdo (Nine-Nine Mother-Numbers Palace-Transformation Yin Diagram, 九九母數變宮陰圖)

> Transcription and translation of 《九九母數變宮陰圖》

—-

# Title

> 九九母數變宮陰圖

## Translation

**Arrangement of the *yin* side (陰圖) of the palace (宮) using the nine-nine numbers (九九數)**

Here, **陰圖** (*yin diagram*) does not carry the full philosophical sense of yin and yang; it appears to mean a variant arrangement paired with the *yang* diagram (陽圖, the basic arrangement).

—-

# Coordinate Transcription

```text
(5,6) (9,2) (1,7) (7,8) (5,1) (3,6) (1,3) (9,4) (5,8)
(3,8) (4,4) (8,3) (2,4) (9,9) (4,2) (6,7) (2,2) (7,6)
(7,1) (2,9) (6,5) (6,3) (1,5) (8,7) (8,5) (4,9) (3,1)
(1,2) (8,4) (9,6) (6,4) (1,9) (8,2) (9,8) (6,2) (4,1)
(5,7) (3,3) (7,5) (7,3) (5,5) (3,7) (3,5) (7,7) (5,3)
(6,9) (4,8) (2,1) (2,8) (9,1) (4,6) (1,4) (2,6) (8,9)
(7,9) (6,1) (2,5) (2,3) (9,5) (4,7) (4,5) (8,1) (3,9)
(3,4) (8,8) (4,3) (8,6) (1,1) (6,8) (2,7) (6,6) (7,2)
(5,2) (1,6) (9,7) (7,4) (5,9) (3,2) (9,3) (1,8) (5,4)
```

—-

# Postscript (後註)

> 共積上同  
> 從橫及九宮皆得九十數  
> 九宮之內每行三者皆得三十數  
> 陽圖則九宮數多少不齊  
> 此圖尨妙允符洛書之數

## Literal Translation

- The grand total of the whole is the same as above.
- Vertically and horizontally, and in the nine palaces (宮), all obtain the number ninety (90).
- Within the nine palaces, every row of three obtains the number thirty (30).
- In the *yang* diagram (陽圖), the numbers of the nine palaces are uneven, some more and some less.
- This diagram is intermingled yet marvelous, truly in accord with the numbers of the Luoshu (洛書).

## Free Translation

The total sum is the same as in the preceding *yang* diagram (陽圖).
Every column and every row sums to 90, each of the nine 3×3 palaces (宮) also sums to 90,
and every three-cell horizontal sub-row (小行) within each palace makes 30.
Whereas in the *yang* diagram the palace sums were uneven,
this *yin* diagram — though its numbers appear intermingled — possesses a marvelous balance and conforms to the numbers of the Luoshu (洛書).

—-

# Commentary

This diagram is the *yin* arrangement (陰圖) paired with 《Gugumosubyeongungyangdo (九九母數變宮陽圖)》, and it belongs to the same orthogonal Latin-square system.

Verifying the transcribed coordinates confirms the postscript's description exactly.

- The 81 ordered pairs (a, b) each appear exactly once, with no duplicates.
- Every row and every column sums to 90 (從橫皆得九十數).
- Each of the nine 3×3 palaces (宮) sums to 90.
- Every three-cell horizontal sub-row (小行) within each palace sums to 30 (每行三者皆得三十數).

As the text itself points out, **陽圖則九宮數多少不齊** — in the *yang* diagram the palace sums are uneven (e.g., the upper-left palace sums to 63, the central palace to 90). By contrast, the *yin* diagram is balanced all the way down to the palace level, which is why it is praised as **尨妙** — outwardly intermingled yet marvelous.

**允符洛書之數** means that the structure — in which the palaces (sum 90) and the sub-rows (sum 30) overlap to form a balance — conforms to the principle of the Luoshu (洛書), the 3×3 magic square.

—-

# Overlay Analysis of the Yang and Yin Diagrams

This is the result of overlaying 《Gugumosubyeongungyangdo (九九母數變宮陽圖)》 and 《Gugumosubyeongungeumdo (九九母數變宮陰圖)》 at matching coordinates and verifying them (`../analyze_overlay.py`, `../visualize_overlay.py`).

**Common properties**

- In both diagrams the 81 ordered pairs (a, b) each appear exactly once, with no duplicates.
- In both diagrams every row and column sums to 90, and the grand total is 810.

**Complementary structure — the yang diagram is row/column-Latin, the yin diagram is palace-Latin**

- In the *yang* diagram, each component (first number, second number) uses 1–9 exactly once across every row and column — a Latin square. The row and column sums of 90 follow from this property. However, within a palace (3×3) the components do not form permutations, so the palace sums are uneven, ranging from 36 to 144 — exactly as the text states, **陽圖則九宮數多少不齊**.
- In the *yin* diagram, each component uses 1–9 exactly once within each palace. The nine palaces (九宮) each summing to 90, and the three-cell sub-rows within each palace summing to 30, follow from this property. Rows and columns are not permutations, yet they still maintain the sum of 90.

**Numerical confirmation of 宮兩一變**

- In the *yang* diagram, the palace sums pair up between vertically symmetric palaces to make 180 (63+117, 144+36). This matches **宮兩一變** — the palaces correspond to one another in pairs.
- In the *yin* diagram all nine palaces are uniform at 90, so the paired-palace imbalance of the *yang* diagram is resolved.

**Overlay permutation**

- The correspondence from *yang*-diagram pairs to *yin*-diagram pairs at the same position is a permutation on the 81 pairs; its only fixed point is the center (5,5) (cycle lengths 1, 2, 6, 8, 8, 8, 8, 9, 10, 21).
- Cross-overlaying the *yang* component and the *yin* component within each palace yields 9 combinations with no duplicates (because the *yin* component is a 1–9 permutation within each palace).
- No simple generation rule — such as a positional transformation (rotation or reflection) or a mod 9–based correspondence — was found to hold.

![Cell-sum heatmap](../yang-yin-sums.png)
![Yang–yin overlay table](../yang-yin-overlay.png)
