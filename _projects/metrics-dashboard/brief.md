---
created: 2026-09-07
updated: 2026-09-07
---
# Brief: BibleChat metrics dashboard, published page, refreshed monthly

You are building a published dashboard of BibleChat's business metrics that updates itself every month without anyone remembering to do it. Denis (product, delegates syntax to agents) asked for a published page. Read this whole file before acting.

## What exists already

- **Validated BigQuery queries**: `.claude/commands/unit-economics.md` in this repo. Five queries (normalized MRR/ARR, 13-month revenue trend, monthly spend/trials/payers/CPT/CPS, matured trial-to-paid, MAU) with the correctness rules written in. Run them through the `biblechat-analytics` MCP (`mcp__biblechat-analytics__execute_query`; load it with ToolSearch first). If that MCP is not connected in your session, stop and ask Denis to run `/mcp` and authenticate it; do not guess numbers.
- **Gotchas that break naive queries**: `/Users/dennisk/.claude/projects/-Users-dennisk-Documents-project---bib-content-gen/memory/project_mrr_method.md`. Read it. The two that matter most: `trial_started` events carry phantom revenue and must never be summed as revenue; `revenue_usd` is gross and `proceeds_usd` (~74% of gross) is cash after store fees, while `net_revenue_usd`/`tax_amount_usd` are unusable before July 2026.
- **The ground-truth doc** with the current numbers and their definitions: `_docs/core/01_biblechat-business-overview.md`. Do not rewrite it. You may add one line under its metrics section linking to the dashboard once published.
- **Return-curve tables** not in the command file: `bc-ads-tester.limited.cpt_master_daily` (iOS, per country per day; spend-weight everything: `SUM(metric*total_spend)/SUM(total_spend)`; its ROAS columns are GROSS; `predicted_roas_m1` equals `realized_roas_30d` once a day is 30+ days old) and `bc-ads-tester.limited.cpt_master_daily_regions_android` (use `row_type='overall'`). Month-1 return = gross revenue in the first 30 days over that month's spend. The projection model sets M12 at roughly 3.1x M1.

## The shape to build

**A published Artifact page backed by the artifact database.** The page holds no numbers in its code. It reads one document per month from the database and renders charts. A monthly job writes the new month's document. Load the `artifact-capabilities` skill (for the `db` capability contract, read the `.d.ts` it points to before writing any `claude.use("db")` code), then `artifact-design` and `dataviz` before writing the page. Inline SVG charts, no external libraries unless a CDN on the allowlist is genuinely needed. Theme-aware per the Artifact tool rules. Favicon on first publish.

**Database layout** (collection `months`, doc id `YYYY-MM`), fields per month:
- `revenue_gross`, `revenue_proceeds`, `revenue_ios_gross`, `revenue_android_gross` (recognized revenue that calendar month, phantom-trial excluded, refunds netted)
- `ad_spend`, `spend_facebook`, `spend_tiktok`, `spend_apple`, `spend_google`
- `trials`, `new_payers`, `direct_purchases`, `payers_ios`, `payers_android`, `cpt_blended`, `cps_blended`
- `m1_ios_gross`, `m1_android_gross` (measured, that month's spend), `m12_projected_ios`, `m12_projected_android`
- `trial_to_paid_ios`, `trial_to_paid_android` (matured cohort: trials started the 15th of the prior month to the 15th of this month)
- `mau` (device-level, `ga_events_staging` session_start, ~1.2 GB per month queried; optional for history, required for the latest month)
- `partial: true` on a month that is not yet complete
Collection `snapshots`, doc id `YYYY-MM-DD`: `active_subs`, `active_subs_committed`, `mrr_gross`, `mrr_proceeds`, `mrr_gross_committed`, `arr_gross`, `arr_proceeds`. Doc `meta/latest`: `{month, snapshot, refreshed_at, source: "biblechat-analytics MCP"}`.
Seed with the Artifact tool's `write_db` (`batch`), never by hardcoding rows in the page.

**Seed history**: revenue and spend from 2025-07 onward (revenue is cheap; spend and funnel per month come from the command's Query 3 with the month window moved; M1 from cpt_master_daily from 2025-07 onward in one query grouped by month). Snapshots: run Query 1 once now for today's date. Two earlier snapshots are known and may be seeded by hand: 2026-08-16 (184,621 subs; committed 138,835; MRR gross 2,281,429; proceeds 1,705,089; committed gross 2,051,136) and 2026-09-07 is what Query 1 returns today.

**Charts**, in this order:
1. Monthly revenue, gross and proceeds, with the current month drawn as partial.
2. Spend vs trials by month, with CPT as a line. This is where August 2026 should visibly read as a spike, not a new level.
3. Month-1 return by month, iOS and Android, with a reference line at 32% (the M1 level that projects to the 100% M12 rule) and a note that it is gross.
4. Trial-to-paid by platform by month.
5. Stat tiles for the latest snapshot: MRR gross, MRR cash, committed floor, active subs, ARR, with the snapshot date. Every money tile says gross or cash.
Each chart states its window and source table in small text. A freshness line at the top from `meta/latest`. Empty-state if the database is unreachable (`claude.use("db")` resolved null).

## The monthly refresh

Create an Orca automation (`orca skills get orca-cli` for the exact commands; the app is running) that runs a Claude session **in this workspace** on the 2nd of every month at 09:00, provider `claude`, `--workspace` this worktree with `--fresh-session`. Its prompt must be self-contained for a fresh agent: read `_projects/metrics-dashboard/README.md`, run the unit-economics queries for the previous calendar month plus Query 1 for today, write the `months` doc, the `snapshots` doc and `meta/latest` via `write_db` to the artifact URL recorded in the README, then update the two-column metrics table in `_docs/core/01_biblechat-business-overview.md` so the doc and dashboard never disagree, bumping its `updated` date. Create the automation `--disabled`, run it once by hand with `orca automations run` to prove the loop works end to end, then enable it. If the automation's session cannot reach the analytics MCP, say so in the README as the known limitation and leave the manual fallback (running the same prompt in a Claude session here) documented.

## Deliverables

- The published artifact URL.
- `_projects/metrics-dashboard/README.md` (with `created`/`updated` frontmatter): what the dashboard shows, the database layout, the artifact URL, the automation id and schedule, how to refresh by hand, and the known limitations. Written for a fresh agent with zero history: describe the system as it is, no change log.
- The page source kept in `_projects/metrics-dashboard/dashboard.html` so it can be republished to the same URL.
- Update the Orca worktree comment at checkpoints (`orca worktree set --worktree active --comment "..." --json`) and set workspace status `in-review` when done. Denis is not watching live; leave everything he needs in the README.

## Constraints

- BigQuery is read-only; keep every query partition-filtered and column-pruned (per-person daily quota).
- Do not commit to git. Do not edit files outside `_projects/metrics-dashboard/`, the artifact database, and the one permitted line in the overview doc.
- No em dashes anywhere. Docs carry `created`/`updated` frontmatter.
- Never publish a page that hardcodes the observed numbers as sample data.
- If a query result contradicts the ground-truth doc by more than 10%, do not silently pick one: write both to the README under "discrepancies" and continue.
