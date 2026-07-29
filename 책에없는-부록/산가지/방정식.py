import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle


# Matplotlib이 이 환경의 Noto CJK 컬렉션을 JP 이름으로 등록한다.
# Noto에는 한글을, DejaVu에는 Noto에 없는 아래첨자 수학 기호를 맡긴다.
plt.rcParams["font.family"] = ["Noto Sans CJK JP", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# 1. 5-10진 산가지 단일 자릿수 렌더링 함수
def draw_single_digit(ax, center_x, val, is_vertical, scale=1.0):
    """
    center_x: 산가지 자릿수의 중심 X 좌표
    val: 0~9 사이의 단일 자릿수 값 (음수 부호는 별도 처리)
    is_vertical: 세로식/가로식 여부
    scale: 자릿수가 늘어날 때 전체 폭과 두께를 줄이는 축소 비율
    """
    # 빈칸과 구별되도록 0은 작은 빈 원으로 표시한다.
    if val == 0:
        ax.add_patch(Circle((center_x, 0), 0.13 * scale, fill=False, color="black", linewidth=2 * scale))
        return center_x, 0

    five_count = val // 5
    one_count = val % 5
    
    color = 'black'
    spacing = 0.15 * scale
    start_offset = -((one_count - 1) * spacing) / 2 if one_count > 0 else 0
    
    last_rod_pos = None

    if is_vertical:
        for i in range(one_count):
            lx = center_x + start_offset + (i * spacing)
            ax.plot([lx, lx], [-0.4 * scale, 0.4 * scale], color=color, linewidth=4 * scale)
            last_rod_pos = (lx, 0)
            
        if five_count > 0:
            ax.plot([center_x - 0.3 * scale, center_x + 0.3 * scale], [0.6 * scale, 0.6 * scale], color=color, linewidth=5 * scale)
            if last_rod_pos is None:
                last_rod_pos = (center_x, 0.6 * scale)
    else:
        for i in range(one_count):
            ly = start_offset + (i * spacing)
            ax.plot([center_x - 0.4 * scale, center_x + 0.4 * scale], [ly, ly], color=color, linewidth=4 * scale)
            last_rod_pos = (center_x, ly)
            
        if five_count > 0:
            ax.plot([center_x, center_x], [-0.6 * scale, 0.6 * scale], color=color, linewidth=5 * scale)
            if last_rod_pos is None:
                last_rod_pos = (center_x, 0)

    return last_rod_pos

# 2. 다자릿수 전체를 산가지 배열로 이어서 그리는 함수
def draw_full_number_sangi(ax, x_pos, val, is_first_vertical):
    """
    x_pos: 해당 계수의 중앙 영역 X 좌표
    val: 표현할 전체 정수 (예: 140688000)
    is_first_vertical: 최고 자릿수의 세로식/가로식 여부
    """
    if val == 0:
        draw_single_digit(ax, x_pos, 0, is_first_vertical)
        return

    sign = 1 if val >= 0 else -1
    abs_str = str(abs(val))
    num_digits = len(abs_str)
    
    # 자릿수 개수에 비례하여 산가지 축소 비율 및 간격 결정
    scale = max(0.25, 1.0 / (num_digits ** 0.5))
    digit_width = 0.8 * scale
    
    total_width = num_digits * digit_width
    start_x = x_pos - (total_width / 2) + (digit_width / 2)
    
    last_rod = None
    last_is_vert = False

    # 높은 자릿수부터 낮은 자릿수까지 세로/가로 교대 배열
    for i, char_digit in enumerate(abs_str):
        d_val = int(char_digit)
        cx = start_x + (i * digit_width)
        
        # 짝수/홀수 자릿수에 따라 세로식과 가로식 교대
        is_vert = is_first_vertical if (i % 2 == 0) else not is_first_vertical
        
        rod_pos = draw_single_digit(ax, cx, d_val, is_vert, scale)
        if rod_pos is not None:
            last_rod = rod_pos
            last_is_vert = is_vert

    # 음수일 경우 전체 숫자의 맨 마지막 산가지 막대에 사선 겹침 표시
    if sign < 0 and last_rod is not None:
        rx, ry = last_rod
        if last_is_vert:
            ax.plot([rx - 0.15 * scale, rx + 0.15 * scale], 
                    [ry - 0.25 * scale, ry + 0.25 * scale], color='black', linewidth=3 * scale)
        else:
            ax.plot([rx - 0.25 * scale, rx + 0.25 * scale], 
                    [ry - 0.15 * scale, ry + 0.15 * scale], color='black', linewidth=3 * scale)

# 3. 데이터 및 애니메이션 실행
steps_data = [
    ([1, 0, 0, -2], "1단계: 처음 방정식", "x³ − 2 = 0"),
    ([1, 0, 0, -2], "2단계: 정수 자리 확인", "f(1) = −1,  f(2) = 6  →  x = 1.…"),
    ([1, 3, 3, -1], "3단계: x = 1 + y", "y³ + 3y² + 3y − 1 = 0"),
    ([1, 30, 300, -1000], "4단계: u = 10y", "u³ + 30u² + 300u − 1000 = 0"),
    ([1, 30, 300, -1000], "5단계: 첫째 소수 자리", "f(2) = −272,  f(3) = 197  →  x = 1.2…"),
    ([1, 360, 43200, -272000], "6단계: y = 0.2 + v/100", "v³ + 360v² + 43200v − 272000 = 0"),
    ([1, 360, 43200, -272000], "7단계: 둘째 소수 자리", "f(5) = −48,125,  f(6) = 376  →  x = 1.25…"),
    ([1, 0, 0, -2], "8단계: 근", "x ≈ 1.259921  (x³ ≈ 2)")
]

fig, ax = plt.subplots(figsize=(10, 6))

fps = 15
seconds_per_step = 5
total_frames = len(steps_data) * fps * seconds_per_step

def update(frame):
    ax.clear()
    
    step_idx = min(frame // (fps * seconds_per_step), len(steps_data) - 1)
    matrix, title_text, desc_text = steps_data[step_idx]
    
    ax.set_xlim(-1, 5)
    ax.set_ylim(-2, 2)
    ax.axis('off')
    
    ax.text(2, 1.6, title_text, fontsize=16, fontweight='bold', ha='center')
    ax.text(2, 1.3, desc_text, fontsize=12, ha='center', color='darkblue')
    
    labels = ["x³", "x²", "x", "상수항"]
    for i, val in enumerate(matrix):
        x_pos = i
        ax.text(x_pos, -1.2, labels[i], fontsize=11, ha='center')
        ax.text(x_pos, -1.5, f"val: {val:,}", fontsize=10, ha='center', color='darkgreen')
        
        is_first_vertical = (i % 2 == 0)
        draw_full_number_sangi(ax, x_pos, val, is_first_vertical)

ani = animation.FuncAnimation(fig, update, frames=total_frames, interval=1000/fps)

# mp4 동영상 파일 저장 시 주석 해제 (ffmpeg 필요)
# ani.save("sangi_full_digits.mp4", writer='ffmpeg', fps=fps)
plt.show()
