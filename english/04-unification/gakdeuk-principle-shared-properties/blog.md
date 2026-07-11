# What Is the Gakdeuk (各得) Principle? A Structure Uniting Gu, O, Yuk, Chil, and Paljagakdeuk

The Gakdeuk (各得) puzzles handed down in the *Gusuryak (九數略)* tradition are diagrams in which several subsets are arranged so that each one “obtains” the same sum. Gujagakdeuk (9), Ojagakdeuk (5), Yukjagakdeuk (6), Chiljagakdeuk (7), and Paljagakdeuk (8) — the number in each name indicates the size of each subset.

## Core Question: What Do These Puzzles Share?

### 1. All Have Five Subsets

The first common feature of the Gakdeuk family is that there are **five subsets**. Spatially, they follow a cruciform layout:

```
        Up
         │
    Left ─ Center ─ Right
         │
       Down
```

Why five? Five is the number of the Wuxing (Water, Fire, Wood, Metal, Earth) and also the number of the five directions: the four cardinal directions plus the center. Thus, Gakdeuk puzzles can be seen as expressing a **traditional cosmological spatial model** in numbers, going beyond a mere mathematical puzzle.

### 2. Every Subset Has the Same Sum

The core rule of Gakdeuk puzzles is that **“each one obtains.”**

| Family | Subset size | Subset sum |
|:---:|:---:|:---:|
| Ojagakdeuk | 5 | 65 |
| Yukjagakdeuk | 6 | 63 |
| Chiljagakdeuk | 7 | 120 |
| Paljagakdeuk | 8 | 164 |
| Gujagakdeuk | 9 | 207 |

This sum is not an arbitrary number but the average of the used numbers multiplied by the subset size. For example, in Paljagakdeuk the average of 1–40 is 20.5, and 20.5 × 8 = 164.

### 3. The Center Acts as the Core

In every family, the **central subset** is the key to the whole structure.

- Yukjagakdeuk: the 6 vertices of the central hexagon are all shared vertices.
- Paljagakdeuk · Gujagakdeuk: the central palace connects the four directional palaces through the grid.
- Chiljagakdeuk: the central cluster is arranged together with the four directions.

Removing the center causes the remaining four subsets to fall apart; this structure is repeated in every family.

### 4. Wuxing mod 5 Arithmetic Progression

If numbers are classified into Water, Fire, Wood, Metal, and Earth by their remainder modulo 5, the sum of each Wuxing group forms an arithmetic progression.

| Family | Wuxing sums |
|:---|:---|
| Yukjagakdeuk | 34, 38, 42, 46, 50 |
| Paljagakdeuk | 148, 156, 164, 172, 180 |
| Gujagakdeuk | 189, 198, 207, 216, 225 |

The common difference equals the number of elements in each Wuxing group. This is an inevitable pattern when 1, 2, 3, … are grouped in fives.

### 5. Controlling Relationships Dominate the Wuxing Connections

When connections between subsets are viewed as Wuxing relationships, **controlling (相剋)** relationships appear most frequently.

- Yukjagakdeuk: controlling 50%
- Paljagakdeuk: controlling 55.8%
- Gujagakdeuk: controlling 40.3%

This shows that Gakdeuk puzzles visualize not just simple harmony but **tension and constraint among the Wuxing**.

## Individual Character of Each Family

### Ojagakdeuk (Cheonsuyongodo): A Sum Invariant inside Geometry

Ojagakdeuk has also been confirmed to have five subsets each summing to **65**. Since 5×65 = 325 and the sum of the 21 used numbers is 265, the duplication sum of the shared vertices is 60. In addition, positional invariants such as **left-right symmetric sum = 86** exist.

### Chiljagakdeuk: Center-Periphery Split

Chiljagakdeuk consists of 1 center + 6 periphery numbers. It is distinctive in that the centers `{1, 2, 3, 4, 5}` form a complete residue system modulo 5.

### Gujagakdeuk · Paljagakdeuk: The 3×3 Grid Family

Both are based on a 3×3 grid. Gujagakdeuk uses all nine cells, while Paljagakdeuk uses the eight peripheral cells excluding the center. Strong positional invariants are found in the corner and edge-midpoint sums.

## Generalization: The Formulas of Gakdeuk Puzzles

Abstracting a Gakdeuk puzzle gives:

```
5 subsets, each with n vertices
Every subset sum = S
Total sum of all numbers = T
Amount counted by duplication = D
5·S = T + D
```

- If subsets share no vertices: D = 0
- If subsets share vertices: D > 0
- If duplicated numerical values appear as in Chiljagakdeuk: D equals the sum of those duplicated values

The general formula for Wuxing sums is:

```
WX(r) = 5·m(m−1)/2 + m·r    (r = 1, 2, 3, 4, 5)
```

where `m` is the number of elements in each Wuxing group.

---

## Appendix: N-Gakdeuk Solver

This folder includes a Python + PuLP MILP solver that automatically finds Gakdeuk puzzles given only `n`. It can be run in a virtual environment without SageMath.

```bash
source venv/bin/activate
python gakdeuk_solver.py --all --time-limit 180 --max-solutions 1 --visualize --output solutions.json
```

This solver handles geometric and Wuxing constraints all at once:

1. **Geometric sharing constraint**: shared vertices occur only between adjacent clusters. It provides built-in adjacency graphs for `cross` (cruciform), `honeycomb` (hexagonal beehive), and `grid` (3×3 grid), and also allows custom adjacent pairs.
2. **Pairwise shared vertex counts**: for example, one can force the center-up pair to share 2 vertices and the center-left pair to share 2 vertices. This reproduces the detailed geometric structure of Jisuyongyukdo or Cheonsuyongodo.
3. **Up/down / left/right residue symmetry**: the `--symmetry ud|lr|both` option makes the mod 5 remainder distribution symmetric across clusters, numerically reflecting the left-right or up-down mirror symmetry of traditional diagrams.
4. **mod 5 remainder (Wuxing) equivalence-class constraint**: `--residue-balance` encourages each cluster’s Wuxing distribution to be balanced against the overall distribution.

The solver also **saves solutions as JSON** (`--output`) and generates **matplotlib visualizations** (`--visualize`) in one step. Multiple valid placements can be enumerated with `--max-solutions`.

```bash
# Yukjagakdeuk-like: honeycomb adjacency + pairwise shared vertex counts + up-down symmetry
python gakdeuk_solver.py --n 6 --max 20 --sum 63 \
    --adjacency honeycomb --pair-shared-counts "0-1:2,0-2:2,0-3:2,0-4:2" \
    --symmetry ud --residue-balance --visualize

# Search, save, and visualize all known families at once
python gakdeuk_solver.py --all --time-limit 180 \
    --max-solutions 1 --visualize --output solutions.json
```

This finds Gakdeuk-principle-following solutions for Ojagakdeuk, Yukjagakdeuk, Chiljagakdeuk, Paljagakdeuk, and Gujagakdeuk, and records them in `solutions.json` and `viz_*.png` files.

## Conclusion

Although the Gakdeuk families differ in size and shape, they share the following five principles:

1. **Five subsets + central core**
2. **Sum invariant**
3. **Duplication equation `5·S = T + D`**
4. **Wuxing mod 5 arithmetic progression**
5. **Controlling-dominant Wuxing relationships**

These principles show the meeting point of traditional numerology with modern combinatorics and graph theory, and reveal Gakdeuk puzzles not as mere mental arithmetic games but as **diagrams exploring the harmony of numbers and space**.
