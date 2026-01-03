---
description: Search conversation history for keywords across all project conversations
argument-hint: [search-term]
allowed-tools: Bash(ls:*), Bash(cat:*), Bash(jq:*), Bash(grep:*), Bash(wc:*), Bash(sort:*)
---

# Search Conversation History

Search for: **$ARGUMENTS**

## Instructions

### Step 1: Locate Project Folder

1. Get current working directory: `pwd`
2. Find the corresponding folder in `~/.claude/projects/` that matches this project
   - The folder name will be a transformed version of the current path (slashes and spaces converted to dashes)
   - Use `ls ~/.claude/projects/` to list available project folders
   - Match the current directory path to the correct folder name

### Step 2: Find Matching Files (Quick Filter)

Use grep to find which conversations contain the search term:

```bash
cd ~/.claude/projects/{PROJECT_FOLDER}/ && grep -l -i "$ARGUMENTS" *.jsonl 2>/dev/null
```

This quickly filters ~886 files down to ~10-15 relevant conversations.

### Step 3: Get Accurate Counts (Top Results Only)

For each file from Step 2, run this single chained command:

```bash
echo "File: FILENAME.jsonl" && \
echo "User: $(cat FILENAME.jsonl | jq -r 'select(.type=="user") | .message | if .content | type == "array" then (.content[] | select(.type == "text") | .text) else .content end' 2>/dev/null | grep -o -i "$ARGUMENTS" | wc -l | tr -d ' ')" && \
echo "Assistant: $(cat FILENAME.jsonl | jq -r 'select(.type=="assistant") | .message.content[] | select(.type == "text") | .text' 2>/dev/null | grep -o -i "$ARGUMENTS" | wc -l | tr -d ' ')" && \
echo "Last: $(cat FILENAME.jsonl | jq -r 'select(.type=="user" or .type=="assistant") | .timestamp' 2>/dev/null | sort | tail -1)"
```

This gives you all data in one command per file (instead of 3 separate commands).

### Step 4: Rank and Display Results

1. Sort conversations by total mention count (descending)
2. Display top 10 results

**Output format:**
```
Found "SEARCH_TERM" in X conversations (Y total mentions)

Ranked by relevance:

1. session-uuid-1 - 48 mentions - Nov 24, 2025
2. session-uuid-2 - 35 mentions - Nov 27, 2025
3. session-uuid-3 - 27 mentions - Dec 1, 2025
...
```

### Notes

- Only count actual conversation text (exclude tool_results, thinking blocks, etc.)
- Show full session UUIDs (not truncated)
- Include last activity date for context
- Search is case-insensitive
