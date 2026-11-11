# 木與木相摩則然: an exhaustive test of the "Wood × Wood → Fire" multiplicative reading

The Hado Saodo source text says "兩木相摩 … 木與木相摩則然". If 相摩 is read as **multiplication**, it suggests that the product of Wood-group numbers produces the Fire group. This note runs that hypothesis the same way over 17 diagrams from the Gusuryak magic-figure article. The Nakseo Yukgodo is treated only theoretically.

- Script: [`wood_product_audit.py`](wood_product_audit.py) (no external dependencies)
- Full output: [`audit_report.txt`](audit_report.txt)
- Source-text reinterpretation: [The Hado Saodo source text, reinterpreted](../../01-saodo-family/hado-saodo-5-coloring/docs/source_text_reinterpretation.en.md)

Labels follow the source: `n ≡ 1 Water(水), 2 Fire(火), 3 Wood(木), 4 Metal(金), 0 Earth(土) (mod 5)`.

## 1. Summary of conclusions

1. **The multiplicative hypothesis fails.** Mod 5, `木·木 = 3·3 = 9 ≡ 4`, which is **Metal**. All 124 Wood·Wood pairs that lie inside one palace have a Metal product, and none has a Fire product. This is an algebraic fact, so no layout can change it.
2. **Reducing by another modulus gives no meaningful signal either.** We reduced each product mod N (the largest number used) and mod C (the complement sum) and checked whether the result is a Fire number of that diagram. The hits were 8/124 and 34/124, against a base-rate expectation of about 24.5. The excess mod C has a one-sided binomial p ≈ 0.025. Three moduli were tried without prior motivation, so after correction p ≈ 0.075, which is not significant. The phase of `ab mod C` also shifts with the quotient k as `4 − k·C (mod 5)`, so there is no structural reason for it.
3. **What explains the three source phrases exactly is addition, through complement pairs.** The Hado Saodo complement sum is `C = 21 ≡ 1 (mod 5)`, so the involution `n ↦ 21 − n` maps phases as Water↔Earth, Fire↔Metal and Wood↔Wood. This involution has exactly three orbit types, and the phrases **水土相滲 · 金火相守 · 兩木相摩** list all three of them. Wood is the unique fixed point (self-complementary), which is why "two Woods" pair with each other. The source-text note has the details.
4. **The multiplicative view does yield one clean structure.** The product of a complement pair, `n·(C−n) ≡ r(1−r) (mod 5)`, is:

   | Pair type | Phase of product |
   |---|---|
   | 水土 (相滲) | Earth |
   | 火金 (相守) | **Wood** |
   | 木木 (相摩) | **Metal** |

   So under multiplication the 相守 and 相摩 pairs trade elements, and a Water–Earth pair is absorbed into Earth, the zero for multiplication. Fire arises only as `木³ = 27 ≡ 2` or `木·金 = 12 ≡ 2`. This gives no basis for reading 則然 ("catches fire") as a product. We still record it, together with the palace-level products (mod 5) of the Hado Saodo: Wood palace → Water (3⁴ ≡ 1), Fire–Metal palaces → Metal, Water–Earth palaces → Earth.

## 2. Multiplication table mod 5

```
     Wa  Fi  Wo  Me  Ea
  Wa  Wa  Fi  Wo  Me  Ea
  Fi  Fi  Me  Wa  Wo  Ea
  Wo  Wo  Wa  Me  Fi  Ea
  Me  Me  Wo  Fi  Wa  Ea
  Ea  Ea  Ea  Ea  Ea  Ea
```

Powers of Wood: `木¹ = Wood, 木² = Metal, 木³ = Fire, 木⁴ = Water`. Wood (3) generates the multiplicative group (ℤ/5)\*.

## 3. Results by diagram

`C` is the complement sum each diagram uses. It is usually N+1; for the Nakseo Gugudo it is 91, the sum used for the surrounding numbers. "Partner of 木" is the phase Wood is paired with under `r ↦ C − r (mod 5)`.

| Diagram | Range | C | C mod 5 | Partner of 木 | Wood·Wood pairs in palaces | Product ≡ Fire | Complement-pair types in palaces |
|---|---|---|---|---|---|---|---|
| Hado Saodo | 1–20 | 21 | 1 | **Wood** | 6 | 0 | 火金 4, 木木 2, 水土 4 (5/5 palaces split fully) |
| Nakseo Sagudo | 1–20 | 21 | 1 | **Wood** | 8 | 0 | 火金 8, 木木 4, 水土 6 (9/9 palaces split fully) |
| Nakseo Palgudo | 1–40 | 41 | 1 | **Wood** | 10 | 0 | 水土 11, 火金 10, 木木 5 |
| Nakseo Gugudo (reading) | 1–81 | 91 | 1 | **Wood** | 7 | 0 | (complement pairs mostly replaced by the mod-9 transversal structure) |
| Hado Chilodo (article table) | 1–35 | 36 | 1 | **Wood** | 11 | 0 | 火金 2, 木木 2, 水土 2 |
| Hado Palodo | 1–40 | 41 | 1 | **Wood** | 28 | 0 | 火金 4, 木木 4, 水土 4 |
| Hado Guodo | 1–45 | 46 | 1 | **Wood** | 21 | 0 | 火金 6, 木木 3, 水土 7 |
| Nakseo Yukgodo | 1–270 | 271 | 1 | **Wood** | — | — | antipodal pairs are only of types 水土, 火金, 木木 |
| Beomsu Yongodo | 1–9 | 10 | 0 | Fire | 0 | — | 火木 2, 水金 2 |
| Jangchaek Yongchildo | 1–19 | 20 | 0 | Fire | 1 | 0 | 火木 3, 土土 1, 水金 1 |
| Junggwae Yongpaldo | 1–64 | 65 | 0 | Fire | 5 | 0 | 火木 13, 水金 11, 土土 4 |
| Gichaek Yongpaldo | 1–24 | 25 | 0 | Fire | 5 | 0 | 火木 4, 土土 2, 水金 2 |
| Jungui Yongyukdo | 1–16 | 17 | 2 | Metal | 3 | 0 | 土火 4, 水水 2, 木金 2 |
| Cheonsu Yongodo (revised) | 1–21 | 22 | 2 | Metal | 1 | 0 | 土火 2, 水水 2, 木金 1 |
| Huchaek Yonggudo (corrected) | 1–72 | 73 | 3 | Earth | 5 | 0 | 水火 15, 土木 14, 金金 7 (9/9 split fully) |
| Nakseo Ogudo | 1–33 | 34 | 4 | Water | 1 | 0 | 水木 2 |
| Nakseo Chilgudo | 1–63 | 64 | 4 | Water | 6 | 0 | 水木 9, 土金 6, 火火 4 |
| Jungsang Yonggudo (source) | 1–33 | 34 | 4 | Water | 6 | 0 | 水木 2, 土金 2, 火火 1 |

## 4. Meaningful observations

### 4.1 The three source phrases classify complement pairs in the C ≡ 1 (mod 5) family

Wood is self-complementary exactly when `C ≡ 1 (mod 5)`, and only then do the three types Water–Earth, Fire–Metal and Wood–Wood appear. The Hado Saodo, Nakseo Sagudo, Nakseo Palgudo, Hado Chil-/Pal-/Gu-odo and Nakseo Yukgodo all belong to this family. So 兩木相摩 is not a remark about the Saodo alone. It applies unchanged to the whole Hado family that grows from the Saodo.

- **Hado Saodo**: all five palaces split exactly into two complement pairs. By phase content, top and right are 火金 (相守), centre and bottom are 水土 (相滲), and left is 木木 (相摩).
- **Nakseo Sagudo**: all nine palaces split exactly into two complement pairs, and only the three types occur.
- **Hado Palodo**: the phase content of each palace (top Fire 4 Metal 4, left Wood 8, centre Water 4 Earth 4, right Fire 4 Metal 4, bottom Water 4 Earth 4) repeats the Saodo, with **the same type in the same position**. The three phrases hold palace by palace in the Paljagakdeuk as well.

### 4.2 In other families Wood's partner changes

- `C ≡ 0` (Beomsu Yongodo, Jangchaek Yongchildo, Junggwae Yongpaldo, Gichaek Yongpaldo): Wood's complement partner is **Fire**, so one Wood and one Fire form a complement pair. This is the only family where addition links "Wood to Fire", but the link is Wood with Fire, not Wood with Wood.
- `C ≡ 2` → Wood↔Metal, `C ≡ 3` → Wood↔Earth, `C ≡ 4` → Wood↔Water.

### 4.3 Spatial co-occurrence

We also checked whether a palace holding two or more Woods also holds a Fire. The Wood palace (left) of the Hado Saodo holds no Fire. The text's "catches fire" therefore does not show up as a Fire element in the Saodo layout. The phrase is best read as a **quoted image** (from *Zhuangzi*, "External Things"), not as a layout rule.

## 5. Verdict

| Reading | Verdict |
|---|---|
| 相摩 = product mod 5, 木·木 → 火 | **Rejected** (always 金, 124/124) |
| 相摩 = product reduced mod N or mod C | **Not significant** (after multiple-comparison correction) |
| 相滲 · 相守 · 相摩 = the three orbit types of the complement involution `n ↦ C−n` | **Accepted** (Saodo 5/5 palaces, Sagudo 9/9 palaces, the whole C ≡ 1 family) |
| 則然 · 則流 = Five-Phase images quoted from *Zhuangzi* | Accepted (see the source-text note) |
| Multiplicative side structure: 火金 pair product → 木, 木木 pair product → 金 | Recorded as an algebraic fact, not used as evidence for reading the text |
