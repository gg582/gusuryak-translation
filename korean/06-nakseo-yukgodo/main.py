#!/usr/bin/env python3
"""洛書六觚圖 복원 파이프라인: 탐색 → 저장 → 시각화 → 성질 분석.

사용 예:
    python3 main.py                          # 기본 탐색 (8회 재시작)
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
    ap = argparse.ArgumentParser(description="洛書六觚圖 복원 최적해 탐색")
    ap.add_argument("--iterations", type=int, default=150_000,
                    help="재시작당 담금질 반복 수")
    ap.add_argument("--restarts", type=int, default=8, help="재시작 횟수")
    ap.add_argument("--seed", type=int, default=1715, help="난수 시드")
    ap.add_argument("--outdir", default="output", help="산출물 디렉터리")
    ap.add_argument("--color-by", choices=["ring", "wedge"], default="ring")
    ap.add_argument("--render-only", action="store_true",
                    help="기존 solution.json으로 그림·리포트만 재생성")
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
        print(f"=== 洛書六觚圖 렌더링 (저장된 해, 페널티 {penalty}) ===")
    else:
        print("=== 洛書六觚圖 복원 탐색 ===")
        print(f"격자: 271칸(虛一 → 270칸), 외주 54칸, 한 변 10칸")
        print(f"탐색: 재시작 {args.restarts}회 × 반복 {args.iterations:,}회, 시드 {args.seed}")
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
        print(f"\n소요 시간: {elapsed:.1f}s")
        print(f"재시작별 페널티: {restart_pens}")
    print(f"최종 페널티: {penalty} (이론적 하한 {PENALTY_FLOOR})")
    print(f"  구성: {report.parts}")
    print(f"변 합:   {report.side_sums}  (목표 1355)")
    print(f"섹터 합: {report.wedge_sums}  (목표 6097/6098)")
    print(f"광선 합: {report.ray_sums}  (목표 1219/1220)")
    print(f"꼭짓점:  {report.corner_values}")
    if errors:
        print("\n[경고] 기본 조건 위반:", errors)
    else:
        print("\n기본 조건(270칸, 1..270, 외주 54) 검증 통과")

    # 해 저장
    if not args.render_only:
        with open(sol_path, "w", encoding="utf-8") as f:
            json.dump({
                "meta": {"seed": args.seed, "iterations": args.iterations,
                         "restarts": args.restarts,
                         "restart_penalties": restart_pens,
                         "penalty": penalty, "elapsed_sec": elapsed},
                "values": {f"{q},{r}": v for (q, r), v in values.items()},
            }, f, ensure_ascii=False, indent=1)
        print(f"\n해 저장: {sol_path}")

    # 시각화
    fig_png = os.path.join(args.outdir, "nakseo_yukgodo.png")
    fig_svg = os.path.join(args.outdir, "nakseo_yukgodo.svg")
    draw_figure(values, grid, fig_png, fig_svg, color_by=args.color_by,
                title=f"洛書六觚圖 — 복원 최적해 (페널티 {penalty})")
    dash_png = os.path.join(args.outdir, "dashboard.png")
    draw_dashboard(report, grid, dash_png)
    print(f"도안: {fig_png}, {fig_svg}")
    print(f"대시보드: {dash_png}")

    # 성질 분석
    analysis = build_analysis(values, grid, report, PENALTY_FLOOR)
    analysis_path = os.path.join(args.outdir, "analysis.json")
    write_json(analysis, analysis_path)
    report_md = os.path.join(args.outdir, "report.md")
    write_markdown(analysis, report, report_md, {
        "seed": args.seed, "iterations": args.iterations,
        "restarts": args.restarts,
        "restart_penalties": restart_pens,
    })
    print(f"분석: {analysis_path}, {report_md}")

    # Siamese식 지역 규칙 역산 검토
    siamese = analyze_siamese(values, grid)
    siamese_json = os.path.join(args.outdir, "siamese_analysis.json")
    siamese_md = os.path.join(args.outdir, "siamese_report.md")
    write_siamese_json(siamese, siamese_json)
    write_siamese_markdown(siamese, siamese_md)
    print(f"Siamese 검토: {siamese_json}, {siamese_md}")

    # 생성 규칙 역산 및 주석 대조
    from yukgodo.reverse import build_reverse_analysis, write_reverse_json, write_reverse_markdown
    reverse = build_reverse_analysis(values, grid)
    reverse_json = os.path.join(args.outdir, "reverse_engineering.json")
    reverse_md = os.path.join(args.outdir, "reverse_engineering.md")
    write_reverse_json(reverse, reverse_json)
    write_reverse_markdown(reverse, reverse_md)
    print(f"생성 규칙 역산: {reverse_json}, {reverse_md}")

    # mod 5 잔여류 채색 및 5층 기하 관계 전수조사
    from yukgodo.mod5 import (analyze_mod5, draw_mod5_coloring, draw_mod5_layers,
                              draw_mod5_symmetry, write_mod5_json, write_mod5_markdown)
    mod5 = analyze_mod5(values, grid)
    draw_mod5_coloring(values, grid,
                       os.path.join(args.outdir, "mod5_coloring.png"),
                       os.path.join(args.outdir, "mod5_coloring.svg"))
    draw_mod5_layers(values, mod5["classes"], mod5["class_sums"], grid,
                     os.path.join(args.outdir, "mod5_layers.png"))
    draw_mod5_symmetry(values, mod5["classes"], grid,
                       os.path.join(args.outdir, "mod5_symmetry.png"))
    write_mod5_json(mod5, os.path.join(args.outdir, "mod5_analysis.json"))
    write_mod5_markdown(mod5, os.path.join(args.outdir, "mod5_report.md"))
    print(f"mod 5 분석: {os.path.join(args.outdir, 'mod5_analysis.json')}, "
          f"{os.path.join(args.outdir, 'mod5_report.md')}")


if __name__ == "__main__":
    main()
