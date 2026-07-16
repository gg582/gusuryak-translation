# Deep Dive into Jisu-yong-yukdo (Earth-Number Six-Use Diagram): The Hexagon Puzzle Built from 1 to 20

## Introduction: Five Hexagons, All Summing to 63?

The **Jisu-yong-yukdo (地數用六圖)** handed down in the *Gusuryak* (九數略) family has the following simple yet astonishing rule.

> Place the numbers 1 through 20 into five hexagons, six per hexagon, and **the sum of the six numbers in every hexagon is 63**.

At first sight one asks, "How is that possible?" Five hexagons × six numbers requires 30 positions, but there are only 20 numbers. The answer is that **adjacent hexagons share vertices**. Like a honeycomb, the hexagons touch one another, and the touching vertices belong to several hexagons at once.

In this post we will look step by step at the historical background, mathematical structure, and modern graph-theoretic meaning of Jisu-yong-yukdo.

---

## 1. The Meaning Hidden in the Name

- **Jisu (地數)**: The numbers of Earth, contrasted with the numbers of Heaven (天數, odd numbers); it symbolizes even numbers and the principle of yin.
- **Yong-yuk (用六)**: The number 6 is used as the core unit — hexagons, six numbers per hexagon, and the resulting sum 63 are all linked to 6.
- **Do (圖)**: A diagram, a picture visualizing the placement of numbers.
- **Yukjagakdeuk (六子各得)**: "Each six obtains 63," emphasizing the rule that each hexagon has sum 63.

Thus Jisu-yong-yukdo is not a mere calculation table but a **diagram (圖像) of traditional numerology combining number symbolism with spatial placement**.

---

## 2. Core Structure at a Glance

Jisu-yong-yukdo consists of five hexagons — **upper-left, upper-right, center, lower-left, lower-right**.

| Hexagon | Six numbers | Sum |
|---|---|---|
| Upper-left | 5, 18, 16, 3, 8, 13 | 63 |
| Upper-right | 1, 13, 8, 14, 20, 7 | 63 |
| Center | 3, 8, 14, 15, 11, 12 | 63 |
| Lower-left | 12, 11, 10, 2, 19, 9 | 63 |
| Lower-right | 15, 4, 17, 6, 10, 11 | 63 |

Notice that some numbers appear in several hexagons. For example, 3, 8, 11, 12, 13, 14, and 15 belong to two or more hexagons. We call these **shared vertices**.

### Why Is the Sum 63?

The sum of 1 through 20 is 210. The total of all five hexagon sums is 63 × 5 = 315. The difference from the total sum is **315 − 210 = 105**, and this 105 is the extra amount contributed by shared vertices being counted multiple times.

Also, the average of 1–20 is 10.5. Since each hexagon has six numbers, the "average hexagon" sum is 10.5 × 6 = **63**. Therefore 63 is not accidental; it is the **natural center** of the data and a **balance condition** assigning equal weight to every hexagon.

---

## 3. The Make/Use Distinction: 20 Made, 30 Used

Jisu-yong-yukdo also distinguishes the numbers that are *written* (作) from the positions that are *used* (用).

| Quantity | Value |
|---|---:|---:|
| Numbers written (作) | 20 (1 through 20, each once) |
| Positions used (用) | 30 (5 hexagons × 6 numbers) |
| Duplicate positions | 30 − 20 = 10 |
| Plain sum of written numbers | 210 |
| Repeated hexagon-total sum | 315 |
| Extra from duplication, D | 315 − 210 = **105** |

The 10 duplicate positions come from the 8 shared vertices. Two of them, **8 and 11**, each appear in three hexagons, contributing two extra copies; the other six shared vertices (**3, 10, 12, 13, 14, 15**) appear in two hexagons, contributing one extra copy each. Thus

```
2×8 + 2×11 + (3 + 10 + 12 + 13 + 14 + 15) = 105
```

which explains why the overlap-weighted total 315 exceeds the plain written sum 210 by exactly 105.

---

## 4. Reading Jisu-yong-yukdo Through Wuxing

Jisu-yong-yukdo is not just a placement of numbers; it is also connected to the wuxing (Water, Fire, Wood, Metal, Earth). Classifying numbers by remainder modulo 5 (with 0 treated as Earth) gives the following.

| Wuxing | Residue | Numbers | Sum |
|---|---|---|---|
| Water | 1 | 1, 6, 11, 16 | 34 |
| Fire | 2 | 2, 7, 12, 17 | 38 |
| Wood | 3 | 3, 8, 13, 18 | 42 |
| Metal | 4 | 4, 9, 14, 19 | 46 |
| Earth | 0→5 | 5, 10, 15, 20 | 50 |

The wuxing sums 34, 38, 42, 46, 50 form an **arithmetic progression with common difference 4**. This inevitably appears because 1–20 is divided evenly into five classes. The total range 20 divided by 5 gives width 4, so adjacent class sums differ by 4.

What is more interesting is the **wuxing distribution of shared vertices**. Among the 8 shared vertices, Earth (10, 11, 15) appears 3 times and Wood (3, 8) appears 2 times, so Earth and Wood are concentrated at the junctions. In wuxing symbolism Earth represents mediation and stability, and Wood represents growth and connection, so this placement can be read as structurally meaningful.

---

## 5. Jisu-yong-yukdo as a Graph

If we treat the sides of the hexagons as lines and the numbers as points, Jisu-yong-yukdo becomes a **graph** in modern mathematics.

- **Vertices**: 20
- **Edges**: 24
- **Connected components**: 1 (all connected)
- **Degree**: 2 or 3

There are 8 vertices of degree 3 and 12 vertices of degree 2, matching exactly the counts of shared vertices (8) and unique vertices (12). Shared vertices are connected to several hexagons, so they have higher degree; unique vertices are connected to only one hexagon, so they have degree 2.

### The Center Hexagon Is the Heart of the Graph

The six vertices of the center hexagon {3, 8, 14, 15, 11, 12} are **all shared vertices**. Removing the center hexagon therefore disconnects Upper-left, Upper-right, Lower-left, and Lower-right from one another. The center is not just one hexagon but the **core** of the whole structure.

### Betweenness Centrality: Who Is the Gateway?

In graph theory, **betweenness centrality** measures how often a vertex lies on shortest paths between other vertices. The vertices with the highest values in Jisu-yong-yukdo are 3, 8, 12, 14, and 15. All of them are **gateways** connecting the center hexagon with the outer hexagons.

---

## 6. Cycles and Planar Graphs

Each hexagon forms a cycle of length 6. The five hexagons are independent cycles that together form the **cycle basis** of Jisu-yong-yukdo.

Applying Euler's formula V − E + F = 2:

```
20(vertices) − 24(edges) + F(faces) = 2  ⇒  F = 6
```

This gives 5 hexagonal faces plus 1 outer face, for a total of 6 faces. Thus Jisu-yong-yukdo is a **planar graph** — it can be drawn on paper without edges crossing.

---

## 7. Generation and Overcoming: The Wuxing Meaning of Edges

Classifying the 24 edges by the wuxing relationship of their endpoints gives the following.

| Classification | Count | Ratio |
|---|---|---|
| Overcoming | 12 | 50% |
| Generation | 9 | 37.5% |
| Same-phase | 3 | 12.5% |

- **Generation**: Water→Wood, Wood→Fire, Fire→Earth, Earth→Metal, Metal→Water
- **Overcoming**: Water→Fire, Fire→Metal, Metal→Wood, Wood→Earth, Earth→Water
- **Same-phase**: Same wuxing connected to itself

The fact that overcoming accounts for half is interesting. It shows that Jisu-yong-yukdo contains **not only harmony but also tension and change**. Same-phase connections are few, so most adjacent numbers interact across different wuxing.

---

## 8. Visualization Guide

The images in the same directory show Jisu-yong-yukdo from many angles.

| File | What it shows |
|---|---|
| `01_original_graph.png` | Original honeycomb structure and shared vertices |
| `02_wuxing_decomposition.png` | Numbers separated by wuxing |
| `03_adjacency_spectrum.png` | Adjacency matrix and eigenvalue distribution |
| `04_cycle_analysis.png` | The five 6-cycles with the center hexagon highlighted |
| `05_centrality_invariants.png` | Degree, centrality, and sum invariants |
| `06_wuxing_relations.png` | Wuxing generation/overcoming relation diagram |
| `07_local_extensions.png` | Generalization and concentric extension |
| `08_position_patterns.png` | Shared vertices vs. unique vertex patterns |

Viewing these images in order, one can gradually grasp the structure of Jisu-yong-yukdo from "Why 63?" to "How is it connected?" and "What role does wuxing play?"

---

## 9. Conclusion: A Meeting of Traditional Numerology and Modern Mathematics

Jisu-yong-yukdo may look like a simple puzzle of placing 1–20 into hexagons, but it hides the following multi-layered structures.

1. **Sum invariant**: the rule that every hexagon sums to 63.
2. **Make/use distinction**: 20 numbers are written into 30 positions, giving duplication weight D = 105.
3. **Shared-vertex structure**: 8 shared vertices create the duplication coefficient and connect the graph.
4. **Wuxing arithmetic progression**: mod 5 classification produces the regular sequence 34, 38, 42, 46, 50.
5. **Planar graph**: an Eulerian structure with 20 vertices, 24 edges, and 6 faces.
6. **Central core**: the center hexagon is the hub connecting the four outer hexagons.
7. **Cycle basis**: five 6-cycles generate all cycles of the graph.

Through these layers, Jisu-yong-yukdo can be re-read as a **mathematical object exploring the harmony and spatial connectedness of numbers**, going beyond a traditional mental-calculation or diagrammatic pastime.
