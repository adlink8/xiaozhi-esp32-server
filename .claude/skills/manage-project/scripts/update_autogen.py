#!/usr/bin/env python3
from __future__ import annotations

import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

AUTOGEN_RE = re.compile(
    r"(?s)(<!--\s*AUTOGEN:(?P<key>[A-Z0-9_-]+):START\s*-->)(.*?)(<!--\s*AUTOGEN:(?P=key):END\s*-->)"
)


def run(cmd: list[str], cwd: Path) -> str:
    p = subprocess.run(cmd, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode != 0:
        return ""
    return p.stdout.strip()


def repo_root_from(script_dir: Path) -> Path:
    # Prefer git
    root = run(["git", "rev-parse", "--show-toplevel"], cwd=script_dir)
    if root:
        return Path(root)
    # Fallback: repo/.claude/skills/manage-project/scripts
    return script_dir.parents[4]


def scan_todos(repo_root: Path) -> tuple[int, int, list[str]]:
    scan = repo_root / ".claude/skills/manage-project/scripts/scan_todos.py"
    if not scan.exists():
        return (0, 0, [])

    out = run([str(scan), str(repo_root), "--include", "main", "--include", "project", "--include", "docs", "--limit", "80"], cwd=repo_root)
    if not out:
        return (0, 0, [])

    lines = out.splitlines()
    header = lines[0]
    m_todo = re.search(r"TODO=(\d+)", header)
    m_fixme = re.search(r"FIXME=(\d+)", header)
    todo = int(m_todo.group(1)) if m_todo else 0
    fixme = int(m_fixme.group(1)) if m_fixme else 0

    items: list[str] = []
    for line in lines[1:]:
        parts = line.split("\t", 2)
        if len(parts) != 3:
            continue
        kind, loc, text = parts
        items.append(f"- **{kind}** `{loc}` — {text}")

    return (todo, fixme, items)


def replace_autogen(text: str, replacements: dict[str, str]) -> str:
    def repl(m: re.Match[str]) -> str:
        key = m.group("key")
        start = m.group(1)
        end = m.group(4)
        body = replacements.get(key, m.group(3))
        # Keep a blank line after START and before END for readability
        return f"{start}\n{body}\n{end}"

    return AUTOGEN_RE.sub(repl, text)


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    repo_root = repo_root_from(script_dir)

    now = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %z")

    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_root) or "(unknown)"
    head = run(["git", "rev-parse", "--short", "HEAD"], cwd=repo_root) or "(unknown)"
    recent = run(["git", "--no-pager", "log", "--oneline", "-n", "5"], cwd=repo_root)
    status = run(["git", "--no-pager", "status", "--porcelain=v1"], cwd=repo_root)

    todo_count, fixme_count, todo_items = scan_todos(repo_root)

    discovered_block = "\n".join(
        [
            f"_Generated at: {now}_",
            "",
            f"- Totals: TODO={todo_count}, FIXME={fixme_count}",
            "",
            "### Top TODO/FIXME occurrences (first 80)",
            *todo_items,
        ]
    )

    snapshot_lines = [
        f"_Generated at: {now}_",
        "",
        f"- Git branch: `{branch}`",
        f"- Git HEAD: `{head}`",
        f"- TODO/FIXME in repo: TODO={todo_count}, FIXME={fixme_count}",
        "",
        "### Recent commits (5)",
        "```",
        recent or "(no git history)",
        "```",
        "",
        "### Working tree (porcelain)",
        "```",
        status if status else "(clean)",
        "```",
    ]
    snapshot_block = "\n".join(snapshot_lines)

    # Update todo.md
    todo_path = repo_root / "project/todo.md"
    todo_text = todo_path.read_text(encoding="utf-8")
    todo_text = replace_autogen(todo_text, {"DISCOVERED_TASKS": discovered_block})
    todo_path.write_text(todo_text, encoding="utf-8")

    # Update project-status.md
    ps_path = repo_root / "project/project-status.md"
    ps_text = ps_path.read_text(encoding="utf-8")
    ps_text = replace_autogen(ps_text, {"PROJECT_SNAPSHOT": snapshot_block})
    ps_path.write_text(ps_text, encoding="utf-8")

    print("Updated AUTOGEN blocks:")
    print(f"- {todo_path}")
    print(f"- {ps_path}")


if __name__ == "__main__":
    main()
