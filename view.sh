#!/usr/bin/env bash
set -u

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TARGET=${VIEW_ROOT:-$ROOT}

find "$TARGET" -type f -name '*.md' \
  -not -path '*/.git/*' \
  -not -path '*/venv/*' \
  -not -path '*/.venv/*' \
  -not -path '*/__pycache__/*' -print0 |
  sort -z |
  while IFS= read -r -d '' file; do
  rel=${file#"$TARGET/"}
  printf '\n%s\n' "======================================================================"
  printf 'FILE: %s\n' "$rel"
  cat "$file"
  printf '\n%s\n' "======================================================================"
done
