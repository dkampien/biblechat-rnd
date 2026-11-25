---
created: 2026-08-12
updated: 2026-08-12
---

# Ad Systems Context

Orientation for anyone (human or agent) working on BibleChat's AI ad systems. Covers the company context, the systems as they stand, why past builds failed, the working knowledge about performance creative, and the current goal and objectives. History is confined to the post-mortem section; everything else describes the system as it is now.

## 1. Company and org context

BibleChat is a consumer mobile app: faith-shaped mental health for Christians. Users come with a life problem (marriage, anxiety, grief, guilt) and the app offers scripture-grounded help. Monetization is subscription via trial. All marketing focuses on a single feature: the daily plan, a personalized day-by-day plan built around the user's problem.

Unit economics: blended CPT around $16, CPS around $36, month-12 return around 111.7%. The company objective is to scale marketing spend at acceptable ROAS. Because the creative determines which audience Meta finds, spend capacity scales with the number of distinct working creatives, not with variant counts of one creative. Creative diversity is spend capacity.

The creative org: an internal team of roughly 6 people ships about 10 ads per day. A creative strategist writes briefs (persona, problem, angle, format), informed by 1-2 performance people who track campaigns. Media buyers run the Meta account and hold launch and kill decisions. Nobody in the org can predict whether an ad will win; winners are found through volume plus the feedback loop (metrics inform briefs, briefs inform ads, ads produce metrics).

Infrastructure and assets:

- adloops: the internal platform for posting ads to Meta and reading results.
- VoC corpus: verbatim user problems mined from onboarding free text of users who paid and were retained; the curated map lives in the auto-ads-loop repo (`data/problems.json`). Currently 60 problems: 53 candidates in ranked tiers plus a 7-problem explore tier that carries objective B's rule natively (~1 probe slot in 4, a probe promotes or erases). Each problem has verbatim evidence quotes, stats (users, revenue, 35+ share), and priors including payer_intensity (cheapness) and image_legibility (can one glance communicate this pain). Problems contain framings (mined pain phrasings with counts; historically miscalled "angles", a different thing from the ad model's lens-angle). This is validated demand language, the strongest marketing asset available. New problems keep arriving through the funnel; re-mining is a periodic chore, not a runtime activity.

## 2. The AI systems as they stand

Two systems, consolidated from three builds, owned by the AI automation role. They are two partial builds of the same machine, entered from different doors.

- **cloops-ads**: video ad production. Its backbone is the ad model, a self-built decomposition framework that describes an ad as structured components. It can produce many iterations within one format, but each new format must be designed by hand. Uses Airtable as its board. Output tends toward a polished look.
- **auto-ads-loops**: image-probe system, mid-build. Uses a lighter ad model adapted for statics: persona is skipped (the problem implies it), and the mold is one named format fusing layout and framework. Intended cadence: design an experiment, fix a format (mold), an LLM pours copy into it, HTML/CSS composition plus diffusion illustrations produce the image, post via adloops, collect Meta metrics into a ledger. A first feedback loop was closed once; data existed but nobody knew how to act on it, which identified the missing piece as an interpretation playbook (metric pattern to diagnosis to allowed change), not more infrastructure.
- **The ledger**: the unifying artifact of both systems. One flat table, one row per ad: the ad-model coordinates of what was made, plus launch facts, plus metrics. Probes run the web route (ad to quiz landing page, pixel+CAPI, real per-ad counting), so the diagnostic chain for statics is CPM, link CTR, link CPC, landing-page view rate, cost per registration, with CPT a nullable rollup that fills only at real spend (no trial event exists in the account; installs/CPI are app-route modeled numbers and stay out of probe verdicts). Context and validity columns: spend, impressions, days live, frequency, adset id, impression share plus a starved flag (under ~20% share within its adset or under 100 impressions means unreadable, rerun, never a loser), metrics-as-of date (conversions backfill 24-48h), attribution setting. Joined to Meta by meta_ad_id (name matching only as contains, adloops appends suffixes). Rule: any column that never changes a decision gets deleted.
- **The ad model**: pending structural review. Its job description: serve as the ledger's coordinate system and as the decomposition language for sweeps and diagnoses.

## 3. Post-mortem: why three builds produced no winners (history)

Three systems were built from different production angles and failed the same way. The diagnosis, established through a long structured interview, is five failure layers plus three root causes.

Failure layers:

1. **Format intake.** The systems could vary within a format but not originate formats, and every build stalled at "the initial format." Formats are harvested from platform culture and competitor winners, not invented; no harvest process existed, and the operator (not a native consumer of the content culture) was the component least suited to originate them.
2. **Product info gap.** Neither operator nor systems knew the product mechanism concretely (what the daily plan does on day 1, 3, 7 for a specific pain), so pain-to-feature bridges came out as vague promises, which is what skeptical audiences scroll past.
3. **Copy slop.** LLMs asked to originate scripts from nothing produce generic copy regardless of framework (AIDA, PAS). The working regime is transposition from proven exemplars plus vocabulary grounded in users' verbatim words, which required assets (harvested skeletons, the VoC corpus wired in) that did not exist yet.
4. **Asset polish.** AI assets converge to a polished look, while the market often rewards unpolished, native-looking content: polish pattern-matches to "ad" and gets scrolled. The production bar being aimed at was above the target.
5. **Feedback visibility.** Creatives were handed to the media buyers and the only signal back was "didn't perform": one bit, no per-stage metrics, no per-creative spend visibility. Nothing was learned per failure, across all three builds. Compounded by metric illiteracy at the time (inability to interpret CPT or funnel data), which also kept the account's own winners unstudied.

Root causes:

- All creative layers were fused into one "make an ad" step, so every layer's weakness compounded in the output.
- The systems ran outside the org's learn loop (metrics, briefs, make, test, learn), consuming the strategist's briefs only informally, and competed on production, the org's strongest existing capability.
- Three principals' goals were fused into one system without being named: the CEO wanted cheap problems found from the VoC, the CTO wanted a self-improving creative loop proven, the builder wanted the decomposition thesis validated. Each has a different success bar and budget.

## 4. Creative ops: how performance creative actually works

- **The layer stack.** Insight, then concept/angle, then hook, then format, then treatment, then script. The script is written last, into the chosen mold. An ad is a point in this space.
- **The hook is a first-class object**, separate from the script. It is multimodal (visual, overlay, spoken line, sound), judged by hook rate, and banked and swapped independently of ad bodies. The hook is a promise; the script is the keeping of it.
- **Decay rates differ per layer.** Insights barely expire, concepts last months, formats last a season, treatments expire in weeks (example: notes-app and text-message statics stopped converting by August 2026). Any harvest must therefore be a continuous feed, not a one-time library.
- **Formats are harvested, not invented**: from platform-native content and competitors' long-running ads. Big consumer app teams work concept-first, pour each concept into 2-3 proven molds from a maintained library, and budget roughly 70% iterations on winners, 20% new concepts in proven molds, 10% wild swings.
- **Anti-slop copy doctrine**: transpose proven skeletons instead of originating; ground vocabulary in the users' own words; overgenerate and select with concrete criteria (spoken register, no abstract nouns, would a person say this out loud).
- **Naming convention**: encode concept, format, and hook in every ad name so wins are attributable to a layer.

## 5. Goal and objectives (auto-ads-loops)

**Goal:** increase the supply of winning creatives: more distinct ads that acquire trials at or below target CPT, so spend can scale. Lower blended CPT is a byproduct, not the goal.

**Strategy (a falsifiable bet, deliberately kept out of the goal):** decomposition plus controlled variation over the ad-model space, with the ledger as memory. If the strategy underperforms the dumb baseline (high-volume harvest-and-clone), the goal stands and the strategy gets replaced.

**Objectives:**

- **A. Validate and rank the proven problems.** Sweep the 53 payer-proven pains as image ads to strangers (normal prospecting delivery), all other ad variables locked. Output: one table showing which problems move strangers at all (validation, threshold read) and which respond cheapest (ranking read, the double-down list).
- **B. Promote long-tail funnel problems.** Same instrument for pains with thin payer evidence (few or single mentions). Capped at roughly 1 probe in 4, never displacing A. Winners graduate into A's table.
- **C. Learn which ad-model variables matter to Meta** (standing mission, no finish line). As the ledger accumulates, read which axes move CPM, CTR, and cost. The output is a live, local, decaying map, never a fixed table of laws.
- **D. Close one honest improvement loop.** Metrics name the leaking element, one axis changes, the child beats the parent on that named metric. Requires the interpretation playbook first. Success is defined at proxy-metric level.

**Out of scope:** discovering problems with no funnel evidence (dropped for scope; re-openable later). New problems enter only via periodic VoC re-mining. Recorded constraint: targeting starts at 35+.

**Sequence:** A starts (needs only a stolen constant mold and the ledger schema), B rides along inside every sweep, D fires after the first sweep flags something leaky, C accumulates silently throughout.

## 6. Known risks of the strategy

1. Meta is not a fair test bench: delivery is allocated endogenously, so naive comparisons measure delivery luck as much as creative causality. Clean reads need forced splits or must be treated as directional.
2. Knobs are compound: changing "the problem" changes hook, copy, maybe imagery. The ledger records bundles; templates keep bundles uniform.
3. No stable global importance ranking exists: axis effects interact and decay. C's deliverable is a live map, and drift is the product working, not failing.
4. Statistical cost: at $16 CPT, conversion-level significance per probe cell is expensive. Relative reads on CPM/CTR are trustworthy long before absolute CPT claims. Per-cell budget math must be computed before sizing a sweep.
5. Component knowledge is perishable: even clean attribution results age out within seasons, which caps what learning them is worth.
6. The dumb baseline is strong: volume harvest-and-clone with no component science is roughly what the winning internal team does. The strategy must beat it on winners per dollar.
7. Meta-caveat: the strategy is the builder's own invention, which is the condition under which disconfirming evidence gets explained away. The goal is method-agnostic precisely so the strategy can lose without the project losing.
