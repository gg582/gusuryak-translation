# -*- coding: utf-8 -*-
"""Shared base solver for each-gets series with original simple visualization.
The implementation mirrors the original `gakdeuk_solver.py` logic (MILP via pulp)
and provides `visualize_solution` that draws clusters as simple polygons with
center points, exactly as the user demanded.
"""

import sys
from dataclasses import dataclass
from typing import List, Tuple, Optional

import pulp
import matplotlib.pyplot as plt
import numpy as np


@dataclass
class EachGetsSolution:
    n: int
    S: int
    adjacency: List[Tuple[int, int]]
    clusters: List[Tuple[int, ...]]
    shared_vertices: List[int]


class EachGetsSolver:
    """MILP solver for a given puzzle size `n` and target sum `S`.
    It constructs variables for each vertex, enforces residue class constraints,
    adjacency constraints, and optional symmetry breaking.
    """

    def __init__(self, n: int, S: int, adjacency: List[Tuple[int, int]],
                 max_multiplicity: Optional[int] = None,
                 symmetry: Optional[str] = None,
                 residue_balance: bool = False):
        self.n = n
        self.S = S
        self.adjacency = adjacency
        self.max_multiplicity = max_multiplicity
        self.symmetry = symmetry
        self.residue_balance = residue_balance
        self.model = pulp.LpProblem("EachGets", pulp.LpMinimize)
        self._build_variables()
        self._add_constraints()
        # Dummy objective (we just need feasibility)
        self.model += 0

    def _build_variables(self):
        self.X = pulp.LpVariable.dicts("X", range(1, self.n * 5 + 1), lowBound=0, upBound=self.n, cat=pulp.LpInteger)
        self.T = pulp.LpVariable.dicts("T", range(5), lowBound=0, cat=pulp.LpInteger)
        self.U = pulp.LpVariable.dicts("U", range(5), lowBound=0, cat=pulp.LpInteger)
        self.shared = pulp.LpVariable.dicts("shared", range(1, self.n * 5 + 1), cat=pulp.LpBinary)

    def _add_constraints(self):
        # Sum constraints per cluster
        for i in range(5):
            start = i * self.n + 1
            end = (i + 1) * self.n + 1
            self.model += pulp.lpSum(self.X[v] for v in range(start, end)) == self.S

        # Total sum constraint
        self.model += pulp.lpSum(self.X.values()) == 5 * self.S

        # Adjacent clusters must have equal totals
        for i, j in self.adjacency:
            start_i = i * self.n + 1
            start_j = j * self.n + 1
            self.model += pulp.lpSum(self.X[v] for v in range(start_i, start_i + self.n)) == \
                            pulp.lpSum(self.X[v] for v in range(start_j, start_j + self.n))

        # Shared vertices appear in at most two clusters (binary flag)
        for v in range(1, self.n * 5 + 1):
            self.model += self.shared[v] <= 1
            self.model += self.X[v] - self.shared[v] * self.n >= 0

        if self.max_multiplicity:
            for v in range(1, self.n * 5 + 1):
                self.model += self.X[v] <= self.max_multiplicity

        if self.symmetry:
            # Simple symmetry: enforce non‑decreasing first vertex of each cluster
            for i in range(4):
                self.model += self.X[i * self.n + 1] <= self.X[(i + 1) * self.n + 1]

        if self.residue_balance:
            for r in range(5):
                self.model += pulp.lpSum(self.X[v] for v in range(1, self.n * 5 + 1) if v % 5 == r) == self.T[r]
                self.model += pulp.lpSum(self.shared[v] for v in range(1, self.n * 5 + 1) if v % 5 == r) == self.U[r]

    def solve(self) -> Optional[EachGetsSolution]:
        res = self.model.solve(pulp.PULP_CBC_CMD(msg=False))
        if pulp.LpStatus[res] != "Optimal":
            return None
        clusters = []
        for i in range(5):
            start = i * self.n + 1
            clusters.append(tuple(int(self.X[v].value()) for v in range(start, start + self.n)))
        shared_vertices = [v for v in range(1, self.n * 5 + 1) if self.shared[v].value() == 1]
        return EachGetsSolution(self.n, self.S, self.adjacency, clusters, shared_vertices)

    @classmethod
    def search_s(cls, n: int, adjacency: List[Tuple[int, int]], S_start: int, S_end: int, **kwargs) -> List[EachGetsSolution]:
        sols = []
        for S in range(S_start, S_end + 1):
            solver = cls(n, S, adjacency, **kwargs)
            sol = solver.solve()
            if sol:
                sols.append(sol)
        return sols


# ---------------------------------------------------------------------------
# Original simple visualization (polygons + centre)
# ---------------------------------------------------------------------------

def visualize_solution(sol: EachGetsSolution, output_path: Optional[str] = None) -> None:
    """Draw clusters as simple polygons with a centre point.
    Shared vertices are highlighted in red.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("[오류] matplotlib이 설치되어 있지 않습니다.", file=sys.stderr)
        return

    adjacency_set = {tuple(sorted(e)) for e in sol.adjacency}
    # Base positions – keep the original layout choices
    if adjacency_set == {(0, 1), (0, 2), (0, 3), (0, 4)}:
        positions = {0: (0, 0), 1: (0, 2), 2: (2, 0), 3: (0, -2), 4: (-2, 0)}
    elif adjacency_set == {(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (3, 4)}:
        positions = {0: (0, 0), 1: (-1.5, 1.5), 2: (1.5, 1.5), 3: (-1.5, -1.5), 4: (1.5, -1.5)}
    else:
        angles = [i * 2 * np.pi / 5 for i in range(5)]
        positions = {i: (np.cos(a), np.sin(a)) for i, a in enumerate(angles)}

    fig, ax = plt.subplots(figsize=(8, 8))

    names = ["중", "상", "우", "하", "좌"]
    for c, verts in enumerate(sol.clusters):
        cx, cy = positions[c]
        n = len(verts)
        for idx, v in enumerate(sorted(verts)):
            theta = idx * 2 * np.pi / max(n, 1)
            radius = 0.3
            vx = cx + radius * np.cos(theta)
            vy = cy + radius * np.sin(theta)
            color = "#E74C3C" if v in sol.shared_vertices else "#2ECC71"
            ax.scatter(vx, vy, s=250, c=color, edgecolors="black", linewidths=1.2)
            ax.text(vx, vy, str(v), ha="center", va="center", fontsize=9,
                    fontweight="bold",
                    color="white" if v in sol.shared_vertices else "black")
        ax.text(cx, cy, names[c], ha="center", va="center", fontsize=12,
                fontweight="bold", color="black")

    for i, j in sol.adjacency:
        x_vals = [positions[i][0], positions[j][0]]
        y_vals = [positions[i][1], positions[j][1]]
        ax.plot(x_vals, y_vals, "k--", linewidth=1.5, alpha=0.5)

    ax.set_aspect("equal")
    ax.axis("off")
    if output_path:
        plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor="white")
    else:
        plt.show()


# ---------------------------------------------------------------------------
# Advanced Graph & Topological Extensions for 04-unification
# ---------------------------------------------------------------------------

def analyze_solution_topology(sol: EachGetsSolution) -> dict:
    """Compute topology metrics for an EachGetsSolution using NetworkX."""
    import networkx as nx
    G = nx.Graph()
    G.add_edges_from(sol.adjacency)
    betw = nx.betweenness_centrality(G)
    A = nx.adjacency_matrix(G).toarray().astype(float)
    eigenvals = np.linalg.eigvals(A)
    spectral_radius = float(np.max(np.abs(eigenvals)))
    return {
        "betweenness": betw,
        "eigenvalues": eigenvals,
        "spectral_radius": spectral_radius
    }

