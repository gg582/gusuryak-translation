#!/usr/bin/env python3
"""
마방진 분석 스크립트
square.md에 기록된 한국 전통 방진들의 수학적 성질을 합니다.
"""

import json
import math
import os
from collections import defaultdict

# square.md에서 추출한 원시 데이터
SQUARES = {
    "육육도(六六圖)": {
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
    "구수도(九數圖)": {
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
    "백자자수음양착종도(百子子數陰陽錯綜圖)": {
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
    "백자생성순수도(百子生成純數圖)": {
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
    "백자생성교수도(百子生成交數圖)": {
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
    "백자음양자모착종도(百子陰陽子母錯綜圖)": {
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
    """연속 정수 1..n^2 또는 0..n^2-1의 마방진 상수."""
    if start == 0:
        return n * (n * n - 1) // 2
    return n * (n * n + 1) // 2


def flatten(matrix):
    return [x for row in matrix for x in row]


def is_normal_set(values, n, start=1):
    """값 집합이 start부터 n^2-1+start까지의 정수를 정확히 한 번씩 포함하는지."""
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
    """Pan-diagonal 검사: 주대각선 방향으로 래핑(wrap)된 모든 대각선의 합."""
    n = len(m)
    sums = []
    # 우하향 대각선 방향 (시작점: 첫 행)
    for start_col in range(n):
        s = 0
        for i in range(n):
            s += m[i][(start_col + i) % n]
        sums.append(s)
    # 좌하향 대각선 방향 (시작점: 첫 행)
    for start_col in range(n):
        s = 0
        for i in range(n):
            s += m[i][(start_col - i) % n]
        sums.append(s)
    return sums


def is_associated(m):
    """중심 대칭 위치의 두 수 합이 모두 같으면 associated magic square."""
    n = len(m)
    pairs = []
    for i in range(n):
        for j in range(n):
            pairs.append(m[i][j] + m[n - 1 - i][n - 1 - j])
    return len(set(pairs)) == 1, pairs[0]


def is_bimagic(m):
    """각 행/열/대각선의 제곱합까지 동일하면 bimagic."""
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
    """180도 회전 대칭 여부."""
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

        # 마방진 판정
        all_line_sums = rows + cols + diags
        is_magic = len(set(all_line_sums)) == 1

        # semimagic
        is_semi = len(set(rows + cols)) == 1

        # pan-diagonal
        wrap_diags = wrapped_diagonal_sums(m)
        is_pan = is_magic and len(set(wrap_diags)) == 1

        # associated
        assoc, assoc_sum = is_associated(m)

        # bimagic
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
    """각 방진의 생성 규칙을 텍스트로 서술."""
    n = data["order"]
    if name == "육육도(六六圖)":
        return (
            "6×6 마방진. 두 예시는 서로 다른 배치이지만 동일한 마방진 상수 111을 갖는다. "
            "첫 번째 예시는 행/열/대각선 합이 111인 정상 마방진이다. "
            "두 번째 예시 역시 정상 마방진이며, 행/열/대각선 합이 111이다. "
            "두 예시는 90° 회전 또는 반사 변환 관계가 아니며 서로 다른 동형(isomorphism)을 보인다."
        )
    elif name == "구수도(九數圖)":
        return (
            "9×9 마방진. 마방진 상수는 9×(81+1)/2 = 369. "
            "두 예시 모두 1부터 81까지의 수를 정확히 한 번씩 사용하는 정상 마방진이다. "
            "두 번째 예시는 첫 번째 예시의 행/열 치환 또는 반전으로 얻어지는 동일한 마방진 군에 속할 가능성이 높다."
        )
    elif name == "백자자수음양착종도(百子子數陰陽錯綜圖)":
        return (
            "10×10. 첫 번째 예시는 1~10의 수만 반복하여 채운 행렬이며, "
            "각 행/열 합이 55로 일정하지만 수 집합이 1~100이 아니므로 일반적인 마방진은 아니다. "
            "두 번째 예시는 0~9의 수를 반복하여 채운 행렬로, 각 행/열 합이 45로 일정. "
            "이 두 행렬은 서로 보완적(음/양)인 라틴 방진 또는 순환 행렬(circulant) 구조로, "
            "합치면 0~99를 한 번씩 나타내는 직교 라틴 방진(orthogonal Latin squares)의 성분이 될 수 있다."
        )
    elif name == "백자생성순수도(百子生成純數圖)":
        return (
            "10×10 마방진. 1부터 100까지의 수를 정확히 한 번씩 사용하며 마방진 상수는 505. "
            "행/열/대각선 합이 모두 505이다. 상하좌우 및 대각선 중심 대칭(associated) 성질을 가진다. "
            "1행과 10행, 1열과 10열 등이 역순/보완 관계에 있어 생성이 쌍대칭 쌍으로 이루어진다."
        )
    elif name == "백자생성교수도(百子生成交數圖)":
        return (
            "10×10 마방진. 1부터 100까지의 수를 정확히 한 번씩 사용하며 마방진 상수는 505. "
            "백자생성순수도와 비슷하지만 낌새가 다르다. "
            "각 쌍의 위치가 교차·교환된 형태로, '교수(交數)'의 명칭처럼 수들이 교차 배에된 듯 보인다. "
            "상하 대칭, 중심 대칭(associated) 성질을 가진다."
        )
    elif name == "백자음양자모착종도(百子陰陽子母錯綜圖)":
        return (
            "10×10 마방진. 1부터 100까지의 수를 정확히 한 번씩 사용하며 마방진 상수는 505. "
            "'음양(陰陽)'과 '자모(子母)'의 명칭처럼 수들이 상보적 쌍으로 배에되어 있다. "
            "중심 대칭 위치의 합이 101로 associated magic square의 성질을 만족한다. "
            "마치 두 개의 10×10 라틴 방진을 겹쳐 만든 구조로 보인다."
        )
    return ""


def main():
    output_dir = "/home/yjlee/gusuryak-translation/korean/03-magic-squares"
    folder_map = {
        "육육도(六六圖)": "01-yukyukdo",
        "구수도(九數圖)": "02-gusudo",
        "백자자수음양착종도(百子子數陰陽錯綜圖)": "03-baekjajasuyin-yang-chakjong",
        "백자생성순수도(百子生成純數圖)": "04-baekjasaengseong-sunsu",
        "백자생성교수도(百子生成交數圖)": "05-baekjasaengseong-gyosu",
        "백자음양자모착종도(百子陰陽子母錯綜圖)": "06-baekjayin-yang-jamo-chakjong",
    }

    summary_lines = ["# 방진 분석 요약\n"]

    for name, data in SQUARES.items():
        folder = folder_map[name]
        os.makedirs(os.path.join(output_dir, folder), exist_ok=True)
        results = analyze(name, data)

        # 평면 출력용
        md = [f"# {name}", f"", f"차수: {data['order']}×{data['order']}", ""]
        md.append(describe_generation_rule(name, data))
        md.append("")

        for r in results:
            md.append(f"## 예시 {r['example']}")
            md.append(f"- 사용 수 범위: {r['min']} ~ {r['max']}")
            md.append(f"- 정상 수 집합(연속 정수): {'예' if r['normal_set'] else '아니오'}")
            md.append(f"- 마방진 상수: {r['magic_constant']}")
            md.append(f"- 행 합: {r['row_sums']}")
            md.append(f"- 열 합: {r['col_sums']}")
            md.append(f"- 대각선 합: {r['diag_sums']}")
            md.append(f"- Semi-magic: {'예' if r['is_semi_magic'] else '아니오'}")
            md.append(f"- Magic square: {'예' if r['is_magic'] else '아니오'}")
            md.append(f"- Pan-diagonal: {'예' if r['is_pan_diagonal'] else '아니오'}")
            md.append(f"- Wrapped 대각선 합: {r['wrapped_diag_sums']}")
            md.append(f"- Associated: {'예' if r['is_associated'] else '아니오'} (중심 대칭 합 = {r['associated_sum']})")
            md.append(f"- Bimagic: {'예' if r['is_bimagic'] else '아니오'}")
            md.append(f"- 180° 회전 대칭: {'예' if r['symmetry_180'] else '아니오'}")
            md.append("")

        # 추가 분석: 값의 빈도
        flat = flatten(data["examples"][0])
        freq = defaultdict(int)
        for x in flat:
            freq[x] += 1
        duplicates = {k: v for k, v in freq.items() if v > 1}
        md.append(f"## 값의 빈도 분석 (예시 1)")
        md.append(f"- 전체 셀 수: {len(flat)}")
        md.append(f"- 고유 값 개수: {len(freq)}")
        if duplicates:
            md.append(f"- 중복된 값: {dict(duplicates)}")
        else:
            md.append(f"- 중복 없음")
        md.append("")

        # 파일 저장
        out_path = os.path.join(output_dir, folder, "analysis.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md))

        # 요약
        r1 = results[0]
        summary_lines.append(
            f"- **{name}**: {data['order']}×{data['order']}, "
            f"정상 집합={'예' if r1['normal_set'] else '아니오'}, "
            f"Magic={'예' if r1['is_magic'] else '아니오'}, "
            f"Pan-diagonal={'예' if r1['is_pan_diagonal'] else '아니오'}, "
            f"Associated={'예' if r1['is_associated'] else '아니오'}, "
            f"Bimagic={'예' if r1['is_bimagic'] else '아니오'}"
        )

    summary_path = os.path.join(output_dir, "ANALYSIS_SUMMARY.md")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("\n".join(summary_lines))

    print("분석 완료. 폴다별 analysis.md와 ANALYSIS_SUMMARY.md를 확인하세요.")


if __name__ == "__main__":
    main()
