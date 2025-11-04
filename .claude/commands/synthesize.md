---
description: Consolidate conversations and project state into master memory
---

Synthesize project memory by consolidating all conversation summaries, documentation, and project state into a unified master memory file.

## Instructions

This is a multi-step process. Work through each step systematically.

### Step 1: Gather Conversation Summaries

Read all conversation summary files from `_memory/conversations/`:
- List all `.md` files in the directory
- Read each summary file
- Note key themes, decisions, patterns across summaries

### Step 2: Scan Project Documentation

Read documentation from `_docs/` folder (if it exists):
- List files/folders in `_docs/`
- Identify relevant documentation (READMEs, specs, planning docs)
- Extract key project information, decisions, status updates
- Skip if `_docs/` doesn't exist

### Step 3: Check Project Context (Smart Detection)

**For coding projects:**
- Check if `.git` exists (run `ls -la .git 2>/dev/null || echo "not a git repo"`)
- If git repo: Get recent commits (`git log --oneline -20`)
- Read `package.json` or equivalent config files for tech stack info
- Note current branch and recent changes

**For non-coding projects:**
- Check for any project-specific files (plans, outlines, etc.)
- Note file structure that indicates project type

**Skip code-specific scanning if not applicable**

### Step 4: Read Current Master Memory

Read `_memory/master.md` to understand:
- What's currently captured
- What needs updating
- What's resolved vs. still active

### Step 5: Cross-Reference & Identify Evolution

Compare information across sources:
- Look for decisions that changed over time
- Identify contradictions (planned vs. actual)
- Note what's been resolved vs. still open
- Track evolution: "Started with X → tried Y → now using Z"

### Step 6: Synthesize New Master Memory

Create a comprehensive synthesis using this structure:

```markdown
# Project Memory

*This file is automatically synthesized from conversation summaries and codebase analysis.*

---

## Current Status

[Where is the project NOW? Current phase, recent work, active focus]

## Key Decisions

[Important decisions with context and rationale. Organize by theme/domain]

## Learnings & Discoveries

[Patterns, insights, what worked, what didn't work. Technical or general.]

## Evolution & Changes

[How things changed over time. Show journey: A → B → C. Captures conflicts naturally.]

## Active Questions

[Open items, blockers, unresolved issues. Remove if resolved.]

---

*Last synthesized: [DATE]*
*Source: [N] conversations, [N] docs*
```

**Important synthesis guidelines:**
- Consolidate by theme, not chronologically
- Show evolution where decisions changed
- Keep it concise - distill, don't copy verbatim
- Prioritize recent/current information
- Remove resolved items from "Active Questions"
- Cross-reference summaries with actual project state
- Adapt structure if needed for project type

### Step 7: Present for Review

Show the synthesized master.md to the user for review and approval.

### Step 8: Save

Once approved, write to `_memory/master.md`

---

## Important Notes

- **This runs in a dedicated conversation** - you're doing synthesis work in this thread
- **Full scan every time** - read all summaries, all docs (optimization can come later)
- **Show your work** - explain what you found, how you're consolidating
- **Master memory should be concise** - aim for clarity and usefulness, not completeness
- **Flexible structure** - adapt to project type (coding vs. non-coding)
- **Evolution > conflict** - when things changed, show the journey
