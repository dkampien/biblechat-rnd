---
description: Suggest relevant files based on current conversation context
---

## Analyze Current Context
Based on our current conversation and task:

1. **Review what we're working on** from the conversation so far
2. **Suggest relevant files** that would help:
   - List specific file paths
   - Group by category (Frontend, Backend, Config, Docs, etc.)
   - Include brief reason why each would be helpful

3. **Wait for user confirmation**
   - DO NOT load anything automatically
   - User will confirm, modify, or add to the list

4. **Load only confirmed files** using @ syntax
   - After loading, ask: "Any other files you need?"

## Usage
- Run anytime during conversation when you need relevant file suggestions
- Works best after describing your task or problem
- Can be used multiple times as task evolves

## Examples
- After describing auth bug → Suggests auth-related files
- After mentioning performance → Suggests metrics, config, bottleneck areas
- After discussing UI issue → Suggests components, styles, layouts