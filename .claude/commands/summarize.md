---
description: Summarize conversation for project memory
---

Analyze this conversation and create a summary to preserve important context for future conversations.

## Instructions

1. **Review the conversation** and identify what's worth preserving. Consider:
   - Decisions made (technical, architectural, process)
   - Discoveries and learnings (what worked, what didn't)
   - Status changes (project phase, implementation progress)
   - Blockers or open questions
   - Failed approaches and why they didn't work
   - Patterns or preferences established
   - Important context for future work

2. **Be flexible** - Not every conversation will have all types of tracking points. Focus on what's actually relevant and important.

3. **Create a summary** using this structure:

```markdown
# [Short descriptive title]

## Context
[1-2 sentences: What was this conversation about?]

## Tracking Points
- [Flexible list of important items - use clear labels like "Decision:", "Discovery:", "Blocker:", "Status:", etc.]
- [Focus on information that would be valuable in future conversations]
- [Include rationale where relevant - the "why" matters]

## Related Files/Artifacts (optional)
[If files were created, modified, or are particularly relevant]
```

4. **Present the summary** to the user for review and approval

5. **Generate standardized filename:**
   - Convert summary title to filename format:
     - Lowercase, replace spaces with dashes
     - Keep only key terms (remove filler words like "for", "the", "and")
     - Add date prefix: `YYYY-MM-DD-`
     - Example: "Designing Project Memory System" → `2025-01-04-memory-system-design.md`

6. **Check if file exists:**
   - Run `ls _memory/conversations/` to list existing files
   - Check if the generated filename exists
   - **If exists:** Update that file
   - **If doesn't exist:** Create new file

7. **Auto-announce action:**
   - "Updating `[filename].md`" or "Creating new `[filename].md`"
   - User can override by providing different filename

8. **Save the summary:**
   - Write to `_memory/conversations/[filename].md`

**Important:**
- This summary is for FUTURE conversations, not a transcript
- Be concise but preserve critical context
- The user may work on both coding and non-coding projects - adapt accordingly
- Focus on what would help you (Claude) provide better assistance in future conversations
- One conversation can have multiple updates - later `/summarize` calls should update the same file
- User maintains control over whether to update existing or create new
