# 구수략 퍼즐 모음 — 한국어판

《구수략(九數略)》 등 고전 문헌에 전해지는 한·중 수학 도상을 현대 조합론 관점으로 재정의하고, 검증 코드와 시각화 자료를 정리한 저장소의 한국어판입니다.

- **english/** — 영문판 보고서, 코드, 이미지
- **korean/** — 한국어판 보고서, 코드, 이미지

각 언어판 아래에서 퍼즐은 다음과 같은 계열로 구분됩니다.

1. **01-saodo-family** — 하도·낙서 mod‑5 색칠 전통 도상
2. **02-gakdeuk-series** — "각자 얻는다"는 의미의 각득(各得) 퍼즐
3. **03-magic-squares** — 고전 마방진 및 수정 완성
4. **04-unification** — 위 네 계열을 특수 사례로 포함하는 일반화 프레임워크
5. **05-extra-five** — 추가 각득 도안 5종
6. **06-nakseo-yukgodo** — 낙서육고도와 270칸 육각 격자 분석
7. **07-extra-two** — 추가 도안 2종
8. **08-modn-antipodal** — 위치 대칭 보수쌍 도안의 mod N 잔여류 일반화 (교차 장 분석)

---

## 두 가지 해석: 각득 vs. 사오도

`01-saodo-family/`에 포함된 낙서사구도와 낙서오구도는 두 가지 방식으로 해석됩니다. 이 저장소에서는 두 해석을 모두 다루며, 상호 변환 표는 아래 문서에 정리되어 있습니다.

- `korean/01-saodo-family/사오도와-각득의-상호해석/saodo_gakdeuk_dual_reading.md`
- `english/01-saodo-family/saodo-gakdeuk-dual-reading/saodo_gakdeuk_dual_reading.md`

### 1. 각득(各得) 해석

- **사자각득(四子各得)**: 낙서사구도의 9개 궁 각각이 4개의 수를 받아 합이 42.
- **오자각득(五子各得)**: 낙서오구도의 9개 궁 각각이 5개의 수를 받아 합이 85.
- **칠자각득(七子各得)**: 낙서칠구도의 9개 궁 각각이 7개의 수를 받아 합이 224 (=7×32). 1~63까지의 수를 중복 없이 분할합니다.

주요 특징:
- 부분합 불변량 (예: 사자각득 42, 오자각득 85)
- 중복 계수 방정식
- 블록 디자인과 겹침 구조
- 그래프 이론적 구조 (중심 코어, 4방향 확장, 사이클)

### 2. 사오도(四/五道) 해석

- **사도(四道)**: 사방(동·서·남·북), 사계, 4‑cycle, 각 궁 4자.
- **오도(五道)**: 오행(수·화·목·금·토), 5방위, 각 궁 5자.
- **九宫(낙서九宫)**: 3×3 낙서 마방진 형태의 9궁 공간.

핵심 포인트:
- mod‑5 잉여류에 의한 5개 오행 분류
- 5궁에서 9궁으로의 전이
- 순환 구조와 상호작용 수
- 전통 우주론적 상징 배경

---

## 어느 해석이 전산적 재해석에 더 유용한가?

| 기준 | 각득 해석 | 사오도 해석 |
|---|---|---|
| 수학적 일반성 | 높음: 부분합 불변량을 와 MILP 탐색으로 일반화 가능 | 낮음: 특정 4/5 우주론 틀에 제한 |
| 검증 가능성 | 높음: 합, 중복, 그래프 불변량을 기계적으로 검증 가능 | 낮음: 상징 관계에 해석 여지 존재 |
| 전산 형식화 | 부분합·발생 구조를 바로 표현할 수 있음 | 상징·방위 언어를 먼저 형식화해야 함 |
| 현대적 활용 용이성 | 높음: 조합론·그래프 이론에 직접 대응 | 낮음: 형식화 전에 번역 작업 필요 |

**현대 관점**에서는 각득 해석이 보다 선진적이라고 볼 수 있습니다. 관찰 가능한 불변량을 분리하고, 매개변수화된 퍼즐군의 일원으로 삼을 수 있기 때문입니다.

사오도 해석은 원문의 상징·방위 언어를 보존하는 역할을 합니다. 이는 분석
목적의 차이지 근세 수학의 우열 판단이 아닙니다.

두 해석은 원문 주석에 모두 존재합니다. , 는 각득 해석이며, , , 오행 분류는 사오도 해석에 해당합니다. 따라서 두 시각은 경쟁 관계라기보다 **같은 도상을 보는 상호 변환 가능한 두 관점**이라 할 수 있습니다.

---

## 낙서칠구도(洛書七九圖) 해석 요약

낙서칠구도는 9개 궁에 각각 7개의 수를 배치한 **칠자각득(七子各得)** 구조입니다.

- 사용 수: 1~63을 중복 없이 분할
- 각 궁 합: **224** (=7×32)
- 9궁 총합: **2016**

현재 전사본에는 몇몇 오류가 있습니다. 중심 6번 궁은 합이 **174**이며, 23·38·43이 중복되고 45·51·58이 누락되었습니다.

### 교정된 9궁 배치
| 궁 (중심) | 7개 수 | 합 |
|---|---|---:|
| 4 | 4, 22, 27, 31, 37, 43, 60 | 224 |
| 9 | 9, 10, 15, 36, 45, 54, 55 | 224 |
| 2 | 2, 17, 28, 29, 39, 47, 62 | 224 |
| 3 | 3, 16, 26, 30, 40, 48, 61 | 224 |
| 5 | 5, 14, 23, 32, 41, 50, 59 | 224 |
| 7 | 7, 20, 24, 34, 38, 44, 57 | 224 |
| 8 | 8, 11, 12, 35, 49, 53, 56 | 224 |
| 1 | 1, 18, 19, 25, 46, 52, 63 | 224 |
| 6 | 6, 13, 21, 33, 42, 51, 58 | 224 |

바뀐 부분: 9번 궁의 23→51, 36→58, 2번 궁의 43→36, 38→45.

## 백자 계통과 추가 도안

`03-magic-squares/`에는 육육도·구수도와 10×10 백자 계통의 원 배열,
검산 결과, 교정 배열이 들어 있습니다. 10×10 교정 배열은 1부터 100까지를
한 번씩 사용하고 모든 행·열·대각선의 합이 505입니다. 원 전사본에서 중복·누락이
확인된 배열은 인쇄본 간 차이 또는 필사·검수 오류 가능성을 주석으로 남겼습니다.

`05-extra-five/`에는 다음 도안이 있습니다.

- `기책용팔도/`, `범수용오도/`, `장책용칠도/`, `중상용구도/`, `중의용육도/`
- 영문 대응 경로: `english/05-extra-five/`

고정 도안의 합·중복·자리 수 검증은 P이고, 임의 크기의 동일합 배치 존재 문제는
일반화하면 제약 분할 문제로 다뤄집니다.

`06-nakseo-yukgodo/`에 대한 상세 정보는 아래의 별도 요약 섹션을 참고하십시오.


`07-extra-two/`에는 `중괘용팔도/`와 `후책용구도/`가 있으며, 팔진도에는
원 전사본과 별도의 수치 교정본을 함께 보존합니다.

---

## 지수귀문도 9hex (Hexagonal Tortoise Problem) 해석 요약

`korean/02-gakdeuk-series/지수귀문도-9hex-원문해석/`에 독립 폴더로 정리돼 있습니다.

- 사용 수: 1~30, 각 1회
- 정육각형 9개, 각 6정점 합: **93**
- 9육각형 총합: **837**
- 작업 구분: 30작 / 54용, 중복 24개, 중복 가중 합 `372`

### 분석 흐름
1. 원문 한문 → 한국어 1차 번역 → 영어 1차 번역 (`origin_text.md`)
2. MILP 솔버로 합 `93` 해 확보 (`solve_jisu_9hex.py`)
3. 다양한 모듈로 잉여 분류 및 공간 분포 분석 (`analyze_jisu_9hex.py`)
4. CRT 기반 재구성 (mod 3×4, 3×5, 4×5)
5. 각 육각형을 회전 객체로 보고 클러스터 별 회전 분석 ()

---

## 낙서육고도(洛書六觚圖) 해석 요약

`korean/06-nakseo-yukgodo/` 및 `english/06-nakseo-yukgodo/`에 정리되어 있습니다.

- **격자 구조**: 반지름 9 육각 격자, 전체 271칸 (중심 虛一 제외 시 270수 배치)
- **주석 수치**: 270(共積), 54(외주), 19(中觚), 252 (주 사슬 합류 노드), 270 = 6×45(洛書數六倍)
- **목표 조건**: 점대칭 보수 쌍 합 271, 고리 k 합 813k, 변당 합 1355, 축 합 2439, 섹터 합 6097/6098, 광선 합 1219/1220

### 분석 결론
1. **기하 및 칸 수 검증**: 주석의 수치들은 기하 격자의 불변량과 일치하며, 중심 본체 계산 사슬은 새 OCR 판독을 통해 1급 확정(Tier 1)에 도달했습니다.
2. **배치 규칙의 반증**: 添六을 값 배치 규칙(±6 mod 271 나선 등)으로 해석하는 모든 건설 가설은 반증되었습니다.
3. **알고리즘의 불확정성**: 주어진 조건을 만족하는 최적해(벌점 6.0)가 다수 존재하고(시드 간 일치 칸 수 0/270) 이 표본들에 어떠한 선형·등차 흔적도 남지 않으므로, 배치 순서 구절(寄左/序左) 및 꼬리 수치(得五百)의 복원에는 더 선명한 판본이 필요합니다.

---


## 흥미로운 탐구 포인트

- `korean/04-unification/misc-interesting-points.md`
- `english/04-unification/misc-interesting-points.md`

다루는 주제: 작업·사용 간극, mod 2 균형, 9궁→12궁 재해석, 지수귀문도의 적합도 경관, 1700년대 근세 수학자들의 배치 방법 등.

---

## 클러스터별 회전 분석

모든 퍼즐에 대해 회전 분석을 실행하려면 아래 명령을 사용합니다.

Saved cluster: figures/rotation_cluster_C1.png
Saved cluster: figures/rotation_cluster_C2.png
Saved cluster: figures/rotation_cluster_C3.png
Saved cluster: figures/rotation_cluster_C4.png
Saved cluster: figures/rotation_cluster_C5.png
Saved overview: figures/rotation_overview.png
============================================================
Per-cluster rotation analysis: Chiljagakdeuk (Seven-Each-Gets)
============================================================

Cluster: C1
  Cyclic order (7 elements): 2 -> 29 -> 1 -> 24 -> 34 -> 11 -> 19
  Sum: 120
  Residue pattern (mod 5): F-M-W-M-M-W-M
  No nontrivial rotational invariance.
  Note: center=2, direction=top

Cluster: C2
  Cyclic order (7 elements): 3 -> 6 -> 33 -> 23 -> 13 -> 34 -> 8
  Sum: 120
  Residue pattern (mod 5): Wd-W-Wd-Wd-Wd-M-Wd
  No nontrivial rotational invariance.
  Note: center=3, direction=left

Cluster: C3
  Cyclic order (7 elements): 5 -> 22 -> 7 -> 20 -> 30 -> 26 -> 10
  Sum: 120
  Residue pattern (mod 5): E-F-F-E-E-W-E
  No nontrivial rotational invariance.
  Note: center=5, direction=center

Cluster: C4
  Cyclic order (7 elements): 4 -> 15 -> 28 -> 9 -> 18 -> 32 -> 14
  Sum: 120
  Residue pattern (mod 5): M-E-Wd-M-Wd-F-M
  No nontrivial rotational invariance.
  Note: center=4, direction=right

Cluster: C5
  Cyclic order (7 elements): 1 -> 35 -> 16 -> 21 -> 24 -> 6 -> 17
  Sum: 120
  Residue pattern (mod 5): W-E-W-W-M-W-F
  No nontrivial rotational invariance.
  Note: center=1, direction=bottom

Global rotational symmetry for Chiljagakdeuk (Seven-Each-Gets)
--------------------------------------------------
NOTE: These are geometric cluster-center mappings under a counterclockwise rotation. They describe where each cluster's center moves; they do NOT imply the labels/stars inside the clusters are preserved or that the puzzle has a true label-rotation symmetry.
  90° counterclockwise rotation:
    C1 -> C2
    C2 -> C5
    C3 -> C3 (fixed)
    C4 -> C1
    C5 -> C4
  180° counterclockwise rotation:
    C1 -> C5
    C2 -> C4
    C3 -> C3 (fixed)
    C4 -> C2
    C5 -> C1
  270° counterclockwise rotation:
    C1 -> C4
    C2 -> C1
    C3 -> C3 (fixed)
    C4 -> C5
    C5 -> C2

전체 디렉터리에서 한 번에 실행하려면:



### 출력물
- `rotation_report.txt` — 회전 순서, 잉여 패턴, 불변량, 전체 대칭성
- `rotation_cluster_*.png` — 클러스터별 원형 시각화
- `rotation_overview.png` — 전체 클러스터 요약 그림

---

## 기여 방법

1. 이 저장소를 포크합니다.
2. 번역·코드·시각화 자료를 개선합니다.
3. Pull Request를 통해 제안합니다.

감사합니다!
