# Deterministic Solution Generator, SMT Completeness Proofs, and Algorithm Specifications for Nakseo Yukgodo (GENERATOR.md)

## 1. Overview

This document provides a comprehensive specification of **deterministic algorithms (generators)** capable of producing **always-valid optimal solutions (theoretical penalty floor of 6.0)** without relying on stochastic randomness or seeds for **Nakseo Yukgodo (洛書六觚圖)** from Choi Seok-jeong's (崔錫鼎) *Gusuryak (九數略)*. Furthermore, it records the exact mathematical proofs regarding **SMT Solver Completeness, Orbit Separation**, and the **Master Integrated Pipeline** using Z3 SMT Solver and Group Theory ($C_6 \times \mathbb{Z}_2$).

---

## 2. Mathematical Formulation & Theoretical Bounds

Nakseo Yukgodo consists of a hexagonal grid of radius $R=9$ containing 271 cells. Excluding the central cell (虛一), the remaining **270 cells** are filled with distinct natural numbers $1 \dots 270$.

### Core Structural Targets
1. **Antipodal Complementary Pair Constraint**:
   $$\forall c \in \text{Filled}, \quad v(c) + v(-c) = 271$$
   - The 270 cells are partitioned into 135 point-symmetric slot pairs $(c_i, -c_i)$, assigned complementary pairs $(t, 271-t)$ ($1 \le t \le 135$).
2. **Side Sum**: Sum of 10 cells along each of the 6 outer sides $= 1355$ ($5 \times 271$).
3. **Wedge Sum**: Sum of 45 cells in each of the 6 $60^\circ$ wedge sectors $\approx 6097.5$ (optimal alternating $6097 / 6098$).
4. **Ray Sum**: Sum of 9 cells along each of the 6 center-to-corner rays $\approx 1219.5$ (optimal alternating $1219 / 1220$).
5. **Axis Sum (中觚)**: Sum of 19 cells along each of the 3 central axes $= 2439$ ($9 \times 271$, automatically satisfied under antipodal pair symmetry).
6. **Penalty Floor**:
   $$P = \sum_{j=0}^5 |S_j - 1355| + \sum_{i=0}^5 |W_i - 6097.5| + \sum_{r=0}^5 |R_r - 1219.5| \ge 6.0$$
   *(The minimum possible penalty floor is $6.0$ due to the odd cell count per wedge/ray).*

---

## 3. Deterministic Algorithm Hypotheses & Experimental Results

Four deterministic algorithm hypotheses were tested via `yukgodo/experiment/deterministic_experiments.py`:

| Hypothesis Type | Deterministic Placement Method | Best Penalty (Goal: 6.0) | Assessment & Conclusion |
| :--- | :--- | :---: | :--- |
| **Hypothesis A** | **Deterministic Spiral Mapping** | `6,534.0` | No simple closed-form formula (Falsified) |
| **Hypothesis B** | **Deterministic Modular Mapping** ($v \equiv aq+br \pmod{271}$) | `24,228.0` | No simple closed-form formula (Falsified) |
| **Hypothesis C** | **Deterministic Wedge-Symmetric Equalizer** | `516.0` | Simple closed-form cannot reach lower bound |
| **Hypothesis D** | **Deterministic Pruning Backtracking DFS** | **`6.0` (Optimal)** | **100% Deterministic procedure successfully generates valid solution** |

---

## 4. Deterministic Solution Generator Specifications

### Algorithm 1: Deterministic Pruning Backtracking DFS Solver

This algorithm uses 0% randomness, relying entirely on a pre-sorted slot ordering and strict constraint propagation to generate valid solutions with penalty 6.0.

```python
# pseudo-code of Deterministic DFS Generator (Pair Selection + Orientation Backtracking)
1. Define 135 antipodal slots S_0 ... S_134 sorted deterministically by structural impact:
   - Primary Key: Perimeter side memberships
   - Secondary Key: Ray membership
   - Tertiary Key: Axial index q, then r
2. Define unassigned pairs set UnassignedPairs = {(1, 270), (2, 269), ..., (135, 136)}
3. Function DFS(slot_idx, current_partial_penalty):
   a. If slot_idx == 135:
        If current_partial_penalty <= 6.0: Return Success(assigned_values)
   b. Slot = SortedSlots[slot_idx]
   c. For pair in UnassignedPairs (in deterministic numerical order):
        For (cell_A_val, cell_B_val) in [(pair.t, 271 - pair.t), (271 - pair.t, pair.t)]:
            Set Slot.cell_A = cell_A_val, Slot.cell_B = cell_B_val
            Mark pair as assigned
            Update partial sums (side_sums, wedge_sums, ray_sums)
            Calculate lower-bound partial penalty P_bound
            If P_bound < Best_Penalty:
                If DFS(slot_idx + 1, P_bound) is Success: Return Success
            Revert partial sums & unmark pair
   d. Return Failure
```

> [!NOTE]
> Under a pre-fixed slot-to-pair mapping ($S_i \mapsto (i+1, 271-i-1)$), the search space reduces to $2^{135}$ orientation flips for fast optimization. However, general full-space exploration requires branching on both pair selection and orientation at each step.

---

### Algorithm 2: CCW Rotation-Orbit Solver (序左 · 寄左 Operator)

This algorithm implements the classical annotations **'序左'** (ordering counterclockwise) and **'寄左'** (shifting counterclockwise) as $60^\circ$ rotational operators under the $C_6$ symmetry group.

#### Counterclockwise Rotation Formula in Axial Coordinates
$$(q, r) \mapsto (-r, q + r)$$

#### Orbit-shift operation

For a slot \(s_1=(c_a,c_b)\), find the slot \(s_2=R_k(s_1)\) at the counterclockwise position \(k\times60^\circ\). Exchange the complementary pairs assigned to the two slots as a neighbouring-swap operation to escape local minima.

```python
# pseudo-code of CCW Rotation-Orbit Move
def rotation_orbit_swap(state, slot_1, rot_k):
    target_slot, is_flipped = slot_rotation_map[slot_1][rot_k]
    state.do_swap(slot_1, target_slot, flip=is_flipped)
```

---

## 5. Conditional SMT Solver Completeness & Orbit Separation

Verified via `yukgodo/experiment/smt_completeness_proof.py`.

### Mathematical Findings
1. **Conditional Completeness of SMT Solvers**:
   - Modern SMT Solvers (Z3) are complete for any specified sub-space encoding. Given an explicit constraint model, Z3 will enumerate **100% of all valid solutions within that sub-space** and return `UNSAT` upon exhaustion (Empirically verified: 54 solutions enumerated in the specified sub-space before `UNSAT`).
   - This completeness applies to the specified encoding and search sub-space, not a full unconstrained enumeration of the entire $135! \times 2^{135}$ space.
2. **Orbit Separation of Specific Generators**:
   - A single specific deterministic generator $G_A$ produces solutions strictly within its algebraic orbit $\text{Orbit}(G_A)$. Solutions in other orbits $\text{Orbit}(G_B)$ cannot be generated by $G_A$ itself.
   - However, since these solutions in $\text{Orbit}(G_B)$ are valid magic solutions, **they are searchable and discoverable by Z3 SMT Solver and generalized constraint solvers**.

---

## 6. Conclusion & Scholarly Implications

1. **No Single Closed-Form Formula**: Nakseo Yukgodo is a complex constraint satisfaction problem rather than a one-line formula.
2. **Efficacy of Deterministic Backtracking**: Deterministic pruning backtracking reaches theoretical penalty floors (6.0). General termination and completeness guarantees require explicit mathematical proof.
3. **Completeness of Constraint Solvers**: SMT Solvers guarantee complete search coverage within specified sub-space encodings.
4. **Scholarly Provenance Distinction**: The original **'來積法'** text represents a historical calculation procedure for determining grid dimensions and constants. Modern constraint solvers use these geometric constants as input parameters, but there is no evidence that modern backtracking algorithms were contained in the primary text.
