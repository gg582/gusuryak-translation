#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
오자각득(천수용오도) 배치 2 — mod 5 잉여 클래스 도식.

mod5_residue_diagram.py의 draw()를 재사용하되, 배치 2(1~21)의
POSITIONS/GROUPS로 교체하여 _2 접미사 파일로 저장한다.
"""

from pathlib import Path

import mod5_residue_diagram as base

POSITIONS = {
    12: (0.0, 6.0),

    17: (-1.5, 5.0),
    18: (1.5, 5.0),

    5:  (0.0, 4.2),

    13: (-2.8, 3.3),
    2:  (0.0, 3.3),
    19: (2.8, 3.3),

    7:  (-4.2, 2.0),
    3:  (-2.8, 2.0),
    20: (-1.4, 2.0),
    15: (0.0, 2.0),
    9:  (1.4, 2.0),
    4:  (2.8, 2.0),
    8:  (4.2, 2.0),

    11: (-2.8, 0.8),
    6:  (0.0, 0.8),
    14: (2.8, 0.8),

    10: (-1.8, -0.4),
    1:  (0.0, -0.4),
    21: (1.8, -0.4),

    16: (0.0, -1.7),
}

GROUPS = {
    1: [1, 6, 11, 16, 21],
    2: [2, 7, 12, 17],
    3: [3, 8, 13, 18],
    4: [4, 9, 14, 19],
    0: [5, 10, 15, 20],
}

# 오행별로 시각적으로 구분되는 색상 (기본 STYLE의 수/금 회색 중복 문제 해소)
STYLE = {
    1: {
        "name": "G1 · n mod 5 ≡ 1",
        "face": "#CFE2F5",
        "edge": "#4488CC",
        "text": "#1F4E79",
    },
    2: {
        "name": "G2 · n mod 5 ≡ 2",
        "face": "#F4D0D0",
        "edge": "#CC4444",
        "text": "#7A2020",
    },
    3: {
        "name": "G3 · n mod 5 ≡ 3",
        "face": "#D4ECD4",
        "edge": "#44AA44",
        "text": "#1E5B1E",
    },
    4: {
        "name": "G4 · n mod 5 ≡ 4",
        "face": "#E8E8E8",
        "edge": "#888888",
        "text": "#222222",
    },
    0: {
        "name": "G5 · n mod 5 ≡ 0",
        "face": "#F6E5A3",
        "edge": "#CC9944",
        "text": "#735700",
    },
}


if __name__ == "__main__":
    import os

    os.chdir(Path(__file__).parent)
    base.POSITIONS = POSITIONS
    base.GROUPS = GROUPS
    base.STYLE = STYLE
    base.draw(
        png_output="mod5_residue_diagram_2.png",
        svg_output="mod5_residue_diagram_2.svg",
    )
    print("[저장] mod5_residue_diagram_2.png / mod5_residue_diagram_2.svg")
