# Analysis of Nakseo Gugudo

Nakseo Gugudo (낙서구구도) is a 1–81 magic diagram built on the 3×3 central array of the regular Nakseo (Lo Shu) magic square, with eight outer numbers attached to each center value. Each cluster consists of one center number and eight surrounding numbers, and all nine clusters sum to 369.

```text
4 9 2
3 5 7
8 1 6
```

(On the diagram the palaces are placed in the order obtained by flipping the Nakseo array above vertically: 八·一·六 / 三·五·七 / 四·九·二.)

## Total sum and target constant

The sum of the integers from 1 to 81 is:

```text
1 + 2 + ... + 81 = 81 x 82 / 2 = 3321
```

Dividing this into nine equal clusters gives the target sum per cluster:

```text
3321 / 9 = 369
```

Therefore the eight numbers surrounding a center `n` must sum to exactly:

```text
surrounding sum = 369 - n
```

## Transcribing the source diagram and correcting transcription errors

The original diagram has every one of the nine palaces' numbers inscribed correctly. The placement data is a transcription of this diagram from the upper-left palace onward, each palace in the order center number then ring (clockwise from the upper-left cell). During transcription four cells were miscopied, and `reconstruct_milp.py` corrects them back to the original values subject to the constraints (every palace sums to 369, each of 10..81 used exactly once, centers fixed).

| Palace | Transcription error | Value inscribed in the original |
|---|---|---|
| 四 (center 4) | last ring cell dropped during transcription | **47** |
| 三 (center 3) | 19 transcribed as 71 | **19** |
| 七 (center 7) | 31 transcribed as 3 | **31** |
| 六 (center 6) | 30 transcribed as 38 | **30** |

## Verification of the current diagram

| Palace (center) | Ring of 8 | Ring sum | Total |
|---|---|---:|---:|
| 八 (8) | 16, 51, 56, 27, 64, 32, 40, 75 | 361 | 369 |
| 一 (1) | 69, 34, 77, 12, 53, 58, 45, 20 | 368 | 369 |
| 六 (6) | 38, 79, 14, 63, 46, 22, 71, 30 | 363 | 369 |
| 三 (3) | 11, 76, 60, 36, 19, 68, 52, 44 | 366 | 369 |
| 五 (5) | 29, 24, 62, 37, 70, 81, 48, 13 | 364 | 369 |
| 七 (7) | 74, 26, 55, 31, 42, 50, 66, 18 | 362 | 369 |
| 四 (4) | 15, 80, 61, 23, 28, 72, 39, 47 | 365 | 369 |
| 九 (9) | 49, 57, 17, 73, 41, 25, 65, 33 | 360 | 369 |
| 二 (2) | 54, 43, 67, 10, 59, 21, 78, 35 | 367 | 369 |

## The mod-9 transversal structure

The core generation principle of this arrangement is not the 91 complement-pair rule but **mod-9 residue distribution**.

- The eight ring numbers of each palace carry the **eight mod-9 residue classes exactly once each**.
- However, **the residue class of its own center is missing** (because the center number itself represents that class).
- Hence each whole cluster (center + ring) is a complete transversal set carrying the mod-9 residues 0–8 exactly once each.
- Since the residues sum to 0+1+...+8 = 36 ≡ 0 (mod 9), every cluster sum is a multiple of 9, and 369 = 9 × 41 follows naturally.

| Palace (center) | Mod-9 residue missing from the ring |
|---|---:|
| 八 (8) | 8 |
| 一 (1) | 1 |
| 六 (6) | 6 |
| 三 (3) | 3 |
| 五 (5) | 5 |
| 七 (7) | 7 |
| 四 (4) | 4 |
| 九 (9) | 0 |
| 二 (2) | 2 |

The nine numbers belonging to residue class r (mod 9), {r, r+9, ..., r+72}, are spread one per palace across the nine palaces, and in the palace whose center is r only r itself (the center) remains of them.

## Interpretation

Nakseo Gugudo is not merely a diagram whose surrounding sums happen to be equal. It takes the nine numbers of the central Nakseo (Lo Shu) magic square as reference points of the mod-9 residue classes, and arranges the 72 outer numbers as a transversal such that no palace carries its own residue while carrying every other residue exactly once.

```text
each cluster = a complete mod-9 transversal set (9 numbers, residues 0–8 once each)
cluster sum = 369 = 9 x 41
```

The four corrected values above (47, 19, 31, 30) are precisely the values required by this mod-9 transversal rule. In other words, the gakdeuk sum 369 of the original diagram and the mod-9 structure are equivalent constraints, and the MILP reconstruction restores both simultaneously.

## Reproduction scripts

```bash
python3 reconstruct_milp.py       # source transcription -> transcription-error correction (scipy MILP)
python3 analyze_nakseo_gugudo.py  # verifies 369 sums, 1..81, loshu 15, mod-9 transversal structure
python3 visualize.py              # regenerates the diagram image (PNG/SVG)
```
