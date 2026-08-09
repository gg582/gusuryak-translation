#!/usr/bin/env python3
"""Regression check for the common Lo Shu rules cited in the English README."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from yukgodo.nakseo_family_audit import audit  # noqa: E402


def main() -> None:
    result = audit()
    assert result["lo_shu_opposite_sum"] == 10
    assert result["lo_shu_fixed_center"] == 5
    assert result["gugudo_documented_outer_complement_sum"] == 91
    assert result["yukgodo_sixfold_ring_complement_sum"] == 60
    print("Nakseo-family common-rule audit passed")


if __name__ == "__main__":
    main()
