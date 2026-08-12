# Hetu and Lo Shu in `數原第一`: Evidence for Yukgodo Antipodal Complements

## Source and scope

This document compares passages confirmed in the Gusuryak-Translation Wiki transcription and commentary for `數原苐一` with Yukgodo's placement principle. The quotations follow the transcription supplied by the user. The aim is not to import modern magic-square theory, but to distinguish the internal evidence supplied by the author's own opening account of Hetu and Lo Shu pairing and position.

## 1. Hetu: `併` pairs the extremes into a constant sum

After listing the Heaven and Earth numbers from 1 through 10, the text states:

> 天數一三五七九
>
> 地數二四六八十
>
> 積五十五
>
> 法曰併上下數共一十一
>
> 以位數十乘之得一百一十半之得五十五
>
> 與即四象變數中遍承之法
>
> 化裁五格各得一十一數

The following arrangement makes five pairs:

\[
(10,1),(9,2),(8,3),(7,4),(6,5),
\]

so every pair satisfies

\[
x+(11-x)=11.
\]

The important point is that `併上下數共一十一` is not merely a total-sum calculation. It is a procedure pairing the extreme values so that each of five cells obtains 11 (`化裁五格各得一十一數`). The opening numerical theory of *Gusuryak* therefore already uses **complement pairs as actual computational and constructive units**.

The Heaven/Earth partition by itself does not command an antipodal spatial placement. It is nevertheless a direct arithmetic precedent for the reconstruction principle that pairs `1…270` as `x↔271-x`.

## 2. Lo Shu: direct coupling of positional opposition and value complement

The same exposition gives the Lo Shu arrangement:

\[
\begin{matrix}
4&9&2\\
3&5&7\\
8&1&6
\end{matrix}
\]

Under the 180-degree rotation `\tau` through the center, its four noncentral orbits and central value satisfy

\[
4+6=9+1=2+8=3+7=10,\qquad5\mapsto5.
\]

Thus its 3×3 control layer exactly realizes

\[
v\circ\tau=\kappa_{10}\circ v,
\qquad\kappa_{10}(x)=10-x.
\]

This is more than the observation that complements to 10 exist. **Complementary values occupy opposing positions, while the central 5 is fixed**: a complete positional/value correspondence.

The textual genealogy makes the intended sequence explicit:

> 易大傳曰天一地二天三地四天五地六天七天八天九地十
>
> 此即河圖之數也
>
> 尙書洪範傳曰初一次二次三次四次五次六次七次八次九
>
> 此即洛書之數也
>
> 河圖為體故始於一而終於十
>
> 洛書為用故去其十，止於九數之大原出於次郃

Here Hetu is the `體` of 1…10, while Lo Shu is the `用` of 1…9 after removing 10. Hetu's pairing to 11 and Lo Shu's placement of complements to 10 are therefore adjacent layers of the author's own numerical theory, not unrelated modern readings.

## 3. The exact lift to Yukgodo

Yukgodo is named and described as:

> 洛書六觚圖
>
> 逓加洛書數六倍

Lifting Lo Shu's `k↔10-k` to sixfold ring sizes gives

\[
6k\leftrightarrow6(10-k),\qquad6k+6(10-k)=60.
\]

The handwritten Naejeok Method actually begins by adding the first and last rings:

\[
54+6=60.
\]

Lo Shu's complement sum is therefore genuinely lifted into the Yukgodo ring structure, and its first complementary ring pair is used in the calculation. This makes it difficult to read the title `洛書六觚圖` as merely decorative.

Finally, after `虛一`, Yukgodo's 270 positions split into 135 centrally antipodal pairs, while values `1…270` split into 135 pairs `x↔271-x`:

\[
270=2\times135,
\qquad
\{1,\ldots,270\}=\bigsqcup_{x=1}^{135}\{x,271-x\}.
\]

The minimal lift of the Lo Shu control relation to this value set is

\[
v\circ\tau=\kappa_{271}\circ v,
\qquad\kappa_{271}(x)=271-x.
\]

Once adopted, it necessarily gives `v(c)+v(-c)=271`.

## 4. Revised evidence statement

| Layer | Confirmed content | Weight for Yukgodo |
| --- | --- | --- |
| Hetu arithmetic | `併上下數` and five complement pairs totaling 11 | Direct arithmetic precedent for treating complements as computational/construction units |
| Lo Shu control diagram | Four opposing complement pairs totaling 10, central 5 fixed | Direct coupling of positional opposition and value complement |
| `體`/`用` distinction | Hetu 1…10; Lo Shu 1…9 | Continuous numerical-theoretical context for pairing and Lo Shu control |
| Yukgodo text | `洛書六觚圖`, `逓加洛書數六倍`, `54+6=60` | Actual sixfold lift and use of the Lo Shu complement relation |
| Yukgodo geometry/value set | 135 positional pairs and 135 value pairs | A gapless domain for the equivariant extension |

`v(c)+v(-c)=271` is still not a literally transcribed one-line cell-by-cell command in the Yukgodo passage. But the rule no longer rests only on title, geometry, and value-set compatibility. The author first (a) composes constant sums from complementary values, then (b) places complementary Lo Shu values in opposing positions, and subsequently names and calculates Yukgodo as a sixfold Lo Shu figure. This continuous internal evidence materially strengthens the characterization of the condition as a strong internal antipodal-complement reconstruction principle, not an unsupported hypothesis.

Hetu's complement-to-11 and Lo Shu's complement-to-10 apply to different value sets. They do not logically derive a cell-level 271 placement on their own; the countermodel boundary—that aggregate constraints do not force a positional/value correspondence—remains recorded in [ANTIPODAL_AUDIT.md](ANTIPODAL_AUDIT.md).
