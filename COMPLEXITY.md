# Complexity Scope and a Proven Reduction

This document separates results proved for the repository's concrete diagrams
from claims about generalized placement problems.

## The proved statement

Define **GENERAL-EQUAL-SUM-PLACEMENT** as follows. The input contains positive
integer weights `a_1, ..., a_{3m}`, `m` pairwise disjoint groups, group size 3,
and a target `B`. The question is whether every group can receive three input
weights whose sum is `B`, using every weight exactly once.

This problem is strongly NP-complete by a direct polynomial identity reduction
from **3-PARTITION**:

1. A 3-PARTITION instance is a multiset `A = {a_1, ..., a_{3m}}` with
   `sum(A) = mB` and `B/4 < a_i < B/2`.
2. Create one Gakdeuk group for each of the `m` target groups, set every group
   size to 3, copy the weights unchanged, and set the common sum to `B`.
3. A valid Gakdeuk placement is exactly a partition of `A` into `m` triples of
   sum `B`, and vice versa. The map is the identity and is polynomial-time.
4. A certificate is the group assignment, which can be checked in polynomial
   time. Therefore the problem is in NP, and the reduction proves strong
   NP-completeness.

The strong NP-completeness of 3-PARTITION is a standard result of Garey and
Johnson (1978/1979); see the reference below.

## What this does not prove

The reduction does **not** prove NP-completeness for a fixed historical graph,
for the consecutive set `1..N`, or for the exact overlap pattern of any one
Gusuryak diagram. Those restricted problems may be easier, and this repository
does not claim a reduction for them. The concrete diagrams have polynomial-time
verification because their sums, coverage, multiplicities, and graph invariants
can be checked directly.

Accordingly, the README classifications use these labels:

- **P**: a supplied finite diagram is verified directly.
- **Proved NP-complete**: the arbitrary-weight, variable-group generalization
  above, or another reduction explicitly supplied here.
- **Open / not proved here**: a fixed-topology or consecutive-number variant
  for which no complete reduction is included.

## Reproducible checks run in this repository

`python3 complexity/verify_polynomial_checks.py` currently reports:

- both 6x6 Yukyukdo source arrays: normal magic squares, line sum 111;
- both 9x9 Gusudo source arrays: normal magic squares, line sum 369;
- the five 10-row Baekja source blocks: the first four fail the normal-set
  check and the final mother-child block passes it; the first diagram contains
  two component blocks, which is why the script reports five blocks for four
  named diagrams;
- all eight corrected 10x10 files in the Korean and English editions: values
  1..100 exactly once and every row, column, and main diagonal equal to 505;
- both Korean and English hex-grid geometry test suites: exit status 0.

The script also times the direct checks at several matrix sizes. Those timings
are regression evidence for the stated scan implementations, not a substitute
for the proof above.

## References

- [Garey and Johnson, "'Strong' NP-Completeness Results" (JACM, 1978)](https://doi.org/10.1145/322047.322058)
- [Journal of the Operational Research Society: strong NP-completeness of 3-PARTITION](https://doi.org/10.1057/jors.2013.11)
