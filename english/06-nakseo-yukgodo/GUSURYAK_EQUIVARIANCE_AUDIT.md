# Audit of Equivariance Across *Gusuryak*

## Criterion

Here equivariance means that a positional involution `tau` and a value complement `kappa_S(x)=S-x` satisfy

\[
v\circ\tau=\kappa_S\circ v.
\]

Equivalently, corresponding positions have a constant value sum `S`. This is stricter than merely placing complement pairs in the same aggregate.

## Auditable inventory

| Category | Diagram and unit | Result | Evidence grade |
| --- | --- | --- | --- |
| Exact position-value equivariance | The 3×3 control arrays of 洛書九九圖, 洛書五九圖, and 洛書七九圖 | Four opposite pairs sum to 10; center is 5 | Directly checked in stored data |
| Exact position-value equivariance | Center palace of 九子各得 | Four pairs sum to 46; center 23 = 46/2 | Directly checked |
| Exact local equivariance | The two horizontal formations of 重卦用八圖 | All eight left-right pairs sum to 65 | Directly checked |
| Complement-pair construction, not global equivariance | Outer values of 洛書九九圖 | 36 pairs totaling 91 are used in construction; the full expanded placement is not equivariant | Directly checked |
| Complement distribution and recombination | Remaining formations of 重卦用八圖 | 65-pairs are split and distributed between formations | Structural check |
| Partial/negative control | 侯策用九圖 | 36 positional-pair sums: 67:1, 68:1, 72:7, 73:16, 74:9, 75:1, 78:1 | No global equivariance |
| Negative control | 範數用五圖 | Four antipodal-pair sums: 9:2, 11:2 | No global equivariance |

Equivariance is therefore not a one-off pattern in the book. It recurs as (1) central symmetry of Lo Shu control arrays, (2) local position-value complement placement, and (3) complement-pair construction and redistribution. At the same time, the negative cases show that the author did not apply full equivariance mechanically to every diagram.

## Revised Yukgodo hypothesis after the transcription corrections

The current transcription baseline is:

- In `六而一得一十乃每一包敉也`, the character is **包**, not 危. The mathematical function of `包敉` is unresolved; the correction does not change the numerical calculation network.
- In `今有方箭束一百四十四隻問外周幾何`, `隻` counts one side of a pair, an unpaired member. Read with the vacant-center 圓束樣式, this strongly indicates counting the individual members of a pair structure.

The revised hypothesis is consequently both stricter and stronger:

1. The Naejeok Method strongly supports the **geometric cell-count calculation** `271=19+2((10+18)/2×9)` for the central row and two trapezoidal regions.
2. `隻` and 圓束樣式 strengthen the in-book precedent for individual members of antipodal pair-orbits after a central vacancy.
3. The auditable diagrams across the book repeatedly use equivariance as a control-array rule, a local placement rule, and a complement-pair construction rule.
4. The Yukgodo text still lacks a literal instruction such as `對觚相合二百七十一`. Thus `v(c)+v(-c)=271` remains a strong reconstruction condition synthesized from the evidence, not a direct transcription.

The key change is not merely that pairs can be counted: `隻` counts **one member of a pair**, bringing the reading closer to a correspondence between positional pairs and value pairs. This linguistic support does not alone calculate the value sum 271, so the logical boundary established by the countermodel audit remains in force.

## Reproduction

```bash
cd korean/06-nakseo-yukgodo
python3 tests/test_gusuryak_equivariance_audit.py
python3 -m yukgodo.gusuryak_equivariance_audit
```

This is an inventory of diagrams whose stored coordinates and values can be checked. It is not an arbitrary percentage of every diagram in *Gusuryak*.
