#!/usr/bin/env python3
"""Mechanical kickstart files and checks, so the model writes only what needs judgement.

Run with the skill directory as <skill>; all commands are idempotent and never overwrite.

  python3 <skill>/scripts/kickstart_files.py files    --stack node-typescript --dest . [--ui] [--merge]
      .gitignore and .editorconfig (base + stack section), and design/build_tokens.py with --ui.
      A file that already exists is left alone: its diff against the generated version is
      printed and the exit code is 3, so you can show it and ask. --merge (only for files a
      scaffolder created in this run) appends the missing .gitignore rules instead.

  python3 <skill>/scripts/kickstart_files.py settings --allow "npm run build" "npm test" ...
      Prints .claude/settings.json to stdout (read-only git, the given commands bare and with
      " *", git push in "ask", .env and secrets denied). Write it with your file tool: Claude Code
      protects that path and asks the user.

  python3 <skill>/scripts/kickstart_files.py agents   --dest .
      AGENTS.md -> CLAUDE.md as a relative symlink; a marked copy where symlinks fail (Windows).

  python3 <skill>/scripts/kickstart_files.py check    --dest . [FILE ...]
      CLAUDE.md line limit, leftover {{placeholders}} in the given generated files, relative
      links in CLAUDE.md and README.md, valid JSON in .claude/settings.json and design/tokens.json,
      AGENTS.md matching CLAUDE.md. Exit 1 on any failure.

Python 3.8+, standard library only.
"""
import argparse
import difflib
import json
import os
import re
import shutil
import sys

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(SKILL, "templates")
CLAUDE_MAX_LINES = 80
COPY_HEADER = "<!-- Copy of CLAUDE.md; keep both in sync. -->\n"


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def template(stack, name):
    """Base template plus the stack's section, if any (for gitignore / editorconfig)."""
    text = read(os.path.join(TEMPLATES, "_base", name))
    extra = os.path.join(TEMPLATES, stack, name)
    if stack and os.path.exists(extra):
        text = text.rstrip("\n") + "\n\n" + read(extra).lstrip("\n")
    return text


def place(dest, rel, content):
    """Write rel under dest unless it exists. Return True if written, False if left alone."""
    path = os.path.join(dest, rel)
    if os.path.exists(path):
        current = read(path)
        if current == content:
            print(f"same     {rel}")
            return True
        print(f"exists   {rel}: not changed. Diff to the generated version:")
        sys.stdout.writelines(difflib.unified_diff(current.splitlines(True), content.splitlines(True),
                                                   f"{rel} (current)", f"{rel} (generated)"))
        print()
        return False
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"created  {rel}")
    return True


def merge_gitignore(dest, content):
    path = os.path.join(dest, ".gitignore")
    current = read(path)
    have = {l.strip() for l in current.splitlines()}
    missing = [l for l in content.splitlines() if l.strip() and not l.startswith("#") and l.strip() not in have]
    if missing:
        with open(path, "a", encoding="utf-8") as f:
            f.write(("" if current.endswith("\n") else "\n") + "\n# Added by project-kickstart\n" + "\n".join(missing) + "\n")
    print(f"merged   .gitignore (+{len(missing)} rules)")
    return True


def cmd_files(a):
    if a.stack and not os.path.isdir(os.path.join(TEMPLATES, a.stack)):
        print(f"note: no template for stack '{a.stack}'; using the base only", file=sys.stderr)
    gi = template(a.stack, "gitignore")
    if a.merge and os.path.exists(os.path.join(a.dest, ".gitignore")):
        ok = merge_gitignore(a.dest, gi)
    else:
        ok = place(a.dest, ".gitignore", gi)
    ok &= place(a.dest, ".editorconfig", template(a.stack, "editorconfig"))
    if a.ui:
        ok &= place(a.dest, "design/build_tokens.py", read(os.path.join(SKILL, "scripts", "build_tokens.py")))
    return 0 if ok else 3


def cmd_settings(a):
    base = json.loads(read(os.path.join(TEMPLATES, "_base", "claude", "settings.json")))
    allow = base["permissions"]["allow"]
    for c in a.allow:
        c = c.strip()
        if re.search(r"(^|\s)(rm|curl|wget|sudo)\b|git (push|reset|clean)|npm (publish|install)|\*", c):
            print(f"refused: '{c}' is not a build/test/lint command", file=sys.stderr)
            return 2
        for entry in (f"Bash({c})", f"Bash({c} *)"):
            if entry not in allow:
                allow.append(entry)
    json.dump(base, sys.stdout, indent=2)
    print()
    return 0


def cmd_agents(a):
    claude, agents = os.path.join(a.dest, "CLAUDE.md"), os.path.join(a.dest, "AGENTS.md")
    if not os.path.exists(claude):
        print("CLAUDE.md does not exist yet", file=sys.stderr)
        return 2
    if os.path.lexists(agents):
        print("exists   AGENTS.md: not changed")
        return 3
    try:
        os.symlink("CLAUDE.md", agents)
        print("symlink  AGENTS.md -> CLAUDE.md")
    except (OSError, NotImplementedError):
        with open(agents, "w", encoding="utf-8") as f:
            f.write(COPY_HEADER + read(claude))
        print("copied   AGENTS.md (symlinks unavailable)")
    return 0


def cmd_check(a):
    fails = []
    d = a.dest
    claude = os.path.join(d, "CLAUDE.md")
    if os.path.exists(claude):
        n = len(read(claude).splitlines())
        if n > CLAUDE_MAX_LINES:
            fails.append(f"CLAUDE.md has {n} lines (max {CLAUDE_MAX_LINES})")
    for rel in a.files:
        path = os.path.join(d, rel)
        if os.path.isfile(path):
            for no, line in enumerate(read(path).splitlines(), 1):
                if "{{" in line:
                    fails.append(f"{rel}:{no}: placeholder left: {line.strip()[:80]}")
    for rel in ("CLAUDE.md", "README.md", "docs/ARCHITECTURE.md", "docs/DESIGN.md"):
        path = os.path.join(d, rel)
        if not os.path.exists(path):
            continue
        for target in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", read(path)):
            if re.match(r"^[a-z]+:", target):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(path), target))):
                fails.append(f"{rel}: broken link {target}")
    for rel in (".claude/settings.json", "design/tokens.json"):
        path = os.path.join(d, rel)
        if os.path.exists(path):
            try:
                json.loads(read(path))
            except json.JSONDecodeError as e:
                fails.append(f"{rel}: invalid JSON ({e})")
    agents = os.path.join(d, "AGENTS.md")
    if os.path.exists(agents) and os.path.exists(claude):
        body = read(agents)
        if body.startswith(COPY_HEADER):
            body = body[len(COPY_HEADER):]
        if body != read(claude):
            fails.append("AGENTS.md differs from CLAUDE.md")
    for f in fails:
        print("FAIL  " + f)
    print("checks: " + ("all passed" if not fails else f"{len(fails)} failed"))
    return 1 if fails else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("files")
    f.add_argument("--stack", default="")
    f.add_argument("--dest", default=".")
    f.add_argument("--ui", action="store_true")
    f.add_argument("--merge", action="store_true")
    s = sub.add_parser("settings")
    s.add_argument("--allow", nargs="*", default=[])
    g = sub.add_parser("agents")
    g.add_argument("--dest", default=".")
    c = sub.add_parser("check")
    c.add_argument("--dest", default=".")
    c.add_argument("files", nargs="*")
    a = ap.parse_args(argv)
    return {"files": cmd_files, "settings": cmd_settings, "agents": cmd_agents, "check": cmd_check}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
