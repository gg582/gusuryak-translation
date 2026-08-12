# yukgodo2 — consecutive ring-value reconstruction results

## Arithmetic chain (text-supported part, Z3-verified)

```
逓加: 6 + 12 + … + 54 = 270 = 6 × 45
六包一 series: 1 + (6 + 12 + … + 54) = 271
來積法: 54 + 6 = 60, 60 ÷ 6 = 10, 2 × 10 − 1 = 19
        (10 + 18) × 9 = 252, 252 + 19 = 271
虛一: 271 − 1 = 270
```

## Placement by ring (reconstruction hypothesis)

| ring k | cells 6k | value range | ring sum 18k³+3k |
| ---: | ---: | --- | ---: |
| 1 | 6 | 1..6 | 21 |
| 2 | 12 | 7..18 | 150 |
| 3 | 18 | 19..36 | 495 |
| 4 | 24 | 37..60 | 1164 |
| 5 | 30 | 61..90 | 2265 |
| 6 | 36 | 91..126 | 3906 |
| 7 | 42 | 127..168 | 6195 |
| 8 | 48 | 169..216 | 9240 |
| 9 | 54 | 217..270 | 13149 |

## Verification

- grid cells = 271 (central void 1 + occupied 270)
- values 1..270 are each placed exactly once
- every ring's value set matches its consecutive interval exactly
- every ring sum matches 18k³+3k exactly

## Interpretive boundary

This arrangement is a separate candidate from the antipodal-complement hypothesis (ring sums 813k). The starting point and direction of each ring are a normalization of rotational symmetry; there is no evidence that the text directly prescribes this value placement. The alignment with the 六包一 series only strengthens the cell-count arithmetic.
