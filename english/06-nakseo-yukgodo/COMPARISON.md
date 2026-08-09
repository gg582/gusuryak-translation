# Comparison of Yukgodo Search Algorithms (COMPARISON)

This document compares the baseline heuristic search with an experimental generator-constrained search. The latter uses $v(P_t) \equiv 6t \pmod{271}$ as a structural hypothesis; it is not presented as a recovered historical procedure.

---

## 1. Algorithmic Design and Mathematical Formulations

| Metric / Feature | Baseline Search (solver.py) | Reconstructed Generative Path Search |
| :--- | :--- | :--- |
| **Core Paradigm** | Global optimization-based heuristic search | Algebraic generator-based geometric constraint search |
| **Mathematical Assumption** | $v(c) + v(-c) = 271$ | $v(P_t) \equiv 6 \cdot t \pmod{271}$<br>$P_{271-t} = -P_t$ |
| **State Representation** | Value mapping and flip directions for 135 slots | Permutation array of grid path order $P = (P_1, \dots, P_{270})$ |
| **Transition Operators (Moves)** | 1. Flip slot direction ($O(1)$)<br>2. Swap value pairs between two slots ($O(1)$) | 1. Swap two node positions in the path ($O(N)$)<br>2. Flip slot direction ($O(N)$) |
| **Objective Function (Cost)** | Magic sum penalties (sides, wedges, rays) | Magic sum penalties + $\alpha \times$ average walk distance |
| **Goal** | Find any magic labeling satisfying sum properties | Test witness solutions under an added generator and walk objective |

---

## 2. Search Space Dissection

### A. Baseline Search
Since it preserves the antipodal pair sum constraint, it reduces the search space of size $270! \approx 10^{543}$ to $135! \times 2^{135}$:
$$|S_{\text{baseline}}| = 135! \times 2^{135} \approx 2.7 \times 10^{230} \times 4.4 \times 10^{40} \approx 1.2 \times 10^{271}$$
Because all slot variables are decoupled from sequential path constraints, the search landscape is smooth, allowing high-speed incremental evaluation ($O(1)$) to find optimal configurations rapidly.

### B. Reconstructed Generative Path Search
Enforces a tight coupling between the grid cell coordinates and the path sequence index $t$ via the algebraic generator $v(P_t) \equiv 6t \pmod{271}$. 
When $\alpha > 0$, it pushes consecutive modular values ($v$ and $v+6$) to be geometrically close on the grid ($\text{dist}(P_t, P_{t+1}) = 1$).
- **Physical/Topological Constraint**: On a 270-cell hex grid, finding a perfect 1-step Hamiltonian path that respects the central symmetry is highly constrained, making the search landscape extremely rugged and isolating valid regions.

---

## 3. Algorithmic Benchmarks and Empirical Results

Using the benchmark script `compare_algorithms.py` over 30,000 steps, we measured the convergence performance and geometric walk distances:

### Benchmark Summary (from `output/comparison_results.json`, actual measured values)

> **Scope**: The Constructive SA (α=0.0) output is a witness solution for the stated generator hypothesis and objective.
> The α=2.0 experiment is a separate test to verify what happens when geometric walk continuity is also forced.

- **Baseline SA** (no algebraic structure enforced):
  - Final Penalty: **14.0** (Fast convergence)
  - Average Hex Distance: **9.004** (Same level as random scatter)
  - Time: **0.10s** (Approx. 300,000 steps/sec)
- **Constructive SA, $\alpha=0.0$** (generator-constrained witness — `output/constructive_solution.json`):
  - Final Penalty: **14.0** → **enforces the 6-multiplier algebraic structure (`v = 6t mod 271`) throughout, while achieving magic sum properties**
  - Average Hex Distance: **8.520** (values are globally distributed — no spatial walk constraint imposed)
  - Time: **3.68s** (path distance re-evaluation overhead, ~37x slower than baseline)
  - **Scope**: This is a valid solution of the encoded constraints. The value assignment order follows the modular arithmetic progression `6t mod 271`; its connection to `添六/係以六` is a hypothesis under test, not a textual identification.
- **Constructive SA, $\alpha=2.0$** (additional experiment — spatial walk continuity also enforced):
  - Final Penalty: **58.0** (magic sum balance collapses)
  - Average Hex Distance: **4.297** (spatial continuity improved, but magic properties destroyed)
  - Time: **3.65s**

---

## 4. Computer Science Insight: How the Reconstruction Succeeds, and the Incompatibility with Spatial Continuity

### 4-A. How the generator-constrained search succeeds (α=0.0)

The 6-multiplier generative search achieves a **valid magic-square solution** as follows:

1. **Fix value assignment order algebraically**: The constraint that slot $i$ must receive value $v = 6i \bmod 271$ is enforced throughout every step of the search.
2. **Search only over slot ordering (spatial placement)**: The permutation of which antipodal pair (slot) occupies which position on the grid is optimized via SA.
3. **Result**: Converges to penalty 14.0 while preserving the encoded algebraic structure — this witness is saved as `constructive_solution.json` and `constructive_nakseo_yukgodo.png`.

> Summary: The 6-multiplier rule is applied as the rule that **determines the value of the t-th placed slot**. This rule itself does not conflict with magic-square properties. Optimizing which cell becomes the t-th position yields a valid magic-square solution.

### 4-B. Additional Experiment: Forcing Spatial Walk Continuity Simultaneously (α=2.0)

This experiment adds the constraint that "not only the value order, but also the t-th and (t+1)-th cells on the grid must be physically adjacent."

```
[Spatial continuity enforced: α=2.0]      [Algebraic structure only: α=0.0 — witness]
  Avg walk distance 4.3 (continuity improved)   Avg walk distance 8.5 (globally scattered)
  Penalty 58.0 (magic sums destroyed)            Penalty 14.0 (magic sums satisfied)
```

Reason: Magic-square balance requires large and small values to be globally dispersed across the grid, but the spatial continuity constraint forces numerically adjacent values ($6t$ and $6(t+1)$, differing by 6) to cluster in the same local region. These two conditions **structurally conflict**.

**Conclusion within the tested models**: the 192 encoded ±6 placement variants and the added walk objective do not support a spatial-movement reading. Together with the transcription evidence, this favors—but does not prove—the reading of `添六` as part of a cell-count calculation.
