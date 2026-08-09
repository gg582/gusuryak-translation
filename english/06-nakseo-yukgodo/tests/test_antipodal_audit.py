#!/usr/bin/env python3
"""Regression check for the hypothesis-removal antipodal countermodel."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from yukgodo.antipodal_audit import audit  # noqa: E402


def main() -> None:
    result = audit()
    assert result["verdict"] == "not_derived_without_equivariance"
    assert result["pairs_still_summing_271"] < result["pair_count"]
    print("Antipodal hypothesis-removal audit passed")


if __name__ == "__main__":
    main()
