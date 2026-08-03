#!/usr/bin/env python3
"""
Convert each cloops-* Claude Code session to its own markdown file.

Why not just `specstory sync -s ... -s ...`?
    SpecStory derives output filenames from the session's first-message
    timestamp. Sessions that branch from the same parent at the same instant
    collide on filename and overwrite each other. We bypass this by using
    `specstory sync -s <id> --print` (stdout) and writing files ourselves
    with title-based names.

Inputs:  _out/session-lookup/cloops_session_lookup.json (built by build_session_lookup.py)
Outputs: _out/specstory-md/<NN>_<slug>__<sessionid>.md
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOOKUP_JSON = PROJECT_ROOT / "_out" / "session-lookup" / "cloops_session_lookup.json"
OUT_DIR = PROJECT_ROOT / "_out" / "specstory-md"


def slugify(text: str, max_len: int = 60) -> str:
    """Filesystem-safe slug from a title."""
    s = text.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:max_len].rstrip("-") or "session"


def session_sort_key(title: str) -> tuple:
    """Sort cloops-s1, s2, ..., s10, s11a, s11a2, s11b, s12 in human order."""
    m = re.match(r"cloops-s(\d+)([a-z0-9]*)", title.lower())
    if not m:
        return (9999, "", title.lower())
    return (int(m.group(1)), m.group(2), title.lower())


def sync_one(session_id: str) -> str | None:
    """Run specstory and return the markdown text, or None on failure."""
    try:
        result = subprocess.run(
            [
                "specstory", "sync",
                "-s", session_id,
                "--print",
                "--no-cloud-sync",
                "--silent",
            ],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"    ! ERROR: {e}", file=sys.stderr)
        return None

    if result.returncode != 0:
        print(f"    ! specstory exited {result.returncode}: {result.stderr.strip()[:200]}", file=sys.stderr)
        return None
    return result.stdout


def main() -> None:
    if not LOOKUP_JSON.exists():
        sys.exit(f"Lookup JSON not found: {LOOKUP_JSON}\nRun build_session_lookup.py first.")

    rows = json.loads(LOOKUP_JSON.read_text(encoding="utf-8"))
    rows.sort(key=lambda r: session_sort_key(r["title"]))

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Syncing {len(rows)} cloops sessions to {OUT_DIR}/\n")

    written, failed, empty = 0, 0, 0
    for i, r in enumerate(rows, start=1):
        sid = r["sessionId"]
        title = r["title"]
        slug = slugify(title)
        # Index prefix keeps files sorted in the same order as the lookup table
        out_path = OUT_DIR / f"{i:02d}_{slug}__{sid[:8]}.md"

        print(f"  [{i:2d}/{len(rows)}] {title[:60]:60s}  -> {out_path.name}")
        md = sync_one(sid)
        if md is None:
            failed += 1
            continue
        if not md.strip():
            empty += 1
            print("    ! empty output")
            continue
        out_path.write_text(md, encoding="utf-8")
        written += 1

    print(f"\nDone. Written: {written}  |  Failed: {failed}  |  Empty: {empty}")


if __name__ == "__main__":
    main()
