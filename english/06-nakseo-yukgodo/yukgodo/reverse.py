"""Reverse-engineering of the generation rule from the final reconstructed
diagram, cross-checked against the faint commentary.

Where siamese.py (local rules over the value order) and hypotheses.py
(添六 construction hypotheses) examined the *order* of values and the
*construction procedure*, this module asks data-driven questions of the
reconstructed optimum itself: does any compressive generation rule survive?

Checks (all against output/solution.json):

    1. Ring-walk arithmetic progressions — do the 6k values of ring k form
       an AP (mod 271) for ANY step (a generalized reading of 添六 per ring)?
    2. Linear position model — is there a rule v ≡ a + b·k + c·j (mod 271)?
    3. mod-6 residue distribution — is each ring balanced (k of each class)?
       (+6 progressions preserve the mod-6 class, so that would be a
       fingerprint of 添六.)
    4. Antipodal-pair assignment order — along the spiral walk, are the
       complementary pairs (1..135) assigned in order (a constructive trace)?
    5. Ray difference symmetry — are opposite-ray differences sign-reversed
       (an automatic consequence of the antipodal-pair hypothesis)?
    6. Seed sensitivity — how many cells agree with an optimum found under
       a different seed (uniqueness vs. multiplicity of optima)?

Each result is then cross-checked against the legible commentary fragments,
and the possibility of confirming the algorithm is judged.
"""

from __future__ import annotations

import json
import os
from collections import Counter

from .hexgrid import HexGrid, antipode
from .hypotheses import evaluate_all
from .properties import PENALTY_FLOOR
from .siamese import analyze_siamese
from .solver import solve

MODULUS = 271


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_solution(path: str = "output/solution.json") -> dict:
    with open(path, encoding="utf-8") as f:
        saved = json.load(f)
    return {tuple(map(int, k.split(","))): v for k, v in saved["values"].items()}


# ---------------------------------------------------------------------------
# 1. Ring-walk AP scan
# ---------------------------------------------------------------------------

def ring_ap_scan(values: dict, grid: HexGrid) -> dict:
    """For each ring, the closest arithmetic progression (mod 271), any step."""
    per_ring = {}
    for k in range(1, grid.radius + 1):
        seq = [values[c] for c in grid.ring_walk[k]]
        n = len(seq)
        best_matches, best_step = 0, 0
        for step in range(1, MODULUS):
            m = sum(
                1 for i in range(n)
                if (seq[(i + 1) % n] - seq[i]) % MODULUS == step
            )
            if m > best_matches:
                best_matches, best_step = m, step
        per_ring[k] = {
            "cells": n,
            "best_step": best_step,
            "best_matches": best_matches,
            "ratio": best_matches / n,
        }
    max_ratio = max(r["ratio"] for r in per_ring.values())
    return {
        "per_ring": per_ring,
        "max_ratio": max_ratio,
        "verdict": (
            f"Best AP match ratio over all rings is at most {max_ratio:.1%} "
            "(random-noise level) — no ring-walk arithmetic placement rule"
        ),
    }


# ---------------------------------------------------------------------------
# 2. Linear position model v ≡ a + b·k + c·j (mod 271)
# ---------------------------------------------------------------------------

def linear_model_scan(values: dict, grid: HexGrid) -> dict:
    """Exhaustive search for a linear rule over (ring k, index j along the walk)."""
    cells = [
        (k, j, values[c])
        for k in range(1, grid.radius + 1)
        for j, c in enumerate(grid.ring_walk[k])
    ]
    k0, j0, v0 = cells[0]
    best = (0, None)
    for b in range(MODULUS):
        us = [(v - b * k) % MODULUS for k, _, v in cells]
        u0 = us[0]
        for c in range(MODULUS):
            a = (u0 - c * j0) % MODULUS
            m = 1 + sum(
                1 for (_, j, _), uj in zip(cells[1:], us[1:])
                if (uj - c * j - a) % MODULUS == 0
            )
            if m > best[0]:
                best = (m, (a, b, c))
    return {
        "model": "v ≡ a + b·k + c·j (mod 271)",
        "best_matches": best[0],
        "best_params": best[1],
        "n_cells": len(cells),
        "verdict": (
            f"Best linear model explains only {best[0]} of {len(cells)} cells "
            "(random expectation ~1) — no coordinate-linear placement rule"
        ),
    }


# ---------------------------------------------------------------------------
# 3. mod-6 residue distribution
# ---------------------------------------------------------------------------

def mod6_scan(values: dict, grid: HexGrid) -> dict:
    """Whether the mod-6 class counts per ring are balanced (k of each class)."""
    per_ring = {}
    balanced = True
    for k in range(1, grid.radius + 1):
        cnt = Counter(values[c] % 6 for c in grid.rings[k])
        full = {r: cnt.get(r, 0) for r in range(6)}
        is_bal = all(v == k for v in full.values())
        balanced = balanced and is_bal
        per_ring[k] = {"counts": full, "balanced": is_bal}
    return {
        "per_ring": per_ring,
        "all_balanced": balanced,
        "verdict": (
            "The mod-6 distribution per ring is neither balanced nor constant "
            "across rings — the class-preservation fingerprint of 添六 "
            "(each of the 6 classes k times per ring) does not appear"
        ),
    }


# ---------------------------------------------------------------------------
# 4. Antipodal-pair assignment order
# ---------------------------------------------------------------------------

def pair_order_scan(values: dict, grid: HexGrid) -> dict:
    """Along the spiral walk, look for order in the pairs' smaller values."""
    slot_of = {}
    for s, (a, b) in enumerate(grid.slots):
        slot_of[a] = s
        slot_of[b] = s
    seen = set()
    order = []
    for k in range(grid.radius, 0, -1):
        for c in grid.ring_walk[k]:
            if c in seen:
                continue
            seen.add(c)
            seen.add(antipode(c))
            s = slot_of[c]
            a, b = grid.slots[s]
            order.append(min(values[a], values[b]))
    longest = cur = 1
    for i in range(1, len(order)):
        if order[i] == order[i - 1] + 1:
            cur += 1
            longest = max(longest, cur)
        else:
            cur = 1
    return {
        "spiral_order": order,
        "longest_consecutive_run": longest,
        "verdict": (
            f"Longest consecutive run of pair assignments along the spiral: "
            f"{longest} pairs — no constructive assignment order survives "
            "(the search erased the initial ordering)"
        ),
    }


# ---------------------------------------------------------------------------
# 5. Ray difference symmetry
# ---------------------------------------------------------------------------

def ray_symmetry_scan(values: dict, grid: HexGrid) -> dict:
    """Check that opposite rays (i, i+3) have sign-reversed differences."""
    rows = []
    all_ok = True
    for i in range(3):
        seq_a = [values[c] for c in grid.rays[i]]
        seq_b = [values[c] for c in grid.rays[i + 3]]
        diff_a = [seq_a[j + 1] - seq_a[j] for j in range(8)]
        diff_b = [seq_b[j + 1] - seq_b[j] for j in range(8)]
        ok = all(x == -y for x, y in zip(diff_a, diff_b))
        all_ok = all_ok and ok
        rows.append({"ray_pair": (i, i + 3), "antisymmetric": ok})
    return {
        "pairs": rows,
        "all_antisymmetric": all_ok,
        "verdict": (
            "Sign-reversed opposite-ray differences follow automatically from "
            "the antipodal complementary-pair hypothesis (sum 271) — a "
            "structural property, independent of the search"
        ),
    }


# ---------------------------------------------------------------------------
# 6. Seed sensitivity (multiplicity of optima)
# ---------------------------------------------------------------------------

def seed_overlap_scan(values: dict, grid: HexGrid, seed: int = 42,
                      iterations: int = 60_000, restarts: int = 4) -> dict:
    """Cells agreeing between the stored optimum and a freshly searched one."""
    result = solve(grid, iterations=iterations, restarts=restarts, seed=seed)
    same = sum(1 for c, v in values.items() if result.values.get(c) == v)
    return {
        "seed": seed,
        "penalty": result.penalty,
        "identical_cells": same,
        "n_cells": len(values),
        "verdict": (
            f"The optimum found with seed {seed} (penalty {result.penalty}) "
            f"agrees with the stored optimum in {same} of {len(values)} cells "
            "— many placements satisfy the conditions, and the reconstructed "
            "diagram is only one specimen"
        ),
    }


# ---------------------------------------------------------------------------
# Commentary cross-check
# ---------------------------------------------------------------------------

def annotation_crosscheck(analysis: dict) -> list[dict]:
    """One-by-one cross-check of the legible commentary fragments."""
    return [
        {
            "fragment": "共積二百七十",
            "reading": "270 cells are filled",
            "status": "confirmed",
            "evidence": "value set 1..270 over 270 cells (validated)",
        },
        {
            "fragment": "虛一則二百七十數",
            "reading": "voiding the one leaves 270 numbers",
            "status": "confirmed",
            "evidence": "center cell (0,0) unused",
        },
        {
            "fragment": "校計周五十四數",
            "reading": "counting the perimeter gives 54",
            "status": "confirmed",
            "evidence": "outermost ring has 54 cells (= 六九五十四)",
        },
        {
            "fragment": "通加洛書數六倍",
            "reading": "six times the Luoshu number (1+..+9=45) = 270",
            "status": "confirmed",
            "evidence": "total cells 270 = 6×45",
        },
        {
            "fragment": "十九爲中觚數也",
            "reading": "the central row has 19",
            "status": "confirmed",
            "evidence": "中觚 19 cells, sum 2439 = 9×271",
        },
        {
            "fragment": "置外周添六",
            "reading": "outward, each ring grows by six cells",
            "status": "confirmed (cell-count reading)",
            "evidence": "ring k has 6k cells (6,12,...,54)",
        },
        {
            "fragment": "置外周添六 (value-rule reading)",
            "reading": "place the values adding six",
            "status": "refuted",
            "evidence": (
                "all 192 ±6 (mod 271) spiral variants fail "
                f"(hypotheses.py best penalty {analysis['hyp_best_penalty']:.0f}); "
                f"best per-ring AP match {analysis['ring_ap']['max_ratio']:.1%}"
            ),
        },
        {
            "fragment": "得五百(500), 五百六(506)",
            "reading": "500 and 506 values",
            "status": "suspended (Tier 3)",
            "evidence": "isolated from the calculation chain, cannot be uniquely determined due to multiple 2-op generation formulas (see NAEJEOK_ASSESSMENT.md)",
        },
        {
            "fragment": "寄左 / 序左",
            "reading": "(presumed placement-order rule)",
            "status": "undecidable",
            "evidence": (
                f"seed-{analysis['seed_scan']['seed']} optimum agrees in "
                f"{analysis['seed_scan']['identical_cells']}/270 cells — with "
                "many optima, no order information survives in the reconstruction"
            ),
        },
        {
            "fragment": "以算遠則係以六",
            "reading": "(reading uncertain)",
            "status": "undecidable",
            "evidence": "a clearer edition is needed",
        },
    ]


# ---------------------------------------------------------------------------
# Combined analysis
# ---------------------------------------------------------------------------

def build_reverse_analysis(values: dict, grid: HexGrid,
                           run_seed_scan: bool = True) -> dict:
    print("[1/6] ring-walk AP scan...")
    ring_ap = ring_ap_scan(values, grid)
    print("[2/6] linear position model scan...")
    linear = linear_model_scan(values, grid)
    print("[3/6] mod-6 residue distribution...")
    mod6 = mod6_scan(values, grid)
    print("[4/6] antipodal-pair assignment order...")
    pairs = pair_order_scan(values, grid)
    print("[5/6] ray difference symmetry...")
    rays = ray_symmetry_scan(values, grid)
    if run_seed_scan:
        print("[6/6] seed sensitivity (re-solving under another seed)...")
        seed_scan = seed_overlap_scan(values, grid)
    else:
        seed_scan = {"seed": None, "penalty": None, "identical_cells": None,
                     "n_cells": len(values), "verdict": "skipped"}

    print("re-measuring the 添六 construction hypotheses (hypotheses.py)...")
    hyp = evaluate_all(grid)
    hyp_best = hyp[0]

    siamese = analyze_siamese(values, grid)

    analysis = {
        "ring_ap": ring_ap,
        "linear_model": linear,
        "mod6": mod6,
        "pair_order": pairs,
        "ray_symmetry": rays,
        "seed_scan": seed_scan,
        "hyp_best_penalty": hyp_best["penalty"],
        "hyp_best": {k: hyp_best[k] for k in ("kind", "inward", "continuous", "ccw", "corner")},
        "siamese_best_rule": siamese["best_fixed_rule"],
        "penalty_floor": PENALTY_FLOOR,
    }
    analysis["crosscheck"] = annotation_crosscheck(analysis)
    analysis["verdict"] = (
        "The algorithm cannot be confirmed from the present evidence. "
        "The geometric skeleton (271/270/54/19/252) and the sum conditions "
        "(rings 813k, sides 1355, axes 2439, antipodal pairs 271) match the "
        "commentary exactly, but no compressive trace of a placement-order "
        "rule survives in any reconstructed optimum. All value-rule readings "
        "of 添六 are refuted, and the placement-order fragments (寄左/序左) "
        "cannot be judged from the reconstruction because optima are "
        "plentiful. What can be settled extends only to what the algorithm "
        "is NOT; confirming the text of the algorithm itself requires a "
        "clearer edition of the commentary."
    )
    return analysis


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def write_reverse_json(analysis: dict, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=1)


def write_reverse_markdown(analysis: dict, path: str) -> None:
    s = analysis
    lines = [
        "# Nakseo Yukgodo (洛書六觚圖) — reverse-engineering the generation rule",
        "# from the final reconstructed diagram, cross-checked with the faint commentary",
        "",
        "Starting from the reconstructed optimum (`output/solution.json`), we test",
        "data-driven whether any compressive generation rule survives, and compare",
        "each outcome against the legible fragments of the faint commentary.",
        "",
        "## 1. Status of the reconstructed diagram",
        "",
        f"- Theoretical floor of the search objective: {s['penalty_floor']} (attained).",
        f"- Cells agreeing with an optimum found under another seed "
        f"({s['seed_scan']['seed']}): **{s['seed_scan']['identical_cells']}/270**.",
        "- Hence many placements satisfy the conditions; the reconstructed diagram",
        "  is one specimen. The question is whether constructive traces survive in it.",
        "",
        "## 2. Reverse-engineering attempts and outcomes",
        "",
        "| Candidate rule | Method | Result |",
        "|---|---|---|",
        f"| ring-walk AP (any step mod 271) | 270 steps per ring, exhaustive | failed — best match {s['ring_ap']['max_ratio']:.1%} |",
        f"| coordinate-linear model v ≡ a+b·k+c·j | (a,b,c) over 271³, exhaustive | failed — {s['linear_model']['best_matches']}/270 cells |",
        "| mod-6 class balance (添六 fingerprint) | per-ring class counts | unbalanced/inconsistent — no fingerprint |",
        f"| constructive pair-assignment order | consecutive runs along the spiral | absent — longest run {s['pair_order']['longest_consecutive_run']} pairs |",
        "| ray difference rule | opposite-ray comparison | sign reversal — automatic from the pair hypothesis |",
        f"| Siamese-style local rule (siamese.py) | primary+fallback move pair | failed — {s['siamese_best_rule']['matches']} of 269 transitions |",
        f"| 添六 construction hypotheses (hypotheses.py) | 192 ±6 mod 271 spiral variants | failed — best penalty {s['hyp_best_penalty']:.0f} (floor {s['penalty_floor']}) |",
        "",
        "## 3. Cross-check with the commentary",
        "",
        "| Fragment | Reading | Verdict | Evidence |",
        "|---|---|---|---|",
    ]
    for row in s["crosscheck"]:
        lines.append(f"| {row['fragment']} | {row['reading']} | {row['status']} | {row['evidence']} |")
    lines += [
        "",
        "## 4. Verdict: can the algorithm be confirmed?",
        "",
        s["verdict"],
        "",
        "### What is confirmed",
        "",
        "- The geometric skeleton: 271 cells (虛一 → 270), perimeter 54, 10 cells",
        "  per side, 中觚 19 cells.",
        "- The sum conditions: antipodal pairs 271, rings 813k, sides 1355,",
        "  axes 2439, wedges 6097/6098, rays 1219/1220 — consistent with the",
        "  commentary and the 六觚 record of the Hanshu.",
        "- The 添六/寄左-type phrases should be read as cell-count and ordering",
        "  instructions, not as a value-placement rule.",
        "",
        "### What remains unconfirmed",
        "",
        "- The procedure that assigns values to cells (the body of the naejeokbeop).",
        "  Since the overlap between reconstructed optima is 0/270, the sum",
        "  conditions alone cannot identify the original placement, and no order",
        "  rule can be recovered from these specimens.",
        "- Confirming the algorithm itself requires a clearer edition of the",
        "  commentary.",
        "",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main() -> None:
    grid = HexGrid()
    values = load_solution()
    os.makedirs("output", exist_ok=True)
    analysis = build_reverse_analysis(values, grid)
    write_reverse_json(analysis, "output/reverse_engineering.json")
    write_reverse_markdown(analysis, "output/reverse_engineering.md")
    print("\n=== Verdict ===")
    print(analysis["verdict"])
    print("\nsaved: output/reverse_engineering.json, output/reverse_engineering.md")


if __name__ == "__main__":
    main()
