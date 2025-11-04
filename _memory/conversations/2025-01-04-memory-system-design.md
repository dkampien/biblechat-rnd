# Designing Project Memory System for Claude Code

## Context
Designed, implemented, and iteratively refined a cross-conversation memory system for Claude Code CLI, including successful testing of `/recall` and multiple improvements to `/summarize` command logic.

## Tracking Points

- **Decision: Three-command architecture**
  - `/summarize` - Captures current conversation into individual summary file
  - `/synthesize` - Runs synthesis agent to consolidate all summaries + codebase scan into master memory
  - `/recall` - Loads master.md into context for new conversations
  - Rationale: Clear separation of concerns, each command has distinct purpose

- **Decision: Dual-write synthesis approach**
  - Save individual summary AND update master.md immediately
  - Alternative (synthesize-on-load) rejected due to token consumption
  - Rationale: Keeps master.md always current, loading is fast and token-efficient

- **Decision: Master memory as synthesis, not verbatim**
  - Individual summaries contain detailed tracking points
  - Master.md consolidates and distills across conversations by theme
  - Rationale: Keeps master.md concise, avoids token limit issues

- **Decision: Iterative summary updates with standardized filenames**
  - `/summarize` can be run multiple times in same conversation
  - Generates standardized filename from title (date-prefix + lowercase-dashes)
  - Checks if exact filename exists → update if yes, create if no
  - No fuzzy matching - simple `ls` check for exact filename
  - Rationale: Minimal manual decisions, automated but predictable

- **Decision: Synthesis agent over slash command**
  - Synthesis requires heavy operations: codebase scanning, git commits review
  - Agent provides independent context window
  - Rationale: Computational efficiency, separation of concerns

- **Discovery: `/recall` successfully tested**
  - Tested in fresh conversation with populated master.md
  - Met all success criteria: technical, functional, and UX
  - Validates core concept works end-to-end

- **Discovery: `/prime` commands complement memory system**
  - `/prime` + `/prime-suggest` = session setup & file discovery (current state)
  - `/recall` = project memory & continuity (historical context)
  - No overlap, complementary purposes
  - Ideal flow: `/recall` → `/prime` → `/prime-suggest` → work → `/summarize`

- **Pattern: Flexible "tracking points" structure**
  - Adapts to conversation content, not rigid categories
  - Clear labels: Decision:, Discovery:, Blocker:, Status:, Failed approach:, Pattern:
  - Works for coding and non-coding projects

- **Pattern: Minimize manual decisions**
  - Rejected "list and pick" approach (too manual)
  - Rejected fuzzy keyword matching (too complex)
  - Chose standardized filename generation (automated + predictable)
  - User preference: automate where possible, override only when wrong

- **Status: Memory system foundation complete**
  - ✅ `/summarize` command working with auto-update logic
  - ✅ `/recall` command working and tested successfully
  - ✅ `_memory/` structure created
  - ✅ Master.md manually populated and tested
  - ⏳ `/synthesize` agent not built yet

- **User preference: Simplicity over complexity**
  - Explicit request to avoid overcomplication
  - Call out overthinking when it happens
  - Keep designs simple, pragmatic, automated

## Related Files/Artifacts

- `.claude/commands/summarize.md` - Iteratively refined with standardized filename logic
- `.claude/commands/recall.md` - Created and tested successfully
- `.claude/commands/prime.md` - Existing command, confirmed complementary
- `.claude/commands/prime-suggest.md` - Existing command, confirmed complementary
- `_memory/conversations/` - Directory for individual summaries
- `_memory/master.md` - Synthesized project memory (manually populated for testing)
