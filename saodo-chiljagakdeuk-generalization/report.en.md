# Integrated Report: Generalization of Saodo and Chiljagakdeuk

**Date**: 2026-07-07

---

## 1. Overview

This report unifies the Hado (Saodo) puzzle and the Chiljagakdeuk puzzle within a single abstract framework `Π(p, q, T)`, and formally analyzes to what extent Saodo follows the structural rule of Chiljagakdeuk.

---

## 2. General Framework

Definition encompassing both puzzles:

```
Π = (D, M, X, E, K, S, W, Φ)
```

| Symbol | Meaning |
|---|---|
| `D` | Direction set (5 elements) |
| `M` | Element / mark set |
| `X` | Geometric placement |
| `E` | Edge set |
| `K` | Direction-center correspondence |
| `S` | Per-direction peripheral slots |
| `W` | Weight function (numeral label) |
| `Φ` | Invariant conditions |

Parameterized puzzle family:

```
Π(p, q, T)
```

- `p`: number of directions
- `q`: number of peripheral slots per direction
- `T`: target sum per direction

---

## 3. Parameter Mapping of the Two Puzzles

| Puzzle | p | q | T |
|---|---|---|---|
| Chiljagakdeuk | 5 | 6 | 120 (same for all directions) |
| Saodo (color classes) | 5 | 3 | 34, 38, 42, 46, 50 (direction-dependent) |

---

## 4. Step-by-Step Following Verdict

| Level | Condition | Saodo satisfies? |
|---|---|---|
| 0 | 5-direction structure | Yes |
| 1 | Center-periphery split possible | Yes (3 periphery slots) |
| 2 | Peripheral slot count = 6 | No |
| 3 | Per-direction sum invariant | No |
| 4 | Explicit edges | No |

---

## 5. Conclusion

- Saodo shares the **weak skeleton** of Chiljagakdeuk: five directions, mod-5 residues, complete residue system of centers, and a global sum invariant.
- However, it does **not** follow the **strong structure**: six peripheral slots, constant per-direction sum, and explicit edges.
- Therefore, the statement "Saodo follows the rule of Chiljagakdeuk" is strictly false; it is best viewed as a non-uniform parameter setting within the same family.

---

## 6. Generated Documents and Code

- `docs/generalization.ko.md` / `generalization.en.md`: Generalized definition and following verdict
- `report.ko.md` / `report.en.md`: Integrated report
- `compare_structures.py`: Verification script for structural conditions of both puzzles

## 7. Verification Script Output

Output of `compare_structures.py`:

- Chiljagakdeuk: 5 directions, centers `{1,2,3,4,5}`, 6 peripheral slots each, all cluster sums equal 120.
- Saodo: centers `{1,2,3,4,5}` form a complete mod-5 residue system, but each class has only 3 peripheral slots and cluster sums are 34/38/42/46/50.
- Thus Saodo is confirmed to be a non-uniform parameter setting `Π(5, 3, T_d)`.
