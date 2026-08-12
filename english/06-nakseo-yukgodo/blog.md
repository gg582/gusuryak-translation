# Choe Seok-jeong, Joseon's Algorithmic Wizard, and His 270-Cell Giant Magic Hexagon: Reconstructing the Nakseo Yukgodo (洛書六觚圖)

Did you know that, more than 300 years ago, a Korean mathematician left the world's first study of magic squares in book form? This is the story of *Gusuryak* (九數略), the mathematical work of Choe Seok-jeong (崔錫鼎, 1646–1715), a Joseon-era Chief State Councillor and Silhak scholar.

Among its diagrams, the imposing **Nakseo Yukgodo** (洛書六觚圖) is a particularly large geometric construction. Its structure is being explored through modern computational search and mathematical symmetry analysis. This article introduces, for developers and general readers interested in computation, how algorithms can help illuminate this giant hexagonal magic grid from the historical record.

---

## 1. Before We Begin: A Glossary of Mathematical and Traditional Terms

Before turning to the reconstruction, here are the mathematical and classical terms used throughout this article.

* **Magic square and magic graph**: An arrangement of distinct numbers in cells such that the sums on designated lines—horizontal, vertical, diagonal, and so on—are equal. Extending this idea beyond square grids to shapes such as hexagons or circles is broadly called a magic graph or *mado* (魔圖).
* **Nakseo Yukgodo (洛書六觚圖)**: A hexagonal numerical arrangement recorded in *Gusuryak* (九數略). Its grid is a regular hexagon with ten cells on each side.
* **Heoil (虛一, “leaving one empty”)**: A traditional mathematical expression meaning that one is left vacant. The geometrical central cell—the origin—is not assigned a value, a choice that allows the global sum and symmetry conditions to be satisfied.
* **Complementary antipodal pairs**: A pairing in which the numbers in two cells at point-symmetric positions about the centre always add to a fixed complementary sum \(S\). In the Nakseo Yukgodo, that sum is \(271\).
* **Naejeok method (來積法)**: This is not the modern vector dot product. The classical term, written with the characters for “come” (來) and “accumulate” (積), denotes an algorithmic calculation used to derive and check geometrical dimensions such as the number of cells (area/volume) and the length of the central axes (*junggo*).
* **Junggo (中觚)**: The three central axes crossing the hexagonal grid—one horizontal and two diagonal. Each has length 19 cells.
* **Modulo congruence**: Two integers \(a\) and \(b\) are congruent modulo a natural number \(m\) when they have the same remainder after division by \(m\), written \(a \equiv b \pmod m\). In this reconstruction, it is used for “mod 5 colouring,” which colours the grid by the residues \(0\) through \(4\) of the assigned values.
* **Positional involution**: An operation \(\pi\) that returns to the original position when applied twice, \(\pi^2 = id\). Here it denotes a \(180^\circ\) point-symmetry rotation of the grid.
* **The dihedral group \(D_6\)**: The group containing every geometric symmetry of a regular hexagon: six rotations and six reflections.

---

## 2. The Geometric Structure and Conditions of the Nakseo Yukgodo

The Nakseo Yukgodo is a large regular hexagonal grid with ten cells on each side.

[Insert `nakseo_yukgodo.png` here]

Its mathematical rules help explain why Choe Seok-jeong called this diagram “Nakseo” (洛書, *Luoshu*).

1. **Total number of cells**: The rings surrounding the central cell increase by six cells each time they expand outward (\(6 \times k\) cells). A side length of ten requires nine rings, giving \(1 + (6 + 12 + \dots + 54) = 271\) cells in total.
2. **The heoil condition**: The central cell is left empty by the *heoil* (虛一) method. Thus **270 cells** must be filled, with each of the natural numbers from \(1\) through \(270\) used exactly once.
3. **The Luoshu number and ring sums (逓加洛書數六倍)**: In traditional mathematics, the Luoshu number (洛書數) is \(45\), the sum of \(1\) through \(9\). Six times \(45\), or **270**, is precisely the number of cells to be filled. Their total is \(1+2+\dots+270 = 36{,}585\). The values in the \(k\)-th ring must also be distributed so that their sum is exactly **\(813 \times k\)**.
4. **Outer perimeter (外周)**: The outermost ring has 54 cells. The sum of the numbers on each of the six outside sides of the hexagon must be **1355**.
5. **The three axes and junggo (中觚)**: Each of the three axes passing through the centre, with 19 cells per axis, must sum to **2439**.

---

## 3. Deciphering the Faint 300-Year-Old Commentary on the Naejeok Method (來積法)

The project began with documentary research. The commentary on the *Naejeok method* (來積法) in the original *Gusuryak* is so poorly preserved in scans that it is extremely difficult to read by eye.

[Insert `original_comments_reconstructed_by_genai.png` here]

The researchers used generative AI and image-analysis techniques to reconstruct characters from a rough black-and-white image, then reviewed the entire chain of numerical calculations using the reconstructed transcription in [ALGO_OCR_SUCCESS.md](ALGO_OCR_SUCCESS.md).

The result was a reconstruction of the precise calculation graph concealed in the blurred annotations. The calculation flow, verified by the `naejeok.py` module, is as follows:

```
[Outer perimeter 54] --(add 6)--> [60] --(divide by 6)--> [10 (cells per side)]
                                                          |
                                                          +--(double)--> [20] --(subtract 1)--> [19 (junggo count)]
                                                          |
                                                          +--(evaluate 10 through 18, then multiply by 9)--> [252]
                                                                                                             |
                                                                             [252] + [junggo 19] ----------> [271]
                                                                                                             |
                                                                                               (leave 1 empty)--> [270 (total cells)]
```

This chain revealed some remarkably integrated connections.

* **The secret of 152**: The value **152**, thought to be a lost line in the transcription, was not a simple misreading. It is generated independently by \((20 - 12) \times 19 = 152\), then joins the main chain as \(152 + 100 = 252\): a carefully constructed independent checking path. See [NAEJEOK_ASSESSMENT.md](NAEJEOK_ASSESSMENT.md).
* **What the algorithm is**: The commentary does not give a “placement algorithm” telling us where to put each value. Rather, it is a kind of **geometrical verification script**, expressed in an older mathematical grammar, that describes the diagram’s geometrical structure and rules for checking its cell count.

---

## 4. Reconstruction with Modern Computation: Simulated-Annealing Search

Some numerical conditions of the Nakseo Yukgodo’s grid are legible, but the document alone does not specify the order in which its values were placed. The number of ways to arrange the integers from \(1\) through \(270\) subject to the conditions is \(270! \approx 10^{543}\).

We introduce the **complementary-antipodal-pair hypothesis**, under which two values at antipodal positions always sum to \(271\). Fixing the relation \(v + v' = 271\) reduces the search space to \(2^{135} \times 135! \approx 1.2 \times 10^{271}\). This is not a historical fact; it is the combinatorial solution space under that hypothesis.

Even so, the remaining space is vast. To explore it, we used **simulated annealing**, an algorithm inspired by the physical process of gradually cooling metal to obtain a stable crystal ([solver.py](yukgodo/solver.py)).

[Insert `dashboard.png` here]

After many random trials and temperature adjustments, the program found an optimal arrangement with the theoretical lower-bound **final penalty of 6.0**.

* **Why 6.0 rather than 0.0?** The six sectors (45 cells each) and six rays (9 cells each) have odd numbers of cells, so they cannot be divided into exact halves. Perfectly equal sums are therefore structurally impossible. The alternating arrangements \(6097/6098\) and \(1219/1220\) are mathematically optimal, and reaching this limit gives a penalty of 6.0.

---

## 5. The Art of Residue Classes Forced by Mathematics: Modulo-5 Colouring and the Mod-\(N\) Generalisation

Another interesting analysis was applied to the reconstructed arrangement. The grid was coloured in five layers according to the remainder when each value \(v\) is divided by 5 (modulo 5, \(0 \dots 4\)); see `mod5.py`.

[Insert `mod5_coloring.png` here]
[Insert `mod5_layers.png` here]

An exhaustive analysis of the resulting residue-class layers from the perspective of hexagonal \(D_6\) symmetry uncovered a striking congruence relation.

* The **residue-2 and residue-4 layers**, as well as the **residue-1 and residue-0 layers**, coincide perfectly in all 54 cells after a \(180^\circ\) rotation (point symmetry).
* The **residue-3 layer** is itself point-symmetric under a \(180^\circ\) rotation.

[Insert `mod5_symmetry.png` here]

Is this a coincidence? The researchers formalised it mathematically as the following **mod-\(N\) antipodal-residue action theorem**.

### Mod-\(N\) Antipodal-Residue Action Theorem

> Suppose a point-symmetry map \(\pi\) exists on a grid and the sum of the values in every antipodal pair is a fixed constant \(S\). Then, for every modulus \(m\),
> \[
> v' \equiv (S - v) \pmod m.
> \]
> In other words, the antipodal transformation \(\pi\) always acts on a residue \(r\) as \(r \mapsto (S-r) \pmod m\).

For the Nakseo Yukgodo, the antipodal sum is \(S = 271\), which has remainder \(1\) modulo 5. Therefore:

* Residue 0 corresponds to \(1 - 0 = 1\). (\(0 \leftrightarrow 1\), perfect overlap.)
* Residue 2 corresponds to \(1 - 2 = -1 \equiv 4\). (\(2 \leftrightarrow 4\), perfect overlap.)
* Residue 3 corresponds to \(1 - 3 = -2 \equiv 3\). (\(3 \leftrightarrow 3\), self-antipodal symmetry.)

The `modn_generalization.py` module confirms that this theorem is a general mathematical consequence that applies equally to other diagrams in *Gusuryak*, such as Guhjagakdeuk Junggung and Junggwae Yongpaldo.

---

## 6. Conclusion: Traditional Mathematics Meets Computation—and the Questions That Remain

This Nakseo Yukgodo reconstruction project is more than an attempt to solve an old puzzle. It demonstrates several contemporary computational ideas.

1. **Data-driven documentary verification**: An exhaustive review of the formulas showed that the numbers in the lost traditional mathematical commentary were not misreadings, but independently checkable, mathematically precise calculation chains.
2. **Search techniques for constraint-satisfaction problems (CSPs)**: Simulated annealing efficiently found an optimal arrangement that reaches the mathematical limit (penalty 6.0) in a huge multidimensional search space.
3. **Generalisation through group theory and symmetry**: The analysis formalised traditional residue-class reasoning as a modern algebraic orbit action, then cross-validated it across several diagrams to reveal the deep symmetrical aesthetics of Joseon mathematics.

Because many arrangements satisfy the numerical sum conditions, reverse calculation alone cannot identify with certainty the exact, original arrangement drawn by Choe Seok-jeong; information about its ordering has been lost. Even so, the project establishes a rigorous boundary between what is geometrically possible and impossible.

Doesn’t the enormous numerical-grid algorithm imagined by a Joseon Chief State Councillor seem even more remarkable through the lens of today’s computers? We hope that clearer editions of the old text will someday be found, allowing the still-veiled placement-order rules (*gijwa*/寄左 and *seojwa*/序左) to be fully understood.

---

*This article is based on the results of the [Nakseo Yukgodo reconstruction project](README.md). Detailed code and consistency reports are available in the `output/` directory.*
