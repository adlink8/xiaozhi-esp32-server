#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-.}"
if git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "## Git Snapshot"
  echo
  echo "- Branch: $(git -C "$ROOT" rev-parse --abbrev-ref HEAD)"
  echo "- HEAD:   $(git -C "$ROOT" rev-parse --short HEAD)"
  echo
  echo "### Recent commits (5)"
  git -C "$ROOT" --no-pager log --oneline -n 5
  echo
  echo "### Working tree"
  git -C "$ROOT" --no-pager status --porcelain=v1 || true
else
  echo "Not a git repository: $ROOT" >&2
  exit 2
fi
