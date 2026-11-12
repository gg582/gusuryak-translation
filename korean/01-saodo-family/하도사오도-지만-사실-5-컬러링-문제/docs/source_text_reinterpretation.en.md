# The Hado Saodo source text, reinterpreted: 水土相涵 · 金火相守 · 兩木相摩

## 1. Source text

> 一六水 二七火 三八木 四九金 五十土
> 此圖水土相涵 金火相守 兩木相摩
> 傳曰 木與木相摩則然 金與火相守則流

## 2. Literal translation

| Source | Translation |
|---|---|
| 一六水 二七火 三八木 四九金 五十土 | 1 and 6 are Water, 2 and 7 Fire, 3 and 8 Wood, 4 and 9 Metal, 5 and 10 Earth. |
| 此圖水土相涵 | In this diagram Water and Earth are steeped in each other. |
| 金火相守 | Metal and Fire keep company. |
| 兩木相摩 | The two Woods rub together. |
| 傳曰 | As the tradition has it, |
| 木與木相摩則然 | when wood rubs against wood, it catches fire; |
| 金與火相守則流 | when metal stays with fire, it (melts and) flows. |

### 2.1 Source of the quotation and the character 然

- The two lines after 傳曰 quote *Zhuangzi*, "External Things" (外物): "木與木相摩則然，金與火相守則流". Choe Seok-jeong did not invent the image. He attached a classical quotation as a gloss on the three preceding phrases.
- **然** is neither a misprint nor a loose phonetic loan. It is the **original character** for "to burn". The *Shuowen Jiezi* gives "然，燒也。从火肰聲", and 燃 is a later form that added another 火 after 然 came to be used mostly for "so, thus". "則然" therefore reads exactly as "then it catches fire".

## 3. Number labels

The Hado assignment in the first line coincides exactly with the residue classes mod 5.

| Phase | Hado numbers | n mod 5 | Elements in Saodo |
|---|---|---|---|
| Water 水 | 一六 | 1 | 1, 6, 11, 16 |
| Fire 火 | 二七 | 2 | 2, 7, 12, 17 |
| Wood 木 | 三八 | 3 | 3, 8, 13, 18 |
| Metal 金 | 四九 | 4 | 4, 9, 14, 19 |
| Earth 土 | 五十 | 0 | 5, 10, 15, 20 |

## 4. Reinterpretation: the three phrases are the three types of complement pair

These are the five palaces (2×2 blocks) of the Hado Saodo, as laid out in the source:

| Palace | Four numbers | Complement pairs (sum 21) | Phase content | Source phrase |
|---|---|---|---|---|
| Top | 19, 2, 7, 14 | (2,19), (7,14) | Fire 2, Metal 2 | 金火相守 |
| Right | 4, 17, 12, 9 | (4,17), (9,12) | Fire 2, Metal 2 | 金火相守 |
| Centre | 5, 16, 11, 10 | (5,16), (10,11) | Water 2, Earth 2 | 水土相涵 |
| Bottom | 15, 1, 6, 20 | (1,20), (6,15) | Water 2, Earth 2 | 水土相涵 |
| Left | 13, 8, 18, 3 | (3,18), (8,13) | Wood 4 | 兩木相摩 |

Every palace sums to 42, and every palace splits exactly into two complement pairs with sum 21.

Because `21 ≡ 1 (mod 5)`, the involution `n ↦ 21 − n` acts on the phase labels as `r ↦ 1 − r (mod 5)`:

- Water (1) ↔ Earth (0)
- Fire (2) ↔ Metal (4)
- Wood (3) ↔ Wood (3), since `1 − 3 = −2 ≡ 3`

This involution has exactly three orbit types, and the three phrases list all three of them:

1. **水土相涵**: Water pairs with Earth. The centre and bottom palaces are of this type.
2. **金火相守**: Metal pairs with Fire. The top and right palaces are of this type.
3. **兩木相摩**: Wood is the **unique fixed point** of the involution, so its partner is again Wood. That is why "two Woods" form a pair, and all four Wood numbers sit together in the left palace.

The palace sum 42 then follows at once: each palace holds two complement pairs, so `2 × 21 = 42`. The arithmetic progression of phase-group sums (Water 34, Fire 38, Wood 42, Metal 46, Earth 50) with `34 + 50 = 38 + 46 = 2 × 42` is the same involution seen at the level of whole groups.

The *Zhuangzi* lines after 傳曰 attach images from nature to these three pairings. Wood rubbed on wood catches fire, and metal kept with fire melts and flows. We read them as a literary gloss: two elements of different nature are bound into one palace and balance each other there.

## 5. Testing the multiplicative reading

One proposed reading takes 相摩 as multiplication: "the product of Wood-group numbers produces the Fire group".

- Mod 5, `Wood · Wood = 3 · 3 = 9 ≡ 4`, which is **Metal**. All six Wood·Wood products in the left palace (3·8, 3·13, 3·18, 8·13, 8·18, 13·18) are Metal. This is an algebraic fact and holds for any layout.
- Fire arises only as `Wood³ ≡ 2` or `Wood · Metal ≡ 2`, never as the product of "two Woods".
- The left (Wood) palace of Saodo contains no Fire element, so "catches fire" is not reflected in the layout either.

**Reading 則然 as the result of a product therefore does not hold.** The multiplicative view does show one tidy side structure:

| Pair type | Pair product n·(21−n) mod 5 | Product of the palace's four numbers mod 5 |
|---|---|---|
| 水土 (相涵) | Earth | Earth |
| 火金 (相守) | Wood | Metal |
| 木木 (相摩) | Metal | Water (3⁴ ≡ 1) |

The product of a 相守 pair is Wood and the product of a 相摩 pair is Metal, so under multiplication the two phrases trade elements. We record this only as an algebraic fact and do not use it as evidence for how to read the text.

The same test run over every other Gusuryak diagram is in [Wood-product audit](../../../04-unification/목-곱셈-검증/README.md). In short, of the 124 Wood·Wood pairs that lie inside a single palace, none has a Fire product. Every diagram whose complement sum satisfies `C ≡ 1 (mod 5)` (Nakseo Sagudo, Nakseo Palgudo, Hado Chil-/Pal-/Gu-odo, Nakseo Yukgodo) shows the same three pairings: Water–Earth, Fire–Metal and Wood–Wood. In the Hado Palodo in particular, the phase content of each palace repeats Saodo's, with the same type in the same position.
