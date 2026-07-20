#!/usr/bin/env python3
"""Matplotlib font setup for CJK labels in generated figures."""

from __future__ import annotations

from pathlib import Path

import matplotlib
from matplotlib import font_manager


FONT_CANDIDATES = [
    (
        "Noto Sans CJK KR",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ),
    (
        "Noto Sans CJK SC",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ),
    (
        "Noto Sans CJK TC",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ),
    (
        "Noto Sans CJK JP",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ),
    (
        "Droid Sans Fallback",
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
    ),
    (
        "NanumGothic",
        "/usr/share/fonts/naver-nanum-gothic-fonts/NanumGothic.ttf",
    ),
]


def configure_matplotlib_fonts() -> None:
    """Prefer installed CJK fonts so Han characters render without warnings."""
    families: list[str] = []

    for family, font_path in FONT_CANDIDATES:
        path = Path(font_path)
        if not path.exists():
            continue

        try:
            font_manager.fontManager.addfont(str(path))
        except RuntimeError:
            continue

        if family not in families:
            families.append(family)

    families.append("DejaVu Sans")

    matplotlib.rcParams["font.family"] = "sans-serif"
    matplotlib.rcParams["font.sans-serif"] = families
    matplotlib.rcParams["axes.unicode_minus"] = False

    # Keep vector exports portable across viewers.
    matplotlib.rcParams["pdf.fonttype"] = 42
    matplotlib.rcParams["ps.fonttype"] = 42
    matplotlib.rcParams["svg.fonttype"] = "path"
