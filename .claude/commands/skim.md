# /skim — outline-level priming (progressive disclosure)

Prime context with OUTLINES instead of full files: markdown reduced to heading skeletons, code reduced to exported symbols, JSON reduced to key shapes. The whole scanned area lands in a few hundred lines of context. Full bodies are pulled later, on demand, one file per question.

## Input format

User input: $ARGUMENTS

Free-form: `[paths] [filters]`, all optional.

- **paths**: one or more directories or files to scan. Resolve each token against the project root and `_projects/` (follow symlinks). Tokens that resolve are paths; everything else is a filter word. No path = the whole project root.
- **filters** (plain words, combinable):
  - `docs` = markdown outlines only · `code` = code outlines only · `json` = JSON shapes only. Absent = all three.
  - `exclude <glob-or-name>` (repeatable) = add to the exclusion list.
  - `include <glob-or-name>` (repeatable) = scan something the defaults would skip (e.g. `include _archive`).

**Default exclusions** (always applied unless the user says `include`): `node_modules`, `_generated`, `_archive`, `archive`, `.obsidian`, `dist`, `build`, `__pycache__`, lockfiles, media files.

## Step 1: extract outlines (few batched calls, not per-file)

Run the applicable recipes against the scan targets. Batch aggressively: one command per recipe, not per file. Strip absolute path prefixes from output for readability.

**Markdown → heading skeletons:**
```bash
rg -n '^#{1,6} ' <targets> --glob '*.md'
```
Also capture each doc's `Created:`/`Updated:` header if present (loose match, first 8 lines): `rg -oN -m1 'Updated:[^0-9]*([0-9]{4}-[0-9]{2}-[0-9]{2})' -r '$1'`.

**Code → exported/top-level symbols:**
```bash
# TypeScript / JavaScript
rg -n '^export\s+(async\s+)?(function|const|class|interface|type|enum|default)\s*\w*' <targets> -g '*.ts' -g '*.tsx' -g '*.js' -g '*.mjs'
# Python
rg -n '^(def|class)\s+\w+|^[A-Z_]+\s*=' <targets> -g '*.py'
```
If output exceeds ~300 lines for one recipe, tighten (exports only, or per-directory summaries) rather than dumping; a skim that floods context has failed its purpose.

**JSON → key shapes, representative files only.** Pick ONE representative file per distinct shape (e.g. one `beats.json`, not thirty):
```bash
jq -r 'paths(scalars) | map(tostring) | join(".")' <file> | awk -F. '{if (NF>=3) print $1"."$2"."$3; else print $0}' | sort -u | head -40
```

## Step 2: report and hold

- Give a SHORT orientation (a few sentences): what the scanned area contains, anything structurally surprising. Do not re-print the outlines back at the user; they are your map, in your context.
- State the contract you now operate under: **outlines are the map; full bodies load on demand, one file per question, when a question actually needs that file's evidence.** Never wholesale-read the scanned area after a skim.
- If the user gave a task, proceed on it using the map. Otherwise ask what to work on.

## Notes

- `/prime` shows the file TREE (structure); `/skim` shows what's INSIDE at outline level. They compose: `/prime` first when the layout is unknown, `/skim` when the contents are the question.
- Re-running `/skim` on the same area is a smell; the map is already in context. Pull the specific file instead.

Created: 2026-07-12 · Updated: 2026-07-12
