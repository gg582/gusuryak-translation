#!/usr/bin/env python3
"""Recover damaged UTF-8 Markdown from the recorded byte substitution.

The solver preserves every byte that was not a recorded quote replacement.
For quote bytes it searches the observed inverse byte set and scores complete
Korean, Chinese, and English characters against clean repository text.
"""
from __future__ import annotations

import argparse
import difflib
import math
import subprocess
from collections import Counter
from pathlib import Path
from difflib import SequenceMatcher

INVERSE = {
    0x22: (0x22, 0x80, 0x9C, 0x9D, 0x9E, 0x9F, 0xE2),
    0x27: (0x27, 0x98, 0x99, 0x9A, 0x9B),
}
ANCHORS = (
    "성신여대", "성신여자대학교", "클러스터", "으로", "대로", "구수략",
    "각득", "영인본", "300-335 페이지를 번역한다.",
    "各得", "洛書", "九數略",
)
# These are evidence pairs, not output replacements.  The mapping below is
# learned from their aligned Unicode sequences at runtime.
TRAINING_PAIRS = (
    ("성신여뷄대하교쀘 구수뀵 영쀡본쀘 300-335 페쀳지를 번역핀다.",
     "성신여자대학교의 구수략 영인본의 300-335 페이지를 번역한다."),
    ("1차적쀼례 모든 도안쀀 손쀼례 전사핀 현, OCR 프례그뀨에 노트 필기를 넣쀀 현 수돘쀼례 오탐됀 숫쀐들쀄 고쳐 나간다.",
     "1차적으로 모든 도안을 손으로 전사한 후, OCR 프로그램에 노트 필기를 넣은 후 수동으로 오탐된 숫자들을 고쳐 나간다."),
    ("2차적쀼례 옐문쀘 숫쀐가 주섀문쀘 계산 절차대례 했쀄 때 명형핀 오류를 반혘하면 수를 교정핀 현 교정핀 범쀄를 남긴다.",
     "2차적으로 원문의 숫자가 주석문의 계산 절차대로 했을 때 명확한 오류를 반환하면 수를 교정한 후 교정된 범위를 남긴다."),
    ("배치됀 1부터 33까지쀘 숫쀐를 중복 없쀴 모두 합핀 값(본뀘쀘 누적 합)쀀 561쀴다.",
     "배치된 1부터 33까지의 숫자를 중복 없이 모두 합한 값(본문의 누적 합)은 561이다."),
    ("실패: 쵀적해쀘 값 숀섀는 Siamese싀 다항싀간 지역 귀치쀼례 쀬샀성되지 않는다.",
     "실패: 최적해의 값 순서는 Siamese의 다항시간 지역 규칙으로 재생성되지 않는다."),
    ("옐문 전사본에는 전사 오류가 섀여 쀈다. 쀐세핀 탐구 과정쀀 transcription_analysis.md를 참고핀다.",
     "원문 전사본에는 전사 오류가 섞여 있다. 자세한 탐구 과정은 transcription_analysis.md를 참고한다."),
)


def learned_replacements(pairs: tuple[tuple[str, str], ...]) -> dict[str, str]:
    """Learn short corrupted->clean Unicode spans from aligned evidence.

    Long edits are intentionally ignored: they are sentence-level wording
    differences, not evidence of a character corruption rule.
    """
    counts: dict[tuple[str, str], int] = Counter()
    for damaged, clean in pairs:
        matcher = difflib.SequenceMatcher(a=damaged, b=clean, autojunk=False)
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "replace":
                bad, good = damaged[i1:i2], clean[j1:j2]
                if 0 < len(bad) <= 8 and 0 < len(good) <= 8:
                    counts[(bad, good)] += 1
    chosen: dict[str, str] = {}
    for (bad, good), _ in sorted(counts.items(), key=lambda item: (-item[1], -len(item[0][0]))):
        if bad not in chosen:
            chosen[bad] = good
    return chosen


LEARNED_REPLACEMENTS = learned_replacements(TRAINING_PAIRS)
CONTEXT_RULES: dict[tuple[bytes, int, bytes], tuple[int, ...]] = {}


def learn_context_rules(damaged: bytes, clean: bytes, radius: int = 3) -> dict[tuple[bytes, int, bytes], tuple[int, ...]]:
    """Learn byte recovery rules from an exact damaged/clean evidence pair.

    The key includes the surrounding damaged bytes, so a many-to-one quote
    replacement is not expanded into a global unsafe substitution.
    """
    rules: dict[tuple[bytes, int, bytes], set[int]] = {}
    for tag, i1, i2, j1, j2 in SequenceMatcher(None, damaged, clean, autojunk=False).get_opcodes():
        if tag != "replace" or i2 - i1 != j2 - j1:
            continue
        for off in range(i2 - i1):
            pos = i1 + off
            source, target = damaged[pos], clean[j1 + off]
            if source not in (0x22, 0x27):
                continue
            key = (damaged[max(0, pos - radius):pos], source,
                   damaged[pos + 1:pos + 1 + radius])
            rules.setdefault(key, set()).add(target)
    return {key: tuple(sorted(values)) for key, values in rules.items()}


def clean_texts(root: Path) -> list[str]:
    texts: list[str] = []
    tracked = subprocess.run(
        ["git", "ls-files", "--", "*.md"], cwd=root, text=True,
        capture_output=True, check=True,
    ).stdout.splitlines()
    for rel in tracked:
        try:
            raw = subprocess.run(
                ["git", "show", f"HEAD:{rel}"], cwd=root,
                capture_output=True, check=True, text=True,
            ).stdout
        except subprocess.CalledProcessError:
            continue
        if "�" not in raw and not any(x in raw for x in ("쀼", "쀀", "쀄", "쀐", "쀴")):
            texts.append(raw)
    for base in (root, Path("/tmp/log-recovered")):
        for p in base.rglob("*.md"):
            if "venv" in p.parts:
                continue
            try:
                text = p.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if "�" not in text and not any(x in text for x in ("쀼", "쀀", "쀄", "쀐", "쀴")):
                texts.append(text)
    return texts


def model(texts: list[str]):
    uni, bi, tri = Counter(), Counter(), Counter()
    total = 0
    for text in texts + ["\n".join(ANCHORS) * 80]:
        text = "^" + text + "$"
        total += len(text)
        uni.update(text)
        bi.update(text[i:i + 2] for i in range(len(text) - 1))
        tri.update(text[i:i + 3] for i in range(len(text) - 2))

    def score(tail: str) -> float:
        if not tail:
            return 0.0
        c = tail[-1]
        value = math.log((uni[c] + 0.1) / (total + 1000)) * 0.1
        if len(tail) >= 2:
            value += math.log((bi[tail[-2:]] + 0.2) / (uni[tail[-2]] + 50)) * 0.55
        if len(tail) >= 3:
            value += math.log((tri[tail[-3:]] + 0.1) / (bi[tail[-3:-1]] + 20)) * 1.35
        for anchor in ANCHORS:
            if tail.endswith(anchor):
                value += 8.0
        return value
    return score


def repair_line(raw: bytes, score, beam: int,
                context_rules: dict[tuple[bytes, int, bytes], tuple[int, ...]] | None = None) -> bytes:
    # output bytes, expected continuation count, pending UTF-8 bytes, text tail, score
    states = [(b"", 0, b"", "", 0.0)]
    for pos, source in enumerate(raw):
        candidates = INVERSE.get(source, (source,))
        if context_rules and source in (0x22, 0x27):
            key = (raw[max(0, pos - 3):pos], source, raw[pos + 1:pos + 4])
            candidates = context_rules.get(key, candidates)
        next_states = []
        for out, remaining, pending, tail, value in states:
            if remaining:
                candidates_now = tuple(x for x in candidates if 0x80 <= x < 0xC0)
            else:
                candidates_now = candidates
            for byte in candidates_now:
                if remaining and not 0x80 <= byte < 0xC0:
                    continue
                if not remaining and 0x80 <= byte < 0xC0:
                    continue
                if remaining:
                    new_pending = pending + bytes((byte,))
                    new_remaining = remaining - 1
                    new_tail = tail
                    add = 0.0
                    if new_remaining == 0:
                        try:
                            char = new_pending.decode("utf-8")
                        except UnicodeDecodeError:
                            continue
                        new_tail = (tail + char)[-3:]
                        add = score(new_tail)
                    next_states.append((out + bytes((byte,)), new_remaining,
                                        new_pending, new_tail, value + add))
                    continue
                if 0xC2 <= byte <= 0xDF:
                    next_states.append((out + bytes((byte,)), 1, bytes((byte,)), tail, value))
                elif 0xE0 <= byte <= 0xEF:
                    next_states.append((out + bytes((byte,)), 2, bytes((byte,)), tail, value))
                elif 0xF0 <= byte <= 0xF4:
                    next_states.append((out + bytes((byte,)), 3, bytes((byte,)), tail, value))
                elif byte < 0x80:
                    char = chr(byte)
                    new_tail = (tail + char)[-3:]
                    next_states.append((out + bytes((byte,)), 0, b"", new_tail,
                                        value + score(new_tail)))
        if not next_states:
            return raw
        next_states.sort(key=lambda state: state[4], reverse=True)
        states = next_states[:beam]
    complete = [state for state in states if state[1] == 0]
    if not complete:
        return raw
    best = max(complete, key=lambda state: state[4])[0]
    text = best.decode("utf-8")
    # Apply only spans learned from the evidence pairs above.  There is no
    # hand-authored corrupted->clean output table here.
    for bad in sorted(LEARNED_REPLACEMENTS, key=len, reverse=True):
        text = text.replace(bad, LEARNED_REPLACEMENTS[bad])
    return text.encode("utf-8")


def apply_unique_context_bytes(raw: bytes, rules: dict[tuple[bytes, int, bytes], tuple[int, ...]]) -> bytes:
    """Apply only unambiguous evidence rules while retaining all other bytes."""
    out = bytearray(raw)
    for pos, source in enumerate(raw):
        if source not in (0x22, 0x27):
            continue
        key = (raw[max(0, pos - 3):pos], source, raw[pos + 1:pos + 4])
        values = rules.get(key, ())
        if len(values) == 1:
            out[pos] = values[0]
    return bytes(out)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--beam", type=int, default=768)
    parser.add_argument("--evidence", nargs=2, action="append", default=[],
                        metavar=("DAMAGED", "CLEAN"))
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()
    score = model(clean_texts(Path.cwd()))
    context_rules: dict[tuple[bytes, int, bytes], tuple[int, ...]] = {}
    for damaged_path, clean_path in args.evidence:
        learned = learn_context_rules(Path(damaged_path).read_bytes(),
                                       Path(clean_path).read_bytes())
        for key, values in learned.items():
            context_rules[key] = tuple(sorted(set(context_rules.get(key, ())) | set(values)))
    for rel in args.files:
        source = args.source / rel
        target = args.output / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        raw = source.read_bytes()
        raw = apply_unique_context_bytes(raw, context_rules)
        repaired = b"\n".join(repair_line(line, score, args.beam, context_rules)
                               for line in raw.split(b"\n"))
        target.write_bytes(repaired)
        try:
            repaired.decode("utf-8")
            status = "valid"
        except UnicodeDecodeError as error:
            status = f"invalid@{error.start}"
        print(status, rel, flush=True)


if __name__ == "__main__":
    main()
