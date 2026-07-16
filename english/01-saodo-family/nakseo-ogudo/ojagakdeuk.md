# Reading Nakseo Ogudo as Ojagakdeuk (Five-Each-Gets)

The original note for Nakseo Ogudo (洛書五九圖) condenses into one sentence:

> 五子各得 八十五數  
> 九宮共得 七百六十五數

This is an **Ojagakdeuk (五子各得)** structure:  
nine palaces (宮), each receiving five numbers (五子), each summing to 85, and the nine palace totals together reaching 765 when counted with overlap.

---

## 1. The Basic Numbers of Ojagakdeuk

| Quantity | Value |
|---|---:|
| Numbers used | 1 through 33, each once |
| Total sum | 561 |
| Number of palaces | 9 |
| Numbers per palace | 5 |
| Sum per palace | **85** |
| Repeated palace-total sum | 85 × 9 = **765** |

Where Sajagakdeuk (Nakseo Sagudo) places four numbers in each palace, Nakseo Ogudo places five numbers in each palace to obtain the sum 85.  
The value 85 can also be read as 5 × 17, where 17 is the average of the numbers 1 through 33.

---

## 2. The Make/Use Distinction: 33 Made, 45 Used

The structure implicitly distinguishes the numbers that are *written* (作) from the positions that are *used* (用). In Ojagakdeuk:

| Quantity | Value |
|---|---:|---:|
| Numbers written (作) | 33 (1 through 33, each once) |
| Positions used (用) | 45 (9 palaces × 5 numbers) |
| Duplicate positions | 45 − 33 = 12 |
| Plain sum of written numbers | 561 |
| Repeated palace-total sum | 765 |
| Extra from duplication, D | 765 − 561 = **204** |

The 765 repeated palace-total is therefore not a new total but the plain sum 561 plus the duplication weight 204. Those 12 duplicate positions are the overlaps created when neighboring plus-shaped palaces share boundary vertices.

---

## 3. The Nine Palaces: Each Gets Five

In Nakseo Ogudo, the nine palaces have a plus (十) shape. Each palace consists of a center point together with its four orthogonal neighbors, for a total of five vertices.

| Palace | Five numbers | Sum |
|---|---|---:|
| Upper-left | 4, 20, 16, 23, 22 | 85 |
| Upper-center | 9, 16, 14, 28, 18 | 85 |
| Upper-right | 2, 14, 33, 21, 15 | 85 |
| Middle-left | 3, 31, 19, 22, 10 | 85 |
| Center | 5, 19, 26, 18, 17 | 85 |
| Middle-right | 7, 26, 25, 15, 12 | 85 |
| Lower-left | 8, 29, 11, 10, 27 | 85 |
| Lower-center | 1, 11, 24, 17, 32 | 85 |
| Lower-right | 6, 24, 30, 12, 13 | 85 |

Adjacent palaces share boundary points. For example, Upper-left and Upper-center share the middle vertex 16, while Middle-left and Center share 19.  
That every palace still sums to 85 despite these overlaps is the central invariant of Ojagakdeuk.

---

## 4. Wuxing Mod 5 Classification

Grouping the numbers 1 through 33 by their remainder modulo 5 gives the following wuxing classes.

| Wuxing | Numbers | Count | Sum |
|---|---|---:|---:|
| Water (1 mod 5) | 1, 6, 11, 16, 21, 26, 31 | 7 | 112 |
| Fire (2 mod 5) | 2, 7, 12, 17, 22, 27, 32 | 7 | 119 |
| Wood (3 mod 5) | 3, 8, 13, 18, 23, 28, 33 | 7 | 126 |
| Metal (4 mod 5) | 4, 9, 14, 19, 24, 29 | 6 | 99 |
| Earth (0 mod 5) | 5, 10, 15, 20, 25, 30 | 6 | 105 |

The wuxing sums 99, 105, 112, 119, 126 increase by steps of 5, but the class sizes split into 6 and 7.  
Metal (4 mod 5) and Earth (0 mod 5) have 6 elements each, while Water, Fire, and Wood have 7 each. This follows from 33 = 5 × 6 + 3, so residues 1, 2, and 3 each receive one extra number.

---

## 5. Overlap Counting and 765

The phrase “九宮共得 七百六十五數” is simply the sum of the nine palace sums.

```
85 × 9 = 765
```

This value is the **overlap-weighted total**: each number is counted as many times as it belongs to palaces.  
Numbers lying on the central horizontal band or the vertical axis belong to more palaces, so the total exceeds the plain sum 561.

---

## 6. Nakseo Ogudo Summarized as Ojagakdeuk

| Aspect | Summary |
|---|---|
| Combinatorial structure | 33 numbers → 9 palaces, 5 numbers each |
| Invariant | Every palace sums to 85 |
| Construction principle | Plus-shaped five-vertex palaces sharing edges form the 3×3 grid |
| Spatial structure | 3×3 palace lattice with the center palace at the core |
| Overlap total | Sum of all nine palace sums = 765 |

Nakseo Ogudo, read as Ojagakdeuk, is a combinatorial structure built from 33 numbers.  
The simple rule that each palace receives five numbers summing to 85 ties the nine palaces together, and 765 is the natural overlap-weighted total of that structure.

---

## 7. Viewed through Saodo (the Four/Five Way)

Nakseo Ogudo is a Saodo structure in which the **Five-Way (오도)** takes center stage.

- **Five-Way (오도) aspect**: Each of the nine palaces receives five numbers (五子), summing to 85. The plus (十) shape of each palace — one center plus four orthogonal neighbors — directly implements the five-direction spatial model.
- **Four-Way (사도) aspect**: The nine palaces are arranged in a 3×3 grid, split into four corner palaces, four edge palaces, and one central palace. This 4+4+1 partition is the geometry of the Four-Way superimposed on the Five-Way.

Thus Ojagakdeuk realizes a Five-Way partial-sum invariant inside a Four-Way 3×3 grid.  
The original phrase “五子各得” emphasizes that the five numbers per palace are the action of the Five-Way, while “九宮共得” says the nine palaces are the Four-Way space that contains it.

---

## 8. Unification: Common Ground and Differences with Sajagakdeuk

From the Gakdeuk-principle viewpoint discussed in `04-unification`, Ojagakdeuk (Nakseo Ogudo) and Sajagakdeuk (Nakseo Sagudo) belong to the same family.

### Common ground

| Feature | Ojagakdeuk (Nakseo Ogudo) | Sajagakdeuk (Nakseo Sagudo) |
|---|---|---|
| Number of palaces | 9 | 9 |
| Wuxing classification | 5 residue classes | 5 residue classes |
| Partial-sum invariant | Every palace sums to 85 | Every palace sums to 42 |
| Repeated palace-total sum | 85 × 9 = 765 | 42 × 9 = 378 |
| Numbers written (作) | 33 | 20 |
| Positions used (用) | 45 | 36 |
| Extra duplication weight, D | 204 | 168 |
| Core spatial structure | Central core + four-direction extension | Central core + four-direction extension |

### Interpretive differences

| Feature | Ojagakdeuk (Nakseo Ogudo) | Sajagakdeuk (Nakseo Sagudo) |
|---|---|---|
| Numbers per palace | 5 | 4 |
| Range of numbers used | 1–33 (33 numbers) | 1–20 (20 numbers) |
| Central core | Plus-shaped 5 vertices (5, 19, 26, 18, 17) | 4-cycle (5, 16, 10, 11) |
| Geometry | 3×3 grid, nine plus-shaped palaces | 3×2 rectangle, four hexagonal faces |
| Original sum formula | 9 palaces × 85 = 765 | 5 classes × 9 palaces × 42 = 1,890 |
| Duplicate positions | 12 | 16 |
| Emphasized Way | Five-Way (오도) | Four-Way (사도) |

Ojagakdeuk expands a Five-Way partial-sum invariant into a Four-Way 3×3 grid, while Sajagakdeuk realizes a Four-Way partial-sum invariant on top of a Five-Way classification.  
Both share the Gakdeuk principle — every palace has the same partial sum — but their geometry and total sums differ according to whether the Five-Way or the Four-Way is central.

---

## 9. Place in the Π(p, q, T) Framework

The parameter family introduced in the `04-unification` Saodo-Chiljagakdeuk generalization is

```
Π(p, q, T)
```

- `p`: number of directions (or wuxing phases)
- `q`: number of peripheral slots per direction
- `T`: target sum for each direction (cluster)

Under this framework, Ojagakdeuk can be reinterpreted as follows.

| Puzzle | p | q | T |
|---|---|---|---|
| Ojagakdeuk (9 palaces, 5 numbers) | 5 (wuxing) | 6 or 7 (under full 5×5 extension) | 99, 105, 112, 119, 126 |
| Ojagakdeuk (9-palace incidence) | 9 palaces × 5 numbers | — | common partial sum 85 |

In other words, Ojagakdeuk is an example of a **5-ary direction-weighted puzzle**: the Five-Way classification is expanded into a Four-Way spatial grid.  
Because 33 = 5 × 6 + 3, Metal (4 mod 5) and Earth (0 mod 5) have 6 elements while the other three phases have 7, breaking perfect 5×5 symmetry; yet the nine palace partial sums remain uniformly 85.  
Read this way, Ojagakdeuk and Sajagakdeuk are two variations of the same Gakdeuk principle, differing only in the relative weight of Five and Four.
