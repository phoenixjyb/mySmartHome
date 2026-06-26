#!/usr/bin/env bash
set -euo pipefail
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DST="$HOME/Projects/smartHouse"
mkdir -p "$DST"
if command -v rsync >/dev/null 2>&1; then
  rsync -av --exclude '.git/' "$SRC/" "$DST/"
else
  cp -a "$SRC/." "$DST/"
fi
printf '\n已同步到：%s\n' "$DST"
