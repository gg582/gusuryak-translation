# Reading Paljagakdeuk as Modern Mathematics: 40 Numbers, Five Palaces, and 164

Paljagakdeuk places the numbers 1 through 40 into five palaces, eight numbers per palace. Each palace is a 3x3 grid with the center cell empty.

```text
        Top palace
            |
Left palace - Center palace - Right palace
            |
        Bottom palace
```

The checksum is simple: the sum of 1 through 40 is 820, and 5 x 164 = 820. The diagram is therefore a structured five-way partition.

[01_original_graph.png attached]

## Each Palace Is an 8-Cycle

Connecting grid-adjacent numbers inside each palace gives one 8-cycle per palace.

| Palace | 8-cycle | Sum |
|---|---|---:|
| Top | 19 -> 34 -> 7 -> 39 -> 12 -> 24 -> 2 -> 27 -> 19 | 164 |
| Left | 18 -> 33 -> 8 -> 38 -> 13 -> 23 -> 3 -> 28 -> 18 | 164 |
| Center | 16 -> 30 -> 5 -> 21 -> 15 -> 36 -> 10 -> 31 -> 16 | 164 |
| Right | 4 -> 22 -> 14 -> 37 -> 9 -> 32 -> 17 -> 29 -> 4 | 164 |
| Bottom | 1 -> 25 -> 11 -> 40 -> 6 -> 35 -> 20 -> 26 -> 1 | 164 |

[04_cycle_analysis.png attached]

The full grid has 12 inter-palace edges. The four center-palace corner nodes, 30, 21, 31, and 36, have degree 4 and the highest betweenness centrality.

[05_centrality_invariants.png attached]

## Phase Sums

Partitioning 1 through 40 by residue modulo 5 gives phase sums 148, 156, 164, 172, and 180.

| Phase | Numbers | Sum |
|---|---|---:|
| Water | 1, 6, 11, 16, 21, 26, 31, 36 | 148 |
| Fire | 2, 7, 12, 17, 22, 27, 32, 37 | 156 |
| Wood | 3, 8, 13, 18, 23, 28, 33, 38 | 164 |
| Metal | 4, 9, 14, 19, 24, 29, 34, 39 | 172 |
| Earth | 5, 10, 15, 20, 25, 30, 35, 40 | 180 |

The value 164 is the Wood-group sum. The top and right palaces balance Metal and Fire, the center and bottom palaces balance Earth and Water, and the left palace takes the Wood group.

[02_wuxing_decomposition.png attached]

## Positional Pattern

| Palace | Corner sum | Edge-midpoint sum |
|---|---:|---:|
| Top | 124 | 40 |
| Left | 122 | 42 |
| Center | 118 | 46 |
| Right | 120 | 44 |
| Bottom | 126 | 38 |

The edge-midpoint sums are 38, 40, 42, 44, and 46, increasing by 2.

[08_position_patterns.png attached]

## Generalization

| M0 | Palace sum |
|---|---:|
| 1 | 148 |
| 2 | 156 |
| 3 | 164 |
| 4 | 172 |
| 5 | 180 |

Paljagakdeuk corresponds to M0 = 3. Increasing M0 by 1 increases the palace sum by 8.

[07_local_extensions.png attached]

## Conclusion

Paljagakdeuk is a compact combinatorial device built from five 8-cycles, central gateway nodes, mod-5 phase sums, positional sum patterns, and an M0-indexed family.
