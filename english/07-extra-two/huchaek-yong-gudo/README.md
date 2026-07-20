# Huchaek-yong-gudo

Following the LibreWiki description, Huchaek-yong-gudo is read as a diagram
using the 72 values 1..72, with 13 octagons and 12 squares arranged together.
The eight values of each octagon sum to 292, and the four values of each square
sum to 146.

The construction rule can be summarized as follows.

- Make the diagonal edge pairs of the octagons sum to 73.
- Then an octagon sum is obtained as `73 x 4 = 292`.
- For the squares, make one two-value side sum to 74 and the opposite side sum
  to 72; then `74 + 72 = 146`.
- This can be read as placing 1..36 in a reference region and matching them
  with 37..72 in the complementary direction.

The original reconstruction also follows the LibreWiki Huchaek-yong-gudo rule.
However, it is a conservative reconstruction centered on preserving the diagram
shape and the displayed local pair sums, rather than a numerically optimized
edition that enforces every 1..72 and unit-sum condition. The differences found
by the checker should therefore be read as the gap between a form-centered
original reconstruction and a numerically complete corrected edition, not as a
rejection of the rule.

The corrected edition is stored separately as `CORRECTED_FORMATIONS` in
`huchaek_data.py`. In that edition, 1..72 are used exactly once, the side-pair
sum distribution is `73` x 18, `74` x 9, and `72` x 9, and every working
octagon unit sums to 292. See `corrected_analysis.md` for details.

## Files

- `huchaek_data.py` — original reconstruction data and corrected data
- `visualize.py` — original-reconstruction 3x3 working-unit visualization
- `analyze_huchaek_yonggudo.py` — rule checker
- `visualize_huchaek_rule_pairs.py` — pair-sum visualization for `73`, `74`, `72`
- `visualize_corrected.py` — corrected-edition visualization
- `visualize_corrected_rule_pairs.py` — corrected pair-sum visualization
- `corrected_analysis.md` — corrected-edition study
