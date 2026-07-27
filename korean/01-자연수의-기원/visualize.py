import os
import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ==========================================
# 1. 한글 폰트 자동 탐색 및 설정 (Noto CJK 우선)
# ==========================================
def setup_cjk_font():
    cjk_candidates = [
        'Noto Sans CJK KR', 'Noto Sans CJK JP', 'Noto Serif CJK KR',
        'Noto Serif CJK JP', 'NanumGothic', 'Malgun Gothic', 'AppleGothic'
    ]
    available_fonts = {f.name: f.fname for f in fm.fontManager.ttflist}
    
    # 1차: 정밀 매칭
    for font in cjk_candidates:
        if font in available_fonts:
            plt.rcParams['font.family'] = font
            plt.rcParams['axes.unicode_minus'] = False
            print(f"[Font Manager] 선택된 한글 폰트: {font}")
            return font
            
    # 2차: CJK/Gothic 키워드 서치
    for name, path in available_fonts.items():
        if any(k in name.lower() for k in ['cjk', 'nanum', 'malgun', 'gothic', 'korean']):
            plt.rcParams['font.family'] = name
            plt.rcParams['axes.unicode_minus'] = False
            print(f"[Font Manager] 키워드 탐색 폰트: {name}")
            return name
            
    plt.rcParams['axes.unicode_minus'] = False
    print("[Font Manager] 기본 폰트로 설정합니다. (CJK 폰트 미발견)")
    return "sans-serif"

# ==========================================
# 2. 십자형 그래프 클래스 및 분석 엔진
# ==========================================
class CrossGraphAnalyzer:
    def __init__(self):
        # 격자 좌표 (row, col) 기준 원소 정의 (중심 = (3, 2))
        self.grid_map = {
            (0, 2): 7,
            (1, 2): 2,
            (2, 2): 5,
            (3, 0): 8, (3, 1): 3, (3, 2): 5, (3, 3): 4, (3, 4): 9,
            (4, 2): 5,
            (5, 2): 1,
            (6, 2): 6
        }
        
        # NetworkX 그래프 생성
        self.G = nx.Graph()
        for (r, c), val in self.grid_map.items():
            self.G.add_node((r, c), val=val, label=f"{val}\n({r},{c})")
            
        # 간선(Edge) 연결 (상하좌우 인접)
        edges = [
            ((0,2), (1,2)), ((1,2), (2,2)), ((2,2), (3,2)),
            ((3,2), (4,2)), ((4,2), (5,2)), ((5,2), (6,2)),
            ((3,0), (3,1)), ((3,1), (3,2)), ((3,2), (3,3)), ((3,3), (3,4))
        ]
        self.G.add_edges_from(edges)
        
    def analyze_algebraic_properties(self):
        """대수적/수치적 성질 분석"""
        values = list(self.grid_map.values())
        center_val = self.grid_map[(3, 2)]
        
        v_arm = [self.grid_map[(r, 2)] for r in range(7)]
        h_arm = [self.grid_map[(3, c)] for c in range(5)]
        
        top_branch = [self.grid_map[(r, 2)] for r in range(3)]
        bot_branch = [self.grid_map[(r, 2)] for r in range(4, 7)]
        left_branch = [self.grid_map[(3, c)] for c in range(2)]
        right_branch = [self.grid_map[(3, c)] for c in range(3, 5)]
        
        # 질량 중심 (Center of Mass) 계산 (기하학적 중심 대비)
        r_coords = [r for r, c in self.grid_map.keys()]
        c_coords = [c for r, c in self.grid_map.keys()]
        weighted_r = sum(r * v for (r, c), v in self.grid_map.items()) / sum(values)
        weighted_c = sum(c * v for (r, c), v in self.grid_map.items()) / sum(values)
        
        return {
            "multiset": values,
            "total_sum": sum(values),
            "mean": float(np.mean(values)),
            "std": float(np.std(values)),
            "vertical_arm_sum": sum(v_arm),
            "horizontal_arm_sum": sum(h_arm),
            "center_value": center_val,
            "branch_sums": {
                "top": sum(top_branch),
                "bottom": sum(bot_branch),
                "left": sum(left_branch),
                "right": sum(right_branch)
            },
            "center_of_mass": {"row": round(weighted_r, 4), "col": round(weighted_c, 4)}
        }

    def analyze_graph_properties(self):
        """그래프 이론 및 위상적 성질 분석"""
        adj = nx.adjacency_matrix(self.G).todense()
        lap = nx.laplacian_matrix(self.G).todense()
        dist = nx.floyd_warshall_numpy(self.G)
        
        adj_eigs = np.linalg.eigvalsh(adj)
        lap_eigs = np.linalg.eigvalsh(lap)
        
        degree_cent = {str(k): round(v, 4) for k, v in nx.degree_centrality(self.G).items()}
        closeness_cent = {str(k): round(v, 4) for k, v in nx.closeness_centrality(self.G).items()}
        between_cent = {str(k): round(v, 4) for k, v in nx.betweenness_centrality(self.G).items()}
        eigen_cent = {str(k): round(v, 4) for k, v in nx.eigenvector_centrality(self.G).items()}
        
        return {
            "node_count": self.G.number_of_nodes(),
            "edge_count": self.G.number_of_edges(),
            "graph_type": "Spider Graph / Star-like Tree S(3, 3, 2, 2)",
            "diameter": nx.diameter(self.G),
            "radius": nx.radius(self.G),
            "wiener_index": float(nx.wiener_index(self.G)),
            "spectral_radius": float(np.max(adj_eigs)),
            "algebraic_connectivity": float(lap_eigs[1]),  # Fiedler value
            "adjacency_spectrum": [round(x, 4) for x in adj_eigs.tolist()],
            "laplacian_spectrum": [round(x, 4) for x in lap_eigs.tolist()],
            "centrality": {
                "degree": degree_cent,
                "closeness": closeness_cent,
                "betweenness": between_cent,
                "eigenvector": eigen_cent
            },
            "adj_matrix": adj.tolist(),
            "dist_matrix": dist.tolist()
        }

# ==========================================
# 3. 시각화 엔진
# ==========================================
def visualize_cross_graph(analyzer, output_image_path):
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle("십자형 그래프 대수적·위상적 구조 정밀 분석", fontsize=18, fontweight='bold')
    
    # 1) Grid Map & Node Value Heatmap
    ax1 = fig.add_subplot(2, 2, 1)
    grid_matrix = np.full((7, 5), np.nan)
    for (r, c), val in analyzer.grid_map.items():
        grid_matrix[r, c] = val
        
    im = ax1.imshow(grid_matrix, cmap='YlGnBu', aspect='equal')
    for (r, c), val in analyzer.grid_map.items():
        ax1.text(c, r, str(val), ha='center', va='center', fontsize=14, fontweight='bold')
    ax1.set_title("1. 십자형 배치 및 노드 가중치 열지도", fontsize=13)
    ax1.set_xlabel("열 (Column)")
    ax1.set_ylabel("행 (Row)")
    fig.colorbar(im, ax=ax1, fraction=0.046, pad=0.04)

    # 2) Graph Topology & Centrality Network Diagram
    ax2 = fig.add_subplot(2, 2, 2)
    pos = {node: (node[1], -node[0]) for node in analyzer.G.nodes()}  # Y축 반전
    betweenness = nx.betweenness_centrality(analyzer.G)
    node_sizes = [1000 + 3000 * betweenness[n] for n in analyzer.G.nodes()]
    node_colors = [analyzer.grid_map[n] for n in analyzer.G.nodes()]
    
    labels = {n: f"{analyzer.grid_map[n]}" for n in analyzer.G.nodes()}
    nx.draw_networkx_nodes(analyzer.G, pos, ax=ax2, node_size=node_sizes, node_color=node_colors, cmap=plt.cm.coolwarm)
    nx.draw_networkx_edges(analyzer.G, pos, ax=ax2, width=2, alpha=0.7)
    nx.draw_networkx_labels(analyzer.G, pos, labels, ax=ax2, font_size=12, font_weight='bold')
    ax2.set_title("2. 네트워크 토폴로지 (노드 크기: 매개 중심성)", fontsize=13)
    ax2.axis('off')

    # 3) Distance Matrix Heatmap
    ax3 = fig.add_subplot(2, 2, 3)
    dist_mat = nx.floyd_warshall_numpy(analyzer.G)
    im3 = ax3.imshow(dist_mat, cmap='magma_r')
    ax3.set_title("3. 최단 거리 행렬 (Distance Matrix)", fontsize=13)
    fig.colorbar(im3, ax=ax3, fraction=0.046, pad=0.04)

    # 4) Spectral Spectrum (Eigenvalues)
    ax4 = fig.add_subplot(2, 2, 4)
    adj_eigs = np.linalg.eigvalsh(nx.adjacency_matrix(analyzer.G).todense())
    lap_eigs = np.linalg.eigvalsh(nx.laplacian_matrix(analyzer.G).todense())
    
    x = np.arange(len(adj_eigs))
    ax4.plot(x, adj_eigs, 'o-', color='crimson', label='Adjacency Eigs', linewidth=2)
    ax4.plot(x, lap_eigs, 's--', color='royalblue', label='Laplacian Eigs', linewidth=2)
    ax4.set_title("4. 행렬 스펙트럼 (고윳값 분포)", fontsize=13)
    ax4.set_xlabel("고윳값 인덱스")
    ax4.set_ylabel("고윳값 (Eigenvalue)")
    ax4.grid(True, linestyle=':', alpha=0.6)
    ax4.legend()

    plt.tight_layout()
    plt.savefig(output_image_path, dpi=300)
    plt.close()
    print(f"[Exporter] 시각화 이미지 저장 완료: {output_image_path}")

# ==========================================
# 4. 내보내기 모듈 (JSON & Markdown)
# ==========================================
def export_results(alg_res, graph_res, json_path, md_path):
    # 1) JSON Export
    export_data = {
        "algebraic_analysis": alg_res,
        "graph_analysis": graph_res
    }
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    print(f"[Exporter] JSON 데이터 저장 완료: {json_path}")

    # 2) Markdown Report Export
    md_content = f"""# 십자형 그래프 대수적·위상적 구조 분석 보고서

## 1. 개요
본 보고서는 11개 노드로 구성된 십자형(Cross) 배치 데이터의 대수적 수치 성질 및 그래프 이론적 구조 특성을 분석한 결과입니다.

---

## 2. 대수적 성질 (Algebraic & Numerical Properties)

- **원소 다중집합**: $S = \\{{1, 2, 3, 4, 5, 5, 5, 6, 7, 8, 9\\}}$ (총합: **{alg_res['total_sum']}**)
- **중심점 노드 값**: **{alg_res['center_value']}** (좌표: `(3, 2)`)
- **축별 합계**:
  - 수직축 합계 (Vertical Sum): **{alg_res['vertical_arm_sum']}** (7 + 2 + 5 + 5 + 5 + 1 + 6)
  - 수평축 합계 (Horizontal Sum): **{alg_res['horizontal_arm_sum']}** (8 + 3 + 5 + 4 + 9)
- **가지(Branch)별 합계 (중심 제외)**:
  - 상단 가지 (Top): **{alg_res['branch_sums']['top']}**
  - 하단 가지 (Bottom): **{alg_res['branch_sums']['bottom']}**
  - 좌측 가지 (Left): **{alg_res['branch_sums']['left']}**
  - 우측 가지 (Right): **{alg_res['branch_sums']['right']}**
- **가중 질량 중심 (Center of Mass)**: Row = **{alg_res['center_of_mass']['row']}**, Col = **{alg_res['center_of_mass']['col']}**

---

## 3. 그래프 이론적 특성 (Graph Theoretical Properties)

- **그래프 분류**: 거미 그래프 / 별 모양 트리 $S(3, 3, 2, 2)$
- **노드 수 ($V$)**: {graph_res['node_count']}
- **간선 수 ($E$)**: {graph_res['edge_count']}
- **지름 (Diameter)**: {graph_res['diameter']}
- **반지름 (Radius)**: {graph_res['radius']}
- **위너 지수 (Wiener Index)**: {graph_res['wiener_index']}

### 스펙트럼 분석
- **스펙트럼 반지름 $\\rho(A)$**: `{graph_res['spectral_radius']:.4f}`
- **대수적 연결성 (Fiedler Value $\\lambda_2$)**: `{graph_res['algebraic_connectivity']:.4f}`
- **인접 행렬 고윳값 수열**:
  `{graph_res['adjacency_spectrum']}`

---

## 4. 결론 및 요약
1. **균형 및 대칭성**: 원소 총합은 55이며, 1부터 10까지의 정수 합과 동일합니다 (숫자 5가 3번 중복 사용됨).
2. **트리 중심성**: 지름 6의 트라이디자이너 구조에서 중심 노드 `(3,2)`가 모든 중심성 지표(Degree, Betweenness, Closeness, Eigenvector)에서 압도적 극댓값을 가집니다.
"""
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"[Exporter] Markdown 보고서 저장 완료: {md_path}")

# ==========================================
# 메인 실행부
# ==========================================
if __name__ == "__main__":
    setup_cjk_font()
    
    analyzer = CrossGraphAnalyzer()
    alg_results = analyzer.analyze_algebraic_properties()
    graph_results = analyzer.analyze_graph_properties()
    
    img_filename = "cross_graph_analysis.png"
    json_filename = "cross_graph_analysis.json"
    md_filename = "cross_graph_report.md"
    
    visualize_cross_graph(analyzer, img_filename)
    export_results(alg_results, graph_results, json_filename, md_filename)
    
    print("\n=== 분석 완료 ===")
    print(f"1. 시각화 이미지: {img_filename}")
    print(f"2. Markdown 보고서: {md_filename}")
    print(f"3. JSON 데이터: {json_filename}")
