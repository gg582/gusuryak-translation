#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to read saved JSON results and perform post-hoc visualization using matplotlib.

Usage:
  python visualize_json.py auto.json --viz-prefix my_viz
"""

import argparse
import json
import sys
from pathlib import Path
from gakdeuk_solver import GakdeukSolution, visualize_solution


def main() -> int:
    parser = argparse.ArgumentParser(description="Post-hoc visualization tool for saved Gakdeuk puzzle solutions in JSON")
    parser.add_argument("json_file", type=str, help="Path to the JSON file to visualize")
    parser.add_argument("--viz-prefix", type=str, default="viz_post", help="Prefix for the saved visualization files")
    args = parser.parse_args()

    json_path = Path(args.json_file)
    if not json_path.exists():
        print(f"[Error] File does not exist: {args.json_file}", file=sys.stderr)
        return 1

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[Error] Failed to read JSON file: {e}", file=sys.stderr)
        return 1

    if isinstance(data, dict):
        solutions_data = [data]
    elif isinstance(data, list):
        solutions_data = data
    else:
        print("[Error] Invalid JSON format. Must be a dict or a list.", file=sys.stderr)
        return 1

    print(f"[Visualization Start] Processing {len(solutions_data)} solutions.")

    for idx, s_dict in enumerate(solutions_data, 1):
        try:
            sol = GakdeukSolution(
                n=s_dict["n"],
                N_max=s_dict["N_max"],
                S=s_dict["S"],
                clusters=tuple(tuple(c) for c in s_dict["clusters"]),
                multiplicity=s_dict["multiplicity"],
                shared_vertices=tuple(s_dict["shared_vertices"]),
                missing=tuple(s_dict["missing"]),
                adjacency=s_dict["adjacency"],
            )
            output_path = f"{args.viz_prefix}_{idx}.png"
            visualize_solution(sol, output_path)
        except KeyError as e:
            print(f"[Error] Missing key for solution {idx}: {e}", file=sys.stderr)
        except Exception as e:
            print(f"[Error] Exception occurred while visualizing solution {idx}: {e}", file=sys.stderr)

    print("[Complete] Visualization images saved successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
