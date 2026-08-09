"""Render the local aggregate-proxy countermodel on the hexagonal grid."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

from .antipodal_audit import find_countermodel, load_witness
from .hexgrid import HexGrid, antipode, to_pixel
from .properties import measure


def render(output_prefix: Path = Path("output/antipodal_countermodel")) -> tuple[Path, Path]:
    grid = HexGrid()
    witness = load_witness(Path("output/solution.json"), grid)
    countermodel, left, right = find_countermodel(witness, grid)
    report = measure(countermodel, grid)
    changed = {left, right, antipode(left), antipode(right)}
    fig, ax = plt.subplots(figsize=(11, 10), dpi=180)
    fig.patch.set_facecolor("#fffdf8")
    ax.set_facecolor("#fffdf8")
    for cell in grid.cells:
        x, y = to_pixel(cell, size=1.0)
        face, edge = ("#252525", "#252525") if cell == (0, 0) else ("#ffd7d1", "#b42318") if cell in changed else ("#f3eee5", "#b9afa0")
        ax.add_patch(RegularPolygon((x, y), 6, radius=0.56, orientation=0.0, facecolor=face, edgecolor=edge, linewidth=0.6))
    for cell in changed:
        x, y = to_pixel(cell, size=1.0)
        ax.text(x, y, str(countermodel[cell]), ha="center", va="center", fontsize=10, fontweight="bold", color="#7a1810")
    for first in (left, right):
        second = antipode(first)
        x1, y1 = to_pixel(first, size=1.0)
        x2, y2 = to_pixel(second, size=1.0)
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops={"arrowstyle": "<->", "color": "#b42318", "lw": 1.8})
    ax.text(0, 15.5, "Aggregate-proxy countermodel: swap 10 and 124", ha="center", fontsize=15, fontweight="bold")
    ax.text(0, 14.25, "Ring, axis, side, sector, ray balances and per-ring complement closure remain intact.\n"
            "The two red antipodal pairs are 385 and 157: this is not a counterexample to a source rule.",
            ha="center", va="center", fontsize=9.5)
    ax.text(0, -15.2, f"{sum(dev == 0 for dev in report.pair_devs)} of 135 pairs remain 271; the figure only witnesses non-derivability from proxy constraints.", ha="center", fontsize=9, color="#51483d")
    ax.set_aspect("equal")
    ax.set_xlim(-17, 17)
    ax.set_ylim(-16, 17)
    ax.axis("off")
    output_prefix.parent.mkdir(parents=True, exist_ok=True)
    png, svg = output_prefix.with_suffix(".png"), output_prefix.with_suffix(".svg")
    fig.savefig(png, bbox_inches="tight", facecolor=fig.get_facecolor())
    fig.savefig(svg, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return png, svg


if __name__ == "__main__":
    png, svg = render()
    print(f"wrote {png} and {svg}")
