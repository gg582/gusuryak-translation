"""《구수략》 방진 심층 연구: 성질 계산과 마방진 계열 대조.

squares.py의 전사본을 읽어 각 방진의 성질을 계산하고 properties.md를 쓴다.
README.md의 해설은 이 스크립트가 확인한 사실만 인용한다.
"""
import os
import itertools
from collections import Counter

import numpy as np

import squares as S

LANG = "ko"
HERE = os.path.dirname(os.path.abspath(__file__))

NAMES = {
    "ko": {
        "NAKSEO": "낙서(洛書)", "SASA_YANG": "사사도 양수도", "SASA_EUM": "사사도 음수도",
        "OO_YANG": "오오도 양수도", "OO_EUM": "오오도 음수도",
        "YUKYUK_1": "육육도 예시 1", "YUKYUK_2": "육육도 예시 2",
        "HAENG_YANG": "행수도 양수도", "HAENG_EUM": "행수도 음수도",
        "YEOK_YANG": "역수도 양수도", "YEOK_EUM": "역수도 음수도",
        "GUSU": "구수도", "GUSU_EUM": "구수음도",
        "JASU_YANG": "구구자수변궁양도", "JASU_EUM": "구구자수변궁음도",
        "BAEKJA_ORIG": "백자도 원본", "BAEKJA_ALT": "백자도 대안 재배열", "BAEKJA_HONG": "백자도 재배열(홍정하)",
        "JAMO_ORIG": "백자음양자모착종도 원본", "JAMO_CORR": "백자음양자모착종도 교정본",
        "MOSU_YANG": "구구모수변궁양도", "MOSU_EUM": "구구모수변궁음도",
        "SUNSU": "백자생성순수도", "GYOSU": "백자생성교수도",
        "BAEKJA_PAIR": "백자자수·모수음양착종도",
    },
    "en": {
        "NAKSEO": "Lo Shu (洛書)", "SASA_YANG": "Sasado yang", "SASA_EUM": "Sasado yin",
        "OO_YANG": "Oodo yang", "OO_EUM": "Oodo yin",
        "YUKYUK_1": "Yukyukdo example 1", "YUKYUK_2": "Yukyukdo example 2",
        "HAENG_YANG": "Haengsudo yang", "HAENG_EUM": "Haengsudo yin",
        "YEOK_YANG": "Yeoksudo yang", "YEOK_EUM": "Yeoksudo yin",
        "GUSU": "Gusudo", "GUSU_EUM": "Gusu yin diagram",
        "JASU_YANG": "Gugujasu Byeongung yang", "JASU_EUM": "Gugujasu Byeongung yin",
        "BAEKJA_ORIG": "Baekjado original", "BAEKJA_ALT": "Baekjado alternative rearrangement",
        "BAEKJA_HONG": "Baekjado rearrangement (Hong Jeong-ha)",
        "JAMO_ORIG": "Baekja Eumyang Jamo Chakjongdo original", "JAMO_CORR": "Baekja Eumyang Jamo Chakjongdo corrected",
        "MOSU_YANG": "Gugumosu Byeongung yang", "MOSU_EUM": "Gugumosu Byeongung yin",
        "SUNSU": "Baekja Saengseong Sunsudo", "GYOSU": "Baekja Saengseong Gyosudo",
        "BAEKJA_PAIR": "Baekja child/parent Eumyang Chakjongdo",
    },
}[LANG]

NUMBER_SQUARES = ["NAKSEO", "SASA_YANG", "SASA_EUM", "OO_YANG", "OO_EUM", "YUKYUK_1", "YUKYUK_2",
                  "HAENG_YANG", "HAENG_EUM", "YEOK_YANG", "YEOK_EUM", "GUSU", "GUSU_EUM",
                  "JASU_YANG", "JASU_EUM", "BAEKJA_ORIG", "BAEKJA_ALT", "BAEKJA_HONG", "JAMO_ORIG", "JAMO_CORR"]

# Reference squares from the wider magic-square tradition
DURER = np.array([[16, 3, 2, 13], [5, 10, 11, 8], [9, 6, 7, 12], [4, 15, 14, 1]])
AGRIPPA_JUPITER = np.array([[4, 14, 15, 1], [9, 7, 6, 12], [5, 11, 10, 8], [16, 2, 3, 13]])


def arr(key):
    return np.array(getattr(S, key))


def line_sums(A):
    n = len(A)
    return list(A.sum(1)), list(A.sum(0)), int(np.trace(A)), int(np.trace(np.fliplr(A)))


def d4(A):
    out = []
    for k in range(4):
        R = np.rot90(A, k)
        out += [R, np.fliplr(R)]
    return out


def is_magic_block(B):
    r, c, d, a = line_sums(B)
    return len(set(r) | set(c) | {d, a}) == 1


def is_semi_block(B):
    r, c, _, _ = line_sums(B)
    return len(set(r) | set(c)) == 1


def properties(A):
    n = len(A)
    lo, hi = int(A.min()), int(A.max())
    r, c, d, a = line_sums(A)
    semi = len(set(r) | set(c)) == 1
    magic = semi and d == a == r[0]
    normal = sorted(A.flatten()) == list(range(lo, lo + n * n))
    pair_sum = lo + hi
    assoc = all(A[i, j] + A[n - 1 - i, n - 1 - j] == pair_sum for i in range(n) for j in range(n))
    broken = {int(sum(A[i, (i + s) % n] for i in range(n))) for s in range(n)}
    broken |= {int(sum(A[i, (s - i) % n] for i in range(n))) for s in range(n)}
    pan = magic and len(broken) == 1
    B = A.astype(np.int64) ** 2
    rb, cb, db, ab = line_sums(B)
    bimagic = len(set(rb) | set(cb) | {db, ab}) == 1
    compact = len({int(A[i:i + 2, j:j + 2].sum()) for i in range(n - 1) for j in range(n - 1)}) == 1
    inner = [m for m in range(n - 2, 2, -1) if (n - m) % 2 == 0
             and is_magic_block(A[(n - m) // 2:(n + m) // 2, (n - m) // 2:(n + m) // 2])]
    blocks = None
    if n == 9:
        bs = [A[3 * i:3 * i + 3, 3 * j:3 * j + 3] for i in range(3) for j in range(3)]
        blocks = "magic" if all(map(is_magic_block, bs)) else "semi" if all(map(is_semi_block, bs)) else "-"
    return dict(n=n, lo=lo, hi=hi, normal=normal, const=int(A.sum() // n), semi=semi, magic=magic,
                diag=(d, a), assoc=assoc, pan=pan, bimagic=bimagic, compact=compact, inner=inner, blocks=blocks)


def complement_geometry(A):
    n = len(A)
    lo, hi = int(A.min()), int(A.max())
    pos = {int(A[i, j]): (i, j) for i in range(n) for j in range(n)}
    kinds = Counter()
    for v in range(lo, (lo + hi + 1) // 2):
        (i1, j1), (i2, j2) = pos[v], pos[lo + hi - v]
        if (i2, j2) == (n - 1 - i1, n - 1 - j1):
            kinds["center"] += 1
        elif i1 == i2 and j2 == n - 1 - j1:
            kinds["row-mirror"] += 1
        elif j1 == j2 and i2 == n - 1 - i1:
            kinds["col-mirror"] += 1
        else:
            kinds["other"] += 1
    return dict(kinds)


def same_lines(A, B):
    rows = lambda X: sorted(tuple(sorted(int(x) for x in r)) for r in X)
    return rows(A) == rows(B) and rows(A.T) == rows(B.T)


def relation(A, B):
    """How B relates to A: D4 image, complement, or the same row and column sets."""
    comp = A.min() + A.max() - A
    Bs = B - B.min() + A.min()
    for tag, X in (("same", A), ("complement", comp)):
        if any((T == Bs).all() for T in d4(X)):
            return f"D4-{tag}"
    for tag, X in (("same", A), ("complement", comp)):
        if any(same_lines(T, Bs) for T in d4(X)):
            return f"lines-{tag}"
    return "none"


def siamese(n):
    """De la Loubère's Siamese construction for odd n."""
    A = np.zeros((n, n), int)
    i, j = 0, n // 2
    for k in range(1, n * n + 1):
        A[i, j] = k
        ni, nj = (i - 1) % n, (j + 1) % n
        if A[ni, nj]:
            ni, nj = (i + 1) % n, j
        i, j = ni, nj
    return A


def yukyuk_affine_maps():
    """Affine position maps p -> Mp + b (mod 6), with or without 37 - v, sending example 1 to example 2."""
    Y1, Y2 = arr("YUKYUK_1"), arr("YUKYUK_2")
    pos2 = {int(Y2[r, c]): (r, c) for r in range(6) for c in range(6)}
    found = []
    for a, b, c, d, e, f in itertools.product(range(6), repeat=6):
        for comp in (False, True):
            if all(pos2[37 - int(Y1[r, s]) if comp else int(Y1[r, s])] == ((a * r + b * s + e) % 6, (c * r + d * s + f) % 6)
                   for r in range(6) for s in range(6)):
                found.append((a, b, c, d, e, f, comp))
    return found


def pair_arrays(key):
    M = getattr(S, key)
    a = np.array([[p[0] for p in row] for row in M])
    b = np.array([[p[1] for p in row] for row in M])
    return a, b


def latin(X):
    n = len(X)
    return all(len(set(X[i])) == n for i in range(n)) and all(len(set(X[:, j])) == n for j in range(n))


def pair_properties(a, b):
    n = len(a)
    counts = Counter(Counter(zip(a.flatten(), b.flatten())).values())
    box = None
    if n == 9:
        box = all(len(set(X[3 * i:3 * i + 3, 3 * j:3 * j + 3].flatten())) == 9
                  for X in (a, b) for i in range(3) for j in range(3))
    sym180 = all((a[i, j], b[i, j]) == (a[n - 1 - i, n - 1 - j], b[n - 1 - i, n - 1 - j])
                 for i in range(n) for j in range(n))
    return dict(latin=(latin(a), latin(b)), counts=dict(counts), box=box, sym180=sym180,
                line_sum=sorted({int(x) for x in (a + b).sum(1)} | {int(x) for x in (a + b).sum(0)}))


def verify_findings():
    """Checks behind every claim in README.md; raises if a transcription changes."""
    F = {}
    natural = np.arange(1, 17).reshape(4, 4)
    natdiag = natural.copy()
    for i in range(4):
        natdiag[i, i] = 17 - natural[i, i]
        natdiag[i, 3 - i] = 17 - natural[i, 3 - i]
    F["sasa_eum_is_natural_diagonal_complement"] = any((T == arr("SASA_EUM")).all() for T in d4(natdiag))
    F["sasa_eum_is_agrippa_jupiter"] = any((T == arr("SASA_EUM")).all() for T in d4(AGRIPPA_JUPITER))
    F["sasa_yang_lines_of_durer"] = relation(DURER, arr("SASA_YANG")).startswith("lines")
    F["sasa_yang_eum_same_lines"] = relation(arr("SASA_YANG"), arr("SASA_EUM")) == "lines-same"
    for y, e in (("OO_YANG", "OO_EUM"), ("YUKYUK_1", "YUKYUK_2"), ("HAENG_YANG", "HAENG_EUM"),
                 ("YEOK_YANG", "YEOK_EUM"), ("GUSU", "GUSU_EUM")):
        F[f"{y}_{e}_unrelated"] = relation(arr(y), arr(e)) == "none"
    Y = arr("YEOK_YANG")
    F["yeok_yang_dominoes_65"] = {int(Y[i, 2 * j] + Y[i, 2 * j + 1]) for i in range(8) for j in range(4)} == {65}
    F["yeok_yang_half_rows_130"] = {int(Y[i, :4].sum()) for i in range(8)} | {int(Y[i, 4:].sum()) for i in range(8)} == {130}
    E = arr("YEOK_EUM")
    F["yeok_eum_half_lines_130"] = ({int(E[i, :4].sum()) for i in range(8)} | {int(E[i, 4:].sum()) for i in range(8)}
                                    | {int(E[:4, j].sum()) for j in range(8)} | {int(E[4:, j].sum()) for j in range(8)}) == {130}
    F["yeok_quadrants_520"] = all(int(X[a:a + 4, b:b + 4].sum()) == 520 for X in (Y, E) for a in (0, 4) for b in (0, 4))
    O = arr("BAEKJA_ORIG")
    F["baekja_orig_compact_202"] = {int(O[i:i + 2, j:j + 2].sum()) for i in range(9) for j in range(9)} == {202}
    F["baekja_orig_wrapped_compact_202"] = {int(O[i, j] + O[i, (j + 1) % 10] + O[(i + 1) % 10, j] + O[(i + 1) % 10, (j + 1) % 10])
                                            for i in range(10) for j in range(10)} == {202}
    F["baekja_alt_loses_compact"] = not properties(arr("BAEKJA_ALT"))["compact"]
    G = arr("GUSU_EUM")
    q, r = (G - 1) // 9, (G - 1) % 9
    F["gusu_eum_digits_box_complete"] = all(sorted(X[3 * i:3 * i + 3, 3 * j:3 * j + 3].flatten()) == list(range(9))
                                            for X in (q, r) for i in range(3) for j in range(3))
    F["gusu_eum_digit_lines_36"] = {int(x) for X in (q, r) for x in list(X.sum(0)) + list(X.sum(1))} == {36}
    a, b = pair_arrays("MOSU_YANG")
    comp = 9 * (a - 1) + b
    F["mosu_yang_composite_magic"] = properties(comp)["magic"] and properties(comp)["normal"]
    F["mosu_yang_diagonal_rule"] = (set(np.diag(a)) == {5} and sorted(np.diag(np.fliplr(a))) == list(range(1, 10))
                                    and sorted(np.diag(b)) == list(range(1, 10)) and set(np.diag(np.fliplr(b))) == {5})
    F["mosu_yang_composite_not_gusu"] = not any((T == arr("GUSU")).all() for T in d4(comp))
    ja, mo = arr("BAEKJA_JASU"), arr("BAEKJA_MOSU")
    F["baekja_pair_dependent"] = (ja == np.where(mo == 0, 10, 10 - mo)).all()
    F["baekja_pair_10_pairs"] = len(set(zip(ja.flatten(), mo.flatten()))) == 10
    F["yin_squares_associative"] = all(properties(arr(k))["assoc"] for k in ("SASA_YANG", "SASA_EUM", "OO_EUM", "HAENG_EUM", "YEOK_EUM"))
    F["yang_squares_not_associative"] = not any(properties(arr(k))["assoc"] for k in ("OO_YANG", "HAENG_YANG", "YEOK_YANG"))
    F["oo_haeng_yang_central_3x3"] = properties(arr("OO_YANG"))["inner"] == [3] and properties(arr("HAENG_YANG"))["inner"] == [3]
    F["yeok_eum_central_4x4"] = 4 in properties(arr("YEOK_EUM"))["inner"]
    F["yukyuk_not_assoc_not_pan"] = not any(properties(arr(k))[p] for k in ("YUKYUK_1", "YUKYUK_2") for p in ("assoc", "pan"))
    L = arr("NAKSEO")
    gs = np.array([[int(arr("GUSU")[3 * i:3 * i + 3, 3 * j:3 * j + 3].sum()) for j in range(3)] for i in range(3)])
    F["gusu_block_sums_are_lo_shu"] = (gs == 9 * L + 324).all()
    F["jamo_correction_restores_row_mirror"] = (complement_geometry(arr("JAMO_ORIG")).get("row-mirror") == 48
                                                and complement_geometry(arr("JAMO_CORR")).get("row-mirror") == 50)
    F["baekja_orig_two_broken_diagonal_sums"] = len({int(sum(O[i, (i + s) % 10] for i in range(10))) for s in range(10)}
                                                     | {int(sum(O[i, (s - i) % 10] for i in range(10))) for s in range(10)}) == 2
    F["yukyuk_no_affine_map"] = not yukyuk_affine_maps()
    F["oo_not_siamese"] = all(relation(siamese(5), arr(k)) == "none" for k in ("OO_YANG", "OO_EUM"))
    for k, v in F.items():
        assert v, k
    return F


BLOCKS = {"ko": {"magic": "모두 마방진", "semi": "모두 준마방진"}, "en": {"magic": "all magic", "semi": "all semi-magic"}}


def yn(x):
    return {"ko": {True: "예", False: "아니오"}, "en": {True: "yes", False: "no"}}[LANG][bool(x)]


def write_properties():
    T = {
        "ko": dict(title="# 방진별 성질 표 (자동 생성)", note="`deep_study.py`가 `squares.py`의 전사본에서 계산한 값이다.",
                   head="| 도 | 차수 | 수 범위 | 상수 | 준마방진 | 마방진 | 대각선 합 | 대칭형 | 범대각 | 이중 | 2×2 균일 | 가운데 마방진 | 3×3 궁 |",
                   pairs="## 보수쌍의 위치", pairs_head="| 도 | 중심 대칭 | 행 거울 | 열 거울 | 기타 |",
                   rel="## 양·음 짝의 관계", rel_head="| 짝 | 관계 |",
                   pair_t="## 순서쌍 방진", pair_head="| 도 | 성분 라틴 | 순서쌍 출현 | 궁 완비 | 180° 대칭 | 줄마다 a+b 합 |",
                   rel_names={"none": "회전·반사·보수·행열 재배치로 옮겨지지 않음",
                              "lines-same": "같은 행 집합·열 집합(행·열 재배치 관계)"}),
        "en": dict(title="# Property table (generated)", note="Values computed by `deep_study.py` from the transcriptions in `squares.py`.",
                   head="| Diagram | Order | Range | Constant | Semi-magic | Magic | Diagonals | Associative | Pandiagonal | Bimagic | Uniform 2×2 | Central magic | 3×3 palaces |",
                   pairs="## Position of complementary pairs", pairs_head="| Diagram | Centre | Row mirror | Column mirror | Other |",
                   rel="## Relation between yang and yin partners", rel_head="| Pair | Relation |",
                   pair_t="## Ordered-pair squares", pair_head="| Diagram | Components Latin | Pair occurrences | Palaces complete | 180° symmetry | a+b per line |",
                   rel_names={"none": "not reached by rotation, reflection, complement, or row/column rearrangement",
                              "lines-same": "same row and column sets (a row/column rearrangement)"}),
    }[LANG]
    out = [T["title"], "", T["note"], "", T["head"], "|" + " --- |" * 13]
    for k in NUMBER_SQUARES:
        p = properties(arr(k))
        inner = ", ".join(f"{m}×{m}" for m in p["inner"]) or "-"
        out.append(f"| {NAMES[k]} | {p['n']} | {p['lo']}–{p['hi']} | {p['const']} | {yn(p['semi'])} | {yn(p['magic'])} | "
                   f"{p['diag'][0]}, {p['diag'][1]} | {yn(p['assoc'])} | {yn(p['pan'])} | {yn(p['bimagic'])} | "
                   f"{yn(p['compact'])} | {inner} | {BLOCKS[LANG].get(p['blocks'], '-')} |")
    out += ["", T["pairs"], "", T["pairs_head"], "| --- | ---: | ---: | ---: | ---: |"]
    for k in NUMBER_SQUARES:
        if not properties(arr(k))["normal"]:
            continue
        g = complement_geometry(arr(k))
        out.append(f"| {NAMES[k]} | {g.get('center', 0)} | {g.get('row-mirror', 0)} | {g.get('col-mirror', 0)} | {g.get('other', 0)} |")
    out += ["", T["rel"], "", T["rel_head"], "| --- | --- |"]
    for y, e in (("SASA_YANG", "SASA_EUM"), ("OO_YANG", "OO_EUM"), ("YUKYUK_1", "YUKYUK_2"),
                 ("HAENG_YANG", "HAENG_EUM"), ("YEOK_YANG", "YEOK_EUM"), ("GUSU", "GUSU_EUM")):
        out.append(f"| {NAMES[y]} → {NAMES[e]} | {T['rel_names'][relation(arr(y), arr(e))]} |")
    out += ["", T["pair_t"], "", T["pair_head"], "| --- | --- | --- | --- | --- | --- |"]
    rows = [(k, *pair_arrays(k)) for k in ("MOSU_YANG", "MOSU_EUM", "SUNSU", "GYOSU")]
    rows.append(("BAEKJA_PAIR", arr("BAEKJA_JASU"), arr("BAEKJA_MOSU")))
    for k, a, b in rows:
        if k == "GYOSU":
            b = np.where(b == 0, 10, b)
        p = pair_properties(a, b)
        counts = ", ".join(f"{c}×{t}" for t, c in sorted(p["counts"].items()))
        out.append(f"| {NAMES[k]} | {yn(p['latin'][0])}, {yn(p['latin'][1])} | {counts} | "
                   f"{'-' if p['box'] is None else yn(p['box'])} | {yn(p['sym180'])} | {', '.join(map(str, p['line_sum']))} |")
    with open(os.path.join(HERE, "properties.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


if __name__ == "__main__":
    findings = verify_findings()
    write_properties()
    print(f"{len(findings)} findings verified; properties.md written")
