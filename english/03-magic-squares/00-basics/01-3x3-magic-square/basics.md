# 3×3 Magic Square Basics (三階縱橫圖)

```
4 9 2
3 5 7
8 1 6
```

> 從衡十五 一九爲十 三七爲十 二八爲十 四六爲十.

- Rows and columns all sum to 15 (*縱橫十五*).
- 1 + 9 = 10
- 3 + 7 = 10
- 2 + 8 = 10
- 4 + 6 = 10

—-

一六共宗  
1 and 6 share the same origin (*共宗*).

二七同道  
2 and 7 share the same path (*同道*).

三八爲朋  
3 and 8 are companion numbers (*爲朋*).

四九成友  
4 and 9 are also companion numbers (*成友*).

洛書之中亦有河圖之數焉  
Why is this found both in the Nakseo (Lo Shu) and in the Hado (Yellow River Map)?

## Explanation

Numbers grouped by residue modulo 5:

- x ≡ 1 (mod 5): {1, 6, 11, ...}
- x ≡ 2 (mod 5): {2, 7, 12, ...}
- x ≡ 3 (mod 5): {3, 8, 13, ...}
- x ≡ 4 (mod 5): {4, 9, 14, ...}
- x ≡ 0 (mod 5): {5, 10, 15, ...} (not stated explicitly in the text, but implied)

Because the central number is 5, this magic square places the divisible-by-5 number at the center.

Let the five groups be G0, G1, G2, G3, and G4. Then the square is arranged as:

```
G4 G4 G2
G3 G0 G2
G3 G1 G1
```

- G0 contains 1 number.
- G1 contains 2 numbers.
- G2 contains 2 numbers.
- G3 contains 2 numbers.
- G4 contains 2 numbers.

In total the groups contain 9 numbers.

## Superposition of Two Magic Squares

```
(4,4) (1,9) (2,2)
(7,3) (5,5) (3,7)
(8,8) (9,1) (6,6)
```

九子斜排 左右上更  
The nine numbers are first placed diagonally; then the left and right columns are swapped (*左右上更*).

上下對易 四維單出  
Then the top and bottom are exchanged (*上下對易*); the four corner numbers each appear once.

Although it looks disorderly at first glance, a clear rule operates inside.

This unique superposition matrix is not a random listing of number pairs. It is a device that visualizes, on a single plane, the geometric movement process (dynamic transition) by which the diagonally placed numbers return to their proper positions.

—-

## Superposition of Two Magic Squares

```
(4,4) (1,9) (2,2)
(7,3) (5,5) (3,7)
(8,8) (9,1) (6,6)
```

If we split this superposition matrix into left and right components, the following regularity emerges.

### 1. Left-component magic square (transitional state)

```
4 1 2
7 5 3
8 9 6
```

This is the intermediate stage after only the left-right swap (*左右上更*) has been applied to the initial diagonal placement of the nine numbers (*九子斜排*). The top and bottom numbers (1 and 9) have not yet been exchanged and remain in their original positions (1 in the first row, 9 in the third row).

### 2. Right-component magic square (final Nakseo magic square)

```
4 9 2
3 5 7
8 1 6
```

After the final top-bottom exchange (*上下對易*) of 1 and 9, the square converges to a normal magic square in which every row, column, and diagonal sums to 15.
