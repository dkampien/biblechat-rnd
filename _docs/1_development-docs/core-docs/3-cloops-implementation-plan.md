# CLoops Implementation Plan

Based on PRD and Tech Spec. Steps are designed to be atomic and build on each other.

---

## Phase 1: Project Foundation

### Step 1.1: Project Setup `[ ]`
- **Task:** Initialize Node.js project with TypeScript configuration, folder structure, and dependencies.
- **Files:**
  - `cloops/package.json`
  - `cloops/tsconfig.json`
  - `cloops/.gitignore`
  - `cloops/src/index.ts` (placeholder entry)
- **Dependencies:** None
- **Validation:** `npm install` completes, `npm run build` compiles without errors.
- **Implementation Notes:**
  - Dependencies: `typescript`, `openai`, `replicate`, `commander` (CLI), `dotenv`
  - Dev dependencies: `@types/node`, `tsx` (for running TS directly during dev)

### Step 1.2: Type Definitions `[ ]`
- **Task:** Create all shared TypeScript interfaces from tech spec Section 12.
- **Files:**
  - `cloops/src/types/index.ts`
- **Dependencies:** Step 1.1
- **Validation:** Types compile without errors, can be imported in other files.
- **Implementation Notes:** Copy types from tech spec, export all interfaces.

### Step 1.3: Environment Config `[ ]`
- **Task:** Set up environment variable handling for API keys.
- **Files:**
  - `cloops/.env.example`
  - `cloops/src/utils/env.ts`
- **Dependencies:** Step 1.1
- **Validation:** Missing env vars throw clear error on startup.
- **Implementation Notes:** Required vars: `OPENAI_API_KEY`, `REPLICATE_API_TOKEN`

---

## Phase 2: Services

### Step 2.1: LLM Service `[ ]`
- **Task:** Implement OpenAI API wrapper with structured output support.
- **Files:**
  - `cloops/src/services/llm.ts`
- **Dependencies:** Step 1.2, Step 1.3
- **Validation:** Can make a test call to OpenAI, returns expected response.
- **Implementation Notes:**
  - Support both plain text and JSON schema responses
  - Use `gpt-4o` as default model
  - Handle API errors gracefully

### Step 2.2: Generation Service `[ ]`
- **Task:** Implement Replicate API wrapper for image generation.
- **Files:**
  - `cloops/src/services/generation.ts`
- **Dependencies:** Step 1.2, Step 1.3
- **Validation:** Can generate a test image, downloads to local path.
- **Implementation Notes:**
  - Accept model, prompt, and params
  - Download generated image to temp location
  - Return local file path

### Step 2.3: Storage Service `[ ]`
- **Task:** Implement file operations for bundle output.
- **Files:**
  - `cloops/src/services/storage.ts`
- **Dependencies:** Step 1.2
- **Validation:** Can create output folder, copy files, write JSON metadata.
- **Implementation Notes:**
  - Create directories recursively
  - Write story-data.json with proper structure
  - Handle file copy operations

---

## Phase 3: Datasource

### Step 3.1: Datasource Interface `[ ]`
- **Task:** Define abstract datasource interface and types.
- **Files:**
  - `cloops/src/datasource/types.ts`
- **Dependencies:** Step 1.2
- **Validation:** Interface compiles, can be implemented.
- **Implementation Notes:** Interface with `getNextItem`, `markComplete`, `markFailed`, `markInProgress`

### Step 3.2: Backlog Datasource `[ ]`
- **Task:** Implement JSON file backlog datasource.
- **Files:**
  - `cloops/src/datasource/backlog.ts`
- **Dependencies:** Step 3.1
- **Validation:** Can load backlog, get next pending item, update status.
- **Implementation Notes:**
  - Read/write JSON file
  - Find next pending item
  - Update status and timestamps
  - Save after each operation

---

## Phase 4: Template System

### Step 4.1: Config Loader `[ ]`
- **Task:** Implement template config loading and variable injection.
- **Files:**
  - `cloops/src/utils/config.ts`
- **Dependencies:** Step 1.2
- **Validation:** Can load config.json, inject variables into template strings.
- **Implementation Notes:**
  - Load and parse config.json
  - `injectVariables` function with `{variable.path}` syntax
  - `getNestedValue` helper for dot notation

### Step 4.2: Template Loader `[ ]`
- **Task:** Implement template discovery and loading.
- **Files:**
  - `cloops/src/template/loader.ts`
- **Dependencies:** Step 4.1
- **Validation:** Can list templates, load template with config and prompts.
- **Implementation Notes:**
  - Scan templates folder
  - Load config.json and prompt files
  - Return Template object

---

## Phase 5: Execution Engine

### Step 5.1: Step Runner `[ ]`
- **Task:** Implement individual step execution logic.
- **Files:**
  - `cloops/src/engine/steps.ts`
- **Dependencies:** Step 2.1, Step 2.2, Step 2.3, Step 4.1
- **Validation:** Can execute a single step with input state, returns updated state.
- **Implementation Notes:**
  - Each step is a function: `(template, state) => Promise<State>`
  - Steps: narrative, planning, prompts, thumbnail, generation, bundle
  - Use services for LLM and generation calls

### Step 5.2: Template Runner `[ ]`
- **Task:** Implement main orchestration loop that runs steps sequentially.
- **Files:**
  - `cloops/src/engine/runner.ts`
- **Dependencies:** Step 5.1
- **Validation:** Can run full template pipeline, state passes between steps correctly.
- **Implementation Notes:**
  - Load template config steps
  - Run each step in order
  - Skip generation step if dry run
  - Log progress, handle errors

---

## Phase 6: CLI

### Step 6.1: CLI Commands `[ ]`
- **Task:** Implement CLI with commander: run, templates, status commands.
- **Files:**
  - `cloops/src/cli.ts`
- **Dependencies:** Step 5.2, Step 4.2, Step 3.2
- **Validation:**
  - `cloops run <template>` starts pipeline
  - `cloops run <template> --dry` skips generation
  - `cloops templates` lists available templates
  - `cloops status <template>` shows backlog status
- **Implementation Notes:**
  - Use commander for arg parsing
  - Support `--dry` flag
  - Support `--item <id>` for specific item
  - Add to package.json bin field

### Step 6.2: Logging & Error Handling `[ ]`
- **Task:** Add structured logging and error handling throughout.
- **Files:**
  - `cloops/src/utils/logger.ts`
  - Update: `cloops/src/engine/runner.ts`
  - Update: `cloops/src/cli.ts`
- **Dependencies:** Step 6.1
- **Validation:** Clear progress logs, errors show step name and context.
- **Implementation Notes:**
  - Console logging with step prefixes
  - Error messages include context
  - Exit with non-zero code on failure

---

## Phase 7: Template Integration

### Step 7.1: Comic Books Template Setup `[ ]`
- **Task:** Create comic-books-standard template folder with config and prompts.
- **Files:**
  - `cloops/templates/comic-books-standard/config.json`
  - `cloops/templates/comic-books-standard/prompts/step1-narrative.txt`
  - `cloops/templates/comic-books-standard/prompts/step2-planning.txt`
  - `cloops/templates/comic-books-standard/prompts/step3-prompts.txt`
  - `cloops/templates/comic-books-standard/prompts/step4-thumbnail.txt`
- **Dependencies:** Step 4.2
- **Validation:** Template loads correctly, config is valid.
- **Implementation Notes:**
  - Copy prompts from production-template-plan.md
  - Configure generation settings for Replicate/Seedream

### Step 7.2: Sample Backlog `[ ]`
- **Task:** Create sample backlog with test stories.
- **Files:**
  - `cloops/data/backlogs/comic-books-standard.json`
- **Dependencies:** Step 3.2
- **Validation:** Backlog loads, items are fetchable.
- **Implementation Notes:** Add 2-3 stories from existing stories-meta folder.

---

## Phase 8: End-to-End Testing

### Step 8.1: Dry Run Test `[ ]`
- **Task:** Run full pipeline in dry mode, verify LLM outputs.
- **Files:** None (manual testing)
- **Dependencies:** All previous steps
- **Validation:**
  - `cloops run comic-books-standard --dry` completes
  - Narrative, pages, and prompts are generated
  - No image generation calls made
- **Implementation Notes:** Review generated prompts for quality.

### Step 8.2: Full Run Test `[ ]`
- **Task:** Run full pipeline with image generation.
- **Files:** None (manual testing)
- **Dependencies:** Step 8.1
- **Validation:**
  - `cloops run comic-books-standard` completes
  - Images generated and saved
  - story-data.json created with correct structure
  - Backlog item marked complete
- **Implementation Notes:** Check output folder structure matches spec.

---

## Summary

**Total Steps:** 16
**Phases:** 8

**Key Considerations:**
1. Each step is atomic - can be implemented and tested independently
2. Services are built first so engine can use them
3. Template integration comes last - needs all infrastructure ready
4. Testing phases validate the complete pipeline

**After MVP:**
- Add CSV datasource
- Add parallel image generation
- Add post-processing (cloud upload, AdLoops integration)
- Add more templates

---

*Created: 2025-12-01*
