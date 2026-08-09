# Antipodal-Complement Audit

## Verdict

`v(c)+v(-c)=271` does **not** follow logically from the currently deciphered Naejeok text and the geometric counts alone. It is nevertheless a strong internal reconstruction rule: Lo Shu complements, `通加洛書數六倍`, `54+6=60`, central symmetry, the complement set 1…270, the *Taiyin Numbers* second-method precedent, and the authorial title `洛書六觚圖` all point in the same direction.

The distinction is exact. If the placement is an equivariant Lo Shu expansion, `v∘τ=κ_{271}∘v`, then the antipodal sum is forced. If equivariance is not adopted, it is not forced.

## Hypothesis-removal countermodel

`yukgodo.solver` begins by assigning `(i,271-i)` to every antipodal slot, so it can search under the hypothesis but cannot derive it. The audit swaps values 10 and 124 at `(-9,1)` and `(-9,2)`. It preserves the value set 1…270, all ring sums, all three axis sums, all six side sums, and the solver's sector/ray balance ranges; after the swap only 133 of 135 antipodal pairs sum to 271.

Hence those aggregate conditions are compatible with, but do not imply, antipodal complements. An exhaustive scan of the same kind of local exchange in the English conditional witness finds 504 such countermodels (the independently stored Korean witness yields 514). This is not a single accidental exception in a vast space; it is a structural fact that aggregate constraints do not replace position-value equivariance.

![Local countermodel for aggregate proxy constraints](output/antipodal_countermodel.png)

The figure is nevertheless not a counterexample to the source's placement principle, nor evidence that the source rejects antipodal complements. It is a counterfactual made by deliberately removing `v∘τ=κ_{271}∘v` for the test. It blocks a logically derived confidence claim above 90 percent, but is not negative evidence that independently lowers the historical reconstruction assessment.

## Relation to the internal precedent

The *Taiyin Numbers*, second method (二之四), contains the seven-cell **圓束樣式** with its unique center vacated. The six remaining cells form three antipodal pairs. It is the smallest in-book model of the same structural move as `271→270=2×135`. It increases the historical plausibility of an equivariant extension; it does not replace a direct Yukgodo position-value instruction.

Run `python3 -m yukgodo.antipodal_audit` to reproduce the countermodel.
