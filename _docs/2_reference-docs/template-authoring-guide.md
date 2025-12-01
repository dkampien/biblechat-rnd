# Template Authoring Guide

How to create new CLoops templates.

---

## Folder Structure

```
templates/my-template/
├── config.json       # Settings, parameters, generation config
├── workflow.ts       # Workflow logic (the brain)
├── prompts/          # LLM prompts as .txt files
│   └── *.txt
└── schemas/          # JSON schemas for structured LLM outputs
    └── *.json
```

---

## config.json

Settings only. No step definitions (workflow.ts handles that).

```json
{
  "name": "my-template",
  "datasource": "backlog",
  "settings": {
    "exampleSetting": 123
  },
  "style": {
    "artStyle": "..."
  },
  "generation": {
    "service": "replicate",
    "model": "owner/model-name",
    "params": {
      "aspect_ratio": "9:16"
    }
  }
}
```

---

## workflow.ts

Must export a `run` function with this signature:

```typescript
import type {
  StoryInput,
  TemplateConfig,
  Services,
  WorkflowContext,
} from '../../src/types/index.js';

export async function run(
  input: StoryInput,
  config: TemplateConfig,
  services: Services,
  ctx: WorkflowContext
): Promise<void> {
  // Your workflow logic here
}
```

### Parameters

| Param | Description |
|-------|-------------|
| `input` | Story input from datasource (`title`, `summary`, `keyMoments`) |
| `config` | Template config from config.json |
| `services` | Injected services (`llm`, `replicate`, `storage`) |
| `ctx` | Context (`prompts`, `schemas`, `dry`, `templatePath`) |

### Using Services

**LLM call with JSON schema:**
```typescript
const result = await services.llm.call<{ fieldName: string }>({
  systemPrompt: ctx.prompts['my-prompt'],
  userMessage: 'User input here',
  schema: ctx.schemas['my-schema'],
});
console.log(result.fieldName);
```

**Image generation:**
```typescript
const imagePath = await services.replicate.generateImage(prompt, config.generation);
const imagePaths = await services.replicate.generateImages(prompts, config.generation);
```

**Write bundle:**
```typescript
services.storage.writeBundle(storyId, {
  title: input.title,
  images: imagePaths,
  pages: pagesData,
  thumbnailImage: thumbnailPath,
});
```

### Dry Run Handling

Skip generation steps when `ctx.dry` is true:

```typescript
if (ctx.dry) {
  console.log('[DRY RUN] Skipping generation');
  return;
}

// Generation code here
```

### Variable Injection

Use `injectVariables` to replace `{variable}` placeholders in prompts:

```typescript
import { injectVariables } from '../../src/utils/config.js';

let prompt = ctx.prompts['my-prompt'];
prompt = injectVariables(prompt, {
  artStyle: config.style.artStyle,
  setting: 'custom value',
});
```

---

## prompts/*.txt

Plain text files. Access via `ctx.prompts['filename']` (without .txt extension).

Example `prompts/narrative.txt`:
```
You are a storyteller. Create a narrative for the given story.
Style: {artStyle}
Keep it under {wordCount} words.
```

---

## schemas/*.json

JSON Schema format. Access via `ctx.schemas['filename']` (without .json extension).

Example `schemas/narrative.json`:
```json
{
  "type": "object",
  "properties": {
    "narrative": {
      "type": "string",
      "description": "The story narrative"
    },
    "keyMoments": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "required": ["narrative", "keyMoments"],
  "additionalProperties": false
}
```

---

## Backlog

Create `data/backlogs/my-template.json`:

```json
{
  "templateId": "my-template",
  "items": [
    {
      "id": "item-1",
      "status": "pending",
      "input": {
        "title": "Example Title",
        "summary": "Example summary",
        "keyMoments": ["moment 1", "moment 2"]
      },
      "completedAt": null
    }
  ]
}
```

---

## Running

```bash
cloops run my-template --dry    # Test without generation
cloops run my-template          # Full run
cloops status my-template       # Check backlog status
```

---

## Reference

See `templates/comic-books-standard/` for a complete working example.
