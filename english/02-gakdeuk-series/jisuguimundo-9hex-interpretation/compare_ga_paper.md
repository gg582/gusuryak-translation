# Genetic-Algorithm Approaches for Gakdeuk-Style Node Placement

This document compares two genetic-algorithm approaches for solving
"each-gets" (gakdeuk / 各得) puzzles, in which the numbers 1..N are placed on
N nodes so that every given cluster sums to the same magic constant S.

- **Approach A**: a generic permutation-based GA with optional swap local search.
- **Approach B**: the hybrid GA described in
  *Choe, Choi & Moon, GECCO 2003* for the Hexagonal Tortoise Problem.

Both solvers are applied to the 30-node, 9-hexagon Jisuguimundo (지수귀문도)
with magic constant S = 93.

---

## 1. Reference paper

> Heemahn Choe, Sung-Soon Choi, and Byung-Ro Moon,
> **"A Hybrid Genetic Algorithm for the Hexagonal Tortoise Problem"**,
> in *Genetic and Evolutionary Computation — GECCO 2003* (E. Cantú-Paz et al., eds.),
> Lecture Notes in Computer Science, vol. 2723, pp. 850–861,
> Springer-Verlag, Berlin Heidelberg, 2003.
>
> Direct PDF link:
> [https://www.cs.york.ac.uk/rts/docs/GECCO_2003/papers/2723/27230850.pdf](https://www.cs.york.ac.uk/rts/docs/GECCO_2003/papers/2723/27230850.pdf)

The paper regards the Hexagonal Tortoise Problem (HTP) as a minimisation of
the variance of hexagonal sums.  Its fitness function is

```
fitness = - σ²
```

where σ² is the sum of squared deviations of the cluster sums from their
average.  A perfect solution has fitness 0.

---

## 2. Approach A: generic GA gakdeuk solver (`ga_gakdeuk_solver.py`)

### Encoding
- Permutation of length N: chromosome[i] is the number written on node i.

### Operators
- **Crossover**: PMX (Partially Mapped Crossover), preserves permutation
  validity.
- **Mutation**: single swap of two positions.
- **Local search** (optional): greedy first-improvement swap.
  - `consecutive_only=False`: examines every pair of positions (O(N²) per
    pass).
  - `consecutive_only=True`: examines only pairs whose current values differ
    by 1, motivated by the observation in the paper that such moves dominate
    improving exchanges.

### Selection / replacement
- Tournament selection.
- Generational replacement with elitism.

### Detecting non-existence
Because a GA is not a complete method, it cannot *prove* infeasibility.
The solver returns `not_found_within_limit` when the best fitness stays below
zero for a long stagnation period.  For small instances this can be checked
against an exact MILP solver; for large instances the result is only an
indication that a solution is hard to find within the given budget.

---

## 3. Approach B: paper hybrid GA (`paper_hga_htp_solver.py`)

This is a direct implementation of the algorithm in the GECCO 2003 paper,
simplified only in the aging mechanism (the paper does not give full details).

### Encoding
- Permutation of length N, indexed top-to-bottom in zigzag order.

### Fitness
- `fitness = - variance of hexagonal sums`, identical to Approach A.

### Operators
- **Crossover**: two-point crossover, followed by **repair** (values are
  replaced by their sorted ranks; ties are randomly reordered).
- **Mutation**: each gene is increased by 1 with probability 1/3 or decreased
  by 1 with probability 1/3, then repaired.

### Local optimisation: consecutive exchange + tabu search
- Only pairs of positions whose values differ by 1 are tried.
- Equi-fitness moves are accepted and recorded in a tabu list to avoid
  revisiting the same solution.

### Nearby search
- After the GA loop, each chromosome is perturbed by a few random swaps and
  re-optimised.  If the result is not worse, it replaces the original.

### Replacement
- The worst half of the population is replaced each generation.

---

## 4. Experimental results on the 30-node Jisuguimundo

All runs use the same random seed (42) and target S = 93.

| Method | Population | Local search | Generations | Time (s) | Status | Variance |
|---|---|---:|---:|---:|---|---:|
| Generic GA (full swap) | 200 | all pairs | 1 | 12.59 | optimal | 0.000000 |
| Generic GA (consecutive) | 200 | diff = 1 only | 7 | 8.85 | optimal | 0.000000 |
| Paper hybrid GA | 300 | consecutive + tabu + nearby | 12 | 56.64 | optimal | 0.000000 |

*The generic GA with full swap needed only one generation because the initial
population, after aggressive local search, already contained an optimum.  The
consecutive-only variant is faster per pass and still finds the optimum
quickly.*

---

## 5. Approach-level comparison

| Aspect | Generic GA (Approach A) | Paper hybrid GA (Approach B) |
|---|---|---|
| Encoding | Permutation | Permutation with zigzag index order |
| Crossover | PMX (permutation-safe) | Two-point + repair |
| Mutation | Position swap | Value +/- 1 + repair |
| Local search | Full or consecutive swap | Consecutive exchange only |
| Extra mechanisms | Elitism, stagnation stop | Tabu search, nearby search, worst-half replacement |
| Problem specificity | General gakdeuk puzzles | Tuned for HTP, especially diamond HTPs |
| Implementation complexity | Simple | Moderate (repair, tabu, nearby search) |

---

## 6. Efficiency comparison

On the 30-node instance:

- **Generic GA (consecutive)** is the fastest in wall-clock time (≈ 9 s).
- **Generic GA (full swap)** is slower because it scans O(N²) pairs during
  local search, although it reaches optimum in fewer generations.
- **Paper hybrid GA** takes more time in this demo configuration, mainly
  because of the larger population, the nearby-search loop, and the tabu-list
  management.  However, the paper reports results for much larger instances
  (up to 160 nodes and beyond) where the problem-specific heuristics become
  essential.

Important caveats:

1. The comparison is on a single small instance.  A single run is not enough
   to estimate average-case performance.
2. The paper's algorithm was designed and tuned for large diamond HTPs; its
   overheads pay off when the landscape becomes very rugged.
3. The generic GA relies heavily on local search.  With local search disabled,
   it would be far weaker, whereas the paper's HGA still benefits from
   population-level search and nearby search.

---

## 7. Conclusions

- Both approaches successfully solve the 30-node Jisuguimundo.
- The generic GA with consecutive local search is the simplest and fastest on
  this instance.
- The paper's hybrid GA is more sophisticated and targets large-scale HTPs
  with rugged fitness landscapes; its full advantage appears on instances far
  larger than the 30-node demo.
- For a complete guarantee (finding a solution or proving none exists), both
  GA methods should be complemented by an exact solver such as MILP or
  constraint programming.
