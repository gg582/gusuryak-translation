# Nakseo Sagudo: Analysis Report: 20 Numbers, Nine Palaces, and Sum 42

Nakseo Sagudo is a 20-vertex, 24-edge graph. The natural modern reading is a 3x2 rectangular arrangement with four hexagonal faces sharing the central vertices 5, 16, 10, and 11.

[sanhak_graph.png attached]

[01_original_graph.png attached]

## The Corrected Graph

| Position | Cycle | Sum |
|---|---|---:|
| NW | 19, 2, 14, 5, 16, 7 | 63 |
| NE | 17, 4, 16, 10, 12, 9 | 68 |
| SW | 5, 18, 3, 13, 8, 11 | 58 |
| SE | 10, 6, 1, 20, 15, 11 | 63 |

The graph has an outer Hamiltonian 20-cycle and an inner 4-cycle:

```text
5 -> 16 -> 10 -> 11 -> 5
```

The inner 4-cycle has sum 42.

[04_cycle_analysis.png attached]

## Residues Modulo 5

| Phase | Numbers | Sum |
|---|---|---:|
| Water | 1, 6, 11, 16 | 34 |
| Fire | 2, 7, 12, 17 | 38 |
| Wood | 3, 8, 13, 18 | 42 |
| Metal | 4, 9, 14, 19 | 46 |
| Earth | 5, 10, 15, 20 | 50 |

The sums form the arithmetic progression 34, 38, 42, 46, 50. The average is 42.

[02_wuxing_decomposition.png attached]

## Nine Four-Element Blocks

The annotation can be read as a recombination of five residue classes into nine four-element blocks, all with sum 42.

| Palace | Four numbers | Sum |
|---|---|---:|
| NW | 19, 2, 14, 7 | 42 |
| N | 19, 17, 2, 4 | 42 |
| NE | 17, 4, 12, 9 | 42 |
| W | 14, 7, 18, 3 | 42 |
| C | 5, 16, 10, 11 | 42 |
| E | 9, 12, 6, 15 | 42 |
| SW | 18, 3, 13, 8 | 42 |
| S | 13, 8, 20, 1 | 42 |
| SE | 6, 1, 20, 15 | 42 |

[origin_02_9palace_grid.png attached]

The boundary blocks follow a clockwise order. The center block is the inner 4-cycle.

[origin_translated_03_overlap.png attached]

[origin_03_right_rotation.png attached]

## Mutual Transformation

The value 1890 follows from a weighted incidence count.

- five phase classes
- nine palace blocks
- 5 x 9 = 45 interactions
- each interaction weighted by 42
- 45 x 42 = 1890

[origin_04_mutual_transformation_1890.png attached]

## Graph Invariants

- Vertices: 20
- Edges: 24
- Degree-4 vertices: 5, 10, 11, 16
- Degree-2 vertices: 16
- Girth: 4
- No bridges
- No articulation points
- Diameter: 6
- Radius: 4
- Average shortest-path distance: 3.2

[05_centrality_invariants.png attached]

The graph is bipartite because all simple cycles have even length. The four length-8 cycles all have sum 84, which is 42 x 2.

[08_laplacian_spectrum.png attached]

[09_distance_matrix.png attached]

[10_cycle_distributions.png attached]

## Dual Structure and Extension

The dual graph of the four faces is a 4-cycle whose shared-vertex weights are 5, 16, 10, and 11. Their sum is again 42.

[11_dual_graph.png attached]

The 120-node construction can be modeled as six cyclic copies of the 20-node graph, linked through corresponding shared vertices. It has 120 nodes and 168 edges.

[13_extension_120.png attached]

The SW face contains all four Wood vertices, 3, 8, 13, and 18, showing a concentrated phase pattern.

[15_sw_wood_concentration.png attached]

## Conclusion

The annotation is a computational rule: split 20 numbers into five residue classes, recombine neighboring subsets into nine four-element blocks, preserve the invariant sum 42, and count 45 weighted incidences to obtain 1890.
