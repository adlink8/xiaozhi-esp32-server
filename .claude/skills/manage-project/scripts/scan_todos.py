#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
from dataclasses import dataclass
from pathlib import Path

DEFAULT_EXCLUDES = {
    ".git",
    ".claude",
    "node_modules",
    "dist",
    "build",
    "target",
    ".venv",
    "venv",
    "__pycache__",
}

PATTERN = re.compile(r"\\b(TODO|FIXME)\\b[:]?(.*)")

@dataclass
class Hit:
    kind: str
    file: str
    line: int
    text: str


def iter_files(root: Path, include: list[str], exclude: set[str]) -> list[Path]:
    roots = [root / p for p in include] if include else [root]
    out: list[Path] = []
    for r in roots:
        if not r.exists():
            continue
        if r.is_file():
            out.append(r)
            continue
        for p in r.rglob("*"):
            try:
                if p.is_dir():
                    continue
                parts = set(p.parts)
                if parts & exclude:
                    continue
                # skip huge files
                try:
                    if p.stat().st_size > 512 * 1024:
                        continue
                except OSError:
                    continue
                out.append(p)
            except (OSError, PermissionError):
                continue
    return out


def scan(root: Path, include: list[str], exclude: set[str]) -> list[Hit]:
    hits: list[Hit] = []
    for f in iter_files(root, include, exclude):
        try:
            rel = str(f.relative_to(root))
        except ValueError:
            rel = str(f)

        try:
            with f.open("r", encoding="utf-8", errors="ignore") as fp:
                for i, line in enumerate(fp, start=1):
                    m = PATTERN.search(line)
                    if not m:
                        continue
                    kind = m.group(1)
                    tail = (m.group(2) or "").strip()
                    text = (tail if tail else line.strip())
                    hits.append(Hit(kind=kind, file=rel, line=i, text=text))
        except (OSError, PermissionError, IsADirectoryError):
            continue
    return hits


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--include", action="append", default=[], help="Subpaths to include (repeatable)")
    ap.add_argument("--exclude", action="append", default=[], help="Dir names to exclude (repeatable)")
    ap.add_argument("--limit", type=int, default=200)
    args = ap.parse_args()

    root = Path(args.root).resolve()
    exclude = set(DEFAULT_EXCLUDES) | set(args.exclude)
    hits = scan(root, args.include, exclude)

    todo = sum(1 for h in hits if h.kind == "TODO")
    fixme = sum(1 for h in hits if h.kind == "FIXME")

    print(f"TODO={todo} FIXME={fixme} TOTAL={len(hits)}")
    for h in hits[: args.limit]:
        print(f"{h.kind}\t{h.file}:{h.line}\t{h.text}")


if __name__ == "__main__":
    main()
