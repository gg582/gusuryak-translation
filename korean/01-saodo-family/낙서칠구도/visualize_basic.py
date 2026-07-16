import matplotlib.pyplot as plt
import numpy as np

# 1. 원본 도안의 기하학적 구조를 반영한 수 배치 정의
# 'surround' 배열은 12시 방향부터 시계방향 순서로 원본 도안의 위치와 정확히 매치되도록 정렬했습니다.
groups = [
    # 첫 번째 줄
    {
        "center": 4, 
        "surround": [31, 43, 22, 60, 27, 37],  # 12시부터 시계방향 순서
        "pos": (1, 3)
    },
    {
        "center": 9, 
        "surround": [15, 43, 38, 55, 10, 54], 
        "pos": (2, 3)
    },
    {
        "center": 2, 
        "surround": [28, 29, 39, 62, 17, 47], 
        "pos": (3, 3)
    },
    
    # 두 번째 줄
    {
        "center": 3, 
        "surround": [30, 40, 26, 61, 16, 48], 
        "pos": (1, 2)
    },
    {
        "center": 5, 
        "surround": [32, 41, 23, 59, 14, 50], 
        "pos": (2, 2)
    },
    {
        "center": 7, 
        "surround": [34, 38, 24, 57, 20, 44], 
        "pos": (3, 2)
    },
    
    # 세 번째 줄
    {
        "center": 8, 
        "surround": [35, 49, 12, 56, 11, 53], 
        "pos": (1, 1)
    },
    {
        "center": 1, 
        "surround": [52, 25, 19, 63, 18, 46], 
        "pos": (2, 1)
    },
    {
        "center": 6, 
        "surround": [33, 42, 21, 36, 13, 23],  # 비어있던 자리에 누락 수 '36' 대입
        "pos": (3, 1)
    }
]

def draw_pattern():
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_aspect('equal')
    ax.axis('off')
    
    group_spacing_x = 5.0
    group_spacing_y = 5.0
    
    for g in groups:
        cx = g["pos"][0] * group_spacing_x
        cy = g["pos"][1] * group_spacing_y
        
        # 큰 그룹 배경 원
        outer_boundary = plt.Circle((cx, cy), 2.2, color='#F5F5F5', fill=True, zorder=1)
        ax.add_patch(outer_boundary)
        
        # 1. 중앙 원
        center_val = g["center"]
        c_circle = plt.Circle((cx, cy), 0.5, color='#FFFFFF', ec='#333333', lw=1.5, zorder=3)
        ax.add_patch(c_circle)
        ax.text(cx, cy, str(center_val), fontsize=12, fontweight='bold',
                ha='center', va='center', zorder=4)
        
        # 2. 주변 6개 원 (12시 방향부터 시계방향으로 60도씩 배치)
        surround_vals = g["surround"]
        radius = 1.3
        
        for i, val in enumerate(surround_vals):
            # 12시(90도)를 시작점으로 하여 시계방향(- 방향)으로 60도씩 회전
            angle = np.deg2rad(90 - (60 * i))
            px = cx + radius * np.cos(angle)
            py = cy + radius * np.sin(angle)
            
            p_circle = plt.Circle((px, py), 0.45, color='#FFFFFF', ec='#444444', lw=1.2, zorder=3)
            ax.add_patch(p_circle)
            ax.text(px, py, str(val), fontsize=11, ha='center', va='center', zorder=4)
            
    ax.set_xlim(2, 18)
    ax.set_ylim(2, 18)
    
    plt.tight_layout()
    plt.savefig('pattern_corrected.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    draw_pattern()
