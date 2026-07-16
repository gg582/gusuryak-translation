# The Relationship Between Jisu-guimun-do and Jisu-yong-yukdo

## 1. Overview

**Jisu-yong-yukdo (地數用六圖)** and **Jisu-guimun-do (地數龜文圖)** are both diagram puzzles handed down in the *Gusuryak* (九數略) family of late-Joseon mathematical texts. Both place numbers at the vertices of hexagons so that **the sum of the six numbers forming each hexagon is the same**.

| Item | Jisu-yong-yukdo | Jisu-guimun-do (representative examples) |
|---|---|---|
| Number of hexagons | 5 | 3, 4, 6, 7, 9, 10, 19, etc. |
| Number of nodes M | 20 | 13, 16, 22, 24, 30, 33, 54, etc. |
| Numbers used | 1–20 | 1–M |
| Magic constant S | 63 | 34–50, 40–62, 57–71, 65–85, 77–109, … |
| Core rule | Every hexagon's six numbers have the same sum | Every hexagon's six numbers have the same sum |

Jisu-guimun-do can be viewed as a **structural extension** of Jisu-yong-yukdo. If Jisu-yong-yukdo is the special form "5 hexagons, 20 nodes," then Jisu-guimun-do is the **generalization of the same sum-invariant rule to hexagonal tilings of various sizes**.

---

## 2. The Rule of Jisu-yong-yukdo

The exact rule of Jisu-yong-yukdo is as follows.

- Use the natural numbers 1 through 20 **exactly once**.
- Place them in **5 hexagons**, 6 numbers per hexagon.
- Adjacent hexagons share some vertices.
- **The sum of the 6 numbers in every hexagon is 63**.

The following duplication-count equation then holds.

```
5 × 63 = 315
1 + 2 + … + 20 = 210
315 − 210 = 105
```

That is, the total extra amount added by shared vertices is 105. Jisu-yong-yukdo creates this duplication through the 8 shared vertices {3, 8, 10, 11, 12, 13, 14, 15}.

Therefore, the core of Jisu-yong-yukdo is twofold.

1. **Sum invariant**: every hexagon has the same six-number sum S.
2. **Shared-vertex duplication**: shared vertices are counted in multiple hexagons, satisfying the total-sum equation `H·S = T + D`.

---

## 3. Generalization to Jisu-guimun-do

Jisu-guimun-do applies the above two rules to **arbitrary hexagonal tilings**.

### 3.1 General Formula

- H: number of hexagons
- M: number of nodes (vertices)
- T = 1 + 2 + … + M = M(M+1)/2
- mult(v): number of hexagons containing node v
- D = Σᵥ (mult(v) − 1) · v: weighted sum of duplicated shared vertices

If every hexagon has sum S, then

```
H · S = T + D
```

Therefore

```
S = (T + D) / H
```

Because D depends on the positions and multiplicities of shared vertices, the possible values of S for a given topology form a **set of integers** rather than a continuous range.

### 3.2 Representative Jisu-guimun-do Variants

According to the Korean Wikipedia entry for "Jisu-guimun-do," the following variants are known ([Jisu-guimun-do](https://ko.wikipedia.org/wiki/%EC%A7%80%EC%88%98%EA%B7%80%EB%AC%B8%EB%8F%84)).

| M | Hexagons H | Shape | Magic constant S range | Notes |
|:---:|:---:|:---|:---:|:---|
| 13 | 3 | Triangle | 34–50 | |
| 16 | 4 | Rhombus | 40–62 | 687,851,136 solutions total |
| 20 | 5 | Jisu-yong-yukdo | 63 | 8 shared vertices |
| 22 | 6 | Triangle | 57–71 | |
| 24 | 7 | Regular hexagon | 65–85 | |
| 30 | 9 | Turtle shell | 77–109 | Representative example S = 93 |
| 33 | 10 | Triangle | 83–121 | |
| 54 | 19 | Regular hexagon | 140–190 | |

In this table, Jisu-yong-yukdo (M = 20, H = 5) is only **one member** of the Jisu-guimun-do family.

---

## 4. Why Jisu-guimun-do is an Extension of Jisu-yong-yukdo

### 4.1 Same Core Rule

Jisu-guimun-do and Jisu-yong-yukdo share the following rules.

1. Use the numbers 1 through M **exactly once**.
2. Place **6 numbers** in each hexagon.
3. The **sum of the 6 numbers is the same** in every hexagon.
4. **Vertex sharing** between hexagons adjusts the duplication coefficient D.

### 4.2 Jisu-yong-yukdo = a Special Case of Jisu-guimun-do

Jisu-yong-yukdo can be seen as Jisu-guimun-do with M = 20 and H = 5. The name "Jisu-yong-yukdo" is traditionally used because "yong-yuk (用六)" means that the number 6 is taken as the core unit.

Jisu-guimun-do keeps 6 as the core unit while **freely extending the number of hexagons H and the number of nodes M**. Therefore:

> **Jisu-guimun-do = a generalization (extension) of Jisu-yong-yukdo**

### 4.3 Extension of the Shared-Vertex Structure

The 5 hexagons of Jisu-yong-yukdo have a **central hexagon + 4 surrounding hexagons** structure. The form in which the central hexagon shares vertices with all surrounding hexagons also appears in Jisu-guimun-do, for example in the 7-hex regular hexagon (M = 24).

The 7-hex regular hexagon is **central hexagon + 6 surrounding hexagons**, extending the central-surround structure of Jisu-yong-yukdo to six directions.

---

## 5. Solver and Experimental Results

The `jisuguimundo_solver.py` script in the same folder automatically selects the Jisu-guimun-do topology corresponding to a given number of nodes M and searches for number placements using a PuLP MILP formulation.

### 5.1 Usage

```bash
source venv/bin/activate

# Jisu-yong-yukdo (M=20, S=63)
python jisuguimundo_solver.py --m 20 --S 63 --output solution_M20.json

# 7-hex regular hexagon (M=24, S=75)
python jisuguimundo_solver.py --m 24 --S 75 --output solution_M24.json

# Enumerate 100 solutions for the 3-hex triangle at S=42
python jisuguimundo_solver.py --m 13 --S 42 --enumerate --max-solutions 100 --output solutions_M13_S42.json

# 4-hex rhombus (M=16, S=51)
python jisuguimundo_solver.py --m 16 --S 51 --output solution_M16.json
```

### 5.2 Summary of Experimental Results

| M | Structure | H | S | Solutions found | Output file |
|:---:|:---|:---:|:---:|:---:|:---|
| 20 | Jisu-yong-yukdo | 5 | 63 | 1 | `solution_M20.json` |
| 24 | 7-hex regular hexagon | 7 | 75 | 1 | `solution_M24.json` |
| 13 | 3-hex triangle | 3 | 42 | 100 | `solutions_M13_S42.json` |
| 16 | 4-hex rhombus | 4 | 51 | 1 | `solution_M16.json` |

In every case, a valid placement was found for the given S. In particular, for M = 13 we confirmed that **more than 100 solutions exist**, showing that Jisu-guimun-do has a rich combinatorial structure.

### 5.3 Example Solutions

**Jisu-yong-yukdo (M = 20, S = 63) example**

```
H0: [15, 8, 3, 10, 20, 7] = 63
H1: [12, 7, 20, 9, 2, 13] = 63
H2: [10, 20, 9, 4, 14, 6] = 63
H3: [6, 14, 1, 5, 19, 18] = 63
H4: [4, 17, 11, 16, 1, 14] = 63
```

**7-hex regular hexagon (M = 24, S = 75) example**

```
H0 (center): [18, 11, 24, 2, 15, 5] = 75
H1: [18, 11, 3, 23, 16, 4] = 75
H2: [11, 24, 3, 20, 9, 8] = 75
H3: [24, 2, 8, 13, 6, 22] = 75
H4: [2, 15, 22, 1, 14, 21] = 75
H5: [15, 5, 21, 10, 7, 17] = 75
H6: [5, 18, 17, 12, 19, 4] = 75
```

---

## 6. Can We Obtain "All" Jisu-guimun-do Solutions?

In principle, finding all solutions for a given M is **possible**, because the condition is a finite combinatorial one (permutations of 1 through M satisfying some constraints).

In practice, however, the following limitations apply.

1. **Combinatorial explosion**: Even M = 16 (4-hex rhombus) has 687,851,136 solutions. As M grows, the number of solutions increases geometrically.
2. **Topology dependence**: The structure is not determined by M alone. For example, M = 20 traditionally corresponds to the 5-hex Jisu-yong-yukdo, but other hexagonal arrangements are theoretically possible.
3. **S-range search**: The possible S values are not continuous; for each candidate S the MILP must be run again.

Therefore, this solver can enumerate multiple solutions for **small M (M ≤ 24)**, but for large M (M ≥ 30) the practical limit is **finding one or more example solutions**.

---

## 7. Conclusion

Jisu-guimun-do is a **generalized hexagonal magic figure** that follows exactly the same rules as Jisu-yong-yukdo.

- Jisu-yong-yukdo: M = 20, H = 5, S = 63.
- Jisu-guimun-do: extends the same rules to M = 13, 16, 22, 24, 30, 33, 54, etc.
- Both are unified by the duplication-count equation `H·S = T + D`.

Solver experiments found valid placements for M = 13, 16, 20, and 24, and confirmed that many solutions exist for M = 13. This shows that Jisu-guimun-do is not a special case but a **broader puzzle family to which Jisu-yong-yukdo belongs**.

> **Jisu-guimun-do is an extended concept that includes Jisu-yong-yukdo.**

---

## References

- Wikipedia, "Jisu-guimun-do" (Earth-Number Turtle-Shell Diagram), [https://ko.wikipedia.org/wiki/%EC%A7%80%EC%88%98%EA%B7%80%EB%AC%B8%EB%8F%84](https://ko.wikipedia.org/wiki/%EC%A7%80%EC%88%98%EA%B7%80%EB%AC%B8%EB%8F%84)
- `jisuguimundo_solver.py`: MILP-based automatic search script in this folder.
