# Miscellaneous Interesting Points

This document collects the most intriguing and not-easily-resolved findings
from our exploration of the gusuryak-style diagrams—Nakseo Sagudo/Ogudo/Chilgudo,
Saja/Oja/Yuk/Pal/Gu-jagakdeuk, and the Jisuguimundo (Hexagonal Tortoise
Problem).

---

## 1. The gap between made (作) and used (用)

**Why it is interesting:**
In the 30-node Jisuguimundo, 30 distinct numbers (作) are placed into 54
hexagon positions (用). Hence 24 positions are shared. The original phrase
"三十子作， 五十四子用" is therefore not rhetoric but an exact combinatorial
statement.

**Why it is not easily resolved:**
Vertices with higher multiplicity belong to several clusters simultaneously,
so changing one number perturbs several constraints at once. The central
region becomes extremely sensitive, making trial-and-error optimisation very
hard.

---

## 2. Perfect mod 2 balance

**Why it is interesting:**
The 30-node Jisuguimundo contains exactly 15 odd and 15 even numbers. Moreover,
the odd nodes are fairly evenly spread with respect to the vertical and
horizontal reflection axes.

**Why it is not easily resolved:**
The balance is not just 15:15. Because every hexagon must sum to the odd
constant 93, each hexagon must contain an odd number of odd values (1, 3, or
5). Satisfying this for all nine hexagons while keeping the global balance is
highly non-trivial.

---

## 3. The ambiguity of 9 palaces → 12 palaces

**Why it is interesting:**
The phrase "凡九宮化爲十二宮" suggests that the nine hexagon palaces can be
reinterpreted as twelve palaces. This is not a mere numerical conversion but
a shift in spatial grouping perspective.

**Why it is not easily resolved:**
The original text does not specify the exact composition of the twelve
palaces. A naive count—4 cardinal palaces + 1 middle-6 palace + 2 left/right
palaces + 3 central palaces—gives 10, not 12. Visualising or formalising this
phrase therefore leaves room for interpretation.

---

## 4. The central three palaces govern the rest

**Why it is interesting:**
In the Jisuguimundo, the vertical central column Hex2, Hex5, Hex8 shares
vertices with the six surrounding hexagons and forms the core axis. The text
"中眷三宮， 三宮爲主則" states that these three central palaces are the master.

**Why it is not easily resolved:**
The vertices in the central three hexagons mostly have multiplicity 2 or 3.
Once their values are fixed, the surrounding hexagon sums are heavily
constrained. In practice, the whole solution often branches from the central
region.

---

## 5. The 2·3 modular mutation family

**Why it is interesting:**
The moduli used in the analysis—2, 3, 4, 6, 9, 12—are all generated from the
base moduli 2 and 3. This mirrors the interplay of the four-way (2-power) and
three-way (3-power) structures in the diagrams.

**Why it is not easily resolved:**
Why 2 and 3, not 5 or 7? The geometry (hexagon = 6 = 2×3, nine palaces = 3²)
offers an explanation, but the general condition under which an arbitrary set
of moduli preserves the same invariants remains open.

---

## 6. Higher moduli recovered by CRT

**Why it is interesting:**
Modulo 12 is fully recovered from modulo 3 and modulo 4 by the Chinese
Remainder Theorem. Likewise, mod 3 × mod 5 → mod 15 and mod 4 × mod 5 →
mod 20.

**Why it is not easily resolved:**
CRT only works for coprime pairs. Combinations like mod 2 × mod 4 or mod 3 ×
mod 6 cannot be directly reconstructed. Classifying which modulus pairs give
meaningful spatial information and which are redundant is still an open task.

---

## 7. Gakdeuk vs. Saodo dual readings

**Why it is interesting:**
Nakseo Sagudo can be read either as "Sajagakdeuk" (four numbers per group
summing to 42) or as a nine-palace 42-sum structure. Similarly, Nakseo Ogudo
is both "Ojagakdeuk" (five numbers per group summing to 85) and a nine-palace
total of 765.

**Why it is not easily resolved:**
Are the two readings always equivalent? Some diagrams may admit a gakdeuk
reading but not a saodo reading, or vice versa. The necessary and sufficient
conditions for both readings to coexist have not been fully characterised.

---

## 8. NP-Complete / NP-Hard classification

**Why it is interesting:**
The arbitrary-weight, disjoint-group equal-sum subproblem is strongly
NP-complete by the explicit 3-PARTITION identity reduction in
`COMPLEXITY.md`. This does not classify every fixed topology in the repository.

**Why it is not easily resolved:**
The exact complexity class of concrete existence problems such as Jisuguimundo
or Nakseo Sagudo is not settled here. Their supplied instances have direct
polynomial-time verification; no claim about their restricted generalized
existence problems is made without a topology-preserving reduction.

---

## 9. The rugged fitness landscape of the HTP

**Why it is interesting:**
According to the GECCO 2003 paper by Choe, Choi & Moon, the Hexagonal
Tortoise Problem has a fitness-distance correlation rougher than that of a
1,000-node TSP. In other words, there are many local optima.

**Why it is not easily resolved:**
This ruggedness means that plain GAs or simple local search stagnate on large
instances. The paper's hybrid GA uses problem-specific heuristics—consecutive
exchange, tabu search, nearby search—for this very reason. When and why these
heuristics fail is still not fully understood.

---

## 10. The sophistication of early 18th-century mathematics

**Why it is interesting:**
Diagrams like the Jisuguimundo appeared in Korean publications around 1700.
Finding a valid assignment of 30 numbers into 9 hexagons with constant sum 93
demonstrates considerable combinatorial skill.

**Why it is not easily resolved:**
No record explains how they found the solution. Was it exhaustive trial and
error, or did they use some symmetry or invariant? The surviving commentaries
offer hints, but a complete reconstruction remains difficult.

---

## 11. Absence of rotational symmetry yet global order

**Why it is interesting:**
Rotation analysis shows that none of the nine individual hexagons has a
non-trivial rotational invariant. However, the whole graph has a geometric
180-degree pairing of hexagon centres.

**Why it is not easily resolved:**
The interior of each hexagon is rotationally irregular, yet the global
structure is symmetric. How this "local disorder, global order" is reconciled,
and how it relates to the number of solutions, is not yet clear.

---

## 12. The huge number of optimal solutions

**Why it is interesting:**
The GECCO 2003 paper estimates more than 6×10⁸ optimal solutions among the
16! possible assignments for the 16-node HTP. The solution space is therefore
highly multimodal.

**Why it is not easily resolved:**
The exact number of optimal solutions for the 30-node Jisuguimundo is
unknown. Enumerating all optimal solutions, or understanding the structural
relations among different solutions with the same magic constant, is
computationally prohibitive.

---

## 13. Directions for modern reinterpretation

**Why it is interesting:**
These diagrams connect to several modern fields: magic squares, graph
labelling, combinatorial design, and algebraic graph theory.

**Why it is not easily resolved:**
No unified theory yet identifies which general mathematical structure each
diagram exemplifies. The Jisuguimundo may be viewed as a kind of "magic
labelling on a regular graph", but generalising it to arbitrary regular graphs
is non-trivial.

---

## 14. The equal-axis/equal-ring/equal-ray star family (Beomsu, Jangchaek, Jungsang)

**Why it is interesting:**
The three star diagrams of 05-extra-five form a single design family. With
`a` axes of `L` cells each: `N = a(L−1)+1` values `1..N`, center value = `L`
(the 用 number in the diagram's name), axis sum `S = (T+(a−1)L)/a`, and
concentric ring sum `R = (T−L)/a` hold exactly in all three cases
(2×5, 3×7, 4×9). Moreover all three realize the axis sums through the same
device — a same-ray sum invariant (Beomsu: arm 10; Jangchaek: spoke-pair 61;
Jungsang: ray 69).

**Why it is not easily resolved:**
Does such an equal-axis/equal-ring/equal-ray placement exist for arbitrary
`(a, L)`? Must the center value be exactly `L`? The pattern is observed in
three instances; no general existence theorem or construction is known.

---

## 15. Gichaek-yongpaldo's 50/50 splits and the golden-ratio spectrum

**Why it is interesting:**
In Gichaek-yongpaldo (four octagons, each summing to 100), every octagon
splits into four shared vertices and four unique vertices summing to exactly
50 = S/2 each. The eight shared vertices split alternately into the central
square (50) and the outer quadruple (50), and the concentric ring sums are
50·50·100·100. The graph is bipartite with largest adjacency eigenvalue
φ² ≈ 2.618, the square of the golden ratio.

**Why it is not easily resolved:**
Why does the "25-symmetry" hold — each octagon's opposite-pair sums pairing
into complements of 50? Is the placement satisfying the 50/50 split unique
(up to symmetry)? Whether this placement is a special case of a known
combinatorial design is unknown.

---

## 16. The complement-pair asymmetry of Jungui-yongyukdo

**Why it is interesting:**
In Jungui-yongyukdo (four overlapping groups, each summing to 51), the top
and bottom groups decompose perfectly into three complement pairs summing to
17 = N+1 (51 = 3×17), while the left and right groups admit no such perfect
matching. Instead, the shared and unshared 8-value sets both sum to exactly
68 = T/2, and the row sums by y-coordinate form a palindrome
(17, 13, 17, 21, 21, 17, 13, 17).

**Why it is not easily resolved:**
A fully symmetric placement in which all four groups satisfy the complement
device is not realized in this data. Is it impossible in principle, or did
the source edition carry a different placement? The question is decidable by
MILP search but has not yet been carried out.

---

## 17. The unresolved 演積 1148 of Jungsang-yonggudo

**Why it is interesting:**
The source records the duplication-inclusive total as 「演積一千一百四十八」,
yet every natural accounting based on the measured values — axes plus bare
rings (4×147 + 4×138 = 1140), plus the center once (1149), or the full
用72 accounting (1176) — fails to give exactly 1148. The other two source
figures (本積 561, 各得 147) match the measurements exactly, so 1148 stands
out alone.

**Why it is not easily resolved:**
We cannot decide between transcription damage (the policy applied to the
03-magic-squares series) and an unidentified accounting convention
(e.g. 7×164, 4×287). Resolving it requires comparison with another edition
or with neighboring commentary on the same page.

---

## 18. The multiplicity of Nakseo Yukgodo optima and the unconfirmability of the naejeokbeop

**Why it is interesting:**
The reconstructed optimum of Nakseo Yukgodo (penalty floor 6.0) is not
unique: an optimum found under another seed agrees with it in 0 of 270
cells. Many placements satisfy the commentary's sum conditions, and the
reconstructed diagram is only one specimen. Measurements confirm that no
constructive trace survives in it — no ring APs, no linear position rule,
no mod-6 class fingerprint, no consecutive pair assignment, and no
Siamese-style local rule.

**Why it is not easily resolved:**
The sum conditions alone cannot identify the original placement, and the
placement-order rule (the 寄左/序左 phrase) cannot be recovered from the
reconstruction. All value-rule readings of 添六 are refuted, so what can be
confirmed extends only to the geometric skeleton, the sum conditions, and
the refutation list. The naejeokbeop calculation chain has reached Level 1 confirmation for the core chain via new OCR, but confirming the naejeokbeop text itself (placement-order instructions and the tail segment) requires a
clearer edition of the commentary — a concrete instance of the problems in
§10 and §12.

---

## Summary

These diagrams are far more than curiosities: they link combinatorics,
symmetry, modular arithmetic, computational complexity, and evolutionary
computation. Questions such as "Why are 2 and 3 the base moduli?", "What is
the exact rule for transforming nine palaces into twelve?", and "How did
early modern mathematicians construct these solutions?" remain fully or
partially open. The newly added questions — "Does the star family exist for
arbitrary (a, L)?", "Is Gichaek-yongpaldo's 50/50 placement unique?", "Is a
fully symmetric Jungui-yongyukdo placement possible?", "What does the
source's 演積 1148 count?", and "Can the Nakseo Yukgodo placement-order rule
ever be recovered?" — likewise remain open.
