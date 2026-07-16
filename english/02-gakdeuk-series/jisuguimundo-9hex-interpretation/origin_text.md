# Jisuguimundo (Hexagonal Tortoise Problem) — Original Text Interpretation

> **Translation order:** Chinese original → Korean first translation → English first translation.  
> The Korean version is in the corresponding Korean folder.

---

## 1. Chinese original

> 六子各得九十三數  
> 九宮共得八百三十七數  
> 中眷三宮，三宮爲主則  
> 左右十二子 分爲二宮 若爲以  
> 四正爲四宮，中間六子合爲一宮  
> 凡九宮化爲十二宮

---

## 2. English first translation

- **六子各得九十三數**
  - Partial sum of six numbers is 93.
  - (Each hexagon is made of six vertices whose values sum to 93.)

- **九宮共得八百三十七數**
  - Sum of all nine clusters is 837.
  - (The nine hexagon sums together total 9 × 93 = 837.)

- **中眷三宮，三宮爲主則**
  - Center manages 3 groups, 3 groups are major.
  - (The central three hexagons govern the rest; three principal groups form the core.)

- **左右十二子 分爲二宮 若爲以**
  - 12 numbers are divided into two groups, that means (if we take these as the basis).
  - (The 12 left/right vertices can be split into two palaces.)

- **四正爲四宮，中間六子合爲一宮**
  - 4 orthogonal directions are 4 groups, the center 6 numbers are a single group.
  - (The four cardinal directions form four palaces, and the six intermediate vertices are grouped as one palace.)

- **凡九宮化爲十二宮**
  - Commonly, that nine groups form 12 groups.
  - (The original nine hexagons can be reinterpreted as twelve palace units.)

---

## 3. Numerical cross-check

- 30 distinct numbers (1–30) are written on the graph → **三十子作**.
- Each of the nine hexagons uses 6 vertices, so the structure uses 54 positions → **五十四子用**.
- Therefore the overlap count is 54 − 30 = **24 positions**, explained by the shared vertices of the tiling.

These checks are performed by `solve_jisu_9hex.py` and `analyze_jisu_9hex.py`.
