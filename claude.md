# Project: SoulStream/Bible Chat Content Generation

## Project Status

**Client:** SoulStream (Series A, 40M users, 300% YoY growth)
**Collaboration:** 3900 EUR + 200 EUR testing/month, B2B through LLC
**Phase:** Starting Phase 1 - Find winning ad creatives, automate into AdLoops
**Timeline:** 2-3 months for full pipeline automation

## What We're Building

### Overview
AI-powered content generation pipeline for Bible Chat (SoulStream product). Automates creation of ad creatives and in-app content, integrated with their AdLoop distribution system.

### Evolution
- Started as POC concept (Oct 2025)
- Built technical foundation (Cycles 1-4: frame chaining, manifests, automation)
- Trial period with SoulStream (1 month)
- Now: Paid client collaboration

### Current Scope
**Phase 1:** Find winning ad creative formats, automate generation (full AI), integrate into AdLoops
**Phase 2:** Full pipeline automation (ads + in-app content, testing, scaling, optimization)

### Input
CSV dataset containing user problems from Bible Chat users (170 rows, 9 problem categories)


## Key Decisions
- **Stack**: TypeScript, Node.js
- **APIs**: OpenAI (gpt-5-mini), Replicate (Veo 3.1)
- **Strategy**: "Iterate, Don't Predict" - Manual testing → Find winning patterns → Automate
- **Templates**: D2C (implemented), UGC-Action (in design) - Plugin architecture for multi-template workflows
- **Architecture**: Two-call LLM process → Scene prompts → Veo 3.1 with frame chaining → Video combining

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

## Important Notes
- **Client Work**: This is paid collaboration with SoulStream, not a POC
- **Integration**: Content feeds into AdLoop (their automated distribution system)
- **Goal**: Support $2.5M ad spend by November ($1 cost per install = 2.5M installs)
- **Deliverables**: Incremental - functional systems each month, full automation in 2-3 months
- **Future**: Startup House pitch planned after building leverage (2-3 months of delivery)
