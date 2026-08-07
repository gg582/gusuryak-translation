# 九九母數變宮陽圖

> Transcription and translation of 《九九母數變宮陽圖》

—-

# Title

> 九九母數變宮陽圖

## Translation

**The *yang* (陽) arrangement of the palaces (宮) using the nine-nine numbers (九九數)**

Here, **陽圖** (*yang-myeon*) does not carry the full philosophical sense of yin and yang; it appears to mean the basic or standard arrangement.

—-

# Prefatory Note (前註)

> 宮兩一變  
> 橫看從看  
> 九數無一  
> 重複者  
> 以下四圖  
> 係新定

## Literal Translation

- The palaces (*gung*, 宮) transform two at a time.
- Viewed back and forth, horizontally and vertically, they resemble one another.
- Among the nine numbers, not a single one
- is repeated.
- The four diagrams below
- are newly established.

## Free Translation

This arrangement corresponds palace-by-palace and follows a fixed transformation rule. Horizontally it retains a nearly identical structure, while the nine numbers used are deliberately arranged without repetition. The four figures that follow are newly organized arrangements based on this principle.

—-

# Coordinate Transcription

```text
(5,1) (6,3) (4,2) (8,7) (9,9) (7,8) (2,4) (3,6) (1,5)
(4,3) (5,2) (6,1) (7,9) (8,8) (9,7) (1,6) (2,5) (3,4)
(6,2) (4,1) (5,3) (9,8) (7,7) (8,9) (3,5) (1,4) (2,6)
(2,7) (3,9) (1,8) (5,4) (6,6) (4,5) (8,1) (9,3) (7,2)
(1,9) (2,8) (3,7) (4,6) (5,5) (6,4) (7,3) (8,2) (9,1)
(3,8) (1,7) (2,9) (6,5) (4,4) (5,6) (9,2) (7,1) (8,3)
(8,4) (9,6) (7,5) (2,1) (3,3) (1,2) (5,7) (6,9) (4,8)
(7,6) (8,5) (9,4) (1,3) (2,2) (3,1) (4,9) (5,8) (6,7)
(9,5) (7,4) (8,6) (3,2) (1,1) (2,3) (6,8) (4,7) (5,9)
```

—-

# Postscript (後註)

> 從橫皆得九十數總積八百一十數

## Literal Translation

In both the vertical and horizontal directions, every line yields ninety (90), and the grand total is eight hundred ten.

## Free Translation

Every vertical and horizontal line makes the same sum (90), and the overall computed result is 810.

—-

> 本宮圖卽中編母數名圖此前逢本

## Literal Translation

This palace diagram is precisely the diagram that shows the mother numbers (*mo-su*, 母數) of the middle section, and is the original diagram presented above.

## Free Translation

The current palace diagram is the basic arrangement based on the central mother numbers; it belongs to the same family as the basic diagram explained earlier.

—-

# Commentary

This diagram does not present a new 9×9 magic square. Rather, it belongs to the orthogonal Latin-square system first described by Choi Seok-jeong.

*Among the orthogonal Latin squares presented by Choi Seok-jeong, semi-diagonal orthogonal Latin squares appear frequently, and this arrangement also has that property.*

It explains a transformation obtained by rearranging the existing basic mother-number arrangement into various palace (*gung*) arrangements.

Two points in the commentary are especially important:

- **宮兩一變** — This explicitly states that a transformation rule exists at the palace level.
- **九數無一重複者** — This emphasizes that the nine numbers used in each arrangement are not repeated.

Therefore, the core of this chapter is not the completed magic square itself, but the generation rule that transforms the basic arrangement into different palace arrangements.

—-

# Overlay Analysis of the Yang and Yin Diagrams

This is the result of overlaying 《九九母數變宮陽圖》(Gugumosubyeongungyangdo) and 《九九母數變宮陰圖》(Gugumosubyeongeumdo) coordinate by coordinate for verification (`../analyze_overlay.py`, `../visualize_overlay.py`).

**Common properties**

- In both diagrams, all 81 ordered pairs (a, b) appear exactly once, without duplication.
- In both diagrams, every row and column sums to 90, and the grand total is 810.

**Complementary structure — the yang diagram is row/column Latin, the yin diagram is palace Latin**

- In the yang diagram, each component (the first number, the second number) uses 1–9 exactly once in every row and column — it is a Latin square. The row/column sum of 90 follows from this property. However, within a palace (3×3) the components do not form a permutation, so the palace sums are uneven, ranging from 36 to 144 — exactly as stated in the text's **陽圖則九宮數多少不齊**.
- In the yin diagram, each component uses 1–9 exactly once within each palace. The nine palaces (九宮) each summing to 90 and each mini-row (3 cells) within a palace summing to 30 follow from this property. Rows and columns are not permutations, yet they still maintain the sum of 90.

**Numerical confirmation of 宮兩一變**

- The palace sums of the yang diagram pair up between vertically symmetric palaces to make 180 (63+117, 144+36). This matches **宮兩一變**, which states that the palaces correspond in pairs of two.
- In the yin diagram, all nine palaces are uniformly 90, so the paired-palace imbalance of the yang diagram is resolved.

**Overlay permutation**

- The correspondence from the yang pair to the yin pair at the same position is a permutation on the 81 pairs, with the center (5,5) as its only fixed point (cycle lengths 1, 2, 6, 8, 8, 8, 8, 9, 10, 21).
- Within each palace, interleaving the yang component with the yin component yields all 9 combinations without duplication (because the yin component is a permutation of 1–9 within the palace).
- We confirmed that no simple generation rule — such as a positional transformation (rotation or reflection) or a mod 9–based correspondence — holds.

![Cell-sum heatmap](../yang-yin-sums.png)
![Yang–yin overlay table](../yang-yin-overlay.png)
