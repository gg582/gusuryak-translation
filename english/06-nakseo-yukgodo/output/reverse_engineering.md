# 洛書六觚圖 — Reverse-Engineering Rules & Commentary Cross-Check

Testing reconstructed optimal solutions for compressive generation rules
and cross-checking against manuscript commentary fragments.

## 1. Position of the Reconstructed Solution

- Target function lower bound: 6.0 (achieved).
- Cell overlap with another seed (42) optimum: **0/270**.
- Multiple valid layouts exist; the reconstructed diagram is one specimen.

## 2. Reverse-Engineering Attempts

| Candidate Rule | Method | Result |
|---|---|---|
| Ring-walk AP (mod 271) | 270 steps per ring | Failed — best match 16.7% |
| Linear model v ≡ a+b·k+c·j | 271³ space scan | Failed — 9/270 cells |
| mod 6 class balance | 6-class distribution per ring | Imbalanced — no fingerprint |
| Antipodal pair sequence | Spiral order run | None — max 2 pairs |
| Ray difference symmetry | Opposite ray comparison | Sign flip — antipodal consequence |
| Siamese-type local rule | Shift + correction pair | Failed — 6/269 transitions |
| 添六 construction hypothesis | ±6 mod 271 spiral (192 variants) | Refuted — best penalty 27672 |

## 3. Commentary Passages Cross-Check

| Passage | Reading | Status | Evidence |
|---|---|---|---|
| 共積二百七十 | 270 cells are filled | confirmed | value set 1..270 over 270 cells (validated) |
| 虛一則二百七十數 | voiding the one leaves 270 numbers | confirmed | center cell (0,0) unused |
| 校計周五十四數 | counting the perimeter gives 54 | confirmed | outermost ring has 54 cells (= 六九五十四) |
| 通加洛書數六倍 | six times the Luoshu number (1+..+9=45) = 270 | confirmed | total cells 270 = 6×45 |
| 十九爲中觚數也 | the central row has 19 | confirmed | 中觚 19 cells, sum 2439 = 9×271 |
| 置外周添六 | outward, each ring grows by six cells | confirmed (cell-count reading) | ring k has 6k cells (6,12,...,54) |
| 置外周添六 (value-rule reading) | place the values adding six | refuted | all 192 ±6 (mod 271) spiral variants fail (hypotheses.py best penalty 27672); best per-ring AP match 16.7% |
| 置外周五十四，以九乘之得四百八十六 / 折半加九得二百五十二 | multiply outer perimeter 54 by 9 to get 486, halve and add 9 to get 252 | transcription confirmed (algebraic check passed) | geometric area formula: 54 * 9 / 2 + 9 = 243 + 9 = 252. Geometrically matches trapezoid sum (10 + 18) * 9 = 252. Re-deciphered from early AI misreading |
| 倍之得五百사 / 折半淂二百五두 | double 252 to get 504, halve to get 252 | transcription confirmed (algebraic check passed) | 252 * 2 = 504 and halving back to 252. Discarded early AI pseudo-transcription misreading of 506 |
| 合從九目淂二百五十二不倍 / 去中觚 | combine 9 rings excluding central axes to get 252, not doubled | transcription confirmed (algebraic check passed) | excluding 18 non-central axis cells from 270 total ring cells gives 252 |
| 寄左 / 序左 | placement order instructions (decipherment complete) | unresolved (interpretation) | character decipherment 100% complete, but algorithmic mathematical placement meaning remains unresolved |
| 以算遠則係以六 | mathematical calculation instruction (decipherment complete) | unresolved (interpretation) | character decipherment complete, but contextual mathematical function requires further research |

## 4. Verdict: Can the algorithm be confirmed?

The algorithm body cannot be confirmed from present evidence. The geometric skeleton (271/270/54/19/252) and sum conditions match the commentary exactly, but no placement rule trace survives in any reconstructed optimum. 192 evaluated 添六 value-placement models are refuted. While character decipherment of 寄左/序左 is 100% complete, their algorithmic mathematical interpretation remains open for ongoing research.

### What is confirmed

- The geometric skeleton: 271 cells (虛一 → 270), perimeter 54, 10 cells
  per side, 中觚 19 cells.
- The sum conditions: antipodal pairs 271, rings 813k, sides 1355,
  axes 2439, wedges 6097/6098, rays 1219/1220.
- Phrases like 添六 and 寄左 relate to cell-count calculations and order
  instructions rather than a direct value-placement formula.

### What remains unconfirmed

- Assigning specific values to cells (body of Naejeok Method).
- Character decipherment of 寄左/序左/以算遠則係以六 is complete,
  but their exact mathematical algorithmic interpretation remains open.
