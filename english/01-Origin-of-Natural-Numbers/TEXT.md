## 數原苐一 The Origin of Numbers: Chapter 1

數生於道原者數之本也所以本始而生數者也
物必有本故數原為首

Numbers are born from the Way (道). "Origin" (原) is the root of numbers — that which serves as the beginning and gives birth to numbers.
All things must have a root; therefore the Origin of Numbers (數原) is placed first.

This is best read together with the interpretive chapter on the numbers of the River Map (河圖) and the Luo Writing (洛書) found in the Jeong (正) section of the Gusuryak.
In the commentary that follows, the River Map and the Luo Writing appear; the diagrams are based on the traditional River Map diagram and the Luo Writing magic square.

```
        7
        |
        2
        |
        5
        |
8 - 3 - 5 - 4 - 9
        |
        5 
        |
        1
        |
        6
```

Let us rewrite this as equations.

5 + 2 = 7 (top)
∴ 7 - 2 = 5

5 + 3 = 8 (left)
∴ 8 - 3 = 5

5 + 4 = 9 (right)
∴ 9 - 4 = 5
5 + 1 = 6 (bottom)
∴ 6 - 1 = 5

The number 5 appears three times, and apart from 5, each of the numbers from 1 to 9 is used exactly once.
This can be regarded as a foundational diagram explaining the decimal number system through the correspondence between the numbers 1 to 9 and the central number 5.

The Jeong section of the Gusuryak presents an explanation of this, and Choi Seok-jeong's interpretation is quite original.

First, one constructs a triangular lattice whose side has 10 cells.

Having done this, one decomposes every number from 1 to 10 into a sum of 1s.

```
1 = 1 (odd)
1 + 1 = 2 (even)
1 + 1 + 1 = 3 (odd)
1 + 1 + 1 + 1 = 4 (even)
1 + 1 + 1 + 1 + 1 = 5 (odd)
1 + 1 + 1 + 1 + 1 + 1 = 6 (even)
1 + 1 + 1 + 1 + 1 + 1 + 1 = 7 (odd)
1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 = 8 (even)
1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 = 9 (odd)
1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 = 10 (even)
```

In the original text, odd numbers are called Heavenly numbers (天數, cheonsu) and even numbers are called Earthly numbers (地數, jisu).

The following annotations are attached:

天數一三五七九
The Heavenly numbers are {1, 3, 5, 7, 9}.
地數二四六八十
The Earthly numbers are {2, 4, 6, 8, 10}.

積五十五
The sum of all these numbers is 55.

法曰併上下數共一十一
If the upper and lower numbers are paired side by side, each pair makes 11.

以位數十乘之得一百一十半之得五十五是天地之數

By this, multiplying 11 — the sum of the two end numbers — by 10, the count of the numbers, and then halving the result, one obtains 55.
Transcribing this into Python code gives the following:

```python3
first = 1
last = 10
count = 10

total = (first + last) * count // 2

assert total == 55
print(total)
```

與即四象變數中遍承之法
This is the same as the "universal pairing" (遍承) method within the Changing Numbers of the Four Images (四象變數).

```
十一
九二
八三
七四
六五

化裁五格各得一十一數
```

Transforming and arranging (化裁, hwajae) them, the five cells each obtain the number 11.

10 1
9  2
8  3
7  4
6  5



```
10 + 1 = 11
 9 + 2 = 11
 8 + 3 = 11
 7 + 4 = 11
 6 + 5 = 11
```

*This part calls for interpretation. In the Gusuryak, the four arithmetic operations are written as ga, gam, seung, je (加減承除: add, subtract, multiply/pair, divide), and there is a convention by which a grand total is written as jeok (積) and a partial sum as gakdeuk (各得). Here, however, the text says only "transform and arrange" (化裁) and merely lists the numbers. This admits of several interpretations. One interpretation: when writing 11 — the sum of 10, the first number in the decimal system that gains an extra digit, and 1, the smallest natural number in the decimal system — its foundation is that there is one unit in the tens place and one unit in the ones place, so the two places are set side by side. From this viewpoint, one cannot rule out an approach in which, even when 4 and 7 are added in this way, a 10 is completed to form the numbers of the River Map, while a 1 remains to make 11, so that the two digits come to occupy separate places. A second interpretation is a literary one, reading it as a philosophical symbol of Heaven and Earth meeting. A third interpretation is that it is simply a quotation with no particular meaning. The first interpretation reads naturally in the context of the Gusuryak before and after this passage, but the evidence for it is thin. The second interpretation is the most traditional, yet this is a mathematical treatise, not a philosophical one. The third interpretation is unlikely, given the publishing economics of an era when woodblock printing was expensive. The author's intent cannot be settled, and attempting to reconstruct the thinking of a scholar long gone from this world is liable to be inaccurate. Personally, I strongly advocate the first interpretation, but please judge for yourself after looking at the original text and the context that follows.*


Judging from the calculation that follows, the character 併 here most likely means pairing the numbers at the two ends together and summing them.

After this sentence, the 3x3 Luo Writing magic square appears.

4 9 2

3 5 7

8 1 6

(Rows)
4 + 9 + 2 = 15

3 + 5 + 7 = 15

8 + 1 + 6 = 15

(Columns)
4 + 3 + 8 = 15

9 + 5 + 1 = 15

2 + 7 + 6 = 15

(Diagonals)

4 + 6 + 5 = 15

2 + 5 + 8 = 15

(10 - 2) = 8

(10 - 8) = 2

(10 - 6) = 4

(10 - 4) = 6

8 and 2, and 4 and 6, are complementary pairs (with respect to 10), and they are located at antipodal points on the 3x3 plane.

Since there are two complementary pairs of 10, the sum of the four corners is naturally 20.

4 + 8 + 2 + 6 = 20 (the four corners)



易大傳曰天一地二天三地四天五地六天七天八天九地十
The Great Commentary (大傳) of the I Ching (易) says:
Heaven is 1, Earth is 2,
Heaven is 3, Earth is 4,
Heaven is 5, Earth is 6,
Heaven is 7, Earth is 8,
Heaven is 9, Earth is 10.

此即河圖之數也
These are none other than the numbers of the River Map (河圖).

```
S1 = {1,3,5,7,9}
S2 = {2,4,6,8,10}
```

尙書洪範傳曰初一次二次三次四次五次六次七次八次九
The Commentary on the "Great Plan" (洪範) of the Book of Documents (尙書, Shangshu) says: there is the first one, then the second, the third, the fourth, the fifth, the sixth, the seventh, the eighth, and the ninth.

```
S₀ = 1
Sₙ = Sₙ₋₁ + 1  (1 ≤ n ≤ 8)
∴ S = {S₀, S₁, ..., S₈} = {1, 2, ..., 9}
```

此即洛書之數也
These are the numbers of the Luo Writing (洛書).

河圖為體故始於一而終於十
The River Map is the substance (體), so it begins at 1 and ends at 10.
```
S₀ = 1
Sₙ = Sₙ₋₁ + 1  (1 ≤ n ≤ 9)
∴ S = {S₀, S₁, ..., S₉} = {1, 2, ..., 10}
```

洛書為用故去其十
The Luo Writing is the function (用), so it discards the 10

止於九數之大原出於次郃
and stops at nine. The great origin of numbers comes from combining them in sequence.

*This passage admits of several interpretations. It could be read as mere numerology or in a magical sense, but I append my own interpretation here.*

In the decimal system, the numbers 1 through 9 do not carry over into a new digit, but from 10 onward the digit is advanced. Thus, fundamentally, to express 1+9 one must add a digit and write it as 10. The ancient form of the character for 10 is sometimes written as a tied knot, or as an interlacing of warp and weft threads. Its exact origin is hard to determine, but when calculating with counting rods (算, san), 1 is written as a horizontal bar and 10 as a vertical bar. It is difficult to know whether this convention is related to the ancient character, yet one cannot simply dismiss as coincidence the fact that in the present day it is written in the shape of 十, with one 1 overlaid on another. The rule of the Luo Writing and the River Map is the principle of a pair: discard one from ten and you have nine; add one to nine and it becomes ten.

子曰大衍之數其算法之原乎

Confucius said: "The numbers of the Great Expansion (大衍) — are they not the very origin of the methods of calculation!"
*Confucius was a philosopher born in 551 BC, while the Dayan method (大衍術) first appears in the Sunzi Suanjing (孫子算經), which was compiled between the 3rd and 5th centuries AD. It is therefore far more likely that the Dayan method (the Chinese Remainder Theorem) was inspired by, or named in analogy to, Confucius's "Great Expansion," rather than that Confucius knew the Dayan method itself. In the 17th–18th centuries, when the author was active, more philosophical and mathematical texts survived than do today, and since not all ancient documents of the Spring and Autumn period are extant, it is hard to know which sources and which editions of the classics Choi Seok-jeong used for cross-verification. If new bamboo slips are excavated, the verdict on whether Confucius's mention of the Great Expansion refers to number theory could be overturned. This is a domain for philosophers working in classical Chinese studies, or for the Confucian philosophers of the surviving academies, to judge and research. As someone working in computing, I lack the insight to presume to judge the intent of the greatest scholar-official of the time — the Chief State Councillor — and to engage in textual controversy.*

The Dayan method, named after the "Great Expansion" in this passage, is a method whose name is known across East and West, past and present, and its substance is as follows.

x ≡ rᵢ (mod mᵢ)  (i = 1, 2, ..., n, where the mᵢ are pairwise coprime)

Under this condition, the method finds the smallest non-negative residue solution x with respect to M = m₁ × m₂ × ... × mₙ.

That is, one computes M = ∏ᵢ₌₁ⁿ mᵢ = m₁ × m₂ × ... × mₙ.

One then finds the value obtained by dividing this total product M by each modulus mᵢ.

Mᵢ = M / mᵢ

zᵢ ≡ Mᵢ⁻¹ (mod mᵢ)

Here, Mᵢ is called the "linked base number" (連基數, yeongisu) in East Asian mathematics.

One applies the Dayan search-for-one method (大衍求一術, Daeyeon gu'il-sul).

The solutions are then combined as x ≡ r₁M₁z₁ + r₂M₂z₂ + ... + rₙMₙzₙ  (mod M).

Completing all of this is the Dayan method; in modern terms, it is the Chinese Remainder Theorem.

```python
def crt(r_list, m_list):
    M = 1
    for m in m_list:
        M *= m

    M_list = [M // m for m in m_list]

    z_list = [pow(M_i, -1, m) for M_i, m in zip(M_list, m_list)]

    X = sum(r * M_i * z for r, M_i, z in zip(r_list, M_list, z_list))

    return X % M
```

It stands to reason that crt([2,3,2],[3,5,7]) yields 23.
子曰易有太極是生兩儀兩生象又曰蔘天兩地而倚數按太極者一也
一生二也二生三參兩而數立矣

Confucius said: "In the I Ching there is the Supreme Ultimate (太極, taegeuk); it gives birth to the Two Modes (兩儀, yang'i), and the Two Modes give birth to the Four Images."
He also said: "Three for Heaven, two for Earth — taking counsel of the two, one relies upon them to establish numbers." Upon examination, the Supreme Ultimate is 1. 1 gives birth to 2. 2 gives birth to 3. Three and two — thus are numbers established.

The interpretation of this is ambiguous, but a somewhat easier explanation is also possible.

I would like to add the following explanation.

Here, "Heavenly numbers" is synonymous with odd numbers, and "Earthly numbers" is synonymous with even numbers.
3 is the smallest prime among the odd numbers; 2 is the unique and smallest prime among the even numbers.

In fact, however, the original text speaks of "relying upon 2 and 3."
Let us now examine whether every integer can be expressed as an integer-coefficient linear combination of 2 and 3.

1 = 3 − 2

2 = 2

3 = 3

If n is even, then n = 2q for some integer q.
If n is odd, then n = 2q + 3 for some integer q.

Therefore, since gcd(2, 3) = 1, every integer is expressed as an integer-coefficient linear combination of 2 and 3.

2ℤ + 3ℤ = ℤ

This is not a definitive translation of 「參天兩地而倚數」 ("Three for Heaven, two for Earth, and thereby relying on numbers"), but a modern number-theoretic extension constructed from that phrase.

邵子曰太一者數之始也
Master Shao (邵子, Shao Yong) said: "The Supreme One (太一, tae'il) is the beginning of numbers."

*Here, the Supreme One can be regarded as a concept in image-number learning (象數學) referring to the One, or to the first principle of number. However, since the Supreme One is the first principle while the Supreme Ultimate gives birth to the Two Modes, one cannot carelessly claim that the Supreme One and the Supreme Ultimate are the same.*

太極者道之極也其此之謂乎
The Supreme Ultimate is the utmost of the Way — is this not what is meant?

This passage shows the viewpoint in traditional image-number learning that sets the One as the beginning of numbers. Yet this alone does not warrant the conclusion that the mathematics of that time lacked the concept of zero (零) or of an empty place. Placing 1 at the head in the generative sequence of numbers must be distinguished from the problem of handling zero values in calculation.
