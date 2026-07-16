# unified_solver.py
"""Unified solver for each-gets families (Korean version)

This script uses the shared `base_solver.EachGetsSolver` implementation
and iterates over all known families defined in `base_solver.known_families()`.
For each family it solves the MILP, visualizes the solution and stores the
results in a unified JSON file as well as PNG images.

Running:
    python unified_solver.py
"""

import os
import json
from pathlib import Path

# Import the shared solver and utilities
from .base_solver import EachGetsSolver, known_families, visualize_solution


def main():
    output_dir = Path(__file__).parent / "unified_outputs"
    output_dir.mkdir(exist_ok=True)

    all_solutions = []
    for family in known_families():
        solver = EachGetsSolver(
            name=family["name"],
            n=family["n"],
            N_max=family["N_max"],
            S=family["S"],
            missing=family.get("missing", []),
            max_multiplicity=family.get("max_multiplicity", 1),
            adjacency=family.get("adjacency", "cross"),
            residue_balance=family.get("residue_balance", False),
            pair_shared_counts=family.get("pair_shared_counts"),
        )
        print(f"[Unified] Solving {family['name']} …")
        sol = solver.solve()
        all_solutions.append(sol)
        # Save visualization
        img_path = output_dir / f"viz_{family['name'].replace(' ', '_')}.png"
        visualize_solution(sol, str(img_path))
        print(f"[Unified] Saved viz to {img_path}")

    # Serialize all solutions to JSON
    json_path = output_dir / "solutions_unified.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump([s.to_dict() for s in all_solutions], f, ensure_ascii=False, indent=2)
    print(f"[Unified] All solutions written to {json_path}")


if __name__ == "__main__":
    main()
