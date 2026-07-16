# Reading Nakseo Sagudo as Sajagakdeuk (Four-Each-Gets)

The original annotation of Nakseo Sagudo (洛書四九圖) condenses into one sentence:

> 鄰星相兼五宫化 爲九宫每宫四子 各得四十二數  
> 此即河圖四五画 右旋者 互化則一千八百九十數

In modern terms, this is a **Sajagakdeuk (四子各得)** structure:  
nine palaces (宮), each receiving four numbers (四子), all sharing the same sum of 42.

---

## 1. The Basic Numbers of Sajagakdeuk

| Quantity | Value |
|---|---:|
| Numbers used | 1 through 20, each once |
| Total sum | 210 |
| Number of palaces | 9 |
| Numbers per palace | 4 |
| Sum per palace | **42** |
| Repeated palace-total sum | 42 × 9 = **378** |

The value 42 is not an arbitrary symbol. When 20 numbers are split into five wuxing (mod 5) classes, the average class sum is 42. Sajagakdeuk realizes this average in all nine palaces simultaneously.

---

## 2. The Make/Use Distinction: 20 Made, 36 Used

The structure implicitly distinguishes the numbers that are *written* (作) from the positions that are *used* (用). In Sajagakdeuk:

| Quantity | Value |
|---|---:|---:|
| Numbers written (作) | 20 (1 through 20, each once) |
| Positions used (用) | 36 (9 palaces × 4 numbers) |
| Duplicate positions | 36 − 20 = 16 |
| Plain sum of written numbers | 210 |
| Repeated palace-total sum | 378 |
| Extra from duplication, D | 378 − 210 = **168** |

The 378 repeated palace-total is therefore not a new total but the plain sum 210 plus the duplication weight 168. Those 16 duplicate positions are exactly the overlaps created when neighboring palaces share two elements each.

---

## 3. The Nine Palaces: Each Gets Four

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

The central palace (C) is exactly the inner 4-cycle of the graph: 5 + 16 + 10 + 11 = 42.  
The eight boundary palaces are built from overlapping vertices of adjacent faces in the 3×2 rectangular layout.

---

## 4. From Five Palaces to Nine Palaces

The phrase “五宫化 爲九宫” describes the following procedure:

1. Start with 20 numbers classified into five wuxing (mod 5) groups.
2. Overlap neighboring groups to form nine four-element blocks.
3. Arrange them so every block sums to 42.

| Wuxing | Numbers | Sum |
|---|---|---:|
| Water | 1, 6, 11, 16 | 34 |
| Fire | 2, 7, 12, 17 | 38 |
| Wood | 3, 8, 13, 18 | 42 |
| Metal | 4, 9, 14, 19 | 46 |
| Earth | 5, 10, 15, 20 | 50 |

The wuxing sums 34, 38, 42, 46, 50 form an arithmetic progression with average 42.  
Sajagakdeuk reconstructs these five classes into nine overlapping palace blocks.

---

## 5. Neighboring Stars Overlap

“鄰星相兼” means adjacent palaces share two elements each.

```
NW = {19, 2, 14, 7}
N  = {19, 17, 2, 4}
NW ∩ N = {19, 2}
```

Each palace has four elements, yet neighbors overlap by two, so the nine palaces form a block design with overlap rather than a simple partition.  
The fact that every palace still sums to 42 is the core invariant of Sajagakdeuk.

---

## 6. Right Rotation and Mutual Transformation 1890

“右旋” means the eight boundary palaces cycle clockwise around the center.

```
NW → N → NE → E → SE → S → SW → W → NW
```

“互化則一千八百九十數” counts all pairings between the five wuxing classes and the nine palace blocks, weighted by the common invariant 42.

```
5 × 9 = 45
45 × 42 = 1,890
```

Thus 1,890 is not a free-floating symbol but the incidence product of five classes and nine blocks, multiplied by the invariant sum 42.

---

## 7. Nakseo Sagudo Summarized as Sajagakdeuk

| Aspect | Summary |
|---|---|
| Combinatorial structure | 20 numbers → 9 palaces, 4 numbers each |
| Invariant | Every palace sums to 42 |
| Construction principle | Recombine five wuxing classes into nine overlapping blocks |
| Spatial structure | Central 4-cycle plus eight clockwise boundary palaces |
| Mutual transformation | 5 classes × 9 palaces × 42 = 1,890 |

Nakseo Sagudo, read as Sajagakdeuk, is a small combinatorial device built from 20 numbers.  
The original annotation is its operating manual, and 42 is a designed invariant, not an accident.

---

## 8. Viewed through Saodo (the Four/Five Way)

Nakseo Sagudo simultaneously encodes the interplay of **Saodo (四/五道)** — the Four and Five Ways.

- **Four-Way (사도) aspect**: Each of the nine palaces receives four numbers (四子). The central palace’s 4-cycle (5, 16, 10, 11) is the core of the Four-Way; sixteen boundary vertices and four central vertices form the 3×2 rectangular layout.
- **Five-Way (오도) aspect**: The twenty numbers are classified into five wuxing (mod 5) classes. The transformation of five palaces into nine palaces (五宫化爲九宫) is the action of the Five-Way.

Thus Sajagakdeuk realizes a Four-Way partial-sum invariant on top of a Five-Way classification system.  
This is why the original text calls it “河圖四五画”: the Four and the Five are drawn together and interact.

---

## 9. Unification: Common Ground and Differences with Ojagakdeuk

From the Gakdeuk-principle viewpoint discussed in `04-unification`, Sajagakdeuk (Nakseo Sagudo) and Ojagakdeuk (Nakseo Ogudo) belong to the same family.

### Common ground

| Feature | Sajagakdeuk (Nakseo Sagudo) | Ojagakdeuk (Nakseo Ogudo) |
|---|---|---|
| Number of palaces | 9 | 9 |
| Wuxing classification | 5 residue classes | 5 residue classes |
| Partial-sum invariant | Every palace sums to 42 | Every palace sums to 85 |
| Repeated palace-total sum | 42 × 9 = 378 | 85 × 9 = 765 |
| Numbers written (作) | 20 | 33 |
| Positions used (用) | 36 | 45 |
| Extra duplication weight, D | 168 | 204 |
| Core spatial structure | Central core + four-direction extension | Central core + four-direction extension |

### Interpretive differences

| Feature | Sajagakdeuk (Nakseo Sagudo) | Ojagakdeuk (Nakseo Ogudo) |
|---|---|---|
| Numbers per palace | 4 | 5 |
| Range of numbers used | 1–20 (20 numbers) | 1–33 (33 numbers) |
| Central core | 4-cycle (5, 16, 10, 11) | Plus-shaped 5 vertices (5, 19, 26, 18, 17) |
| Geometry | 3×2 rectangle, four hexagonal faces | 3×3 grid, nine plus-shaped palaces |
| Original sum formula | 5 classes × 9 palaces × 42 = 1,890 | 9 palaces × 85 = 765 |
| Duplicate positions | 16 | 12 |
| Emphasized Way | Four-Way (사도) | Five-Way (오도) |

Sajagakdeuk spreads a Four-Way partial-sum invariant across a Five-Way classification, while Ojagakdeuk expands a Five-Way partial-sum invariant into a 3×3 spatial grid.  
Both share the Gakdeuk principle — every palace has the same partial sum — but their geometry and total sums differ according to whether the Four-Way or the Five-Way is central.

---

## 10. Place in the Π(p, q, T) Framework

The parameter family introduced in the `04-unification` Saodo-Chiljagakdeuk generalization is

```
Π(p, q, T)
```

- `p`: number of directions (or wuxing phases)
- `q`: number of peripheral slots per direction
- `T`: target sum for each direction (cluster)

Under this framework, Sajagakdeuk can be reinterpreted as follows.

| Puzzle | p | q | T |
|---|---|---|---|
| Sajagakdeuk (9 palaces, 4 numbers) | 5 (wuxing) | 3 (two-cycle layers per phase) | 34, 38, 42, 46, 50 |
| Sajagakdeuk (5×9 incidence) | 5 × 9 = 45 interactions | — | common weight 42 |

In other words, Sajagakdeuk can be seen as an **incidence structure** between the Five-Way and the Four-Way (nine palaces), and 1,890 is the total of that interaction: 5 × 9 × 42.  
Read this way, Sajagakdeuk and Ojagakdeuk are two variations of the same Gakdeuk principle, differing only in the relative weight of Four and Five.
