# Conservative Reconstruction Policy: Hado 5-Coloring Puzzle

---

## 1. Purpose

This document describes a Python script and visualization that strictly follow the reconstruction policy of the Problem Constraints and the five mod-5 residue groups of Saodo (Hado) defined in `사오도와-칠자각득의-일반화`.

Only data explicitly present in the source is preserved; inferred structures are kept separate.

---

## 2. Source Data

### 2.1 Geometry

The 20 circular slots are fixed in the following symmetric cross-shaped layout:

```
        19  2
        7  14
13  8   5   16  4   17
18  3   11  10  12   9
        15  1
        6  20
```

- Top arm: 2×2
- Central trunk: 2×6
- Bottom arm: 2×2

Slot positions are immutable.

### 2.2 Labels

Each slot contains exactly one Arabic numeral. The label set is `{1, 2, …, 20}` and every numeral appears exactly once.

### 2.3 Numeral Orientation

Every numeral in the source is intentionally slanted. The script preserves the observed slant as data, currently using `-30°` uniformly.

### 2.4 Residue Groups

The numerals are partitioned by `group(n) = ((n - 1) mod 5) + 1`.

| Group | Name | Elements |
|---|---|---|
| 1 | Water | {1, 6, 11, 16} |
| 2 | Fire | {2, 7, 12, 17} |
| 3 | Wood | {3, 8, 13, 18} |
| 4 | Metal | {4, 9, 14, 19} |
| 5 | Earth | {5, 10, 15, 20} |

### 2.5 Checksum

The manuscript note "共積210" is interpreted as:

```
sum(1..20) = 210
```

---

## 3. Reconstruction Policy

### 3.1 Preserved

- Slot positions of the 20 circular slots
- Circular marks
- Numeral values
- Numeral orientations
- Symmetric cross-shaped layout
- Residue-group partition
- Checksum note (共積210)

### 3.2 Not Introduced

The following are not part of the source and are therefore not introduced in this reconstruction:

- Artificial graph edges
- Nearest-neighbor assumptions
- Rewrite systems
- Finite-state machines
- Traversal rules
- Algebraic semantics

---

## 4. Visualization

Run `figures/reconstruct_source.py` to generate `figures/puzzle_reconstruction.png`:

```bash
python3 figures/reconstruct_source.py
```

The generated image includes:

- 20 circular slots
- Slanted numeral labels
- Group-colored circular borders
- The 共積210 checksum
- Dashed outlines of the symmetric cross layout (visual aid only)
- A legend and a policy note

---

## 5. Script Structure

- `SLOTS`: list of 20 slots with position, label, and orientation
- `RESIDUE_GROUPS`: explicit definition of the five residue groups
- `group_of(label)`: computes `((label - 1) mod 5) + 1`
- `checksum(labels)`: sum of labels
- `draw_reconstruction(...)`: matplotlib-based visualization

The script performs consistency checks at runtime:

- Exactly 20 slots
- Labels are `{1, …, 20}` used exactly once
- Total sum equals 210
- Each residue group contains exactly four labels

---

## 6. Generated Files

| File | Description |
|---|---|
| `figures/reconstruct_source.py` | Conservative reconstruction script |
| `figures/puzzle_reconstruction.png` | Generated visualization |
| `docs/reconstruction_policy.ko.md` | Korean version of this document |
| `docs/reconstruction_policy.en.md` | This document |
