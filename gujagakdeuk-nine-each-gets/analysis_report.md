# Gujagakdeuk: Analysis Report: 45 Numbers, Five Palaces, and 92

Gujagakdeuk places the numbers 1 through 45 into five palaces, nine numbers per palace. Each palace is a full 3x3 grid.

```text
        Top palace
            |
Left palace - Center palace - Right palace
            |
        Bottom palace
```

| Palace | Nine numbers | Sum |
|---|---|---:|
| Top | 12, 44, 9, 19, 21, 29, 37, 2, 34 | 207 |
| Left | 13, 43, 8, 18, 25, 26, 38, 3, 33 | 207 |
| Center | 15, 41, 6, 16, 23, 30, 40, 5, 31 | 207 |
| Right | 14, 42, 7, 17, 24, 28, 39, 4, 32 | 207 |
| Bottom | 11, 45, 10, 20, 22, 27, 36, 1, 35 | 207 |

The sum of 1 through 45 is 1035, and 5 x 207 = 1035.

[01_original_graph.png attached]

## Grid Structure

Each palace is a 3x3 grid graph with 9 nodes, 12 internal edges, girth 4, and several 4-cycles. The full diagram has 72 edges and is connected through the center palace.

[04_cycle_analysis.png attached]

## Phase Sums

| Phase | Numbers | Sum |
|---|---|---:|
| Water | 1, 6, 11, 16, 21, 26, 31, 36, 41 | 189 |
| Fire | 2, 7, 12, 17, 22, 27, 32, 37, 42 | 198 |
| Wood | 3, 8, 13, 18, 23, 28, 33, 38, 43 | 207 |
| Metal | 4, 9, 14, 19, 24, 29, 34, 39, 44 | 216 |
| Earth | 5, 10, 15, 20, 25, 30, 35, 40, 45 | 225 |

The phase sums increase by 9. The common palace sum, 207, is the Wood-group sum.

[02_wuxing_decomposition.png attached]

## The 92 Invariant

| Palace | Corner sum | Edge-midpoint sum | Center | Total |
|---|---:|---:|---:|---:|
| Top | 92 | 94 | 21 | 207 |
| Left | 92 | 90 | 25 | 207 |
| Center | 92 | 92 | 23 | 207 |
| Right | 92 | 91 | 24 | 207 |
| Bottom | 92 | 93 | 22 | 207 |

Every palace has corner sum 92. The edge-midpoint sums are 90 through 94, and the center values 21 through 25 cover all five phase residues.

[08_position_patterns.png attached]

## Graph Summary

- Nodes: 45
- Internal palace edges: 60
- Full-grid edges: 72
- Internal connected components: 5
- Full-grid connected components: 1
- Girth: 4
- Highest betweenness: node 23, the center of the center palace

[03_adjacency_spectrum.png attached]

[05_centrality_invariants.png attached]

[06_wuxing_relations.png attached]

## Generalization

| M0 | Palace sum |
|---|---:|
| 1 | 189 |
| 2 | 198 |
| 3 | 207 |
| 4 | 216 |
| 5 | 225 |

Gujagakdeuk corresponds to M0 = 3.

[07_local_extensions.png attached]

## Conclusion

Gujagakdeuk is a five-palace 3x3-grid structure with common sum 207, corner invariant 92, center values 21 through 25, and a natural M0-indexed family.
