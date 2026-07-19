from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np

OUTPUT_FILE = Path("ojungto_pattern.png")


def get_korean_font():
    """Return a CJK font that can render the Korean/Hanja title."""
    font_candidates = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc",
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf",
        "/usr/share/fonts/truetype/unfonts-core/UnDotum.ttf",
    ]
    for font_path in font_candidates:
        if Path(font_path).exists():
            return fm.FontProperties(fname=font_path)
    return None


KOREAN_FONT = get_korean_font()

# 1. 7x7 격자 위 배열 정의 (행, 열 좌표는 0~6 index)
# 빈칸은 None으로 처리하고, 누락된 수(11, 15, 29)를 대칭 위치에 채워 넣었습니다.
grid_data = [
    # 1행 (index 0)
    [5, 11, 30, 25, 4, 32, 9],
    # 2행 (index 1)
    [36, None, 17, None, 33, None, 28],
    # 3행 (index 2)
    [1, 40, 24, 18, 12, None, 13],
    # 4행 (index 3)
    [27, None, 23, None, 19, None, 16],
    # 5행 (index 4)
    [8, 26, 15, 22, 31, 10, 35],
    # 6행 (index 5)
    [37, None, 38, None, 20, None, 2],  # 기존 '28' 오기를 '38'로 정정 적용
    # 7행 (index 6)
    [7, 34, 3, 14, 21, 39, 6]
]

# 누락된 수 중 29가 들어갈 유력한 빈칸 좌표를 격자 형태에 맞춰 대입 (필요시 위치 조정 가능)
grid_data[2][5] = 29 

def get_color_properties(val):
    """값에 따른 테두리 색상 및 배경색 분류 (n mod 5 기준)"""
    rem = val % 5
    if rem == 1:   # Black
        return '#333333', '#F9F9F9'
    elif rem == 2: # Red
        return '#E05A6D', '#FFF5F5'
    elif rem == 3: # Blue
        return '#4D88E5', '#F0F5FF'
    elif rem == 0: # Yellow
        return '#E5C14D', '#FFFFF0'
    else:          # Grey (rem == 4)
        return '#888888', '#FAFAFA'

def draw_ojungto():
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.axis('off')
    
    # 7x7 격자선 그리기 (정전도 느낌 강조)
    for i in range(8):
        ax.plot([0, 7], [i, i], color='#CCCCCC', lw=1, zorder=1)
        ax.plot([i, i], [0, 7], color='#CCCCCC', lw=1, zorder=1)
        
    for r in range(7):
        for c in range(7):
            val = grid_data[r][c]
            if val is not None:
                # matplotlib y축은 아래에서 위로 올라가므로 역순 매핑
                cx = c + 0.5
                cy = 7 - (r + 0.5)
                
                edge_color, face_color = get_color_properties(val)
                
                # 숫자 원 그리기
                circle = plt.Circle((cx, cy), 0.38, facecolor=face_color, 
                                    edgecolor=edge_color, lw=2.5, zorder=3)
                ax.add_patch(circle)
                
                # 텍스트 렌더링
                ax.text(cx, cy, str(val), fontsize=13, fontweight='bold',
                        ha='center', va='center', color='#222222', zorder=4)
                
    # 타이틀 추가
    title_kwargs = {
        "fontsize": 16,
        "fontweight": "bold",
        "pad": 20,
    }
    if KOREAN_FONT is not None:
        title_kwargs["fontproperties"] = KOREAN_FONT
    plt.title("오팔정전도 (五八井田圖) 복원 도안", **title_kwargs)
    
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 7)
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight')
    plt.close(fig)

if __name__ == "__main__":
    draw_ojungto()
