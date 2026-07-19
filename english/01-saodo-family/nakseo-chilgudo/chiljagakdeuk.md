# Reading Nakseo Chilgudo as Chiljagakdeuk

`Nakseo Chilgudo (洛書七九圖)` is a nine-palace diagram. Each palace contains seven numbers, and the source constraint is that **each palace sums to 224**.

The center layout is the classical Luoshu nine-palace pattern.

```text
4  9  2
3  5  7
8  1  6
```

The six surrounding numbers are listed **clockwise from the 12 o'clock position**.

## OCR Reading and Rule-Based Reconstruction

In the table below, `reconstructed` marks values changed by `reconstruct_milp.py` because the OCR reading conflicts with the source constraints.

Hard constraints:

- The seven numbers in every palace sum to 224.
- The integers 1 through 63 are used exactly once.

| Palace | Center | Six surrounding numbers clockwise from 12 o'clock | Sum |
|---|---:|---|---:|
| Upper-left | 4 | 31, 43, **22**(reconstructed: OCR 12), 60, 27, 37 | 224 |
| Upper-center | 9 | 15, 45, **36**(reconstructed: OCR unclear), 55, 10, 54 | 224 |
| Upper-right | 2 | 28, 29, 39, 62, 17, 47 | 224 |
| Middle-left | 3 | 30, 40, **26**(reconstructed: OCR 36), 61, 16, 48 | 224 |
| Center | 5 | 32, 41, 23, 59, 14, 50 | 224 |
| Middle-right | 7 | 34, **38**(reconstructed: OCR unclear), 24, 57, 20, 44 | 224 |
| Lower-left | 8 | 35, 49, 12, **56**(reconstructed: OCR unclear), 11, 53 | 224 |
| Lower-center | 1 | 52, 25, 19, 63, **18**(reconstructed: OCR 68), **46**(reconstructed: OCR 48) | 224 |
| Lower-right | 6 | 33, 42, 21, 58, 13, **51**(reconstructed: OCR 23) | 224 |

## MILP Reconstruction

The reconstruction script is [reconstruct_milp.py](/home/yjlee/gusuryak-translation/english/01-saodo-family/nakseo-chilgudo/reconstruct_milp.py). Its objective keeps OCR readings whenever possible and changes only the lowest-cost OCR-confusion candidates needed to satisfy the constraints.

The reconstructed nine palaces satisfy these invariants.

| Quantity | Value |
|---|---:|
| Values used | 1-63 |
| Positions | 9 palaces x 7 numbers = 63 |
| Sum per palace | 224 |
| Total of palace sums | 224 x 9 = 2016 |
| Plain total | 1+2+...+63 = 2016 |

Thus the diagram is a 63-position partition with no duplication.

## Visualization

[visualize_basic.py](/home/yjlee/gusuryak-translation/korean/01-saodo-family/낙서칠구도/visualize_basic.py) draws the reconstructed values. Gray cells are not direct OCR readings; they are reconstructed from the rules `sum per palace = 224` and `use 1-63 exactly once`.

## Summary

- The source constraint is that each seven-number palace sums to 224.
- The OCR reading alone breaks that constraint in several palaces, so rule-based reconstruction is required.
- The MILP reconstruction satisfies both the 224 palace sums and the non-overlapping use of 1-63.
