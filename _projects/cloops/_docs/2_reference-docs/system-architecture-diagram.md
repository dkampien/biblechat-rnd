# CLoops System Architecture

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              CLI (cli.ts)                               │
│  Commands: run | templates | status | extract | stories                 │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         │                           │                           │
         ▼                           ▼                           ▼
┌─────────────────┐      ┌─────────────────────┐      ┌─────────────────┐
│ Template Loader │      │    Engine/Runner    │      │   Datasource    │
│   (loader.ts)   │      │    (runner.ts)      │      │   (index.ts)    │
│                 │      │                     │      │                 │
│ • Scan templates│      │ • Orchestrates runs │      │ • Story backlog │
│ • Load configs  │      │ • Creates services  │      │ • Status track  │
│ • Import flows  │      │ • Builds context    │      │ • Extraction    │
└────────┬────────┘      └──────────┬──────────┘      └────────┬────────┘
         │                          │                          │
         └──────────────────────────┼──────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          Template Workflow                              │
│                     (templates/{name}/workflow.ts)                      │
│                                                                         │
│   Step 1 → Step 2 → Step 3 → Step 4 → Step 5 → Step 6                  │
│  Narrative  Planning  Prompts  Thumbnail  Images   Bundle              │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         │                           │                           │
         ▼                           ▼                           ▼
┌─────────────────┐      ┌─────────────────────┐      ┌─────────────────┐
│   LLM Service   │      │  Replicate Service  │      │ Storage Service │
│    (llm.ts)     │      │   (replicate.ts)    │      │  (storage.ts)   │
│                 │      │                     │      │                 │
│ OpenAI gpt-5.1  │      │ Seedream-4 images   │      │ File I/O        │
│ Structured JSON │      │ Async generation    │      │ JSON bundles    │
└─────────────────┘      └─────────────────────┘      └─────────────────┘
```

---

## Data Flow Pipeline

```
┌──────────────────────────────────────────────────────────────────────┐
│                           INPUT LAYER                                │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Bible API (api.bible)                                               │
│       │                                                              │
│       ▼                                                              │
│  ┌─────────────────┐    ┌─────────────────────────────────────┐     │
│  │ Story Extractor │───▶│ Universal Pool (universal.json)     │     │
│  │ (LLM analysis)  │    │ • id, title, summary, keyMoments    │     │
│  └─────────────────┘    └──────────────────┬──────────────────┘     │
│                                            │                         │
│                                            ▼                         │
│                         ┌─────────────────────────────────────┐     │
│                         │ Template Backlogs                   │     │
│                         │ (template-backlogs/{template}.json) │     │
│                         │ • status: pending/in_progress/done  │     │
│                         └─────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        PROCESSING LAYER                              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐  │
│  │  Step 1    │   │  Step 2    │   │  Step 3    │   │  Step 4    │  │
│  │ Narrative  │──▶│ Planning   │──▶│ Prompts    │──▶│ Thumbnail  │  │
│  │            │   │            │   │            │   │            │  │
│  │ LLM call   │   │ LLM call   │   │ LLM call   │   │ LLM call   │  │
│  │ + schema   │   │ + schema   │   │ + schema   │   │ + schema   │  │
│  └────────────┘   └────────────┘   └────────────┘   └────────────┘  │
│                                            │                         │
│                                            ▼                         │
│                              ┌─────────────────────────┐            │
│                              │   Save prompts.md       │            │
│                              │   (enables --replay)    │            │
│                              └─────────────────────────┘            │
│                                            │                         │
│                                            ▼                         │
│                              ┌─────────────────────────┐            │
│                              │  Step 5: Image Gen      │            │
│                              │  Replicate (Seedream-4) │            │
│                              │  • Page images 1-4      │            │
│                              │  • Thumbnail image      │            │
│                              └─────────────────────────┘            │
│                                            │                         │
│                                            ▼                         │
│                              ┌─────────────────────────┐            │
│                              │  Step 6: Bundle         │            │
│                              │  Write story-data.json  │            │
│                              └─────────────────────────┘            │
└──────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌──────────────────────────────────────────────────────────────────────┐
│                          OUTPUT LAYER                                │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  output/{template}/{seq}-{story-id}/                                 │
│  ├── 1.jpg              Page 1 image                                 │
│  ├── 2.jpg              Page 2 image                                 │
│  ├── 3.jpg              Page 3 image                                 │
│  ├── 4.jpg              Page 4 image                                 │
│  ├── thumbnail.jpg      Cover image                                  │
│  ├── prompts.md         All LLM outputs (for replay)                 │
│  └── story-data.json    Final metadata bundle                        │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Template System Structure

```
templates/{template-name}/
│
├── config.json                 Template metadata & settings
│   ├── name                    Template identifier
│   ├── datasource              Which datasource to use
│   ├── settings                Page count, panels per page, etc.
│   ├── style                   Art style, ink style, colors
│   └── generation              Model config (replicate/seedream-4)
│
├── workflow.ts                 Step execution logic
│   └── export default run()    Main workflow function
│
├── system-prompts/             LLM system prompts
│   ├── step1-narrative.md      Story narrative generation
│   ├── step2-planning.md       Page/panel breakdown
│   ├── step3-prompts.md        Image prompt generation
│   └── step4-thumbnail.md      Cover prompt generation
│
└── schemas/                    JSON schemas for LLM output
    ├── narrative.json          { narrative: string }
    ├── planning.json           { pages: Page[] }
    ├── prompts.json            { prompts: PagePrompt[] }
    └── thumbnail.json          { prompt: string }
```

---

## Service Dependencies

```
┌─────────────────────────────────────────────────────────────────────┐
│                         EXTERNAL SERVICES                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────┐                                                │
│  │    OpenAI API   │  Model: gpt-5.1                                │
│  │ (Responses API) │  Purpose: Story generation, planning, prompts  │
│  │                 │  Features: Structured JSON output, reasoning   │
│  └────────┬────────┘                                                │
│           │                                                         │
│           ▼                                                         │
│  ┌─────────────────┐                                                │
│  │  Replicate API  │  Model: bytedance/seedream-4                   │
│  │                 │  Purpose: Image generation                     │
│  │                 │  Output: 2K resolution, 3:4 aspect             │
│  └────────┬────────┘                                                │
│           │                                                         │
│           ▼                                                         │
│  ┌─────────────────┐                                                │
│  │   Bible API     │  Version: Berean Standard Bible                │
│  │  (api.bible)    │  Purpose: Scripture content for extraction     │
│  │                 │  Usage: Story discovery & text retrieval       │
│  └─────────────────┘                                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `run <template>` | Execute template workflow | `cloops run comic-books-standard` |
| `run --dry` | LLM only, skip image generation | `cloops run comic-books-standard --dry` |
| `run --replay` | Regenerate images from saved prompts | `cloops run comic-books-standard --replay` |
| `run --batch N` | Process N items | `cloops run comic-books-standard --batch 5` |
| `run --all` | Process all pending items | `cloops run comic-books-standard --all` |
| `run --item ID` | Process specific item | `cloops run comic-books-standard --item story-123` |
| `templates` | List available templates | `cloops templates` |
| `status <template>` | Show backlog status | `cloops status comic-books-standard` |
| `extract` | Extract stories from Bible | `cloops extract` |
| `stories` | Show extraction status | `cloops stories` |

---

## Key Design Principles

1. **Thin Engine, Rich Templates** — Core logic lives in template `workflow.ts`, not the engine
2. **Stateless CLI** — Status derived from filesystem (no database)
3. **Replay Capability** — Save LLM outputs early → regenerate images without re-running LLM
4. **Schema-Driven** — All LLM calls use JSON schemas for structured output
5. **Fault Tolerance** — Failed items auto-retried, partial state recoverable via `--replay`
6. **Modular Services** — LLM, Replicate, Storage can be swapped/extended
