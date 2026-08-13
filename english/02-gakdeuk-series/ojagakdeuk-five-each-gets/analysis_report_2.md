# Ojagakdeuk (Five-Each-Gets / Heaven-Water Five-Use Diagram) Layout 2 — Modern Combinatorial and Positional Analysis Report

> A modern mathematical reinterpretation of the **second number placement** of the Ojagakdeuk (五子各得) diagram, also known as Cheonsu-yong-odo (天水用五圖), from the *Gusuryak* (九數略) family of diagrams.
> **Analysis target**: A diagram with the same geometric form as the original placement, but placing all of the numbers 1 through 21.
> **Placement rule (per the original text)**: Central line (top to bottom) 12, 5, 2, 15, 6, 1, 16 / Left (outer column to inner column, vertical) 7 / 13, 3, 11 / 17, 20, 10 / Right (outer column to inner column, vertical) 8 / 19, 4, 14 / 18, 9, 21.
> **Analysis premise**: The original diagram contains only points (nodes) and no connecting lines, so this report considers only positional, wuxing (five-phase), and combinatorial invariants.
> **Clarification**: This report and its associated visualization figures represent a **Rule Variation Model** constructed to explore the symmetry and wuxing number structure of the original design, rather than a raw historical facsimile of the original manuscript.

---

## 1. Basic Structure and Verification

### 1.1 Data Summary

Layout 2 places all 21 natural numbers from 1 to 21 in the same Cheonsu-yong-odo geometric form as the original. No numbers are omitted; the 21 numbers are divided into five wuxing (phase) groups by mod 5.

| Item | Content |
|:---:|:---|
| Numbers used | All of 1–21 (21 total) |
| Omitted numbers | None |
| Total sum | 231 |
| Number of wuxing groups | 5 |

- **Verification**: The sum of 1 through 21 is 21 × 22 / 2 = **231**.

### 1.2 Cheonsu-yong-odo Form

The 21 nodes form the same geometric shape as the original, converging from the upper vertex (12) to the lower vertex (16). A central axis 12-5-2-15-6-1-16 runs through the middle, and the widest central horizontal band lies near y = 2.0.

```
        12 (upper vertex)
       /  \
     17 — 5 — 18
      \   |   /
        2
       / | \
   7- 3-20-15- 9- 4- 8 (central horizontal band)
   \  |  X  |  /
    11- 6-14
      \ | /
        1
        |
        16 (lower vertex)
```

> Observation 1: The upper vertex changed from 19 (original) to 12, and the lower vertex from 2 to 16. The central vertical axis 12-5-2-15-6-1-16 sums to 57.

---

## 2. Geometric Structure Analysis

### 2.1 Topological Features

The original text mentions no edges or specific relationships between points, so the structure is analyzed from the placement of points alone.

- **Number of nodes**: 21
- **Upper vertex**: 12 (y = 6.0)
- **Lower vertex**: 16 (y = -1.7)
- **Vertical central axis**: 12 → 5 → 2 → 15 → 6 → 1 → 16 (7 nodes, sum 57)
- **Central horizontal band**: 7 nodes (3, 4, 7, 8, 9, 15, 20) at y = 2.0

> Observation 2: The original's vertical central axis had 6 nodes (19-6-20-5-17-2), but in Layout 2 the axis includes 15, the center of the central horizontal band, forming a single axis of 7 nodes. The mod 5 residues along this axis are Fire(2)-Earth(0)-Fire(2)-Earth(0)-Water(1)-Water(1)-Water(1): the upper part alternates Fire and Earth, while the lower part is three consecutive Waters — a regular pattern.

### 2.2 Vertical Layer Distribution

| Layer | Position | Nodes | Sum |
|:---:|:---|:---|:---:|
| Upper vertex | y = 6.0 | 12 | 12 |
| Upper connector | y = 5.0–4.2 | 5, 17, 18 | 40 |
| Central horizontal band | y = 3.3–2.0 | 2, 3, 4, 7, 8, 9, 13, 15, 19, 20 | 100 |
| Lower connector | y = 0.8–-0.4 | 1, 6, 10, 11, 14, 21 | 63 |
| Lower vertex | y = -1.7 | 16 | 16 |

> Observation 3: The central horizontal band sums to 100, about 43.3% of the total sum 231. As in the original (128/265 ≈ 48.3%), the center is the heaviest part.

---

## 3. Wuxing (Five Phases) mod 5 Analysis

### 3.1 Phase Classification and Sums

| Wuxing | mod 5 | Numbers | Sum | Count |
|:---:|:---:|:---|:---:|:---:|
| Water (水) | 1 | 1, 6, 11, 16, 21 | 55 | 5 |
| Fire (火) | 2 | 2, 7, 12, 17 | 38 | 4 |
| Wood (木) | 3 | 3, 8, 13, 18 | 42 | 4 |
| Metal (金) | 4 | 4, 9, 14, 19 | 46 | 4 |
| Earth (土) | 5 | 5, 10, 15, 20 | 50 | 4 |

> Observation 4: Because 1–21 is used, only Water has 5 numbers while the other four phases have 4 each. Notably, **the sums of Fire, Wood, Metal, and Earth — 38, 42, 46, 50 — form an arithmetic progression with common difference 4** (in residue order, which differs from the generation order Wood → Fire → Earth → Metal → Water). Water (55) lies outside this progression.

### 3.2 Spatial Distribution of Wuxing

| Wuxing | Main positional feature |
|:---:|:---|
| Water | 3 on the vertical central axis (1, 6, 16), 1 on the left (11), 1 on the right (21) |
| Fire | Includes the upper vertex (12), the center (2), and the left (7, 17) |
| Wood | Evenly balanced, 2 on the left (3, 13) and 2 on the right (8, 18) |
| Metal | **All on the right** (4, 9, 14, 19) |
| Earth | Only on the center (5, 15) and the left (10, 20) |

> Observation 5: All four Metal numbers (4, 9, 14, 19) are clustered in the right region, and Earth (5, 10, 15, 20) appears only in the center and left. Unlike the original, where Earth was concentrated on the central axis, Layout 2 shows a much stronger spatial bias of the wuxing.

---

## 4. Position-Based Analysis

### 4.1 Sum by Horizontal Level (y-coordinate)

| y-coordinate | Nodes | Sum |
|:---:|:---|:---:|
| 6.0 | 12 | 12 |
| 5.0 | 17, 18 | 35 |
| 4.2 | 5 | 5 |
| 3.3 | 2, 13, 19 | 34 |
| 2.0 | 3, 4, 7, 8, 9, 15, 20 | 66 |
| 0.8 | 6, 11, 14 | 31 |
| -0.4 | 1, 10, 21 | 32 |
| -1.7 | 16 | 16 |

> Observation 6: The y = 2.0 level holds 7 nodes (sum 66), forming the widest central horizontal band. This is about 28.6% of the total sum 231.

### 4.2 Left-Center-Right Symmetry

| Region | Nodes | Sum |
|:---:|:---|:---:|
| Left (x < -0.5) | 3, 7, 10, 11, 13, 17, 20 | 81 |
| Center (-0.5 ≤ x ≤ 0.5) | 1, 2, 5, 6, 12, 15, 16 | 57 |
| Right (x > 0.5) | 4, 8, 9, 14, 18, 19, 21 | 93 |

> Observation 7: **The strongest invariant of the original placement — the left-right sum equality (86 = 86) — does not hold in Layout 2.** The right side is heavier by 12 (left 81, right 93). This is consistent with the all-right bias of Metal noted in §3.2. Incidentally, right − left = 12 coincidentally equals the upper vertex number 12.

### 4.3 mod 5 Residue Spatial Pattern

Along the vertical central axis (y = 6.0 → -1.7), the sequence is 12 (Fire) → 5 (Earth) → 2 (Fire) → 15 (Earth) → 6 (Water) → 1 (Water) → 16 (Water). The upper 4 nodes alternate Fire and Earth, while the lower 3 are uniformly Water, so the phases converge as the central axis descends.

---

## 5. The Cross-Shaped (十字) Palace Structure — Each Palace Sums to 54

This is the core structural rule of Layout 2. Taking 15, the center of the central horizontal band, as the center palace (中宮), and dividing the remaining 20 nodes into the four palaces (宮) — upper, lower, left, right — corresponding to the four arms of a cross, **each palace consists of exactly 5 numbers and sums to exactly 54**.

| Palace | Position | Numbers | Sum |
|:---:|:---|:---|:---:|
| Upper palace (上宮) | Upper vertex to upper connector | 2, 5, 12, 17, 18 | 54 |
| Left palace (左宮) | Left arm | 3, 7, 11, 13, 20 | 54 |
| Right palace (右宮) | Right arm | 4, 8, 9, 14, 19 | 54 |
| Lower palace (下宮) | Lower connector to lower vertex | 1, 6, 10, 16, 21 | 54 |
| Center palace (中宮) | Center of the central horizontal band | 15 | 15 |

- **Verification**: 54 × 4 = 216 (total of the outer palaces), and 216 + 15 = 231 matches the grand total exactly.
- **Consistency with the source text**: The *Gusuryak*-family text states: "去中宮十五 / 外合得二百一十六 應乾之策 / 每宮各得五十四 爲六九之數" — "Removing the fifteen of the center palace, the outer palaces together yield two hundred sixteen, corresponding to the tally number of Qian (乾之策); each palace obtains fifty-four, which is the number of six-nines (六九之數)." Layout 2 implements this rule numerically and exactly (216 = 36 × 6 = the Qian tally; 54 = 6 × 9 = the six-nine number).
- **The name Ojagakdeuk**: Each palace is made of five (五) numbers, and every palace "each obtains (各得)" the same sum 54 — a structure in keeping with the diagram's name, Ojagakdeuk (五子各得, "five each gets").
- **Relation to §4.2**: Under the straight left-center-right partition the sums were asymmetric (left 81 ≠ right 93, §4.2), but under the cross-palace partition the four palaces upper, lower, left, and right are perfectly equal. In other words, the balancing principle of Layout 2 lies not in an orthogonal straight-line partition but in the cross-palace partition centered on the center palace.
- **Wuxing composition per palace**: The right palace is dominated by a single phase — 4 Metals plus 1 Wood (8); the lower palace likewise has 4 Waters plus 1 Earth (10). The upper palace consists of 3 Fires (2, 12, 17) plus Wood (18) and Earth (5), and the left palace consists of 2 Woods (3, 13) plus Fire (7), Water (11), and Earth (20).

---

## 6. Rotation Analysis

Rotation analysis results for each mod 5 residue class, arranged in angular order (clockwise from 12 o'clock) (`rotation_report_2.txt`):

| Wuxing | Angular order | Sum | Opposite-pair sums |
|:---:|:---|:---:|:---|
| Water (r=1) | 21 → 1 → 6 → 16 → 11 | 55 | — (odd-sized group) |
| Fire (r=2) | 2 → 12 → 7 → 17 | 38 | [9, 29] |
| Wood (r=3) | 18 → 8 → 3 → 13 | 42 | **[21, 21]** |
| Metal (r=4) | 19 → 4 → 9 → 14 | 46 | [28, 18] |
| Earth (r=5) | 5 → 15 → 10 → 20 | 50 | [15, 35] |

> Observation 8: In the Wood group's angular ordering, **all opposite pairs sum to 21** (18 + 3 = 8 + 13 = 21). However, since the original has no intrinsic cycle and this ordering was constructed arbitrarily by angular position, this is treated as an auxiliary observation rather than an invariant of the diagram itself. No global 180° rotational symmetry holds.

---

## 7. Study on Rule Variation and System Extension (Rule Variation & Extension Study)

### 7.1 1–24 Rule Variation Model Study

Constructing a 24-number variation model by adding 22, 23, and 24 to Layout 2 (1–21) gives the following.

| Wuxing | Original Selected | Variation Added | 24-Number Variation Group | Sum | Count |
|:---:|:---|:---:|:---|:---:|:---:|
| Water | 1, 6, 11, 16, 21 | — | 1, 6, 11, 16, 21 | 55 | 5 |
| Fire | 2, 7, 12, 17 | 22 | 2, 7, 12, 17, 22 | 60 | 5 |
| Wood | 3, 8, 13, 18 | 23 | 3, 8, 13, 18, 23 | 65 | 5 |
| Metal | 4, 9, 14, 19 | 24 | 4, 9, 14, 19, 24 | 70 | 5 |
| Earth | 5, 10, 15, 20 | — | 5, 10, 15, 20 | 50 | 4 |

> Observation 9: Under the 24-number variation rule, the sums of Water, Fire, Wood, and Metal — 55, 60, 65, 70 — form an **arithmetic progression increasing by 5**. This is exactly the same property as the variation model of the original placement (21 of 1–24), confirming that it is a structural property of the 1–24 number system itself, independent of the placement.

### 7.2 Full 5 × 5 Extension Model Study

Extending to the 1–25 range and adding 25 to the Earth group yields a full 5 × 5 = 25-number extension model.

| Wuxing | Complete Extension Group | Sum |
|:---:|:---|:---:|
| Water | 1, 6, 11, 16, 21 | 55 |
| Fire | 2, 7, 12, 17, 22 | 60 |
| Wood | 3, 8, 13, 18, 23 | 65 |
| Metal | 4, 9, 14, 19, 24 | 70 |
| Earth | 5, 10, 15, 20, 25 | 75 |

The total sum of the complete 5 × 5 extension model is 55 + 60 + 65 + 70 + 75 = **325**. The Layout 2 sum of 231 is consistent with this complete extension system minus the unused numbers 22 + 23 + 24 + 25 = 94 (325 − 94 = 231).

---

## 8. Conclusion

Layout 2 is a variant that places all of 1–21 without omission in the same geometric framework as the original, and it has the following multi-layered structure.

### Summary of Key Findings

1. **Cross-palace structure — each palace sums to 54**: Excluding the center palace 15, the four palaces upper, lower, left, and right each contain 5 numbers and sum to exactly 54 (= 6 × 9). The outer total 216 corresponds to the tally number of Qian (乾之策). The strongest structural invariant of Layout 2.
2. **21-number geometric placement**: All of 1–21 used, with no omissions. Total sum 231 = 216 + 15.
3. **Cheonsu-yong-odo form**: The same geometric structure as the original, converging from the upper vertex (12) to the lower vertex (16).
4. **Vertical central axis**: 12-5-2-15-6-1-16 (sum 57). Residue pattern: Fire-Earth-Fire-Earth-Water-Water-Water.
5. **Central horizontal band**: 7 nodes at y = 2.0, sum 66.
6. **Left-right asymmetry**: Left 81 ≠ right 93 (difference 12). The original's left-right sum equality (86 = 86) does not hold; the balancing principle of Layout 2 lies in the cross-palace partition (item 1).
7. **Weight of the central horizontal band**: The y = 3.3–2.0 interval has the maximum sum, 100 (43.3% of the total).
8. **Wuxing sums**: Water 55, Fire 38, Wood 42, Metal 46, Earth 50 — Fire, Wood, Metal, and Earth form an arithmetic progression with common difference 4.
9. **Spatial bias of the wuxing**: Metal is entirely on the right; Earth appears only in the center and left.
10. **Wood group opposite-pair sums = 21**: An auxiliary observation based on the angular ordering.
11. **Arithmetic progression on full 25-number extension**: 55, 60, 65, 70, 75 (common difference 5) — identical to the original placement.
12. **No edges in the original**: This analysis is based solely on position, wuxing, and combinatorial invariants.

---

## 9. Generated Visualizations

Running `analyze_ojagakdeuk_2.py` produces the following 8 images:

- `01_original_graph_2.png` — Layout 2 original Cheonsu-yong-odo placement (wuxing colors, no edges)
- `02_wuxing_decomposition_2.png` — Wuxing subgroup decomposition
- `03_spatial_distribution_2.png` — mod 5 residue spatial distribution and phase coordinates
- `04_symmetry_analysis_2.png` — Left-center-right symmetry and sums by horizontal level
- `05_invariants_2.png` — Wuxing sums, left-center-right sums, level sums, and 5 × 5 extension counts
- `06_wuxing_relations_2.png` — Wuxing mutual-generation and mutual-overcoming relation diagram
- `07_rule_variation_model_2.png` — Complete 5 × 5 extension plus vertical layer sum distribution
- `08_position_patterns_2.png` — Sums by horizontal level and left-center-right symmetry

In addition, `mod5_residue_diagram_2.py` generates `mod5_residue_diagram_2.png`/`mod5_residue_diagram_2.svg`, and `analyze_rotations_2.py` generates `rotation_cluster_*_2.png`, `rotation_overview_2.png`, and `rotation_report_2.txt`.
