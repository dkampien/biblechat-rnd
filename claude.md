# Project: Bible Content Video Generation POC

## What We're Building

### Overview
Automated video generation tool for TheBibleChat.com that creates AI-generated video content from user problem data. This POC plugs into their
existing content marketing platform.

### Purpose
Build a standalone MVP that generates video assets automatically. The parent platform handles distribution, stitching, publishing, and analytics.

### Input
CSV dataset containing real user problems from TheBibleChat.com users.

### Output (ideally)
- Video clips (individual assets, no stitching required) - might change
- JSON schema with metadata for CTO's platform to consume - don't have the required schema yet

### Scope
POC focused on proving the concept with minimal complexity. Sequential execution, simple state management, clean integration points for the
larger platform.


## Key Decisions
- **Stack**: TypeScript, Node.js
- **APIs**: OpenAI (gpt-4o-mini), Replicate (Veo 3) *(may change)*
- **Scope**: POC - 2 categories, 2 templates, 3 scenes each = 12 video clips *(may change)*
- **Templates**: Direct-to-camera, Text+Visuals *(to start)*
- **Architecture**: Category + Template → Script (LLM with Zod) → 3 Scene Prompts → Video Clips (Veo 3) *(under review)*

## Docs Location
- **Exploration**: `_docs/1_development-docs/cycle-1/0-exploration.md`
- **PRD**: `_docs/1_development-docs/core-docs/1-product-requirements.md`
- **Tech Specs**: `_docs/1_development-docs/core-docs/3-technical-specs.md`
- **Input Data**: `bquxjob_696709f0_199c894db50.csv` (170 rows, 9 problem categories)

## Project Development Workflow
1. Exploration thread (discuss, clarify, make decisions)
2. Draft PRD
3. Draft Technical Specs (with external API docs)
4. Create Implementation Plan
5. Build incrementally (cycles)

## Important Constraints
- **POC only** - keep it simple, prove the concept
- **No video stitching** - CTO's platform handles that
- **Sequential execution** - parallel is future enhancement
- **Resume capability** - simple state management, don't overcomplicate
- **Clean code** - designed for integration with larger platform
