"""대척보수 감사 반례를 원 격자 위에 시각화한다."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import RegularPolygon

from .antipodal_audit import find_countermodel, load_witness
from .hexgrid import HexGrid, antipode, to_pixel
from .properties import measure


def korean_font() -> FontProperties:
    """Use an installed CJK font so the explanatory labels remain readable."""
    for candidate in (
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
    ):
        if Path(candidate).exists():
            return FontProperties(fname=candidate)
    return FontProperties()


def render(output_prefix: Path = Path("output/antipodal_countermodel")) -> tuple[Path, Path]:
    grid = HexGrid()
    witness = load_witness(Path("output/solution.json"), grid)
    countermodel, left, right = find_countermodel(witness, grid)
    report = measure(countermodel, grid)
    changed = {left, right, antipode(left), antipode(right)}
    font = korean_font()

    fig, ax = plt.subplots(figsize=(11, 10), dpi=180)
    fig.patch.set_facecolor("#fffdf8")
    ax.set_facecolor("#fffdf8")
    for cell in grid.cells:
        x, y = to_pixel(cell, size=1.0)
        if cell == (0, 0):
            face, edge = "#252525", "#252525"
        elif cell in changed:
            face, edge = "#ffd7d1", "#b42318"
        else:
            face, edge = "#f3eee5", "#b9afa0"
        ax.add_patch(RegularPolygon((x, y), 6, radius=0.56, orientation=0.0,
                                    facecolor=face, edgecolor=edge, linewidth=0.6))

    for cell in changed:
        x, y = to_pixel(cell, size=1.0)
        ax.text(x, y, str(countermodel[cell]), ha="center", va="center", fontsize=10,
                fontweight="bold", color="#7a1810")

    for first in (left, right):
        second = antipode(first)
        x1, y1 = to_pixel(first, size=1.0)
        x2, y2 = to_pixel(second, size=1.0)
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops={"arrowstyle": "<->", "color": "#b42318", "lw": 1.8})

    ax.text(0, 15.5, "대리 제약 반례: 값 10과 124를 교환", ha="center", fontsize=16,
            fontweight="bold", fontproperties=font)
    ax.text(0, 14.4,
            "고리·축·변·섹터·광선 균형 및 고리별 보수 폐쇄성은 유지하지만,\n"
            "붉은 두 대척쌍은 각각 385와 157이다. 이는 원문 배정법의 반례가 아니라\n"
            "대리 집계 조건만으로 271을 도출할 수 없다는 증인이다.",
            ha="center", va="center", fontsize=10, fontproperties=font)
    ax.text(0, -15.2,
            f"135쌍 중 {sum(dev == 0 for dev in report.pair_devs)}쌍만 271 유지; "
            "이는 원문 배정 원리의 반증이 아니라, 비대척 복합 조건의 비도출 증인이다.",
            ha="center", fontsize=9, color="#51483d", fontproperties=font)
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
