---
name: ad-draft
description: The authoring phase of the BibleChat ad pipeline. Idea OR existing ad → a fully authored ad on the Airtable board (the single source of truth), ready for production. ZERO spend; the board is written only on the operator's approval. Two entries: a blank page (turn an idea, insight, or pain point into a new ad) and an existing base (change an ad already on the board: a new hook, a different voice or look, one beat's visual, a concept re-aim, a batch of variants, metrics-driven changes; a child inherits the parent's paid work where you say so). Trigger phrases: "draft an ad", "new ad", "write an ad for", "ad about", "iterate on <slug>", "variant of <slug>", "change the hook/voice/music/look", "batch of hooks", "act on the metrics". Not for: rendering to mp4 (ad-produce) or decomposing an outside ad (ad-watch; its landed output re-enters here as a base).
argument-hint: <a rough idea, an audience, a pain point, or an existing ad's slug> [what to change]
allowed-tools: Read, Write, Edit, Bash
---

# ad-draft: idea or existing ad → an authored ad on the board (NO spend)

Author ONE ad: from a blank page (pick who it's for, the pain, the feature, the angle, the form; write the script) or from an existing base (read it, decide what changes, land the change in place or as a child). Everything this skill lands sits on the board as an `idea`, costing nothing until produced. If the user asks for several ads, run the flow once per ad.

**User input:** $ARGUMENTS

## How this skill runs (read first)

- **Decide, then land.** The steps are conversation: read the board, propose, the operator picks. The board gets written only at the LAND step, after the operator approves what you proposed. Drafts iterate in the conversation, not on the board.
- **One pick at a time.** Each step ends with a proposal and a recommendation, then stops for the operator's pick. Skip a step's question only when the operator's input already answered it.
- **Walls of text welcome.** When the operator gives a lot at once (a full idea, a pasted script from anywhere), don't interview them through what they already said: map the text onto the picks, fills, and beats it answers, show that mapping, then ask about what's missing, one gap at a time. The gate is unchanged. A pasted script that fits no canon arc lands on the `freeform` framework, never bent to fit one.
- **One vehicle per session.** An authoring session works one vehicle (several ads on it is fine). When a different vehicle comes up mid-session, land the current work and recommend a fresh session: an agent holding two vehicles' variable sets cross-contaminates them.

## Where things live

- Run every command from `_projects/cloops-ads/` (the repo root).
- **The ad lives on the Airtable board.** Read and write ONLY through the guarded client: `npm run ads -- <command> '<json>'`. The raw Airtable API and the Airtable MCP bypass the guards; the client carries them.
- Preflight: `npm run ads -- pools`. A failure usually means `AIRTABLE_TOKEN` is missing from `.env.local`.
- **Read fresh before you act.** Verbs read live state; so should your proposals. Propose from what the board says now, not remembered state.
- **Discovery:** `npm run ads -- capabilities` prints the verb map (every verb, one line, grouped); `npm run ads -- describe <verb>` prints one verb's full contract (inputs, effects, errors with recovery, an example). Pull a contract before composing any payload you don't know cold; never guess shapes from memory.
- **Big payloads:** ad copy contains apostrophes, which break single-quoted shell JSON. Write the payload to a file and pass it as `@<path>`: `npm run ads -- create-ad @/path/to/payload.json`.

## The contract with the operator

**The machinery stays invisible; the craft language is shared.** The operator is a creative strategist: talk persona, pain, angle, hook, look, voice. The system's internal logic (lineage, inheritance, replans, guards) is yours to reason with and never theirs to operate: they make creative calls, you translate to mechanics and report back only the consequences that matter (what it costs, what gets remade). When a pick is on the table, remind the operator what the thing means in one line (situation = the circumstance, pain = the felt symptom, angle = the lens). **Name the cost in plain terms before landing a child**: the verb's response splits the child's sheet into inherited (free, reused from the parent) and planned (to buy); `npm run ads -- estimate <slug>` prices the planned. Read those out, never guess.

## Load the craft (it is not re-derived, it is loaded)

All under `_projects/cloops-ads/`:
1. `_docs/skill-reference/ad-copy-playbook.md`: how to write the copy (Path A, the hook, the rules).
2. `_docs/skill-reference/audience-product-brief.md`: who we sell to, and the worldview the copy speaks from.
3. `_docs/skill-reference/prompting-guide-2026.md`: how to write t2i/i2v prompts (the {LOCK}/{STYLE} pattern and the prompt rules).

The product truth for features is the **Mechanisms table on the board**: a feature exists only if it is a row there, or the operator explicitly approves adding one.

## The shape of an ad (the vocabulary you author with)

- **Slot**: a named setting the VEHICLE declares; the ad fills it by writing a value (character, treatment, set, voice, music).
- **Reference**: a beat can play an existing registered file instead of generating: its `asset` key names an Assets row with real bytes behind it (an outside import via `insert-asset`, or another production's file).
- **Production sheet**: where landing files the ad's work order: one `planned` row per file the ad needs (stills, videos, vo, music); `estimate` prices them. A referenced file lands ready instead.
- **Child**: an ad landed with a `parent` link, a `changeSet` label saying what it changes, and an `inherit` list naming the parent positions it reuses at $0. Lineage is how the board reads a family; the kind (variation vs iteration) derives from the changeSet.

In one line: the vehicle declares the slots, the framework declares the roles, the beats say the words and what we see, and landing writes the work order.

---

## ENTRY: route before you talk (read this before proposing anything)

**Before doing anything else**, settle which entry you're in. If $ARGUMENTS names an existing ad's slug, or the ask mentions changing/iterating/varianting something, check the board first:

```bash
npm run ads -- get-ad <slug> --view brief
```

- Slug exists → you are in **EXISTING BASE**. Load `references/changing-a-base.md` (the change economics), then route by the table below.
- Slug doesn't exist, or the ask is an idea/audience/pain → **BLANK PAGE**: jump to step 0 of the flow. Do not read any base, do not offer variants of anything, do not load the economics reference.
- Outside mp4/URL → **ad-watch** decomposes it first; its landed output re-enters here as a base. Do not offer a change menu for an ad that isn't decomposed yet.

**EXISTING BASE: note the status, then route by the KIND of change.** Do not start the conversation until you've classified the ask against these four rows; say the classification out loud in plain words so the operator can correct it.

| the ask is | that means | route | do NOT |
|---|---|---|---|
| a glitched/defective file, instruction was fine | not an authoring change | `reroll` via **ad-produce** | do not land a child for a defect |
| a different framework, a reordered or re-roled arc, beats inserted mid-script | a structure break | fresh BLANK PAGE draft; carry winning footage as references (`asset` keys) | do not force it into a child; inherit maps by beat order and a restructure makes that mapping a lie |
| new beats after the existing arc (extra CTA takes, a longer ending) | an extension | a CHILD: the parent's beats plus the new ones, inherit every existing position (orders hold, the mapping stays honest) | do not regenerate what the append leaves untouched |
| a new persona/pain/mechanism/angle/vehicle/format/length | a variation | run the picks flow through the new lens, land as a CHILD of the base | do not skip the gate; script work is script work |
| a hook line, voice, music, one beat's visual, a file swap, a cast member's look | an iteration | judge cost (change economics), then IN PLACE (status `idea` only) or as a CHILD (any status) | do not edit in place on a produced/posted base; do not replan anything before the economics judgment |

**The seam test decides the hook edge:** a new opener that hands cleanly into the existing body is an iteration; one that forces the body to be rewritten is a structure break.

**Status gates the in-place door only**: `idea` = both doors open; `produced` / `posted` = children only (banking children without touching the parent is normal and free).

---

## The flow (blank page, and the script conversation for variations)

> **Curator guardrail, wherever a NEW registry value is proposed (persona, pain, mechanism, angle).** The guards refuse incomplete rows and duplicate slugs; only you can catch a duplicate by MEANING. Merge-check against the existing rows first (same felt thing, same feature: reuse or merge), and name the value in plain everyday words with a one-line definition. Know the trap: upserting an existing slug silently edits that row for every ad linking to it, so send an existing slug only when you mean to edit it. Present a merge as a proposal with its evidence, never a refusal; the new-row door stays open.

### 0. Read the board

```bash
npm run ads -- pools
```

Every registry that exists: personas, pains, mechanisms, angles, vehicles, frameworks. Know what is there before you propose. Growing the registries well is part of this skill.

### 1. PERSONA: pick

Show the existing personas and propose the fit. **Picking is the normal path**: personas are defined upfront, grounded in evidence, and locked. Defining a new one mid-draft is the rare exception; it needs real evidence (user research, reviews, the audience brief) cited in its `evidence` field, and the operator's explicit go-ahead. Stop; the operator picks.

### 2. PAIN: pick, or distill from evidence

Read this persona's pains (`npm run ads -- pains-for-persona <slug>`) and propose plainly.

- **A pain is the felt symptom**: what it feels like from the inside on a bad Tuesday, written the way the person would say it. Source material (quiz answers, reviews) usually describes a SITUATION ("my marriage is broken"); distill the feelings inside it (the guilt, the fear, the loneliness): each is a pain candidate, and the verbatim quote is its `evidence`. Felt states run both directions: an ache (guilt, fear) or a desire (the longing for closeness); the direction lives in the symptom's own wording.
- **Classify, with your reasoning shown:** `universal` (anyone could feel it; keep the wording raw, the faith lens arrives later via the angle) or `faith-native` (the pain itself is faith-shaped and is its own angle).
- **EXPLODE offer:** a persona usually carries several pains; offer running more than one, each as its own ad.

Stop; the operator picks.

### 3. MECHANISM: default it

Default to the **habit-formation feature** (the daily plan); the default stands without a stop. The honest test: **does the feature shown as proof ring true in the moment the script shows?** Any pain can honestly carry the daily plan by moving the script from the moment to the pattern; when the script stays inside the acute now, pick the moment's feature from the Mechanisms table. Stop only when proposing a mechanism that is not yet on the board; the operator decides. **Sell the outcome, prove with the feature**: the copy leads with the benefit ("a calm two-minute start"); the feature is the on-screen proof.

### 4. ANGLE: the lens (universal pains only)

A faith-native pain is its own angle: skip this step, and know the guard refuses an angle on it. For a universal pain an angle is required, and it is not a separate scene: **the angle is the lens the WHOLE script is written through; every beat speaks from it. Faithfulness is judged at the gate.**

Angle rows are the shared lens pool, written **persona-neutral**: define the move without a persona's pronouns baked in ("permission to stop, instead of another demand"), plus one example hook line so the row is navigable (an expression of the lens, not the expression). Let reuse emerge; merge duplicates on contact.

**EXPLODE offer:** try this pain from several angles? Each extra angle = a variation of this ad, landed as a child after the base lands.

Stop; the operator picks.

### 5. FORM: format · vehicle · framework · length

The vehicles ON THE BOARD are the menu; the skill carries no catalog. Read the picked vehicle's row before authoring anything:

```bash
npm run ads -- get-vehicle <slug>
npm run ads -- get-framework <slug>
```

Its `description` is the form's own guidance, its `slots` array is your fills checklist, its `delivery` the script's ad-wide default (a beat may break from it, step 7).

- **Format:** `video` / `image` / `image-carousel`. The medium filters which vehicles can tell the story. Only `video` has an engine path today; an image ad can be drafted but not yet produced.
- **Vehicle** (how the story is told): present each candidate vehicle with its one-line description from the board; never assume the operator (or a new team member) remembers what a form is. Match the operator's ask against those descriptions. When nothing fits, say so plainly: that is a NEW form, and defining a vehicle is its own explicit, operator-gated move (`upsert-vehicle`), never a silent side effect of drafting. A new vehicle whose form the default arrangement serves needs only the row: the engine falls back to the default composition. A form that assembles differently needs its module built first, an engineering move.
- **Framework** (the copy arc): its `roles` are the only legal beat roles. One special row: `freeform`, no role constraint, roles become descriptive labels; the landing pad for scripts that fit no canon arc (a pasted reference script is the usual case).
- **Length band:** `micro`/`short`/`mid`/`long`, video only; an image ad has no band. A creative form band, never a seconds target (real timing derives from the words at production). The band decides the beat structure: a longer band repeats roles.

Stop; the operator picks the form.

### 6. FILLS: author what the vehicle declares

For each slot on the vehicle's checklist, author a value with the operator. **There are no house defaults**: every fill is authored for this ad (look at sibling ads when the operator wants continuity). The craft that holds across vehicles:

- Where the vehicle declares a `character`: write the one-sentence character lock, and pick a `voice` that **gender-matches it**. Where it declares a `treatment`: the one-sentence style bible.
- In beat prompts, write `{LOCK}` and `{STYLE}` where the character and treatment belong; production expands them from the fills, so one swap restyles every prompt at once.
- The ad may carry an `anchor`, optional: a reference image every picture generation receives, for visual continuity. A character reference works; a scene image leaks its scene into every still. Leave unset otherwise.

### 7. BEATS: write the script

**The beats are the script: the framework's roles instantiated.** One beat per role, in order (classic = hook · symptom · solution · result · cta); a longer band repeats roles where the visuals genuinely differ.

Write the copy per the playbook: the raw pain in the hook, symptom to solution on the real feature, talk like a real person, written for the band. Each beat carries:

- `role`: one of the framework's roles.
- `vo`: THE WORDS, always, whatever their delivery.
- `visual`: the stage direction: what we see during this line, prose, no model syntax.
- `delivery`, optional: the per-beat break from the vehicle's default. `narration` = a narrator speaks the line · `dialogue` = the person in the clip says it (`vo` holds the transcript) · `text` = the line burns as on-screen captions. Empty = the vehicle's default.
- `prompts`: the model text compiled FROM the visual: `still` (the image prompt, per the prompting guide, with `{LOCK}`/`{STYLE}` placeholders) and `motion` (motion only). You write them; landing files them onto the ad's planned sheet rows (the sheet is their only home; beats stay pure script).
- `asset`, optional: reference an existing file instead of generating (see the reference exception above).
- **Never author a duration.** Production sizes everything from the words' home: the measured VO when narration, the reading time when text, the file itself when dialogue.

### 8. THE GATE: validate, print, stop

First validate (the guards catch structure; you catch sense):
- The pain classification is actually right: universal wording stays raw; a faith-native pain carries no angle.
- **The script speaks from the angle**: read the WHOLE script against the angle's definition, not just the hook.
- Where a character exists: the voice gender-matches it, and every beat prompt carries `{LOCK}`/`{STYLE}` instead of repeating the text.
- The copy reads like a person talking, written for the band.
- On a child: the inherit list holds ONLY positions the change leaves honest (check it against the table in `references/changing-a-base.md`).

Then print the read-back for the operator: the ad narrated in time order, each beat's line, how it reaches the viewer (spoken / on-screen / said in the clip), and what's on screen while it plays; then the plain summary: who it is for · the angle · how it is told · the look · the voice · and on a child, what it inherits vs what it buys. On request, save this print as a markdown brief (a file the operator can hand to anyone).

**STOP. This is the approval gate. Nothing is written and nothing proceeds without the operator's explicit yes.** Offer a redirect: the whole arc, one line, a beat's visual, the tone.

### 9. LAND: one sweep, all the writes

Only after approval does the board get touched, in one sweep:

1. The registry upserts and links the settled picks need: `upsert-persona` / `upsert-pain` / `upsert-angle` / `upsert-mechanism`, then `link-persona-pain`, `link-pain-mechanism`.
2. `create-ad`: the whole ad in one call; either everything lands or nothing does. **A child is the same call plus three keys**: `parent` (the base's slug), `changeSet` (your honest label of what changes, in the board's vocabulary), and `inherit` (the positions reused from the parent at $0). You compose the COMPLETE child payload yourself: the base's script with your changes applied, full beats; the verb never diffs against the parent.
3. `estimate`: landing filed the ad's work order (the planned sheet rows); price it and report the number with the handoff. On a child, also report the inherited count from the create-ad response.

Registry writes land one by one; `create-ad` is the atomic call. If `create-ad` fails after the upserts, nothing needs undoing: the rows are settled, approved values, and the fixed retry links straight to them.

**The payload shape is not memorized here**: run `npm run ads -- describe create-ad` at landing time and compose against the live contract. The skill's steps taught you what everything MEANS (picks, fills, beats, prompts, parent, inherit); describe gives you the current syntax.

**Guard errors are written for you**: they name the missing slot, the illegal role, the unresolved slug, and what IS valid. Read the error, fix the call, retry; never work around a guard.

**EXPLODE offer (hooks):** bank several openers on the landed ad? Each is a child with `changeSet: ["copy"]`, the new hook `vo`, and an `inherit` list reusing every position the new opener leaves honest; each opener must hand cleanly into the fixed symptom line. Children cost nothing until produced.

## After landing

Edits while the ad is still an `idea` go through `update-ad` / `update-beat`, and `references/changing-a-base.md` is the law: script writes are yours to follow with `replan`, and `lint <slug>` is the net before production.

**Production never starts from this skill.** On approval and landing, print the literal next command for the human:

```
/ad-produce <slug>
```

## Gotchas

- **Never generate, never write files, never start ad-produce yourself.** Author and route.
- **A posted ad is immutable**; its children are the way forward.
- **A vehicle switch on a child re-checks the fills** against the new vehicle's checklist; the guard names anything missing or illegal, fix the fills in the same call.
