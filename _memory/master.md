# Project Memory

*This file is automatically synthesized from conversation summaries and codebase analysis.*

---

## Current Status

**Primary Project:** SoulStream/Bible Chat Content Generation (Active Client Collaboration)
**Client:** SoulStream (Marius & Laurențiu - Series A, 40M users, 300% YoY growth)
**Phase:** Negotiating collaboration terms for Phase 1 start
**Arrangement:** 3900 EUR + 200 EUR testing budget/month, B2B through LLC

**Project Evolution:**
```
Oct 2024: Started as Bible video generation POC concept
     ↓
Cycles 1-4: Built pipeline (frame chaining, manifests, all-problems processing)
     ↓
Hit architectural limits → Pivoted to manual testing + prompt methodology design
     ↓
Reached out to Laur for mentorship → Introduced to Marius (SoulStream)
     ↓
Trial period: 1 month content generation work for Bible Chat
     ↓
NOW: Negotiating paid collaboration (Phase 1 starting)
     ↓
FUTURE: Pitch Startup House as separate venture (after building leverage)
```

**Active Work Tracks:**
1. **SoulStream Phase 1** (imminent): Find winning ad creatives with Marius, automate into AdLoops
2. **SoulStream Phase 2** (2-3 months): Full pipeline automation (ads + in-app content)
3. **Prompt System Design** (ongoing): Model-agnostic framework for AI content generation
4. **Memory System** (current conversation): Building `/synthesize` command

**Their Goal:** $2.5M ad spend by November, $1 cost per install (2.5M installs target)

---

## Key Decisions

### SoulStream Collaboration - Business Terms

**Deal Structure (Negotiated Nov 2024):**
- Monthly retainer: 3900 EUR + 200 EUR testing budget
- B2B collaboration (LLC-to-company, not employment)
- Scope: AI content R&D + code implementation
- Individual contributor role
- Working with head of marketing + Marius
- Temporary bridge arrangement (until Startup House pitch)

**Phase 1 Scope:**
- Find winning ad creative formats
- Automate content generation (full AI)
- Integrate into AdLoops (their distribution system)
- Timeline: ~1 month for functional system

**Phase 2 Scope:**
- Full content pipeline automation
- Includes: Auto testing, scaling, optimization
- Both ads + in-app content generation
- Timeline: 2-3 months total (includes Phase 1)

**Positioning Strategy:**
- "Under-promise, over-deliver" principle
- Incremental delivery (functional systems each month)
- Won't commit to unrealistic timelines (pushed back on "1 month" test)
- Maintains independence (consultant, not employee)

### SoulStream Collaboration - Technical Implementation

**Cycle 1-4 Completion (Pre-Client Context):**
- ✅ Direct-to-Camera template (3 scenes, frame chaining, 24s videos)
- ✅ Frame chaining for character consistency (base64 data URL conversion)
- ✅ All-problems processing (`.filter()` vs `.find()` + `--limit` flag)
- ✅ Video combining (ffmpeg concat)
- ✅ Unified manifest system (timestamped, status tracking)
- ✅ Model upgrades (gpt-5-mini, Veo 3.1)
- ✅ Zod schema simplification

**Multi-Template Architecture (In Design):**
- **Decision:** Different templates need different workflows
  - D2C: 3 scenes, frame chaining, combine into 24s
  - UGC-Action: Single 4-6s clip, text overlay, voiceover, no chaining
- **Approach:** Plugin architecture where templates define workflows
- **Status:** D2C implemented, UGC-Action in manual testing phase

**Template Naming Convention:**
- Pattern: `[visual-format]_[feature/campaign]`
- Examples: `direct-to-camera_comfort`, `ugc-action_lockscreen`

**Two-Call LLM Process (D2C):**
- Call 1: Generate videoScript (Scene 1 baseline) + voiceScript (50-60 words)
- Call 2: Generate 3 scene prompts (Scene 1 full, Scenes 2-3 minimal)
- Frame chaining handles visual continuity

### Strategic Decisions

**"Iterate, Don't Predict" Strategy:**
- **Failed approach:** Design LLM prompts → hope Veo works → 0-33% success
- **Pivot:** Manual Veo testing → find winning pattern → design LLM to match
- **Current:** Testing action-focused, no-emotion prompts manually before automation
- **Rationale:** Understand what works before automating

**SoulStream Relationship Development:**
- **Initiated contact:** Reached out to Laur for mentorship
- **Trial period:** 1 month content generation work (evaluation phase)
- **Leverage building:** Deliver quality work → build credibility → pitch Startup House later
- **Timeline:** Need 2-3 months of solid delivery before Startup House pitch
- **Separation maintained:** B2B contractor (not employee) keeps door open for Startup House

**Startup House - Future Pitch (Separate Project):**
- **Status:** Concept designed, NOT pitched yet
- **Timing:** After building leverage through SoulStream work (2-3 months minimum)
- **Relationship:** Mentioned to Marius as "idea to align all ships down the line"
- **When it starts:** Will create new project folder
- **Purpose:** Funded venture studio to build own business ideas with team
- **Target investors:** Marius & Laur (after proving value through current work)

### Prompt System Design (General-Purpose Tool)

**Model-Agnostic Framework:**
- AI landscape changes constantly (new models monthly)
- Focus on: Modalities (capabilities) + Workflows (chaining) + Prompting (communication)
- Framework works regardless of specific models

**Block-Based Formula System:**
- **Blocks:** Atomic, reusable components with hierarchical paths (`[scene.subject.age]`)
- **Formulas:** Structured templates combining blocks for specific tasks
- **Core blocks:** Terminal nodes with creative freedom
- **Values:** Manually written, AI-generated, or curated lists

**Current Versions:**
- `prompt-generation-guide-v5.md` (modalities, workflows, model selection)
- `prompt-formula-framework-v2.md` (blocks, formulas, methodology)

### Memory System (General-Purpose Tool)

**Purpose:** Cross-conversation memory for ALL projects (not SoulStream-specific)

**Three-Command Architecture:**
- `/summarize` - Capture current conversation → individual summary
- `/synthesize` - Consolidate all summaries + codebase scan → master.md
- `/recall` - Load master.md into context

**Implementation Status:**
- ✅ `/summarize` command (auto-update logic)
- ✅ `/recall` command (tested successfully)
- ✅ `/synthesize` command (completed - this conversation)

**Design Principles:**
- File-based (CLI can't access past conversations)
- Dual-write approach (update master immediately, not on-load)
- Master memory = synthesis by theme (not chronological)
- Standardized filenames (auto-generated, no fuzzy matching)

---

## Learnings & Discoveries

### SoulStream Context

**Who They Are:**
- **Laurențiu (Laur):** Serial entrepreneur, 8 companies founded, 4 sold, co-founded T-Me Studios (3B+ downloads)
- **Marius:** 20+ years coding, focused on scaling apps globally
- **SoulStream:** 40M users, Series A funded, 300% YoY growth
- **Products:** Bible Chat, Basmo (reading app), multiple lifestyle/personal growth apps
- **Philosophy:** "Ship fast, avoid lengthy meetings, rely on usage data"

**Their Secret Weapon - AdLoop:**
- Automated ad creation → publishing pipeline
- Internal platform for social media ads at scale
- How they're achieving 300% growth
- Distribution mechanism they want to plug external apps into

**App Venture Model (Their Idea, Pre-Dennis):**
- Take external founders' ideas/apps
- Plug into AdLoop for distribution
- Revenue share model
- Rationale: External founders already invested
- First project: January 2025 with European record label founder

**Why This Matters for Startup House:**
- They already think in portfolio terms
- Already want to leverage AdLoop for multiple products
- Startup House = potential evolution/pivot of their App Venture thinking
- Advantage: Concept isn't foreign to them

### Video Generation - Technical Insights

**Veo Prompt Challenges:**
- Explicit emotion in prompts → exaggerated/theatrical output
- Literal problem matching → disconnected visuals
- Too detailed prompts → overly cinematic (not authentic UGC)

**UGC-Action Template Strategy:**
- ❌ NOT in video prompt: No emotion words (causes exaggeration)
- ❌ NOT in text hook: No emotion labels ("anxious", "worried")
- ✓ IMPLIED: Through situation, context, viewer projection

**Cohesion Flow:**
```
Video (generic action) → Relatability: "That's like me"
Text Hook (specific situation) → Context: "That's my situation"
Lockscreen CTA → Solution: "I can try that"
```

**Key Insight:** Generic everyday action + situational text hook > Literal problem-action match

### Collaboration & Negotiation Lessons

**Marius's "1 Month" Test:**
- Asked: "Do you propose we succeed in maximum one month?"
- **What he was testing:**
  - Will you overpromise to close the deal?
  - Do you understand the actual scope?
  - Can you push back professionally?
  - Confidence vs desperation signal
- **Response:** Pushed back with realistic 2-3 month timeline
- **Outcome:** Maintained credibility by not overpromising

**Pricing Lessons:**
- **Initial target:** 3.5k/month (above 2.5k last rate, below 4k Phase 1 goal)
- **Actual pitch:** 3900 EUR + 200 EUR testing = 4100 EUR total
- **Rationale:** B2B contractor rates higher than employee salary
- **Their response:** "Sounds ok" (didn't reject price)
- **Learning:** Went higher than planned, got acceptance

**Positioning Strategy:**
- Maintained independence (LLC, not employee)
- "Under-promise, over-deliver" principle
- Realistic timelines with incremental milestones
- Won't commit without understanding full scope

### Personal Working Constraints

**From Professional Cheat Sheet:**
- Can't focus on multiple directions at once
- Prefer single complex challenge vs many small tasks
- Would prefer not stopping midway on tasks
- Conflict-avoidant, mental blockers around sales/public exposure
- Struggle with focus - too many ideas, get distracted by shiny things
- Need external accountability and clear scope

**Financial Reality (Nov 2024):**
- Survival minimum: 2k/month
- Phase 1 goal: 4k/month (escape scarcity energy)
- Current runway: 2 months without income
- Urgency level: REALLY URGENT
- Can walk away if terms don't work, but this is only current option

**Why SoulStream Collaboration Works:**
- Solves Phase 1: Immediate income (3900 EUR)
- Provides structure: External accountability through client work
- Enables Phase 2: Build leverage for Startup House pitch
- Maintains flexibility: B2B keeps door open for future ventures

---

## Evolution & Changes

### Project Journey

```
Oct 2024: Bible video generation POC concept
     ↓
Cycle 1: Basic pipeline (single D2C template, script generation, video clips)
     ↓
Cycle 2-3: Refinements (two-step LLM process, dry-run mode)
     ↓
Cycle 4: Technical maturity (frame chaining, manifests, all-problems, combining)
     ↓
Architectural realization: D2C workflow hardcoded, need multi-template system
     ↓
Strategic pivot: Stop automating, start manual testing ("Iterate, Don't Predict")
     ↓
Prompt system design: Model-agnostic framework (general-purpose tool)
     ↓
Oct-Nov 2024: SoulStream connection
     ↓
Trial period: 1 month content generation for Bible Chat
     ↓
Negotiation: 4100 EUR/month collaboration terms
     ↓
NOW: Starting Phase 1 (find winners, automate into AdLoops)
     ↓
FUTURE: Startup House pitch (separate project, after proving value)
```

### From POC to Client Work

**Original Vision:**
- Standalone POC for TheBibleChat.com
- Prove concept works end-to-end
- Generate video assets for CTO to integrate

**Reality Evolution:**
- Connected with actual decision-makers (Marius & Laur)
- POC became trial → trial became paid work
- Scope evolved from "prove it works" → "integrate into AdLoop production system"
- Now building for 40M user platform with $2.5M ad spend goal

**Scope Changes:**
- **Was:** Generate video clips, JSON scaffolds, standalone system
- **Now:** Automate into AdLoop, scale to support massive ad spend, continuous optimization

### Prompt Strategy Evolution

```
Original: Guess LLM prompt → hope Veo works → fail → adjust
     ↓
Realized: Can't automate what we don't understand
     ↓
Pivot: Manual Veo testing → find winning pattern → design LLM to match
     ↓
Expanded: Built general-purpose prompt framework (beyond just this project)
```

### Relationship Development

```
Reached out to Laur for mentorship
     ↓
Laur introduced to Marius (evaluation mode)
     ↓
1 month trial on content generation
     ↓
"Exploring collaboration options"
     ↓
Negotiated 4100 EUR/month collaboration
     ↓
About to start Phase 1 work
     ↓
Building leverage for Startup House pitch (later)
```

---

## Active Questions

### SoulStream Collaboration

1. **Scope clarity for Phase 1:** What exactly needs to be built? (Gathering info from team)
2. **Success metrics:** How do we measure "winning" ad creatives objectively?
3. **AdLoop integration:** What's the technical integration path?
4. **Content format testing:** Which formats to prioritize? (With Marius)
5. **Phase 2 components:** What infrastructure needed for full automation?

### Video Generation Technical

1. **Tool capability:** Can Veo produce authentic UGC look with better prompting?
2. **Prompt formula:** What exact structure works for action-focused, no-emotion prompts?
3. **Cohesion validation:** Does generic action + situational text hook flow work in practice?
4. **Multi-template architecture:** Clean implementation of template-specific workflows?

### Prompt System

1. **Block library scope:** How many blocks to define upfront vs discover organically?
2. **Formula priorities:** Which formulas to document first? (t2v, i2v, t2i?)
3. **LLM usage patterns:** How to effectively use LLM for populating block values?

### Memory System

1. **Auto-loading:** Can claude.md or hooks auto-trigger `/recall`?
2. **Dynamic structure:** Should master.md adapt based on content in future versions?
3. **Cross-project usage:** How to scale memory system for multiple simultaneous projects?

### Strategic

1. **Startup House timing:** When is the right moment to pitch? (After 2-3 months of delivery?)
2. **Leverage threshold:** What level of proof needed before pitching bigger vision?
3. **Work balance:** How to deliver for SoulStream while developing reusable frameworks?

---

*Last synthesized: 2025-01-04*
*Sources: 2 conversations (memory system design, SoulStream negotiation), 15+ docs, 10 git commits*
*Primary: SoulStream/Bible Chat collaboration (paid client work)*
*Future: Startup House (separate project, not started)*
*General tools: Prompt system + Memory system (reusable across all projects)*
