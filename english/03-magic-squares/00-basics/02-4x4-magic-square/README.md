# 4×4 Magic Square Basics (四四圖)

## Yang Square (陽圖)

```
 2 16 13  3
11  5  8 10
 7  9 12  6
14  4  1 15
```

## Yin Square (陰圖)

```
 4  9  5 16
14  7 11  2
15  6 10  3
 1 12  8 13
```

Superimposing the two squares gives:

```
( 2, 4)(16, 9)(13, 5)( 3,16)
(11,14)( 5, 7)( 8,11)(10, 2)
( 7,15)( 9, 6)(12,10)( 6, 3)
(14, 1)( 4,12)( 1, 8)(15,13)
```

十六子順排四行 倒排四行  
The sixteen numbers are arranged in four rows in the forward direction and in four rows in the reverse direction.

順排者先以 外四角對換得以  
In the forward arrangement, first the outer four corners are swapped with their opposites.

內四角對換得陰圖  
Then the inner four corners are swapped with their opposites to obtain the yin square.

From 橫斜直皆三十四數  
Thus every row, column, and diagonal yields thirty-four (*皆三十四數*).

一變以爲陽圖  
One transformation yields the yang square.

## Reference

A famous artistic treatment of this 4×4 magic-square construction algorithm is found in Albrecht Dürer's engraving *Melencolia I*, dated 1514. In the West, this construction is often called "Dürer's algorithm" in his honor.

The most systematic early study of magic squares (*縱橫圖*) is Yang Hui's *Yang Hui Suanfa* (楊輝算法), written around 1275 during the Southern Song dynasty. Choi Seok-jeong likely consulted this text.

## Author's Note

Research on orthogonal Latin squares and puzzles with shared vertices (such as the Jisu-guimun-do) developed quite early in Korea, but general magic squares are better known in China and Europe through celebrated treatises.

What is remarkable is that, despite this back-and-forth lead, the cultural development of East and West tends to synchronize at similar speeds after a certain point.

It reminds one of the synchronicity in the *Baki* series.
