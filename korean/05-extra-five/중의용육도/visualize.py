import matplotlib.pyplot as plt
import matplotlib.patches as patches
import networkx as nx

# 한글 폰트 설정 (OS 환경별 호환성을 위해 우선순위 부여)
plt.rcParams['font.family'] = ['NanumGothic', 'NanumBarunGothic', 'Malgun Gothic', 'AppleGothic', 'DejaVu Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# 1. 16개 노드의 2차원 좌표 정보
diagram_positions = {
    7: (-2.5, 3), 16: (-1, 3.2), 1: (1, 3.2), 6: (2.5, 3),
    13: (-3, 1.5), 11: (-1, 1), 10: (1, 1), 4: (3, 1.5),
    3: (-3, -1.5), 9: (-1, -1), 12: (1, -1), 14: (3, -1.5),
    8: (-2.5, -3), 2: (-1, -3.2), 15: (1, -3.2), 5: (2.5, -3)
}

# 2. 오직 4개의 T자 화살표 형태의 간선만 정의 (각 그룹 간 독립성 유지)
correct_edges = [
    # 좌상단 T (중심 7 -> 16, 13, 11)
    (7, 16), (7, 13), (7, 11),
    # 우상단 T (중심 6 -> 1, 10, 4)
    (6, 1), (6, 10), (6, 4),
    # 좌하단 T (중심 8 -> 3, 9, 2)
    (8, 3), (8, 9), (8, 2),
    # 우하단 T (중심 5 -> 12, 14, 15)
    (5, 12), (5, 14), (5, 15)
]

# 3. 그래프 객체 생성 및 간선 추가
G = nx.Graph()
G.add_nodes_from(diagram_positions.keys())
G.add_edges_from(correct_edges)

fig, ax = plt.subplots(figsize=(9, 9))

# 4. 노드 및 숫자 라벨 그리기 (연한 노랑 배경)
nx.draw_networkx_nodes(G, diagram_positions, node_color='#FFFBDE', node_size=1500, edgecolors='black', linewidths=1.5, ax=ax)
nx.draw_networkx_labels(G, diagram_positions, font_size=18, font_weight='bold', ax=ax)

# 5. 간선 그리기 (T자 화살표 4개만 표현)
nx.draw_networkx_edges(G, diagram_positions, width=2.5, edge_color='black', ax=ax)

# 6. 각 합 51 구역을 타원으로 표현 (반투명 처리)
ellipse_colors = {
    'top': ('#FFD700', 0.15),    # 상단 (노랑)
    'left': ('#87CEEB', 0.15),   # 좌측 (파랑)
    'bottom': ('#3CB371', 0.15), # 하단 (초록)
    'right': ('#F08080', 0.15)    # 우측 (분홍)
}

# 상단 그룹 타원 (7, 16, 1, 6, 11, 10)
ellipse_top = patches.Ellipse((0, 2.5), width=6.8, height=3.0, color=ellipse_colors['top'][0], alpha=ellipse_colors['top'][1])
# 좌측 그룹 타원 (7, 13, 11, 3, 9, 8)
ellipse_left = patches.Ellipse((-2.0, 0), width=3.5, height=6.8, color=ellipse_colors['left'][0], alpha=ellipse_colors['left'][1])
# 하단 그룹 타원 (8, 2, 9, 12, 15, 5)
ellipse_bottom = patches.Ellipse((0, -2.5), width=6.8, height=3.0, color=ellipse_colors['bottom'][0], alpha=ellipse_colors['bottom'][1])
# 우측 그룹 타원 (6, 10, 4, 12, 14, 5)
ellipse_right = patches.Ellipse((2.0, 0), width=3.5, height=6.8, color=ellipse_colors['right'][0], alpha=ellipse_colors['right'][1])

for ell in [ellipse_top, ellipse_left, ellipse_bottom, ellipse_right]:
    ax.add_patch(ell)

# 7. 합 51 정보 텍스트 추가 (한글 적용)
label_font = {'weight': 'bold', 'color': '#333333'}
ax.text(0, 4.3, "합 = 51", ha='center', fontdict=label_font, fontsize=13)
ax.text(-4.2, 0, "합 = 51", va='center', rotation=90, fontdict=label_font, fontsize=13)
ax.text(0, -4.3, "합 = 51", ha='center', fontdict=label_font, fontsize=13)
ax.text(4.2, 0, "합 = 51", va='center', rotation=-90, fontdict=label_font, fontsize=13)

# 제목 설정 (한글 적용)
plt.title("구수략 - 중의용육도(重儀用六圖)", fontsize=16, pad=40, fontweight='bold')
plt.axis('off')
plt.tight_layout()
plt.show()
