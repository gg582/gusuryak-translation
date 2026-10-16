# 낙서xy도 이름 속의 함수 x → y (not-on-a-textbook)

구수략 낙서(洛書) 계열에서, 낙서육고도(洛書六觚圖)를 제외한 모든 도상은 **낙서xy도(洛書xy圖)**라는 이름을 가지며, 이름의 두 자리 숫자 x와 y가 그대로 계산에 들어간다.

- **x = 각 그룹이 얻는 칸 수(子)**: 공정 몫 규칙 **T = x × (N + 1) / 2**에 들어간다.
- **y = 그룹의 수**: 총 자리 수 用 = **x × y**에 들어간다.

즉 이름 자체가 설계 명세다. "x칸씩 y그룹에 배분한다"는 뜻이며, 실제로 관측된 전 계열에서 用 = x·y, T = x(N+1)/2 두 항등식이 모두 성립한다(아래 스크립트가 assert로 검증한다).

낙서육고도는 이 작명 규칙에서 제외한다. 이름의 숫자 6은 육각형의 변 수(六觚)일 뿐, 나머지 다섯 도상의 x/y 작명 체계와 다른 방식으로 이름에 들어 있기 때문이다.

## 검증 표

| 도상 | x (그룹당 칸 수) | y (그룹 수) | N (作) | 用 = x·y | 그룹 합 T |
|---|---:|---:|---:|---:|---:|
| 낙서사구도 (洛書四九圖) | 4 | 9 | 20 | 36 | 42 |
| 낙서오구도 (洛書五九圖) | 5 | 9 | 33 | 45 | 85 |
| 낙서칠구도 (洛書七九圖) | 7 | 9 | 63 | 63 | 224 |
| 낙서팔구도 (洛書八九圖) | 8 | 9 | 40 | 72 | 164 |
| 낙서구구도 (洛書九九圖) | 9 | 9 | 81 | 81 | 369 |

검산 예: 낙서사구도는 T = 4 × 21 / 2 = 42, 낙서구구도는 T = 9 × 82 / 2 = 369.

참고: 원문 도상 자체(낙서구구도 포함)는 정상적으로 존재하며, 잘못되었던 것은 전사(옮겨 적기) 과정뿐이다.

## 정의역·공역·치역

관측된 계열에서 map x → y를 복원하면:

- **정의역 (domain)**: {4, 5, 7, 8, 9} — 실재하는 도상의 x 값들
- **치역 (image)**: {9} — 모든 관측 y가 9로 일치하므로, 상수함수 가설 y ≡ 9는 현재 데이터로는 기각되지 않는다.
- **공역 (codomain) 후보**:
  - 九宫(구궁) 유일 가설 하에서는 {9} — "낙서 계열은 언제나 아홉 궁 위에 놓인다"는 기하 가정.
  - 산술 게이트(정확 분할 부분류 N = x·y에서 T = x(x·y+1)/2가 정수)만으로는 공역이 강제되지 않는다. x = 6인 가상의 낙서육구도(洛書六九圖)도 게이트를 통과하지만 역사적으로 부재하며, y ≠ 9인 쌍들도 다수 통과한다.

## 스크립트

`nakseo_xy_function.py`는 다음을 수행한다.

- (a) 모든 계열 구성원에 대해 用 = x·y assert
- (b) 모든 계열 구성원에 대해 공정 몫 규칙 T = x(N+1)/2 assert
- (c) 정의역, 관측 y, 치역 출력 및 상수함수 가설 y ≡ 9 검정
- (d) 정확 분할 부분류(N = x·y)의 확장 탐색: x ∈ 1..12, y ∈ 3..12에서 T가 정수인 (x, y) 쌍의 타당성 그리드 출력. x = 6 공백과 y ≠ 9 합격 쌍을 강조.
- (e) 멤버별 중복 자리 D = x·y − N 출력

실행:

```bash
python3 nakseo_xy_function.py
```

실제 출력:

```text
map x -> y from the observed nakseo family:
  domain X       = [4, 5, 7, 8, 9]
  observed y     = [9]
  image  f(X)    = [9]
  constant-function hypothesis (y == 9 for all members): True

extension probe (exact-partition subclass N = x*y):
  grid of y for each x ('.' = infeasible, 'y' = feasible,
  'F' = feasible but historically absent, '*' = observed member)
  x\y |   3   4   5   6   7   8   9  10  11  12
  ----+----------------------------------------
    1 |   F   .   F   .   F   .   F   .   F   .
    2 |   F   F   F   F   F   F   F   F   F   F
    3 |   F   .   F   .   F   .   F   .   F   .
    4 |   F   F   F   F   F   F   *   F   F   F
    5 |   F   .   F   .   F   .   *   .   F   .
    6 |   F   F   F   F   F   F   F   F   F   F
    7 |   F   .   F   .   F   .   *   .   F   .
    8 |   F   F   F   F   F   F   *   F   F   F
    9 |   F   .   F   .   F   .   *   .   F   .
   10 |   F   F   F   F   F   F   F   F   F   F
   11 |   F   .   F   .   F   .   F   .   F   .
   12 |   F   F   F   F   F   F   F   F   F   F

  x = 6 (a hypothetical Nakseo Yuk-gudo 洛書六九圖) passes the gate at y = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12], yet is historically absent.
  pairs with y != 9 that also pass the gate: 78 of 90 feasible pairs
  -> the name-based codomain {9} is NOT forced by arithmetic.

duplication slots D = (用) x*y - (作) N per member:
  Nakseo Sagudo (洛書四九圖): x*y = 36, N = 20, D = 16  (overlap)
  Nakseo Ogudo (洛書五九圖): x*y = 45, N = 33, D = 12  (overlap)
  Nakseo Chilgudo (洛書七九圖): x*y = 63, N = 63, D = 0  (exact partition)
  Nakseo Palgudo (洛書八九圖): x*y = 72, N = 40, D = 32  (overlap)
  Nakseo Gugudo (洛書九九圖): x*y = 81, N = 81, D = 0  (exact partition)

all assertions passed.
```

## 관련 문서

- 통합 핵심을 공유하는 도상들의 공통 특성과 일반화는 ../04-unification 을 참조한다.
