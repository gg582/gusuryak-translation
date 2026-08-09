# The Shared 3×3 Lo Shu Rule Across the Nakseo Diagrams

The stored data for 洛書九九圖, 洛書五九圖, and 洛書七九圖 each retain the same 3×3 Lo Shu control array, up to rotation or reflection:

\[
\begin{matrix}8&1&6\\3&5&7\\4&9&2\end{matrix}.
\]

Its opposite pairs sum to 10 and its central 5 is the unique fixed point. This shows that the Lo Shu array is repeatedly used as a control structure, not merely as a title ornament.

The construction of 洛書九九圖 additionally partitions its outer values 10…81 into 36 complement pairs summing to 91, using three such pairs plus a center-dependent correction pair to balance every nine-cell cluster at 369. Complement pairs are therefore an explicit construction technique in the Nakseo family.

For Yukgodo, `通加洛書數六倍` lifts `k↔10-k` to `6k↔6(10-k)`, whose two members always sum to 60. The Naejeok calculation begins exactly with `54+6=60`. Together with the central-vacancy pairing precedent of 圓束樣式, this materially strengthens the reconstruction rule for a diagram explicitly entitled 洛書六觚圖.

The precise logical criterion is supplied by [Nakseo Generalization](../../nakseo-generalization/README.md): an equivariant placement `v∘τ=κ∘v` forces complement pairs; the aggregate geometry alone does not.

## Where equivariance appears in the other Nakseo diagrams

This cannot be assessed by counting only favorable examples. `python3 tests/test_nakseo_family_audit.py` compares the actual stored coordinates and values of all three diagrams.

| Layer | Nakseo Gugudo | Nakseo Ogudo | Nakseo Chilgudo | Result |
| --- | --- | --- | --- | --- |
| 3×3 control array | holds | holds | holds | all have `v(p)+v(τp)=10` and central 5 |
| Global position-value equivariance over every expanded cell | fails | fails | fails | tested at totals 82, 34, and 64 respectively |
| Complement pairs used as a construction device | holds | not directly audited here | not directly audited here | Gugudo explicitly uses pairs totaling 91 |

The first full-expansion failures are `17+71=88` in Gugudo (not 82), `23+13=36` in Ogudo (not 34), and `31+58=89` in Chilgudo (not 64). Because the existing Chilgudo transcription contains some values reconstructed under its documented rule, this is not a claim about a universal original rule for that diagram; it is a check that the stored diagram data do not show full positional equivariance.

The exact common denominator is therefore not "every expanded cell repeats the same complement placement." What all three diagrams repeat is the position-involution/value-complement equivariance of the **3×3 Lo Shu control layer**. Gugudo then adds a separate local construction using 91-complement pairs. Yukgodo antipodal complements may be an interpretation that extends this control layer to 270 cells, but the other expanded diagrams are not direct precedents already doing the same thing. This negative result deliberately limits the evidence to its actual scope.

## Compound-condition threshold experiment

`python3 tests/test_equivariance_threshold_audit.py` simultaneously imposes: the 271/270/135 Yukgodo geometry; the value set 1...270; the Lo Shu opposite sum 10 and central 5; the documented 91-complement construction of 洛書九九圖; `6k+6(10-k)=60`; complement closure within every Yukgodo ring; the three antipodal orbits of 圓束樣式; and every current non-antipodal solver balance (rings, axes, sides, sectors, and rays).

A countermodel still exists. Moreover, an exhaustive scan of local exchanges that swap only two values with the same ring, axis, and side membership leaves **more than 500** countermodels. This is not one rare exception at the edge of a vast solution space: it is a structural gap in aggregate proxy constraints, which do not preserve a position-value correspondence.

![Local countermodel for aggregate proxy constraints](output/antipodal_countermodel.png)

This figure is not a counterexample to the source's placement principle. The exchange is a modern counterfactual that deliberately breaks the very condition under examination, `v∘τ=κ_{271}∘v`; it does not claim that the Naejeok text permits such an exchange. It establishes only that the present **compound proxy conditions** cannot logically derive antipodal complements and hence cannot independently support a confidence claim above 90 percent. The countermodel is not independent negative evidence that the author chose against equivariant placement.

If a conservative numerical wording is retained, this keeps the approximately 85 percent interpretive reconstruction assessment from being promoted above 90 percent; it supplies no reason, by itself, to lower the estimate below 85 percent. Adding `v∘τ=κ_{271}∘v` immediately forces the rule, but that is an independently adopted historical placement principle, not a new consequence of the other conditions.
