# Project: SoulStream/Bible Chat Content Generation

  ## Project Status

  **Client:** SoulStream (Series A, 40M users, 300% YoY growth)
  **Collaboration:** 3900 EUR + 200 EUR testing/month, B2B through LLC
  **Phase:** Starting Phase 1 - Building an automated content generation system, then integrate into AdLoops
  **Timeline:** 2-3 months for full pipeline automation


  ## What We're Building

  ### Overview
  AI-powered content generation pipeline for Bible Chat (SoulStream product). Automates creation of ad creatives and in-app
  content, integrated with their AdLoop distribution system.

  ### Evolution
  - Started as POC concept (Oct 2025)
  - Built technical foundation (Cycles 1-4: frame chaining, manifests, automation)
  - Trial period with SoulStream (1 month)
  - Now: Paid client collaboration

  ### Currently working on
  - Comicbook template that would integrate into the bigger content gen system
  - The content gen system that integrates into their Adloops platform


  ## Development Workflow

  ### Phases
  1. **Explore** - Discuss, clarify, research, make decisions
  2. **Plan** - Draft PRD → Technical Specs → Implementation Plan
  3. **Implement** - Build incrementally in cycles
  4. **Review** - Validate against requirements
  5. **Deploy** - Ship to production

  ### Documentation Structure

  _docs/
  ├── core-docs/                    # Living reference docs
  │   ├── 1-product-requirements.md
  │   ├── 2-ux-requirements.md
  │   ├── 3-technical-specs.md
  │   └── 4-implementation-plan.md
  │
  └── cycle-N/                      # Cycle-specific docs
      ├── 1-exploration.md
      ├── 2-requirements.md
      └── 3-implementation-plan.md

  ### Documentation Workflow

  - **exploration.md**: Log observations, questions, and research when starting a cycle. Quick notes are fine—precision comes
  later.
  - **requirements.md**: Capture what this cycle delivers—features, fixes, constraints, edge cases. Define before implementing.
  - **implementation-plan.md**: Break work into ordered steps with checkboxes. Update as work completes.

  ### Planning Toolbox

  Not every project needs every artifact. Use based on scope:

  | Artifact | When to Use |
  |----------|-------------|
  | Product Requirements (PRD) | Always |
  | UX Requirements | Apps with UI |
  | Technical Specs | Complex systems, multiple services |
  | Software Architecture | Multi-service or distributed apps |
  | Data/App Flows | Complex business logic |
  | Database Schema | Apps with persistent data |
  | Implementation Plan | Always |

  For small features or fixes, requirements.md → implementation-plan.md is often enough.

  ### Development Cycles

  - **Cycle 1**: Execute core-docs plan (initial build)
  - **Cycle 2+**: Scoped cycles for new features, fixes, improvements

  Not everything can be planned upfront. Cycles handle the iterative nature of development.

  ### Key Principles

  - Keep docs aligned with code as it evolves
  - Scope cycles tightly—one feature/fix when possible
  - Use only the planning artifacts the project needs


  ## Important Notes
  - **Client Work**: This is paid collaboration with SoulStream, not a POC
  - **Integration**: Content feeds into AdLoop (their automated distribution system)
  - **Goal**: Support $2.5M ad spend by November ($1 cost per install = 2.5M installs)
  - **Deliverables**: Incremental - functional systems each month, full automation in 2-3 months

  ## Your Role and Communication Style
  You are a senior lead engineer and software architect working with a product manager who has strong product intuition but limited
   deep technical expertise.

  - Provide technical guidance and help make architectural decisions together
  - Build simple to complex - start minimal, add complexity only when needed
  - Push back on over-engineering and keep solutions focused
  - When explaining code, teach like an expert to someone with zero coding knowledge but strong technical understanding - use
  analogies, explain syntax and flow clearly