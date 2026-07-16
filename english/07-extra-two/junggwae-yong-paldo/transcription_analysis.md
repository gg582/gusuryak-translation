# 八陣圖 — Transcription Error Investigation

After verifying whether the original 八陣圖 data form a complete arrangement of 1..64 with each 陣 having the same sum, **the current transcription contains multiple errors**. This document explores whether those errors are simple transcription mistakes or intended *byeon-jin* (變陣) transformations, and presents a minimal correction.

—-

## 1. Problems in the Current Data

The 8 formations recorded in `visualize_wrong_origin.py` and their sums are as follows.

| Position | Form | Numbers | Sum | Deviation from 260 |
|—-|—-|—-|—-|—-|
| Row 1, Col 1 | vertical | 40, 14, 57, 9, 8, 56, 25, 41 | 250 | **-10** |
| Row 1, Col 2 | horizontal | 14, 51, 19, 46, 33, 30, 62, 3 | 258 | **-2** |
| Row 1, Col 3 | vertical | 45, 24, 52, 4, 13, 61, 22, 36 | 257 | **-3** |
| Row 2, Col 1 | vertical | 48, 32, 49, 16, 17, 35, 1, 64 | 262 | **+2** |
| Row 2, Col 3 | vertical | 37, 21, 60, 12, 5, 53, 28, 44 | 260 | 0 |
| Row 3, Col 1 | vertical | 38, 22, 59, 11, 6, 54, 27, 43 | 260 | 0 |
| Row 3, Col 2 | horizontal | 7, 58, 26, 39, 42, 23, 55, 10 | 260 | 0 |
| Row 3, Col 3 | vertical | 47, 31, 50, 2, 15, 63, 18, 34 | 260 | 0 |

- 4 of the 8 formations do not sum to 260.
- The 64 numbers are not all used. **14** and **22** each appear twice, and **20** and **29** are missing.
- The total sum of the 8 formations is 2067, which is 13 less than the sum of 1..64, 2080. This matches the difference between the excess 36 caused by duplication and the deficit 49 caused by omission (49 − 36 = 13).

—-

## 2. Local Exchange Possibility of 33 and 35

When we focus only on Row 1, Col 2 (horizontal) and Row 2, Col 1 (vertical), the two formation sums deviate by exactly ±2.

```text
Row 1, Col 2: 14 + 51 + 19 + 46 + 33 + 30 + 62 + 3 = 258
Row 2, Col 1: 48 + 32 + 49 + 16 + 17 + 35 + 1 + 64 = 262
```

If we swap **33** and **35** between the two formations:

```text
Row 1, Col 2: 258 − 33 + 35 = 260
Row 2, Col 1: 262 − 35 + 33 = 260
```

This local swap normalizes both formations simultaneously without touching other numbers. However, this alone does not solve the problems of Row 1, Col 1 (−10) and Row 1, Col 3 (−3).

—-

## 3. The ±2 Byeon-jin Structure between Row 1, Col 2 and Row 2, Col 1

When the two formations are aligned and compared, a surprising rule appears.

| Row 1, Col 2 | Row 2, Col 1 | Difference |
|—-|—-|—-|
| 3 | 1 | +2 |
| 14 | 16 | −2 |
| 19 | 17 | +2 |
| 30 | 32 | −2 |
| 33 | 35 | −2 |
| 46 | 48 | −2 |
| 51 | 49 | +2 |
| 62 | 64 | −2 |

The two sets do not share the same 16 numbers (Row 1, Col 2 has 3, 14, 19, 30, 33, 46, 51, 62; Row 2, Col 1 has 1, 16, 17, 32, 35, 48, 49, 64), but **corresponding numbers differ by exactly 2**. This is read as a trace of *byeon-jin* (a rule for transforming formations) rather than coincidence.

Moreover, the following 5 pair swaps all make both formations sum to 260.

- 14 ↔ 16
- 46 ↔ 48
- 33 ↔ 35
- 30 ↔ 32
- 62 ↔ 64

Thus Row 1, Col 2 and Row 2, Col 1 are naturally viewed as the same formation arranged in two phases.

—-

## 4. Duplications and Omissions Cannot Be Explained By Byeon-jin

Another defect of the current data is duplications and omissions.

- **14** appears in both Row 1, Col 1 and Row 1, Col 2.
- **22** appears in both Row 1, Col 3 and Row 3, Col 1.
- **20** and **29** do not appear anywhere.

This pattern is hard to explain with the *byeon-jin* concept. If *byeon-jin* is an intended structure, the set of numbers should remain the same while only positions change. That 14 and 22 appear twice and 20 and 29 disappear directly shows numbers were copied incorrectly during transcription/engraving.

In particular, Row 1, Col 1 has sum 250, 10 short of the target. This is a large deviation that cannot be filled by a single pair swap.

—-

## 5. Grounds for Concluding Transcription Errors

Overall, we can judge as follows.

| Observation | Intended *byeon-jin* explanation | Transcription-error explanation |
|—-|—-|—-|
| Row 1, Col 2 ↔ Row 2, Col 1 ±2 correspondence | Possible | Difficult to regard as accidental |
| 33 ↔ 35 local swap | Possible as one example of *byeon-jin* | Same as left |
| 14, 22 duplicated / 20, 29 missing | Inexplicable | Typical copy error |
| Row 1, Col 1 −10, Row 1, Col 3 −3 | Inexplicable by simple *byeon-jin* | Cumulative result of transcription errors |
| Only 4 formations defective, 4 normal | If intended, a more systematic pattern would be expected | Typical of random errors |

Therefore it is reasonable to **conclude that the entire current data set is a transcription error**. The *byeon-jin* relation between Row 1, Col 2 and Row 2, Col 1 is a remnant of the intended mathematical structure in the original text; the remaining discrepancies are damage from the transcription process.

—-

## 6. Minimal Correction

A minimal correction that preserves the original layout structure as much as possible, uses 1..64 exactly once, and restores every formation sum to 260 is as follows.

| Position | Change | Effect |
|—-|—-|—-|
| Row 1, Col 1 | 14 → 20, 25 → 29 | Restores missing 20 and 29; sum +10 |
| Row 1, Col 2 | 33 → 35 | *Byeon-jin* swap with Row 2, Col 1 |
| Row 1, Col 3 | 22 → 25 | Removes duplicated 22; sum +3 |
| Row 2, Col 1 | 35 → 33 | *Byeon-jin* swap with Row 1, Col 2 |

Formation sums after correction:

| Position | Numbers after correction | Sum |
|—-|—-|—-|
| Row 1, Col 1 | 40, 20, 57, 9, 8, 56, 29, 41 | 260 |
| Row 1, Col 2 | 14, 51, 19, 46, 35, 30, 62, 3 | 260 |
| Row 1, Col 3 | 45, 24, 52, 4, 13, 61, 25, 36 | 260 |
| Row 2, Col 1 | 48, 32, 49, 16, 17, 33, 1, 64 | 260 |
| Row 2, Col 3 | (unchanged) | 260 |
| Row 3, Col 1 | (unchanged) | 260 |
| Row 3, Col 2 | (unchanged) | 260 |
| Row 3, Col 3 | (unchanged) | 260 |

This correction swaps a total of 5 values and keeps 59 of the original 64 value-position pairs unchanged (92.2% preserved). Other equivalent minimal corrections exist (for example, swapping 62 ↔ 64 between Row 1, Col 2 and Row 2, Col 1 while not swapping 33 ↔ 35). In this project we adopted the correction that preserves the **33 ↔ 35** *byeon-jin*.

—-

## 7. Conclusion

- The 33 and 35 exchange is one of several possible exchanges constituting an intended *byeon-jin* relation between Row 1, Col 2 and Row 2, Col 1.
- However, the duplication of 14 and 22, the omission of 20 and 29, and the sum mismatches of Row 1, Col 1 and Row 1, Col 3 are **transcription errors** that cannot be explained as *byeon-jin*.
- Therefore the current transcription contains errors, and the above minimal correction restores every formation sum to 260.
- The original transcription visualization (`visualize_wrong_origin.py`) is preserved as-is; the normal-form visualization is generated separately as `visualize_corrected.py`.

—-

## 8. Connection to Other Approaches in the Repository

This investigation follows the same methodologies used across the repository.

### The `corrected.md` approach in the magic-square series

The 10×10 magic squares in `korean/03-magic-squares/` are not regular magic squares in the source text, so the source text is kept as-is and a corrected normal magic square is presented separately in `corrected.md`. The same principle is applied to the Eight-Formation Diagram: the original transcription visualization and the corrected visualization are separated.

### The MILP minimal-correction approach in unified generalization

The MILP solver in `korean/04-unification/base_solver.py` finds a solution that satisfies the original constraints while matching the source arrangement as closely as possible. Applying the same optimization to the Eight-Formation Diagram (objective: maximize preservation of the original 64 value-position pairs) yields a solution that keeps 59 pairs while making every formation sum 260. The adopted correction is the version among those solutions that preserves the 33 ↔ 35 *byeon-jin*.

### The rotation-analysis perspective

`rotation_analysis.py` analyzes rotational invariance within each cluster and global rotation correspondences between clusters. The ±2 correspondence between Row 1, Col 2 and Row 2, Col 1 in the Eight-Formation Diagram is read as an inter-cluster transformation. The judgment that this relation is the intended *byeon-jin* and the remaining mismatches are transcription errors matches the “local order / global damage” distinction emphasized by rotation analysis.
