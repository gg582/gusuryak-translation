#!/usr/bin/env python3
"""
Compare Saodo and Chiljagakdeuk within the general framework Π(p, q, T).

Run:
    python3 compare_structures.py
"""

from collections import defaultdict


# ---- Saodo (Hado) data --------------------------------------------------
SAODO_LABELS = {
    "water": [1, 6, 11, 16],
    "fire": [2, 7, 12, 17],
    "wood": [3, 8, 13, 18],
    "metal": [4, 9, 14, 19],
    "earth": [5, 10, 15, 20],
}

# ---- Chiljagakdeuk data -------------------------------------------------
CHILJA_CLUSTERS = {
    "top":    {"center": 2,  "periphery": [29, 1, 24, 34, 11, 19]},
    "left":   {"center": 3,  "periphery": [6, 33, 23, 13, 34, 8]},
    "center": {"center": 5,  "periphery": [22, 7, 20, 30, 26, 10]},
    "right":  {"center": 4,  "periphery": [15, 28, 9, 18, 32, 14]},
    "bottom": {"center": 1,  "periphery": [35, 16, 21, 24, 6, 17]},
}


def residue(value):
    return ((value - 1) % 5) + 1


def check_chiljagakdeuk_rule():
    print("=== Chiljagakdeuk rule check ===")
    centers = [data["center"] for data in CHILJA_CLUSTERS.values()]
    print(f"Number of directions: {len(CHILJA_CLUSTERS)}")
    print(f"Centers: {sorted(centers)}")
    print(f"Centers form complete residue system mod 5: {sorted(residue(c) for c in centers) == [1,2,3,4,5]}")

    sums = []
    for direction, data in CHILJA_CLUSTERS.items():
        total = data["center"] + sum(data["periphery"])
        q = len(data["periphery"])
        sums.append(total)
        print(f"  {direction}: center={data['center']}, |periphery|={q}, sum={total}")

    print(f"All cluster sums equal: {len(set(sums)) == 1}, T={sums[0] if len(set(sums))==1 else None}")
    print(f"All |periphery| = 6: {all(len(d['periphery'])==6 for d in CHILJA_CLUSTERS.values())}")
    print()


def check_saodo_against_rule():
    print("=== Saodo mapped as clusters (smallest element as center) ===")
    sums = []
    for name, values in SAODO_LABELS.items():
        center = min(values)
        periphery = [v for v in values if v != center]
        total = sum(values)
        sums.append(total)
        print(f"  {name}: center={center}, |periphery|={len(periphery)}, sum={total}")

    centers = [min(v) for v in SAODO_LABELS.values()]
    print(f"Centers: {sorted(centers)}")
    print(f"Centers form complete residue system mod 5: {sorted(residue(c) for c in centers) == [1,2,3,4,5]}")
    print(f"All |periphery| = 6: {all(len(v)-1 == 6 for v in SAODO_LABELS.values())}")
    print(f"All cluster sums equal: {len(set(sums)) == 1}")
    print(f"Per-cluster sums: {sorted(sums)}")
    print()


def compare_parameters():
    print("=== Parameter comparison Π(p, q, T) ===")
    print("Chiljagakdeuk: Π(5, 6, 120)")
    print("Saodo color classes: Π(5, 3, T_d) where T_d varies")
    print()


if __name__ == "__main__":
    check_chiljagakdeuk_rule()
    check_saodo_against_rule()
    compare_parameters()
