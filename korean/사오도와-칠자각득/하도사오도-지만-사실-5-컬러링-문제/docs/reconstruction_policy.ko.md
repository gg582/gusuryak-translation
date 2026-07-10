# 보존적 재현 정책: 하도 5-컬러링 퍼즐

---

## 1. 목적

본 문서는 `사오도와-칠자각득의-일반화`에서 정의한 사오도(하도)의 5개 mod-5 잉여 그룹 구조와, 아래 Problem Constraints의 재현 정책을 엄격히 따르는 Python 스크립트 및 시각화를 설명합니다.

원문에 명시된 데이터만 보존하고, 추론된 구조는 별도로 표시하지 않습니다.

---

## 2. 원문 데이터

### 2.1 기하 배치

20개의 원형 슬롯은 다음과 같은 대칭 십자가형에 고정되어 있습니다.

```
        19  2
        7  14
13  8   5   16  4   17
18  3   11  10  12   9
        15  1
        6  20
```

- 상단 팔: 2×2
- 중앙 몸통: 2×6
- 하단 팔: 2×2

슬롯 좌표는 변경하지 않습니다.

### 2.2 숫자 라벨

각 슬롯에는 정확히 하나의 아라비아 숫자가 들어 있으며, 집합은 `{1, 2, …, 20}`이고 각 숫자가 정확히 한 번씩 나타납니다.

### 2.3 숫자 기울기

원문의 숫자는 모두 의도적으로 기울어져 있습니다. 현재 스크립트에서는 관측된 기울기를 `-30°`로 통일하여 보존하며, 이 값은 데이터 필드로 취급됩니다.

### 2.4 잉여 그룹 분할

`group(n) = ((n - 1) mod 5) + 1`에 따라 5개 그룹으로 나뉩니다.

| 그룹 | 이름 | 원소 |
|---|---|---|
| 1 | 물(Water) | {1, 6, 11, 16} |
| 2 | 불(Fire) | {2, 7, 12, 17} |
| 3 | 나무(Wood) | {3, 8, 13, 18} |
| 4 | 금속(Metal) | {4, 9, 14, 19} |
| 5 | 흙(Earth) | {5, 10, 15, 20} |

### 2.5 체크섬

원문의 "共積210"은 다음과 같이 해석됩니다.

```
sum(1..20) = 210
```

---

## 3. 재현 정책

### 3.1 보존 대상

- **slot positions**: 20개 슬롯의 좌표
- **circular marks**: 원형 표식
- **numeral values**: 숫자 라벨
- **numeral orientations**: 숫자 기울기
- **symmetric cross-shaped layout**: 대칭 십자가형 배치
- **residue-group partition**: mod 5 잉여 그룹 분할
- **checksum note**: 共積210

### 3.2 도입하지 않는 것

아래 항목은 원문에 명시되지 않았으므로 본 재현에 포함하지 않습니다.

- 인공적 그래프 변(artificial graph edges)
- 최근접 이웃 가정(nearest-neighbor assumptions)
- 재작성 시스템(rewrite systems)
- 유한 상태 기계(finite-state machines)
- 순회 규칙(traversal rules)
- 대수적 의미 부여(algebraic semantics)

---

## 4. 시각화

`figures/reconstruct_source.py`를 실행하면 `figures/puzzle_reconstruction.png`가 생성됩니다.

```bash
python3 figures/reconstruct_source.py
```

생성된 이미지는 다음을 포함합니다.

- 20개의 원형 슬롯
- 기울어진 숫자 라벨
- 잉여 그룹별 테두리 색상
- 共積210 체크섬
- 대칭 십자가형 윤곽(점선, 시각적 보조선)
- 보존/미도입 항목 안내

---

## 5. 스크립트 구조

- `SLOTS`: 20개 슬롯의 좌표, 라벨, 기울기를 담은 리스트
- `RESIDUE_GROUPS`: 5개 잉여 그룹의 명시적 정의
- `group_of(label)`: `((label - 1) mod 5) + 1`
- `checksum(labels)`: 라벨 합계
- `draw_reconstruction(...)`: matplotlib 기반 시각화

스크립트 마지막에서는 다음 데이터 일관성 검사를 수행합니다.

- 슬롯 수 = 20
- 라벨이 `{1, …, 20}`을 정확히 한 번씩 사용
- 총합 = 210
- 각 그룹이 정확히 4개 원소를 가짐

---

## 6. 생성된 파일

| 파일 | 설명 |
|---|---|
| `figures/reconstruct_source.py` | 보존적 재현 스크립트 |
| `figures/puzzle_reconstruction.png` | 생성된 시각화 이미지 |
| `docs/reconstruction_policy.ko.md` | 본 문서(한국어) |
| `docs/reconstruction_policy.en.md` | 영어 버전 |
