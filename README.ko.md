# 구수략 퍼즐 모음

《구수략(九數略)》 등 고전 문헌에 전하는 한중 수학 도상들을 현대 조합론적으로 재정의하고, 검증 코드와 보고서 및 시각화 자료를 모아둔 저장소입니다.

저장소는 두 개의 언어판으로 구성됩니다.

- **`english/`** — 영문판 보고서, 코드, 그림
- **`korean/`** — 한국어판 보고서, 코드, 그림

각 언어판 아래에서 퍼즐은 다음 계열로 분류됩니다.

1. **first-post / introduction** — 개요와 동기 예시
2. **saodo-family** — 하도/낙서 mod-5 색칠 전통의 도상
3. **gakdeuk-series** — “각자 얻는다”는 뜻의 각득(各得) 퍼즐
4. **magic-squares** — 고전 마방진 및 수정 완성
5. **unification** — 위 계열들을 특수 사례로 포함하는 매개변수화 프레임워크
6. **extra-five / extra-two** — 동일한 각득 원리를 따르는 추가 도상

---

## 현대 조합론적 관점

이 저장소의 퍼즐 몇 가지는 현대 조합론에서 다시 보기에 특히 흥미롭습니다.

- **하도/사오도 5-컬러링**: 5원소 사이클에서 유도한 대칭 그래프 위의 정점 색칠 문제입니다. 색수, 리스트 색칠, 평면 그래프의 4색 정리와 자연스럽게 연결됩니다.
- **각득 계열**: 주어진 그래프 정점에 `1..N`을 배치해 지정된 모든 클러스터가 같은 부분합을 갖도록 하는 라벨링 문제입니다. 마법 라벨링(magic labeling), 안티매직 라벨링, 공정 분할(equitable partition)과 인접합니다.
- **지수귀문도(地數龜文圖)**: 9육각형 → 12궁 변환을 담고 있어, 분할 정제(partition refinement), 분해 가능한 디자인(resolvable design), 잉여류 대칭의 예시를 제공합니다.

---

## 저장소 구조

```text
.
├── LICENSE                                   # 공공재산/권리 포기 선언
├── METHOD.md                                 # 연구 방법론(영문)
├── METHOD.ko.md                              # 연구 방법론(한국어)
├── README.md                                 # 영문판 이 파일
├── README.ko.md                              # 이 파일
├── requirements.txt                          # Python 의존성
├── rotation_analysis.py                      # 공용 회전 분석 유틸리티
├── english/                                  # 영문판
│   ├── README.md
│   ├── LICENSE.md
│   ├── blog_post.en.md                       # 종합 블로그 글
│   ├── english_figure_generators.py          # 공용 그림 유틸리티
│   ├── 00-first-post/                        # 소개 및 자산
│   │   ├── index.md
│   │   └── assets/
│   ├── 01-saodo-family/                      # 하도/낙서 계열
│   │   ├── hado-saodo-5-coloring/            # 하도/사오도 5-컬러링 퍼즐
│   │   ├── nakseo-sagudo/                    # 낙서사구도(洛書四九圖)
│   │   ├── nakseo-ogudo/                     # 낙서오구도(洛書五九圖)
│   │   ├── nakseo-chilgudo/                  # 낙서칠구도(洛書七九圖)
│   │   ├── nakseo-palgudo/                   # 낙서팔구도(洛書八九圖)
│   │   └── saodo-gakdeuk-dual-reading/       # 각득 ↔ 사오도 상호 변환
│   ├── 02-gakdeuk-series/                    # 각득 계열
│   │   ├── chiljagakdeuk-seven-each-gets/    # 칠자각득(七子各得)
│   │   ├── gujagakdeuk-nine-each-gets/       # 구자각득(九子各得)
│   │   ├── paljagakdeuk-eight-each-gets/     # 팔자각득(八子各得)
│   │   ├── ojagakdeuk-five-each-gets/        # 오자각득(五子各得 / 천수용오도)
│   │   ├── yukjagakdeuk-six-each-gets/       # 육자각득(六子各得 / 지수용육도·지수귀문도)
│   │   │   ├── jisu-yong-yukdo/
│   │   │   └── jisu-guimun-and-yongyukdo/
│   │   ├── jisu-guimundo-source-interpretation/  # 지수귀문도 원문 해석
│   │   └── jisuguimundo-9hex-interpretation/ # 30정점 9육각형 지수귀문도
│   ├── 03-magic-squares/                     # 마방진 분석
│   │   ├── 00-basics/                        # 차수별 마방진 기초
│   │   │   ├── 01-3x3-magic-square/
│   │   │   ├── 02-4x4-magic-square/
│   │   │   ├── 03-5x5-magic-square/
│   │   │   ├── 04-6x6-magic-square/ → ../01-yukyukdo-six-six-board/
│   │   │   ├── 05-7x7-magic-square/
│   │   │   ├── 06-8x8-magic-square/
│   │   │   └── 07-9x9-magic-square/ → ../02-gusudo-nine-palace/
│   │   ├── 01-yukyukdo-six-six-board/
│   │   ├── 02-gusudo-nine-palace/
│   │   ├── 03-baekjajasuyin-yang-chakjong/
│   │   ├── 04-baekjasaengseong-sunsu/
│   │   ├── 05-baekjasaengseong-gyosu/
│   │   ├── 06-baekjayin-yang-jamo-chakjong/
│   │   ├── 07-gugusubyeongungyangdo/
│   │   ├── ANALYSIS_SUMMARY.md
│   │   ├── analyze_squares.py
│   │   ├── generate_and_visualize.py
│   │   └── square.md
│   ├── 04-unification/                       # 통합 일반화
│   │   ├── base_solver.py                    # 공용 MILP 베이스 솔버
│   │   ├── unified_solver.py                 # 통합 솔버 진입점
│   │   ├── misc-interesting-points.md        # 흥미로운 탐구 포인트
│   │   ├── saodo-sajagakdeuk-ojagakdeuk-interchange.md  # 사오도 ↔ 사자/오자 변환
│   │   ├── saodo-chiljagakdeuk-generalization/  # Π(p, q, T) 프레임워크
│   │   └── gakdeuk-principle-shared-properties/ # 각득 퍼즐 공유 특성
│   ├── 05-extra-five/                        # 추가 5종
│   │   ├── gichaek-yong-paldo/
│   │   ├── beomsu-yong-odo/
│   │   ├── jangchaek-yong-chil-do/
│   │   ├── jungsang-yong-gudo/
│   │   └── jungui-yong-yukdo/
│   └── extra-two/                            # 추가 2종
│       ├── junggwae-yong-paldo/
│       └── huchaek-yong-gudo/
└── korean/                                   # 한국어판
    ├── README.md
    ├── LICENSE.ko.md
    ├── blog_post.ko.md                       # 종합 블로그 글
    ├── 01-saodo-family/                      # 하도/낙서 계열
    │   ├── 하도사오도-지만-사실-5-컬러링-문제/
    │   ├── 낙서사구도/
    │   ├── 낙서오구도/
    │   ├── 낙서칠구도/
    │   ├── 낙서팔구도/
    │   └── 사오도와-각득의-상호해석/
    ├── 02-gakdeuk-series/                    # 각득 계열
    │   ├── 구자각득/
    │   ├── 팔자각득/
    │   ├── 칠자각득-일곱이-따로따로/
    │   ├── 오자각득(천수용오도)/
    │   ├── 육자각득(지수용육도와 지수귀문도)/
    │   ├── 지수귀문도-9hex-원문해석/
    │   └── 지수귀문도-원문-해석/
    ├── 03-magic-squares/                     # 마방진 계열
    │   ├── 00-basics/
    │   ├── 01-yukyukdo/
    │   ├── 02-gusudo/
    │   ├── 03-baekjajasuyin-yang-chakjong/
    │   ├── 04-baekjasaengseong-sunsu/
    │   ├── 05-baekjasaengseong-gyosu/
    │   ├── 06-baekjayin-yang-jamo-chakjong/
    │   ├── 07-gugusubyeongungyangdo/
    │   ├── ANALYSIS_SUMMARY.md
    │   ├── analyze_squares.py
    │   ├── generate_and_visualize.py
    │   └── square.md
    ├── 04-unification/                       # 통합 일반화
    │   ├── misc-interesting-points.md
    │   ├── 사오도-사자각득-오자각득-상호변환.md
    │   ├── 사오도와-칠자각득의-일반화/
    │   └── 각득 원리를 따르는 퍼즐들의 공유 특성 및 일반화/
    ├── 05-extra-five/                        # 추가 5종
    │   ├── 기책용팔도/
    │   ├── 범수용오도/
    │   ├── 장책용칠도/
    │   ├── 중상용구도/
    │   └── 중의용육도/
    └── extra-two/                            # 추가 2종
        ├── 중괘용팔도/
        └── 후책용구도/
```

---

## 퍼즐 계열

### 01. 사오도 계열 (하도/낙서 전통)

mod-5 잉여류에 따라 분할된 대칭 배치를 기반으로 한 도상들입니다.

| 퍼즐 | 영문 경로 | 한국어 경로 |
|------|-----------|-------------|
| 하도/사오도 5-컬러링 | `english/01-saodo-family/hado-saodo-5-coloring/` | `korean/01-saodo-family/하도사오도-지만-사실-5-컬러링-문제/` |
| 낙서사구도(洛書四九圖) | `english/01-saodo-family/nakseo-sagudo/` | `korean/01-saodo-family/낙서사구도/` |
| 낙서오구도(洛書五九圖) | `english/01-saodo-family/nakseo-ogudo/` | `korean/01-saodo-family/낙서오구도/` |
| 낙서칠구도(洛書七九圖) | `english/01-saodo-family/nakseo-chilgudo/` | `korean/01-saodo-family/낙서칠구도/` |
| 낙서팔구도(洛書八九圖) | `english/01-saodo-family/nakseo-palgudo/` | `korean/01-saodo-family/낙서팔구도/` |
| 각득 ↔ 사오도 상호 해석 | `english/01-saodo-family/saodo-gakdeuk-dual-reading/` | `korean/01-saodo-family/사오도와-각득의-상호해석/` |

핵심 사실:
- 하도/사오도 원소 집합 `V = {1, 2, …, 20}`, 총합 `Σ V = 210`.
- 5개 잉여 클래스(수, 화, 목, 금, 토)의 합은 각각 `34, 38, 42, 46, 50`.
- 낙서사구도는 20개 노드의 이분 그래프로, 외곽 합토니안 20-cycle과 합 42인 내곽 4-cycle을 가집니다.
- 낙서오구도는 `1`부터 `33`까지를 한 번씩 9개 십자형 궁에 배치합니다. 각 궁의 합은 `85`이고, 중복 가중 총합은 `765`입니다.
- 낙서칠구도는 `1`부터 `63`까지를 3×3 낙서 궁격에 배치합니다. 각 궁은 7개 수를 받아 합 `224`(= 7 × 32)를 목표로 합니다. 현재 데이터에는 전사 오류(중복 `23, 38, 43`, 누락 `45, 51, 58`)가 있으며, 9개 궁 모두의 합을 `224`로 복원하는 교정 분할이 디렉토리에 포함되어 있습니다.
- 낙서팔구도는 `1`부터 `80`까지를 5개의 8×4 블록 구조에 배치하여 각 궁/클러스터의 합이 `164`가 되도록 합니다.

#### 낙서칠구도의 두 가지 읽기

**각득 해석.** 이 도상은 `1`부터 `63`까지의 정수를 9개의 7원소 블록으로 분할한 것이며, 각 블록의 합은 `224`(= 7 × 32, 1..63의 평균)입니다. 사구도·오구도와 달리 중복이 없으므로 `作 = 用 = 63`이고 중복 가중 합 `D = 0`입니다. 현재 데이터는 손상되어 있어 중심 `6`인 궁의 합은 `174`이고, 나머지 8개 궁만 `224`를 만족합니다. 54개 주변 수 중 50개를 유지한 교정 분할은 다음과 같습니다.

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

**사오도 해석.** 9개 중심수는 고전적인 3×3 낙서 마방진을 이루어 九宫(구궁)의 공간적 골격을 제공합니다. 각 궁이 7개 수를 받는 것은 9궁 체계 안에서 북두칠성/7기를 배분한 형태로 읽을 수 있습니다. 모든 궁의 합이 `224`가 되면 궁 단위 3×3 격자의 각 행·열·대각선 합이 모두 `672`가 됩니다.

---

### 02. 각득 계열 (各得, “각자 얻는다”)

수 집합을 클러스터로 나누고, 모든 클러스터가 동일한 목표 합을 갖도록 하는 도상들입니다.

| 퍼즐 | 영문 경로 | 한국어 경로 |
|------|-----------|-------------|
| 칠자각득(七子各得) | `english/02-gakdeuk-series/chiljagakdeuk-seven-each-gets/` | `korean/02-gakdeuk-series/칠자각득-일곱이-따로따로/` |
| 구자각득(九子各得) | `english/02-gakdeuk-series/gujagakdeuk-nine-each-gets/` | `korean/02-gakdeuk-series/구자각득/` |
| 팔자각득(八子各得) | `english/02-gakdeuk-series/paljagakdeuk-eight-each-gets/` | `korean/02-gakdeuk-series/팔자각득/` |
| 오자각득(五子各得, 천수용오도) | `english/02-gakdeuk-series/ojagakdeuk-five-each-gets/` | `korean/02-gakdeuk-series/오자각득(천수용오도)/` |
| 육자각득(六子各得, 지수용육도·지수귀문도) | `english/02-gakdeuk-series/yukjagakdeuk-six-each-gets/` | `korean/02-gakdeuk-series/육자각득(지수용육도와 지수귀문도)/` |
| 지수귀문도 원문 해석 | `english/02-gakdeuk-series/jisu-guimundo-source-interpretation/` | `korean/02-gakdeuk-series/지수귀문도-원문-해석/` |
| 지수귀문도 9hex | `english/02-gakdeuk-series/jisuguimundo-9hex-interpretation/` | `korean/02-gakdeuk-series/지수귀문도-9hex-원문해석/` |

핵심 사실:
- **칠자각득**: 5개 클러스터, 각 7개 수, 합 `120`.
- **구자각득**: 5개 3×3 궁격, 각 9개 수, 합 `207`; 각 궁 모서리 합 `92`.
- **팔자각득**: 5개 8-cycle, 각 8개 수, 합 `164`.
- **오자각득**: `1..24`에서 `3, 10, 22`를 제외한 21개 수를 천수용오도 형태로 배치. 총합 `265`, 좌우 영역 합 각 `86`.
- **육자각득**: `1..20`을 5개 정육각형에 배치. 각 합 `63`, 공유 정점 8개, 평면 그래프 `V = 20`, `E = 24`, `F = 6`.
- **지수귀문도 원문 해석**: 지수귀문도(地數龜文圖) 원문에 대한 해석 자료.
- **지수귀문도 9hex**: 30정점 9육각형 배치, 마법 상수 `S = 93`. 30개 서로 다른 수를 作하고 54개 위치를 用하여 중복은 24개. 디렉토리에 정확한 그래프, 검증된 해, 모듈러 분석, CRT 재구성, 육각형별 회전 분석이 포함되어 있습니다.

---

### 03. 마방진 계열

원문에 기록된 고전 마방진 도상과 현대 검증, 수정 완성안입니다.

| 퍼즐 | 영문 경로 | 한국어 경로 |
|------|-----------|-------------|
| 마방진 기초 | `english/03-magic-squares/00-basics/` | `korean/03-magic-squares/00-basics/` |
| 육육도(六六圖) | `english/03-magic-squares/01-yukyukdo-six-six-board/` | `korean/03-magic-squares/01-yukyukdo/` |
| 구수도(九數圖) | `english/03-magic-squares/02-gusudo-nine-palace/` | `korean/03-magic-squares/02-gusudo/` |
| 백자자수음양착종도 | `english/03-magic-squares/03-baekjajasuyin-yang-chakjong/` | `korean/03-magic-squares/03-baekjajasuyin-yang-chakjong/` |
| 백자생성순수도 | `english/03-magic-squares/04-baekjasaengseong-sunsu/` | `korean/03-magic-squares/04-baekjasaengseong-sunsu/` |
| 백자생성교수도 | `english/03-magic-squares/05-baekjasaengseong-gyosu/` | `korean/03-magic-squares/05-baekjasaengseong-gyosu/` |
| 백자음양자모착종도 | `english/03-magic-squares/06-baekjayin-yang-jamo-chakjong/` | `korean/03-magic-squares/06-baekjayin-yang-jamo-chakjong/` |
| 구구변운양도 | `english/03-magic-squares/07-gugusubyeongungyangdo/` | `korean/03-magic-squares/07-gugusubyeongungyangdo/` |

핵심 사실:
- 마방진 상수: `M_6 = 111`, `M_9 = 369`, `M_10 = 505`.
- **육육도**(`6×6`)와 **구수도**(`9×9`)는 정규 마방진입니다. `6×6` associated square는 불가능합니다.
- **구수도** 예시 1은 완전 associated(`a_{i,j} + a_{8-i,8-j} = 82`)입니다. 예시 2는 associated로 교정 가능합니다.
- 4개의 `10×10` 도상은 정규 마방진이 아니며, `1..100`로 모든 행·열·대각선 합을 `505`로 만드는 교정안이 `corrected.md`에 제공되어 있습니다.
- **구구변운양도**는 九宫(구궁) 프레임워크를 기반으로 한 추가 변환 도상입니다.
- 6개 도상 모두 pan-diagonal은 아닙니다.

---

### 04. 통합 일반화

앞선 퍼즐들을 특수 사례로 포함하는 매개변수화 프레임워크입니다.

| 퍼즐 | 영문 경로 | 한국어 경로 |
|------|-----------|-------------|
| 사오도–칠자각득 일반화 | `english/04-unification/saodo-chiljagakdeuk-generalization/` | `korean/04-unification/사오도와-칠자각득의-일반화/` |
| 각득 원리 공유 특성 | `english/04-unification/gakdeuk-principle-shared-properties/` | `korean/04-unification/각득 원리를 따르는 퍼즐들의 공유 특성 및 일반화/` |
| 사오도 ↔ 사자/오자 변환 | `english/04-unification/saodo-sajagakdeuk-ojagakdeuk-interchange.md` | `korean/04-unification/사오도-사자각득-오자각득-상호변환.md` |
| 흥미로운 탐구 포인트 | `english/04-unification/misc-interesting-points.md` | `korean/04-unification/misc-interesting-points.md` |

핵심 사실:
- `Π(p, q, T)` 프레임워크는 사오도 색 클래스와 칠자각득을 모두 포착합니다.

| 퍼즐 | p | q | T |
|------|---|---|---|
| 칠자각득 | 5 | 6 | 120 (균일) |
| 사오도 색 클래스 | 5 | 3 | 34, 38, 42, 46, 50 (가변) |

- 각득 원리 공유 특성 디렉토리는 구자각득, 오자각득, 육자각득, 칠자각득, 팔자각득 전체를 `S = n × μ`, 중복 방정식 `5S = T + D` 등 공통 불변량으로 통합하고, 새 배치를 탐색하는 MILP 솔버를 제공합니다.
- `base_solver.py`와 `unified_solver.py`는 통합 실험을 위한 공용 MILP 인프라입니다.

---

### 05. 추가 5종 및 추가 2종

동일한 각득식 등분 합 제약을 따르는 추가 도상들입니다.

| 퍼즐 | 영문 경로 | 한국어 경로 |
|------|-----------|-------------|
| 기책용팔도(奇策用八圖) | `english/05-extra-five/gichaek-yong-paldo/` | `korean/05-extra-five/기책용팔도/` |
| 범수용오도(泛水用五圖) | `english/05-extra-five/beomsu-yong-odo/` | `korean/05-extra-five/범수용오도/` |
| 장책용칠도(長策用七圖) | `english/05-extra-five/jangchaek-yong-chil-do/` | `korean/05-extra-five/장책용칠도/` |
| 중상용구도(象上用九圖) | `english/05-extra-five/jungsang-yong-gudo/` | `korean/05-extra-five/중상용구도/` |
| 중의용육도(中用六圖) | `english/05-extra-five/jungui-yong-yukdo/` | `korean/05-extra-five/중의용육도/` |
| 중괘용팔도(中卦用八圖) | `english/extra-two/junggwae-yong-paldo/` | `korean/extra-two/중괘용팔도/` |
| 후책용구도(後策用九圖) | `english/extra-two/huchaek-yong-gudo/` | `korean/extra-two/후책용구도/` |

이 디렉토리들은 추가 도상의 원본 데이터, 분석, 시각화를 모아둡니다.

---

## 두 가지 읽기: 각득 해석과 사오도 해석

`01-saodo-family/`의 퍼즐들은 두 가지 방식으로 읽힙니다. 이 저장소에서는 두 해석을 모두 다루며, 상호 변환은 다음 문서에 정리되어 있습니다.

- `korean/01-saodo-family/사오도와-각득의-상호해석/saodo_gakdeuk_dual_reading.md`
- `english/01-saodo-family/saodo-gakdeuk-dual-reading/saodo_gakdeuk_dual_reading.md`

### 각득(各得) 해석

도상을 “모든 부분집합이 같은 합을 갖도록 수를 배치한 것”으로 봅니다.

- **사자각득(四子各得)**: 낙서사구도의 9개 궁이 각각 4개 수를 받아 합 `42`.
- **오자각득(五子各得)**: 낙서오구도의 9개 궁이 각각 5개 수를 받아 합 `85`.
- **칠자각득(七子各得)**: 낙서칠구도의 9개 궁이 각각 7개 수를 받아 합 `224`, `1..63`을 중복 없이 분할.

이 해석이 강조하는 것:
- 부분합 불변량(사구도 `42`, 오구도 `85`)
- 중복 방정식 `k·S = T + D`(`k`: 궁 수, `S`: 궁 합, `T`: 서로 다른 수 총합, `D`: 중복 가중 합)
- 블록 디자인과 겹침 구조(인접 궁끼리 원소 공유)
- 그래프 이론적 구조(중앙 코어, 4방향 확장, 합토니안 사이클)

### 사오도(四/五道) 해석

도상을 4(사)와 5(오)의 상호작용, 즉 전통 오행·방위 우주론의 틀 안에서 봅니다.

- **사도(四道)**: 사방(동서남북), 사계, 4-cycle, 각 궁 4자.
- **오도(五道)**: 오행, 5방위, 각 궁 5자.
- **九宫(낙서九宫)**: 3×3 낙서 마방진 형태의 9궁 공간. 낙서칠구도에서 가장 뚜렷하며, 각 궁이 7개 수를 받고 중심수들이 고전 마방진을 이룹니다.

이 해석이 강조하는 것:
- mod 5 잉여류에 의한 5개 오행 분류
- 5궁에서 9궁으로의 변화(五宫化爲九宫)
- 순환 구조(右旋)와 상호작용 수(`1890`, `765`)
- 전통 우주론적 상징의 배경

### 어느 해석이 더 선진적인가?

“선진적”의 기준에 따라 다릅니다.

| 기준 | 각득 해석 | 사오도 해석 |
|---|---|---|
| 수학적 일반성 | 높음: `Π(p, q, T)`와 MILP 탐색으로 일반화 | 낮음: 특정 4/5 우주론 틀에 묶임 |
| 검증 가능성 | 높음: 합·중복·그래프 불변량을 기계적으로 검증 | 낮음: 상징 관계에 해석의 여지 |
| 당대 학술적 자연스러움 | 낮음: 부분집합 합 일치는 당시 표준 언어가 아님 | 높음: 오행·방위·4/5 수비학은 주류 학문 도구 |
| 현대적 다루기 쉬움 | 높음: 조합론·그래프 이론에 직접 대응 | 낮음: 형식화 전 번역 작업 필요 |

현대 관점에서는 각득 해석이 더 선진적입니다. 관찰 가능한 불변량을 분리하고 매개변수화된 퍼즐족의 일원으로 삼기 때문입니다. 근세 조선·청대 학술 관점에서는 사오도 해석이 더 자연스럽고 완결적이었을 것입니다. 당시 수를 우주론에 배치하는 것이 가장 익숙한 설명 방식이었기 때문입니다.

두 해석은 경쟁 관계가 아니라 **같은 도상을 보는 상호 변환 가능한 두 시각**입니다.

### 현대적으로 재해석하려면

상징 해설보다는 다음 관찰 가능한 특징들에 집중하는 것이 가장 생산적입니다.

1. 사용된 수와 총합
2. 궁/클러스터 구조
3. 부분합 불변량
4. mod 5 잉여류(오행)
5. 중복/겹침 계수
6. 그래프 구조
7. 매개변수화된 배치

---

## 부분 문제의 계산 복잡도

역사적 도상 자체는 작고 구체적이라 검증은 모두 다항 시간입니다. 아래 분류는 임의 크기 또는 임의 목표값으로 **자연스럽게 일반화**했을 때를 나타냅니다.

| 퍼즐 / 계열 | 부분 문제 | 복잡도 | 이유 / 비고 |
|---|---|---|---|
| 하도/사오도 5-컬러링 | 체크섬 210과 mod-5 색 클래스 검증 | **P** | 직접 합산과 잉여 검사 |
| 하도/사오도 5-컬러링 | 주어진 기하 슬롯 그래프 라벨링이 제약을 만족하는지 결정 | **NP-complete** | k ≥ 3 색칠 및 exact-cover형 슬롯 제약을 포착 |
| 하도/사오도 5-컬러링 | 대합 `σ, τ`와 블록 디자인 교차 행렬 검증 | **P** | 유한하고 상수 크기 |
| 낙서사구도(사자각득) | 모든 궁 합이 42인지 검증 | **P** | 9궁 × 4수 |
| 낙서사구도 | `1..20`을 9개 겹치는 4집합에 합 42로 배치 가능한지 결정 | **NP-complete** | `04-unification`의 MILP 솔버가 작은 경우 처리 |
| 낙서오구도(오자각득) | 모든 궁 합 85, 9궁 총합 765 검증 | **P** | 직접 합산 |
| 낙서오구도 | `1..33`을 9개 십자 궁에 합 85로 배치 가능한지 결정 | **NP-complete** | 사구도와 동일한 겹침 그래프 구조 |
| 낙서칠구도(칠자각득) | 모든 궁 합 224 검증 | **P** | 9궁 × 7수 |
| 낙서칠구도 | `1..63`을 9개 7원소 블록으로 합 224로 분할(낙서 중심 고정) 가능한지 결정 | **NP-complete** | 고정 원소를 가진 등분할 |
| 칠자각득 | 5개 클러스터 각 7수 합 120 검증 | **P** | O(35) 덧셈 |
| 칠자각득 | `Π(5, 6, 120)` 배치 존재 여부 | **NP-complete** | mod-5 중심 제약을 가진 다중 분할 |
| 구자각득 | 5개 3×3 격자 합 207, 모서리 합 92 검증 | **P** | 직접 검사 |
| 팔자각득 | 5개 8-cycle 합 164 검증 | **P** | 직접 검사 |
| 오자각득(천수용오도) | 좌우 합 및 영역 합 검증 | **P** | 직접 검사 |
| 육자각득(지수용육도) | 5개 육각형 합 63 검증 | **P** | 직접 검사 |
| 마방진 | 채워진 정사각형이 정규 마방진인지 검증 | **P** | O(n²) 행/열/대각선 검사 |
| 마방진 | 정규 마방진 생성 | **P** | n ≠ 2에서 Siamese, Strachey 등 결정적 방법 |
| 마방진 | 부분 채워진 마방진 완성 | **NP-complete** | 라틴 방진 완성 문제로 일반화 |
| `Π(p, q, T)` / 각득 MILP | 임의 `(p, q, T)`에 배치 존재 여부 | **NP-complete** | exact cover와 유계 다중 분할을 포착 |
| `Π(p, q, T)` / 각득 MILP | 후보 배치가 제약을 만족하는지 검증 | **P** | 선형 시간 제약 평가 |

### 왜 이 대비가 중요한가

모든 퍼즐에 대해 두 종류의 질문이 있습니다.

1. **검증**: “이 구체적 도상이 주어진 규칙을 만족하는가?” — 항상 쉽습니다(P).
2. **존재/완성**: “이 조건을 만족하는 도상이 존재하는가?” — 크기가 고정되지 않으면 보통 어렵습니다(NP-complete 또는 NP-hard).

이 저장소는 역사적 인스턴스(직접 검증)와 일반화된 탐색 문제(MILP, 휴리스틱, 구조적 알고리즘)를 분리해 다룹니다. 역사적 도상은 특정 NP 증거의 witness 역할을 하지만, 임의 매개변수에 대한 새 witness 탐색은 여전히 계산적으로 어렵습니다.

---

## 클러스터별 회전 분석

원형 또는 다각형으로 배치된 클러스터를 가진 모든 도상, 그리고 30정점 9육각형 지수귀문도에도 `analyze_rotations.py` 스크립트가 포함되어 있습니다. 이 스크립트는 각 클러스터를 회전하는 객체로 보고, 시계 방향 순서, 마주 보는 위치의 합, 잉여 패턴, 클러스터 수준의 회전 불변량, 그리고 클러스터 간 전역 회전 대응 관계를 출력합니다.

한 퍼즐에 대해 실행하려면:

```bash
cd english/02-gakdeuk-series/chiljagakdeuk-seven-each-gets
python3 analyze_rotations.py
```

모든 회전 분석을 한 번에 실행하려면:

```bash
find . -name analyze_rotations.py -print0 | \
  while IFS= read -r -d '' script; do
    (cd "$(dirname "$script")" && python3 analyze_rotations.py)
  done
```

출력물은 각 퍼즐 디렉토리에 저장됩니다.

- `rotation_report.txt` — 회전 순서, 잉여 패턴, 불변량, 전체 대칭성
- `rotation_cluster_*.png` — 클러스터별 원형 시각화
- `rotation_overview.png` — 전체 클러스터 요약 그림

낙서칠구도는 현재 데이터와 교정된 분할 두 경우 모두에 대한 추가 회전 보고서/그림을 생성합니다.

---

## 코드 실행 방법

각 퍼즐 디렉토리에는 독립 실행형 Python 스크립트가 있습니다. 전형적인 사용법:

```bash
cd english/01-saodo-family/nakseo-sagudo
python3 analyze_saodo_graph.py          # 기본 분석 및 그림
python3 analyze_saodo_graph_advanced.py # 확장 그래프 불변량
```

마방진 분석:

```bash
cd english/03-magic-squares
python3 analyze_squares.py
python3 generate_and_visualize.py
```

각득 원리 MILP 솔버:

```bash
cd english/04-unification/gakdeuk-principle-shared-properties
python3 gakdeuk_solver.py --all --time-limit 120
```

대부분의 스크립트는 `matplotlib`, `numpy`, `networkx`만 필요하고, MILP 솔버는 추가로 `pulp`가 필요합니다.

---

## 흥미로운 탐구 포인트

전체 탐구 중 가장 흥미롭고 쉽게 풀리지 않는 점들을 한국어와 영문 모두로 정리했습니다.

- `korean/04-unification/misc-interesting-points.md`
- `english/04-unification/misc-interesting-points.md`

다루는 주제: 作/용 간극, mod 2의 완벽한 균형, 9궁→12궁 재해석, 지수귀문도의 거친 적합도 경관, 18세기 합법적 배치 방법에 대한 미해결 질문 등.

---

## 미해결 문제

1. **`Π(p, q, T)`의 존재 조건**: 어떤 삼항에 대해 퍼즐이 존재하는가?
2. **사오도의 균일화**: 20개 표식을 색칠과 기하 제약을 유지하면서 7개씩 5개 클러스터로 재배치할 수 있는가?
3. **낙서사구도의 그래프 구조**: 교정된 20노드 그래프가 모든 중심성 측도에서 완벽한 4중 대칭을 보이는 이유는 무엇인가?
4. **구자각득·팔자각득·칠자각득의 관계**: 이들을 `Π(p, q, T)`를 확장하는 하나의 매개변수족 안에 넣을 수 있는가?
5. **칠자각득의 중복 구조**: 특정 값이 두 번씩 나타나는 구조의 기하적 원인은 무엇인가?
