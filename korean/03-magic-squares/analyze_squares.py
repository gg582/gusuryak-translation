#!/usr/bin/env python3
"""
마방진 분석 스크립트
square.md에 기록된 한국 전통 방진들의 수학적 성질을 합니다.
"""

import json
import math
import os
from collections import defaultdict

# square.md에서 데이터를 동적으로 파싱
def parse_squares_from_md(md_path):
    import re
    if not os.path.exists(md_path):
        return {}
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 0## 또는 ## 등으로 시작하는 섹션 분리
    sections = re.split(r'\n(?=0?##\s+)', content)
    parsed = {}
    for sec in sections:
        if not sec.strip():
            continue
        lines = sec.strip().split('\n')
        # 첫 번째 라인에서 0## 또는 ## 제거하고 제목 추출
        title_line = lines[0].strip()
        title_match = re.match(r'^(?:0?##\s*)([^\n]+)', title_line)
        if not title_match:
            continue
        name = title_match.group(1).strip()
        
        # 코드 블록 추출
        code_blocks = re.findall(r'```\s*\n(.*?)\n```', sec, re.DOTALL)
        examples = []
        for block in code_blocks:
            matrix = []
            for row_line in block.strip().split('\n'):
                # 주석 라인이나 빈 라인 무시
                if not row_line.strip() or row_line.strip().startswith('*'):
                    continue
                try:
                    row = [int(x) for x in row_line.split()]
                    if row:
                        matrix.append(row)
                except ValueError:
                    continue
            if matrix:
                examples.append(matrix)
        
        if examples:
            order = len(examples[0])
            parsed[name] = {
                "order": order,
                "examples": examples
            }
    return parsed

SQUARES = parse_squares_from_md("/home/yjlee/gusuryak-translation/korean/03-magic-squares/square.md")


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


def parse_matrix_from_md(md_path):
    """corrected.md 등에서 단일 행렬 데이터를 파싱"""
    import re
    if not os.path.exists(md_path):
        return None
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    code_blocks = re.findall(r'```\s*\n(.*?)\n```', content, re.DOTALL)
    if not code_blocks:
        return None
    
    matrix = []
    for row_line in code_blocks[0].strip().split('\n'):
        if not row_line.strip() or row_line.strip().startswith('*'):
            continue
        try:
            row = [int(x) for x in row_line.split()]
            if row:
                matrix.append(row)
        except ValueError:
            continue
    return matrix if matrix else None


def compare_matrices(orig, corr):
    """원본과 교정본을 비교하여 차이점을 분석 리포트로 작성"""
    if not orig or not corr:
        return ""
    if len(orig) != len(corr) or len(orig[0]) != len(corr[0]):
        return "\n> [!WARNING]\n> 원본 배열과 교정본 배열의 차수가 달라 비교할 수 없습니다.\n"
    
    n = len(orig)
    diffs = []
    for i in range(n):
        for j in range(n):
            if orig[i][j] != corr[i][j]:
                diffs.append({
                    "row": i + 1,
                    "col": j + 1,
                    "orig_val": orig[i][j],
                    "corr_val": corr[i][j]
                })
                
    md = ["## 원본 필사본과 교정본 비교 분석", ""]
    
    if not diffs:
        md.append("- **원본 필사본과 교정본이 완벽히 일치합니다.** 문헌 원본에 수리적 오류가 없거나 필사 과정의 오류가 모두 해결된 상태입니다.")
        md.append("")
        return "\n".join(md)
        
    md.append(f"- **총 수리적 오류(불일치 셀) 수**: {len(diffs)}개")
    md.append("")
    md.append("| 좌표 (행, 열) | 원본 필사본 값 | 교정본 값 | 수치 오차 (교정본 - 원본) |")
    md.append("| :---: | :---: | :---: | :---: |")
    for d in diffs:
        diff_val = d["corr_val"] - d["orig_val"]
        sign = "+" if diff_val > 0 else ""
        md.append(f"| ({d['row']}행, {d['col']}열) | {d['orig_val']} | {d['corr_val']} | {sign}{diff_val} |")
    
    md.append("")
    md.append("### 오류 원인 및 수리적 영향 분석")
    
    from collections import Counter
    orig_flat = [x for row in orig for x in row]
    corr_flat = [x for row in corr for x in row]
    
    orig_counter = Counter(orig_flat)
    
    # 0부터 시작하는지, 1부터 시작하는지 판단
    start_val = min(corr_flat)
    expected_set = set(range(start_val, start_val + n*n))
    
    missing = sorted(list(expected_set - set(orig_flat)))
    duplicates = sorted([k for k, v in orig_counter.items() if v > 1])
    
    if missing:
        md.append(f"- **원본에서 누락된 수(수치 결함)**: {missing}")
    if duplicates:
        dup_details = {k: orig_counter[k] for k in duplicates}
        md.append(f"- **원본에서 중복된 수**: {dup_details}")
        
    md.append("- **행/열 합의 오차 분석**:")
    orig_rows = [sum(row) for row in orig]
    orig_cols = [sum(orig[i][j] for i in range(n)) for j in range(n)]
    corr_target = sum(corr[0]) # 교정본 상수
    
    bad_rows = [(i+1, orig_rows[i], orig_rows[i] - corr_target) for i in range(n) if orig_rows[i] != corr_target]
    bad_cols = [(j+1, orig_cols[j], orig_cols[j] - corr_target) for j in range(n) if orig_cols[j] != corr_target]
    
    if bad_rows:
        md.append("  - **원본 행 합 오차** (목표 합: " + str(corr_target) + "):")
        for r_num, s_val, err in bad_rows:
            sign = "+" if err > 0 else ""
            md.append(f"    - {r_num}행: 합 {s_val} (오차: {sign}{err})")
    else:
        md.append("  - **원본 행 합**: 모든 행의 합이 목표 합 " + str(corr_target) + "을 만족합니다.")
        
    if bad_cols:
        md.append("  - **원본 열 합 오차** (목표 합: " + str(corr_target) + "):")
        for c_num, s_val, err in bad_cols:
            sign = "+" if err > 0 else ""
            md.append(f"    - {c_num}열: 합 {s_val} (오차: {sign}{err})")
    else:
        md.append("  - **원본 열 합**: 모든 열의 합이 목표 합 " + str(corr_target) + "을 만족합니다.")
        
    return "\n".join(md)


def describe_generation_rule(name, data, is_corrected):
    """각 방진의 생성 규칙을 텍스트로 서술."""
    n = data["order"]
    prefix = "[교정본 기준] " if is_corrected else "[원본 기준] "
    
    if name == "육육도(六六圖)":
        return (
            prefix + "6×6 마방진. 두 예시는 서로 다른 배치이지만 동일한 마방진 상수 111을 갖는다. "
            "첫 번째 예시는 행/열/대각선 합이 111인 정상 마방진이다. "
            "두 번째 예시 역시 정상 마방진이며, 행/열/대각선 합이 111이다. "
            "두 예시는 90° 회전 또는 반사 변환 관계가 아니며 서로 다른 동형(isomorphism)을 보인다."
        )
    elif name == "구수도(九數圖)":
        return (
            prefix + "9×9 마방진. 마방진 상수는 9×(81+1)/2 = 369. "
            "두 예시 모두 1부터 81까지의 수를 정확히 한 번씩 사용하는 정상 마방진이다. "
            "두 번째 예시는 첫 번째 예시의 행/열 치환 또는 반전으로 얻어지는 동일한 마방진 군에 속할 가능성이 높다."
        )
    elif name == "백자자수음양착종도(百子子數陰陽錯綜圖)":
        if is_corrected:
            return (
                prefix + "10×10 마방진 교정본. 1부터 100까지의 수를 정확히 한 번씩 사용하며, "
                "모든 가로, 세로, 주대각선 및 반대각선의 합이 505를 만족하는 완전한 마방진(Magic Square) 구조이다."
            )
        return (
            prefix + "10×10. 《구수략》 원전에는 이 두 개의 개별 라틴 방진('백자자수음양착종도' 1~10 및 '백자모수음양착종도' 0~9)만 분리 수록되어 있으며, 이들의 합성 방진 자체는 책에 수록되지 않았습니다.\n"
            "최석정은 이 두 방진을 십의 자리(모수)와 일의 자리(자수)로 결합하여 1~100의 마방진을 만드는 **합성 방법(조합 원리)**을 명확하게 제시했습니다. "
            "원전에 제시된 두 방진은 각각 행과 열에 중복이 없는 올바른(옳은) 라틴 방진이며, 비록 이 두 특정 방진 쌍이 수학적으로 완벽히 직교(Orthogonal)하지 않아 직접 합성 시 중복이 발생하지만, "
            "라틴 방진 쌍을 결합하여 고차 방진을 생성하려 한 **조합론적 발견 및 합성 방법론 자체는 매우 정합하고 역사적으로 선구적인 수학적 업적**입니다."
        )
    elif name == "백자생성순수도(百子生成純數圖)":
        if is_corrected:
            return (
                prefix + "10×10 수 배열 교정본. 원본 격자가 내포하고 있는 180도 회전 대칭성(점대칭)을 복구하기 위해 (2행, 3열)의 값 `39`를 `69`로 교정한 버전입니다. 교정 후 가로 및 세로의 모든 행/열 합이 495로 완벽히 일치하여 고유한 점대칭 성질을 온전히 유지합니다."
            )
        return (
            prefix + "10×10 수 배열. 1부터 100까지의 자연수 중 일부의 누락·중복이 있어 정상 마방진이 아니다."
        )
    elif name == "백자생성교수도(百子生成交數圖)":
        if is_corrected:
            return (
                prefix + "10×10 수 배열 교정본. 원본 격자가 내포하고 있는 180도 회전 대칭성을 깨뜨리는 두 위치 `(6행, 1열)`의 `42 -> 52` 및 `(6행, 10열)`의 `49 -> 59`를 점대칭에 맞추어 보정하고, 원전 필사본에 명시된 교정 주석(16 -> 11, 85 -> 86)을 반영한 버전입니다."
            )
        return (
            prefix + "10×10 수 배열. 1부터 100까지의 자연수 중 일부의 누락·중복이 있어 정상 마방진이 아니다."
        )
    elif name == "백자음양자모착종도(百子陰陽子母錯綜圖)":
        if is_corrected:
            return (
                prefix + "10×10 마방진(준마방진) 교정본. 원본의 1~100 수 배열 중에서 단순 필사 오사로 추정되는 5개 셀(2행 Col 3-Col 8 교환 및 5~6행 Col 3-Col 8의 3-cycle 순환 교정)만 정정하여 가로/세로 합이 모두 505인 마방진 조건을 충족하도록 복구한 정합적인 버전입니다."
            )
        return (
            prefix + "10×10 수 배열. 1부터 100까지의 수를 정확히 한 번씩 사용하지만, 행·열·대각선 합이 모두 505인 마방진은 아니다."
        )
    elif name == "백자도(百子圖)":
        if is_corrected:
            return (
                prefix + "10×10 수 배열(준마방진) 교정본. 송나라 수학자 양휘의 백자도 원본에서 코너 부분의 필사 오사(5행~8행의 양쪽 끝 8개 셀)로 인해 행 합과 열 합이 어긋났던 부분을 바로잡아, 모든 가로와 세로의 합이 마방진 상수 505를 정확하게 만족하는 원래의 정합적인 준마방진(Semi-magic) 구조와 십의 자리 대칭 패턴을 복원한 버전입니다."
            )
        return (
            prefix + "10×10 수 배열. 1부터 100까지의 수를 한 번씩 정확하게 사용하지만, 필사 과정의 코너 영역 오사로 인해 일부 행/열의 합이 어긋나 정상적인 준마방진을 만족하지 못한다."
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
        "백자도(百子圖)": "07-baekjado",
    }

    summary_lines = ["# 방진 분석 요약\n"]

    for name, data in SQUARES.items():
        folder = folder_map[name]
        folder_path = os.path.join(output_dir, folder)
        os.makedirs(folder_path, exist_ok=True)
        
        # 교정본(corrected.md) 로드 시도
        corrected_path = os.path.join(folder_path, "corrected.md")
        corrected_matrix = parse_matrix_from_md(corrected_path)
        
        is_corrected = corrected_matrix is not None
        
        # 분석할 데이터 결정: 교정본이 있으면 교정본을 분석 대상으로 삼음
        analysis_data = {
            "order": data["order"],
            "examples": [corrected_matrix] if is_corrected else data["examples"]
        }
        
        results = analyze(name, analysis_data)
        original_matrix = data["examples"][0] # 원본 예시 1

        # 평면 출력용 md 구성
        md = [f"# {name}", f"", f"차수: {data['order']}×{data['order']}", ""]
        md.append(describe_generation_rule(name, analysis_data, is_corrected))
        md.append("")

        for r in results:
            ex_num = r['example']
            label = " (교정본)" if is_corrected else f" {ex_num}"
            md.append(f"## 예시{label}")
            md.append(f"- 사용 수 범위: {r['min']} ~ {r['max']}")
            md.append(f"- 정상 수 집합(연속 정수): {'예' if r['normal_set'] else '아니오'}")
            md.append(f"- 기준 마방진 상수: {r['magic_constant']}")
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

        # 추가 분석: 값의 빈도 (분석 대상 기준)
        target_flat = flatten(analysis_data["examples"][0])
        freq = defaultdict(int)
        for x in target_flat:
            freq[x] += 1
        duplicates = {k: v for k, v in freq.items() if v > 1}
        
        label_freq = " (교정본)" if is_corrected else " (예시 1)"
        md.append(f"## 값의 빈도 분석{label_freq}")
        md.append(f"- 전체 셀 수: {len(target_flat)}")
        md.append(f"- 고유 값 개수: {len(freq)}")
        if duplicates:
            md.append(f"- 중복된 값: {dict(duplicates)}")
        else:
            md.append(f"- 중복 없음")
        md.append("")

        # 원본과의 비교 리포트 섹션 추가 (교정본이 존재할 때만)
        if is_corrected:
            comparison_report = compare_matrices(original_matrix, corrected_matrix)
            md.append(comparison_report)
            md.append("")

        # 파일 저장
        out_path = os.path.join(output_dir, folder, "analysis.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md))

        # 요약 (교정본이 있을 경우 교정본 분석 결과 기준)
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

    print("분석 완료. 폴더별 analysis.md와 ANALYSIS_SUMMARY.md를 확인하세요.")


if __name__ == "__main__":
    main()
