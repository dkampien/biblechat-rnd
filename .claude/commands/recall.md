---
description: Load project memory into context
---

Load the synthesized project memory to restore context from previous conversations.

## Instructions

1. **Read the master memory file:**
   `_memory/master.md`

2. **Acknowledge what you've loaded:**
   - Briefly mention key project status
   - Note any important recent decisions
   - Highlight active blockers if present

3. **Be ready to reference this context:**
   - Use this memory naturally throughout the conversation
   - Don't just read and forget - actively integrate this context
   - When user asks about past decisions, reference the memory

4. **If master.md is empty or placeholder:**
   - Inform the user no memory has been synthesized yet
   - Suggest running `/summarize` after conversations to build memory

**Important:**
- This loads synthesized memory from ALL previous conversations
- The memory is distilled and organized by theme, not chronological
- Always reference this context when relevant to current discussion
