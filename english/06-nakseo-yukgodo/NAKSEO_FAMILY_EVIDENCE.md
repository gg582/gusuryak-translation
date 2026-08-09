# The Shared 3×3 Lo Shu Rule Across the Nakseo Diagrams

The stored data for 洛書九九圖, 洛書五九圖, and 洛書七九圖 each retain the same 3×3 Lo Shu control array, up to rotation or reflection:

\[
\begin{matrix}8&1&6\\3&5&7\\4&9&2\end{matrix}.
\]

Its opposite pairs sum to 10 and its central 5 is the unique fixed point. This shows that the Lo Shu array is repeatedly used as a control structure, not merely as a title ornament.

The construction of 洛書九九圖 additionally partitions its outer values 10…81 into 36 complement pairs summing to 91, using three such pairs plus a center-dependent correction pair to balance every nine-cell cluster at 369. Complement pairs are therefore an explicit construction technique in the Nakseo family.

For Yukgodo, `通加洛書數六倍` lifts `k↔10-k` to `6k↔6(10-k)`, whose two members always sum to 60. The Naejeok calculation begins exactly with `54+6=60`. Together with the central-vacancy pairing precedent of 圓束樣式, this materially strengthens the reconstruction rule for a diagram explicitly entitled 洛書六觚圖.

The precise logical criterion is supplied by [Nakseo Generalization](../../nakseo-generalization/README.md): an equivariant placement `v∘τ=κ∘v` forces complement pairs; the aggregate geometry alone does not.

## Compound-condition threshold experiment

`python3 tests/test_equivariance_threshold_audit.py` simultaneously imposes: the 271/270/135 Yukgodo geometry; the value set 1...270; the Lo Shu opposite sum 10 and central 5; the documented 91-complement construction of 洛書九九圖; `6k+6(10-k)=60`; complement closure within every Yukgodo ring; the three antipodal orbits of 圓束樣式; and every current non-antipodal solver balance (rings, axes, sides, sectors, and rays).

A countermodel still exists. Thus these compound conditions do not logically force antipodal sums of 271, and they do not by themselves justify raising the reconstruction confidence beyond 90 percent. Adding `v∘τ=κ_{271}∘v` immediately forces the rule, but that is an independently adopted historical placement principle, not a new consequence of the other conditions.
