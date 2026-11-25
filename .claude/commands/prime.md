---
description: Prime context with project structure scan. Usage: /prime [path] [task]
argument-hint: [path] [task]
---

## Input format

User input: $ARGUMENTS

The input is `[path] [task]`, both optional:

- **path** (optional): scopes the structure scan. The first token is a path only if it resolves to an existing directory, symlink, or subpath (check the project root and `_projects/`; resolve symlinks). If it does, scan only that path in Step 1 and treat the remaining words (minus filler like "only" or "just") as the task. If the first token does not resolve to a real path, the entire input is the task.
- **task** (optional): what the user is working on, handled in Step 2.

With no path given, scan the whole project root.

## Step 1: Show structure

Run the scan against the chosen root (`.` if no path was given):

```bash
eza <SCAN_ROOT> --tree --git-ignore --follow-symlinks --level 8 --ignore-glob="node_modules|__pycache__|.next|dist|build|lib|output|*.mp4|*.mp3|*.jpg|*.png|*.jpeg|*.mov|*.m4a|*.js.map|4_exported-threads|conversations|step-summaries|_archive|archive"
```

## Step 2: Initial context

**If the input included a task:**
- Acknowledge the task
- Mention: "Run `/prime-suggest` if you'd like file suggestions for this task"

**If the input was a path with no task:**
- Give a brief orientation of what the scanned area contains, then ask what to work on

**If the input was "general":**
- Load package.json and main entry points
- Ask: "Any specific area to explore?"

**If no input:**
- Ask: "What are you working on today?"

Note: If the user references files with @, still suggest additional relevant files before loading anything.

## Next steps
After initial context is established:
- Use `/prime-suggest` anytime to get file suggestions based on the conversation
- Reference files directly with @ to load them
