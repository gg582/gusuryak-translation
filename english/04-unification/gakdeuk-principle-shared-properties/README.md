# Shared Properties and Generalization of Puzzles Following the Gakdeuk (各得) Principle

This directory analyzes the shared structure and generalization model of the Gakdeuk puzzle family from the *Gusuryak (九數略)* tradition (Gujagakdeuk, Ojagakdeuk, Yukjagakdeuk, Chiljagakdeuk, Paljagakdeuk), and includes a MILP solver that automatically finds Gakdeuk-style number placements for a given `n`.

## File Structure

| File | Description |
|---|---|
| `analysis_report.md` | In-depth analysis of shared properties, differences, and generalization models of the Gakdeuk family |
| `blog.md` | Popular explanation of the Gakdeuk principle |
| `generalize_gakdeuk.py` | Data definitions for each family and verification of Five-Element sums and duplication equations |
| `gakdeuk_solver.py` | **N-Gakdeuk MILP Solver** (Python + PuLP) |
| `computed_report.md` | Output of `generalize_gakdeuk.py` |

## Installation

If SageMath is not available, install PuLP in a Python virtual environment.

```bash
cd "/home/yjlee/gusuryak-translation/english/04-unification/gakdeuk-principle-shared-properties"
python3 -m venv venv
source venv/bin/activate
pip install pulp
```

## Solver Usage

### Solve all five known families at once

```bash
source venv/bin/activate
python gakdeuk_solver.py --all --time-limit 120
```

Sample output:

```
[Solving] Ojagakdeuk (Cheonsuyongodo) (n=5, N_max=24, S=65)
N=5, N_max=24, S=65
Unique vertex sum T=265, duplicated-inclusive sum 5S=325, D=60
Missing numbers: [3, 10, 22]
Shared vertices: [6, 7, 23, 24]
  C1(Center): 2 + 7 + 12 + 20 + 24 = 65
  ...
```

### Solve for arbitrary n, N_max, S

```bash
# No shared vertices between subsets (D=0)
python gakdeuk_solver.py --n 8 --max 40 --sum 164

# With missing numbers
python gakdeuk_solver.py --n 5 --max 24 --sum 65 --missing 3 10 22 --num-shared 4

# Max duplication coefficient 3, 8 shared vertices (Yukjagakdeuk-like)
python gakdeuk_solver.py --n 6 --max 20 --sum 63 --max-multiplicity 3 --num-shared 8

# Let the MILP choose missing numbers automatically (Chiljagakdeuk-like)
python gakdeuk_solver.py --n 7 --max 35 --sum 120 \
    --auto-missing --missing-count 4 --missing-sum 95 --required 1 2 3 4 5

# Yukjagakdeuk-like: honeycomb adjacency + pairwise shared vertex counts + up-down symmetry + visualization
python gakdeuk_solver.py --n 6 --max 20 --sum 63 \
    --adjacency honeycomb --pair-shared-counts "0-1:2,0-2:2,0-3:2,0-4:2" \
    --symmetry ud --residue-balance --visualize

# Search all five families at once, save to JSON, and visualize
python gakdeuk_solver.py --all --time-limit 180 \
    --max-solutions 1 --visualize --output solutions.json
```

### Automatic S search

```bash
python gakdeuk_solver.py --n 8 --max 40 --search --time-limit 120
```

## Solver Design

`gakdeuk_solver.py` uses Mixed Integer Linear Programming (MILP).

- Variables: `x[v][c] ∈ {0,1}` — whether number `v` belongs to cluster `c`
- Basic constraints:
  - Each cluster has exactly `n` vertices
  - Each cluster sums to `S`
  - Each number belongs to at least 1 and at most `max_multiplicity` clusters
  - Total duplication `D = 5S − T` constraint
  - Optional automatic missing-number selection
- Geometric constraints:
  - Adjacency graph: `cross` / `honeycomb` / `grid` or custom adjacent pairs
  - Pairwise shared vertex counts (`--pair-shared-counts`)
  - Up/down / left/right residue symmetry (`--symmetry`)
- Five-Element constraints:
  - Balanced `mod 5` remainder distribution (`--residue-balance`)
- Output:
  - Multiple solution enumeration (`--max-solutions`)
  - JSON save (`--output`)
  - matplotlib visualization (`--visualize`)

## Notes

- The solver searches for **combinatorial number assignments** overlaid with **geometric constraints** (adjacency graph, pairwise shared vertex counts, symmetry) and **Five-Element constraints** (`mod 5` residue balance).
- With enough geometric constraints, the resulting placements closely resemble traditional diagrams, but perfect reproduction requires additional information such as coordinates, angles, and figure shapes.
- When run with `--all`, the solver uses built-in presets for the traditional conditions (missing numbers, shared structure, sum invariant) of each family.

## Core Generalization Formulas

- Sum invariant: `S = n × μ`
- Duplication equation: `5S = T + D`
- Five-Element mod 5 sum: `WX(r) = 5·m(m−1)/2 + m·r`

For details, see `analysis_report.md` and `blog.md`.
