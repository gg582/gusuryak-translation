# 각득(各得) 원리를 따르는 퍼즐들의 공유 특성 및 일반화

《구수력(九數略)》 계열 각득 퍼즐(구·오·육·칠·팔자각득)의 공유 구조와 일반화 모델을 분석하고, `n`이 주어졌을 때 자동으로 각득 계열 수 배치를 찾아주는 MILP Solver를 포함합니다.

## 파일 구성

| 파일 | 설명 |
|---|---|
| `analysis_report.md` | 각득 계열의 공유 특성·차이점·일반화 모델 심층 분석 |
| `blog.md` | 각득 원리를 쉽게 풀어쓴 대중적 설명 |
| `generalize_gakdeuk.py` | 각 계열 데이터 정의 및 오행 합·중복 계수 방정식 검증 |
| `gakdeuk_solver.py` | **N자각득 MILP Solver** (Python + PuLP) |
| `computed_report.md` | `generalize_gakdeuk.py` 실행 결과 |

## 설치

SageMath가 없는 환경에서는 Python 가상환경에 PuLP를 설치해 사용합니다.

```bash
cd "/home/yjlee/gusuryak-translation/korean/04-unification/각득 원리를 따르는 퍼즐들의 공유 특성 및 일반화"
python3 -m venv venv
source venv/bin/activate
pip install pulp
```

## Solver 사용법

### 알려진 5개 계열을 한 번에 풀기

```bash
source venv/bin/activate
python gakdeuk_solver.py --all --time-limit 120
```

출력 예시:

```
[풀이 시도] 오자각득(천수용오도) (n=5, N_max=24, S=65)
N=5, N_max=24, S=65
고유 정점 합 T=265, 중복 포함 합 5S=325, D=60
누락된 수: [3, 10, 22]
공유 정점: [6, 7, 23, 24]
  C1(중): 2 + 7 + 12 + 20 + 24 = 65
  ...
```

### 임의의 n, N_max, S로 풀기

```bash
# 부분 집합 간 정점 공유 없음 (D=0)
python gakdeuk_solver.py --n 8 --max 40 --sum 164

# 누락된 수가 있을 때
python gakdeuk_solver.py --n 5 --max 24 --sum 65 --missing 3 10 22 --num-shared 4

# 최대 중복 계수 3, 공유 정점 8개 (육자각득 유사)
python gakdeuk_solver.py --n 6 --max 20 --sum 63 --max-multiplicity 3 --num-shared 8

# 누락 수를 MILP가 자동 선택 (칠자각득 유사)
python gakdeuk_solver.py --n 7 --max 35 --sum 120 \
    --auto-missing --missing-count 4 --missing-sum 95 --required 1 2 3 4 5

# 육자각득 유사: 벌집 인접 + 쌍별 공유 정점 수 + 상하 대칭 + 시각화
python gakdeuk_solver.py --n 6 --max 20 --sum 63 \
    --adjacency honeycomb --pair-shared-counts "0-1:2,0-2:2,0-3:2,0-4:2" \
    --symmetry ud --residue-balance --visualize

# 5개 계열을 한 번에 탐색·JSON 저장·시각화
python gakdeuk_solver.py --all --time-limit 180 \
    --max-solutions 1 --visualize --output solutions.json
```

### S를 자동 탐색

```bash
python gakdeuk_solver.py --n 8 --max 40 --search --time-limit 120
```

## Solver 설계

`gakdeuk_solver.py`는 Mixed Integer Linear Programming(MILP)을 사용합니다.

- 변수: `x[v][c] ∈ {0,1}` — 수 `v`가 클러스터 `c`에 속하는지
- 기본 제약:
  - 각 클러스터는 정확히 `n`개 정점
  - 각 클러스터의 합은 `S`
  - 각 수는 1개 이상, `max_multiplicity`개 이하의 클러스터에 속함
  - 중복 총량 `D = 5S − T` 제약
  - 누락 수 자동 선택 (선택)
- 기하 제약:
  - 인접 그래프: `cross`/`honeycomb`/`grid` 또는 사용자 정의 인접 쌍
  - 인접 쌍별 공유 정점 수 (`--pair-shared-counts`)
  - 상하/좌우 residue 대칭성 (`--symmetry`)
- 오행 제약:
  - `mod 5` remainder 분포 균형 (`--residue-balance`)
- 출력:
  - 여러 해 enumeration (`--max-solutions`)
  - JSON 저장 (`--output`)
  - matplotlib 시각화 (`--visualize`)

## 주의사항

- solver는 **수 조합적 해** 위에 **기하 제약**(인접 그래프, 쌍별 공유 정점 수, 대칭성)과 **오행 제약**(`mod 5` residue 균형)을 겹쳐 찾습니다.
- 기하 제약을 충분히 주면 실제 전통 도상과 매우 비슷한 배치가 나오지만, 완벽한 재현을 위해서는 좌표·각도·그림 형태 등의 추가 정보가 필요합니다.
- `--all` 실행 시 각 계열의 전통 조건(누락 수, 공유 구조, 합 불변량)을 내장 프리셋으로 사용합니다.

## 핵심 일반화 공식

- 합 불변량: `S = n × μ`
- 중복 계수 방정식: `5S = T + D`
- 오행 mod 5 합: `WX(r) = 5·m(m−1)/2 + m·r`

자세한 내용은 `analysis_report.md`와 `blog.md`를 참조하세요.
