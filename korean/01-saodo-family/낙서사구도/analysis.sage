# SageMath script to analyze the graph structure
EDGES = [
    (19, 2), (2, 14), (14, 5), (5, 16), (16, 7), (7, 19), 
    (17, 4), (4, 16), (16, 10), (10, 12), (12, 9), (9, 17), 
    (5, 18), (18, 3), (3, 13), (13, 8), (8, 11), (11, 5), 
    (10, 6), (6, 1), (1, 20), (20, 15), (15, 11), (11, 10),
]
G = Graph([list(range(1, 21)), EDGES], format='vertices_and_edges')

def analyze_graph_structure(G):
    print(f"1. Connectivity: {G.is_connected()}")
    print(f"2. Planarity: {G.is_planar()}")
    print(f"3. Automorphism Group Order: {G.automorphism_group().order()}")
    
    # Laplacian Spectrum links directly to the solution space constraints
    L = G.laplacian_matrix()
    print(f"4. Laplacian Spectrum: {L.eigenvalues()}")
    
    # Degree distribution characterizes the rigidity
    degrees = G.degree()
    print(f"5. Degree Distribution: {sorted(degrees)}")
    
    # Cycle basis relates to the magic sum constraints
    print(f"6. Cycle Basis Size: {len(G.cycle_basis())}")
    
    # Characteristic polynomial directly relates to the Determinant problem
    print(f"7. Characteristic Polynomial: {G.adjacency_matrix().charpoly()}")

analyze_graph_structure(G)
