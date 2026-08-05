import platform
import matplotlib.pyplot as plt

# OS별 한글 폰트 및 마이너스 기호 설정
system_os = platform.system()

if system_os == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif system_os == 'Darwin':  # macOS
    plt.rcParams['font.family'] = 'AppleGothic'
else:  # Linux (Ubuntu/Debian 등 NanumFont 설치 환경)
    plt.rcParams['font.family'] = 'NanumGothic'

plt.rcParams['axes.unicode_minus'] = False

# 좌표 설정
# 갑(A), 을(B), 병(C), 정(D), 무(E)
A = (0, 8)   # 갑
B = (0, 0)   # 을
C = (4, 0)   # 병
D = (6, 0)   # 정
E = (6, 3)   # 무

plt.figure(figsize=(6, 8))

# 선 그리기
plt.plot([B[0], D[0]], [B[1], D[1]], 'k-', lw=2)  # 지평선 (을-정)
plt.plot([A[0], B[0]], [A[1], B[1]], 'k--', lw=2) # 물체 높이 (갑-을)
plt.plot([E[0], D[0]], [E[1], D[1]], 'k-', lw=2)  # 사람 높이 (무-정)
plt.plot([A[0], C[0]], [A[1], C[1]], 'k-', lw=2)  # 입사 광선 (갑-병)
plt.plot([E[0], C[0]], [E[1], C[1]], 'k-', lw=2)  # 반사 광선 (무-병)

# 거울 표시 (병 위치 원형)
circle = plt.Circle(C, 0.8, color='k', fill=False, lw=1.5)
plt.gca().add_patch(circle)

# 한글 라벨 배치
plt.text(A[0] - 0.3, A[1] + 0.2, '갑', fontsize=16, fontweight='bold')
plt.text(B[0] - 0.3, B[1] - 0.5, '을', fontsize=16, fontweight='bold')
plt.text(C[0] - 0.1, C[1] - 0.5, '병', fontsize=16, fontweight='bold')
plt.text(D[0] + 0.2, D[1] - 0.5, '정', fontsize=16, fontweight='bold')
plt.text(E[0] + 0.1, E[1] + 0.2, '무', fontsize=16, fontweight='bold')

plt.xlim(-1, 8)
plt.ylim(-1, 10)
plt.axis('off')
plt.gca().set_aspect('equal', adjustable='box')

plt.show()
