## Yukyukdo (Six-Six Board, 六六圖)

```
13 22 18 27 11 20
31  4 36  9 29  2
12 21 14 23 16 25
30  3  5 32 34  7
17 26 10 19 15 24
 8 35 28  1  6 33
```

```
 4 13 36 27 29  2
22 31 18  9 11 20
 3 21 23 32 25  7
30 12  5 14 16 34
17 26 19 28  6 15
35  8 10  1 24 33
```

## Gusudo (Nine Palace, 九數圖)

```
31 76 13 36 81 18 29 74 11
22 40 58 27 45 63 20 38 56
67  4 49 72  9 54 65  2 47
30 75 12 32 77 14 34 79 16
21 39 57 23 41 59 25 43 61
66  3 48 68  5 50 70  7 52
35 80 17 28 73 10 33 78 15
26 44 62 19 37 55 24 42 60
71  8 53 64  1 46 69  6 51
```

```
50 18 55 70  5 48  3 76 44
66 31 26 29 81 13 52 11 60
 7 74 42 24 37 62 68 36 19
54 67  2 65 25 33 28 23 72
59 21 43  9 41 73 15 61 47
10 35 78 49 57 17 80 39  4
79  6 38 20 69 34 32 64 27
30 71 22 45  1 77 16 51 56
14 46 63 58 53 12 75  8 40
```

## Order-ten Baekja (Hundred-Numbers, 百子) diagrams

These are the 10×10 Baekja-family diagrams recorded in transcriptions of
*Gusuryak*. The source arrays are retained as transcriptions and analysed as
such; they are not silently normalized to fit a magic-square condition. The
separately documented Baekjado rearrangement is a normal semi-magic square:
all rows and columns sum to 505, while its main diagonals sum to 490 and 520.

### Baekjayin-yang-chakjong: child and mother Latin squares

```
10  9  8  7  6  5  4  3  2  1
 1 10  9  8  7  6  5  4  3  2
 2  1 10  9  8  7  6  5  4  3
 3  2  1 10  9  8  7  6  5  4
 4  3  2  1 10  9  8  7  6  5
 5  4  3  2  1 10  9  8  7  6
 6  5  4  3  2  1 10  9  8  7
 7  6  5  4  3  2  1 10  9  8
 8  7  6  5  4  3  2  1 10  9
 9  8  7  6  5  4  3  2  1 10
```

```
0 1 2 3 4 5 6 7 8 9
9 0 1 2 3 4 5 6 7 8
8 9 0 1 2 3 4 5 6 7
7 8 9 0 1 2 3 4 5 6
6 7 8 9 0 1 2 3 4 5
5 6 7 8 9 0 1 2 3 4
4 5 6 7 8 9 0 1 2 3
3 4 5 6 7 8 9 0 1 2
2 3 4 5 6 7 8 9 0 1
1 2 3 4 5 6 7 8 9 0
```

### Baekjasaengseong-sunsu (Hundred-Numbers Pure-Generation Diagram, 百子生成純數圖)

```
(9,10) (8,9) (7,8) (6,7) (5,6) (4,5) (3,4) (2,3) (1,2) (0,1)
(8,6) (7,10) (6,9) (5,8) (9,7) (0,4) (4,3) (3,2) (2,1) (1,5)
(7,7) (6,6) (5,10) (9,9) (8,8) (1,3) (0,2) (4,1) (3,5) (2,4)
(6,8) (5,7) (9,6) (8,10) (7,9) (2,2) (1,1) (0,5) (4,4) (3,3)
(5,9) (9,8) (8,7) (7,6) (6,10) (3,1) (2,5) (1,4) (0,3) (4,2)
(4,2) (0,3) (1,4) (2,5) (3,1) (6,10) (7,6) (8,7) (9,8) (5,9)
(3,3) (4,4) (0,5) (1,1) (2,2) (7,9) (8,10) (9,6) (5,7) (6,8)
(2,4) (3,5) (4,1) (0,2) (1,3) (8,8) (9,9) (5,10) (6,6) (7,7)
(1,5) (2,1) (3,2) (4,3) (0,4) (9,7) (5,8) (6,9) (7,10) (8,6)
(0,1) (1,2) (2,3) (3,4) (4,5) (5,6) (6,7) (7,8) (8,9) (9,10)
```

Sunsu-do is also read as an **ordered-pair** grid. Split a two-digit entry into
its digits, write `10` as `(0,10)`, and write a one-digit entry such as `7` as
`(0,7)`. A two-digit entry ending in `0` has second component `10`, so `90`
means `(9,10)`, while the terminal `1` means `(0,1)`.
It must not be collapsed into a decimal array for magic-square or point-symmetry
tests.

Both components are Latin squares of order ten. Their superposition contains
50 ordered pairs, each twice, so Sunsu-do is a **50-orthogonal Latin-square
pair**. Its additional feature is 180-degree rotational symmetry: every pair
recurs at its antipodal position. The 100 cells therefore form 50 antipodal
position-pairs, each occupied by one repeated ordered pair.

### Baekjasaengseong-gyosu (Hundred-Numbers Crossed-Numbers Diagram, 百子生成交數圖)

```
 (0,10) (1,9) (2,8) (3,7) (4,6) (5,5) (6,4) (7,3) (8,2) (9,1)
 (1,6) (2,0) (3,9) (4,8) (0,7) (9,4) (5,3) (6,2) (7,1) (8,5)
 (2,7) (3,6) (4,0) (0,9) (1,8) (8,3) (9,2) (5,1) (6,5) (7,4)
 (3,8) (4,7) (0,6) (0,10) (2,9) (7,2) (8,1) (9,5) (5,4) (6,3)
 (5,9) (0,8) (1,7) (2,6) (3,0) (6,1) (7,5) (8,4) (9,3) (5,2)
 (4,2) (9,3) (8,4) (7,5) (6,1) (3,0) (2,6) (1,7) (0,8) (4,9)
 (6,3) (5,4) (9,5) (8,1) (7,2) (2,9) (0,10) (0,6) (4,7) (3,8)
 (7,4) (6,5) (5,1) (9,2) (8,3) (1,8) (0,9) (4,0) (3,6) (2,7)
 (8,5) (7,1) (6,2) (5,3) (9,4) (0,7) (4,8) (3,9) (2,0) (1,6)
 (9,1) (8,2) (7,3) (6,4) (5,5) (4,6) (3,7) (2,8) (1,9) (0,10)
```

The source records ordered pairs, not decimal integers formed by concatenating their components. It is a 50-orthogonal superposition of two order-ten Latin squares, in which 50 ordered pairs each occur twice. The earlier numerical “corrections” (`16→11`, `85→86`, and symmetry-based substitutions) therefore do not apply. This diagram is a pair-grid, not a magic square.

### Baekjayin-yang-jamo-chakjong (Hundred-Numbers Yin-Yang Mother-Child Intertwining Diagram, 百子陰陽子母錯綜圖)

```
100 89 78 67 56 45 34 23 12  1
 29 28 47 36 10 91 65 54 73 72
 48 17 26 40 39 62 61 75 84 53
 27 46 50  9 88 13 92 51 55 74
 76 80 59 98 87 14  3 32 21 25
 15 31 42 43  4 97 58 69 70 86
 24 35 41  2 83 18 99 60 66 77
 93 94 85 71 52 49 30 16  7  8
 82 63 64 95 81 20  6 37 38 19
 11 22 33 44  5 96 57 68 79 90
```

### Baekjado (Hundred-Numbers Diagram, 百子圖)

#### Source array

```
 1 20 21 40 41 60 61 80 81 100
99 82 79 62 59 42 39 22 19  2
 3 18 23 38 43 58 63 78 83 98
97 84 77 64 57 44 37 24 17  4
 5 16 25 36 45 56 65 76 85 96
95 86 75 66 55 46 35 26 15  6
14  7 34 27 54 47 74 67 94 87
88 93 68 73 48 53 28 33  8 13
12  9 32 29 52 49 72 69 92 89
91 90 71 70 51 50 31 30 11 10
```

#### Alternative rearrangement

```
 1 20 21 40 41 60 61 80 81 100
99 82 79 62 59 42 39 22 19   2
 3 18 23 38 43 58 63 78 83  98
97 84 77 64 57 44 37 24 17   4
96 86 75 66 55 46 35 26 15   5
 6 16 25 36 45 56 65 76 85  95
87  7 34 27 54 47 74 67 94  14
13 93 68 73 48 53 28 33  8  88
12  9 32 29 52 49 72 69 92  89
91 90 71 70 51 50 31 30 11  10
```

The alternative rearrangement uses every number from 1 through 100 exactly once, and
every row and column sums to 505. Its main diagonals sum to 490 and 520, so it
is not a complete magic square.

| Coordinates (row, column) | Source values | Rearranged values |
| --- | ---: | ---: |
| (5, 1), (5, 2), (5, 3) | 5, 16, 25 | 96, 86, 75 |
| (5, 8), (5, 9) | 76, 85 | 26, 15 |
| (6, 1), (6, 2), (6, 3) | 95, 86, 75 | 6, 16, 25 |
| (6, 8), (6, 9) | 26, 15 | 76, 85 |
| (7, 1), (7, 10) | 14, 87 | 87, 14 |
| (8, 1), (8, 10) | 88, 13 | 13, 88 |

## Source-transcription analysis and the Baekjado rearrangement

The blocks of the five diagrams above are source transcriptions retained for
comparison with the *Gusuryak* material. Their analyses describe the readings
as supplied; only Baekjado has a separately documented rearrangement:

- [Baekjajasuyin-yang-chakjong analysis](03-baekjajasuyin-yang-chakjong/analysis.md)
- [Baekjasaengseong-sunsu analysis](04-baekjasaengseong-sunsu/analysis.md)
- [Baekjasaengseong-gyosu analysis](05-baekjasaengseong-gyosu/analysis.md)
- [Baekjayin-yang-jamo-chakjong analysis](06-baekjayin-yang-jamo-chakjong/analysis.md)

Sunsu-do and Gyosu-do are order-ten 50-orthogonal Latin-square pairs recorded
as ordered pairs, not magic-square verification targets. The child and mother diagrams
are likewise separate Latin-square bases in the source rather than a single
composed source diagram. The alternative Baekjado arrangement shown above is
a semi-magic square, with only its row and column sums equal to 505.

## References

- Kim Sung-sook, Kang Mi-kyung, "Choi Seok-jeong's Orthogonal Latin Squares," *Journal of the Korean Society for the History of Mathematics*, Vol. 23, No. 3 (2010), 21-31. [ScienceON full text](https://scienceon.kisti.re.kr/commons/util/originalView.do?cn=JAKO201033538926931&oCn=JAKO201033538926931&dbt=JAKO&journal=294661)
