# Memory System Architecture

**Version:** 1.0
**Status:** Foundation complete, synthesis pending
**Last Updated:** 2025-01-04

---

## Overview

Cross-conversation memory system for Claude Code CLI that preserves project context, decisions, and learnings across isolated conversation sessions. Inspired by Claude web's memory feature but adapted for file-based CLI environment.

### Purpose

- **Problem:** Each Claude Code conversation starts fresh with no memory of previous sessions
- **Solution:** File-based memory system that captures, synthesizes, and recalls project context on demand
- **Scope:** Works for both coding and non-coding projects

---

## Architecture

### Three-Command System

```
/summarize  → Capture THIS conversation → save to conversations/
/synthesize → Consolidate all summaries + scan project → update master.md
/recall     → Load master.md into context
```

### Information Flow

```
Conversation 1 → /summarize → summary-1.md ─┐
Conversation 2 → /summarize → summary-2.md ─┤
Conversation 3 → /summarize → summary-3.md ─┼→ /synthesize → master.md
                              _docs/ scan ───┤                    ↓
                              git analysis ──┘              /recall loads
```

### File Structure

```
_memory/
├── ARCHITECTURE.md           # This file
├── conversations/            # Individual conversation summaries
│   ├── 2025-01-04-memory-system-design.md
│   ├── 2025-01-05-feature-implementation.md
│   └── ...
└── master.md                 # Synthesized project memory (loads via /recall)
```

---

## Commands

### `/summarize` - Capture Conversation

**Purpose:** Preserve important context from current conversation

**How it works:**
1. Analyzes conversation for tracking points (decisions, discoveries, learnings, etc.)
2. Generates summary with flexible structure
3. Creates standardized filename from title (date-prefix + lowercase-dashes)
4. Checks if file exists via `ls _memory/conversations/`
5. Updates existing file OR creates new file
6. Minimal manual decisions - automated but predictable

**When to use:**
- End of conversation
- Mid-conversation when major decisions made
- Can run multiple times to update summary

**Example:**
```
Title: "Implementing User Authentication"
↓
Filename: 2025-01-04-user-authentication.md
↓
Exists? → Update | Doesn't exist? → Create
```

### `/synthesize` - Consolidate Memory

**Purpose:** Merge multiple conversation summaries + project state into master memory

**How it works:**
1. Runs in dedicated conversation thread (not background agent)
2. Scans all sources:
   - All conversation summaries (`_memory/conversations/*.md`)
   - Project documentation (`_docs/` folder)
   - Git commits (if git repo exists)
   - Codebase patterns (for coding projects only - smart detection)
3. Cross-references conversations with actual project state
4. Synthesizes by theme (not chronological)
5. Shows evolution/changes over time
6. Replaces master.md with fresh synthesis

**When to use:**
- After multiple conversations accumulate
- When master.md feels stale
- Weekly or after major work sessions
- Manual trigger only (not automated)

**Output structure:**
```markdown
## Current Status
Where is the project now?

## Key Decisions
What was decided and why?

## Learnings & Discoveries
Patterns, insights, what worked/didn't work

## Evolution & Changes
How things changed over time (handles conflicts)

## Active Questions
Open items, blockers, unclear areas
```

### `/recall` - Load Context

**Purpose:** Load synthesized project memory into current conversation

**How it works:**
1. Reads `_memory/master.md`
2. Acknowledges key status/decisions
3. Makes context available throughout conversation
4. Lightweight, fast operation

**When to use:**
- Start of new conversation
- Can be auto-triggered via hook (future enhancement)

---

## Design Principles

### 1. Simplicity Over Complexity
- Avoid overthinking and overcomplication
- Choose pragmatic over clever solutions
- Automate where possible, minimize manual decisions

### 2. Dual-Write Approach
- **Decision:** Save individual summary AND update master immediately (when synthesis runs)
- **Rejected:** Synthesize-on-load (would require reading all conversation files = token heavy)
- **Rationale:** Keeps master.md current, loading is fast and efficient

### 3. Synthesis = Distillation
- Master.md consolidates by theme, not verbatim copies
- "Summary of summaries" approach
- Prevents context bloat, stays within token limits

### 4. Standardized Filenames
- Auto-generate from title: `YYYY-MM-DD-key-terms.md`
- Exact filename match for updates (no fuzzy matching)
- Same conversation = same title = same filename = automatic update

### 5. Flexibility
- Tracking points adapt to conversation content
- Works for coding and non-coding projects
- Structure is consistent but content is dynamic

### 6. Evolution Tracking
- Show how decisions changed over time
- Track "Decision A → tried B → settled on C"
- Cross-reference with actual codebase state to prevent drift

---

## Integration with Existing Commands

### Complementary, Not Overlapping

**`/prime` + `/prime-suggest`** - Session setup & file discovery
- Purpose: Understand current codebase structure, find relevant files
- Scope: This session only
- Source: Filesystem (current state)

**`/recall` + `/summarize`** - Project memory & continuity
- Purpose: Remember historical decisions, patterns, learnings
- Scope: Cross-session memory
- Source: Conversation summaries + synthesis

### Ideal Workflow

```
1. /recall          → Load project memory
2. /prime           → See current project structure
3. /prime-suggest   → Get relevant files for task
4. [do work]
5. /summarize       → Capture learnings for next time
```

---

## Current Implementation Status

### ✅ Complete
- `/summarize` command with auto-update logic
- `/recall` command (tested and working)
- `_memory/` file structure
- Standardized filename generation
- master.md template with generic structure

### ⏳ Pending
- `/synthesize` command and implementation
- Synthesis logic (scan + consolidate + cross-reference)
- Auto-load `/recall` via hooks

---

## Future Enhancements

### Considered but Postponed for v1

#### 1. Dynamic Master.md Structure
**Current:** Fixed structure (Status, Decisions, Learnings, Evolution, Questions)
**Future:** Let synthesis agent create structure dynamically based on content
**Why postponed:** Fixed structure provides consistency, works for v1

#### 2. State Tracking (.synthesis-state.json)
**Concept:** Track last synthesis date, processed commits, included conversations
**Benefits:**
- Could show "Last synthesized X days ago"
- Enable incremental synthesis (only new content)
- Performance optimization for large projects
**Why postponed:**
- Over-engineering for initial version
- Full scan every synthesis works fine for reasonable project sizes
- Can add later if synthesis becomes slow

#### 3. Auto-triggered Synthesis
**Concept:** Automatically run synthesis after N conversations or on schedule
**Why postponed:**
- Want manual control initially
- Heavy operation, user should decide when to run
- Can add automation later if workflow proves stable

#### 4. Fuzzy Keyword Matching for Updates
**Concept:** Intelligent matching of new summaries to existing files
**Why rejected:** Too complex, standardized filenames are simpler and work better

#### 5. Conversation Summary Versioning
**Concept:** Keep multiple versions when updating (v1, v2, v3)
**Why rejected:** One conversation = one summary file. Updates replace, not version.

#### 6. Synthesis Diff View
**Concept:** Show what changed in master.md after synthesis
**Future:** Could be helpful to see "what's new" after synthesis runs
**Why postponed:** Add after basic synthesis is working

#### 7. Project-Specific Memory Scopes
**Concept:** Separate memories for sub-projects or domains
**Future:** `_memory/frontend/`, `_memory/backend/`, etc.
**Why postponed:** Single memory scope sufficient for v1

#### 8. Memory Search/Query
**Concept:** Search across summaries and master memory
**Future:** "When did we decide about X?"
**Why postponed:** Can manually read files for now, add if needed

#### 9. Memory Export/Import
**Concept:** Transfer memory between projects or share with team
**Future:** Portable memory for project templates
**Why postponed:** Single-user, single-project focus for v1

---

## Technical Decisions Log

### Why File-Based?
CLI Claude can't access past conversation history like web Claude. Must explicitly capture current conversation before it's lost. Web Claude has backend database + automatic synthesis; we need manual triggers.

### Why Slash Commands Instead of Agents?
- `/summarize`: Lightweight, runs in current conversation
- `/recall`: Lightweight, just reads one file
- `/synthesize`: Heavy operation, but runs in dedicated thread (not background)
- Result: Simpler mental model, user maintains control

### Why Separate Summaries + Master?
**Couldn't we just update master.md directly?**
- Individual summaries = audit trail, can review/refine later
- Master.md = working memory, stays concise
- Separation allows for re-synthesis if master.md structure changes

### Token Management Strategy
- Loading master.md (single file) vs. reading all conversations (many files) = huge difference
- Master memory must stay concise to avoid context window bloat
- Synthesis happens in dedicated thread, so its token usage doesn't affect working conversations

---

## User Preferences

- **Minimize manual decisions** - automate where possible, override only when wrong
- **Simplicity over complexity** - call out overthinking when it happens
- **Flexible but structured** - consistent patterns that adapt to content
- **Multi-project compatible** - must work for coding and non-coding projects

---

## Notes

- Inspired by Claude web's automatic memory feature, adapted for CLI constraints
- Designed to be project-agnostic (works in any folder with any project type)
- Memory is scoped to project folder (each project has its own `_memory/`)
- System is manual-trigger by design (user controls when to capture/synthesize/recall)
