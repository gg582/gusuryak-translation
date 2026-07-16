#!/usr/bin/env python3
"""Nakseo Yukgodo (洛書六觚圖) reconstruction pipeline: search → save → visualize → analyze.

Usage:
    python3 main.py                          # default search (8 restarts)
    python3 main.py --iterations 300000 --restarts 12
    python3 main.py --seed 42 --outdir output_run2
"""

from __future__ import annotations

import argparse
import json
import os
import time

from yukgodo.analyze import build_analysis, write_json, write_markdown
from yukgodo.hexgrid import HexGrid
from yukgodo.properties import PENALTY_FLOOR, measure, validate
from yukgodo.siamese import analyze_siamese, write_siamese_json, write_siamese_markdown
from yukgodo.solver import solve
from yukgodo.visualize import draw_dashboard, draw_figure


def main() -> None:
    ap = argparse.ArgumentParser(description="Nakseo Yukgodo (洛書六觚圖) reconstruction optimum search")
    ap.add_argument("--iterations", type=int, default=150_000,
                    help="annealing iterations per restart")
    ap.add_argument("--restarts", type=int, default=8, help="number of restarts")
    ap.add_argument("--seed", type=int, default=1715, help="random seed")
    ap.add_argument("--outdir", default="output", help="output directory")
    ap.add_argument("--color-by", choices=["ring", "wedge"], default="ring")
    ap.add_argument("--render-only", action="store_true",
                    help="regenerate figures/report from an existing solution.json")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    grid = HexGrid()
    sol_path = os.path.join(args.outdir, "solution.json")

    if args.render_only:
        with open(sol_path, encoding="utf-8") as f:
            saved = json.load(f)
        values = {tuple(map(int, k.split(","))): v
                  for k, v in saved["values"].items()}
        penalty = saved["meta"]["penalty"]
        restart_pens = saved["meta"].get("restart_penalties", [])
        elapsed = saved["meta"].get("elapsed_sec", 0.0)
        args.seed = saved["meta"].get("seed", args.seed)
        args.iterations = saved["meta"].get("iterations", args.iterations)
        args.restarts = saved["meta"].get("restarts", args.restarts)
        print(f"=== Nakseo Yukgodo (洛書六觚圖) rendering (saved solution, penalty {penalty}) ===")
    else:
        print("=== Nakseo Yukgodo (洛書六觚圖) reconstruction search ===")
        print(f"lattice: 271 cells (虛一 → 270 filled), perimeter 54 cells, 10 cells per side")
        print(f"search: {args.restarts} restarts × {args.iterations:,} iterations, seed {args.seed}")
        t0 = time.time()
        result = solve(grid, iterations=args.iterations,
                       restarts=args.restarts, seed=args.seed)
        elapsed = time.time() - t0
        values = result.values
        penalty = result.penalty
        restart_pens = result.restart_penalties

    errors = validate(values, grid)
    report = measure(values, grid)

    if not args.render_only:
        print(f"\nelapsed: {elapsed:.1f}s")
        print(f"restart penalties: {restart_pens}")
    print(f"final penalty: {penalty} (theoretical floor {PENALTY_FLOOR})")
    print(f"  breakdown: {report.parts}")
    print(f"side sums:   {report.side_sums}  (target 1355)")
    print(f"sector sums: {report.wedge_sums}  (target 6097/6098)")
    print(f"ray sums:    {report.ray_sums}  (target 1219/1220)")
    print(f"corners:     {report.corner_values}")
    if errors:
        print("\n[warning] basic conditions violated:", errors)
    else:
        print("\nbasic conditions (270 cells, 1..270, perimeter 54) validated")

    # save the solution
    if not args.render_only:
        with open(sol_path, "w", encoding="utf-8") as f:
            json.dump({
                "meta": {"seed": args.seed, "iterations": args.iterations,
                         "restarts": args.restarts,
                         "restart_penalties": restart_pens,
                         "penalty": penalty, "elapsed_sec": elapsed},
                "values": {f"{q},{r}": v for (q, r), v in values.items()},
            }, f, ensure_ascii=False, indent=1)
        print(f"\nsolution saved: {sol_path}")

    # visualization
    fig_png = os.path.join(args.outdir, "nakseo_yukgodo.png")
    fig_svg = os.path.join(args.outdir, "nakseo_yukgodo.svg")
    draw_figure(values, grid, fig_png, fig_svg, color_by=args.color_by,
                title=f"Nakseo Yukgodo (洛書六觚圖) — reconstructed optimum (penalty {penalty})")
    dash_png = os.path.join(args.outdir, "dashboard.png")
    draw_dashboard(report, grid, dash_png)
    print(f"diagram: {fig_png}, {fig_svg}")
    print(f"dashboard: {dash_png}")

    # property analysis
    analysis = build_analysis(values, grid, report, PENALTY_FLOOR)
    analysis_path = os.path.join(args.outdir, "analysis.json")
    write_json(analysis, analysis_path)
    report_md = os.path.join(args.outdir, "report.md")
    write_markdown(analysis, report, report_md, {
        "seed": args.seed, "iterations": args.iterations,
        "restarts": args.restarts,
        "restart_penalties": restart_pens,
    })
    print(f"analysis: {analysis_path}, {report_md}")

    # reverse-engineer possible Siamese-style local rules
    siamese = analyze_siamese(values, grid)
    siamese_json = os.path.join(args.outdir, "siamese_analysis.json")
    siamese_md = os.path.join(args.outdir, "siamese_report.md")
    write_siamese_json(siamese, siamese_json)
    write_siamese_markdown(siamese, siamese_md)
    print(f"Siamese check: {siamese_json}, {siamese_md}")


if __name__ == "__main__":
    main()
