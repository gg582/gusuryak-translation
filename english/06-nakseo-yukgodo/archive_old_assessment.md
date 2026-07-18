# Archive: Old Assessment of Nakseo Yukgodo (○ = Illegible Character and the 504 Theory)

This document is preserved to archive the historical assessment and numeric analysis prior to the adoption of the new reading (○ = sentence-initial/terminal mark).

## 1. Overview of the Old Assessment (Illegible ○ and the 504 Theory)

In earlier OCR scans and translation assessments, the `○` at the end of the phrase "二百五十二倍之得五百○" was treated as an illegible or damaged placeholder character.
* **Numeric Correction Hypothesis**:
  * Doubling (`倍之`) `二百五十二` (252) mathematically yields 504.
  * Hence, the `○` in `得五百○` was interpreted as a worn-away representation of the character for 4 (e.g., 四).
  * Under this reading, the source figure was settled as **504** and incorporated as a cross-check term in the naejeokbeop calculation chain.

## 2. Interpretation Based on the Old Assessment

* **The 252 Cross-Check Route**:
  * 252 = 271 − 19 (the remaining cell count excluding the 中觚 19 cells).
  * 504 (2 × 252) was interpreted as a cross-check checking twice the area outside the 中觚.
* **Traces Left in Earlier Documents**:
  * The notation "二百五十二倍之得五百○ (252×2=504) confirmed" in the conclusion of `output/hypotheses.json` and in the §3 table of `output/reverse_engineering.md`.
  * The verdict in `README.md` that "confirming the body of the naejeokbeop requires a clearer edition" (retaining uncertainty because the identity of ○ was unresolved).

## 3. Refutation and Updates Under the New Assessment

* **New OCR Reading Results**:
  * The `○` is determined to be a **sentence-initial/terminal punctuation mark**, not a numeral. (In the *Gusuryak*, the number zero is written exclusively as '零'.)
  * Consequently, the source text must be read with a break after **得五百 (500)**. The number 504 does not exist in the source text.
* **Reclassification of the Calculation Chain**:
  * As the source figure is updated to 500, the 252 × 2 = 504 route is discarded.
  * 500 and 506 (五百六) are reclassified as Tier 3 (deferred) because they are isolated from the main chain (54 → 60 → 10 → 20 → 19 → 252 → 271 → 270) and cannot be uniquely determined due to multiple possible 2-op generation formulas.
  * The main naejeokbeop chain has reached Tier-1 (confirmed) status via the new OCR, narrowing down the items requiring a clearer edition solely to the tail figure (得五百) and the 序左 order directive.
