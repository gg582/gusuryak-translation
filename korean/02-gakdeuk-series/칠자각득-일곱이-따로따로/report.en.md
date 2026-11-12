# Report: Structure of the Hado Chilodo (河圖七五圖, Chiljagakdeuk 七子各得)

## 1. Overview

The Hado Chilodo has five hexagonal clusters (top, left, centre, right, bottom). Each cluster has a centre and six vertices, seven numbers in all. The annotation is 七子各得一百二十六數: each group of seven obtains 126. The numbers 1–35 are each used once, so 5 × 126 = 630 = 1 + 2 + … + 35.

## 2. Data

Each cluster is listed as centre, then the six vertices clockwise from a starting vertex. The top and bottom hexagons have a vertex at the top, which is the starting vertex. The left, centre and right hexagons have an edge at the top, and the starting vertex is the left end of that edge.

| Cluster | Direction | Centre | Vertices | Sum |
|---|---|---|---|---|
| C1 | top | 2 | 7, 24, 34, 11, 19, 29 | 126 |
| C2 | left | 3 | 18, 33, 23, 13, 28, 8 | 126 |
| C3 | centre | 5 | 31, 20, 12, 26, 10, 22 | 126 |
| C4 | right | 4 | 15, 27, 9, 25, 32, 14 | 126 |
| C5 | bottom | 1 | 16, 21, 30, 6, 17, 35 | 126 |

- 35 numbers, 1–35, each once (an exact partition)
- Centres 1–5 placed as in the Hetu: 2 top, 3 left, 5 centre, 4 right, 1 bottom

## 3. Findings

Labels are the Five Phases mod 5: 1 Water, 2 Fire, 3 Wood, 4 Metal, 0 Earth. The complement of n is 36 − n. Since 36 ≡ 1 (mod 5), complementation exchanges Water and Earth and Fire and Metal, and keeps Wood.

1. **The left cluster is the whole Wood class.** It holds exactly 3, 8, 13, 18, 23, 28, 33, whose sum is 126. The class is closed under complementation: (3, 33), (8, 28), (13, 23) are complement pairs, and 18 is the fixed point (18 + 18 = 36).
2. **Every other cluster holds two complement pairs and a remainder of 54.**

   | Cluster | Complement pairs (sum 36) | Pair type | Remaining three | Sum |
   |---|---|---|---|---|
   | top | (2, 34), (7, 29) | Fire–Metal | 24, 11, 19 | 54 |
   | right | (4, 32), (27, 9) | Fire–Metal | 15, 25, 14 | 54 |
   | centre | (5, 31), (26, 10) | Water–Earth | 20, 12, 22 | 54 |
   | bottom | (1, 35), (30, 6) | Water–Earth | 16, 21, 17 | 54 |

   So each cluster sum is 2 × 36 + 54 = 126, and in the Wood cluster 3 × 36 + 18 = 126.
3. **The pair types sit where they sit in the Hado Saodo.** Top and right have Fire–Metal pairs (金火相守), centre and bottom have Water–Earth pairs (水土相涵), and left is Wood (兩木相摩). This is the same assignment, by position, as in the Hado Saodo and Hado Palodo, as the note on p.139 says: 五行相錯 如上四五圖之例 下並同 ("the Five Phases interlock as in the four-five diagram above; likewise below").
4. **The phase class sums form an arithmetic progression.** Water 112, Fire 119, Wood 126, Metal 133, Earth 140 (step 7). The Wood class sum equals the cluster sum, as in the Hado Saodo (Wood 42 = palace sum 42).

## 4. Formal definition

```
P = (C, K, S, X, I)
```

- `C`: 5 clusters; `K: C → {1,…,5}` centre labels (Hetu placement)
- `S: C → ℕ⁶` vertex labels, clockwise from the starting vertex
- `X`: cross layout of the five hexagons
- `I`: `K(c) + ΣS(c) = 126` for every `c`, and the 35 labels are exactly 1–35

## 5. Deliverables

- `modern_redefinition.en.md`: the definition above in more detail, with open problems
- `visualize.py`: figures (`figures/base_layout.png`, `figures/residue_distribution.png`, `figures/cluster_structure.png`, `figures/direction_graph.png`)
- `analyze_rotations.py`: per-cluster rotation report (`figures/rotation_report.txt`)
- `from_textbook.py`: the diagram as printed (`七子各得_예시.png`, `.pdf`)
