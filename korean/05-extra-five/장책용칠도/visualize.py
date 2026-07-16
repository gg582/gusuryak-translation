import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# 한글 폰트 설정 (OS별 호환성 반영)
plt.rcParams['font.family'] = ['NanumGothic', 'NanumBarunGothic', 'Malgun Gothic', 'AppleGothic', 'DejaVu Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# 1. 기하학적 3축 좌표 자동 계산 (중앙 7을 (0,0) 기준 설정)
diagram_positions_68 = {7: (0.0, 0.0)}

# 축 2 (수직선: 90도 방향)
line2_nodes = [5, 18, 9, 7, 12, 2, 15]
for i, node in enumerate(line2_nodes):
    if node != 7:
        diagram_positions_68[node] = (0.0, (3 - i) * 1.2)

# 축 1 (좌상 -> 우하 대각선: 150도 방향)
line1_nodes = [4, 10, 19, 7, 1, 14, 13]
angle1 = np.radians(150)
for i, node in enumerate(line1_nodes):
    if node != 7:
        dist = 3 - i
        diagram_positions_68[node] = (dist * np.cos(angle1) * 1.2, dist * np.sin(angle1) * 1.2)

# 축 3 (우상 -> 좌하 대각선: 30도 방향)
line3_nodes = [8, 6, 17, 7, 3, 11, 16]
angle3 = np.radians(30)
for i, node in enumerate(line3_nodes):
    if node != 7:
        dist = 3 - i
        diagram_positions_68[node] = (dist * np.cos(angle3) * 1.2, dist * np.sin(angle3) * 1.2)

# 2. 3개 축의 단순 직선 간선만 구성
edges_68 = []
for line in [line1_nodes, line2_nodes, line3_nodes]:
    for i in range(len(line) - 1):
        edges_68.append((line[i], line[i+1]))

# 3. 그래프 시각화
G = nx.Graph()
G.add_nodes_from(diagram_positions_68.keys())
G.add_edges_from(edges_68)

fig, ax = plt.subplots(figsize=(9, 9))

# 중앙 7 노드와 일반 노드의 색상 분리
node_colors = ['#FF9999' if node == 7 else '#FFFBDE' for node in G.nodes()]

nx.draw_networkx_nodes(G, diagram_positions_68, node_color=node_colors, node_size=1300, edgecolors='black', linewidths=1.5, ax=ax)
nx.draw_networkx_labels(G, diagram_positions_68, font_size=16, font_weight='bold', ax=ax)
nx.draw_networkx_edges(G, diagram_positions_68, width=2.5, edge_color='gray', ax=ax)

plt.title("구수략 - 장책용칠도(章策用七圖) (합 = 68)", fontsize=16, pad=25, fontweight='bold')
plt.axis('off')
plt.tight_layout()
plt.show()
