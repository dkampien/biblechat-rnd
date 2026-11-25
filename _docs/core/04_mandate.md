---
created: 2026-08-17
updated: 2026-09-14
---
# Mandate

What Denis is trying to do, and the constraints any system he builds must respect. Facts about the world live in 01-03; this doc is decisions. Objectives get added once the current system's shape is chosen.

## Goal

Increase the supply of winning ads: distinct creatives that acquire trials at a cost the economics can carry, so the company can scale spend. The goal is method-agnostic on purpose: systems, pipelines, and theses are bets placed against it, and a bet can lose without the goal changing.

## Standing constraints

- The economics floor: every month's spend must project at least 100% gross month-12 return; the team steers daily by CPT (values and definitions in 01).
- Winners already exist: an internal team ships ~10 ads/day. An AI lane earns its seat by adding what that team lacks (variety, speed, cheapness per concept), not by duplicating its production.
- Access: media buyers control launch, kill, and budgets. Denis has read access to the app-route ad account (Basmo IOS) only; the WEB account is out of reach. Anything requiring spend or the web funnel needs cooperation, not just code.
- Ground truths are binding: no system may contradict docs 01-03. When reality disagrees with them, fix the doc first, then the system.

## Objectives (placeholder, pending calibration)

Not set yet. Two things are still open: the route (app via the Basmo account, or web via the quiz funnels; leverage favors web, access favors app, and the web numbers and WEB account access that would settle it are pending), and the calibration data, which does not exist until the first ads have run for 4 to 6 weeks.

When that data exists, fill this section from the capacity formula:

capacity = ads launched per month (capped by the buyers' testing slots) × hit rate (borrow the internal team's from the Basmo account until measured) × spend a winner absorbs at or under target CPT

Set the share against the gap (capacity the plan needs minus what the internal team supplies), not against the total. A winner is an ad that absorbs real spend at or under target CPT, never above the ceiling. Per-ad visibility ends at trial start, so measure in spend at CPT and report MRR only as a derived estimate.

Three inputs to pull from the Basmo account first: the team's hit rate, the spend distribution of winning ads, the buyers' weekly testing slots.
