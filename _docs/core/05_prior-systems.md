---
created: 2026-08-17
updated: 2026-08-17
---
# Prior Systems

What was built before, what each was for, and what the attempts taught. History, bounded to this doc; the current direction lives in 04.

## The systems

**cloops-ads** (repo: `project - cloops-ads`). Video ad production. Backbone is the ad model: a self-built decomposition framework where an ad = eight picks (persona, pain, mechanism, angle, vehicle, framework, format, length) drawn from curated registries, plus execution slots and a script in beats. Variation vs iteration is read off a declared changeSet; ads harden as they age (idea, produced, posted). It can produce many iterations within one format, but every new format must be designed by hand. Uses Airtable as its board. Status: works, overengineered by its own author's judgment, parked pending simplification.

**auto-ads-loops** (repo: `project - auto-ads-loop`). Image-probe experiment system. Born from two asks: the CEO's (mine the voice-of-customer tool for user pains, probe them with cheap image ads, find the cheap problems and double down) and the CTO's (prove a self-improving creative loop: Meta metrics name an ad's weak element, the system changes that one thing, the child beats the parent). Its objectives, as last settled: (A) validate and rank the payer-proven problems by sweeping them as statics with everything else locked; (B) same sweep for thin-evidence long-tail problems on a capped explore slice; (C) as a standing mission, accumulate which ad-model variables move CPM, CTR, and cost; (D) close one honest improvement loop at proxy-metric level. Status: mid-build. A first experiment (16-problem sweep, format phone-story-v1, $320 cap) was fully designed but never launched; posting and metrics ingestion were never wired.

**Consolidation note:** these are two partial builds of one machine, entered from different doors (video with the full ad model, images with a lite version).

## Reusable assets that survive any reset

- The problem map (`auto-ads-loop/data/problems.json`): 60 problems mined from onboarding free text of paying retained users, with verbatim quotes, framings (pain phrasings with counts), ranked tiers, an explore tier, and priors including image legibility. The strongest marketing asset in the building.
- The ledger schema and `ads` CLI (auto-ads-loop): one row per ad with full coordinates, lineage, and a typed metrics contract; walls that refuse out-of-order operations.
- The ad model doc (cloops-ads `_docs/core-docs/ad-model_v5.md`) as a coordinate system and decomposition language.
- One registered static format (`phone-story-v1`) and the render/fit-check pipeline.
- The core docs (this `_docs/core/` set).

## What the attempts taught

- Five failure layers, one per creative layer: format intake (systems vary within a format but can't originate formats; every build stalled at "the initial format"; formats are harvested from platform culture and competitor winners, not invented), product knowledge (nobody had written down what the daily plan concretely does, so ads made vague promises), copy (LLMs originating from nothing produce slop; the working regime is transposition from proven examples plus the users' own words), asset polish (AI output trends polished while unpolished often wins), and feedback (creatives went to the media buyers and came back as "didn't perform", one bit, nothing learned per death).
- Three principals' goals were fused into one system without being named (CEO: cheap problems; CTO: self-improving loop; builder: the decomposition thesis). Each has a different success bar and budget; unnamed, they produced months of aimless architecture.
- The systems ran outside the org's learn loop (metrics inform briefs, briefs inform ads) and competed with the internal team's strength, production, instead of adding what it lacks.
- The org's winning method is volume search: ~10 ads/day, nobody can predict a winner, the feedback loop finds them. Any new system must either feed that loop or run its own honest version of it.

## Known risks of the decomposition strategy

The prior systems bet on breaking ads into parts and testing the parts. The bet was never disproven, but six things were learned that any future version of it must respect:

1. Meta doesn't run fair tests. It chooses which ads get shown, so when ad A beats ad B, part of that is just Meta's choice. Either force an even split, or treat results as hints, not verdicts.
2. You can't change just one thing. Change the problem an ad targets and the words and image change with it. Write down everything that changed, not just the thing you meant to change.
3. There's no permanent answer to "which part matters most." It shifts with context and time. Keep a running picture, don't expect fixed rules.
4. Certainty is expensive. At ~$16 per trial, proving something at the trial level costs real money. Cheap early signals (CPM, CTR) are good for comparing ads against each other long before the money metrics can be trusted.
5. Whatever you learn expires. Even a clean finding stops being true within a season. Don't overpay for knowledge with a short shelf life.
6. The boring alternative is strong. Copy proven ads, make lots of them, keep what works: that's roughly what the winning internal team does, with no theory at all. Any smarter system has to beat that on winners per dollar, not on elegance.
