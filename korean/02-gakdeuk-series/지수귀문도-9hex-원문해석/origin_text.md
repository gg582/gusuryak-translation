# 지수귀문도(地數龜文圖 / Hexagonal Tortoise Problem) 원문 해석

> **번역 순서:** 한문 원문 → 한국어 1차 번역 → 영어 1차 번역  
> (Chinese original → Korean first translation → English first translation)

---

## 1. 한문 원문

> 六子各得九十三數  
> 九宮共得八百三十七數  
> 中眷三宮，三宮爲主則  
> 左右十二子 分爲二宮 若爲以  
> 四正爲四宮，中間六子合爲一宮  
> 凡九宮化爲十二宮

---

## 2. 한국어 1차 번역

- **六子各得九十三數**
  - 6개 수의 부분합이 93이다.
  - (각 육각형을 이루는 6개 정점의 합이 93이다.)

- **九宮共得八百三十七數**
  - 9개의 모든 그룹의 합은 837이다.
  - (9개 육각형의 합을 모두 더하면 9 × 93 = 837이다.)

- **中眷三宮，三宮爲主則**
  - 가운데 중앙의 것이 3개 그룹을 돌보고, 3개 그룹이 주가 되는데
  - (중심 3개 육각형이 나머지를 관장하며, 3개 주요 그룹이 중심 역할을 한다.)

- **左右十二子 分爲二宮 若爲以**
  - 좌우 12자가 2개의 그룹으로 나뉜다는 것은 (만약 이를 기준으로 삼는다면)
  - (좌우에 위치한 12개 정점이 2개 궁으로 분할될 수 있다.)

- **四正爲四宮，中間六子合爲一宮**
  - 4개의 꼭지그룹이 4개의 그룹이므로, 중간 6개 수를 합쳐 1개의 그룹으로 둔다.
  - (4방 정면을 4개 궁으로 보고, 그 사이 중간 6정점을 1개 궁으로 묶는다.)

- **凡九宮化爲十二宮**
  - 무릇 9그룹이 12개 그룹이 된다.
  - (원래 9개 육각형을 12개의 궁 해석 단위로 재구성할 수 있다.)

---

## 3. 영어 1차 번역

- **六子各得九十三數**
  - Partial sum of six numbers is 93.
  - (The six vertices of each hexagon sum to 93.)

- **九宮共得八百三十七數**
  - Sum of all nine clusters is 837.
  - (The nine hexagon sums together total 9 × 93 = 837.)

- **中眷三宮，三宮爲主則**
  - Center manages 3 groups, 3 groups are major.
  - (The central three hexagons govern the rest; three principal groups act as the core.)

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

## 4. 해석상 참고

위 번역은 **1차 번역**이다.  
수학적 검증은 별도의 `analyze_jisu_9hex.py`와 `solve_jisu_9hex.py`를 통해 수행한다.

- 30개의 서로 다른 수(1~30)가 그래프에 적힌다 → **三十子作**.
- 9개 육각형 각각이 6정점을 사용하므로 구조상 쓰이는 자리는 54개 → **五十四子用**.
- 따라서 중복 자리는 54 − 30 = **24개**, 이는 공유 정점들로 설명된다.
