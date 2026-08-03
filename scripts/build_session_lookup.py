#!/usr/bin/env python3
"""
Build a lookup table mapping Claude Code custom session titles -> session IDs.

Scans all .jsonl conversation files under the bib-content-gen project folders
in ~/.claude/projects/, extracts `custom-title` entries, filters for titles
starting with a given prefix (default: "cloops-"), dedupes, and writes
the result as a Markdown table.

Usage:
    python build_session_lookup.py [--prefix cloops-] [--out-dir ./out]
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable

CLAUDE_PROJECTS_DIR = Path.home() / ".claude" / "projects"
PROJECT_GLOB = "*bib-content-gen*"


def find_jsonl_files(projects_dir: Path, project_glob: str) -> list[Path]:
    """Find all .jsonl conversation files across matching project folders."""
    files: list[Path] = []
    for project_dir in projects_dir.glob(project_glob):
        if project_dir.is_dir():
            files.extend(project_dir.glob("*.jsonl"))
    return files


def scan_session_file(jsonl_path: Path) -> dict | None:
    """Return one summary record per session file, or None if no usable data.

    Strategy: walk the JSONL once and capture
      - sessionId  (the file's session)
      - latestTitle (last `custom-title` entry wins; that's the canonical name)
      - forkedFromSessionId (from `forkedFrom.sessionId` on any line; same value
        for all forked-in lines, so first wins)
      - latestTimestamp (most recent ISO timestamp in the file -> recency)
      - messageCount (rough size signal: count of user/assistant message lines)
    """
    session_id: str | None = None
    latest_title: str | None = None
    forked_from: str | None = None
    latest_ts: str | None = None
    message_count = 0

    try:
        with jsonl_path.open("r", encoding="utf-8") as f:
            for line in f:
                # Pre-filter for speed: only parse lines we care about
                if not line.startswith("{"):
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue

                t = obj.get("type")

                # SessionId — same on every line, but capture once
                if session_id is None:
                    sid = obj.get("sessionId")
                    if sid:
                        session_id = sid

                # Latest custom-title wins (file is append-only -> last line is newest)
                if t == "custom-title":
                    title = obj.get("customTitle")
                    if title:
                        latest_title = title

                # Branch parent (set once)
                if forked_from is None:
                    ff = obj.get("forkedFrom")
                    if isinstance(ff, dict):
                        forked_from = ff.get("sessionId")

                # Track latest timestamp seen (string compare works for ISO-8601)
                ts = obj.get("timestamp")
                if ts and (latest_ts is None or ts > latest_ts):
                    latest_ts = ts

                if t in ("user", "assistant"):
                    message_count += 1
    except OSError:
        return None

    if not session_id:
        return None

    return {
        "sessionId": session_id,
        "title": latest_title,           # may be None if session never had a custom title
        "forkedFromSessionId": forked_from,
        "latestTimestamp": latest_ts,
        "messageCount": message_count,
        "file": str(jsonl_path),
    }


def natural_key(title: str) -> list:
    """Sort key that orders s1, s2, s10 naturally instead of s1, s10, s2."""
    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r"(\d+)", title)
    ]


def build_lookup(prefix: str) -> list[dict]:
    """Return one row per session, filtered by title prefix, naturally sorted.

    One row per sessionId. The canonical title is the LATEST custom-title in
    the file (renames are append-only, so last wins). Includes branch parent
    via forkedFromSessionId.
    """
    files = find_jsonl_files(CLAUDE_PROJECTS_DIR, PROJECT_GLOB)
    print(f"Scanning {len(files)} .jsonl files...")

    rows: list[dict] = []
    for path in files:
        rec = scan_session_file(path)
        if rec is None:
            continue
        title = rec["title"]
        if not title or not title.startswith(prefix):
            continue
        rows.append(rec)

    # Build sessionId -> title map so we can resolve forkedFrom -> parent title
    sid_to_title = {r["sessionId"]: r["title"] for r in rows}
    for r in rows:
        parent_sid = r.get("forkedFromSessionId")
        r["forkedFromTitle"] = sid_to_title.get(parent_sid) if parent_sid else None

    rows.sort(key=lambda r: natural_key(r["title"]))
    return rows


def md_escape(text: str) -> str:
    """Escape characters that would break a Markdown table cell."""
    return text.replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def write_outputs(rows: list[dict], out_dir: Path, prefix: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{prefix.rstrip('-')}_session_lookup"
    md_path = out_dir / f"{stem}.md"

    branch_count = sum(1 for r in rows if r.get("forkedFromSessionId"))
    root_count = len(rows) - branch_count

    lines = [
        f"# Session lookup: `{prefix}*`",
        "",
        f"Total: **{len(rows)}** sessions  \u2014  "
        f"{root_count} root, {branch_count} branched",
        "",
        "| # | Title | Session ID | Forked From | Last Activity | Msgs |",
        "|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(rows, start=1):
        if r.get("forkedFromSessionId"):
            parent_title = r.get("forkedFromTitle") or "(unknown / non-cloops parent)"
            forked = f"{md_escape(parent_title)} `{r['forkedFromSessionId'][:8]}\u2026`"
        else:
            forked = "\u2014"
        ts = (r.get("latestTimestamp") or "")[:16].replace("T", " ")
        lines.append(
            f"| {i} | {md_escape(r['title'])} | `{r['sessionId']}` | "
            f"{forked} | {ts} | {r.get('messageCount', 0)} |"
        )
    lines.append("")  # trailing newline

    md_path.write_text("\n".join(lines), encoding="utf-8")

    # Also write a plain .txt of session IDs for easy piping into other tools
    # (e.g. `xargs -I{} specstory sync -s {}`)
    ids_path = out_dir / f"{stem}_ids.txt"
    ids_path.write_text("\n".join(r["sessionId"] for r in rows) + "\n", encoding="utf-8")

    # And a JSON for programmatic use
    json_path = out_dir / f"{stem}.json"
    json_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Wrote {len(rows)} entries:")
    print(f"  - {md_path}")
    print(f"  - {ids_path}")
    print(f"  - {json_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--prefix",
        default="cloops-",
        help="Only include custom titles starting with this prefix (default: cloops-)",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "_out" / "session-lookup",
        help="Directory to write CSV/JSON outputs",
    )
    args = parser.parse_args()

    rows = build_lookup(args.prefix)
    write_outputs(rows, args.out_dir, args.prefix)

    # Print a small preview to stdout
    print("\nPreview (first 10):")
    for r in rows[:10]:
        print(f"  {r['title']}  ->  {r['sessionId']}")


if __name__ == "__main__":
    main()
