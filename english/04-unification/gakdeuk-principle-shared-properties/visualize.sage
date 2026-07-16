# radial_symmetry_network_visualize.sage
# Visualization of the Radial Symmetry Network (RSN) in a Cross-Pattern Layout

def create_radial_symmetry_graph(n):
    """
    Creates an RSN graph.
    Structure: 5 radial clusters, each with one central vertex and n-1 peripheral vertices.
    """
    G = Graph()
    for i in range(5):
        for j in range(1, n):
            G.add_edge(f"V{i}_0", f"V{i}_{j}")
            
    # Connect cluster centers to form the core
    G.add_cycle([f"V{i}_0" for i in range(5)])
    return G

print("--- Radial Symmetry Network (RSN) - Cross-Pattern Layout ---")

for n in range(5, 10):
    G = create_radial_symmetry_graph(n)
    
    # 0: Center, 1:North, 2:South, 3:West, 4:East
    pos = {}
    coords = {0: (0, 0), 1: (0, 3), 2: (0, -3), 3: (-3, 0), 4: (3, 0)}
    
    for i in range(5):
        cx, cy = coords[i]
        pos[f"V{i}_0"] = (cx, cy)
        for j in range(1, n):
            angle = 2 * pi * (j-1) / (n-1)
            pos[f"V{i}_{j}"] = (cx + 0.6 * cos(angle), cy + 0.6 * sin(angle))
    
    symmetry_order = G.automorphism_group().order()
    evals = G.laplacian_matrix().eigenvalues()
    spectral_radius = float(max(evals).n())
    
    print(f"n={n} | Symmetry Order: {symmetry_order:<6} | Spectral Radius: {spectral_radius:.2f}")
    
    G.plot(pos=pos, vertex_size=250, vertex_color='salmon', vertex_labels=False, edge_color='gray',
           edge_thickness=0.5, title=f"RSN Cross-Pattern (n={n})").show()
