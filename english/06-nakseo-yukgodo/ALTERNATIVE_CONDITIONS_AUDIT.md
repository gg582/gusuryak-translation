# Competing Conditions Beyond Antipodal Complements

## Purpose and common basis

This audit does not fix `v(c)+v(-c)=271` as its only starting point. Six condition families are implemented as alternatives, all retaining a one-time use of `1…270`, the central vacancy (`虛一`), the 271-cell hexagon, and nine rings.

```bash
python3 tests/test_alternative_models.py
python3 -m yukgodo.alternative_models
```

`balance_penalty_side_wedge_ray` is the absolute deviation from the same side, sector, and ray targets used for the existing witness. A lower value means less disruption of that modern balance objective; it is not by itself evidence of authorial intent. Axis and ring deviations are reported separately.

## Implemented competitors and first reproducible run

| Model | Exact enforced condition | Side/sector/ray penalty | Axis deviation | Ring `813k` deviation | Antipodal pairs summing 271 |
| --- | --- | ---: | ---: | ---: | ---: |
| Internal antipodal-complement principle | Every antipodal positional pair sums to 271 | 6 | 0 | 0 | 135 / 135 |
| Opposed-region aggregates only | Preserve ring, axis, side, sector, and ray aggregates; release antipodes | 6 | 0 | 0 | 133 / 135 |
| Intra-ring complement pairs | Adjacent pair within every ring sums to 271; no paired slots are antipodal | 10 | 2 | 0 | 0 / 135 |
| Global non-antipodal complement pairs | A cross-ring non-antipodal matching sums to 271 | 7 | 1 | 2740 | 0 / 135 |
| Sixfold rotation-orbit sum | Every sixfold rotation orbit sums to 813 | 127 | 2 | 0 | 25 / 135 |
| One 45-cell unit + fixed six-cycle value transform | The same six-cycle transformation generates all 45 rotation orbits, each totaling 813 | 300 | 0 | 0 | 0 / 135 |

These are fixed-seed, reproducible first comparison values. The models have broad solution spaces, so the experiment distinguishes mathematical compatibility from proximity to the current balance objective; it is not a proof of global optimality.

## Scope of each model

1. **Non-antipodal complement pairs** are easy to realize mathematically, but the choice of matching is arbitrary unless a source specifies it.
2. **Intra-ring complement pairs** automatically give ring sums `813k`. They fit the ring structure and `逓加洛書數六倍`, but require an independent reason to choose adjacent pairings.
3. **Sixfold rotation-orbit sum 813** naturally fits rings of size `6k` and automatically preserves their sums. No currently read text says `六轉` or specifies orbit total 813.
4. **Opposed-region aggregates only** already have a penalty-6 countermodel. Aggregate invariants cannot replace a cell-level positional rule.
5. **Nine Lo Shu rings plus a separate placement method** remains viable in both the countermodel and the intra-ring model. `洛書數六倍` strongly controls ring size/order, but does not by itself choose one value placement.
6. **Generating six sectors from one 45-cell unit** is implementable, but demanding a fixed value transformation has the highest cost against the current balance objective. That is relative objective cost, not a textual disproof.

## The immediately preceding Cheonsu Yong-o reprint

The stored transcription for the Cheonsu Yong-o material immediately preceding Yukgodo reads:

> 去中宮十五
>
> 外合得二百一十六
>
> 無宮各得五十四爲六九之數
>
> 二十二子作二十五子用同前

It contains two direct numerical bridges:

\[
216=4\times54,\qquad54=6\times9.
\]

If the reprint is read as deliberately related to Yukgodo, it most strongly supports:

- `去中宮` together with `虛一`: calculate the outer structure after removing or excluding a center.
- **Equal aggregates of outer regions**: partial sums of 54 build the total 216. This is a direct internal precedent for aggregate-region balance and for ring control separated from a placement method.
- `五十四爲六九之數`: a numerical and lexical bridge to Yukgodo's outer perimeter 54 and `6×9`.

It does not directly prescribe cell-wise `v(c)+v(-c)=271`, an arbitrary non-antipodal matching, a sixfold rotational value transform, or a 45-cell sector generator. The repository's Cheonsu Yong-o diagram analysis explicitly labels itself a mathematical rule-variation model, so its modern left-right totals and five-phase patterns are not promoted to source instructions.

## Present comparison

| Family | Mathematical compatibility | Direct link to the preceding reprint | Internal support for a value-position correspondence |
| --- | --- | --- | --- |
| Antipodal-complement reconstruction principle | Very good | Indirect: compatible with centre removal and `54=6×9` | Strongest: Lo Shu complement constructions plus the exact 135-pair correspondence |
| Opposed-region aggregates only | Very good | **Closest direct link**: `外合` and `各得五十四` | Weak as a cell-level rule |
| Intra-ring complements | Good | Compatible with `54=6×9` | No source rule selecting the pairs |
| Global non-antipodal complements | Good | No direct link | Matching choice is arbitrary |
| Sixfold orbit sums | Good | Compatible with 6 and 9; no rotation instruction | Interesting geometric competitor |
| 45-cell sixfold generation | Feasible | No direct link | Strongest additional assumption |

The Cheonsu Yong-o reprint therefore substantially reinforces **aggregate balance and the immediate `54=6×9` precedent**. It does not replace the antipodal-complement reconstruction principle; instead, it makes the alternative space precise: ring control and regional aggregates can be distinct from the value-placement rule. At present the internal antipodal-complement principle still preserves the Lo Shu family's positional/value construction precedents with the fewest additional choices, while the experiments again confirm that aggregates alone do not logically force it.
