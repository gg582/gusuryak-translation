# Modern Combinatorial Definition of the Hado Chilodo (七子各得)

## 1. Objects

- **5 clusters** in a cross: top, left, centre, right, bottom
- **Centre** of each cluster: one of 1–5, placed as in the Hetu (2 top, 3 left, 5 centre, 4 right, 1 bottom)
- **Six vertices** of each hexagon; top and bottom hexagons have a vertex at the top, the others an edge at the top
- **Labels**: 1–35, each used once

## 2. Definition

A Chilodo is a map `L: V → {1,…,35}`, bijective on the 35 positions, such that for every cluster `c`

```
L(centre(c)) + Σ_{v ∈ ring(c)} L(v) = 126.
```

The constant is forced: 1 + … + 35 = 630 = 5 × 126.

## 3. mod-5 structure

With `r(n) = n mod 5` and complement `σ(n) = 36 − n`, we have `r(σ(n)) ≡ 1 − r(n)`. The involution σ has three orbit types on phases: Water–Earth, Fire–Metal, Wood–Wood.

The printed solution satisfies a stronger condition than the sum alone:

- the left cluster is exactly the Wood class `{3, 8, …, 33}`, which is σ-closed with fixed point 18;
- each of the other four clusters contains two σ-pairs of a single type (Fire–Metal at top and right, Water–Earth at centre and bottom) and three further numbers summing to 54.

Class sums: Water 112, Fire 119, Wood 126, Metal 133, Earth 140.

## 4. Open problems

1. **Counting.** How many bijections satisfy the sum condition alone? How many also satisfy the σ-pair condition of §3?
2. **Uniqueness of the remainder.** Is the split of the twelve unpaired numbers into four triples of sum 54 forced by the pair condition?
3. **Generalisation.** For the Hado family with q numbers per cluster and C = 5q + 1, when does a solution exist with the Saodo pair assignment?
