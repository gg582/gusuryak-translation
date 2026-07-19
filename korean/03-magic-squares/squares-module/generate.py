#!/usr/bin/env python3
"""
백자도(10x10 마방진) 정정본 생성, 도출 관계 검증 및 시각화 프로그램
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# 10x10 정정본 방진 데이터 정의 (원본의 점대칭성 및 조합론적 규칙 복구 모델)

# M04_orig
M04_orig = np.array([
    [90, 89, 78, 67, 56, 45, 34, 23, 12,  1],
    [86, 70, 39, 58, 97,  4, 43, 32, 21, 15],
    [77, 66, 50, 99, 88, 13,  2, 41, 35, 24],
    [68, 57, 96, 80, 79, 22, 11,  5, 44, 33],
    [59, 98, 87, 76, 60, 31, 25, 14,  3, 42],
    [42,  3, 14, 25, 31, 60, 76, 87, 98, 59],
    [33, 44,  5, 11, 22, 79, 80, 96, 57, 68],
    [24, 35, 41,  2, 13, 88, 99, 50, 66, 77],
    [15, 21, 32, 43,  4, 97, 58, 69, 70, 86],
    [ 1, 12, 23, 34, 45, 56, 67, 78, 89, 90]
])

M04_corr = M04_orig.copy()
M04_corr[1, 2] = 69 # 39 -> 69 (점대칭 오류 교정)

# M05_orig
M05_orig = np.array([
    [10, 19, 28, 37, 46, 55, 64, 73, 82, 91],
    [16, 20, 39, 48,  7, 94, 53, 62, 71, 85],
    [27, 36, 40,  9, 18, 83, 92, 51, 65, 74],
    [38, 47,  6, 10, 29, 72, 81, 95, 54, 63],
    [59,  8, 17, 26, 30, 61, 75, 84, 93, 52],
    [42, 93, 84, 75, 61, 30, 26, 17,  8, 49],
    [63, 54, 95, 81, 72, 29, 10,  6, 47, 38],
    [74, 65, 51, 92, 83, 18,  9, 40, 36, 27],
    [85, 71, 62, 53, 94,  7, 48, 39, 20, 16],
    [91, 82, 73, 64, 55, 46, 37, 28, 19, 10]
])

M05_corr = M05_orig.copy()
M05_corr[5, 0] = 52 # 42 -> 52 (점대칭 오류 교정)
M05_corr[5, 9] = 59 # 49 -> 59 (점대칭 오류 교정)
# 주석 교정 반영 (16 -> 11, 85 -> 86)
M05_corr[1, 0] = 11
M05_corr[8, 9] = 11
M05_corr[8, 0] = 86
M05_corr[1, 9] = 86

# M06_orig
M06_orig = np.array([
    [100, 89, 78, 67, 56, 45, 34, 23, 12,  1],
    [ 29, 28, 47, 36, 10, 91, 65, 54, 73, 72],
    [ 48, 17, 26, 40, 39, 62, 61, 75, 84, 53],
    [ 27, 46, 50,  9, 88, 13, 92, 51, 55, 74],
    [ 76, 80, 59, 98, 87, 14,  3, 32, 21, 25],
    [ 15, 31, 42, 43,  4, 97, 58, 69, 70, 86],
    [ 24, 35, 41,  2, 83, 18, 99, 60, 66, 77],
    [ 93, 94, 85, 71, 52, 49, 30, 16,  7,  8],
    [ 82, 63, 64, 95, 81, 20,  6, 37, 38, 19],
    [ 11, 22, 33, 44,  5, 96, 57, 68, 79, 90]
])

M06_corr = M06_orig.copy()
# 2행 Col 3(47)과 Col 8(54) 교환
M06_corr[1, 2] = 54
M06_corr[1, 7] = 47
# 3-cycle: (5,3) 59 -> 42, (6,3) 42 -> 32, (5,8) 32 -> 59
M06_corr[4, 2] = 42
M06_corr[4, 7] = 59
M06_corr[5, 2] = 32

def verify_relations():
    """방진들의 수학적 성질 및 점대칭성 검증"""
    print("=== 방진 수학적 검증 ===")
    
    # 1. 백자생성순수도(M04) 검증
    m04 = np.array(M04_corr)
    # 점대칭 검증
    is_m04_symmetric = True
    for i in range(10):
        for j in range(10):
            if m04[i, j] != m04[9-i, 9-j]:
                is_m04_symmetric = False
    print(f"M04 180도 회전 점대칭 충족 여부: {is_m04_symmetric}")
    print(f"M04 행 합: {m04.sum(axis=1)}")
    print(f"M04 열 합: {m04.sum(axis=0)}")

    # 2. 백자생성교수도(M05) 검증
    m05 = np.array(M05_corr)
    is_m05_symmetric = True
    for i in range(10):
        for j in range(10):
            if m05[i, j] != m05[9-i, 9-j]:
                is_m05_symmetric = False
    print(f"M05 180도 회전 점대칭 충족 여부: {is_m05_symmetric}")
    print(f"M05 행 합: {m05.sum(axis=1)}")
    print(f"M05 열 합: {m05.sum(axis=0)}")

    # 3. 백자음양자모착종도(M06) 검증
    m06 = np.array(M06_corr)
    is_m06_semi = np.all(m06.sum(axis=1) == 505) and np.all(m06.sum(axis=0) == 505)
    print(f"M06 가로/세로 합 505(준마방진) 충족 여부: {is_m06_semi}")
    print(f"M06 행 합: {m06.sum(axis=1)}")
    print(f"M06 열 합: {m06.sum(axis=0)}")

def visualize_squares(output_dir):
    """방진들을 시각화하여 히트맵으로 저장"""
    os.makedirs(output_dir, exist_ok=True)
    m04 = np.array(M04_corr)
    m05 = np.array(M05_corr)
    m06 = np.array(M06_corr)
    
    squares = [
        (m04, "M04: Pure Square (Baekjasaengseong-sunsu)", "m04_pure.png"),
        (m05, "M05: Cross Square (Baekjasaengseong-gyosu)", "m05_cross.png"),
        (m06, "M06: Mother Square (Baekjayin-yang-jamo-chakjong)", "m06_mother.png")
    ]
    
    for matrix, title, filename in squares:
        fig, ax = plt.subplots(figsize=(8, 8))
        im = ax.imshow(matrix, cmap="YlGnBu", vmin=1, vmax=100)
        
        # 각 셀에 텍스트 표시
        for i in range(10):
            for j in range(10):
                val = matrix[i, j]
                color = "white" if val > 60 else "black"
                ax.text(j, i, str(val), ha="center", va="center", 
                        color=color, fontsize=10, fontweight="bold")
        
        ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
        ax.set_xticks(range(10))
        ax.set_yticks(range(10))
        ax.set_xticklabels(range(1, 11))
        ax.set_yticklabels(range(1, 11))
        
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        plt.tight_layout()
        
        path = os.path.join(output_dir, filename)
        plt.savefig(path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        print(f"시각 자료 저장 완료: {path}")

if __name__ == "__main__":
    verify_relations()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    figures_dir = os.path.join(current_dir, "figures")
    visualize_squares(figures_dir)
