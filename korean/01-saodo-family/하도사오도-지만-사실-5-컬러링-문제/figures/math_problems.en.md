# Modern Combinatorial Problems Extracted from the Hado Puzzle

> These problems translate the classical diagram into modern combinatorics / discrete mathematics language.

---

## Problem 1. Proper 5-Coloring on a Symmetric Cross

Twenty circular slots are placed in a symmetric cross. Each slot is labeled with a unique integer from 1 to 20. Define the coloring function

```
c(v) = L(v) mod 5   (with 0 replaced by 5)
```

Prove that this function yields a **proper 5-coloring** with exactly four vertices in each color class.

---

## Problem 2. Heaven-and-Earth Number Partition


Following the original text "河圖五五卽上天數圖，六五卽上地數圖", partition the numbers 1 through 10 into

- Heaven numbers `H = {1,3,5,7,9}`
- Earth numbers `E = {2,4,6,8,10}`

Prove the identities

```
ΣH = 25 = 5²
ΣE = 30 = 5·6
ΣH + ΣE = 55
```

Extend this to 1 through 20 by `H' = H ∪ (H+10)` and `E' = E ∪ (E+10)`, and show `|H'| = |E'| = 10`, `ΣH' = 100`, and `ΣE' = 110`.

---

## Problem 3. Involution Structure on the Five Phases


On the five-phase set `G = {Water, Fire, Wood, Metal, Earth}` define

- Opposition `σ`: Water ↔ Earth
- Complement `τ`: Fire ↔ Metal

Prove that both `σ` and `τ` are involutions on `G`, i.e. `σ² = τ² = Id`. Investigate whether `σ` and `τ` commute.

---

## Problem 4. Block Design Consistency


On `V = {1,…,20}` define two block families

```
B_H = { {1,6,11,16}, {2,7,12,17}, {3,8,13,18}, {4,9,14,19}, {5,10,15,20} }
B_E = { {1,11}, {3,13}, {5,15}, {7,17}, {9,19} }
```

Verify that each is a family of subsets of `V`, and compute the intersection matrix

```
M[i,j] = |B_H[i] ∩ B_E[j]|
```

Describe any structural property you observe in this matrix.

---

## Problem 5. Term Rewriting System


On the five-phase set `G` define the rewriting rules

```
Wood + Wood → Fire
Metal + Fire → ∅   (annihilation)
```

Treating these as part of a term rewriting system, answer the following.

1. Are these rules **confluent**?
2. What are the normal forms reachable from the multiset `{Wood, Wood, Metal, Fire}`?
3. How does the checksum `Σ L(v) = 210` change under rewriting?

---

## Problem 6. Checksum Invariant


The diagram states that the sum of all numerals is `共積210`. Prove that this equals `1 + 2 + … + 20`. Discuss what additional invariant must be defined if the rewriting rules `Wood + Wood → Fire` or `Metal + Fire → ∅` are actually applied, so that the total sum does not lose its meaning.
