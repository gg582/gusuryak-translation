# Saodo (Four/Five Way) and the Interchange of Gakdeuk: Unifying Sajagakdeuk and Ojagakdeuk

Nakseo Sagudo (Sajagakdeuk) and Nakseo Ogudo (Ojagakdeuk) both belong to `01-saodo-family`, yet one places 4 at the center and the other places 5 at the center. This document unifies the two diagrams from the **Saodo (四/五道, Four/Five Way)** perspective of mutual interchange, and connects them to the Gakdeuk principle in `04-unification`.

---

## 1. What Is Saodo (the Four/Five Way)?

**Saodo** is a traditional numerological framework that handles 4 (사) and 5 (오) together.

- **Four-Way (사도)**: The four cardinal directions, four seasons, 4-cycles, four children (四子), and other structures centered on 4.
- **Five-Way (오도)**: The five wuxing phases (Water, Fire, Wood, Metal, Earth), the five directions (four cardinals plus center), five children (五子), and other structures centered on 5.

Saodo means the structure in which 4 and 5 transform into or overlap with each other.  
Nakseo Sagudo and Nakseo Ogudo are two variations of this Saodo: one foregrounds the Four-Way, the other foregrounds the Five-Way.

---

## 2. Sajagakdeuk (Nakseo Sagudo) as Saodo

Nakseo Sagudo is a Saodo structure in which the **Four-Way is central**.

- **Four-Way core**: Each of the nine palaces receives four numbers (四子), summing to 42. The central palace is itself the 4-cycle (5, 16, 10, 11).
- **Five-Way action**: The twenty numbers are divided into five wuxing (mod 5) classes, and five palaces are transformed into nine palaces (五宫化爲九宫).
- **Saodo interaction**: 5 wuxing classes × 9 palaces × 42 = 1,890.

Thus Sajagakdeuk realizes a **Four-Way partial-sum invariant (42) on top of a Five-Way classification system**.

---

## 3. Ojagakdeuk (Nakseo Ogudo) as Saodo

Nakseo Ogudo is a Saodo structure in which the **Five-Way is central**.

- **Five-Way core**: Each of the nine palaces receives five numbers (五子), summing to 85. Each palace has a plus (十) shape: one center plus four orthogonal neighbors = 5 vertices.
- **Four-Way action**: The nine palaces are arranged in a 3×3 grid, split into four corner palaces, four edge palaces, and one central palace — a 4+4+1 structure.
- **Saodo interaction**: 9 palaces × 85 = 765.

Thus Ojagakdeuk expands a **Five-Way partial-sum invariant (85) into a Four-Way 3×3 grid**.

---

## 4. Sajagakdeuk ↔ Ojagakdeuk Interchange

The two diagrams can be read as mutually transformable through the following correspondence.

| Axis of interchange | Sajagakdeuk → Ojagakdeuk | Ojagakdeuk → Sajagakdeuk |
|---|---|---|
| Subset size | 4 → 5 (increase by 1) | 5 → 4 (decrease by 1) |
| Partial sum | 42 → 85 (average × size) | 85 → 42 (average × size) |
| Number range | 1–20 → 1–33 | 1–33 → 1–20 |
| Central core | 4-cycle → plus-shaped 5 vertices | plus-shaped 5 vertices → 4-cycle |
| Geometric space | 3×2 rectangle → 3×3 grid | 3×3 grid → 3×2 rectangle |
| Emphasized Way | Four-Way → Five-Way | Five-Way → Four-Way |

This correspondence is not mere analogy. Under the same generative rule — the Gakdeuk principle — the two diagrams are structural transformations that differ only in the ratio of Four to Five.

---

## 5. Unification: Common Ground

From the Gakdeuk-principle viewpoint in `04-unification`, the two diagrams share the following.

### 5.1 Nine palaces + central core

Both have nine palaces, with the central palace acting as the core of the whole structure.

- Sajagakdeuk: the central 4-cycle (5, 16, 10, 11) connects the four faces.
- Ojagakdeuk: the central plus-shaped 5 vertices (5, 19, 26, 18, 17) connect the four directional palaces.

### 5.2 Five wuxing (mod 5) classes

Both classify numbers into five residue classes (wuxing).

- Sajagakdeuk: 20 numbers into five groups of 4, sums 34/38/42/46/50.
- Ojagakdeuk: 33 numbers into five groups of 6 or 7, sums 99/105/112/119/126.

### 5.3 Partial-sum invariant

In both, every palace has the same sum.

- Sajagakdeuk: all nine palaces sum to 42.
- Ojagakdeuk: all nine palaces sum to 85.

### 5.4 Duplication-count equation

A variant of the Gakdeuk equation `5·S = T + D` for the nine-palace structure is:

```
Repeated palace-total sum = (sum per palace) × 9
```

- Sajagakdeuk: 42 × 9 = 378. (Total of 20 numbers 210 + duplication sum 168)
- Ojagakdeuk: 85 × 9 = 765. (Total of 33 numbers 561 + duplication sum 204)

### 5.5 Saodo interaction

Both express the interaction of 4 and 5 numerically.

- Sajagakdeuk: 5 (wuxing) × 9 (palaces) × 42 (partial sum) = 1,890.
- Ojagakdeuk: 9 (palaces) × 85 (partial sum) = 765. (Here 85 = 5 × 17, where 17 is the average of 1–33.)

---

## 6. Unification: Interpretive Differences

| Feature | Sajagakdeuk (Nakseo Sagudo) | Ojagakdeuk (Nakseo Ogudo) |
|---|---|---|
| Central Way | Four-Way (사도) | Five-Way (오도) |
| Numbers per palace | 4 | 5 |
| Partial sum | 42 | 85 |
| Numbers used | 20 | 33 |
| Central core | 4-cycle | Plus-shaped 5 vertices |
| Geometry | 3×2 rectangle, four hexagonal faces | 3×3 grid, nine plus-shaped palaces |
| Wuxing group sizes | 4 each (uniform) | 6 or 7 (non-uniform) |
| Original sum formula | 5 × 9 × 42 = 1,890 | 9 × 85 = 765 |
| Saodo reading | Realizes Four-Way on Five-Way | Expands Five-Way into Four-Way space |

The key difference is **which Way is in the foreground**.  
Sajagakdeuk shows a Four-Way partial-sum invariant on top of a Five-Way wuxing classification, while Ojagakdeuk places a Five-Way partial-sum invariant inside a Four-Way 3×3 grid.

---

## 7. Place in the Π(p, q, T) Framework

The parameter family defined in the `04-unification` Saodo-Chiljagakdeuk generalization is

```
Π(p, q, T)
```

- `p`: number of directions (or wuxing phases)
- `q`: number of peripheral slots per direction
- `T`: target sum for each direction (cluster)

Within this framework, Sajagakdeuk and Ojagakdeuk are positioned as follows.

| Puzzle | p | q | T | Reading |
|---|---|---|---|---|
| Chiljagakdeuk | 5 | 6 | 120 | 5 clusters, 7 elements each, sum 120 |
| Sajagakdeuk (wuxing classes) | 5 | 3 | 34, 38, 42, 46, 50 | 5 wuxing classes, 4 elements each, arithmetic progression |
| Ojagakdeuk (wuxing classes) | 5 | 6 or 7 | 99, 105, 112, 119, 126 | 5 wuxing classes, 6–7 elements, arithmetic progression |

Sajagakdeuk and Ojagakdeuk both share `p = 5`, a Five-Way structure, but differ in `q` and `T`.  
Sajagakdeuk reorganizes 4-element wuxing classes into nine palaces, foregrounding the Four-Way. Ojagakdeuk places 6–7-element wuxing classes into a nine-palace plus-shaped structure, foregrounding the Five-Way.

From the per-palace partial-sum viewpoint:

```
Sajagakdeuk: 9 palaces × 4 numbers = 42  →  Π-like: 9 palaces, target 42, 4-element blocks
Ojagakdeuk:  9 palaces × 5 numbers = 85  →  Π-like: 9 palaces, target 85, 5-element blocks
```

Thus the two diagrams are members of the same family occupying different "slices" of Π(p, q, T).

---

## 8. Conclusion: Two Variations on Four and Five

Sajagakdeuk and Ojagakdeuk are two variations on the same Gakdeuk theme, played in two different Saodo colors.

- **Sajagakdeuk**: Spreads a Four-Way partial-sum invariant across a Five-Way wuxing classification.
- **Ojagakdeuk**: Places a Five-Way partial-sum invariant inside a Four-Way 3×3 grid.

They share nine palaces, five wuxing classes, identical partial sums, and overlap-weighted totals, yet their geometry and sum magnitudes differ according to whether Four or Five is in the foreground.  
This is precisely the "mutual interchange of Four and Five" that Saodo and the Gakdeuk principle describe.
