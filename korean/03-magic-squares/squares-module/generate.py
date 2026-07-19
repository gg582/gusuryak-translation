#!/usr/bin/env python3
"""
백자도(10x10 마방진) 정정본 생성, 도출 관계 검증 및 시각화 프로그램
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# 10x10 정정본 방진 데이터 정의
# M03: 백자자수음양착종도 교정본 (아들 방진)
M03 = [
    [92, 99,  1,  8, 15, 67, 74, 51, 58, 40],
    [98, 80,  7, 14, 16, 73, 55, 57, 64, 41],
    [ 4, 81, 88, 20, 22, 54, 56, 63, 70, 47],
    [85, 87, 19, 21,  3, 60, 62, 69, 71, 28],
    [86, 93, 25,  2,  9, 61, 68, 75, 52, 34],
    [17, 24, 76, 83, 90, 42, 49, 26, 33, 65],
    [23,  5, 82, 89, 91, 48, 30, 32, 39, 66],
    [79,  6, 13, 95, 97, 29, 31, 38, 45, 72],
    [10, 12, 94, 96, 78, 35, 37, 44, 46, 53],
    [11, 18, 100, 77, 84, 36, 43, 50, 27, 59]
]

# M04: 백자생성순수도 교정본 (회전 방진)
M04 = [
    [40, 41, 47, 28, 34, 65, 66, 72, 53, 59],
    [58, 64, 70, 71, 52, 33, 39, 45, 46, 27],
    [51, 57, 63, 69, 75, 26, 32, 38, 44, 50],
    [74, 55, 56, 62, 68, 49, 30, 31, 37, 43],
    [67, 73, 54, 60, 61, 42, 48, 29, 35, 36],
    [15, 16, 22,  3,  9, 90, 91, 97, 78, 84],
    [ 8, 14, 20, 21,  2, 83, 89, 95, 96, 77],
    [ 1,  7, 88, 19, 25, 76, 82, 13, 94, 100],
    [99, 80, 81, 87, 93, 24,  5,  6, 12, 18],
    [92, 98,  4, 85, 86, 17, 23, 79, 10, 11]
]

# M05: 백자생성교수도 교정본 (좌우반사 방진)
M05 = [
    [40, 58, 51, 74, 67, 15,  8,  1, 99, 92],
    [41, 64, 57, 55, 73, 16, 14,  7, 80, 98],
    [47, 70, 63, 56, 54, 22, 20, 88, 81,  4],
    [28, 71, 69, 62, 60,  3, 21, 19, 87, 85],
    [34, 52, 75, 68, 61,  9,  2, 25, 93, 86],
    [65, 33, 26, 49, 42, 90, 83, 76, 24, 17],
    [66, 39, 32, 30, 48, 91, 89, 82,  5, 23],
    [72, 45, 38, 31, 29, 97, 95, 13,  6, 79],
    [53, 46, 44, 37, 35, 78, 96, 94, 12, 10],
    [59, 27, 50, 43, 36, 84, 77, 100, 18, 11]
]

# M06: 백자음양자모착종도 교정본 (모도 - 엄마 방진)
M06 = [
    [11, 18, 100, 77, 84, 36, 43, 50, 27, 59],
    [10, 12, 94, 96, 78, 35, 37, 44, 46, 53],
    [79,  6, 13, 95, 97, 29, 31, 38, 45, 72],
    [23,  5, 82, 89, 91, 48, 30, 32, 39, 66],
    [17, 24, 76, 83, 90, 42, 49, 26, 33, 65],
    [86, 93, 25,  2,  9, 61, 68, 75, 52, 34],
    [85, 87, 19, 21,  3, 60, 62, 69, 71, 28],
    [ 4, 81, 88, 20, 22, 54, 56, 63, 70, 47],
    [98, 80,  7, 14, 16, 73, 55, 57, 64, 41],
    [92, 99,  1,  8, 15, 67, 74, 51, 58, 40]
]

def verify_relations():
    """방진들 사이의 공간 변환(대칭/회전) 유도 관계 검증"""
    m03 = np.array(M03)
    m04 = np.array(M04)
    m05 = np.array(M05)
    m06 = np.array(M06)
    
    print("=== 방진 간 유도 관계 수학적 검증 ===")
    
    # 1. 백자생성순수도(M04)는 아들 방진(M03)의 반시계 방향 90도 회전
    rot90_m03 = np.rot90(m03, 1)
    is_m04_ok = np.all(m04 == rot90_m03)
    print(f"M04 == rot90(M03, 1): {is_m04_ok}")
    
    # 2. 백자생성교수도(M05)는 아들 방진(M03)의 좌우 반전
    fliplr_m03 = np.fliplr(m03)
    is_m05_ok = np.all(m05 == fliplr_m03)
    print(f"M05 == fliplr(M03): {is_m05_ok}")
    
    # 3. 백자음양자모착종도(M06, 엄마 방진)는 아들 방진(M03)의 상하 반전
    flipud_m03 = np.flipud(m03)
    is_m06_ok = np.all(m06 == flipud_m03)
    print(f"M06 == flipud(M03): {is_m06_ok}")
    
    # 4. 각 방진의 마방진 성질(가로, 세로, 대각선 합 505) 검증
    for name, matrix in [("M03 (아들 방진)", m03), 
                         ("M04 (순수도)", m04), 
                         ("M05 (교수도)", m05), 
                         ("M06 (엄마 방진)", m06)]:
        row_sums = matrix.sum(axis=1)
        col_sums = matrix.sum(axis=0)
        diag_sum1 = np.trace(matrix)
        diag_sum2 = np.trace(np.fliplr(matrix))
        
        is_magic = (all(row_sums == 505) and 
                    all(col_sums == 505) and 
                    diag_sum1 == 505 and 
                    diag_sum2 == 505)
        print(f"  {name} 마방진 충족 여부 (합 505): {is_magic} "
              f"(대각합: {diag_sum1}, {diag_sum2})")

def visualize_squares(output_dir):
    """방진들을 시각화하여 히트맵으로 저장"""
    os.makedirs(output_dir, exist_ok=True)
    m03 = np.array(M03)
    m04 = np.array(M04)
    m05 = np.array(M05)
    m06 = np.array(M06)
    
    squares = [
        (m03, "M03: Son Square (Baekjajasuyin-yang-chakjong)", "m03_son.png"),
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
    
    # 이 스크립트 파일 기준 상위의 figures 디렉토리
    current_dir = os.path.dirname(os.path.abspath(__file__))
    figures_dir = os.path.join(current_dir, "figures")
    visualize_squares(figures_dir)
