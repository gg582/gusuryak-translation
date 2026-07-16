# Π(5, q, T): A 5-ary Direction-Weighted Puzzle Framework for Saodo and Chiljagakdeuk

> This post redefines two traditional diagrams—Saodo and Chiljagakdeuk—in modern combinatorial and discrete-mathematical language, and shows how both fit inside a single parameterized family `Π(5, q, T)`. Cultural or rhetorical interpretations are excluded; the focus is on observable data and mathematical structure.

---

## 1. Source Data of the Two Puzzles

### Saodo 5-coloring diagram

```text
        19  2
        7  14
13  8   5   16  4   17
18  3   11  10  12   9
        15  1
        6  20
```

- 20 circular marks.
- Total sum `Σ = 210`.
- Five color classes (Water, Fire, Wood, Metal, Earth), four elements each.
- Color rule: `c(v) = L(v) mod 5` (with 0 replaced by 5).

### Chiljagakdeuk (七子各得)

| Cluster | Center | Peripheral slots | Sum |
|---|---|---|---|
| C₁ (top) | 2 | 29, 1, 24, 34, 11, 19 | 120 |
| C₂ (left) | 3 | 6, 33, 23, 13, 34, 8 | 120 |
| C₃ (center) | 5 | 22, 7, 20, 30, 26, 10 | 120 |
| C₄ (right) | 4 | 15, 28, 9, 18, 32, 14 | 120 |
| C₅ (bottom) | 1 | 35, 16, 21, 24, 6, 17 | 120 |

- 5 clusters, 7 elements each (1 center + 6 peripheral slots).
- Per-cluster sum `T = 120`.
- Center set `{1,2,3,4,5}` forms a complete residue system modulo 5.

---

## 2. Extracting a Common Skeleton

Comparing the two diagrams reveals the following shared structure.

1. **Five directions**: Saodo's five color classes correspond to Chiljagakdeuk's five clusters.
2. **Mod-5 residue classification**: both puzzles rely on a modulo-5 partition.
3. **Weight function**: each element is assigned a natural-number label.
4. **Sum invariant**: Saodo has global sum 210; Chiljagakdeuk has per-direction sum 120.
5. **Geometric placement**: the positions of the circular marks are part of the data.

Differences are also clear. Chiljagakdeuk has an explicit center-periphery split and connecting edges, while Saodo has no edges and no explicit center concept in the original text.

---

## 3. General Framework `Π(p, q, T)`

The following definition captures both puzzles.

```text
Π = (D, M, X, E, K, S, W, Φ)
```

| Symbol | Meaning |
|---|---|
| `D` | Direction set, `|D| = p` |
| `M` | Element / mark set |
| `X` | Geometric placement `X: M → ℝ²` |
| `E` | Edge set `E ⊆ M × M` |
| `K` | Direction-center correspondence `K: D → M` |
| `S` | Per-direction peripheral slots `S: D → 2^M` |
| `W` | Weight function `W: M → ℕ` |
| `Φ` | Invariant conditions |

This collapses to three positive-integer parameters:

```text
Π(p, q, T)
```

- `p`: number of directions.
- `q`: number of peripheral slots per direction.
- `T`: target sum per direction.

The two puzzles map as follows.

| Puzzle | p | q | T |
|---|---|---|---|
| Chiljagakdeuk | 5 | 6 | 120 |
| Saodo (color classes) | 5 | 3 | 34, 38, 42, 46, 50 |

---

## 4. Following Verdict

Applying Chiljagakdeuk's strict rule to Saodo gives the following.

| Level | Condition | Saodo satisfies? |
|---|---|---|
| 0 | `p = 5` directional structure | Yes |
| 1 | Center-periphery split possible | Yes (3 peripheral slots) |
| 2 | `q = 6` | No |
| 3 | All direction sums equal `T` | No |
| 4 | Explicit center-periphery edges | No |

Thus Saodo shares the **weak skeleton** of Chiljagakdeuk but not its **strong structure**. It is best viewed as a non-uniform parameter setting inside the same family `Π(5, q, T)`.

---

## 5. Key Mathematical Constraints

### 5.1 Mod-5 residue completeness

Both puzzles have five centers forming a complete residue system of `ℤ/5ℤ`.

```text
{1, 2, 3, 4, 5}  →  residues {1, 2, 3, 4, 0}
```

### 5.2 Sum invariants

- Saodo: `Σ_{v∈M} W(v) = 210 = 1 + 2 + … + 20`.
- Chiljagakdeuk: `∀d ∈ D, W(K(d)) + Σ_{s∈S(d)} W(s) = 120`.

### 5.3 Duplication and placement

- Saodo: all 20 numbers are distinct.
- Chiljagakdeuk: 1, 6, 24, 34 each appear twice; 31 distinct values.

### 5.4 Geometry

- Saodo: symmetric cross, row sizes `2, 2, 6, 6, 2, 2`.
- Chiljagakdeuk: five star configurations arranged in a cross; each star is a center plus hexagonal periphery.

---

## 6. Python Code

The following code verifies the core conditions of both puzzles.

```python
#!/usr/bin/env python3
"""
Compare Saodo and Chiljagakdeuk within Π(p, q, T).
"""

# Saodo color classes
SAODO = {
    "water": [1, 6, 11, 16],
    "fire":  [2, 7, 12, 17],
    "wood":  [3, 8, 13, 18],
    "metal": [4, 9, 14, 19],
    "earth": [5, 10, 15, 20],
}

# Chiljagakdeuk clusters
CHILJA = {
    "top":    {"center": 2,  "periphery": [29, 1, 24, 34, 11, 19]},
    "left":   {"center": 3,  "periphery": [6, 33, 23, 13, 34, 8]},
    "center": {"center": 5,  "periphery": [22, 7, 20, 30, 26, 10]},
    "right":  {"center": 4,  "periphery": [15, 28, 9, 18, 32, 14]},
    "bottom": {"center": 1,  "periphery": [35, 16, 21, 24, 6, 17]},
}


def residue(value):
    return ((value - 1) % 5) + 1


def check_chiljagakdeuk():
    centers = [d["center"] for d in CHILJA.values()]
    sums = [d["center"] + sum(d["periphery"]) for d in CHILJA.values()]
    qs = [len(d["periphery"]) for d in CHILJA.values()]
    return {
        "p": len(CHILJA),
        "centers_complete": sorted(residue(c) for c in centers) == [1, 2, 3, 4, 5],
        "q_uniform": all(q == 6 for q in qs),
        "sum_uniform": len(set(sums)) == 1,
        "T": sums[0] if len(set(sums)) == 1 else None,
    }


def check_saodo():
    centers = [min(v) for v in SAODO.values()]
    sums = [sum(v) for v in SAODO.values()]
    qs = [len(v) - 1 for v in SAODO.values()]
    return {
        "p": len(SAODO),
        "centers_complete": sorted(residue(c) for c in centers) == [1, 2, 3, 4, 5],
        "q_uniform": all(q == qs[0] for q in qs),
        "q": qs[0],
        "sum_uniform": len(set(sums)) == 1,
        "sums": sorted(sums),
    }


if __name__ == "__main__":
    print("Chiljagakdeuk:", check_chiljagakdeuk())
    print("Saodo:        ", check_saodo())
```

Output:

```text
Chiljagakdeuk: {'p': 5, 'centers_complete': True, 'q_uniform': True, 'sum_uniform': True, 'T': 120}
Saodo:         {'p': 5, 'centers_complete': True, 'q_uniform': True, 'q': 3, 'sum_uniform': False, 'sums': [34, 38, 42, 46, 50]}
```

---

## 7. Open Problems

1. Existence conditions for `Π(p, q, T)`: for which triples of positive integers does a puzzle exist?
2. Uniformization of Saodo: can the 20 marks be rearranged into 5 clusters of 7 with a constant sum, while preserving the 5-coloring and geometric constraints?
3. If no per-direction sum invariant exists, what additional algebraic or combinatorial conditions are needed?
4. What graph structure arises if a minimal edge set `E` is added to Saodo?

---

## 8. Related Artifacts

This post synthesizes results from the following projects.

- `01-saodo-family/hado-saodo-5-coloring/`
  - `figures/modern_redefinition.en.md`
  - `docs/detailed_analysis.en.md`
  - `docs/explanation.en.md`
  - `figures/math_problems.en.md`
  - `docs/report.en.md`
- `02-gakdeuk-series/chiljagakdeuk-seven-each-gets/`
  - `modern_redefinition.en.md`
  - `report.en.md`
- `04-unification/saodo-chiljagakdeuk-generalization/`
  - `docs/generalization.en.md`
  - `compare_structures.py`

---

## 9. Closing

Saodo and Chiljagakdeuk may look like unrelated diagrams, but they can both be understood as different instances of the same family `Π(5, q, T)`. Chiljagakdeuk is the strict uniform case `Π(5, 6, 120)`, while Saodo is the non-uniform case `Π(5, 3, T_d)`. By translating traditional diagrams into modern combinatorial language, we move beyond interpretation and obtain precise mathematical problems and generalizations.
