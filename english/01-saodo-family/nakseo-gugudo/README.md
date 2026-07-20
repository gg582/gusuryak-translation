# Analysis of Nakseo Gugudo

Nakseo Gugudo is an expanded magic-square construction using the Lo Shu 3x3 center square and eight surrounding numbers for each center. The construction uses all numbers from 1 to 81. Each of the nine clusters consists of one center number and eight surrounding numbers, and every cluster has the same total: 369.

```text
8 1 6
3 5 7
4 9 2
```

## Total Sum and Magic Constant

The sum of the numbers from 1 to 81 is:

```text
1 + 2 + ... + 81 = 81 x 82 / 2 = 3321
```

Dividing this total into nine equal clusters gives:

```text
3321 / 9 = 369
```

Therefore, if the center number is `n`, the eight surrounding numbers must sum to:

```text
surrounding sum = 369 - n
```

The larger the center number is, the smaller the surrounding sum must be. The smaller the center number is, the larger the surrounding sum must be.

## 91 Complement Pairs

The surrounding numbers are 10 through 81. These 72 numbers can be divided into 36 complement pairs whose sums are 91.

```text
10 + 81 = 91
11 + 80 = 91
12 + 79 = 91
...
45 + 46 = 91
```

If every center used four ordinary 91-pairs, the eight surrounding numbers would always sum to:

```text
91 x 4 = 364
```

Then the cluster total would be `364 + n`, so only the cluster with center 5 would total 369. Nakseo Gugudo solves this imbalance by keeping three of the four pairs as 91-pairs and adjusting the remaining pair according to the center number.

## Center-Correction Pair

Three 91-pairs contribute:

```text
91 x 3 = 273
```

To make the cluster total 369, the remaining pair must have this sum:

```text
correction-pair sum = 369 - n - 273 = 96 - n
```

Thus the correction-pair sums run once each from 87 to 95.

| center | correction-pair sum |
|---:|---:|
| 9 | 87 |
| 8 | 88 |
| 7 | 89 |
| 6 | 90 |
| 5 | 91 |
| 4 | 92 |
| 3 | 93 |
| 2 | 94 |
| 1 | 95 |

This table is the core of the construction. The different center values are exactly cancelled by the different correction-pair sums, so all nine clusters total 369.

## Verification of the Current Diagram

The arrangement encoded in `visualize.py` verifies as follows.

| center | correction pair | correction sum | surrounding sum | total |
|---:|---:|---:|---:|---:|
| 8 | 46 + 42 | 88 | 361 | 369 |
| 1 | 54 + 41 | 95 | 368 | 369 |
| 6 | 47 + 43 | 90 | 363 | 369 |
| 3 | 53 + 40 | 93 | 366 | 369 |
| 5 | 52 + 39 | 91 | 364 | 369 |
| 7 | 51 + 38 | 89 | 362 | 369 |
| 4 | 48 + 44 | 92 | 365 | 369 |
| 9 | 50 + 37 | 87 | 360 | 369 |
| 2 | 49 + 45 | 94 | 367 | 369 |

Each cluster contains one correction pair and three ordinary 91 complement pairs. For example, the center-8 cluster is:

```text
17 + 74 = 91
35 + 56 = 91
26 + 65 = 91
46 + 42 = 88

8 + 91 + 91 + 91 + 88 = 369
```

The center-1 cluster is:

```text
10 + 81 = 91
28 + 63 = 91
19 + 72 = 91
54 + 41 = 95

1 + 91 + 91 + 91 + 95 = 369
```

## Generation Formula

In the current arrangement, the three ordinary 91 complement pairs for a center value `n` follow this form:

```text
(n + 9)  + (82 - n) = 91
(n + 27) + (64 - n) = 91
(n + 18) + (73 - n) = 91
```

The remaining pair is placed so that its sum is `96 - n`. These correction pairs assign the sums 87, 88, ..., 95 exactly once across centers 9 through 1.

## Interpretation

Nakseo Gugudo is not merely a diagram whose octagonal surrounding sums happen to match. Because the Lo Shu center numbers are different, one pair in each surrounding octagon is designed to compensate for the center value.

In short:

```text
each center cluster = three 91 complement pairs + one center-correction pair
correction-pair sum = 96 - center
center + eight surrounding numbers = 369
```

Nakseo Gugudo is therefore an expanded Lo Shu magic square that partitions all numbers from 1 to 81 into nine clusters of 369. Its construction is explained by combining 91 complement pairs with the correction-pair sequence 87 through 95.

## Reproducible Script

`analyze_nakseo_gugudo.py` verifies the structure from data.

```bash
python3 analyze_nakseo_gugudo.py
```

The script checks:

- whether 1 through 81 are used exactly once
- whether every center cluster totals 369
- whether every cluster has three 91 complement pairs and one `96 - center` correction pair
- whether the Lo Shu center square has row, column, and diagonal sums of 15
