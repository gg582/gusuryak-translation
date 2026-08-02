# Interdisciplinary Gap & Standard Interface Specification

This document explains the **Triple Interdisciplinary Void** surrounding the **Nakseo Yukgodo (洛書六觚圖)** reconstruction project and defines the **Standard Interface Specification** established to bridge research across disciplines.

---

## 1. The Triple Interdisciplinary Void

The Nakseo Yukgodo remained historically buried or overlooked not due to intellectual incapacity, but because of structural drop-off points at the boundaries between **History of Mathematics**, **Pure Combinatorics**, and **Computer Science / Constraint Programming**.

| Discipline | Perspective on Yukgodo | Drop-off Point / Obstacle |
| :--- | :--- | :--- |
| **History of Math** | A numerological / cosmological diagram on a centered hex grid | Stays within reading primary text conditions (`虛一`, 270, 54). Avoids asserting derived properties (ring sums, axis sums) as authorial intent, fearing modern over-interpretation. |
| **Pure Mathematics** | A system with antipodal complement pairs ($v(c)+v(-c)=271$) and $D_6$ symmetry | With only antipodal sum constraints, the solution space trivially decomposes into $135! \times 2^{135}$, appearing as an elementary enumeration/search modeling problem rather than a deep theorem. |
| **Computer Science (CS/CP)** | A promising structural benchmark candidate | Specifications are not given as `.cnf` or MiniZinc models. CS researchers cannot independently parse classical Hanja manuscript jargon (`積`, `觚`, `虛一`, `寄左`), making it impossible to separate historical constraints from modern additions (lacking provenance). |

### Interdisciplinary Handoff and Cycle

In this topic, **the most interesting aspect of each field immediately transitions into the jurisdiction of the next**:

1. **History of Mathematics** deciphers `虛一` and the 270-cell grid structure from classical text.
2. Formalizing this into antipodal pair sums ($v(c)+v(-c)=271$) turns it into **Combinatorics**.
3. Adding side, sector, and ray sum constraints to search for solutions moves it into **Constraint Programming (CS)**.
4. Validating whether those exact constraints are historically sound requires returning to **Classical Philology (History of Math)**.

### Elementary Components vs. Combined Strength

* **Centered Hexagonal Number 271**: Well-known centered hex sequence ($3n(n-1)+1$).
* **Complement Pairs (1–270)**: Elementary algebraic relation.
* **Antipodal Position Pairs & Ring Sums ($813k$)**: One-line proof under $S=271$.

While each piece appears trivial individually, uniting them across **manuscript text, published diagrams, Choi Seok-jeong's other magic square works, and solver solution space modeling** fundamentally transforms the nature of the historical artifact.

---

## 2. Standard Interfaces Connecting the Three Fields

The bottleneck was not that a single researcher had to master all three fields, but that **there were no deliverable intermediate artifacts (interfaces)** between them. This project provides seven standard interfaces:

### ① Textual Corpus & Provenance
* Confirmed cross-textual evidence with *Book of Han (漢書·律曆志)* and Su Lin's commentary.
* 6 confirmed primary textual statements (`共積二百七十`, `校計周五十四數`, `以算遠則係以六`, `通加洛書數六倍`, `見甲編數器章`, `虛一則二百七十數`).
* High-confidence OCR numerical baseline in `ALGO_OCR_SUCCESS.md`.

### ② Numerical Evidence Chain
* `python3 -m yukgodo.naejeok`: Complete graph verification connecting numerical values 60, 10, 19, 152, 252, 504, 271, 270.
* Mathematical restoration of scribal transcription errors (e.g., correcting 500/506 misreadings to 504 / 五百四).

### ③ Explicit Separation of Primary vs. Derived Constraints
* **Primary / Historical Constraints**: 270-cell grid, outer perimeter 54, central axis 19.
* **Structural Hypotheses**: Antipodal complement pairs $v(c)+v(-c)=271$ (consistent across Choi Seok-jeong's diagrams).
* **Derived Invariants**: Ring sums $813k$, axis sums $2439$.
* **Optimization Objective**: Variance minimization across sides, sectors, and rays.

### ④ Standard Hexagonal Coordinate System
* `yukgodo/hexgrid.py`: Axial/cubic coordinate system with $D_6$ symmetry group actions.
* Center 1, rings $k=1..9$ ($6k$ cells per ring), side length 10 (Total 271 cells / Excluded center 270 cells).

### ⑤ Reproducible Verifier
* `python3 tests/test_hexgrid.py`: Geometric invariant testing.
* `python3 main.py`: SA (Simulated Annealing) optimization achieving penalty score 6.0.
* `python3 -m yukgodo.search_constructive`: Partitioning and verifying constructive solutions under the 6-multiplier rule ($v(P_t) \equiv 6t \pmod{271}$).

### ⑥ CS / SAT Benchmark Specification
* `output/solution.json`, `output/constructive_solution.json`: Standard JSON models of representative optimal solutions.
* Ready-to-use variable and constraint definitions for MiniZinc / CP / SAT solvers.

### ⑦ Historical Scope Claim
* Proved that the Naejeok Method (來積法) is a calculation chain for grid cell counts (積), not a spatial number placement algorithm.
* Completely disproved spatial placement interpretations (192 variations of 添六 rule) via exhaustive search (`output/hypotheses.json`).

---

## 3. Conclusion: Computational History of Mathematics

This project establishes a methodology of **Text-Based Constraint Reconstruction**, enabling specialists in each domain to conduct independent research via standardized interfaces:

* **Historians of Math**: Focus on Hanja texts, philology, and textual transmission chains.
* **Combinatorists**: Study algebraic structures of the solution space under $D_6$ symmetry and antipodal constraints.
* **CS Researchers**: Benchmarking constraint solver performance and symmetry breaking on verified historical instances.
