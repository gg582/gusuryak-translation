import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


# Matplotlib이 이 환경의 Noto CJK 컬렉션을 JP 이름으로 등록한다.
# Noto에는 한글을, DejaVu에는 Noto에 없는 아래첨자 수학 기호를 맡긴다.
plt.rcParams["font.family"] = ["Noto Sans CJK JP", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


SCALE = 1_000_000


def cube_root_newton_rods(start, scale=SCALE, count=4):
    """Return fixed-point Newton steps for the positive root of x³ - 2 = 0."""
    values = [start]
    value = start
    for _ in range(count - 1):
        # x' = (2x + 2/x²) / 3, written entirely with rod-friendly integers.
        reciprocal_term = (2 * scale**3) // (value * value)
        value = (2 * value + reciprocal_term) // 3
        values.append(value)
    return values


def draw_digit(ax, center_x, digit, vertical, scale=1.0):
    """Draw one 0–9 rod-numeral digit and return its last rod position."""
    # 빈칸과 구별되도록 0은 작은 빈 원으로 표시한다.
    if digit == 0:
        ax.add_patch(Circle((center_x, 0), 0.13 * scale, fill=False, color="black", linewidth=2 * scale))
        return center_x, 0

    ones = digit % 5
    has_five = digit >= 5
    spacing = 0.15 * scale
    start = -((ones - 1) * spacing) / 2 if ones else 0
    last = None

    for index in range(ones):
        if vertical:
            x = center_x + start + index * spacing
            ax.plot([x, x], [-0.35 * scale, 0.35 * scale], color="black", lw=4 * scale)
            last = (x, 0)
        else:
            y = start + index * spacing
            ax.plot([center_x - 0.35 * scale, center_x + 0.35 * scale], [y, y], color="black", lw=4 * scale)
            last = (center_x, y)

    if has_five:
        if vertical:
            ax.plot([center_x - 0.28 * scale, center_x + 0.28 * scale], [0.52 * scale, 0.52 * scale], color="black", lw=5 * scale)
            last = last or (center_x, 0.52 * scale)
        else:
            ax.plot([center_x, center_x], [-0.52 * scale, 0.52 * scale], color="black", lw=5 * scale)
            last = last or (center_x, 0)
    return last


def draw_number(ax, center_x, number):
    """Draw a non-negative integer as alternating rod-numeral digits."""
    digits = str(number)
    size = max(0.25, 0.8 / len(digits))
    width = 0.7 * size
    left = center_x - (len(digits) - 1) * width / 2
    for index, char in enumerate(digits):
        draw_digit(ax, left + index * width, int(char), index % 2 == 0, size)


steps = cube_root_newton_rods(1_250_000)

fig, ax = plt.subplots(figsize=(10, 6))


def update(frame):
    ax.clear()
    index = min(frame // 60, len(steps) - 1)
    value = steps[index]
    approximation = value / SCALE

    ax.set_xlim(-1, 7)
    ax.set_ylim(-2, 2)
    ax.axis("off")
    ax.text(3, 1.55, "산가지로 하는 뉴턴-랩슨법: x³ − 2 = 0", fontsize=16, fontweight="bold", ha="center")
    ax.text(3, 1.23, "aₙ₊₁ = (2aₙ + 2S³ ÷ aₙ²) ÷ 3   (S = 1,000,000)", fontsize=12, ha="center", color="darkblue")
    ax.text(1.2, 0.85, f"반복 {index}", fontsize=15, ha="center")
    ax.text(4.7, 0.85, f"x ≈ {approximation:.6f}", fontsize=15, ha="center")

    ax.text(3, -0.95, "산가지로 놓은 a = Sx", fontsize=12, ha="center")
    draw_number(ax, 3, value)
    ax.text(3, -1.55, f"정수값: {value:,}", fontsize=11, ha="center", color="darkgreen")


ani = animation.FuncAnimation(fig, update, frames=len(steps) * 60, interval=1000 / 15)
plt.show()
