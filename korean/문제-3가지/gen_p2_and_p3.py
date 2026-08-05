import matplotlib.pyplot as plt
import platform

# OS별 한글 폰트 및 마이너스 기호 설정
system_os = platform.system()
if system_os == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif system_os == 'Darwin':  # macOS
    plt.rcParams['font.family'] = 'AppleGothic'
else:  # Linux
    plt.rcParams['font.family'] = 'NanumGothic'

plt.rcParams['axes.unicode_minus'] = False

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

# --------------------------------------------------
# 표목 거리 측량도 (유클리드 닮음 정합성 적용)
# --------------------------------------------------
# 정(D)에서 출발한 시선이 표목 끝 병(C)을 지나 목표물 을(B)에 도달함
# 직선 방정식: y - y_D = m * (x - x_D)
D_1 = (0, 6)     # 정 (관측자의 눈 위치)
E_1 = (0, 0)     # 무 (관측자 발 위치)
G_1 = (0, 4.5)   # 기 (표목 상단 수평선과 수직축의 교점)
A_1 = (2, 0)     # 갑 (표목 위치 바닥)
C_1 = (2, 4.5)   # 병 (표목 꼭대기) -> 기울기 m = (4.5 - 6) / (2 - 0) = -0.75
B_1 = (8, 0)     # 을 (목표물, x_B = 0 - (6 / -0.75) = 8)

# 주요 선분 작도
ax1.plot([E_1[0], B_1[0]], [E_1[1], B_1[1]], 'k-', lw=2)    # 지평선 (무-갑-을)
ax1.plot([E_1[0], D_1[0]], [E_1[1], D_1[1]], 'k-', lw=2)    # 관측축 (무-기-정)
ax1.plot([A_1[0], C_1[0]], [A_1[1], C_1[1]], 'k-', lw=2)    # 표목 (갑-병)
ax1.plot([G_1[0], C_1[0]], [G_1[1], C_1[1]], 'k--', lw=1.5) # 보조 수평선 (기-병)
ax1.plot([D_1[0], B_1[0]], [D_1[1], B_1[1]], 'k-', lw=2)    # 관측 시선 (정-병-을)

# 라벨배치 (음독 한글)
ax1.text(D_1[0] - 0.4, D_1[1] + 0.1, '정', fontsize=14, fontweight='bold')
ax1.text(G_1[0] - 0.4, G_1[1] - 0.1, '기', fontsize=14, fontweight='bold')
ax1.text(E_1[0] - 0.4, E_1[1] - 0.3, '무', fontsize=14, fontweight='bold')
ax1.text(C_1[0] + 0.1, C_1[1] + 0.1, '병', fontsize=14, fontweight='bold')
ax1.text(A_1[0], A_1[1] - 0.4, '갑', fontsize=14, fontweight='bold')
ax1.text(B_1[0] + 0.1, B_1[1] - 0.4, '을', fontsize=14, fontweight='bold')

ax1.set_xlim(-1, 9)
ax1.set_ylim(-1, 7)
ax1.set_title("표목 거리 측량", fontsize=14)
ax1.axis('off')
ax1.set_aspect('equal', adjustable='box')

# --------------------------------------------------
# 중구법 측량도 (이중 꺾쇠자 및 정밀 시선 교차 정합성)
# 병(C)에서 연장된 두 시선이 우측 기준선 상의 점들을 통과
# --------------------------------------------------
C_2 = (0, 0)     # 병 (좌하단 기준점)
CH_2 = (6, 0)    # 축 (우하단)
GI_2 = (0, 4.5)  # 기 (좌상단 사각형 꼭짓점)
A_2 = (6, 4.5)   # 갑 (우상단 사각형 꼭짓점)

# 우측 수직선 상의 지점들 (기울기에 따른 기하적 위치)
# 첫 번째 시선 (병 -> 무): 기울기 1.0 (45도) -> 戊(x=6, y=6.0)
# 두 번째 시선 (병 -> 신): 기울기 1.25 -> 辛(x=6, y=7.5)
E_2 = (6, 6.0)   # 무 (첫 번째 관측 교점)
S_2 = (6, 7.5)   # 신 (두 번째 관측 교점)
G_2 = (6, 5.25)  # 경 (무와 갑 사이의 중구 보조점)

# 사각형 뼈대 및 연장 수직선
ax2.plot([C_2[0], CH_2[0]], [C_2[1], CH_2[1]], 'k-', lw=2)  # 하단선 (병-축)
ax2.plot([C_2[0], GI_2[0]], [C_2[1], GI_2[1]], 'k-', lw=2)  # 좌측 수직선 (병-기)
ax2.plot([GI_2[0], A_2[0]], [GI_2[1], A_2[1]], 'k-', lw=2)  # 사각형 상단선 (기-갑)
ax2.plot([CH_2[0], S_2[0]], [CH_2[1], S_2[1]], 'k-', lw=2)  # 우측 수직 연장선 (축-갑-경-무-신)

# 안쪽 구고거(꺾쇠자) 두 번째 수직축
ax2.plot([5.2, 5.2], [0, S_2[1]], 'k-', lw=1.2)

# 병(C)에서 발사되는 2개의 정확한 시선 직선
ax2.plot([C_2[0], S_2[0]], [C_2[1], S_2[1]], 'k-', lw=1.8) # 병 -> 신
ax2.plot([C_2[0], E_2[0]], [C_2[1], E_2[1]], 'k-', lw=1.8) # 병 -> 무

# 꺾쇠자(구고거) 수평선 구조
ax2.plot([5.2, 6.0], [G_2[1], G_2[1]], 'k-', lw=1.5) # 경 위치 수평선
ax2.plot([5.2, 6.0], [E_2[1], E_2[1]], 'k-', lw=1.5) # 무 위치 수평선
ax2.plot([5.2, 6.0], [S_2[1], S_2[1]], 'k-', lw=1.5) # 신 위치 수평선

# 라벨 배치 (음독 한글)
ax2.text(C_2[0] - 0.4, C_2[1] - 0.3, '병', fontsize=14, fontweight='bold')
ax2.text(CH_2[0] + 0.1, CH_2[1] - 0.3, '축', fontsize=14, fontweight='bold')
ax2.text(GI_2[0] - 0.4, GI_2[1] - 0.1, '기', fontsize=14, fontweight='bold')

ax2.text(A_2[0] + 0.2, A_2[1] - 0.1, '갑', fontsize=13, fontweight='bold')
ax2.text(G_2[0] + 0.2, G_2[1] - 0.1, '경', fontsize=13, fontweight='bold')
ax2.text(E_2[0] + 0.2, E_2[1] - 0.1, '무', fontsize=13, fontweight='bold')
ax2.text(S_2[0] + 0.2, S_2[1] - 0.1, '신', fontsize=13, fontweight='bold')

ax2.set_xlim(-1, 8)
ax2.set_ylim(-1, 9)
ax2.set_title("중구법 측량", fontsize=14)
ax2.axis('off')
ax2.set_aspect('equal', adjustable='box')

plt.tight_layout()
plt.show()
