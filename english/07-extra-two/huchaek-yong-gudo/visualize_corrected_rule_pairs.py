#!/usr/bin/env python3
"""Visualize pair-sum classes in the corrected Huchaek-yong-gudo arrangement."""

from __future__ import annotations

from huchaek_data import CORRECTED_FORMATIONS
from visualize_huchaek_rule_pairs import draw


def main() -> None:
    draw(CORRECTED_FORMATIONS, "huchaek_rule_pairs_corrected", " (corrected)")


if __name__ == "__main__":
    main()
