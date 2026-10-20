# In-depth Study of the *Gusuryak* Squares and Comparison with Magic-Square Families

This document gathers every square in the *Gusuryak*, computes its properties, and compares it with the main families studied in the magic-square tradition.

- Transcriptions: [`squares.py`](squares.py), copied from the latest corrected transcriptions in the repository and wiki.
- Computation: [`deep_study.py`](deep_study.py). It checks each of the 33 claims made below and stops if a change in the transcriptions breaks one.
- Generated table: [`properties.md`](properties.md)

```
python deep_study.py
```

## 1. Families used for comparison

| Family | Definition | Typical example |
| --- | --- | --- |
| Semi-magic | Every row and column has the same sum | |
| Magic | Semi-magic, and both main diagonals share that sum | Lo Shu, Dürer's order-4 square |
| Associative | Every two cells symmetric about the centre sum to min + max | Dürer's order-4 square |
| Pandiagonal | All diagonals, including broken ones, share the sum | the 48 pandiagonal order-4 squares |
| Compact (uniform 2×2) | Every 2×2 block of adjacent cells has the same sum | McClintock's most-perfect squares |
| Bordered / embedded | A smaller magic square sits in the centre | bordered squares |
| Compound | The blocks of a partition are themselves magic | Lo Shu ⊗ Lo Shu |
| Latin decomposition | Two Latin squares superposed as place values | the methods of de la Hire (1705) and Euler (1782) |
| Franklin type | Order 8, half lines sum to 130 and bent diagonals to 260 | Franklin's squares |

## 2. Overview

| Family | Diagrams in the *Gusuryak* |
| --- | --- |
| Magic | Lo Shu, Sasado yang/yin, Oodo yang/yin, Yukyukdo 1/2, Haengsudo yang/yin, Yeoksudo yang/yin, Gusudo, Gusu yin diagram, Gugujasu Byeongung yang |
| Semi-magic (diagonals differ) | Gugujasu Byeongung yin, Baekjado original and both rearrangements, Baekja Eumyang Jamo Chakjongdo corrected |
| Associative | Lo Shu, Sasado yang/yin, Oodo yin, Haengsudo yin, Yeoksudo yin, Gusudo |
| Pandiagonal | none |
| Compact | Baekjado original (2×2 sum 202) |
| Embedded centre | Oodo yang (3×3), Haengsudo yang (3×3), Yeoksudo yin (4×4), Gusudo and Gusu yin diagram (central palace) |
| Compound | Gusudo (every palace magic), Gugujasu Byeongung yang (every palace magic), Gusu yin diagram (every palace semi-magic) |
| Latin decomposition | Gugumosu Byeongung yang (orthogonal Latin pair → order-9 magic square) |
| Half-orthogonal Latin pair | Baekja Saengseong Sunsudo and Gyosudo (50 ordered pairs × 2) |

## 3. Square by square

### 3.1 Lo Shu

Up to rotation and reflection, the Lo Shu is the only order-3 magic square on 1–9. It is associative: the complementary pairs (1,9), (2,8), (3,7), (4,6) all face each other across the centre 5. The order-9 squares of the *Gusuryak* start from using this Lo Shu twice (see 3.8).

### 3.2 Sasado (order 4)

- Both the yang and yin squares are associative magic squares. Of the 880 order-4 magic squares (Frénicle, 1693), only 48 are associative, and both diagrams belong to them.
- The yin square equals, up to rotation and reflection, the array obtained by writing 1–16 in order and replacing the numbers on both diagonals by their complements (17 − v). The source text "十六子順排四行 … 外四角對換 … 內四角對換得陰圖" describes exactly this procedure. The same array is known as the order-4 square that Agrippa (1531) assigned to Jupiter.
- The yang square has the same row sets and column sets as the yin square, so it comes from rearranging the rows and columns of the yin square ("一變以爲陽圖"). The square in Dürer's *Melencolia I* (1514) has the same row and column sets and belongs to the same class.

### 3.3 Oodo (order 5)

- The yang square is not associative, but its central 3×3, made of 7, 8, 9, 12, 13, 14, 17, 18, 19, is a magic square with constant 39. Of its 12 complementary pairs, 8 are centrally symmetric, 2 are mirrored within a row and 2 within a column.
- The yin square is a magic square on 9–33 with constant 105, and all its complementary pairs are centrally symmetric (pair sum 42). The set is 1–25 shifted by 8, so the constant is 65 + 5 × 8 = 105.
- Neither rotation, reflection, complement nor row/column rearrangement turns one square into the other. Neither is related in these ways to the order-5 square produced by de la Loubère's Siamese method.

### 3.4 Yukyukdo (order 6)

- For orders that leave remainder 2 on division by 4, such as 6, no associative and no pandiagonal magic squares exist. Neither example is either.
- In example 2, 16 of the 18 complementary pairs are centrally placed, so it comes as close as possible to the impossible associative square. In example 1, 6 pairs are mirrored within a row and 12 lie elsewhere.
- Rotation, reflection, complement and row/column rearrangement do not turn one example into the other. Even every affine map of positions over ℤ₆, with or without the complement 37 − v, fails to send example 1 to example 2, so the two are independent solutions.

### 3.5 Haengsudo (order 7)

- The yang square is not associative, but its central 3×3 is a magic square with constant 75. Its complementary pairs are 16 centrally symmetric, 4 row-mirrored and 4 column-mirrored.
- The yin square is associative: all 24 complementary pairs are centrally symmetric.
- Yang Hui's *Xugu zhaiqi suanfa* (1275) called its order-7 square 衍數圖. The characters 行 and 衍 look alike, which is worth keeping in mind when tracing the name.

### 3.6 Yeoksudo (order 8)

- Yang square: every two horizontally adjacent cells (columns 1–2, 3–4, …) form a complementary pair summing to 65. Hence the left and right halves of every row sum to 130. All four 4×4 quadrants sum to 520. It is not associative.
- Yin square: associative; every half row and half column sums to 130 and every quadrant to 520. The central 4×4 is a magic square with constant 130. The half-line sums resemble a Franklin square, but its bent diagonals do not all sum to 260, so it is not one.
- The name 易數圖 matches the name Yang Hui gave his order-8 square.

### 3.7 A rule shared by the yang/yin pairs

The yin squares of orders 4, 5, 7 and 8 are all associative, while the yang squares of orders 5, 7 and 8 are not. The yang squares carry local structure (an embedded centre in orders 5 and 7, adjacent complementary pairs in order 8), and the yin squares carry the global structure of central symmetry. Apart from order 4, each yang/yin pair consists of two independent solutions with no transformation between them.

### 3.8 Gusudo and the Gusu yin diagram (order 9)

- The Gusudo is Lo Shu ⊗ Lo Shu (a Kronecker structure). All nine palaces are magic, and the whole square is associative. The palace sums are 9 × Lo Shu + 324, so the arrangement of palace sums is itself a Lo Shu.
- The Gusu yin diagram is not associative, and its palaces are semi-magic (rows and columns 123). Still, all nine palace sums equal 369. Writing v − 1 = 9q + r, both q and r take each of 0–8 once in every palace, and every row and column of each sums to 36. This reads as de la Hire's method with "palace-complete" arrays in place of Latin squares.
- In both squares the central palace is a full order-3 magic square.

### 3.9 Gugumosu Byeongung yang and yin

- In the yang diagram both components are Latin squares and all 81 ordered pairs occur once: an orthogonal Latin pair. The first component is constant 5 on the main diagonal and a permutation of 1–9 on the other; the second is the reverse. This is exactly the condition de la Hire (1705) and Euler (1782) used, and it makes 9(a − 1) + b a normal order-9 magic square on 1–81. That square differs from the Gusudo.
- In the yin diagram the components are not Latin squares, but each takes 1–9 once in every palace and all 81 ordered pairs are distinct. As in the yang diagram, a + b sums to 90 in every row and column.

### 3.10 Gugujasu Byeongung yang and yin

- Both diagrams hold each of the 81 products of the multiplication table once (36 distinct numbers).
- In the yang diagram each cell is L(palace) × L(position in palace), so every palace is k × Lo Shu and the whole is a magic square with constant 225.
- The yin diagram is symmetric about the secondary diagonal; rows and columns give 225, the diagonals 165 and 285.
- The cells hold products, but the lines balance sums rather than products, so these are not multiplicative magic squares.

### 3.11 The Baekja family (order 10)

- Yang Hui's original Baekjado is semi-magic, and every 2×2 block of adjacent cells, including blocks that wrap around the edges, sums to 202 = 2(n² + 1). This compactness is one of the conditions of a most-perfect square. Order 10 cannot be pandiagonal, so the square cannot be most-perfect, yet it is regular enough that its broken diagonals take only the two values 470 and 540. All 50 complementary pairs sit opposite each other within the same row.
- The alternative rearrangement and Hong Jeong-ha's rearrangement move the diagonal sums closer to 505 (490 and 520; 504 and 506) at the cost of compactness. The compactness of the original is better read as intended structure than as a copying error.
- Baekja Eumyang Jamo Chakjongdo: in the original only 48 of the 50 complementary pairs are mirrored within a row; in the five-cell correction all 50 are. This gives independent support for the correction, since it restores the original symmetry rule.
- The two Latin squares of the Baekja child/parent Eumyang Chakjongdo satisfy child = 10 − parent (10 when the parent is 0), so they are dependent, and only 10 ordered pairs occur, 10 times each. Superposing them therefore cannot give a 1–100 magic square.
- In the Sunsudo and Gyosudo both components are Latin squares, 50 ordered pairs occur twice each, and the diagrams have 180° rotational symmetry. Contrary to Euler's conjecture, orthogonal Latin squares of order 10 exist, as Bose, Shrikhande and Parker showed in 1959. The two *Gusuryak* diagrams stop at half of that: a "half-orthogonal" pair with 50 pairs.

## 4. Conclusions

1. Every normal square of orders 3–9 in the *Gusuryak* is magic, and none is pandiagonal. Associative and embedded-centre squares stand out instead.
2. Apart from order 4, each yang/yin pair consists of independent solutions, and the rule that the yin square is the associative one holds for orders 4, 5, 7 and 8.
3. Order 9 brings together a compound square built from two layers of Lo Shu (Gusudo), a square of semi-magic palaces built from palace-complete arrays (Gusu yin diagram), and an orthogonal Latin pair (Mosu yang). Latin-decomposition constructions appear in one book around the time of de la Hire (1705) and well before Euler (1782).
4. Order 10 shows distinct solutions: a compact semi-magic square (Baekjado), half-orthogonal Latin pairs (Sunsudo, Gyosudo) and a dependent Latin pair (child/parent Chakjongdo).
