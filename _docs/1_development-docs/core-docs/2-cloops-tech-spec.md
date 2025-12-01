# CLoops Technical Specification

---

## Tech Stack

- **Language:** TypeScript
- **Runtime:** Node.js

---

## External Dependencies

Use MCP server `context7` to fetch latest docs for these services.

### LLM Service
- **API:** OpenAI Responses API (not Chat Completions)
- **Model:** GPT 5.1
- **Docs:** `context7` → `openai responses api`

### Image Generation (Replicate)
- **Models:**
  - Seedream 4: `bytedance/seedream-4`
  - Nano-banana-pro: `google/nano-banana-pro` (TODO: add schema)
- **Docs:** `context7` → `replicate javascript api`

**Seedream 4 Input Schema:**
```typescript
interface Seedream4Input {
  prompt: string;                    // Required - text prompt
  size?: "1K" | "2K" | "4K" | "custom";  // Default: "2K"
  aspect_ratio?: "match_input_image" | "1:1" | "4:3" | "3:4" | "16:9" | "9:16" | "3:2" | "2:3" | "21:9";
  width?: number;                    // 1024-4096, only when size="custom"
  height?: number;                   // 1024-4096, only when size="custom"
  enhance_prompt?: boolean;          // Default: true
  image_input?: string[];            // URLs for img2img
  sequential_image_generation?: "disabled" | "auto";  // Default: "disabled"
  max_images?: number;               // 1-15, used with sequential_image_generation="auto"
}
```

### CLI
- **Library:** Commander.js

---

## Decisions

1. **Execution runtime** - Custom scripts. No SDK for MVP.
2. **Backlog format** - JSON file.
3. **Config injection** - Simple string replace with `{variable}` syntax.
4. **Image gen parallelization** - Sequential for MVP. Parallel is a later optimization.
5. **Error handling** - Log error and fail. No automatic retries for MVP.

## Future Considerations

### Cloud Deployment
MVP writes bundles to local disk. For cloud deployment (e.g., Firebase Functions):
- No persistent local filesystem in serverless
- Bundle output goes directly to cloud storage
- Consider function timeout limits (9-60 min depending on generation)
- Parallel generation could leverage multiple function instances

---

## 1. System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                          CLI                                │
│                    cloops run <template>                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   Execution Engine                          │
│  - Loads template config                                    │
│  - Fetches input from datasource                            │
│  - Runs steps sequentially                                  │
│  - Passes state between steps                               │
└──────┬──────────────┬──────────────┬───────────────────────┘
       │              │              │
       ▼              ▼              ▼
┌────────────┐ ┌────────────┐ ┌────────────┐
│ LLM Service│ │ Gen Service│ │Storage Svc │
│  (OpenAI)  │ │ (Replicate)│ │  (Files)   │
└────────────┘ └────────────┘ └────────────┘
```

**Data flow:** CLI → Load template → Fetch input → Run steps (LLM → LLM → LLM → Generate) → Write bundle

---

## 2. Project Structure

```
cloops/
├── src/
│   ├── cli.ts                # Entry point
│   ├── engine/
│   │   └── runner.ts         # Step orchestration
│   ├── services/
│   │   ├── llm.ts            # OpenAI API calls
│   │   ├── generation.ts     # Replicate API calls
│   │   └── storage.ts        # File operations
│   ├── datasource/
│   │   ├── backlog.ts        # JSON backlog
│   │   └── csv.ts            # CSV datasource
│   ├── utils/
│   │   └── config.ts         # Config loading, variable injection
│   └── types/
│       └── index.ts          # Shared type definitions
├── templates/
│   └── comic-books-standard/
│       ├── config.json
│       ├── production-plan.md
│       └── prompts/
│           ├── step1-system.txt
│           ├── step2-system.txt
│           └── step3-system.txt
├── data/
│   └── backlogs/
│       └── comic-books-standard.json
├── output/
│   └── comic-books/
│       └── {story-id}/
│           ├── 1.jpg
│           ├── story-data.json
│           └── ...
├── package.json
└── tsconfig.json
```

---

## 3. CLI Implementation

**Commands:**
```bash
cloops run <template>           # Full run (default)
cloops run <template> --dry     # Dry run (LLM only)
cloops run <template> --item <id>  # Run specific item
cloops templates                # List available templates
cloops status <template>        # Show backlog status
```

**Implementation:**
- Use `commander` or `yargs` for arg parsing
- Config overrides via flags: `--pages 3`
- Output: console logs for progress, errors to stderr

---

## 4. Template System

**Template discovery:**
- Scan `templates/` folder
- Each subfolder with `config.json` is a valid template

**Template loading:**
```typescript
interface Template {
  config: TemplateConfig;
  prompts: Record<string, string>;
}

function loadTemplate(name: string): Template {
  const basePath = `templates/${name}`;
  return {
    config: JSON.parse(readFileSync(`${basePath}/config.json`, 'utf-8')),
    prompts: {
      step1: readFileSync(`${basePath}/prompts/step1-system.txt`, 'utf-8'),
      step2: readFileSync(`${basePath}/prompts/step2-system.txt`, 'utf-8'),
      // ...
    }
  };
}
```

**Prompts:** Stored as plain text files. Loaded at runtime, variables injected.

---

## 5. Config System

**Config structure (config.json):**
```json
{
  "name": "comic-books-standard",
  "datasource": "backlog",
  "steps": ["narrative", "planning", "prompts", "thumbnail", "generation", "bundle"],
  "settings": {
    "pageCount": { "min": 3, "max": 5 },
    "panelsPerPage": 3
  },
  "style": {
    "artStyle": "children's book illustration",
    "inkStyle": "bold ink lines"
  },
  "generation": {
    "service": "replicate",
    "model": "bytedance/seedream-3.0",
    "params": {
      "size": "2K",
      "aspect_ratio": "9:16"
    }
  }
}
```

**Variable injection:**
```typescript
function injectVariables(template: string, variables: Record<string, unknown>): string {
  return template.replace(/\{(\w+(?:\.\w+)*)\}/g, (match, path) => {
    return getNestedValue(variables, path) ?? match;
  });
}

// Usage:
// "Style: {style.artStyle}" → "Style: children's book illustration"
```

**Runtime overrides:** CLI flags merge into config before execution.

---

## 6. Execution Engine

**Step orchestration:**
```typescript
interface RunOptions {
  dry: boolean;
}

interface State {
  input: StoryInput;
  narrative?: string;
  pages?: Page[];
  prompts?: string[];
  images?: string[];
}

async function runTemplate(template: Template, input: StoryInput, options: RunOptions): Promise<State> {
  let state: State = { input };

  for (const stepName of template.config.steps) {
    // Skip generation step in dry run
    if (options.dry && stepName === 'generation') {
      console.log(`[DRY RUN] Skipping: ${stepName}`);
      continue;
    }

    console.log(`Running: ${stepName}`);
    state = await runStep(stepName, template, state);
  }

  return state;
}
```

**State passing:** Each step receives previous state, returns updated state.
```typescript
// State shape evolves through steps:
// After step1: { input, narrative }
// After step2: { input, narrative, pages }
// After step3: { input, narrative, pages, prompts }
// etc.
```

**Error handling:** On failure, log error with step name and context, then exit.

---

## 7. Datasource Manager

**Backlog schema (JSON file):**
```json
{
  "templateId": "comic-books-standard",
  "items": [
    {
      "id": "david-and-goliath",
      "status": "pending",
      "input": {
        "title": "David and Goliath",
        "summary": "Boy defeats giant warrior with sling",
        "keyMoments": ["battle", "stone throw", "giant falling"]
      },
      "completedAt": null
    }
  ]
}
```

**Status values:** `pending`, `in_progress`, `completed`, `failed`

**Operations:**
```typescript
// Fetch next pending item
function getNextItem(backlog: Backlog): BacklogItem | undefined {
  return backlog.items.find(i => i.status === 'pending');
}

// Mark complete
function markComplete(backlog: Backlog, itemId: string): void {
  const item = backlog.items.find(i => i.id === itemId);
  if (item) {
    item.status = 'completed';
    item.completedAt = new Date().toISOString();
    saveBacklog(backlog);
  }
}
```

**Modular architecture:** Datasource interface:
```typescript
interface Datasource {
  getNextItem(): BacklogItem | null;
  markComplete(itemId: string): void;
  markFailed(itemId: string, error: string): void;
}
```
Backlog and CSV implement this interface. New datasources can be added.

---

## 8. Services

### 8.1 LLM Service

**OpenAI integration:**
```typescript
interface LLMCallParams {
  systemPrompt: string;
  userMessage: string;
  schema?: object;
}

async function llmCall<T = string>({ systemPrompt, userMessage, schema }: LLMCallParams): Promise<T> {
  const messages: ChatCompletionMessageParam[] = [
    { role: 'system', content: systemPrompt },
    { role: 'user', content: userMessage }
  ];

  const options: ChatCompletionCreateParams = {
    model: 'gpt-4o',
    messages
  };

  // Structured output if schema provided
  if (schema) {
    options.response_format = {
      type: 'json_schema',
      json_schema: { name: 'response', schema }
    };
  }

  const response = await openai.chat.completions.create(options);
  const content = response.choices[0].message.content ?? '';
  return schema ? JSON.parse(content) : content as T;
}
```

### 8.2 Generation Service

**Replicate integration:**
```typescript
interface GenerateImageParams {
  model: string;
  prompt: string;
  params: Record<string, unknown>;
}

async function generateImage({ model, prompt, params }: GenerateImageParams): Promise<string> {
  const prediction = await replicate.run(model, {
    input: { prompt, ...params }
  });

  // prediction is URL or array of URLs
  const imageUrl = Array.isArray(prediction) ? prediction[0] : prediction;

  // Download and return local path
  return downloadFile(imageUrl as string);
}
```

**Sequential generation:**
```typescript
async function generatePages(prompts: string[], config: TemplateConfig): Promise<string[]> {
  const results: string[] = [];
  for (let i = 0; i < prompts.length; i++) {
    console.log(`Generating page ${i + 1}/${prompts.length}...`);
    const path = await generateImage({
      model: config.generation.model,
      prompt: prompts[i],
      params: config.generation.params
    });
    results.push(path);
  }
  return results;
}
```

### 8.3 Storage Service

**Bundle output:**
```typescript
interface BundleData {
  title: string;
  images: string[];
  pages: Page[];
}

function writeBundle(storyId: string, templateName: string, data: BundleData): void {
  const outputDir = `output/${templateName}/${storyId}`;
  mkdirSync(outputDir, { recursive: true });

  // Copy images
  data.images.forEach((img, i) => {
    copyFileSync(img, `${outputDir}/${i + 1}.jpg`);
  });

  // Write metadata
  writeFileSync(`${outputDir}/story-data.json`, JSON.stringify({
    storyId,
    title: data.title,
    totalPages: data.pages.length,
    pages: data.pages.map((p, i) => ({
      pageNumber: i + 1,
      imageFile: `${i + 1}.jpg`,
      narration: p.narration
    }))
  }, null, 2));
}
```

---

## 9. Knowledge Layer

**Location:** `src/knowledge/` or inline in template prompts.

**Contents:**
- Block system definitions
- Assembly rules
- Visual-only principle

**Injection:** Appended to Step 3 system prompt:
```typescript
function buildStep3Prompt(template: Template): string {
  const basePrompt = template.prompts.step3;
  const knowledge = readFileSync('src/knowledge/prompting.md', 'utf-8');
  return `${basePrompt}\n\n<knowledge>\n${knowledge}\n</knowledge>`;
}
```

**For MVP:** Keep knowledge inline in step3 prompt file. Extract to shared file later if multiple templates need it.

---

## 10. Post-Processing

**MVP:** Not implemented. Bundles written to local disk.

**Future:**
```typescript
async function postProcess(bundlePath: string, config: TemplateConfig): Promise<void> {
  // 1. Upload to cloud storage
  const urls = await uploadToStorage(bundlePath);

  // 2. Transform to AdLoops format
  const manifest = transformToAdLoops(bundlePath, urls);

  // 3. Write to Firestore
  await firestore.collection('bodies').add(manifest);
}
```

---

## 11. Testing Strategy

**Dry run as primary validation:**
- Run `cloops run comic-books-standard --dry`
- Validates: config loading, datasource, LLM calls, prompt assembly
- Outputs generated prompts for review

**Manual end-to-end:**
- Run full pipeline on one story
- Verify output bundle structure
- Check image quality

**Unit tests (later):**
- Config loading
- Variable injection
- Datasource operations

---

## 12. Type Definitions

All shared types in `src/types/index.ts`:

```typescript
// ===================
// Template Types
// ===================

interface Template {
  config: TemplateConfig;
  prompts: Record<string, string>;
}

interface TemplateConfig {
  name: string;
  datasource: 'backlog' | 'csv';
  steps: StepName[];
  settings: TemplateSettings;
  style: StyleConfig;
  generation: GenerationConfig;
}

type StepName = 'narrative' | 'planning' | 'prompts' | 'thumbnail' | 'generation' | 'bundle';

interface TemplateSettings {
  pageCount: { min: number; max: number };
  panelsPerPage: number;
}

interface StyleConfig {
  artStyle: string;
  inkStyle: string;
  colorTreatment?: string;
}

interface GenerationConfig {
  service: 'replicate' | 'comfyui';
  model: string;
  params: Record<string, unknown>;
}

// ===================
// Datasource Types
// ===================

interface Datasource {
  getNextItem(): BacklogItem | null;
  markComplete(itemId: string): void;
  markFailed(itemId: string, error: string): void;
}

interface Backlog {
  templateId: string;
  items: BacklogItem[];
}

interface BacklogItem {
  id: string;
  status: ItemStatus;
  input: StoryInput;
  completedAt: string | null;
  error?: string;
}

type ItemStatus = 'pending' | 'in_progress' | 'completed' | 'failed';

// ===================
// Story/Content Types
// ===================

interface StoryInput {
  title: string;
  summary: string;
  keyMoments: string[];
}

interface Page {
  pageNumber: number;
  title: string;
  narration: string;
  panels: Panel[];
}

interface Panel {
  panel: number;
  moment: string;
  visualAnchor: string;
}

interface PagePrompt {
  pageNumber: number;
  prompt: string;
}

// ===================
// Execution Types
// ===================

interface RunOptions {
  dry: boolean;
  item?: string;  // Specific item ID to run
}

interface State {
  input: StoryInput;
  narrative?: string;
  pages?: Page[];
  prompts?: PagePrompt[];
  thumbnailPrompt?: string;
  images?: string[];
  thumbnailImage?: string;
}

// ===================
// Service Types
// ===================

interface LLMCallParams {
  systemPrompt: string;
  userMessage: string;
  schema?: object;
}

interface GenerateImageParams {
  model: string;
  prompt: string;
  params: Record<string, unknown>;
}

// ===================
// Output Types
// ===================

interface BundleData {
  title: string;
  images: string[];
  pages: Page[];
  thumbnailImage?: string;
}

interface StoryDataJson {
  storyId: string;
  title: string;
  thumbnailFile?: string;
  totalPages: number;
  pages: {
    pageNumber: number;
    imageFile: string;
    narration: string;
  }[];
}
```

---

*v1 - 2025-11-28*
