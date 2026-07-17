# Nakseo Yukgodo (洛書六觚圖) — reverse-engineering the generation rule
# from the final reconstructed diagram, cross-checked with the faint commentary

Starting from the reconstructed optimum (`output/solution.json`), we test
data-driven whether any compressive generation rule survives, and compare
each outcome against the legible fragments of the faint commentary.

## 1. Status of the reconstructed diagram

- Theoretical floor of the search objective: 6.0 (attained).
- Cells agreeing with an optimum found under another seed (42): **0/270**.
- Hence many placements satisfy the conditions; the reconstructed diagram
  is one specimen. The question is whether constructive traces survive in it.

## 2. Reverse-engineering attempts and outcomes

| Candidate rule | Method | Result |
|---|---|---|
| ring-walk AP (any step mod 271) | 270 steps per ring, exhaustive | failed — best match 16.7% |
| coordinate-linear model v ≡ a+b·k+c·j | (a,b,c) over 271³, exhaustive | failed — 9/270 cells |
| mod-6 class balance (添六 fingerprint) | per-ring class counts | unbalanced/inconsistent — no fingerprint |
| constructive pair-assignment order | consecutive runs along the spiral | absent — longest run 2 pairs |
| ray difference rule | opposite-ray comparison | sign reversal — automatic from the pair hypothesis |
| Siamese-style local rule (siamese.py) | primary+fallback move pair | failed — 6 of 269 transitions |
| 添六 construction hypotheses (hypotheses.py) | 192 ±6 mod 271 spiral variants | failed — best penalty 27672 (floor 6.0) |

## 3. Cross-check with the commentary

| Fragment | Reading | Verdict | Evidence |
|---|---|---|---|
| 共積二百七十 | 270 cells are filled | confirmed | value set 1..270 over 270 cells (validated) |
| 虛一則二百七十數 | voiding the one leaves 270 numbers | confirmed | center cell (0,0) unused |
| 校計周五十四數 | counting the perimeter gives 54 | confirmed | outermost ring has 54 cells (= 六九五十四) |
| 通加洛書數六倍 | six times the Luoshu number (1+..+9=45) = 270 | confirmed | total cells 270 = 6×45 |
| 十九爲中觚數也 | the central row has 19 | confirmed | 中觚 19 cells, sum 2439 = 9×271 |
| 置外周添六 | outward, each ring grows by six cells | confirmed (cell-count reading) | ring k has 6k cells (6,12,...,54) |
| 置外周添六 (value-rule reading) | place the values adding six | refuted | all 192 ±6 (mod 271) spiral variants fail (hypotheses.py best penalty 27672); best per-ring AP match 16.7% |
| 二百五十二倍之得五百○ | 252 × 2 = 504 | confirmed (cell-count arithmetic) | 252 = 271 − 19 (excluding 中觚), 504 = 2×252 |
| 寄左 / 序左 | (presumed placement-order rule) | undecidable | seed-42 optimum agrees in 0/270 cells — with many optima, no order information survives in the reconstruction |
| 以算遠則係以六 | (reading uncertain) | undecidable | a clearer edition is needed |

## 4. Verdict: can the algorithm be confirmed?

The algorithm cannot be confirmed from the present evidence. The geometric skeleton (271/270/54/19/252) and the sum conditions (rings 813k, sides 1355, axes 2439, antipodal pairs 271) match the commentary exactly, but no compressive trace of a placement-order rule survives in any reconstructed optimum. All value-rule readings of 添六 are refuted, and the placement-order fragments (寄左/序左) cannot be judged from the reconstruction because optima are plentiful. What can be settled extends only to what the algorithm is NOT; confirming the text of the algorithm itself requires a clearer edition of the commentary.

### What is confirmed

- The geometric skeleton: 271 cells (虛一 → 270), perimeter 54, 10 cells
  per side, 中觚 19 cells.
- The sum conditions: antipodal pairs 271, rings 813k, sides 1355,
  axes 2439, wedges 6097/6098, rays 1219/1220 — consistent with the
  commentary and the 六觚 record of the Hanshu.
- The 添六/寄左-type phrases should be read as cell-count and ordering
  instructions, not as a value-placement rule.

### What remains unconfirmed

- The procedure that assigns values to cells (the body of the seungjeokbeop).
  Since the overlap between reconstructed optima is 0/270, the sum
  conditions alone cannot identify the original placement, and no order
  rule can be recovered from these specimens.
- Confirming the algorithm itself requires a clearer edition of the
  commentary.
