#!/usr/bin/env python3
"""Regression check for the equivariance threshold audit."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from yukgodo.equivariance_threshold_audit import audit  # noqa: E402


def main() -> None:
    result = audit()
    assert result["lo_shu_family_conditions_hold"]
    assert result["compound_non_equivariant_conditions_hold"]
    assert not result["antipodal_complement_forced_without_equivariance"]
    assert result["equivariance_forces_antipodal_complement"]
    assert result["local_transposition_countermodels"] == 504
    print("Equivariance-threshold audit passed")


if __name__ == "__main__":
    main()
