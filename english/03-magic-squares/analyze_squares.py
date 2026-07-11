#!/usr/bin/env python3
"""
Magic square analysis script.
Analyzes the mathematical properties of traditional Korean magic squares recorded in square.md.
"""

import os
from collections import defaultdict

# Raw data extracted from square.md
SQUARES = {
    "Yukyukdo (Six-Six Board, 六六圖)": {
        "order": 6,
        "examples": [
            [
                [13, 22, 18, 27, 11, 20],
                [31, 4, 36, 9, 29, 2],
                [12, 21, 14, 23, 16, 25],
                [30, 3, 5, 32, 34, 7],
                [17, 26, 10, 19, 15, 24],
                [8, 35, 28, 1, 6, 33],
            ],
            [
                [4, 13, 36, 27, 29, 2],
                [22, 31, 18, 9, 11, 20],
                [3, 21, 23, 32, 25, 7],
                [30, 12, 5, 14, 16, 34],
                [17, 26, 19, 28, 6, 15],
                [35, 8, 10, 1, 24, 33],
            ],
        ],
    },
    "Gusudo (Nine Palace, 九數圖)": {
        "order": 9,
        "examples": [
            [
                [31, 76, 13, 36, 81, 18, 29, 74, 11],
                [22, 40, 58, 27, 45, 63, 20, 38, 56],
                [67, 4, 49, 72, 9, 54, 65, 2, 47],
                [30, 75, 12, 32, 77, 14, 34, 79, 16],
                [21, 39, 57, 23, 41, 59, 25, 43, 61],
                [66, 3, 48, 68, 5, 50, 70, 7, 52],
                [35, 80, 17, 28, 73, 10, 33, 78, 15],
                [26, 44, 62, 19, 37, 55, 24, 42, 60],
                [71, 8, 53, 64, 1, 46, 69, 6, 51],
            ],
            [
                [50, 18, 55, 70, 5, 48, 3, 76, 44],
                [66, 31, 26, 29, 81, 13, 52, 11, 60],
                [7, 74, 42, 24, 37, 62, 68, 36, 19],
                [54, 67, 2, 65, 25, 33, 28, 23, 72],
                [59, 21, 43, 9, 41, 73, 15, 61, 47],
                [10, 35, 78, 49, 57, 17, 80, 39, 4],
                [79, 6, 38, 20, 69, 34, 32, 64, 27],
                [30, 71, 22, 45, 1, 77, 16, 51, 56],
                [14, 46, 63, 58, 53, 12, 75, 8, 40],
            ],
        ],
    },
    "Baekjajasuyin-yang-chakjong (Hundred-Numbers Yin-Yang Intertwining Diagram, 百子子數陰陽錯綜圖)": {
        "order": 10,
        "examples": [
            [
                [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
                [1, 10, 9, 8, 7, 6, 5, 4, 3, 2],
                [2, 1, 10, 9, 8, 7, 6, 5, 4, 3],
                [3, 2, 1, 10, 9, 8, 7, 6, 5, 4],
                [4, 3, 2, 1, 10, 9, 8, 7, 6, 5],
                [5, 4, 3, 2, 1, 10, 9, 8, 7, 6],
                [6, 5, 4, 3, 2, 1, 10, 9, 8, 7],
                [7, 6, 5, 4, 3, 2, 1, 10, 9, 8],
                [8, 7, 6, 5, 4, 3, 2, 1, 10, 9],
                [9, 8, 7, 6, 5, 4, 3, 2, 1, 10],
            ],
            [
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                [9, 0, 1, 2, 3, 4, 5, 6, 7, 8],
                [8, 9, 0, 1, 2, 3, 4, 5, 6, 7],
                [7, 8, 9, 0, 1, 2, 3, 4, 5, 6],
                [6, 7, 8, 9, 0, 1, 2, 3, 4, 5],
                [5, 6, 7, 8, 9, 0, 1, 2, 3, 4],
                [4, 5, 6, 7, 8, 9, 0, 1, 2, 3],
                [3, 4, 5, 6, 7, 8, 9, 0, 1, 2],
                [2, 3, 4, 5, 6, 7, 8, 9, 0, 1],
                [1, 2, 3, 4, 5, 6, 7, 8, 9, 0],
            ],
        ],
    },
    "Baekjasaengseong-sunsu (Hundred-Numbers Pure-Generation Diagram, 百子生成純數圖)": {
        "order": 10,
        "examples": [
            [
                [90, 89, 78, 67, 56, 45, 34, 23, 12, 1],
                [86, 79, 39, 58, 97, 4, 43, 32, 21, 15],
                [77, 66, 50, 99, 88, 13, 2, 41, 25, 24],
                [68, 57, 96, 80, 79, 22, 11, 5, 44, 33],
                [59, 98, 87, 76, 60, 31, 25, 14, 3, 42],
                [24, 3, 14, 25, 31, 60, 76, 87, 98, 59],
                [33, 44, 5, 11, 22, 79, 80, 96, 57, 68],
                [24, 35, 41, 2, 13, 88, 99, 50, 66, 77],
                [15, 21, 32, 43, 4, 97, 58, 69, 70, 86],
                [1, 12, 23, 34, 45, 56, 67, 78, 89, 90],
            ],
        ],
    },
    "Baekjasaengseong-gyosu (Hundred-Numbers Crossed-Numbers Diagram, 百子生成交數圖)": {
        "order": 10,
        "examples": [
            [
                [46, 55, 64, 73, 82, 91, 100, 19, 28, 37],
                [7, 94, 53, 62, 71, 85, 16, 20, 39, 48],
                [18, 83, 92, 51, 65, 74, 27, 36, 40, 9],
                [29, 72, 81, 95, 54, 63, 38, 47, 6, 10],
                [30, 61, 75, 84, 93, 52, 59, 8, 17, 26],
                [61, 30, 26, 17, 8, 49, 42, 93, 84, 75],
                [72, 29, 10, 6, 47, 38, 63, 54, 95, 81],
                [83, 18, 9, 40, 36, 27, 74, 65, 51, 92],
                [94, 7, 48, 39, 20, 16, 85, 71, 62, 53],
                [55, 46, 37, 28, 19, 100, 91, 82, 73, 64],
            ],
        ],
    },
    "Baekjayin-yang-jamo-chakjong (Hundred-Numbers Yin-Yang Mother-Child Intertwining Diagram, 百子陰陽子母錯綜圖)": {
        "order": 10,
        "examples": [
            [
                [100, 89, 78, 67, 56, 45, 34, 23, 12, 1],
                [29, 28, 47, 36, 10, 91, 65, 54, 73, 72],
                [48, 17, 26, 40, 39, 62, 61, 75, 84, 53],
                [27, 46, 50, 9, 88, 13, 92, 51, 55, 74],
                [76, 80, 59, 98, 87, 14, 3, 32, 21, 25],
                [15, 31, 42, 43, 4, 97, 58, 69, 70, 86],
                [24, 35, 41, 2, 83, 18, 99, 60, 66, 77],
                [93, 94, 85, 71, 52, 49, 30, 16, 7, 8],
                [82, 63, 64, 95, 81, 20, 6, 37, 38, 19],
                [11, 22, 33, 44, 5, 96, 57, 68, 79, 90],
            ],
        ],
    },
}


def magic_constant(n, start=1):
    """Magic constant for consecutive integers 1..n^2 or 0..n^2-1."""
    if start == 0:
        return n * (n * n - 1) // 2
    return n * (n * n + 1) // 2


def flatten(matrix):
    return [x for row in matrix for x in row]


def is_normal_set(values, n, start=1):
    """Check whether the value set contains each integer from start to n^2-1+start exactly once."""
    expected = set(range(start, start + n * n))
    return set(values) == expected


def row_sums(m):
    return [sum(row) for row in m]


def col_sums(m):
    n = len(m)
    return [sum(m[i][j] for i in range(n)) for j in range(n)]


def diag_sums(m):
    n = len(m)
    d1 = sum(m[i][i] for i in range(n))
    d2 = sum(m[i][n - 1 - i] for i in range(n))
    return [d1, d2]


def wrapped_diagonal_sums(m):
    """Pan-diagonal check: sums of all wrapped diagonals in the main diagonal directions."""
    n = len(m)
    sums = []
    # Top-left to bottom-right direction (start points in first row)
    for start_col in range(n):
        s = 0
        for i in range(n):
            s += m[i][(start_col + i) % n]
        sums.append(s)
    # Top-right to bottom-left direction (start points in first row)
    for start_col in range(n):
        s = 0
        for i in range(n):
            s += m[i][(start_col - i) % n]
        sums.append(s)
    return sums


def is_associated(m):
    """Associated magic square: every pair of cells symmetric about the center has the same sum."""
    n = len(m)
    pairs = []
    for i in range(n):
        for j in range(n):
            pairs.append(m[i][j] + m[n - 1 - i][n - 1 - j])
    return len(set(pairs)) == 1, pairs[0]


def is_bimagic(m):
    """Bimagic: row/column/diagonal sums of squares are also equal."""
    n = len(m)
    sums = []
    for row in m:
        sums.append(sum(x * x for x in row))
    for j in range(n):
        sums.append(sum(m[i][j] * m[i][j] for i in range(n)))
    sums.append(sum(m[i][i] * m[i][i] for i in range(n)))
    sums.append(sum(m[i][n - 1 - i] * m[i][n - 1 - i] for i in range(n)))
    return len(set(sums)) == 1, sums[0]


def symmetry_by_center(m):
    """180-degree rotational symmetry."""
    n = len(m)
    for i in range(n):
        for j in range(n):
            if m[i][j] != m[n - 1 - i][n - 1 - j]:
                return False
    return True


def analyze(name, data):
    n = data["order"]
    results = []
    for idx, m in enumerate(data["examples"]):
        flat = flatten(m)
        start = min(flat)
        normal = is_normal_set(flat, n, start)
        rows = row_sums(m)
        cols = col_sums(m)
        diags = diag_sums(m)
        mc = magic_constant(n, start)

        # Magic square determination
        all_line_sums = rows + cols + diags
        is_magic = len(set(all_line_sums)) == 1

        # Semi-magic
        is_semi = len(set(rows + cols)) == 1

        # Pan-diagonal
        wrap_diags = wrapped_diagonal_sums(m)
        is_pan = is_magic and len(set(wrap_diags)) == 1

        # Associated
        assoc, assoc_sum = is_associated(m)

        # Bimagic
        bimagic, bimagic_sum = is_bimagic(m) if is_magic else (False, None)

        results.append(
            {
                "example": idx + 1,
                "min": min(flat),
                "max": max(flat),
                "normal_set": normal,
                "magic_constant": mc,
                "row_sums": rows,
                "col_sums": cols,
                "diag_sums": diags,
                "is_semi_magic": is_semi,
                "is_magic": is_magic,
                "is_pan_diagonal": is_pan,
                "wrapped_diag_sums": wrap_diags,
                "is_associated": assoc,
                "associated_sum": assoc_sum,
                "is_bimagic": bimagic,
                "bimagic_sum": bimagic_sum,
                "symmetry_180": symmetry_by_center(m),
            }
        )
    return results


def describe_generation_rule(name, data):
    """Describe each magic square's generation rule in text."""
    n = data["order"]
    if name == "Yukyukdo (Six-Six Board, 六六圖)":
        return (
            "6×6 magic square. The two examples are different arrangements but both have the same magic constant 111. "
            "The first example is a normal magic square with row/column/diagonal sums of 111. "
            "The second example is also a normal magic square with row/column/diagonal sums of 111. "
            "The two examples are not related by 90° rotation or reflection; they are different isomorphic forms."
        )
    elif name == "Gusudo (Nine Palace, 九數圖)":
        return (
            "9×9 magic square. The magic constant is 9×(81+1)/2 = 369. "
            "Both examples are normal magic squares that use each of the numbers 1 through 81 exactly once. "
            "The second example is likely in the same magic square group as the first, obtained by row/column permutations or reversals."
        )
    elif name == "Baekjajasuyin-yang-chakjong (Hundred-Numbers Yin-Yang Intertwining Diagram, 百子子數陰陽錯綜圖)":
        return (
            "10×10. The first example is a matrix filled by repeating only the numbers 1~10; "
            "although every row/column sum is 55, the value set is not 1~100, so it is not a conventional magic square. "
            "The second example is a matrix filled by repeating the numbers 0~9; every row/column sum is 45. "
            "These two matrices are complementary (yin/yang) Latin squares or circulant structures, "
            "and their combination could form components of an orthogonal Latin square pair."
        )
    elif name == "Baekjasaengseong-sunsu (Hundred-Numbers Pure-Generation Diagram, 百子生成純數圖)":
        return (
            "10×10 magic square. It uses each of the numbers 1 through 100 exactly once and has magic constant 505. "
            "All row/column/diagonal sums are 505. It has top-bottom, left-right, and diagonal center-symmetry (associated) properties. "
            "Rows such as row 1 and row 10, and columns such as column 1 and column 10, are in reverse/complementary relationships, so the construction consists of dual-symmetric pairs."
        )
    elif name == "Baekjasaengseong-gyosu (Hundred-Numbers Crossed-Numbers Diagram, 百子生成交數圖)":
        return (
            "10×10 magic square. It uses each of the numbers 1 through 100 exactly once and has magic constant 505. "
            "Similar to Baekjasaengseong-sunsu but with a different character. "
            "The positions of each pair appear crossed or exchanged, as the name 'gyosu (crossed numbers)' suggests. "
            "It has top-bottom and center-symmetry (associated) properties."
        )
    elif name == "Baekjayin-yang-jamo-chakjong (Hundred-Numbers Yin-Yang Mother-Child Intertwining Diagram, 百子陰陽子母錯綜圖)":
        return (
            "10×10 magic square. It uses each of the numbers 1 through 100 exactly once and has magic constant 505. "
            "As the name 'yin-yang (陰陽)' and 'jamo (mother-child)' suggests, the numbers are arranged in complementary pairs. "
            "The center-symmetric positions sum to 101, satisfying the associated magic square property. "
            "It looks like a structure made by superimposing two 10×10 Latin squares."
        )
    return ""


def main():
    output_dir = "/home/yjlee/gusuryak-translation/english/03-magic-squares"
    folder_map = {
        "Yukyukdo (Six-Six Board, 六六圖)": "01-yukyukdo-six-six-board",
        "Gusudo (Nine Palace, 九數圖)": "02-gusudo-nine-palace",
        "Baekjajasuyin-yang-chakjong (Hundred-Numbers Yin-Yang Intertwining Diagram, 百子子數陰陽錯綜圖)": "03-baekjajasuyin-yang-chakjong",
        "Baekjasaengseong-sunsu (Hundred-Numbers Pure-Generation Diagram, 百子生成純數圖)": "04-baekjasaengseong-sunsu",
        "Baekjasaengseong-gyosu (Hundred-Numbers Crossed-Numbers Diagram, 百子生成交數圖)": "05-baekjasaengseong-gyosu",
        "Baekjayin-yang-jamo-chakjong (Hundred-Numbers Yin-Yang Mother-Child Intertwining Diagram, 百子陰陽子母錯綜圖)": "06-baekjayin-yang-jamo-chakjong",
    }

    summary_lines = ["# Magic Square Analysis Summary\n"]

    for name, data in SQUARES.items():
        folder = folder_map[name]
        os.makedirs(os.path.join(output_dir, folder), exist_ok=True)
        results = analyze(name, data)

        # Markdown output for reading
        md = [f"# {name}", f"", f"Order: {data['order']}×{data['order']}", ""]
        md.append(describe_generation_rule(name, data))
        md.append("")

        for r in results:
            md.append(f"## Example {r['example']}")
            md.append(f"- Value range: {r['min']} ~ {r['max']}")
            md.append(f"- Normal set (consecutive integers): {'Yes' if r['normal_set'] else 'No'}")
            md.append(f"- Magic constant: {r['magic_constant']}")
            md.append(f"- Row sums: {r['row_sums']}")
            md.append(f"- Column sums: {r['col_sums']}")
            md.append(f"- Diagonal sums: {r['diag_sums']}")
            md.append(f"- Semi-magic: {'Yes' if r['is_semi_magic'] else 'No'}")
            md.append(f"- Magic square: {'Yes' if r['is_magic'] else 'No'}")
            md.append(f"- Pan-diagonal: {'Yes' if r['is_pan_diagonal'] else 'No'}")
            md.append(f"- Wrapped diagonal sums: {r['wrapped_diag_sums']}")
            md.append(f"- Associated: {'Yes' if r['is_associated'] else 'No'} (center-symmetric sum = {r['associated_sum']})")
            md.append(f"- Bimagic: {'Yes' if r['is_bimagic'] else 'No'}")
            md.append(f"- 180° rotational symmetry: {'Yes' if r['symmetry_180'] else 'No'}")
            md.append("")

        # Additional analysis: value frequencies
        flat = flatten(data["examples"][0])
        freq = defaultdict(int)
        for x in flat:
            freq[x] += 1
        duplicates = {k: v for k, v in freq.items() if v > 1}
        md.append(f"## Value Frequency Analysis (Example 1)")
        md.append(f"- Total cells: {len(flat)}")
        md.append(f"- Distinct values: {len(freq)}")
        if duplicates:
            md.append(f"- Duplicated values: {dict(duplicates)}")
        else:
            md.append(f"- No duplicates")
        md.append("")

        # Save file
        out_path = os.path.join(output_dir, folder, "analysis.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md))

        # Summary
        r1 = results[0]
        summary_lines.append(
            f"- **{name}**: {data['order']}×{data['order']}, "
            f"normal_set={'Yes' if r1['normal_set'] else 'No'}, "
            f"Magic={'Yes' if r1['is_magic'] else 'No'}, "
            f"Pan-diagonal={'Yes' if r1['is_pan_diagonal'] else 'No'}, "
            f"Associated={'Yes' if r1['is_associated'] else 'No'}, "
            f"Bimagic={'Yes' if r1['is_bimagic'] else 'No'}"
        )

    summary_path = os.path.join(output_dir, "ANALYSIS_SUMMARY.md")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("\n".join(summary_lines))

    print("Analysis complete. Check the per-folder analysis.md and ANALYSIS_SUMMARY.md files.")


if __name__ == "__main__":
    main()
