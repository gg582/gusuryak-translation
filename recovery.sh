#!/usr/bin/env bash
set -u

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
DAMAGED=${RECOVERY_DAMAGED:-"$ROOT/../gusuryak-translation-damaged-20260717-060415"}
RECOVERED=${RECOVERY_STAGING:-/tmp/gusuryak-recovery-20260717}
SHOW_BODIES=1
[[ "${1:-}" == "--summary" ]] && SHOW_BODIES=0

if [[ ! -d "$DAMAGED" ]]; then
  printf 'Missing damaged snapshot: %s\n' "$DAMAGED" >&2
  exit 1
fi

python3 - "$ROOT" "$DAMAGED" "$RECOVERED" "$SHOW_BODIES" <<'PY'
from pathlib import Path
import hashlib
import sys

repo = Path(sys.argv[1])
damaged = Path(sys.argv[2])
recovered = Path(sys.argv[3])
show_bodies = sys.argv[4] == "1"

def digest(path):
    if not path.exists():
        return "missing"
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]

def status(path):
    if not path.exists():
        return ("missing", 0, 0)
    raw = path.read_bytes()
    bad = 0
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("utf-8", "replace")
        bad = text.count("\ufffd")
    return ("valid" if bad == 0 else "invalid", len(raw), bad)

paths = sorted(p.relative_to(damaged) for p in damaged.rglob("*.md"))
print(f"Damaged snapshot : {damaged}")
print(f"Recovery staging : {recovered}")
print(f"Repository       : {repo}")
print(f"Documents        : {len(paths)}")
print()

for rel in paths:
    d = damaged / rel
    r = recovered / rel
    c = repo / rel
    ds, dn, db = status(d)
    rs, rn, rb = status(r)
    cs, cn, cb = status(c)
    print("=" * 100)
    print(rel)
    print(f"  damaged   {ds:7} bytes={dn:7} replacement={db:4} sha256={digest(d)}")
    print(f"  recovered {rs:7} bytes={rn:7} replacement={rb:4} sha256={digest(r)}")
    print(f"  current   {cs:7} bytes={cn:7} replacement={cb:4} sha256={digest(c)}")
    if r.exists() and d.exists() and r.read_bytes() == d.read_bytes():
        print("  result    unchanged from damaged snapshot")
    elif r.exists():
        print("  result    staging differs from damaged snapshot")
    else:
        print("  result    no staging candidate")
    if show_bodies and (ds == "invalid" or rs == "invalid" or cs == "invalid"):
        if ds == "invalid":
            print("  ----- damaged file bytes decoded with replacement -----")
            print(d.read_bytes().decode("utf-8", "replace"), end="")
        if rs == "invalid":
            print("  ----- recovered candidate bytes decoded with replacement -----")
            print(r.read_bytes().decode("utf-8", "replace"), end="")
        if cs == "invalid":
            print("  ----- current repository bytes decoded with replacement -----")
            print(c.read_bytes().decode("utf-8", "replace"), end="")
PY
