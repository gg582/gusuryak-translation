# yukgodo2 — Consecutive Ring-Value Reconstruction (六包一/逓加 family)

An independent mini-repo for another plausible reconstruction of the Nakseo Yukgodo. It is a separate candidate from the antipodal-complement reconstruction of the parent project (`../yukgodo`).

## Hypothesis

Arithmetic structure directly supported by the text:

- 逓加 ring sizes 6k (k = 1..9), 6×(1+…+9) = 270
- 來積法 chain: 54+6=60, 60÷6=10, 2×10−1=19, (10+18)×9=252, 252+19=271
- 虛一: the center left void, 270 occupied cells
- 六包一 series (Gyowusa edition of the 九數略, Kun vol., p. 11): 1+(6+12+…+54) = 271

Reconstruction hypothesis for the values:

- place values 1..270 each exactly once
- ring k receives the consecutive interval 3k(k−1)+1 … 3k(k+1) (ring 1: 1..6, …, ring 9: 217..270)
- within each ring, values proceed consecutively around the circumference

The starting point and direction of each ring are a normalization of rotational symmetry, not a manuscript claim. Ring sums under this hypothesis are 18k³+3k, unlike the 813k of the antipodal-complement hypothesis.

## Run

```bash
python3 solver.py   # writes solution.json, report.md, reconstruction.png to output/
```

## Results

See [output/report.md](output/report.md). The arithmetic chain is Z3-verified as consistent, and the placement satisfies all checks: 271 cells, values 1..270 each once, exact ring intervals, exact ring sums.
