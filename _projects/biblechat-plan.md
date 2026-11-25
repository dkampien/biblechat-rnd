# BibleChat Plan

_Last updated: 2026-05-07_

> Personal task tracker across BibleChat work. Expand as needed.

## OVERALL TASKS

- [ ] **50 videos with localization**
    - [x] Generation — 51 bundles done (over the 50 target)
    - [x] Phase 1: Subtitles — en / ro / es complete for all 51
    - [ ] Phase 2: Dubbing — architecture not started

- [ ] **Video quality review**
    - Apply `template-plans/_recipes/debug-from-output.md` recipe
    - Watch all 51 against the "decent" bar (no severed limbs, anachronistic objects, child-rendering of adults, etc.)
    - Per-bundle outcome: approved / needs-regen / skip
    - Tooling decision: browser viewer / terminal walker / manual

- [ ] **Regen flagged scenes**
    - Per scene: `cli regen --story <X> --scenes <N> --asset image`
    - Re-localize + re-upload to R2 after regen
    - Re-run audit to confirm 0 drift

- [ ] **App integration**
    - Wait for Firestore-owner colleague to respond on schema / collection / app ID (handoff doc sent)
    - Build `ops/bc-main-videos/2-publish-videos.ts` per their spec
    - Verify end-to-end: app fetches Firestore docs → loads R2 video + sidecar SRTs → plays correctly

- [ ] **Workflow / pipeline walkthrough**
    - Walk Stages 1 → 1b → 2 → 3 → image/video/audio/alignment/assembly
    - Consolidate understanding (focus on data flow, system prompts, schemas)
    - Identify gaps and improvement candidates

- [ ] **Character consistency library — recap**
    - Umbrella: understand what exists + what's proposed, then decide what to build
    - Text library — character description blocks
        - Current: static per-character appearance, step1b emits one block, step3 injects mechanically
        - Design proposed: state-aware (`template-plans/_recipes/state-aware-character-arch.md`)
        - Decision: implement state-aware, or stay static?
    - Asset library — reference images of recurring characters
        - Not yet built
        - Purpose: anchor visual consistency across scenes/stories where same character appears

- [ ] **Ops folder inventory + cleanup**
    - Inventory every script in `ops/` and `functions/scripts/` — one-line description of each
    - Identify one-shots (already-run migrations) vs recurring tools
    - Archive or delete the one-shots; promote recurring tools to clear naming
    - Goal: at-a-glance know what each script does without reading code

- [ ] **CMS revisit**
    - Draft exists in worktree: `cloops/.claude/worktrees/cms-experiment` (branch `worktree-cms-experiment`)
    - Goal: reviewer-friendly UI for marking what needs regen, plus founder's items section
    - Decision: build out the worktree draft, or different approach?

- [ ] **AI content moderation system** (long-arc)
    - **Pipeline-stage layers** (where to check):
        - Scripts (Stage 1 narration) — theology, age-appropriateness, doctrinal accuracy
        - Prompts (Stages 2/3 per-scene) — flag prompts likely to produce artifacts
        - Image outputs — biggest win; vision models check for severed limbs, anachronisms, child-rendering of adults, multi-object hallucinations
        - Voice/audio outputs — narration quality, mispronunciations
        - Video outputs — mostly inherits from image checks
    - **Maturity layers** (how moderation evolves):
        - L1 (current) — human-driven with `debug-from-output` framework
        - L2 — CMS-assisted review (worktree draft above)
        - L3 — automatic LLM/agent flagging + auto-dispatch regen until passes

---

## Status snapshot (2026-05-07)

| | Count |
|---|---|
| Video bundles generated | 51 |
| EN subtitles in bundles | 51 (WebVTT) |
| RO subtitles in bundles | 51 (WebVTT) |
| ES subtitles in bundles | 51 (WebVTT) |
| Bundles uploaded to R2 | 51 (255 files / 2.8 GB) |
| Bundles reviewed for content quality | 0 |
| Firestore docs published | 0 (handoff sent, awaiting Firestore owner) |
| Bundles dubbed | 0 |

## Open dependencies (waiting on humans)

| | Owner | Blocks |
|---|---|---|
| Firestore schema decisions | Firestore-owner colleague | App integration |
| Theological/doctrinal review process | You + CTO | Pre-public-launch |
| Custom R2 domain (optional) | You | Cosmetic only |

---

## Pointers (for next session bootstrap)

**Reference docs:**
- `_projects/cloops/_docs/2_reference-docs/handoff_firestore-publish-bc-adult.md` — Firestore handoff brief sent to colleague
- `_projects/cloops/template-plans/bc-adult-vids-bible-stories/_handoff.md` — Phase 1 generation context
- `_projects/cloops/template-plans/_recipes/debug-from-output.md` — debug recipe for QA review
- `_projects/cloops/template-plans/_recipes/state-aware-character-arch.md` — character library design
- `_projects/cloops/_docs/index.md` — full markdown index (regen: `python3 _docs/build-index.py`)

**Tools:**
- `cli run <template> --item <id>` — generate
- `cli regen --story <X> --scenes <N> --asset image` — regen specific scenes
- `cli localize <template> --locale <X> --all --parallel <N>` — translate SRTs
- `npx tsx scripts/audit-bundles.ts <template> --locales ro,es` — drift check
- `bun run ops/bc-main-videos/1-upload-videos.ts --parallel 8` — R2 upload

**Distribution:**
- R2 bucket: `biblechat-vids` (Cloudflare account `b8ce6...`)
- Public URL base: `https://pub-2631064746a44e24a2bd1adcc79d64c1.r2.dev/`
