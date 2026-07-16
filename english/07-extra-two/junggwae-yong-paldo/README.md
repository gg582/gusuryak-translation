## Source Text

六十四子總積一千
八十以八子為一隊
各得一百六十數
變則八隊化為二十
四隊再變則為一百
五十六隊演積六萬
六千五百六十合於
武侯陣圖

## Explanation

- 64 numbers are used; the source states the total accumulation as 1,000.
- They are grouped eight at a time to make one *dae* (隊, squad).
- Each squad sums to 160.
- When transformed, 8 squads become 20 forms.
- Transformed again, they become 100 forms.
- In total, 56 squads (formations) are produced, and the overall case corresponds to 6,560.
- This is related to the *Muhu-jin-do* (武侯陣圖), i.e., Zhuge Liang's Eight-Formation Diagram (八陣圖).

## Data Correction

The original transcription contains transcription errors. For the detailed investigation, see `transcription_analysis.md`.

### Problems Found

- The sums of 4 of the 8 formations are not 260.
- **14** and **22** appear twice, while **20** and **29** are missing.
- The total sum of the 8 formations is 13 less than the sum 1..64, which is 2080.

### Adopted Correction

Restore the sum of every formation to 260 while preserving the original layout as much as possible.

| Position | Change |
|---|---|
| Row 1, Col 1 (vertical) | 14 → 20, 25 → 29 |
| Row 1, Col 2 (horizontal) | 33 → 35 |
| Row 1, Col 3 (vertical) | 22 → 25 |
| Row 2, Col 1 (vertical) | 35 → 33 |

- The 33 ↔ 35 swap preserves the intended *byeon-jin* (變陣, transformation) relation (±2 correspondence) between Row 1, Col 2 and Row 2, Col 1.
- 14 → 20, 25 → 29, and 22 → 25 resolve the duplication and omission.

### Generated Files

- `visualize_wrong_origin.py` — visualizes the original transcription (with errors) (`eight_formation_diagram_wrong_origin.png`, `.svg`)
- `visualize_corrected.py` — visualizes the corrected version (`eight_formation_diagram_corrected.png`, `.svg`)

The original transcription visualization is preserved as-is; the normal form is generated as a separate file.
