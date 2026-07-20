# Corrected Huchaek-yong-gudo Analysis

This note distinguishes the original reconstruction from the numerically
complete corrected edition. The original reconstruction is also read as a
diagram following the LibreWiki Huchaek-yong-gudo rule. It is conservative in a
specific sense: it prioritizes the visible diagrammatic form and the displayed
local pair sums, rather than forcing every numerical condition at once.

The corrected edition is a separate edition that keeps the same construction
rule but enforces the full numerical conditions.

## 1. Rule Applied

The core rule is expressed by two pair-sum classes.

```text
octagon: 73 x 4 = 292
square: 74 + 72 = 146
```

Across the 3x3 working units there are 36 side pairs. Since the values are
1..72, their total is:

```text
1 + ... + 72 = 2628
```

For the side-pair sums to match this total, the balanced distribution is:

```text
18 pairs summing to 73
9 pairs summing to 74
9 pairs summing to 72
18x73 + 9x74 + 9x72 = 2628
```

The displayed sums in the original reconstruction have distribution `73` x 17,
`74` x 11, and `72` x 8, whose total is 2631. This cannot simultaneously be the
sum of 1..72. The corrected edition therefore uses the balanced `18/9/9`
distribution required by the Huchaek-yong-gudo rule.

## 2. Correction Principle

The corrected edition was obtained by solving for a placement satisfying all of
the following conditions:

- use 1..72 exactly once;
- make every side pair sum to one of `73`, `74`, or `72`;
- make every working octagon unit sum to 292;
- preserve as many original-reconstruction position values as possible.

The optimum keeps 61 of the 72 position values unchanged.

## 3. Changed Positions

| position | side | original reconstruction | corrected | target sum |
|---|---|---:|---:|---:|
| row 1 col 1 | left | (33,45) | (32,42) | 74 |
| row 1 col 2 | bottom | (64,4) | (69,4) | 73 |
| row 1 col 3 | top | (73,1) | (72,1) | 73 |
| row 2 col 1 | top | (18,55) | (20,53) | 73 |
| row 2 col 1 | left | (19,56) | (19,55) | 74 |
| row 2 col 1 | right | (54,20) | (54,18) | 72 |
| row 3 col 1 | top | (11,62) | (17,56) | 73 |
| row 3 col 1 | right | (42,25) | (47,25) | 72 |

This changes 11 individual position values, grouped into 8 adjusted side pairs.

## 4. Corrected Rule Check

The corrected side-pair sum distribution is:

```text
72: 9
73: 18
74: 9
```

Every working octagon unit sums to 292.

| position | top+bottom | left+right | total |
|---|---:|---:|---:|
| row 1 col 1 | 146 | 146 | 292 |
| row 1 col 2 | 146 | 146 | 292 |
| row 1 col 3 | 146 | 146 | 292 |
| row 2 col 1 | 146 | 146 | 292 |
| row 2 col 2 | 146 | 146 | 292 |
| row 2 col 3 | 146 | 146 | 292 |
| row 3 col 1 | 146 | 146 | 292 |
| row 3 col 2 | 146 | 146 | 292 |
| row 3 col 3 | 146 | 146 | 292 |

The corrected edition also uses 1..72 exactly once.

## 5. Interpretation

In the corrected edition, each working octagon has two `73 + 73` axes and one
`74 + 72` axis:

```text
(73 + 73) + (74 + 72) = 292
```

This shows how the diagonal-pair complement sum 73 and the square-side
adjustment `74/72` operate together in the same diagram. The corrected edition
is therefore not an arbitrary sum-fitting arrangement; it is a numerically
complete edition of the construction rule described for Huchaek-yong-gudo.
