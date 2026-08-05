# 洛書六觚圖(낙서육고도) 결정론적 해 생성기, SMT 완전성 증명 및 알고리즘 명세 (GENERATOR.md)

## 1. 개요 (Overview)

본 문서는 조선 시대 최석정(崔錫鼎)의 《구수략(九數略)》에 수록된 **낙서육고도(洛書六觚圖)**에 대하여, 난수 시드(Stochastic Seed / Randomness)에 의존하지 않고 **항상 참인 최적해(이론적 벌점 하한 6.0)**를 생성하는 **결정론적 알고리즘(Deterministic Generator)**의 명세와, Z3 SMT Solver 및 군론(Group Theory) 기법을 통한 **SMT 탐색의 완전성(Completeness), 궤도 분리(Orbit Separation)** 및 **결정론적 파이프라인의 전역 커버리지** 수리 검증 실험 결과를 정밀히 기록한다.

---

## 2. 수학적 제약 조건 및 이론적 하한 (Mathematical Formulation)

육고도는 반지름 $R=9$인 육각 격자 271칸 중 중심(虛一) 1칸을 제외한 **270칸**에 $1 \dots 270$의 자연수를 중복 없이 배치하는 구조이다.

### 핵심 제약 구조 (Target Specifications)
1. **대척 보수쌍 조건 (Antipodal Complementary Pair)**:
   $$\forall c \in \text{Filled}, \quad v(c) + v(-c) = 271$$
   - 270칸은 135개의 점대칭 슬롯 쌍 $(c_i, -c_i)$으로 완전히 분할되며, 각 슬롯에는 보수쌍 $(t, 271-t)$ ($1 \le t \le 135$)이 배정된다.
2. **변 합 (Side Sum)**: 6개 변 각각의 10칸 합 $= 1355$ ($5 \times 271$)
3. **섹터 합 (Wedge Sum)**: 6개 60° 쐐기 섹터(45칸) 각각의 합 $\approx 6097.5$ (최적 $6097 / 6098$ 교대)
4. **광선 합 (Ray Sum)**: 6개 중심-꼭짓점 광선(9칸) 각각의 합 $\approx 1219.5$ (최적 $1219 / 1220$ 교대)
5. **축(中觚) 합**: 3개 중심 통과 축(19칸) 각각의 합 $= 2439$ ($9 \times 271$, 보수쌍 구조 하에 자동 성립)
6. **벌점 함수 (Penalty Floor)**:
   $$P = \sum_{j=0}^5 |S_j - 1355| + \sum_{i=0}^5 |W_i - 6097.5| + \sum_{r=0}^5 |R_r - 1219.5| \ge 6.0$$
   *(홀수 칸 구조로 인한 오차 한계 $6.0$이 이론적 하한임)*

---

## 3. 결정론적 알고리즘 가설 및 실험 결과 (Experimental Findings)

`yukgodo/experiment/deterministic_experiments.py`를 통해 4가지 가설을 검증하였다.

| 가설 유형 | 결정론적 배치 알고리즘 | 최선 벌점 (Goal: 6.0) | 평가 및 판단 |
| :--- | :--- | :---: | :--- |
| **가설 A** | **결정론적 나선 매핑** (*Deterministic Spiral Mapping*) | `6,534.0` | 단순 닫힌 수식 해 없음 (반증) |
| **가설 B** | **결정론적 잉여류 매핑** ($v \equiv aq+br \pmod{271}$) | `24,228.0` | 단순 닫힌 수식 해 없음 (반증) |
| **가설 C** | **결정론적 섹터 대칭 균등 매핑** (*Wedge Pairing Equalizer*) | `516.0` | 단순 수식으로 대역 하한 도출 불가 |
| **가설 D** | **결정론적 가지치기 백트래킹** (*Deterministic DFS Solver*) | **`6.0` (완벽 수렴)** | **100% 결정론적 절차로 참인 해 생성 성공** |

---

## 4. 구체적인 결정론적 해 생성 알고리즘 명세 (Algorithm Specification)

### 알고리즘 1: 결정론적 제약-가지치기 백트래킹 솔버 (Deterministic Pruning Backtracking DFS)

이 알고리즘은 무작위 난수를 0% 사용하며, 사전 정렬된 슬롯 순서와 획정된 제약 전파(Constraint Propagation)만으로 페널티 $6.0$의 완벽한 해를 구성한다.

```python
# pseudo-code of Deterministic DFS Generator (Pair Selection + Orientation Backtracking)
1. Define 135 antipodal slots S_0 ... S_134 sorted deterministically by structural impact:
   - Primary Key: Perimeter side memberships
   - Secondary Key: Ray membership
   - Tertiary Key: Axial index q, then r
2. Define unassigned pairs set UnassignedPairs = {(1, 270), (2, 269), ..., (135, 136)}
3. Function DFS(slot_idx, current_partial_penalty):
   a. If slot_idx == 135:
        If current_partial_penalty <= 6.0: Return Success(assigned_values)
   b. Slot = SortedSlots[slot_idx]
   c. For pair in UnassignedPairs (in deterministic numerical order):
        For (cell_A_val, cell_B_val) in [(pair.t, 271 - pair.t), (271 - pair.t, pair.t)]:
            Set Slot.cell_A = cell_A_val, Slot.cell_B = cell_B_val
            Mark pair as assigned
            Update partial sums (side_sums, wedge_sums, ray_sums)
            Calculate lower-bound partial penalty P_bound
            If P_bound < Best_Penalty:
                If DFS(slot_idx + 1, P_bound) is Success: Return Success
            Revert partial sums & unmark pair
   d. Return Failure
```

> [!NOTE]
> 사전 지정된 특정 슬롯-보수쌍 고정 매핑($S_i \mapsto (i+1, 271-i-1)$) 아래에서는 방향 $2^{135}$만 탐색하여 빠른 최적해 도달이 가능하지만, 일반적인 해공간 탐색을 위해서는 위와 같이 각 단계에서 보수쌍 선택과 방향 선정을 동시 수행해야 한다.

---

### 알고리즘 2: 序左·寄左 반시계 회전 대칭 연산 솔버 (CCW Rotation-Orbit Solver)

원문의 **'序左(서좌)'** 및 **'寄左(기좌)'** 지시어를 $60^\circ$ 단위 반시계 회전 대칭군 $C_6$ 변환 연산자로 구현한 알고리즘이다.

#### 반시계 회전 변환식 ($60^\circ$ CCW Rotation in Axial Coordinates)
$$(q, r) \mapsto (-r, q + r)$$

#### 궤적 이동(Orbit Shift) 연산
슬롯 $s_1 = (c_a, c_b)$에 대해 반시계 방향 $k \times 60^\circ$ 위치의 슬롯 $s_2 = R_k(s_1)$를 구하고, 두 슬롯에 배치된 보수쌍을 이웃 교환 연산자로 전환하여 local minima를 탈출한다.

```python
# pseudo-code of CCW Rotation-Orbit Move
def rotation_orbit_swap(state, slot_1, rot_k):
    target_slot, is_flipped = slot_rotation_map[slot_1][rot_k]
    state.do_swap(slot_1, target_slot, flip=is_flipped)
```

---

## 5. SMT Solver의 조건부 완전성(Completeness) 및 궤도 분리 실증 (SMT Completeness & Orbit Separation)

`yukgodo/experiment/smt_completeness_proof.py`를 통하여, 인코딩된 제약 조건 아래에서의 SMT Solver 완전성과 궤도 분리 성질을 수리 실증하였다.

### 핵심 수리 판정 및 검증 결과

1. **지정된 인코딩 및 부분공간 내에서의 SMT Solver 완전 탐색성**:
   - Z3 SMT Solver는 명시적으로 인코딩된 제약 방정식(변 1355, 섹터 6097/6098, 광선 1219/1220, 대척쌍 271)과 고정된 부분공간 조건 아래에서 단 1개의 해도 놓치지 않고 **조건부 완전 열거(Conditional Complete Enumeration)**를 수행하며, 해당 하위 제약 공간 탐색 완료 시 `UNSAT` 신호를 반환한다 (실증 완료: 지정 부분 공간 내 54개 모델 열거 후 `UNSAT` 도달).
   - 이는 전체 해공간($135! \times 2^{135}$) 전체에 대한 완전 열거 완료를 의미하는 것이 아니라, 명시된 하위 제약 인코딩 범위 내에서의 논리적 완전성을 의미한다.
2. **단일 특정 생성기의 한계와 궤도의 분리 (Orbit Separation)**:
   - 고정된 1개의 탐색 트리를 사용하는 특정 결정론적 생성기 $G_A$는 자신의 대수적 궤도 $\text{Orbit}(G_A)$ 속 해들만 산출하므로, 다른 궤도에 속한 참인 해들을 스스로 생성하지 못한다.
   - 그러나 이 다른 궤도의 해들 역시 육고도의 마법 제약식을 100% 충족하는 참인 해이므로, **Z3 SMT Solver나 제약 전파 탐색기를 통하여 탐색 및 생성이 가능**하다.

---

## 6. 결론 및 학술적 의의 (Conclusion & Implications)

1. **단순 수식 해의 부재**:
   낙서육고도는 한 줄짜리 계산 수식($v = 6t \pmod{271}$ 등)으로 즉시 풀리는 구조가 아니며, 복합적인 면적 및 6축 균형 제약이 얽혀 있다.
2. **결정론적 백트래킹 탐색기의 유효성**:
   사전 지정된 규칙과 가지치기를 통한 결정론적 백트래킹을 통해 이론적 하한(벌점 6.0)을 만족하는 최적해에 도달할 수 있다. 다만 일반적인 종료 및 완전성 보장을 위해서는 별도의 수리적 증명이 요구된다.
3. **SMT Solver 완전성에 기반한 통합 탐색 파이프라인**:
   특정 인코딩 제약 아래에서 Z3 SMT Solver는 모델 열거와 UNSAT 판정의 완전성을 제공하며, 대칭군 $C_6 \times \mathbb{Z}_2$ 작용과 결합하여 부분공간별 해 구조를 체계적으로 분석할 수 있다.
4. **《구수략》 원문과 현대 탐색기의 provenance 구분**:
   원문의 **'來積法'**은 육각 격자의 칸 수와 기하 상수를 산출하는 문헌적 사술 절차로 확인된다. 현대의 결정론적 제약 충족 생성기는 이 기하 조건(270칸, 변당 10칸, 중고 19칸 등)을 입력 제약으로 활용하지만, 탐색기 자체의 백트래킹 알고리즘이 원문 문헌에 명시되어 있었다고 볼 증거는 없다.

