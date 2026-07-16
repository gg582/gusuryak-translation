#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

case "${1:-}" in
  korean) TARGET="$ROOT/korean" ;;
  english) TARGET="$ROOT/english" ;;
  *)
    printf 'Usage: %s korean|english\n' "$0" >&2
    exit 2
    ;;
esac

find "$TARGET" -type f -name '*.md' \
  -not -path '*/venv/*' \
  -not -path '*/.venv/*' \
  -not -path '*/__pycache__/*' -print0 |
  sort -z |
  while IFS= read -r -d '' file; do
    rel=${file#"$ROOT/"}
    printf '\n%s\nFILE: %s\n%s\n' \
      '======================================================================' \
      "$rel" \
      '======================================================================'
    cat "$file"
    printf '\n%s\n' '======================================================================'
  done
