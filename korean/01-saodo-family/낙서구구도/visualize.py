#!/usr/bin/env python3
"""
Recreate the uploaded 3×3 magic-square complex diagram.

Outputs:
  - magic_square_complex_recreated.png
  - magic_square_complex_recreated.svg

Dependencies:
  python3 -m pip install matplotlib
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Circle


@dataclass(frozen=True)
class Cluster:
    center_label: str
    values: tuple[int, int, int, int, int, int, int, int]


CLUSTERS: tuple[tuple[Cluster, ...], ...] = (
    (
        Cluster("八", (17, 35, 56, 26, 65, 46, 42, 74)),
        Cluster("一", (10, 28, 63, 19, 72, 54, 41, 81)),
        Cluster("六", (15, 33, 58, 24, 67, 47, 43, 76)),
    ),
    (
        Cluster("三", (12, 30, 61, 21, 70, 53, 40, 79)),
        Cluster("五", (14, 32, 59, 23, 68, 52, 39, 77)),
        Cluster("七", (16, 34, 57, 25, 66, 51, 38, 75)),
    ),
    (
        Cluster("四", (13, 31, 60, 22, 69, 48, 44, 78)),
        Cluster("九", (18, 36, 55, 27, 64, 50, 37, 73)),
        Cluster("二", (11, 29, 62, 20, 71, 49, 45, 80)),
    ),
)

# Values are ordered clockwise from the upper-left circle:
# upper-left, upper-right, right-upper, right-lower,
# lower-right, lower-left, left-lower, left-upper.
RING_OFFSETS: tuple[tuple[float, float], ...] = (
    (-0.39,  0.96),
    ( 0.39,  0.96),
    ( 0.90,  0.48),
    ( 0.90, -0.28),
    ( 0.39, -0.88),
    (-0.39, -0.88),
    (-0.90, -0.28),
    (-0.90,  0.48),
)

HIGHLIGHT_INDICES = {5, 6}


def choose_cjk_font() -> str:
    preferred = (
        "Noto Serif CJK JP",
        "Noto Sans CJK JP",
        "Noto Serif CJK KR",
        "Noto Sans CJK KR",
        "NanumMyeongjo",
        "NanumGothic",
        "UnBatang",
        "UnDotum",
        "Baekmuk Batang",
        "Baekmuk Dotum",
    )

    installed = {font.name for font in font_manager.fontManager.ttflist}
    for name in preferred:
        if name in installed:
            return name

    return "DejaVu Sans"


def iter_clusters() -> Iterable[tuple[int, int, Cluster]]:
    for row_index, row in enumerate(CLUSTERS):
        for column_index, cluster in enumerate(row):
            yield row_index, column_index, cluster


def draw_cluster(
    ax,
    cluster: Cluster,
    center_x: float,
    center_y: float,
    *,
    ring_radius: float,
    circle_radius: float,
    rough_edges: bool,
    number_font_size: float,
    center_font_size: float,
) -> None:
    for index, ((offset_x, offset_y), value) in enumerate(
        zip(RING_OFFSETS, cluster.values)
    ):
        x = center_x + offset_x * ring_radius
        y = center_y + offset_y * ring_radius

        circle = Circle(
            (x, y),
            radius=circle_radius,
            facecolor="#fff500" if index in HIGHLIGHT_INDICES else "white",
            edgecolor="black",
            linewidth=0.85,
        )

        if rough_edges:
            circle.set_sketch_params(scale=0.7, length=55.0, randomness=1.4)

        ax.add_patch(circle)
        ax.text(
            x,
            y,
            str(value),
            ha="center",
            va="center",
            fontsize=number_font_size,
            color="black",
        )

    ax.text(
        center_x,
        center_y,
        cluster.center_label,
        ha="center",
        va="center",
        fontsize=center_font_size,
        color="black",
    )


def build_figure(
    *,
    width: float,
    height: float,
    dpi: int,
    rough_edges: bool,
):
    font_name = choose_cjk_font()
    plt.rcParams["font.family"] = font_name
    plt.rcParams["axes.unicode_minus"] = False

    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    x_positions = (1.10, 3.65, 6.20)
    y_positions = (6.05, 3.55, 1.05)

    for row_index, column_index, cluster in iter_clusters():
        draw_cluster(
            ax,
            cluster,
            x_positions[column_index],
            y_positions[row_index],
            ring_radius=1.03,
            circle_radius=0.305,
            rough_edges=rough_edges,
            number_font_size=21,
            center_font_size=39,
        )

    ax.set_xlim(-0.18, 7.48)
    ax.set_ylim(-0.20, 7.38)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")

    fig.subplots_adjust(left=0.005, right=0.995, bottom=0.005, top=0.995)
    return fig


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recreate the 3×3 magic-square complex diagram."
    )
    parser.add_argument(
        "--output-prefix",
        default="magic_square_complex_recreated",
        help="Output path prefix without extension.",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=160,
        help="PNG resolution.",
    )
    parser.add_argument(
        "--clean-circles",
        action="store_true",
        help="Use perfectly smooth circle outlines instead of slightly rough outlines.",
    )
    parser.add_argument(
        "--no-svg",
        action="store_true",
        help="Do not write the SVG file.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    prefix = Path(args.output_prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)

    fig = build_figure(
        width=8.85,
        height=8.56,
        dpi=args.dpi,
        rough_edges=not args.clean_circles,
    )

    png_path = prefix.with_suffix(".png")
    fig.savefig(
        png_path,
        dpi=args.dpi,
        facecolor="white",
        bbox_inches=None,
        pad_inches=0,
    )

    if not args.no_svg:
        svg_path = prefix.with_suffix(".svg")
        fig.savefig(
            svg_path,
            facecolor="white",
            bbox_inches=None,
            pad_inches=0,
        )

    plt.close(fig)

    print(f"Wrote {png_path}")
    if not args.no_svg:
        print(f"Wrote {prefix.with_suffix('.svg')}")


if __name__ == "__main__":
    main()
