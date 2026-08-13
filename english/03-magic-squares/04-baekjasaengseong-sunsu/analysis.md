# Baekjasaengseong-sunsu (Hundred-Numbers Pure-Generation Diagram, 百子生成純數圖)

Order: 10×10

## Transcription and classification

Sunsu-do is an **ordered-pair** grid. Split a two-digit entry into its digits,
write `10` as `(0,10)`, and write a one-digit entry such as `7` as `(0,7)`.
A two-digit entry ending in `0` has second component `10`, hence `90=(9,10)`.
It must not be collapsed into a decimal array and tested as a normal 1–100
magic square.

## Component structure

- The first component is a Latin square on `0`–`9`; the second is a Latin
  square on `1`–`10`.
- The superposition has 50 distinct ordered pairs, each occurring twice. Thus
  Sunsu-do is an **order-ten 50-orthogonal Latin-square pair**.
- Under a 180-degree rotation, every ordered pair maps to an identical pair at
  its antipodal position. The 100 cells partition into 50 antipodal pairs,
  each holding the same ordered pair.

Sunsu-do therefore shares Gyosu-do’s ordered-pair and 50-orthogonal structure,
while additionally possessing this rotational symmetry. It is not a magic
square defined by sums of decimal cell values.
