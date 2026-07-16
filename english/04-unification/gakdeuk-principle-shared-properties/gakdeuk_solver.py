#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
N-Each-Gets (各得) Puzzle MILP Solver — integrated geometry, phase, and visualization

Uses Python + PuLP instead of SageMath.

Features:
  1. Cluster adjacency-graph-based sharing constraints
  2. mod 5 remainder (phase) equivalence-class constraints
  3. Pairwise shared-vertex-count constraints
  4. Up/down / left/right residue symmetry constraints
  5. Multiple-solution enumeration and JSON save
  6. matplotlib-based visualization (--visualize)

Example usage:
  source venv/bin/activate
  python gakdeuk_solver.py --all --time-limit 180 --output solutions.json --visualize
  python gakdeuk_solver.py --n 6 --max 20 --sum 63 --adjacency honeycomb \
      --max-multiplicity 3 --pair-shared-counts "0-1:2,0-2:2,0-3:2,0-4:2,1-2:2,3-4:2" \
      --symmetry both --max-solutions 5 --output yukdo.json --visualize
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from itertools import combinations
from pathlib import Path
from typing import Iterable

import pulp


@dataclass(frozen=True)
class EachGetsSolution:
    """Solution returned by the solver."""

    n: int
    N_max: int
    S: int
    clusters: tuple[tuple[int, ...], ...]
    multiplicity: dict[str, int]
    shared_vertices: tuple[int, ...]
    missing: tuple[int, ...]
    adjacency: list[list[int]]

    def total_sum(self) -> int:
        return sum(v for v in range(1, self.N_max + 1) if v not in self.missing)

    def duplicated_sum(self) -> int:
        return 5 * self.S

    def duplicated_amount(self) -> int:
        return self.duplicated_sum() - self.total_sum()

    def residue_counts(self) -> list[dict[str, int]]:
        """Per-cluster mod 5 residue counts (1-based)."""
        counts = []
        for cluster in self.clusters:
            c = defaultdict(int)
            for v in cluster:
                c[str(v % 5 if v % 5 != 0 else 5)] += 1
            counts.append(dict(c))
        return counts

    def to_dict(self) -> dict:
        """Dictionary for JSON serialization."""
        return {
            "n": self.n,
            "N_max": self.N_max,
            "S": self.S,
            "clusters": [list(c) for c in self.clusters],
            "multiplicity": self.multiplicity,
            "shared_vertices": sorted(self.shared_vertices),
            "missing": sorted(self.missing),
            "adjacency": self.adjacency,
            "total_sum": self.total_sum(),
            "duplicated_sum": self.duplicated_sum(),
            "duplicated_amount": self.duplicated_amount(),
            "residue_counts": self.residue_counts(),
        }

    def __str__(self) -> str:
        lines = [
            f"N={self.n}, N_max={self.N_max}, S={self.S}",
            f"Unique vertex sum T={self.total_sum()}, duplicated-inclusive sum 5S={self.duplicated_sum()}, D={self.duplicated_amount()}",
            f"Adjacency graph: {self.adjacency}",
            f"Missing numbers: {list(self.missing) if self.missing else 'None'}",
            f"Shared vertices: {sorted(self.shared_vertices)}",
        ]
        names = ["Center", "Up", "Right", "Down", "Left"]
        for i, cluster in enumerate(self.clusters, 1):
            rc = self.residue_counts()[i - 1]
            rc_str = ", ".join(f"{k}:{v}" for k, v in sorted(rc.items()))
            lines.append(
                f"  C{i}({names[i-1]}): {' + '.join(map(str, cluster))} = {sum(cluster)}  [residue {rc_str}]"
            )
        return "\n".join(lines)


# ============================================================
# 1. Adjacency graph and connected-subset utilities
# ============================================================

PREDEFINED_ADJACENCY = {
    "cross": {(0, 1), (0, 2), (0, 3), (0, 4)},
    "honeycomb": {(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (3, 4)},
    "grid": {(0, 1), (0, 2), (0, 3), (0, 4)},
}


def parse_adjacency(s: str) -> set[tuple[int, int]]:
    edges: set[tuple[int, int]] = set()
    for token in s.split(","):
        a, b = token.strip().split("-")
        edges.add((int(a), int(b)))
    return edges


def get_adjacency(name_or_string: str) -> frozenset[tuple[int, int]]:
    if name_or_string in PREDEFINED_ADJACENCY:
        return frozenset(PREDEFINED_ADJACENCY[name_or_string])
    return frozenset(parse_adjacency(name_or_string))


def connected_subsets(
    adjacency: frozenset[tuple[int, int]], max_size: int
) -> list[frozenset[int]]:
    graph: dict[int, set[int]] = defaultdict(set)
    for a, b in adjacency:
        graph[a].add(b)
        graph[b].add(a)
    nodes = list(range(5))
    result: list[frozenset[int]] = []
    seen: set[frozenset[int]] = set()

    def is_connected(subset: frozenset[int]) -> bool:
        if len(subset) <= 1:
            return True
        start = next(iter(subset))
        visited = {start}
        stack = [start]
        while stack:
            cur = stack.pop()
            for nb in graph[cur]:
                if nb in subset and nb not in visited:
                    visited.add(nb)
                    stack.append(nb)
        return visited == subset

    for size in range(1, max_size + 1):
        for combo in combinations(nodes, size):
            subset = frozenset(combo)
            if subset not in seen and is_connected(subset):
                seen.add(subset)
                result.append(subset)
    return result


def parse_pair_shared_counts(s: str) -> dict[tuple[int, int], int]:
    """'0-1:2,0-2:2' -> {(0,1):2, (0,2):2}"""
    result: dict[tuple[int, int], int] = {}
    for token in s.split(","):
        pair, count = token.strip().split(":")
        a, b = pair.split("-")
        result[(int(a), int(b))] = int(count)
    return result


# ============================================================
# 2. Solver
# ============================================================

class EachGetsSolver:
    def __init__(self, solver_name: str | None = None, verbose: int = 0):
        self.solver_name = solver_name
        self.verbose = verbose

    def _make_solver(self, time_limit: int | None = None) -> pulp.LpSolver:
        if self.solver_name:
            solver = pulp.getSolver(self.solver_name, msg=self.verbose)
        else:
            solver = pulp.PULP_CBC_CMD(msg=self.verbose, timeLimit=time_limit or 300)
        return solver

    def solve(
        self,
        n: int,
        N_max: int,
        S: int,
        adjacency: frozenset[tuple[int, int]] | None = None,
        missing: Iterable[int] | None = None,
        auto_missing: bool = False,
        missing_count: int | None = None,
        missing_sum: int | None = None,
        required: Iterable[int] | None = None,
        max_multiplicity: int = 2,
        residue_balance: bool = False,
        residue_slack: int = 1,
        pair_shared_counts: dict[tuple[int, int], int] | None = None,
        symmetry: str | None = None,
        forbid_solutions: list[EachGetsSolution] | None = None,
        time_limit: int | None = None,
    ) -> EachGetsSolution | None:
        """
        Find a single solution. Solutions given in forbid_solutions are excluded.
        """
        if missing and auto_missing:
            raise ValueError("missing and auto_missing cannot be used together.")

        if adjacency is None:
            adjacency = frozenset(PREDEFINED_ADJACENCY["cross"])

        fixed_missing = set(missing or ())
        required_set = set(required or ())
        all_vertices = list(range(1, N_max + 1))

        subsets = connected_subsets(adjacency, max_multiplicity)
        subset_keys = [tuple(sorted(s)) for s in subsets]

        prob = pulp.LpProblem("EachGetsGeo", pulp.LpStatusOptimal)

        a = pulp.LpVariable.dicts(
            "a", (all_vertices, subset_keys), lowBound=0, upBound=1, cat=pulp.LpBinary
        )

        y: dict[int, pulp.LpVariable] | None = None
        if auto_missing:
            y = pulp.LpVariable.dicts(
                "y", all_vertices, lowBound=0, upBound=1, cat=pulp.LpBinary
            )
            for v in required_set:
                prob += y[v] == 0, f"required_{v}"
            if missing_count is not None:
                prob += pulp.lpSum(y[v] for v in all_vertices) == missing_count, "missing_count"
            if missing_sum is not None:
                prob += pulp.lpSum(v * y[v] for v in all_vertices) == missing_sum, "missing_sum"

        x: dict[int, dict[int, pulp.LpVariable | pulp.LpAffineExpression]] = {}
        for v in all_vertices:
            x[v] = {}
            if not auto_missing and v in fixed_missing:
                for s in subsets:
                    skey = tuple(sorted(s))
                    prob += a[v][skey] == 0, f"fixed_missing_{v}_{skey}"
            for c in range(5):
                relevant = [tuple(sorted(s)) for s in subsets if c in s]
                if auto_missing:
                    x[v][c] = pulp.lpSum(a[v][s] for s in relevant)
                    prob += x[v][c] <= (1 - y[v]) * max_multiplicity, f"x_missing_{v}_{c}"
                else:
                    if v in fixed_missing:
                        x[v][c] = pulp.LpVariable(f"x_{v}_{c}", lowBound=0, upBound=0, cat=pulp.LpBinary)
                    else:
                        x[v][c] = pulp.lpSum(a[v][s] for s in relevant)

        # Each vertex assigned to exactly one connected subset
        for v in all_vertices:
            if auto_missing:
                prob += (
                    pulp.lpSum(a[v][tuple(sorted(s))] for s in subsets) == 1 - y[v],
                    f"assign_{v}",
                )
            else:
                if v in fixed_missing:
                    prob += pulp.lpSum(a[v][tuple(sorted(s))] for s in subsets) == 0, f"assign_{v}"
                else:
                    prob += pulp.lpSum(a[v][tuple(sorted(s))] for s in subsets) == 1, f"assign_{v}"

        # Cluster size and sum
        for c in range(5):
            prob += pulp.lpSum(x[v][c] for v in all_vertices) == n, f"size_{c}"
            prob += pulp.lpSum(v * x[v][c] for v in all_vertices) == S, f"sum_{c}"
        # Heuristic: enforce smallest vertex (1) to be in cluster 0 if not missing
        if 1 not in fixed_missing and (not auto_missing or (auto_missing and 1 not in required_set)):
            prob += x[1][0] == 1, "heuristic_vertex1_cluster0"
        # Multiplicity bounds
        for v in all_vertices:
            prob += pulp.lpSum(x[v][c] for c in range(5)) <= max_multiplicity, f"max_mult_{v}"
            if auto_missing:
                prob += pulp.lpSum(x[v][c] for c in range(5)) >= 1 - y[v], f"min_mult_{v}"
            else:
                if v not in fixed_missing:
                    prob += pulp.lpSum(x[v][c] for c in range(5)) >= 1, f"min_mult_{v}"

        # Duplicated amount
        if auto_missing:
            prob += (
                pulp.lpSum(
                    (pulp.lpSum(x[v][c] for c in range(5)) - (1 - y[v])) * v
                    for v in all_vertices
                )
                == 5 * S - pulp.lpSum(v * (1 - y[v]) for v in all_vertices),
                "duplicated_amount",
            )
        else:
            present_vertices = [v for v in all_vertices if v not in fixed_missing]
            T = sum(present_vertices)
            D = 5 * S - T
            if D < 0:
                print(f"[Error] S={S} is too small. 5S={5*S} < T={T}", file=sys.stderr)
                return None
            prob += (
                pulp.lpSum(
                    (pulp.lpSum(x[v][c] for c in range(5)) - 1) * v
                    for v in present_vertices
                )
                == D,
                "duplicated_amount",
            )

        # mod 5 residue balance
        if residue_balance:
            for r in range(1, 6):
                if r == 5:
                    verts_r_all = [v for v in all_vertices if v % 5 == 0]
                else:
                    verts_r_all = [v for v in all_vertices if v % 5 == r]
                total_r = len(verts_r_all)
                lb = max(0, total_r // 5 - residue_slack)
                ub = (total_r + 4) // 5 + residue_slack
                for c in range(5):
                    count_r = pulp.lpSum(x[v][c] for v in verts_r_all)
                    prob += count_r >= lb, f"res_lb_{c}_{r}"
                    prob += count_r <= ub, f"res_ub_{c}_{r}"

        # Pair shared counts
        if pair_shared_counts:
            for (i, j), target in pair_shared_counts.items():
                skey = tuple(sorted({i, j}))
                # sum over v of a[v][skey] plus subsets that contain both i and j
                shared_expr = pulp.lpSum(
                    a[v][tuple(sorted(s))]
                    for v in all_vertices
                    for s in subsets
                    if i in s and j in s
                )
                prob += shared_expr == target, f"pair_shared_{i}_{j}"

        # Symmetry (residue counts)
        if symmetry in ("ud", "both"):
            # cluster 1 (up) and 3 (down) have same residue counts
            for r in range(1, 6):
                verts_r = [v for v in all_vertices if (v % 5 if v % 5 != 0 else 5) == r]
                prob += (
                    pulp.lpSum(x[v][1] for v in verts_r)
                    == pulp.lpSum(x[v][3] for v in verts_r),
                    f"sym_ud_{r}",
                )
        if symmetry in ("lr", "both"):
            for r in range(1, 6):
                verts_r = [v for v in all_vertices if (v % 5 if v % 5 != 0 else 5) == r]
                prob += (
                    pulp.lpSum(x[v][2] for v in verts_r)
                    == pulp.lpSum(x[v][4] for v in verts_r),
                    f"sym_lr_{r}",
                )

        # Forbid previous solutions
        if forbid_solutions:
            for idx, sol in enumerate(forbid_solutions):
                # Forbid same assignment: at least one vertex must differ
                expr = 0
                for c, cluster in enumerate(sol.clusters):
                    for v in cluster:
                        if v not in fixed_missing and (not auto_missing or True):
                            expr += 1 - x[v][c]
                    for v in range(1, N_max + 1):
                        if v not in cluster and v not in fixed_missing:
                            expr += x[v][c]
                # Simplified: sum of differences >= 1
                prob += expr >= 1, f"forbid_{idx}"

        prob += 0  # feasible

        solver = self._make_solver(time_limit)
        prob.solve(solver)

        if pulp.LpStatus[prob.status] != "Optimal":
            return None

        missing_result: set[int] = set()
        if auto_missing:
            for v in all_vertices:
                if int(pulp.value(y[v]) or 0) == 1:
                    missing_result.add(v)
        else:
            missing_result = fixed_missing

        present_vertices = [v for v in all_vertices if v not in missing_result]
        clusters: list[list[int]] = [[] for _ in range(5)]
        multiplicity: dict[str, int] = {}
        for v in present_vertices:
            m = sum(int(pulp.value(x[v][c]) or 0) for c in range(5))
            multiplicity[str(v)] = m
            for c in range(5):
                if int(pulp.value(x[v][c]) or 0) == 1:
                    clusters[c].append(v)

        shared = tuple(v for v, m in multiplicity.items() if m >= 2)
        shared_ints = tuple(int(v) for v in shared)

        return EachGetsSolution(
            n=n,
            N_max=N_max,
            S=S,
            clusters=tuple(tuple(sorted(c)) for c in clusters),
            multiplicity=multiplicity,
            shared_vertices=shared_ints,
            missing=tuple(sorted(missing_result)),
            adjacency=sorted([sorted(e) for e in adjacency]),
        )

    def solve_all(
        self,
        n: int,
        N_max: int,
        S: int,
        max_solutions: int,
        **kwargs,
    ) -> list[EachGetsSolution]:
        """Enumerate multiple solutions."""
        solutions: list[EachGetsSolution] = []
        for _ in range(max_solutions):
            sol = self.solve(
                n=n,
                N_max=N_max,
                S=S,
                forbid_solutions=solutions,
                **kwargs,
            )
            if sol is None:
                break
            solutions.append(sol)
        return solutions


# ============================================================
# 3. Visualization
# ============================================================

def visualize_solution(sol: EachGetsSolution, output_path: str | None = None) -> None:
    """Visualize a solution with matplotlib."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("[Error] matplotlib is not installed.", file=sys.stderr)
        return

    adjacency_set = {tuple(sorted(e)) for e in sol.adjacency}

    # Choose layout according to adjacency graph
    if adjacency_set == {(0, 1), (0, 2), (0, 3), (0, 4)}:
        _draw_cross(sol, output_path)
    elif adjacency_set == {(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (3, 4)}:
        _draw_honeycomb(sol, output_path)
    else:
        _draw_generic(sol, output_path)


def _draw_cross(sol: EachGetsSolution, output_path: str | None) -> None:
    import matplotlib.pyplot as plt
    positions = {
        0: (0, 0),
        1: (0, 2),
        2: (2, 0),
        3: (0, -2),
        4: (-2, 0),
    }
    _draw_layout(sol, positions, output_path)


def _draw_honeycomb(sol: EachGetsSolution, output_path: str | None) -> None:
    import matplotlib.pyplot as plt
    # Central hexagon + 4 directional hexagons
    positions = {
        0: (0, 0),
        1: (-1.5, 1.5),
        2: (1.5, 1.5),
        3: (-1.5, -1.5),
        4: (1.5, -1.5),
    }
    _draw_layout(sol, positions, output_path)


def _draw_generic(sol: EachGetsSolution, output_path: str | None) -> None:
    import matplotlib.pyplot as plt
    import numpy as np
    # Circular layout
    angles = [i * 2 * 3.14159 / 5 for i in range(5)]
    positions = {i: (np.cos(a), np.sin(a)) for i, a in enumerate(angles)}
    _draw_layout(sol, positions, output_path)


def _draw_layout(
    sol: EachGetsSolution,
    positions: dict[int, tuple[float, float]],
    output_path: str | None,
) -> None:
    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax = plt.subplots(figsize=(12, 10))

    # Cluster centers
    centers = {c: np.array(pos) for c, pos in positions.items()}

    # Vertex positions: arranged in a circle around each cluster center
    vertex_pos: dict[int, tuple[float, float]] = {}
    for c, cluster in enumerate(sol.clusters):
        cx, cy = centers[c]
        m = len(cluster)
        for idx, v in enumerate(sorted(cluster)):
            angle = idx * 2 * np.pi / m - np.pi / 2
            r = 0.7
            vx = cx + r * np.cos(angle)
            vy = cy + r * np.sin(angle)
            # Shared vertices: slightly adjust if already placed elsewhere
            if v in vertex_pos:
                # average with existing position
                ox, oy = vertex_pos[v]
                vertex_pos[v] = ((ox + vx) / 2, (oy + vy) / 2)
            else:
                vertex_pos[v] = (vx, vy)

    # Edges between adjacent clusters
    for (i, j) in sol.adjacency:
        x_vals = [centers[i][0], centers[j][0]]
        y_vals = [centers[i][1], centers[j][1]]
        ax.plot(x_vals, y_vals, "k-", linewidth=2, alpha=0.3)

    # Draw vertices
    shared_set = set(sol.shared_vertices)
    for v, (vx, vy) in vertex_pos.items():
        color = "#FF6B6B" if v in shared_set else "#4ECDC4"
        size = 300 if v in shared_set else 200
        ax.scatter(vx, vy, s=size, c=color, edgecolors="black", zorder=3)
        ax.text(vx, vy, str(v), ha="center", va="center", fontsize=9, fontweight="bold", zorder=4)

    # Cluster labels
    names = ["Center", "Up", "Right", "Down", "Left"]
    for c, (cx, cy) in centers.items():
        ax.text(cx, cy + 1.1, f"C{c}({names[c]})\nS={sol.S}", ha="center", va="center", fontsize=10)

    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"N={sol.n}, N_max={sol.N_max}, S={sol.S}\nShared vertices: {sorted(shared_set)}", fontsize=14)

    if output_path:
        plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor="white")
        print(f"[Visualization saved] {output_path}")
    else:
        plt.show()
    plt.close()


# ============================================================
# 4. Known family parameters
# ============================================================

def known_families() -> list[dict]:
    return [
        {
            "name": "Five-each-gets (Heaven-Water Five-Use Diagram)",
            "n": 5,
            "N_max": 24,
            "S": 65,
            "missing": [3, 10, 22],
            "max_multiplicity": 2,
            "adjacency": "cross",
            "residue_balance": True,
        },
        {
            "name": "Six-each-gets (Jisu-Yong-Yukdo)",
            "n": 6,
            "N_max": 20,
            "S": 63,
            "missing": [],
            "max_multiplicity": 3,
            "adjacency": "honeycomb",
            "residue_balance": True,
            "pair_shared_counts": "0-1:2,0-2:2,0-3:2,0-4:2,1-2:2,3-4:2",
        },
        {
            "name": "Seven-each-gets",
            "n": 7,
            "N_max": 35,
            "S": 120,
            "auto_missing": True,
            "missing_count": 4,
            "missing_sum": 95,
            "required": [1, 2, 3, 4, 5],
            "max_multiplicity": 2,
            "adjacency": "cross",
            "residue_balance": True,
        },
        {
            "name": "Eight-each-gets",
            "n": 8,
            "N_max": 40,
            "S": 164,
            "missing": [],
            "max_multiplicity": 2,
            "adjacency": "grid",
            "residue_balance": True,
        },
        {
            "name": "Nine-each-gets",
            "n": 9,
            "N_max": 45,
            "S": 207,
            "missing": [],
            "max_multiplicity": 2,
            "adjacency": "grid",
            "residue_balance": True,
        },
    ]


# ============================================================
# 5. CLI
# ============================================================

def main() -> int:
    parser = argparse.ArgumentParser(description="N-Each-Gets MILP Solver (geometry, phase, visualization)")
    parser.add_argument("--n", type=int, help="Number of vertices per subset")
    parser.add_argument("--max", dest="N_max", type=int, help="Maximum number value to use")
    parser.add_argument("--sum", dest="S", type=int, help="Target sum for each subset")
    parser.add_argument("--adjacency", default="cross", help="cross/honeycomb/grid or custom")
    parser.add_argument("--missing", type=int, nargs="*", default=[])
    parser.add_argument("--auto-missing", action="store_true")
    parser.add_argument("--missing-count", type=int, default=None)
    parser.add_argument("--missing-sum", type=int, default=None)
    parser.add_argument("--required", type=int, nargs="*", default=[])
    parser.add_argument("--max-multiplicity", type=int, default=2)
    parser.add_argument("--residue-balance", action="store_true")
    parser.add_argument("--residue-slack", type=int, default=1)
    parser.add_argument(
        "--pair-shared-counts",
        type=str,
        default=None,
        help="Shared vertex counts per adjacent pair, e.g. '0-1:2,0-2:2'",
    )
    parser.add_argument(
        "--symmetry",
        choices=["ud", "lr", "both"],
        default=None,
        help="Up/down / left/right residue symmetry",
    )
    parser.add_argument("--search", action="store_true", help="Automatic S search")
    parser.add_argument("--all", action="store_true", help="Solve all five known families")
    parser.add_argument("--max-solutions", type=int, default=1, help="Maximum number of solutions to find")
    parser.add_argument("--output", type=str, default=None, help="JSON save path")
    parser.add_argument("--visualize", action="store_true", help="Run visualization")
    parser.add_argument("--viz-prefix", type=str, default="viz", help="Visualization file prefix")
    parser.add_argument("--time-limit", type=int, default=60)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    solver = EachGetsSolver(verbose=1 if args.verbose else 0)

    if args.all:
        all_solutions: list[EachGetsSolution] = []
        for fam in known_families():
            print("=" * 70)
            print(f"[Solving] {fam['name']} (n={fam['n']}, S={fam['S']})")
            adj = get_adjacency(fam.get("adjacency", "cross"))
            psc_str = fam.get("pair_shared_counts")
            psc = parse_pair_shared_counts(psc_str) if psc_str else None

            sols = solver.solve_all(
                n=fam["n"],
                N_max=fam["N_max"],
                S=fam["S"],
                max_solutions=args.max_solutions,
                adjacency=adj,
                missing=fam.get("missing"),
                auto_missing=fam.get("auto_missing", False),
                missing_count=fam.get("missing_count"),
                missing_sum=fam.get("missing_sum"),
                required=fam.get("required"),
                max_multiplicity=fam["max_multiplicity"],
                residue_balance=fam.get("residue_balance", False),
                pair_shared_counts=psc,
                symmetry=fam.get("symmetry"),
                time_limit=args.time_limit,
            )
            if sols:
                for idx, sol in enumerate(sols, 1):
                    print(f"\n[Solution {idx}/{len(sols)}]")
                    print(sol)
                    all_solutions.append(sol)
                    if args.visualize:
                        viz_path = f"{args.viz_prefix}_{fam['name'].split('(')[0]}_{idx}.png"
                        visualize_solution(sol, viz_path)
            else:
                print("  -> No solution found.")

        if args.output:
            data = [sol.to_dict() for sol in all_solutions]
            Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"\n[JSON saved] {args.output} ({len(data)} solutions)")
        return 0

    if args.n is None or args.N_max is None:
        print("[Error] --n and --max are required. (except when using --all)", file=sys.stderr)
        return 1

    if args.S is None and not args.search:
        print("[Error] Specify --sum or use --search.", file=sys.stderr)
        return 1

    adj = get_adjacency(args.adjacency)
    psc = parse_pair_shared_counts(args.pair_shared_counts) if args.pair_shared_counts else None

    if args.search and args.S is None:
        sol = solver.search_s(
            n=args.n,
            N_max=args.N_max,
            adjacency=adj,
            missing=args.missing or None,
            auto_missing=args.auto_missing,
            missing_count=args.missing_count,
            missing_sum=args.missing_sum,
            required=args.required or None,
            max_multiplicity=args.max_multiplicity,
            residue_balance=args.residue_balance,
            pair_shared_counts=psc,
            symmetry=args.symmetry,
            time_limit=args.time_limit,
        )
        sols = [sol] if sol else []
    else:
        sols = solver.solve_all(
            n=args.n,
            N_max=args.N_max,
            S=args.S,
            max_solutions=args.max_solutions,
            adjacency=adj,
            missing=args.missing or None,
            auto_missing=args.auto_missing,
            missing_count=args.missing_count,
            missing_sum=args.missing_sum,
            required=args.required or None,
            max_multiplicity=args.max_multiplicity,
            residue_balance=args.residue_balance,
            residue_slack=args.residue_slack,
            pair_shared_counts=psc,
            symmetry=args.symmetry,
            time_limit=args.time_limit,
        )

    if not sols or sols[0] is None:
        print("No solution found.")
        return 1

    for idx, sol in enumerate(sols, 1):
        print(f"\n[Solution {idx}/{len(sols)}]")
        print(sol)
        if args.visualize:
            viz_path = f"{args.viz_prefix}_solution_{idx}.png"
            visualize_solution(sol, viz_path)

    if args.output:
        data = [sol.to_dict() for sol in sols]
        Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n[JSON saved] {args.output} ({len(data)} solutions)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
